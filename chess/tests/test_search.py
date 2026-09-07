import json
import os
import unittest

from chess_cards.san import Board, replay
from chess_cards.search import Budget, Move, _defend, apply, is_checkmate, is_stalemate, legal_moves, mate_in, mate_line, san

HERE = os.path.dirname(__file__)


def perft(b: Board, depth: int) -> int:
    if depth == 0:
        return 1
    return sum(perft(apply(b, m), depth - 1) for m in legal_moves(b))


class MoveGeneration(unittest.TestCase):
    """Perft node counts are the standard oracle for move generators."""

    def test_perft_start_position(self):
        b = Board.from_fen()
        self.assertEqual([perft(b, d) for d in (1, 2, 3)], [20, 400, 8902])

    def test_perft_kiwipete(self):
        b = Board.from_fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1")
        self.assertEqual([perft(b, d) for d in (1, 2)], [48, 2039])

    def test_perft_position_3_en_passant_heavy(self):
        b = Board.from_fen("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1")
        self.assertEqual([perft(b, d) for d in (1, 2, 3)], [14, 191, 2812])

    def test_perft_position_4_promotions_and_castling(self):
        b = Board.from_fen("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1")
        self.assertEqual([perft(b, d) for d in (1, 2)], [6, 264])

    def test_checkmate_and_stalemate_detection(self):
        self.assertTrue(is_checkmate(Board.from_fen("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3")))
        self.assertTrue(is_stalemate(Board.from_fen("7k/5Q2/6K1/8/8/8/8/8 b - - 0 1")))
        self.assertFalse(is_checkmate(Board.from_fen()))


class SanOutput(unittest.TestCase):
    def test_san_roundtrips_through_the_replayer(self):
        b = Board.from_fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1")
        for m in legal_moves(b):
            with self.subTest(uci=m.uci):
                text = san(b, m)
                b2 = b.copy()
                b2.push_san(text)
                self.assertEqual(b2.fen(), apply(b, m).fen())

    def test_disambiguation_forms(self):
        b = Board.from_fen("4k3/8/8/8/8/R7/8/R3K3 w - - 0 1")
        self.assertEqual(san(b, Move.from_uci("a1a2")), "R1a2")
        b = Board.from_fen("4k3/8/8/8/8/8/4K3/R6R w - - 0 1")
        self.assertEqual(san(b, Move.from_uci("a1d1")), "Rad1")
        self.assertEqual(san(b, Move.from_uci("h1d1")), "Rhd1")


class MateSolverAgainstLichess(unittest.TestCase):
    with open(os.path.join(HERE, "fixtures", "lichess_puzzles.json")) as f:
        puzzles = json.load(f)

    @staticmethod
    def position(p: dict) -> Board:
        return Board.from_fen(p["fen"]) if p.get("fen") else replay(p["pgn"])

    def test_fixture_is_substantial(self):
        counts = {t: sum(1 for p in self.puzzles if p["theme"] == t) for t in ("mateIn1", "mateIn2", "mateIn3")}
        self.assertGreaterEqual(counts["mateIn1"], 20)
        self.assertGreaterEqual(counts["mateIn2"], 20)
        self.assertGreaterEqual(counts["mateIn3"], 8)

    def test_replayed_pgn_matches_puzzle_fen_when_given(self):
        for p in self.puzzles:
            if p.get("fen"):
                with self.subTest(id=p["id"]):
                    self.assertEqual(replay(p["pgn"]).fen().split()[:4], p["fen"].split()[:4])

    def test_solver_finds_a_mate_and_none_shorter(self):
        for p in self.puzzles:
            n = int(p["theme"][-1])
            with self.subTest(id=p["id"], theme=p["theme"]):
                b = self.position(p)
                self.assertIn(Move.from_uci(p["solution"][0]), legal_moves(b))
                found = mate_in(b, n, Budget(seconds=20))
                self.assertIsNotNone(found, f"no mate in {n} for https://lichess.org/training/{p['id']}")
                if n > 1:
                    self.assertIsNone(mate_in(b, n - 1, Budget(seconds=20)),
                                      f"Lichess says mate in {n} but we found shorter: {p['id']}")

    def test_lichess_solution_is_a_forced_mate_by_our_search(self):
        """Walk Lichess's own solution line and confirm we agree at every attacker ply."""
        for p in self.puzzles:
            n = int(p["theme"][-1])
            with self.subTest(id=p["id"]):
                b = self.position(p)
                sol = [Move.from_uci(u) for u in p["solution"]]
                depth = n
                for i, m in enumerate(sol):
                    child = apply(b, m)
                    if i % 2 == 0:  # attacker just moved
                        self.assertTrue(is_checkmate(child) or _defend(child, depth - 1, Budget(seconds=20)))
                        depth -= 1
                    b = child
                self.assertTrue(is_checkmate(b))

    def test_mate_line_ends_in_checkmate(self):
        for p in [q for q in self.puzzles if q["theme"] == "mateIn2"][:10]:
            with self.subTest(id=p["id"]):
                b = self.position(p)
                line = mate_line(b, 2)
                self.assertTrue(line)
                end = b
                for m in line:
                    end = apply(end, m)
                self.assertTrue(is_checkmate(end))

    def test_no_false_positives(self):
        self.assertIsNone(mate_in(Board.from_fen(), 2))
        self.assertIsNone(mate_in(Board.from_fen("7k/8/8/8/8/8/8/K5R1 w - - 0 1"), 1))


if __name__ == "__main__":
    unittest.main()
