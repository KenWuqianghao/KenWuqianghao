import datetime as dt
import json
import os
import unittest

from chess_cards import analyze, render
from chess_cards.analyze import WDL, opening_family

HERE = os.path.dirname(__file__)


def load(name):
    with open(os.path.join(HERE, "fixtures", name)) as f:
        return json.load(f)


class OpeningFamily(unittest.TestCase):
    def test_truncates_at_family_word(self):
        self.assertEqual(opening_family("https://www.chess.com/openings/Sicilian-Defense-Open-Najdorf-Variation-6.Be3"),
                         "Sicilian Defense")
        self.assertEqual(opening_family("https://www.chess.com/openings/Giuoco-Piano-Game-Main-Line"),
                         "Giuoco Piano Game")

    def test_restores_possessives(self):
        self.assertEqual(opening_family("https://www.chess.com/openings/Queens-Gambit-Declined-3...Nf6"),
                         "Queen's Gambit")
        self.assertEqual(opening_family("https://www.chess.com/openings/Kings-Indian-Defense-Normal-Variation"),
                         "King's Indian Defense")

    def test_move_list_ends_name(self):
        self.assertEqual(opening_family("https://www.chess.com/openings/Caro-Kann-Defense-2.d4-d5-3.e5"),
                         "Caro Kann Defense")

    def test_falls_back_to_three_words(self):
        self.assertEqual(opening_family("https://www.chess.com/openings/Van-t-Kruijs-Opening"), "Van t Kruijs Opening")
        self.assertEqual(opening_family("https://www.chess.com/openings/Alpha-Beta-Gamma-Delta"), "Alpha Beta Gamma")

    def test_missing(self):
        self.assertEqual(opening_family(None), "Unknown")


class Stats(unittest.TestCase):
    games = load("chesscom_month.json")["games"]

    def test_wdl_counts_every_rated_standard_game(self):
        w = analyze.overall_wdl(self.games, "kenwuu")
        std = [g for g in self.games if g["rules"] == "chess" and g["rated"]]
        self.assertEqual(w.games, len(std))
        self.assertAlmostEqual(w.score, (w.win + 0.5 * w.draw) / w.games)

    def test_openings_by_color_sorted_by_frequency(self):
        ob = analyze.openings_by_color(self.games, "kenwuu", top=3)
        for side in ("white", "black"):
            counts = [wdl.games for _, wdl in ob[side]]
            self.assertEqual(counts, sorted(counts, reverse=True))
            self.assertLessEqual(len(ob[side]), 3)

    def test_since_filter_excludes_old_games(self):
        future = dt.datetime.now(dt.timezone.utc) + dt.timedelta(days=1)
        ob = analyze.openings_by_color(self.games, "kenwuu", since=future)
        self.assertEqual(ob, {"white": [], "black": []})

    def test_monthly_rating_fills_gaps_and_is_monotonic_in_time(self):
        series = analyze.monthly_rating(self.games, "kenwuu", "blitz", months=48)
        months = [m for m, _ in series]
        self.assertEqual(months, sorted(months))
        # consecutive months, no holes
        for a, b in zip(months, months[1:]):
            y, m = map(int, a.split("-"))
            nxt = f"{y + 1:04d}-01" if m == 12 else f"{y:04d}-{m + 1:02d}"
            self.assertEqual(b, nxt)

    def test_average_accuracy_bounded(self):
        acc = analyze.average_accuracy(self.games, "kenwuu")
        if acc is not None:
            self.assertTrue(0 <= acc <= 100)

    def test_highest_rated_win_is_a_win(self):
        best = analyze.highest_rated_win(self.games, "kenwuu")
        self.assertIsNotNone(best)
        self.assertIn(best["time_class"], {"bullet", "blitz", "rapid", "daily"})


class Rendering(unittest.TestCase):
    def test_openings_card_renders_both_columns_with_unique_clip_ids(self):
        svg = render.openings_card({
            "white": [("French Defense", WDL(5, 1, 4))],
            "black": [("Sicilian Defense", WDL(2, 0, 3)), ("Caro Kann <Defense>", WDL(0, 0, 1))],
        })
        ids = [s.split('"')[0] for s in svg.split('clipPath id="')[1:]]
        self.assertEqual(len(ids), 3)
        self.assertEqual(len(set(ids)), 3)
        self.assertIn("&lt;Defense&gt;", svg)  # escaped, not injected

    def test_ratings_card_handles_missing_values(self):
        svg = render.ratings_card({
            "lichess": [("Bullet", None, ""), ("Blitz", 1916, "top 14%"), ("Rapid", None, ""), ("Puzzles", 2009, "")],
            "chesscom": [("Bullet", 1229, "peak 1,250")] * 4,
            "series_label": "x", "series": [("2025-01", 1500)], "footer": [("games", "1")],
        })
        self.assertIn("not enough history", svg)
        self.assertIn("—", svg)

    def test_board_places_all_pieces_from_fen(self):
        svg = render.board_svg("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", 0, 0, 240)
        self.assertEqual(svg.count("<g transform="), 32)
        self.assertEqual(svg.count('fill="#f4f4f2"'), 16)

    def test_board_flip_puts_black_at_bottom(self):
        svg = render.board_svg("k7/8/8/8/8/8/8/7K w - - 0 1", 0, 0, 80, flip=True)
        # black king (a8) lands on the bottom-right square (col 7, row 7 -> 70px + inset)
        black_group = [g for g in svg.split("<g ") if 'fill="#1c2028"' in g][0]
        self.assertIn("translate(70.5 70.4)", black_group)
        self.assertIn("<svg", render.board_card({"fen": "k7/8/8/8/8/8/8/7K w - - 0 1", "flip": True}))


if __name__ == "__main__":
    unittest.main()
