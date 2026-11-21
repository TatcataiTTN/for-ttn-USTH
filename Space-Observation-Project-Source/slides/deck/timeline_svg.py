# -*- coding: utf-8 -*-
"""Timeline NHIỀU LANE bằng SVG thuần (không drawio), phỏng mẫu TikZ trong Slides_HuongA_AITPACK.tex:
 mỗi lane = 1 nhánh công nghệ (đường ngang), mốc tròn đặt theo năm, nhãn trên/dưới, nét đứt = ảnh hưởng ý tưởng,
 nét liền = phụ thuộc lúc chạy. Dùng thẳng trong f-string của slide: {lane_timeline_svg(...)}.

nodes: dict key -> (lane, năm(float được), tên, mô tả, key_node(bool), dx, hướng 'u'|'d', căn 'c'|'l'|'r', lệch_nhãn_x)
links: [(từ_key, đến_key, 'dash'|'solid', '#màu')]
Quy tắc đã rút ra từ lần vẽ thật:
 - Khoảng cách tối thiểu giữa 2 nhãn cùng phía ≈ 1,6 năm với step=64; gần hơn thì đổi phía (u/d) hoặc căn l/r, hoặc dùng dx ±8 cho 2 mốc cùng năm.
 - Nhãn có nền mờ (color-mix) để đường nối chạy phía sau không cắt chữ.
 - Đường nối đi từ lane trên xuống lane dưới thì KHÔNG đặt nhãn 'd' của lane trên ngay dưới mốc nguồn.
 - Thang năm có thể đứt: truyền tick_labels và nhét mốc xa (vd 2022) vào sau dấu '⋯'.
"""
import math

def lane_timeline_svg(lanes, nodes, links, y0, y1, ml=150, step=64, lane_gap=96, top=72, extra_ticks=None):
    def X(year): return ml + (year - y0) * step
    for i, ln in enumerate(lanes): ln.setdefault("y", top + i * lane_gap)
    H = lanes[-1]["y"] + 110
    W = X(y1) + 150
    def pos(k):
        n = nodes[k]; return X(n[1]) + n[5], lanes[n[0]]["y"]
    cols = sorted({c for _, _, _, c in links})
    s = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img">']
    s.append("<defs>" + "".join(f'<marker id="ah{c[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                                f'orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>' for c in cols) + "</defs>")
    for yr in range(int(y0), int(y1)):
        x = X(yr)
        s.append(f'<line x1="{x}" y1="36" x2="{x}" y2="{H-60}" stroke="var(--border)"/>')
        s.append(f'<text x="{x}" y="{H-30}" font-size="13" fill="var(--muted)" text-anchor="middle">{yr}</text>')
    for yr, lab in (extra_ticks or []):
        s.append(f'<text x="{X(yr)}" y="{H-30}" font-size="13" fill="var(--muted)" text-anchor="middle">{lab}</text>')
    xend = X(max([n[1] for n in nodes.values()] + [y1])) + 30
    for ln in lanes:
        s.append(f'<line x1="{ml-20}" y1="{ln["y"]}" x2="{xend}" y2="{ln["y"]}" stroke="{ln["color"]}" stroke-width="2.5" opacity=".5"/>')
        s.append(f'<foreignObject x="0" y="{ln["y"]-24}" width="{ml-30}" height="48"><div xmlns="http://www.w3.org/1999/xhtml" '
                 f'style="font:700 14px sans-serif;color:{ln["color"]};text-align:right;line-height:1.25;height:48px;display:flex;'
                 f'align-items:center;justify-content:flex-end"><span>{ln["label"]}</span></div></foreignObject>')
    def shorten(a, b, r=11):
        dx, dy = b[0]-a[0], b[1]-a[1]; d = math.hypot(dx, dy) or 1
        return (a[0]+dx/d*r, a[1]+dy/d*r), (b[0]-dx/d*(r+2), b[1]-dy/d*(r+2))
    for a, b, kind, col in links:
        pa, pb = shorten(pos(a), pos(b))
        s.append(f'<line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{pb[0]:.1f}" y2="{pb[1]:.1f}" stroke="{col}" '
                 f'stroke-width="{1.4 if kind=="dash" else 1.8}"{" stroke-dasharray=\"5,4\"" if kind=="dash" else ""} opacity=".85" marker-end="url(#ah{col[1:]})"/>')
    for k, (li, year, name, sub, key, dx, side, al, lx) in nodes.items():
        ln = lanes[li]; x = X(year) + dx; y = ln["y"]
        s.append(f'<circle cx="{x}" cy="{y}" r="{8 if key else 6}" fill="{ln["color"]}" stroke="var(--panel)" stroke-width="2"/>')
        bw = 150; bx = {"c": x-bw/2, "l": x-6+lx, "r": x-bw+6}[al]
        ta = {"c": "center", "l": "left", "r": "right"}[al]; ai = {"c": "center", "l": "flex-start", "r": "flex-end"}[al]
        by, just = (y-12-52, "flex-end") if side == "u" else (y+12, "flex-start")
        s.append(f'<foreignObject x="{bx}" y="{by}" width="{bw}" height="52"><div xmlns="http://www.w3.org/1999/xhtml" style="height:52px;'
                 f'display:flex;flex-direction:column;justify-content:{just};align-items:{ai};text-align:{ta};font-family:sans-serif">'
                 f'<div style="background:color-mix(in srgb,var(--panel) 90%,transparent);padding:0 3px;border-radius:3px">'
                 f'<div style="font-weight:{"800" if key else "700"};font-size:{"15" if key else "13.5"}px;color:var(--text);line-height:1.15">{name}</div>'
                 f'<div style="font-size:11.5px;color:var(--muted);line-height:1.2">{sub}</div></div></div></foreignObject>')
    s.append("</svg>")
    return "".join(s)

if __name__ == "__main__":      # ví dụ chạy thử: python3 timeline_svg.py > t.svg
    lanes = [{"label": "Nghiên cứu", "color": "#2b5ce6"}, {"label": "Hệ thống", "color": "#0f9d58"}]
    nodes = {"A": (0, 2003, "Paper A", "Hội nghị 2003", True, 0, "u", "c", 0), "B": (1, 2006, "Hệ thống B", "Mã nguồn mở", True, 0, "d", "c", 0)}
    print(lane_timeline_svg(lanes, nodes, [("A", "B", "dash", "#7a8499")], 2002, 2010))
