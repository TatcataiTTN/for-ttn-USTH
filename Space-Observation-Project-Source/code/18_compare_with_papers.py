# -*- coding: utf-8 -*-
"""Bước 18 - Đối chiếu kết quả đo của dự án với giá trị TÁC GIẢ CÔNG BỐ trong các PDF đã tải (literature/pdf, trích bằng pdftotext).
Mỗi giá trị công bố ghi kèm tệp nguồn và dòng/bảng trong literature/text/. Ra: results/paper_comparison.csv"""
import json
import math
import pathlib
import re
import sys

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
ROOT = pathlib.Path(__file__).resolve().parents[1]
slug = lambda n: re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_")
RJ = 11.2089          # R_Jup / R_Earth, hằng số danh định IAU (71492 / 6378.1)
RJ_RSUN = 0.102763    # R_Jup / R_Sun (71492 / 695700)

# tên | bài | P công bố (ngày) ± | Rp/R* công bố ± | Rp công bố (R_earth) ± | ghi chú về nguồn
PUB = [
    ("HD 118203 b", "Pepper+2020 (TESS), Table: Rp/R*=0.05538; abstract P=6.134980, R=1.133 RJ", 6.134980, 0.000038, 0.05538, 0.00023, 1.133 * RJ, 0.031 * RJ, "TESS, 5 transits; same data type as ours"),
    ("HD 189733 b", "Bouchy+2005 (ELODIE + 1.2 m CCD), Table: Rp/R*=0.172±0.003, R=1.26±0.03 RJ, P=2.219 d", 2.219, 0.0005, 0.172, 0.003, 1.26 * RJ, 0.03 * RJ, "discovery paper, ground-based; early value"),
    ("HD 189733 b", "Knutson+2007 (Spitzer 8 um) text: Rp/R*=0.1545±0.0002, R*=0.757±0.003 Rsun (Rp derived by us = ratio x R*)", None, None, 0.1545, 0.0002, 0.1545 * 0.757 * 109.076, 0.1545 * 0.003 * 109.076, "independent Spitzer light curve; Rp derived"),
    ("HD 209458 b", "Charbonneau+2000 abstract: R=1.27±0.02 RJ assuming R*=1.1 Rsun (ratio derived by us)", None, None, 1.27 * RJ_RSUN / 1.1, 0.02 * RJ_RSUN / 1.1, 1.27 * RJ, 0.02 * RJ, "ground-based 1999; ratio derived from R and the assumed R*"),
    ("WASP-18 b", "Shporer+2019 (TESS S2) Table: P=0.9414526, depth 9439 ppm, Rp=1.191±0.038 RJ", 0.9414526, 0.0000016, math.sqrt(9439e-6), 0.5 * 27 / 9439 * math.sqrt(9439e-6), 1.191 * RJ, 0.038 * RJ, "TESS sector 2; ratio taken as sqrt(depth)"),
    ("WASP-62 b", "Hellier+2012 Table 5: P=4.411953±0.000003, dF=Rp2/R*2=0.0123±0.0002, Rp=1.39±0.06 RJ", 4.411953, 0.000003, math.sqrt(0.0123), 0.5 * 0.0002 / 0.0123 * math.sqrt(0.0123), 1.39 * RJ, 0.06 * RJ, "WASP-South + Euler + TRAPPIST, ground-based"),
    ("LTT 9779 b", "Jenkins+2020 Table: P=0.7920520±0.0000093, Rp/R*=0.0455+0.0022 (upper error used), abstract R=4.6 Rearth", 0.7920520, 0.0000093, 0.0455, 0.0022, 4.6, 0.2, "TESS + follow-up; Rp error not printed in abstract, 0.2 assumed"),
    ("TOI-270 c", "Gunther+2019 Table: P=5.660172±0.000035, Rp/R*=0.05825+0.00079-0.00058, R=2.42±0.13 Rearth", 5.660172, 0.000035, 0.05825, 0.00069, 2.42, 0.13, "TESS + ground follow-up"),
    ("LTT 1445 A b", "Winters+2021 Table: P=5.3587657+0.0000043, Rp/R*=0.0451+0.0014 (upper error used), abstract R=1.304+0.067-0.060", 5.3587657, 0.0000043, 0.0451, 0.0014, 1.304, 0.064, "TESS + RV; their R uses their R*"),
    ("GJ 1132 b", "Berta-Thompson+2015 Table: P=1.628930±0.000031, Rp/R*=0.0512±0.0025, R=1.16±0.11 Rearth", 1.628930, 0.000031, 0.0512, 0.0025, 1.16, 0.11, "MEarth ground-based discovery"),
    ("K2-141 b", "Malavolta+2018 Table 3: P=0.2803244±0.0000015, Rp/R*=0.02037±0.00046, R=1.51±0.05 Rearth", 0.2803244, 0.0000015, 0.02037, 0.00046, 1.51, 0.05, "K2 light curve + HARPS-N"),
    ("pi Men c", "Huang+2018 abstract: P=6.27 d, R=2.04±0.05 Rearth (Gandolfi+2018: R=2.06±0.03); Rp/R* read off Fig 4 (~290 ppm, approximate)", 6.27, 0.005, math.sqrt(290e-6), 0.0010, 2.04, 0.05, "TESS S1; ratio only read off a figure, treat as approximate"),
]

rows = []
for n, src, P, Pe, ror, rore, rp, rpe, note in PUB:
    r = json.load(open(ROOT / "results" / slug(n) / "result.json")); f = r["fit"]
    d = dict(planet=n, source=src, note=note)
    d.update(ours_P=f["period"], ours_P_err=f["period_err"], pub_P=P, pub_P_err=Pe)
    if P:
        d["dP_ppm"] = 1e6 * (f["period"] - P) / P
        d["P_pull"] = (f["period"] - P) / math.hypot(f["period_err"], Pe)
    d.update(ours_ror=f["ror"], ours_ror_err=f["ror_err"], pub_ror=ror, pub_ror_err=rore,
             dror_pct=100 * (f["ror"] - ror) / ror, ror_pull=(f["ror"] - ror) / math.hypot(f["ror_err"], rore))
    d.update(ours_Rp=r["rp_rearth"], ours_Rp_err=r["rp_rearth_err"], pub_Rp=rp, pub_Rp_err=rpe, catalog_Rp=r["catalog"]["rade"],
             dRp_pct=100 * (r["rp_rearth"] - rp) / rp, Rp_pull=(r["rp_rearth"] - rp) / math.hypot(r["rp_rearth_err"], rpe),
             rstar_used=r["rstar_rsun"], rstar_implied_by_pub=rp / (ror * 109.076))
    rows.append(d)
df = pd.DataFrame(rows)
df.to_csv(ROOT / "results" / "paper_comparison.csv", index=False)
pd.set_option("display.width", 250)
print(df[["planet", "dP_ppm", "P_pull", "ours_ror", "pub_ror", "dror_pct", "ror_pull", "ours_Rp", "pub_Rp", "dRp_pct", "Rp_pull", "rstar_used", "rstar_implied_by_pub"]].round(4).to_string(index=False))


# ---- kiểm lần cuối: mọi con số công bố phải xuất hiện NGUYÊN VĂN trong văn bản PDF (literature/text/*.txt)
VERIFY = {"Pepper_2020": ["0.05538", "6.134980", "1.133"], "Bouchy_2005": ["0.172", "1.26", "2.219"], "Knutson_2007": ["0.1545", "0.757"],
          "Charbonneau_2000": ["1.27", "1.1 R"], "Shporer_2019": ["9439", "0.9414526", "1.191"], "Hellier_2012": ["0.0123", "4.411953", "1.39"],
          "Jenkins_2020": ["0.0455", "0.7920520", "4.6 R"], "Gunther_2019": ["0.05825", "5.660172", "2.42"], "Winters_2021": ["0.0451", "5.3587657", "1.304"],
          "Berta_Thompson": ["0.0512", "1.628930", "1.16"], "Malavolta_2018": ["0.02037", "0.2803244", "1.51"], "Huang_2018": ["2.04", "6.27"], "Gandolfi_2018": ["2.06", "6.27"]}
import glob
chk = []
for pre, vals in VERIFY.items():
    f = glob.glob(str(ROOT / "literature" / "text" / (pre + "*.txt")))[0]
    lines = open(f, errors="ignore").read().replace("\u2212", "-").split("\n")
    for v in vals:
        hit = next((i + 1 for i, l in enumerate(lines) if v in l), None)
        chk.append(dict(pdf_text=pathlib.Path(f).name, value=v, found=hit is not None, first_line=hit))
chk = pd.DataFrame(chk)
chk.to_csv(ROOT / "results" / "paper_value_check.csv", index=False)
print("\nso khớp chuỗi số trong PDF: %d/%d giá trị tìm thấy nguyên văn" % (chk.found.sum(), len(chk)))
print(chk[~chk.found].to_string(index=False) if (~chk.found).any() else "  không thiếu giá trị nào")
