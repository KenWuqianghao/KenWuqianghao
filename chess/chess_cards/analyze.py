"""Turn raw API payloads into the numbers the cards display."""
from __future__ import annotations

import datetime as dt
import re
from collections import defaultdict
from dataclasses import dataclass

from .sources import DRAW_RESULTS

FAMILY_SUFFIXES = {
    "Defense", "Defence", "Opening", "Game", "Gambit", "Attack", "System",
    "Countergambit", "Counter-Gambit", "Variation",
}
POSSESSIVES = {"Queens": "Queen's", "Kings": "King's", "Bishops": "Bishop's",
               "Alekhines": "Alekhine's", "Nimzowitschs": "Nimzowitsch's"}


def opening_family(eco_url: str | None) -> str:
    """'…/openings/Sicilian-Defense-Open-Najdorf-6.Be3' -> 'Sicilian Defense'."""
    if not eco_url:
        return "Unknown"
    slug = eco_url.rstrip("/").rsplit("/", 1)[-1]
    words = []
    for w in slug.split("-"):
        if not w or re.search(r"\d", w):  # move lists like '6.Be3' end the name
            break
        words.append(POSSESSIVES.get(w, w))
    if not words:
        return "Unknown"
    family = []
    for w in words:
        family.append(w)
        if w in FAMILY_SUFFIXES and len(family) >= 2:
            break
    else:
        family = family[:3]
    return " ".join(family)


@dataclass
class WDL:
    win: int = 0
    draw: int = 0
    loss: int = 0

    @property
    def games(self) -> int:
        return self.win + self.draw + self.loss

    @property
    def score(self) -> float:
        return (self.win + 0.5 * self.draw) / self.games if self.games else 0.0

    def add(self, outcome: str) -> None:
        setattr(self, outcome, getattr(self, outcome) + 1)


def my_side(game: dict, user: str) -> str | None:
    u = user.lower()
    if game["white"]["username"].lower() == u:
        return "white"
    if game["black"]["username"].lower() == u:
        return "black"
    return None


def outcome(game: dict, user: str) -> str:
    side = my_side(game, user)
    res = game[side]["result"]
    if res == "win":
        return "win"
    if res in DRAW_RESULTS:
        return "draw"
    return "loss"


def standard_games(games: list[dict]) -> list[dict]:
    return [g for g in games if g.get("rules") == "chess" and g.get("rated")]


def openings_by_color(games: list[dict], user: str, top: int = 5,
                      since: dt.datetime | None = None) -> dict[str, list[tuple[str, WDL]]]:
    """Top opening families as white and black, ordered by frequency."""
    buckets: dict[str, dict[str, WDL]] = {"white": defaultdict(WDL), "black": defaultdict(WDL)}
    for g in standard_games(games):
        if since and dt.datetime.fromtimestamp(g["end_time"], dt.timezone.utc) < since:
            continue
        side = my_side(g, user)
        if not side:
            continue
        buckets[side][opening_family(g.get("eco"))].add(outcome(g, user))
    out = {}
    for side, fam in buckets.items():
        ranked = sorted(fam.items(), key=lambda kv: (-kv[1].games, kv[0]))
        out[side] = ranked[:top]
    return out


def overall_wdl(games: list[dict], user: str, time_class: str | None = None) -> WDL:
    w = WDL()
    for g in standard_games(games):
        if time_class and g.get("time_class") != time_class:
            continue
        if my_side(g, user):
            w.add(outcome(g, user))
    return w


def monthly_rating(games: list[dict], user: str, time_class: str = "blitz",
                   months: int = 24) -> list[tuple[str, int]]:
    """Rating at the end of each month (last rated game), most recent `months`."""
    last: dict[str, int] = {}
    for g in standard_games(games):
        if g.get("time_class") != time_class:
            continue
        side = my_side(g, user)
        if not side:
            continue
        when = dt.datetime.fromtimestamp(g["end_time"], dt.timezone.utc)
        last[when.strftime("%Y-%m")] = g[side]["rating"]
    series = sorted(last.items())
    if not series:
        return []
    # fill months with no games by carrying the previous rating forward
    filled, (y, m) = [], map(int, series[0][0].split("-"))
    idx, cur = 0, series[0][1]
    end_y, end_m = map(int, series[-1][0].split("-"))
    while (y, m) <= (end_y, end_m):
        key = f"{y:04d}-{m:02d}"
        if idx < len(series) and series[idx][0] == key:
            cur = series[idx][1]
            idx += 1
        filled.append((key, cur))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return filled[-months:]


def average_accuracy(games: list[dict], user: str, last_n: int = 100) -> float | None:
    vals = []
    for g in reversed(standard_games(games)):
        side = my_side(g, user)
        acc = g.get("accuracies", {}).get(side) if side else None
        if acc is not None:
            vals.append(acc)
            if len(vals) >= last_n:
                break
    return sum(vals) / len(vals) if vals else None


def longest_win_streak(games: list[dict], user: str) -> int:
    best = cur = 0
    for g in standard_games(games):
        if not my_side(g, user):
            continue
        if outcome(g, user) == "win":
            cur += 1
            best = max(best, cur)
        else:
            cur = 0
    return best


def highest_rated_win(games: list[dict], user: str) -> dict | None:
    best = None
    for g in standard_games(games):
        side = my_side(g, user)
        if side and outcome(g, user) == "win":
            opp = g["black" if side == "white" else "white"]
            if best is None or opp["rating"] > best["rating"]:
                best = {"rating": opp["rating"], "username": opp["username"], "url": g["url"],
                        "time_class": g.get("time_class")}
    return best
