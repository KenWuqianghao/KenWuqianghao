"""Legal move generation and a forced-mate searcher on top of san.Board.

`mate_in(board, n)` returns the first move of a forced mate in at most `n`
moves for the side to move, or None. It is a plain depth-first proof search
with check-first move ordering: at the last ply only checking moves are tried,
because nothing else can deliver mate. Validated against Lichess mateIn1/2/3
puzzles in tests/test_search.py.
"""
from __future__ import annotations

import time
from dataclasses import dataclass

from .san import FILES, Board, sq_name


@dataclass(frozen=True)
class Move:
    frm: int
    to: int
    promo: str | None = None

    @property
    def uci(self) -> str:
        return sq_name(self.frm) + sq_name(self.to) + (self.promo.lower() if self.promo else "")

    @classmethod
    def from_uci(cls, s: str) -> "Move":
        f = FILES.index(s[0]) + (int(s[1]) - 1) * 8
        t = FILES.index(s[2]) + (int(s[3]) - 1) * 8
        return cls(f, t, s[4].upper() if len(s) > 4 else None)


def _castling_moves(b: Board, white: bool) -> list[Move]:
    base = 0 if white else 56
    king = base + 4
    if b.squares[king] != ("K" if white else "k"):
        return []
    out = []
    for right, path, transit, to in (
        ("K" if white else "k", (base + 5, base + 6), (king, base + 5, base + 6), base + 6),
        ("Q" if white else "q", (base + 3, base + 2, base + 1), (king, base + 3, base + 2), base + 2),
    ):
        if right not in b.castling:
            continue
        if any(b.squares[s] is not None for s in path):
            continue
        if any(b.attacked_by(s, not white) for s in transit):
            continue
        out.append(Move(king, to))
    return out


def apply(b: Board, m: Move) -> Board:
    child = b.copy()
    child._apply(m.frm, m.to, m.promo)
    return child


def legal_moves(b: Board) -> list[Move]:
    white = b.white_to_move
    own = str.isupper if white else str.islower
    out: list[Move] = []
    for i, p in enumerate(b.squares):
        if p is None or not own(p):
            continue
        promo_rank = 7 if white else 0
        for to in b._pseudo_targets(i):
            if b.squares[to] in ("K", "k"):  # only reachable from an illegal position
                continue
            if p.upper() == "P" and to // 8 == promo_rank:
                cands = [Move(i, to, pr) for pr in "QNRB"]
            else:
                cands = [Move(i, to)]
            for m in cands:
                child = b.copy()
                child._apply(m.frm, m.to, m.promo)
                if not child.in_check(white):
                    out.append(m)
    out.extend(_castling_moves(b, white))
    return out


def is_checkmate(b: Board) -> bool:
    return b.in_check(b.white_to_move) and not legal_moves(b)


def is_stalemate(b: Board) -> bool:
    return not b.in_check(b.white_to_move) and not legal_moves(b)


def _ordered(b: Board, moves: list[Move], checks_only: bool) -> list[tuple[Move, Board]]:
    """Pair moves with child boards, checks first, then captures, then the rest."""
    scored = []
    for m in moves:
        child = apply(b, m)
        gives_check = child.in_check(child.white_to_move)
        if checks_only and not gives_check:
            continue
        capture = b.squares[m.to] is not None or (b.squares[m.frm].upper() == "P" and m.to == b.ep)
        scored.append((0 if gives_check else 1, 0 if capture else 1, m, child))
    scored.sort(key=lambda t: (t[0], t[1]))
    return [(m, c) for _, _, m, c in scored]


class Budget:
    def __init__(self, seconds: float | None = None):
        self.deadline = time.monotonic() + seconds if seconds else None
        self.nodes = 0

    def tick(self) -> None:
        self.nodes += 1
        if self.deadline and self.nodes % 256 == 0 and time.monotonic() > self.deadline:
            raise TimeoutError("mate search budget exhausted")


def mate_in(b: Board, n: int, budget: Budget | None = None) -> Move | None:
    """First move of a forced mate in <= n moves for the side to move, else None."""
    budget = budget or Budget()
    return _attack(b, n, budget)


def _attack(b: Board, n: int, budget: Budget) -> Move | None:
    budget.tick()
    for m, child in _ordered(b, legal_moves(b), checks_only=(n == 1)):
        if is_checkmate(child):
            return m
        if n > 1 and _defend(child, n - 1, budget):
            return m
    return None


def _defend(b: Board, n: int, budget: Budget) -> bool:
    """True if every legal reply for the side to move still allows mate in n."""
    budget.tick()
    replies = legal_moves(b)
    if not replies:
        return False  # stalemate (checkmate was already handled by the caller)
    for r in replies:
        child = apply(b, r)
        if _attack(child, n, budget) is None:
            return False
    return True


def mate_line(b: Board, n: int, budget: Budget | None = None) -> list[Move]:
    """Principal line of a forced mate found by `mate_in` (attacker moves + one
    defender reply each ply, following the defender's first legal reply)."""
    budget = budget or Budget()
    line: list[Move] = []
    cur = b
    depth = n
    while depth > 0:
        m = _attack(cur, depth, budget)
        if m is None:
            break
        line.append(m)
        cur = apply(cur, m)
        if is_checkmate(cur):
            break
        reply = legal_moves(cur)[0]
        line.append(reply)
        cur = apply(cur, reply)
        depth -= 1
    return line


def san(b: Board, m: Move) -> str:
    """SAN for a legal move on `b` (with disambiguation and +/# suffix)."""
    piece = b.squares[m.frm]
    kind = piece.upper()
    child = apply(b, m)
    suffix = "#" if is_checkmate(child) else ("+" if child.in_check(child.white_to_move) else "")
    if kind == "K" and abs(m.to - m.frm) == 2:
        return ("O-O" if m.to > m.frm else "O-O-O") + suffix
    capture = b.squares[m.to] is not None or (kind == "P" and m.to == b.ep)
    dest = sq_name(m.to)
    if kind == "P":
        s = (sq_name(m.frm)[0] + "x" if capture else "") + dest
        if m.promo:
            s += "=" + m.promo
        return s + suffix
    others = [x for x in legal_moves(b) if x.to == m.to and x.frm != m.frm and b.squares[x.frm] == piece]
    dis = ""
    if others:
        same_file = any(o.frm % 8 == m.frm % 8 for o in others)
        same_rank = any(o.frm // 8 == m.frm // 8 for o in others)
        if not same_file:
            dis = sq_name(m.frm)[0]
        elif not same_rank:
            dis = sq_name(m.frm)[1]
        else:
            dis = sq_name(m.frm)
    return kind + dis + ("x" if capture else "") + dest + suffix
