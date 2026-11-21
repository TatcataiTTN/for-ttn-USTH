# -*- coding: utf-8 -*-
"""Bước 19 - Tạo literature/checking/: bản SAO của các PDF có nhắc tới 11 hành tinh, đã ghi chú:
  - bôi VÀNG mọi lần xuất hiện tên hành tinh
  - bôi XANH (khớp) / ĐỎ (lệch >= 2 sigma) các giá trị tác giả công bố, có comment: số công bố, số của mình, độ lệch, nhận xét
  - sticky note ở trang 1 tóm tắt hành tinh nào xuất hiện bao nhiêu lần và kết luận
Bản gốc trong literature/pdf/ không bị sửa. Chạy: python -I code/19_annotate_pdfs.py  (PDF tải về là dữ liệu không tin cậy, chỉ đọc/ghi chú bằng PyMuPDF)."""
import csv
import json
import math
import pathlib
import re

import pandas as pd
import pymupdf

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "literature" / "checking"
OUT.mkdir(parents=True, exist_ok=True)
slug = lambda n: re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_")
YELLOW, GREEN, RED = (1, 1, 0), (0.55, 0.9, 0.55), (1, 0.55, 0.55)
AUTHOR = "Group 2 check"

NAMES = {
    "HD 118203 b": ["HD 118203", "HD118203"], "HD 189733 b": ["HD 189733", "HD189733"], "HD 209458 b": ["HD 209458", "HD209458"],
    "WASP-18 b": ["WASP-18", "WASP 18"], "WASP-62 b": ["WASP-62", "WASP 62"], "LTT 9779 b": ["LTT 9779", "LTT9779"],
    "TOI-270 c": ["TOI-270", "TOI 270", "TOI270"], "LTT 1445 A b": ["LTT 1445", "LTT1445"], "GJ 1132 b": ["GJ 1132", "GJ1132"],
    "K2-141 b": ["K2-141", "K2 141"], "pi Men c": ["π Men", "pi Men", "HD 39091", "HD39091", "TOI 144", "TOI-144"],
}
cmp_ = pd.read_csv(ROOT / "results" / "paper_comparison.csv")
RES = {n: json.load(open(ROOT / "results" / slug(n) / "result.json")) for n in NAMES}

# tiền tố tên PDF -> [(chuỗi cần tìm, đại lượng, hành tinh, tiền tố cột 'source' trong paper_comparison.csv)]
VAL = {
    "Pepper_2020": [("0.05538", "ror", "HD 118203 b", "Pepper"), ("6.134980", "P", "HD 118203 b", "Pepper"), ("1.133", "Rp", "HD 118203 b", "Pepper")],
    "Bouchy_2005": [("0.172", "ror", "HD 189733 b", "Bouchy"), ("1.26", "Rp", "HD 189733 b", "Bouchy"), ("2.219", "P", "HD 189733 b", "Bouchy")],
    "Knutson_2007": [("0.1545", "ror", "HD 189733 b", "Knutson")],
    "Charbonneau_2000": [("1.27", "Rp", "HD 209458 b", "Charbonneau")],
    "Shporer_2019": [("9439", "ror", "WASP-18 b", "Shporer"), ("0.9414526", "P", "WASP-18 b", "Shporer"), ("1.191", "Rp", "WASP-18 b", "Shporer")],
    "Hellier_2012": [("0.0123", "ror", "WASP-62 b", "Hellier"), ("4.411953", "P", "WASP-62 b", "Hellier"), ("1.39", "Rp", "WASP-62 b", "Hellier")],
    "Jenkins_2020": [("0.0455", "ror", "LTT 9779 b", "Jenkins"), ("0.7920520", "P", "LTT 9779 b", "Jenkins"), ("4.6 R", "Rp", "LTT 9779 b", "Jenkins")],
    "Gunther_2019": [("0.05825", "ror", "TOI-270 c", "Gunther"), ("5.660172", "P", "TOI-270 c", "Gunther"), ("2.42", "Rp", "TOI-270 c", "Gunther")],
    "Winters_2021": [("0.0451", "ror", "LTT 1445 A b", "Winters"), ("5.3587657", "P", "LTT 1445 A b", "Winters"), ("1.304", "Rp", "LTT 1445 A b", "Winters")],
    "Berta_Thompson": [("0.0512", "ror", "GJ 1132 b", "Berta"), ("1.628930", "P", "GJ 1132 b", "Berta"), ("1.16", "Rp", "GJ 1132 b", "Berta")],
    "Malavolta_2018": [("0.02037", "ror", "K2-141 b", "Malavolta"), ("0.2803244", "P", "K2-141 b", "Malavolta"), ("1.51", "Rp", "K2-141 b", "Malavolta")],
    "Huang_2018": [("2.04", "Rp", "pi Men c", "Huang"), ("6.27", "P", "pi Men c", "Huang")],
    "1809.05967v2": [("2.04", "Rp", "pi Men c", "Huang"), ("6.27", "P", "pi Men c", "Huang")],
    "Gandolfi_2018": [("2.06", "Rp", "pi Men c", "GANDOLFI"), ("6.27", "P", "pi Men c", "GANDOLFI")],
}
EXPLAIN = {   # lời giải thích đã kiểm bằng số cho các độ lệch lớn
    ("HD 189733 b", "Bouchy", "ror"): "Bouchy+2005 is the discovery paper (ground-based CCD). The independent Spitzer value in Knutson+2007 is 0.1545 +-0.0002 and agrees with ours; NASA catalog 0.15534. The 2005 ratio looks too large, not our value.",
    ("HD 189733 b", "Bouchy", "Rp"): "Same cause as the ratio: 1.26 RJ is the 2005 discovery value. Knutson+2007 radius (ratio x R*) = 12.76 Rearth agrees with ours.",
    ("HD 209458 b", "Charbonneau", "Rp"): "Radius differs because R* differs, not the light curve: the paper ASSUMES R*=1.1 Rsun, the archive value we use is 1.19 Rsun. The ratio Rp/R* (derived) differs only +2.2 %.",
    ("WASP-18 b", "Shporer", "ror"): "Ratio is +1.5 % above sqrt(depth); with the paper's tiny error this is formally 5 sigma. Different data (their TESS sector 2 of 2018, ours sectors 103-106 of 2026), no per-point red-noise correction in our error (beta=2.1). Unresolved; radius still agrees (+1.1 sigma).",
    ("WASP-18 b", "Shporer", "Rp"): "Radius differs by +6 % but this is only 1.1 sigma because R* has a 5 % error.",
    ("pi Men c", "Huang", "Rp"): "Radius agrees (-0.5 %) but by two offsets that cancel: our ratio is ~6.6 % lower than the paper's (read off Fig 4, ~290 ppm) while our R* (archive 1.17) is 6.5 % higher than the paper's 1.10.",
    ("pi Men c", "GANDOLFI", "Rp"): "Gandolfi+2018 finds 2.06 +-0.03 Rearth with their own stellar radius; ours 2.03 +-0.07 agrees within 0.4 sigma.",
}
GUIDED = {n for n in NAMES if RES[n]["mode"] == "guided"}


def verdict(pull):
    return ("CONSISTENT" if abs(pull) < 2 else "DEVIATION") + f" ({pull:+.1f} sigma)"


def comment(pl, key, qty):
    r = RES[pl]
    if key == "GANDOLFI":
        pub, pe = (2.06, 0.03) if qty == "Rp" else (6.27, 0.005)
        ours, oe = (r["rp_rearth"], r["rp_rearth_err"]) if qty == "Rp" else (r["fit"]["period"], r["fit"]["period_err"])
        d = 100 * (ours - pub) / pub; pull = (ours - pub) / math.hypot(oe, pe)
        fmt = (lambda x: f"{x:.2f}") if qty == "Rp" else (lambda x: f"{x:.5f}")
        extra = EXPLAIN.get((pl, key, qty), "")
        return f"[{pl}] published {qty} = {fmt(pub)} +-{pe}. OURS = {fmt(ours)} +-{oe:.3g}. diff = {d:+.2f} %. {verdict(pull)}. {extra}"
    row = cmp_[(cmp_.planet == pl) & cmp_.source.str.startswith(key)].iloc[0]
    if qty == "P":
        pub, pe, ours, oe = row.pub_P, row.pub_P_err, row.ours_P, row.ours_P_err
        d, pull, unit = 1e6 * (ours - pub) / pub, row.P_pull, "ppm"
        fmt = lambda x: f"{x:.7g}"
    elif qty == "ror":
        pub, pe, ours, oe = row.pub_ror, row.pub_ror_err, row.ours_ror, row.ours_ror_err
        d, pull, unit = row.dror_pct, row.ror_pull, "%"
        fmt = lambda x: f"{x:.5f}"
    else:
        pub, pe, ours, oe = row.pub_Rp, row.pub_Rp_err, row.ours_Rp, row.ours_Rp_err
        d, pull, unit = row.dRp_pct, row.Rp_pull, "%"
        fmt = lambda x: f"{x:.3f}"
    mode = " (guided search: search window uses the catalog period, not independent)" if pl in GUIDED else ""
    extra = EXPLAIN.get((pl, key, qty), "")
    names_ = {"P": "period (d)", "ror": "Rp/R*", "Rp": "Rp (Rearth)"}[qty]
    return (f"[{pl}] published {names_} = {fmt(pub)} +-{pe:.2g}. OURS (TESS, our pipeline) = {fmt(ours)} +-{oe:.2g}. "
            f"diff = {d:+.2f} {unit}. {verdict(pull)}{mode}. {extra}")


def _norm(w):
    return w.strip(".,;:()[]{}\"'“”‘’").replace("\u2212", "-").replace("\u2013", "-").replace("\u2010", "-").replace("\u2011", "-")


def find_words(words, text, number=False):
    """Khớp theo từ trên cùng một dòng; trả về hộp hợp nhất. Từ cuối không được dính tiếp chữ số ('WASP-18' không khớp 'WASP-180')."""
    toks = text.split()
    n = len(toks)
    out = []
    for i in range(len(words) - n + 1):
        seq = words[i:i + n]
        if len({(w[5], w[6]) for w in seq}) != 1:
            continue
        ok = True
        for j, (w, t) in enumerate(zip(seq, toks)):
            nw = _norm(w[4])
            if j < n - 1:
                ok = ok and nw == t
            elif number and re.fullmatch(r"[0-9.]+", t):
                ok = ok and re.search(r"(?<![0-9.])" + re.escape(t) + r"(?![0-9])", nw) is not None
            else:
                ok = ok and re.match(re.escape(t) + r"(?![0-9])", nw) is not None
        if ok:
            r = pymupdf.Rect(seq[0][:4])
            for w in seq[1:]:
                r |= pymupdf.Rect(w[:4])
            out.append(r)
    return out


def hits(page, strings, limit=None):
    words = page.get_text("words")
    out = []
    for s_ in strings:
        out += find_words(words, s_)
    return out[:limit] if limit else out


index = []
pdfs = sorted((ROOT / "literature" / "pdf").glob("*/*.pdf")) + [ROOT / "inputs" / "papers" / "1809.05967v2.pdf"]
for src in pdfs:
    doc = pymupdf.open(src)
    counts = {n: 0 for n in NAMES}
    for page in doc:
        for pl, strs in NAMES.items():
            rects = hits(page, strs)
            if rects:
                a = page.add_highlight_annot(rects)
                a.set_colors(stroke=YELLOW); a.set_info(title=AUTHOR, content=f"planet: {pl}"); a.update()
                counts[pl] += len(rects)
    found = {n: c for n, c in counts.items() if c}
    if not found:
        doc.close(); continue
    # giá trị công bố
    nval = 0; verdicts = []
    pre = next((k for k in VAL if src.stem.startswith(k)), None)
    if pre:
        for page in doc:
            for s, qty, pl, key in VAL[pre]:
                rects = find_words(page.get_text("words"), s, number=True)[:3]
                if not rects or sum(1 for v in verdicts if v[0][0] == s) >= 2:      # mỗi giá trị chỉ đánh dấu ở 2 trang đầu có nó
                    continue
                text = comment(pl, key, qty)
                a = page.add_highlight_annot(rects)
                a.set_colors(stroke=GREEN if "CONSISTENT" in text else RED); a.set_info(title=AUTHOR, content=text); a.update()
                p0 = rects[0]
                n = page.add_text_annot(pymupdf.Point(page.rect.width - 30, max(p0.y0, 20)), text, icon="Comment")
                n.set_info(title=AUTHOR, content=text); n.update()
                verdicts.append(((s, page.number), pl, qty, "CONSISTENT" in text)); nval += 1
    # note tổng hợp trang 1
    lines = ["GROUP 2 CHECK (copy; original untouched in literature/pdf/)",
             "Planets found (yellow highlight): " + ", ".join(f"{n} x{c}" for n, c in found.items())]
    if verdicts:
        ok = sum(v[3] for v in verdicts)
        lines.append(f"Published values compared with ours: {len(verdicts)} marked (green = consistent within 2 sigma: {ok}; red = deviation: {len(verdicts)-ok}). Click each marked number for the comment.")
    else:
        lines.append("Mentions only: this paper gives no parameter we compare against.")
    note = doc[0].add_text_annot(pymupdf.Point(20, 20), "\n".join(lines), icon="Note")
    note.set_info(title=AUTHOR, content="\n".join(lines)); note.update()
    dst = OUT / ("" if src.stem == "1809.05967v2" else src.parent.name) / (src.name if src.stem != "1809.05967v2" else "1809.05967v2_Huang2018_pi_Men_checked.pdf")
    dst.parent.mkdir(parents=True, exist_ok=True)
    doc.save(dst, garbage=3, deflate=True)
    doc.close()
    index.append(dict(file=str(dst.relative_to(ROOT)), planets="; ".join(f"{n}:{c}" for n, c in found.items()), values_marked=nval,
                      consistent=sum(v[3] for v in verdicts), deviation=sum(not v[3] for v in verdicts)))
    print(f"{src.name[:55]:55s} {len(found):2d} planets, {nval} values marked")

with open(OUT / "INDEX.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["file", "planets", "values_marked", "consistent", "deviation"]); w.writeheader(); w.writerows(index)
print(len(index), "PDF đã ghi chú ->", OUT)
