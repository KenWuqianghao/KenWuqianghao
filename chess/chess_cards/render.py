"""Hand-authored SVG cards. No templating library, no fonts, no external assets:
everything the card needs is inside the file so GitHub's image proxy renders it
identically everywhere.

Palette follows the profile README: surface #0d1117, accent #E8567C. The
win/loss pair (#E8567C / #3D8BFF) passes the CVD + contrast checks on that
surface; draws use a deliberate neutral (#8B949E) and every bar carries a
direct label so identity never rests on colour alone.
"""
from __future__ import annotations

from xml.sax.saxutils import escape

from .analyze import WDL

SURFACE = "#0d1117"
CARD = "#161b22"
BORDER = "#30363d"
ACCENT = "#E8567C"
ACCENT_SOFT = "#E8567C33"
TEXT = "#e6edf3"
TEXT_2 = "#9da7b3"
TEXT_3 = "#6e7681"
WIN, DRAW, LOSS = "#E8567C", "#8B949E", "#3D8BFF"
LIGHT_SQ, DARK_SQ = "#7f8a9c", "#3b4352"
FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace"

WIDTH = 495


def _t(x: float, y: float, s: str, *, size: int = 12, fill: str = TEXT, weight: int = 400,
       anchor: str = "start", mono: bool = False, extra: str = "") -> str:
    fam = MONO if mono else FONT
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{extra}>{escape(str(s))}</text>')


def _frame(height: int, title: str, subtitle: str, body: str, width: int = WIDTH) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">\n'
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" '
        f'fill="{SURFACE}" stroke="{BORDER}"/>\n'
        f'{_t(20, 30, title, size=16, weight=600)}\n'
        f'{_t(width - 20, 30, subtitle, size=11, fill=TEXT_3, anchor="end")}\n'
        f'<line x1="20" y1="42" x2="{width - 20}" y2="42" stroke="{BORDER}"/>\n'
        f'{body}\n</svg>\n'
    )


def _fmt(n: float | int | None, digits: int = 0) -> str:
    if n is None:
        return "—"
    return f"{n:,.{digits}f}"


# ------------------------------------------------------------------ sparkline
def sparkline(points: list[tuple[str, int]], x: float, y: float, w: float, h: float) -> str:
    if len(points) < 2:
        return _t(x, y + h / 2, "not enough history", size=10, fill=TEXT_3)
    vals = [v for _, v in points]
    lo, hi = min(vals), max(vals)
    span = max(hi - lo, 1)
    step = w / (len(vals) - 1)
    coords = [(x + i * step, y + h - (v - lo) / span * h) for i, v in enumerate(vals)]
    path = "M" + " L".join(f"{cx:.1f} {cy:.1f}" for cx, cy in coords)
    area = path + f" L{coords[-1][0]:.1f} {y + h:.1f} L{coords[0][0]:.1f} {y + h:.1f} Z"
    lx, ly = coords[-1]
    hi_i = vals.index(hi)
    hx, hy = coords[hi_i]
    out = [
        f'<path d="{area}" fill="{ACCENT}" fill-opacity="0.10"/>',
        f'<path d="{path}" fill="none" stroke="{ACCENT}" stroke-width="2" '
        f'stroke-linejoin="round" stroke-linecap="round"/>',
        f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="4" fill="{ACCENT}" stroke="{SURFACE}" stroke-width="2"/>',
        _t(lx - 6, ly - 8 if ly - 12 > y else ly + 16, _fmt(vals[-1]), size=11, weight=600, anchor="end"),
    ]
    if hi_i != len(vals) - 1:
        out.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="3" fill="{SURFACE}" stroke="{ACCENT}" stroke-width="2"/>')
        anchor = "middle" if 20 < hx - x < w - 20 else ("start" if hx - x <= 20 else "end")
        out.append(_t(hx, hy - 7, f"peak {_fmt(hi)}", size=9, fill=TEXT_2, anchor=anchor))
    out.append(_t(x, y + h + 14, points[0][0], size=9, fill=TEXT_3))
    out.append(_t(x + w, y + h + 14, points[-1][0], size=9, fill=TEXT_3, anchor="end"))
    return "\n".join(out)


# ------------------------------------------------------------- ratings card
def ratings_card(d: dict) -> str:
    """d = {lichess: [(label, rating, note)], chesscom: [...], series: [(month, rating)],
            series_label: str, footer: [(label, value)]}"""
    body = []
    col_w = (WIDTH - 40) / 2
    for ci, (platform, rows) in enumerate((("Lichess", d["lichess"]), ("Chess.com", d["chesscom"]))):
        x0 = 20 + ci * col_w
        body.append(_t(x0, 64, platform.upper(), size=10, fill=TEXT_3, weight=600, extra=' letter-spacing="1.2"'))
        for ri, (label, rating, note) in enumerate(rows):
            y = 86 + ri * 22
            body.append(_t(x0, y, label, size=12, fill=TEXT_2))
            body.append(_t(x0 + 112, y, _fmt(rating), size=13, weight=600, anchor="end", mono=True))
            if note:
                body.append(_t(x0 + 120, y, note, size=10, fill=TEXT_3))
    y_sp = 86 + 4 * 22 + 4
    body.append(_t(20, y_sp, d["series_label"].upper(), size=10, fill=TEXT_3, weight=600, extra=' letter-spacing="1.2"'))
    body.append(sparkline(d["series"], 20, y_sp + 10, WIDTH - 40, 46))
    y_f = y_sp + 10 + 46 + 34
    n = len(d["footer"])
    for i, (label, value) in enumerate(d["footer"]):
        cx = 20 + (WIDTH - 40) * (i + 0.5) / n
        body.append(_t(cx, y_f, value, size=15, weight=600, anchor="middle", mono=True))
        body.append(_t(cx, y_f + 15, label, size=10, fill=TEXT_3, anchor="middle"))
    return _frame(y_f + 30, d.get("title", "Chess"), d.get("subtitle", ""), "\n".join(body))


# ------------------------------------------------------------ openings card
def _wdl_bar(x: float, y: float, w: float, h: float, wdl: WDL) -> str:
    total = wdl.games or 1
    segs = [(wdl.win, WIN), (wdl.draw, DRAW), (wdl.loss, LOSS)]
    gap = 2
    n_nonzero = sum(1 for v, _ in segs if v)
    usable = w - gap * max(n_nonzero - 1, 0)
    out, cx = [], x
    for v, color in segs:
        if not v:
            continue
        sw = usable * v / total
        out.append(f'<rect x="{cx:.1f}" y="{y}" width="{sw:.1f}" height="{h}" fill="{color}"/>')
        cx += sw + gap
    r = 4  # rounded ends come from the clip; the track underneath shows through the 2px gaps
    out.insert(0, f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{BORDER}"/>')
    cid = f"bar-{int(x)}-{int(y)}"
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>'
            + out[0] + f'<g clip-path="url(#{cid})">' + "".join(out[1:]) + '</g>')


def openings_card(d: dict) -> str:
    """d = {white: [(name, WDL)], black: [(name, WDL)], title, subtitle}"""
    body = []
    col_w = (WIDTH - 40) / 2
    bar_w = col_w - 24
    max_rows = max(len(d["white"]), len(d["black"]), 1)
    for ci, (side, rows) in enumerate((("As White", d["white"]), ("As Black", d["black"]))):
        x0 = 20 + ci * col_w
        body.append(_t(x0, 64, side.upper(), size=10, fill=TEXT_3, weight=600, extra=' letter-spacing="1.2"'))
        for ri, (name, wdl) in enumerate(rows):
            y = 76 + ri * 34
            label = name if len(name) <= 26 else name[:25] + "…"
            body.append(_t(x0, y + 4, label, size=11, fill=TEXT_2))
            body.append(_t(x0 + bar_w, y + 4, f"{wdl.score * 100:.0f}% · {wdl.games}", size=10,
                           fill=TEXT_3, anchor="end", mono=True))
            body.append(_wdl_bar(x0, y + 9, bar_w, 8, wdl))
    y_leg = 76 + max_rows * 34 + 2
    lx = 20
    for label, color in (("Win", WIN), ("Draw", DRAW), ("Loss", LOSS)):
        body.append(f'<rect x="{lx}" y="{y_leg - 8}" width="10" height="10" rx="2" fill="{color}"/>')
        body.append(_t(lx + 15, y_leg + 1, label, size=10, fill=TEXT_2))
        lx += 58
    body.append(_t(WIDTH - 20, y_leg + 1, "score % · games", size=10, fill=TEXT_3, anchor="end"))
    return _frame(y_leg + 18, d.get("title", "Repertoire"), d.get("subtitle", ""), "\n".join(body))


# --------------------------------------------------------------- board card
# Piece silhouettes on a 100x100 box, y down. Own design; no external glyphs.
PIECE_PATHS = {
    "P": ["M50 17a13 13 0 1 0 0.01 0Z",
          "M50 42C38 46 35 58 40 70H60C65 58 62 46 50 42Z",
          "M31 74H69V85H31Z"],
    "R": ["M30 24H40V33H46V24H54V33H60V24H70V44H30Z",
          "M36 44H64V74H36Z",
          "M30 74H70V85H30Z"],
    "N": ["M31 85H72V77C72 62 66 52 60 41C58 35 62 28 59 19L51 26L45 19C35 26 29 39 28 50L38 52L33 63C31 70 31 78 31 85Z"],
    "B": ["M50 12a6 6 0 1 0 0.01 0Z",
          "M50 22C33 39 34 57 42 67H58C66 57 67 39 50 22Z",
          "M40 67H60V75H40Z",
          "M31 75H69V85H31Z"],
    "Q": ["M30 34a5 5 0 1 0 0.01 0Z", "M50 20a5 5 0 1 0 0.01 0Z", "M70 34a5 5 0 1 0 0.01 0Z",
          "M35 75L30 40L42 54L50 28L58 54L70 40L65 75Z",
          "M29 75H71V85H29Z"],
    "K": ["M47 12H53V20H61V26H53V34H47V26H39V20H47Z",
          "M36 75L32 48C32 40 44 36 50 44C56 36 68 40 68 48L64 75Z",
          "M29 75H71V85H29Z"],
}


def piece_svg(piece: str, x: float, y: float, size: float) -> str:
    white = piece.isupper()
    fill = "#f4f4f2" if white else "#1c2028"
    stroke = "#1c2028" if white else "#c5cad3"
    s = size / 100
    paths = "".join(f'<path d="{p}"/>' for p in PIECE_PATHS[piece.upper()])
    extra = ""
    if piece.upper() == "N":  # eye
        extra = f'<circle cx="52" cy="34" r="2.6" fill="{stroke}" stroke="none"/>'
    if piece.upper() == "B":  # mitre slit
        extra = f'<path d="M50 34V52" stroke="{stroke}" stroke-width="3" fill="none"/>'
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s:.4f})" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="4" stroke-linejoin="round">{paths}{extra}</g>')


def board_svg(fen: str, x: float, y: float, size: float, flip: bool = False,
              last_move: tuple[str, str] | None = None) -> str:
    sqs = size / 8
    rows = fen.split()[0].split("/")
    out = [f'<rect x="{x - 2}" y="{y - 2}" width="{size + 4}" height="{size + 4}" rx="4" fill="{BORDER}"/>']
    grid: dict[tuple[int, int], str] = {}
    for r, row in enumerate(rows):  # r=0 is rank 8
        f = 0
        for ch in row:
            if ch.isdigit():
                f += int(ch)
            else:
                grid[(f, 7 - r)] = ch
                f += 1
    hl = set()
    if last_move:
        for name in last_move:
            hl.add(("abcdefgh".index(name[0]), int(name[1]) - 1))
    for file in range(8):
        for rank in range(8):
            col = 7 - file if flip else file
            row = rank if flip else 7 - rank
            px, py = x + col * sqs, y + row * sqs
            light = (file + rank) % 2 == 1
            fill = LIGHT_SQ if light else DARK_SQ
            out.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{sqs:.2f}" height="{sqs:.2f}" fill="{fill}"/>')
            if (file, rank) in hl:
                out.append(f'<rect x="{px:.1f}" y="{py:.1f}" width="{sqs:.2f}" height="{sqs:.2f}" fill="{ACCENT}" fill-opacity="0.45"/>')
            p = grid.get((file, rank))
            if p:
                out.append(piece_svg(p, px + sqs * 0.05, py + sqs * 0.04, sqs * 0.9))
    # coordinates
    for i in range(8):
        file_ch = "abcdefgh"[7 - i if flip else i]
        rank_ch = str(i + 1 if flip else 8 - i)
        out.append(_t(x + i * sqs + sqs - 3, y + size - 3, file_ch, size=7, fill=TEXT_2, anchor="end"))
        out.append(_t(x + 2, y + i * sqs + 9, rank_ch, size=7, fill=TEXT_2))
    return "\n".join(out)


def board_card(d: dict) -> str:
    """d = {fen, flip, last_move, title, subtitle, lines: [(label, value)], result: str, opening: str, url}"""
    size = 232
    bx, by = 20, 56
    body = [board_svg(d["fen"], bx, by, size, d.get("flip", False), d.get("last_move"))]
    x0 = bx + size + 22
    y = by + 12
    body.append(_t(x0, y, d.get("result", ""), size=15, weight=600))
    y += 20
    body.append(_t(x0, y, d.get("opening", ""), size=11, fill=TEXT_2))
    y += 26
    for label, value in d.get("lines", []):
        body.append(_t(x0, y, label.upper(), size=9, fill=TEXT_3, weight=600, extra=' letter-spacing="1"'))
        body.append(_t(x0, y + 15, value, size=12, fill=TEXT))
        y += 36
    moves = d.get("moves_tail")
    if moves:
        body.append(_t(x0, by + size - 4, moves, size=9, fill=TEXT_3, mono=True))
    return _frame(by + size + 20, d.get("title", "Latest game"), d.get("subtitle", ""), "\n".join(body))


# -------------------------------------------------------------- puzzle card
def puzzle_card(d: dict) -> str:
    """d = {fen, flip, last_move, side, goal, lines: [(label, value)], themes: [str], solver: str, subtitle}"""
    size = 232
    bx, by = 20, 56
    body = [board_svg(d["fen"], bx, by, size, d.get("flip", False), d.get("last_move"))]
    x0 = bx + size + 22
    y = by + 12
    body.append(_t(x0, y, d.get("side", ""), size=15, weight=600))
    y += 20
    body.append(_t(x0, y, d.get("goal", ""), size=12, fill=ACCENT, weight=600))
    y += 26
    for label, value in d.get("lines", []):
        body.append(_t(x0, y, label.upper(), size=9, fill=TEXT_3, weight=600, extra=' letter-spacing="1"'))
        body.append(_t(x0, y + 15, value, size=12, fill=TEXT))
        y += 36
    tx, ty = x0, y + 2
    for t in (d.get("themes") or [])[:4]:
        w = 6.2 * len(t) + 14
        if tx + w > WIDTH - 20:
            break
        body.append(f'<rect x="{tx:.1f}" y="{ty - 11}" width="{w:.1f}" height="16" rx="8" fill="{CARD}" stroke="{BORDER}"/>')
        body.append(_t(tx + w / 2, ty + 1, t, size=9, fill=TEXT_2, anchor="middle"))
        tx += w + 6
    return _frame(by + size + 20, d.get("title", "Daily puzzle"), d.get("subtitle", ""), "\n".join(body))
