# chess_cards

Self-hosted chess profile cards for the README, rendered from the public
[Lichess](https://lichess.org/api) and [Chess.com](https://www.chess.com/news/view/published-data-api)
APIs. Pure Python 3.11+, **zero dependencies**, no fonts or external assets in
the SVGs, so GitHub's image proxy renders them the same everywhere.

| Card | What it shows |
|---|---|
| `output/ratings.svg` | Ratings on both sites with Lichess percentiles and Chess.com peaks, a 24-month blitz rating sparkline, and lifetime totals. |
| `output/openings.svg` | Top five opening families as White and as Black over the last 12 months, with win/draw/loss bars. |
| `output/latest-game.svg` | Final position of the most recent game on either site, last move highlighted, with result, opponent, time control, and accuracy. |
| `output/puzzle.svg` | Lichess's daily puzzle, plus how long my own solver took to find the forced mate. |

## How it works

```
chess_cards/
  sources.py   urllib fetchers with an on-disk cache (finished months cached forever)
  san.py       SAN move replayer -> FEN: pins, disambiguation, en passant, castling, promotion
  search.py    legal move generation, checkmate/stalemate, forced-mate search, move -> SAN
  analyze.py   opening families, W/D/L, monthly rating series, accuracy, streaks
  render.py    hand-written SVG: sparkline, stacked bars, board + own piece silhouettes
  __main__.py  CLI glue
```

The interesting piece is `san.py`. Lichess's game endpoints stopped shipping a
final FEN, so the board card replays the SAN move list itself. The replayer is
validated in CI against 400 real Chess.com games whose final FEN is known (an
oracle that came for free with the archive API). Across the full 3,518-game
archive it matches on every game once one Chess.com quirk is normalised:
Chess.com keeps a castling right after that side's rook has been captured on
its home square, which FIDE (and this replayer) drop.

`search.py` builds legal move generation on the same board and runs a
depth-first proof search for forced mates (checks first; at the last ply only
checking moves are tried). Move generation is checked with the standard perft
node counts (start position, Kiwipete, and two tricky en passant / promotion
positions). The solver is checked against 72 Lichess puzzles tagged mateIn1,
mateIn2, and mateIn3: it must find a mate in n, must not find one in n-1, and
must agree with Lichess's own solution line at every attacking ply. The whole
suite runs in about two seconds.

## Run it

```bash
cd chess
python -m unittest discover -s tests -t .          # ~2 s
python -m chess_cards --cache .cache --out output  # hits the APIs, writes the SVGs
```

Options: `--lichess USER`, `--chesscom USER`, `--offline` (cache only).

`.github/workflows/chess-cards.yml` runs the tests on every change and
re-renders the cards daily, committing `chess/output` only when something
changed.

## Design notes

Surface `#0d1117`, accent `#E8567C`, matching the profile. The win/loss pair
`#E8567C` / `#3D8BFF` was checked for colour-vision-deficiency separation and
3:1 contrast against the surface; draws are a deliberate neutral, and every bar
carries its score and game count as text so nothing relies on colour alone.
Piece silhouettes are original paths, drawn in a 100x100 box and scaled per square.
