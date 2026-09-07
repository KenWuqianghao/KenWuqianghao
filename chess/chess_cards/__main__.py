"""CLI: python -m chess_cards --out ../chess/output [--cache DIR] [--offline]"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys

from . import analyze, render, sources
from .san import IllegalMove, pgn_moves, replay, sq_name

RESULT_WORDS = {
    "mate": "by checkmate", "resign": "by resignation", "outoftime": "on time",
    "timeout": "on time", "draw": "", "stalemate": "by stalemate", "checkmated": "by checkmate",
    "resigned": "by resignation", "abandoned": "by abandonment", "repetition": "by repetition",
    "agreed": "by agreement", "insufficient": "insufficient material",
}


def build(lichess_user: str, chesscom_user: str, fetcher: sources.Fetcher) -> dict[str, str]:
    """Fetch everything and return {filename: svg}. Also returns a data snapshot under 'data.json'."""
    now = dt.datetime.now(dt.timezone.utc)
    stamp = now.strftime("%Y-%m-%d")

    li = sources.lichess_user(fetcher, lichess_user)
    li_perfs = li.get("perfs", {})
    cc_stats = sources.chesscom_stats(fetcher, chesscom_user)
    games = sources.chesscom_games(fetcher, chesscom_user)

    def li_row(key: str, label: str):
        p = li_perfs.get(key)
        if not p or p.get("games", 0) == 0:
            return (label, None, "")
        note = ""
        detail = sources.lichess_perf(fetcher, lichess_user, key) if key != "puzzle" else None
        if detail and detail.get("percentile"):
            note = f"top {100 - detail['percentile']:.0f}%"
        elif p.get("prov"):
            note = "provisional"
        return (label, p["rating"], note)

    def cc_row(key: str, label: str):
        s = cc_stats.get(key)
        if not s:
            return (label, None, "")
        if key == "tactics":
            return (label, s.get("highest", {}).get("rating"), "peak")
        rec = s.get("record", {})
        n = rec.get("win", 0) + rec.get("loss", 0) + rec.get("draw", 0)
        best = s.get("best", {}).get("rating")
        return (label, s["last"]["rating"], f"peak {best:,}" if best else f"{n} games")

    series = analyze.monthly_rating(games, chesscom_user, "blitz", months=24)
    wdl = analyze.overall_wdl(games, chesscom_user)
    acc = analyze.average_accuracy(games, chesscom_user, 100)
    li_games = li.get("count", {}).get("all", 0)
    total_games = li_games + wdl.games
    hours = round(li.get("playTime", {}).get("total", 0) / 3600)

    ratings = {
        "title": "Chess ratings",
        "subtitle": f"updated {stamp}",
        "lichess": [li_row("bullet", "Bullet"), li_row("blitz", "Blitz"),
                    li_row("rapid", "Rapid"), li_row("puzzle", "Puzzles")],
        "chesscom": [cc_row("chess_bullet", "Bullet"), cc_row("chess_blitz", "Blitz"),
                     cc_row("chess_rapid", "Rapid"), cc_row("tactics", "Puzzles")],
        "series_label": "Chess.com blitz rating, last 24 months",
        "series": series,
        "footer": [
            ("games played", f"{total_games:,}"),
            ("hours on lichess", f"{hours:,}"),
            ("chess.com score", f"{wdl.score * 100:.0f}%"),
            ("avg accuracy", f"{acc:.0f}%" if acc else "—"),
        ],
    }

    since = now - dt.timedelta(days=365)
    ob = analyze.openings_by_color(games, chesscom_user, top=5, since=since)
    openings = {
        "title": "Opening repertoire",
        "subtitle": f"chess.com · rated · last 12 months · {stamp}",
        "white": ob["white"], "black": ob["black"],
    }

    latest = latest_game(fetcher, lichess_user, chesscom_user, games)
    latest["subtitle"] = f"{latest['platform']} · {latest['when']}"

    data = {"generated": now.isoformat(), "ratings": ratings, "openings": {
        k: [(n, vars(w)) for n, w in v] for k, v in ob.items()}, "latest": latest}
    return {
        "ratings.svg": render.ratings_card(ratings),
        "openings.svg": render.openings_card(openings),
        "latest-game.svg": render.board_card(latest),
        "data.json": json.dumps(data, indent=1, default=str),
    }


def latest_game(fetcher, lichess_user, chesscom_user, cc_games) -> dict:
    """Most recent finished game across both platforms, as a board-card payload."""
    cands = []
    lg = sources.lichess_current_game(fetcher, lichess_user)
    if lg and lg.get("status") not in (None, "started", "created"):
        cands.append(("lichess", lg.get("lastMoveAt", 0) / 1000, lg))
    if cc_games:
        g = cc_games[-1]
        cands.append(("chess.com", g.get("end_time", 0), g))
    if not cands:
        return {"fen": "8/8/8/8/8/8/8/8 w - - 0 1", "title": "Latest game", "platform": "—", "when": "—"}
    platform, ts, g = max(cands, key=lambda c: c[1])
    when = dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%b %d, %Y")
    if platform == "lichess":
        me_white = g["players"]["white"]["user"]["id"] == lichess_user.lower()
        me = g["players"]["white" if me_white else "black"]
        opp = g["players"]["black" if me_white else "white"]
        moves = g.get("moves", "").split()
        board = replay(moves)
        fen = board.fen()
        accuracy = None
        winner = g.get("winner")
        won = winner == ("white" if me_white else "black")
        result = ("Won " if won else "Lost " if winner else "Drew ") + RESULT_WORDS.get(g.get("status", ""), g.get("status", ""))
        opening = g.get("opening", {}).get("name", "")
        opp_name = opp.get("user", {}).get("name", "?")
        opp_rating = opp.get("rating")
        my_rating = me.get("rating")
        diff = me.get("ratingDiff")
        clock = g.get("clock", {})
        tc = f"{clock.get('initial', 0) // 60}+{clock.get('increment', 0)}" if clock else g.get("speed", "")
        url = f"https://lichess.org/{g['id']}"
        n_moves = len(moves)
    else:
        me_white = g["white"]["username"].lower() == chesscom_user.lower()
        me = g["white" if me_white else "black"]
        opp = g["black" if me_white else "white"]
        try:
            moves = pgn_moves(g["pgn"])
            board = replay(moves, g.get("initial_setup", None) or None)
            fen = board.fen()
        except IllegalMove:
            moves = []
            board = None
            fen = g["fen"]
        accuracy = g.get("accuracies", {}).get("white" if me_white else "black")
        res = me["result"]
        if res == "win":
            result = "Won " + RESULT_WORDS.get(opp["result"], opp["result"])
        elif res in sources.DRAW_RESULTS:
            result = "Drew " + RESULT_WORDS.get(res, res)
        else:
            result = "Lost " + RESULT_WORDS.get(res, res)
        opening = analyze.opening_family(g.get("eco")) if g.get("eco") else ""
        full = g.get("eco", "").rsplit("/", 1)[-1].replace("-", " ")
        opening = full if len(full) <= 40 else opening
        opp_name, opp_rating, my_rating, diff = opp["username"], opp["rating"], me["rating"], None
        tc = g.get("time_control", "")
        if tc.isdigit():
            tc = f"{int(tc) // 60}+0"
        elif "+" in tc:
            a, b = tc.split("+")
            tc = f"{int(a) // 60}+{b}"
        url = g["url"]
        n_moves = len(moves)
    lines = [
        ("Opponent", f"{opp_name} ({opp_rating})"),
        ("Me", f"{'White' if me_white else 'Black'} · {my_rating}" + (f" ({diff:+d})" if diff is not None else "")),
        ("Time control", f"{tc} · {(n_moves + 1) // 2} moves"),
    ]
    if accuracy is not None:
        lines.append(("Accuracy", f"{accuracy:.1f}%"))
    tail = " ".join(moves[-6:]) if moves else ""
    last_move = None
    if board is not None and board.last_move:
        last_move = (sq_name(board.last_move[0]), sq_name(board.last_move[1]))
    return {
        "fen": fen, "flip": not me_white, "last_move": last_move,
        "title": "Latest game", "platform": platform, "when": when,
        "result": result.strip(), "opening": opening, "lines": lines, "moves_tail": ("… " + tail) if tail else "",
        "url": url,
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Render chess profile cards as SVG.")
    ap.add_argument("--lichess", default="kenwuu")
    ap.add_argument("--chesscom", default="kenwuu")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "output"))
    ap.add_argument("--cache", default=None, help="directory for the API cache")
    ap.add_argument("--offline", action="store_true", help="never hit the network; require cache")
    args = ap.parse_args(argv)

    fetcher = sources.Fetcher(cache_dir=args.cache, offline=args.offline)
    files = build(args.lichess, args.chesscom, fetcher)
    os.makedirs(args.out, exist_ok=True)
    for name, content in files.items():
        with open(os.path.join(args.out, name), "w") as f:
            f.write(content)
        print(f"wrote {os.path.join(args.out, name)} ({len(content):,} bytes)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
