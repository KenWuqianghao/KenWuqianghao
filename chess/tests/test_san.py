import json
import os
import unittest

from chess_cards.san import Board, IllegalMove, START_FEN, pgn_moves, replay

HERE = os.path.dirname(__file__)


def normalize_castling(fen_fields: list[str], board: Board) -> list[str]:
    """Chess.com keeps a castling right after the rook on that side was captured;
    FIDE (and this replayer) drop it. Drop rights whose rook is gone from the oracle."""
    home = {"K": (7, "R"), "Q": (0, "R"), "k": (63, "r"), "q": (56, "r")}
    rights = "".join(c for c in fen_fields[2] if c != "-" and board.squares[home[c][0]] == home[c][1])
    return fen_fields[:2] + [rights or "-"] + fen_fields[3:]


class ReplayAgainstChessComOracle(unittest.TestCase):
    def test_final_fen_matches_chesscom(self):
        with open(os.path.join(HERE, "fixtures", "chesscom_games.json")) as f:
            games = json.load(f)
        self.assertGreaterEqual(len(games), 300)
        for g in games:
            with self.subTest(url=g["url"]):
                board = replay(g["moves"], g["start"])
                want = normalize_castling(g["fen"].split(), board)
                got = board.fen().split()[: len(want)]
                self.assertEqual(got, want)


class SanSemantics(unittest.TestCase):
    def test_start_position_roundtrip(self):
        self.assertEqual(Board.from_fen().fen(), START_FEN)

    def test_en_passant_capture_removes_pawn(self):
        b = replay("e4 a6 e5 d5 exd6")
        self.assertIsNone(b.squares[35])  # d5 pawn gone
        self.assertEqual(b.squares[43], "P")  # white pawn on d6
        self.assertEqual(b.fen().split()[3], "-")

    def test_en_passant_square_is_set_after_double_push(self):
        self.assertEqual(replay("e4").fen().split()[3], "e3")

    def test_promotion_and_underpromotion(self):
        b = replay("h4 g5 hxg5 h6 gxh6 Nf6 h7 Rg8 hxg8=N")
        self.assertEqual(b.squares[62], "N")

    def test_castling_moves_rook_and_clears_rights(self):
        b = replay("e4 e5 Nf3 Nc6 Bc4 Bc5 O-O")
        self.assertEqual(b.squares[6], "K")
        self.assertEqual(b.squares[5], "R")
        self.assertEqual(b.fen().split()[2], "kq")

    def test_queenside_castling_with_zero_notation(self):
        b = replay("d4 d5 Nc3 Nc6 Bf4 Bf5 Qd2 Qd7 0-0-0 0-0-0")
        self.assertEqual(b.squares[2], "K")
        self.assertEqual(b.squares[3], "R")
        self.assertEqual(b.squares[58], "k")
        self.assertEqual(b.fen().split()[2], "-")

    def test_pin_disambiguates_knight(self):
        # Knights on c3 and e3 both reach d5, but c3 is pinned by the bishop on b4.
        fen = "4k3/8/8/8/1b6/2N1N3/8/4K3 w - - 0 1"
        b = Board.from_fen(fen)
        b.push_san("Nd5")  # unambiguous only because the pin is honoured
        self.assertEqual(b.squares[18], "N")
        self.assertIsNone(b.squares[20])
        self.assertEqual(b.squares[35], "N")

    def test_pinned_piece_cannot_move_and_raises(self):
        fen = "4k3/8/8/8/1b6/2N5/8/4K3 w - - 0 1"
        with self.assertRaises(IllegalMove):
            Board.from_fen(fen).push_san("Ne4")

    def test_file_and_rank_disambiguation(self):
        fen = "4k3/8/8/8/8/R7/8/R3K3 w - - 0 1"
        b = Board.from_fen(fen)
        b.push_san("R1a2")
        self.assertEqual(b.squares[8], "R")
        self.assertEqual(b.squares[16], "R")

    def test_rook_capture_on_home_square_clears_opponent_right(self):
        fen = "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1"
        b = Board.from_fen(fen)
        b.push_san("Rxa8+")
        self.assertEqual(b.fen().split()[2], "Kk")

    def test_halfmove_and_fullmove_clocks(self):
        b = replay("Nf3 Nf6 Ng1 Ng8")
        self.assertEqual(b.halfmove, 4)
        self.assertEqual(b.fullmove, 3)
        b.push_san("e4")
        self.assertEqual(b.halfmove, 0)

    def test_last_move_tracks_squares(self):
        b = replay("e4 c5")
        self.assertEqual(b.last_move, (50, 34))

    def test_unparseable_token_raises(self):
        with self.assertRaises(IllegalMove):
            Board.from_fen().push_san("Zz9")


class PgnParsing(unittest.TestCase):
    def test_strips_headers_clocks_numbers_and_result(self):
        pgn = ('[Event "x"]\n[Result "1-0"]\n\n1. e4 {[%clk 0:03:00]} 1... e5 {[%clk 0:02:59]} '
               '2. Nf3 (2. Nc3 Nc6) Nc6 $1 3. Bb5+ 1-0')
        self.assertEqual(pgn_moves(pgn), ["e4", "e5", "Nf3", "Nc6", "Bb5+"])


if __name__ == "__main__":
    unittest.main()
