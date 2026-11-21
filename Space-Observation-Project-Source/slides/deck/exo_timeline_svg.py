# -*- coding: utf-8 -*-
"""Timeline nhiều lane cho lịch sử tìm exoplanet (SVG tự vẽ, mọi chữ >= 20 px trên canvas 1160 px).
Dựa trên kiểu của timeline_svg.py (mẫu Hadoop, HUST): lane = vai trò, nét đứt = ý tưởng / lý do, nét liền = cùng một thiên thể hoặc cùng phần cứng.
Mọi mốc có bài gốc trong literature/pdf/K_Search_history (và literature/pdf/*) với đoạn nguyên văn đã kiểm trong data/literature/tess_fact_sources.csv."""
import math

LANES = [("Doppler and timing", "#ED1C24"), ("Ground transit surveys", "#0f9d58"), ("Atmospheres, follow-up", "#d98e00"), ("Space photometry", "#273896")]
Y0, Y1 = 1991.5, 2027.0
ML, W, MR = 190, 1160, 28
K = (W - ML - MR) / (Y1 - Y0)
LANE_Y = [72, 184, 296, 408]
X = lambda yr: ML + (yr - Y0) * K

# (lane, năm, tên, mô tả, quan trọng, vị trí nhãn u/d, căn nhãn l/m/r, id)
NODES = [
    (0, 1992.0, "Pulsar planets", "Wolszczan 1992", True, "u", "l", "W92"),
    (0, 1995.7, "Mayor & Queloz", "1995", True, "d", "l", "MQ"),
    (0, 2021.0, "ESPRESSO", "Pepe 2021", False, "u", "m", "ESP"),
    (1, 2000.0, "HD 209458 b", "first transits", True, "d", "r", "HD"),
    (1, 2004.0, "TrES-1, HAT", "2004", True, "u", "m", "TR"),
    (1, 2006.5, "SuperWASP", "2006", False, "d", "l", "WA"),
    (1, 2008.0, "MEarth", "2008", False, "u", "l", "ME"),
    (2, 2002.2, "HST", "sodium", False, "u", "m", "HS"),
    (2, 2005.4, "Spitzer", "2005", True, "d", "m", "SP"),
    (2, 2022.55, "JWST", "WASP-39 b", True, "u", "m", "JW"),
    (3, 2006.95, "CoRoT", "2006", False, "d", "r", "CO"),
    (3, 2009.2, "Kepler", "2009", True, "d", "m", "KP"),
    (3, 2014.0, "K2", "2014", False, "d", "r", "K2"),
    (3, 2014.0, "PLATO", "selected", False, "u", "l", "PL"),
    (3, 2018.3, "TESS", "2018", True, "d", "r", "TE"),
    (3, 2019.95, "CHEOPS", "2019", False, "d", "l", "CH"),
]
# (từ, đến, kiểu): dash = ý tưởng / lý do; solid = cùng thiên thể hoặc cùng phần cứng
LINKS = [("MQ", "HD", "dash"), ("HD", "TR", "dash"), ("HD", "WA", "dash"), ("HD", "HS", "solid"), ("TR", "SP", "solid"),
         ("KP", "K2", "solid"), ("KP", "TE", "dash"), ("TE", "JW", "dash")]
GR = "#7a8499"
# hành tinh của ta: (số, lane, năm, lệch ngang px) theo cột discoverymethod, disc_facility, disc_year của catalog
OURS = [(3, 0, 1999.0, 0, 0), (1, 0, 2005.0, -17, 0), (2, 0, 2005.0, 17, 0), (4, 1, 2009.0, 0, 0), (5, 1, 2012.0, 0, 0), (9, 1, 2015.0, 0, 0),
        (10, 3, 2018.0, -8, 0), (7, 3, 2019.0, 0, -27), (8, 3, 2019.0, 0, 27), (6, 3, 2020.0, 8, 0)]   # (số, lane, năm, dx, dy)


def _grid(svg, h_axis):
    for yr in range(1995, 2030, 5):
        if yr > 2027: break
        x = X(yr)
        svg.append(f'<line x1="{x:.1f}" y1="30" x2="{x:.1f}" y2="{h_axis - 26}" stroke="#d5dae6" stroke-width="1"/>')
        svg.append(f'<text x="{x:.1f}" y="{h_axis}" font-size="20" fill="#566074" text-anchor="middle">{yr}</text>')


def _lanes(svg, ys, x_end):
    for (name, col), y in zip(LANES, ys):
        svg.append(f'<line x1="{ML-24}" y1="{y}" x2="{x_end}" y2="{y}" stroke="{col}" stroke-width="3" opacity=".45"/>')
        parts = name.split(" ", 1) if len(name) > 14 else [name]
        words = name.split(); half = len(words) // 2 or 1
        l1, l2 = " ".join(words[:half]), " ".join(words[half:])
        if len(name) > 15:
            svg.append(f'<text x="{ML-36}" y="{y-4}" font-size="20" font-weight="700" fill="{col}" text-anchor="end">{l1}</text>'
                       f'<text x="{ML-36}" y="{y+20}" font-size="20" font-weight="700" fill="{col}" text-anchor="end">{l2}</text>')
        else:
            svg.append(f'<text x="{ML-36}" y="{y+7}" font-size="20" font-weight="700" fill="{col}" text-anchor="end">{name}</text>')


def exo_timeline_svg():
    H = 500
    svg = [f'<svg viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Timeline of exoplanet discovery in four lines of work" style="font-family:Helvetica,Arial,sans-serif">']
    svg.append('<defs>' + "".join(f'<marker id="ah{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for c in {GR, *[c for _, c in LANES]}) + '</defs>')
    _grid(svg, 488)
    x_end = X(2026.6)
    _lanes(svg, LANE_Y, x_end)
    pos = {n[7]: (X(n[1]), LANE_Y[n[0]]) for n in NODES}
    lane_of = {n[7]: n[0] for n in NODES}

    def shorten(a, b, r=12):
        dx, dy = b[0] - a[0], b[1] - a[1]; d = math.hypot(dx, dy) or 1
        return (a[0] + dx / d * r, a[1] + dy / d * r), (b[0] - dx / d * (r + 3), b[1] - dy / d * (r + 3))

    for a, b, kind in LINKS:
        col = GR if kind == "dash" else LANES[lane_of[a]][1]
        pa, pb = shorten(pos[a], pos[b])
        dash = ' stroke-dasharray="6,5"' if kind == "dash" else ""
        svg.append(f'<line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{pb[0]:.1f}" y2="{pb[1]:.1f}" stroke="{col}" stroke-width="{1.6 if kind == "dash" else 2.2}"{dash} marker-end="url(#ah{col[1:]})" opacity=".9"/>')
    for lane, yr, name, sub, key, side, al, nid in NODES:
        x, y = X(yr), LANE_Y[lane]; col = LANES[lane][1]
        svg.append(f'<circle cx="{x:.1f}" cy="{y}" r="{9 if key else 7}" fill="{col}" stroke="#fff" stroke-width="2"/>')
        anchor = {"l": "start", "m": "middle", "r": "end"}[al]; tx = x + {"l": -8, "m": 0, "r": 8}[al]
        yn, ys = (y - 40, y - 17) if side == "u" else (y + 31, y + 53)
        wbox = 11.2 * max(len(name), len(sub)) + 8
        bx = {"l": tx - 4, "m": tx - wbox / 2, "r": tx - wbox + 4}[al]
        svg.append(f'<rect x="{bx:.1f}" y="{min(yn, ys) - 22:.1f}" width="{wbox:.1f}" height="50" fill="#fff" opacity=".82" rx="3"/>')
        svg.append(f'<text x="{tx:.1f}" y="{yn}" font-size="20" font-weight="{800 if key else 700}" fill="#1b1f3b" text-anchor="{anchor}">{name}</text>')
        svg.append(f'<text x="{tx:.1f}" y="{ys}" font-size="20" fill="#566074" text-anchor="{anchor}">{sub}</text>')
    svg.append('</svg>')
    return "".join(svg)


def exo_planets_svg(width=760, height=420):
    """Phiên bản gọn: chỉ lane, trục năm và 10 hành tinh của ta (số trong vòng tròn đỏ) đặt theo năm và loại phát hiện trong catalog."""
    Wd, ml = width, 175
    k = (Wd - ml - 24) / (2022 - 1996)
    xx = lambda yr: ml + (yr - 1996) * k
    ys = [64, 150, 236]; used = [0, 1, 3]
    svg = [f'<svg viewBox="0 0 {Wd} {height}" width="{Wd}" height="{height}" role="img" aria-label="Where our ten planets were discovered" style="font-family:Helvetica,Arial,sans-serif">']
    for yr in range(1996, 2023, 4):
        x = xx(yr); svg.append(f'<line x1="{x:.1f}" y1="30" x2="{x:.1f}" y2="{height-60}" stroke="#d5dae6" stroke-width="1"/><text x="{x:.1f}" y="{height-28}" font-size="20" fill="#566074" text-anchor="middle">{yr}</text>')
    for (name, col), y in [(LANES[i], y) for i, y in zip(used, ys)]:
        svg.append(f'<line x1="{ml-24}" y1="{y}" x2="{Wd-10}" y2="{y}" stroke="{col}" stroke-width="3" opacity=".5"/>')
        words = name.split(); half = len(words) // 2
        svg.append(f'<text x="{ml-34}" y="{y-3}" font-size="20" font-weight="700" fill="{col}" text-anchor="end">{" ".join(words[:half])}</text><text x="{ml-34}" y="{y+21}" font-size="20" font-weight="700" fill="{col}" text-anchor="end">{" ".join(words[half:])}</text>')
    for num, lane, yr, dx, dy in OURS:
        x, y = xx(yr) + dx, ys[used.index(lane)] + dy
        svg.append(f'<circle cx="{x:.1f}" cy="{y}" r="15" fill="#ED1C24" stroke="#fff" stroke-width="2"/><text x="{x:.1f}" y="{y+7}" font-size="20" font-weight="700" fill="#fff" text-anchor="middle">{num}</text>')
    svg.append('</svg>')
    return "".join(svg)
