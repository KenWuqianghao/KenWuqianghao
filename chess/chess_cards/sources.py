"""Fetchers for the public Lichess and Chess.com APIs (stdlib only).

Every fetch goes through `Fetcher.get_json`, which supports an on-disk cache so
tests and local runs never hit the network, and Chess.com month archives that
are already complete are cached forever.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import time
import urllib.error
import urllib.request

USER_AGENT = "kenwuqianghao-profile-chess-cards (+https://github.com/KenWuqianghao)"
LICHESS = "https://lichess.org"
CHESSCOM = "https://api.chess.com/pub"

DRAW_RESULTS = {
    "agreed", "repetition", "stalemate", "insufficient", "50move",
    "timevsinsufficient",
}


class Fetcher:
    def __init__(self, cache_dir: str | None = None, offline: bool = False,
                 retries: int = 3, timeout: int = 60):
        self.cache_dir = cache_dir
        self.offline = offline
        self.retries = retries
        self.timeout = timeout
        if cache_dir:
            os.makedirs(cache_dir, exist_ok=True)

    # ------------------------------------------------------------- caching
    def _cache_path(self, url: str) -> str | None:
        if not self.cache_dir:
            return None
        key = hashlib.sha1(url.encode()).hexdigest()[:16]
        return os.path.join(self.cache_dir, key + ".json")

    def get_json(self, url: str, *, max_age: float | None = None, accept: str = "application/json"):
        """GET a JSON document. `max_age` seconds (None = cache forever)."""
        path = self._cache_path(url)
        if path and os.path.exists(path):
            age = time.time() - os.path.getmtime(path)
            if self.offline or max_age is None or age < max_age:
                with open(path) as f:
                    return json.load(f)
        if self.offline:
            raise RuntimeError(f"offline and not cached: {url}")
        data = self._fetch(url, accept)
        if path:
            with open(path, "w") as f:
                json.dump(data, f)
        return data

    def _fetch(self, url: str, accept: str):
        last: Exception | None = None
        for attempt in range(self.retries):
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    return json.load(r)
            except urllib.error.HTTPError as e:  # 404 etc. are not retryable
                if e.code == 429:
                    last = e
                    time.sleep(2 ** attempt * 5)
                    continue
                raise
            except (urllib.error.URLError, TimeoutError) as e:
                last = e
                time.sleep(2 ** attempt)
        raise RuntimeError(f"failed to fetch {url}: {last}")


# ----------------------------------------------------------------- Lichess
def lichess_user(f: Fetcher, user: str) -> dict:
    return f.get_json(f"{LICHESS}/api/user/{user}", max_age=0)


def lichess_perf(f: Fetcher, user: str, perf: str) -> dict | None:
    try:
        return f.get_json(f"{LICHESS}/api/user/{user}/perf/{perf}", max_age=0)
    except urllib.error.HTTPError:
        return None


def lichess_current_game(f: Fetcher, user: str) -> dict | None:
    try:
        return f.get_json(f"{LICHESS}/api/user/{user}/current-game", max_age=0)
    except urllib.error.HTTPError:
        return None


# ---------------------------------------------------------------- Chess.com
def chesscom_stats(f: Fetcher, user: str) -> dict:
    return f.get_json(f"{CHESSCOM}/player/{user}/stats", max_age=0)


def chesscom_archives(f: Fetcher, user: str) -> list[str]:
    return f.get_json(f"{CHESSCOM}/player/{user}/games/archives", max_age=0)["archives"]


def chesscom_games(f: Fetcher, user: str, months: int | None = None) -> list[dict]:
    """All games, oldest first. Completed months are cached forever; the
    current month is re-fetched every run."""
    urls = chesscom_archives(f, user)
    if months:
        urls = urls[-months:]
    now = dt.datetime.now(dt.timezone.utc)
    this_month = f"/{now.year}/{now.month:02d}"
    games: list[dict] = []
    for u in urls:
        max_age = 0 if u.endswith(this_month) else None
        games.extend(f.get_json(u, max_age=max_age)["games"])
    games.sort(key=lambda g: g.get("end_time", 0))
    return games


def lichess_daily_puzzle(f: Fetcher) -> dict:
    return f.get_json(f"{LICHESS}/api/puzzle/daily", max_age=0)
