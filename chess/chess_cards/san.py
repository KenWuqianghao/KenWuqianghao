"""Minimal, dependency-free chess move replayer.

Replays Standard Algebraic Notation (SAN) move lists on a board and emits FEN.
Handles piece disambiguation, pins (via legality filtering), en passant,
castling rights, promotions, and the halfmove / fullmove clocks.

Validated against thousands of real Chess.com games whose final FEN is known
(see tests/test_san.py).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

FILES = "abcdefgh"
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

_SAN_RE = re.compile(
    r"^(?P<piece>[KQRBN])?(?P<from_file>[a-h])?(?P<from_rank>[1-8])?"
    r"(?P<capture>x)?(?P<to>[a-h][1-8])(?:=?(?P<promo>[QRBN]))?$"
)

KNIGHT_DELTAS = ((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2))
KING_DELTAS = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
ROOK_DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
BISHOP_DIRS = ((1, 1), (1, -1), (-1, 1), (-1, -1))


class IllegalMove(ValueError):
    """Raised when a SAN token cannot be matched to exactly one legal move."""


def sq(file: int, rank: int) -> int:
    """0-based file/rank -> square index (a1 = 0, h8 = 63)."""
    return rank * 8 + file


def sq_name(index: int) -> str:
    return FILES[index % 8] + str(index // 8 + 1)


def parse_sq(name: str) -> int:
    return sq(FILES.index(name[0]), int(name[1]) - 1)


@dataclass
class Board:
    squares: list = field(default_factory=lambda: [None] * 64)
    white_to_move: bool = True
    castling: set = field(default_factory=lambda: set("KQkq"))
    ep: int | None = None
    halfmove: int = 0
    fullmove: int = 1
    last_move: tuple | None = None  # (from_index, to_index) of the last move applied

    # ----------------------------------------------------------------- setup
    @classmethod
    def from_fen(cls, fen: str = START_FEN) -> "Board":
        parts = fen.split()
        b = cls()
        rank = 7
        file = 0
        for ch in parts[0]:
            if ch == "/":
                rank -= 1
                file = 0
            elif ch.isdigit():
                file += int(ch)
            else:
                b.squares[sq(file, rank)] = ch
                file += 1
        b.white_to_move = parts[1] == "w" if len(parts) > 1 else True
        b.castling = set(parts[2]) - {"-"} if len(parts) > 2 else set("KQkq")
        b.ep = parse_sq(parts[3]) if len(parts) > 3 and parts[3] != "-" else None
        b.halfmove = int(parts[4]) if len(parts) > 4 else 0
        b.fullmove = int(parts[5]) if len(parts) > 5 else 1
        return b

    def fen(self) -> str:
        rows = []
        for rank in range(7, -1, -1):
            row, empty = "", 0
            for file in range(8):
                p = self.squares[sq(file, rank)]
                if p is None:
                    empty += 1
                else:
                    if empty:
                        row += str(empty)
                        empty = 0
                    row += p
            if empty:
                row += str(empty)
            rows.append(row)
        castling = "".join(c for c in "KQkq" if c in self.castling) or "-"
        ep = sq_name(self.ep) if self.ep is not None else "-"
        return " ".join(
            ["/".join(rows), "w" if self.white_to_move else "b", castling, ep,
             str(self.halfmove), str(self.fullmove)]
        )

    def copy(self) -> "Board":
        return Board(list(self.squares), self.white_to_move, set(self.castling),
                     self.ep, self.halfmove, self.fullmove, self.last_move)

    # -------------------------------------------------------------- geometry
    def _is_white(self, piece: str) -> bool:
        return piece.isupper()

    def king_square(self, white: bool) -> int:
        target = "K" if white else "k"
        return self.squares.index(target)

    def attacked_by(self, index: int, by_white: bool) -> bool:
        """Is `index` attacked by any piece of colour `by_white`?"""
        f, r = index % 8, index // 8
        own = str.isupper if by_white else str.islower
        # pawns
        pawn_rank = r - 1 if by_white else r + 1
        if 0 <= pawn_rank < 8:
            for df in (-1, 1):
                if 0 <= f + df < 8:
                    p = self.squares[sq(f + df, pawn_rank)]
                    if p and own(p) and p.upper() == "P":
                        return True
        # knights
        for df, dr in KNIGHT_DELTAS:
            nf, nr = f + df, r + dr
            if 0 <= nf < 8 and 0 <= nr < 8:
                p = self.squares[sq(nf, nr)]
                if p and own(p) and p.upper() == "N":
                    return True
        # king
        for df, dr in KING_DELTAS:
            nf, nr = f + df, r + dr
            if 0 <= nf < 8 and 0 <= nr < 8:
                p = self.squares[sq(nf, nr)]
                if p and own(p) and p.upper() == "K":
                    return True
        # sliders
        for dirs, kinds in ((ROOK_DIRS, "RQ"), (BISHOP_DIRS, "BQ")):
            for df, dr in dirs:
                nf, nr = f + df, r + dr
                while 0 <= nf < 8 and 0 <= nr < 8:
                    p = self.squares[sq(nf, nr)]
                    if p:
                        if own(p) and p.upper() in kinds:
                            return True
                        break
                    nf += df
                    nr += dr
        return False

    def in_check(self, white: bool) -> bool:
        return self.attacked_by(self.king_square(white), not white)

    def _pseudo_targets(self, index: int) -> list[int]:
        """Squares a piece on `index` could move to, ignoring king safety."""
        p = self.squares[index]
        white = self._is_white(p)
        f, r = index % 8, index // 8
        out: list[int] = []

        def friendly(i: int) -> bool:
            q = self.squares[i]
            return q is not None and self._is_white(q) == white

        kind = p.upper()
        if kind == "P":
            step = 1 if white else -1
            start_rank = 1 if white else 6
            one = sq(f, r + step) if 0 <= r + step < 8 else None
            if one is not None and self.squares[one] is None:
                out.append(one)
                two = sq(f, r + 2 * step)
                if r == start_rank and self.squares[two] is None:
                    out.append(two)
            for df in (-1, 1):
                nf, nr = f + df, r + step
                if 0 <= nf < 8 and 0 <= nr < 8:
                    i = sq(nf, nr)
                    q = self.squares[i]
                    if (q is not None and not friendly(i)) or i == self.ep:
                        out.append(i)
            return out
        if kind == "N" or kind == "K":
            deltas = KNIGHT_DELTAS if kind == "N" else KING_DELTAS
            for df, dr in deltas:
                nf, nr = f + df, r + dr
                if 0 <= nf < 8 and 0 <= nr < 8 and not friendly(sq(nf, nr)):
                    out.append(sq(nf, nr))
            return out
        dirs = ROOK_DIRS if kind == "R" else BISHOP_DIRS if kind == "B" else ROOK_DIRS + BISHOP_DIRS
        for df, dr in dirs:
            nf, nr = f + df, r + dr
            while 0 <= nf < 8 and 0 <= nr < 8:
                i = sq(nf, nr)
                if self.squares[i] is None:
                    out.append(i)
                else:
                    if not friendly(i):
                        out.append(i)
                    break
                nf += df
                nr += dr
        return out

    # ----------------------------------------------------------------- moves
    def _apply(self, frm: int, to: int, promo: str | None = None) -> None:
        """Apply a (pseudo-legal) move in place, maintaining all state."""
        piece = self.squares[frm]
        white = self._is_white(piece)
        captured = self.squares[to]
        kind = piece.upper()
        is_pawn = kind == "P"

        # en passant capture: remove the pawn behind the target square
        if is_pawn and to == self.ep and captured is None:
            self.squares[to - 8 if white else to + 8] = None
            captured = "p"

        self.squares[to] = piece
        self.squares[frm] = None

        if promo:
            self.squares[to] = promo if white else promo.lower()

        # castling: also move the rook
        if kind == "K" and abs(to - frm) == 2:
            rank_base = 0 if white else 56
            if to > frm:  # king side
                self.squares[rank_base + 5] = self.squares[rank_base + 7]
                self.squares[rank_base + 7] = None
            else:
                self.squares[rank_base + 3] = self.squares[rank_base + 0]
                self.squares[rank_base + 0] = None

        # castling rights
        if kind == "K":
            self.castling -= {"K", "Q"} if white else {"k", "q"}
        for s, right in ((0, "Q"), (7, "K"), (56, "q"), (63, "k")):
            if frm == s or to == s:
                self.castling.discard(right)

        # en passant target
        self.ep = None
        if is_pawn and abs(to - frm) == 16:
            self.ep = (frm + to) // 2

        self.halfmove = 0 if (is_pawn or captured is not None) else self.halfmove + 1
        if not white:
            self.fullmove += 1
        self.white_to_move = not white
        self.last_move = (frm, to)

    def legal_from_squares(self, kind: str, to: int, white: bool,
                           promo: str | None = None) -> list[int]:
        """All origin squares from which a `kind` piece can legally reach `to`."""
        target_piece = kind if white else kind.lower()
        result = []
        for i, p in enumerate(self.squares):
            if p != target_piece:
                continue
            if to not in self._pseudo_targets(i):
                continue
            trial = self.copy()
            trial._apply(i, to, promo)
            if not trial.in_check(white):
                result.append(i)
        return result

    def push_san(self, san: str) -> None:
        token = san.rstrip("+#!?").replace("0", "O")
        white = self.white_to_move
        if token in ("O-O", "O-O-O"):
            self._castle(token == "O-O", white)
            return
        m = _SAN_RE.match(token)
        if not m:
            raise IllegalMove(f"cannot parse SAN token {san!r}")
        kind = m.group("piece") or "P"
        to = parse_sq(m.group("to"))
        promo = m.group("promo")
        candidates = self.legal_from_squares(kind, to, white, promo)
        if m.group("from_file"):
            ff = FILES.index(m.group("from_file"))
            candidates = [c for c in candidates if c % 8 == ff]
        if m.group("from_rank"):
            fr = int(m.group("from_rank")) - 1
            candidates = [c for c in candidates if c // 8 == fr]
        if kind == "P" and not m.group("capture"):
            candidates = [c for c in candidates if c % 8 == to % 8]
        if len(candidates) != 1:
            raise IllegalMove(
                f"{san!r} matches {len(candidates)} pieces on {self.fen()}"
            )
        self._apply(candidates[0], to, promo)

    def _castle(self, kingside: bool, white: bool) -> None:
        base = 0 if white else 56
        king_from = base + 4
        right = ("K" if kingside else "Q") if white else ("k" if kingside else "q")
        if right not in self.castling:
            raise IllegalMove(f"no {right} castling right on {self.fen()}")
        path = (base + 5, base + 6) if kingside else (base + 3, base + 2, base + 1)
        if any(self.squares[s] is not None for s in path):
            raise IllegalMove("castling path blocked")
        king_to = base + 6 if kingside else base + 2
        transit = (king_from, base + 5, base + 6) if kingside else (king_from, base + 3, base + 2)
        if any(self.attacked_by(s, not white) for s in transit):
            raise IllegalMove("castling through check")
        self._apply(king_from, king_to)


def replay(moves: str | list[str], start: str = START_FEN) -> Board:
    """Replay SAN moves (space-separated string or list) from `start`."""
    if isinstance(moves, str):
        moves = moves.split()
    b = Board.from_fen(start)
    for mv in moves:
        b.push_san(mv)
    return b


_PGN_MOVE_NUMBER = re.compile(r"\d+\.(\.\.)?")
_PGN_COMMENT = re.compile(r"\{[^}]*\}")
_PGN_VARIATION = re.compile(r"\([^()]*\)")


def pgn_moves(pgn: str) -> list[str]:
    """Extract the SAN move tokens from a PGN body (headers, clocks, results stripped)."""
    body = "\n".join(line for line in pgn.splitlines() if not line.startswith("["))
    body = _PGN_COMMENT.sub(" ", body)
    while _PGN_VARIATION.search(body):
        body = _PGN_VARIATION.sub(" ", body)
    body = _PGN_MOVE_NUMBER.sub(" ", body)
    body = body.replace(";", " ")
    tokens = []
    for tok in body.split():
        if tok in ("1-0", "0-1", "1/2-1/2", "*"):
            continue
        if tok.startswith("$"):
            continue
        tokens.append(tok)
    return tokens


def pgn_headers(pgn: str) -> dict[str, str]:
    return dict(re.findall(r'^\[(\w+) "([^"]*)"\]', pgn, flags=re.M))
