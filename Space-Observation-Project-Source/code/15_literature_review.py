# -*- coding: utf-8 -*-
"""Bước 15 - Literature review TESS theo nhóm phương pháp: notes/literature_review_TESS.md + figures/paper/lit_map.png.
Đầu vào: data/literature/verified_curated.csv (đã kiểm chứng), data/literature/downloaded.csv (PDF tải được)."""
import csv
import pathlib
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lit_content import GROUPS, USED

ROOT = pathlib.Path(__file__).resolve().parents[1]
L = ROOT / "data" / "literature"
rows = list(csv.DictReader(open(L / "verified_curated.csv")))
dl = {r["ref"]: r for r in csv.DictReader(open(L / "downloaded.csv"))}
for r in rows:
    d = dl.get(r["ref"])
    r["pdf"] = d["file"] if d and d["status"] in ("OK", "already") else ""
    r["key"] = r["group"][0]
    r["used"] = USED.get((r["first_author"], str(r["year"])), "")
    r["title_clean"] = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", r["title"])).strip()
rows.sort(key=lambda r: (r["key"], int(r["year"]), r["first_author"]))
NAVY, RED = "#273896", "#ED1C24"

# ---- hình bản đồ literature
plt.rcParams.update({"font.size": 15, "axes.labelsize": 15, "xtick.labelsize": 14.5, "ytick.labelsize": 14.5, "figure.dpi": 100, "savefig.dpi": 100})
keys = sorted(GROUPS)
cnt = [sum(r["key"] == k for r in rows) for k in keys]
fig, axs = plt.subplots(1, 2, figsize=(11.6, 3.9), constrained_layout=True, gridspec_kw=dict(width_ratios=[1, 1.5]))
axs[0].barh(range(len(keys)), cnt, color=NAVY)
axs[0].set_yticks(range(len(keys))); axs[0].set_yticklabels(keys); axs[0].invert_yaxis()
for i, c in enumerate(cnt):
    axs[0].text(c + 0.3, i, str(c), va="center", fontsize=14)
axs[0].set(xlabel="Verified papers per sub-method", xlim=(0, max(cnt) * 1.18))
rng = np.random.default_rng(3)
for r in rows:
    y = keys.index(r["key"])
    u = bool(r["used"])
    axs[1].scatter(int(r["year"]) + rng.uniform(-0.25, 0.25), y + rng.uniform(-0.28, 0.28), s=46 if not u else 80, color=RED if u else NAVY, alpha=0.8, edgecolor="white", linewidth=0.5)
axs[1].set_yticks(range(len(keys))); axs[1].set_yticklabels(keys); axs[1].invert_yaxis()
axs[1].set(xlabel="Publication year (red: used in this project)", xlim=(1990, 2027))
fig.savefig(ROOT / "figures" / "paper" / "lit_map.png")
plt.close(fig)

# ---- markdown
n_pdf = sum(bool(r["pdf"]) for r in rows)
md = ["# Literature review: TESS transit photometry, by sub-method", "",
      f"{len(rows)} papers, each checked on arXiv or Crossref (first-author surname and title overlap); {n_pdf} open-access PDFs downloaded to `literature/pdf/<group>/`.",
      "Papers not found on arXiv or open access are listed without a PDF; none was fetched around a paywall. Candidates that could not be verified were dropped (McQuillan 2014, Lissauer 2012, Parmentier 2018, Montalto 2020, Cameron 2012, Winters 2019).", ""]
for k in keys:
    title, blurb, subs = GROUPS[k]
    md += [f"## {re.sub('<[^>]+>', '', title)}", "", re.sub("<[^>]+>|&[a-z#0-9]+;", "", blurb), "", "Sub-methods: " + "; ".join(re.sub("<[^>]+>|&[a-z#0-9]+;", "", s) for s in subs) + ".", "",
           "| Year | First author | Title | Reference | Used in this project | PDF |", "|---|---|---|---|---|---|"]
    for r in rows:
        if r["key"] != k:
            continue
        ref = re.sub(r"v\d+$", "", r["ref"])
        md.append(f"| {r['year']} | {r['first_author']} | {r['title_clean']} | {ref} | {r['used']} | {r['pdf'] or 'no open PDF'} |")
    md.append("")
(ROOT / "notes").mkdir(exist_ok=True)
(ROOT / "notes" / "literature_review_TESS.md").write_text("\n".join(md), encoding="utf-8")
print(len(rows), "bài;", n_pdf, "PDF;", {k: c for k, c in zip(keys, cnt)})
