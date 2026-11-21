# -*- coding: utf-8 -*-
"""Bước 22 - Lệch giữa kết quả của dự án và catalog NASA có "hợp lý" không? Đọc lệch theo đơn vị sai số (pull), và catalog lấy từng giá trị từ bài nào.
Đầu vào : results/*/result.json, results/results_table.csv, results/paper_comparison.csv, data/raw/catalog_methods.csv (chạy code/21_catalog_methods.py trước)
Đầu ra  : results/deviation_vs_catalog.csv, results/catalog_sources.csv, results/deviation_summary.json, figures/paper/deviation_vs_catalog.png"""
import html
import json
import pathlib
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
slug = lambda n: re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_")
NAVY, RED, GREY = "#273896", "#ED1C24", "#6b7280"
names = [l.strip() for l in open(ROOT / "data" / "selected.txt") if l.strip()]
M = pd.read_csv(ROOT / "data" / "raw" / "catalog_methods.csv").set_index("pl_name")
RT = pd.read_csv(ROOT / "results" / "results_table.csv").set_index("planet")
CMP = pd.read_csv(ROOT / "results" / "paper_comparison.csv")
unq = lambda s: html.unescape(str(s)).replace("Cortes-Zuleta", "Cortés-Zuleta").replace("Barragan", "Barragán")

rows = []
for n in names:
    r = json.load(open(ROOT / "results" / slug(n) / "result.json")); f = r["fit"]; c = M.loc[n]
    eP = np.nanmean([abs(c.pl_orbpererr1), abs(c.pl_orbpererr2)]); eT = np.nanmean([abs(c.pl_ratrorerr1), abs(c.pl_ratrorerr2)]); eR = np.nanmean([abs(c.pl_radeerr1), abs(c.pl_radeerr2)])
    sP = max(f["period_err"], r.get("period_err_sys") or 0); sT = RT.loc[n, "ror_err_total"]; sR = r["rp_rearth_err"]
    rows.append(dict(
        planet=n, mode=r["mode"], n_transits=f["n_transits"],
        period=f["period"], period_cat=c.pl_orbper, dP_ppm=1e6 * (f["period"] - c.pl_orbper) / c.pl_orbper, P_pull=(f["period"] - c.pl_orbper) / np.hypot(sP, eP),
        ratio=f["ror"], ratio_err=sT, ratio_cat=c.pl_ratror, ratio_cat_err=eT, dratio_pct=100 * (f["ror"] - c.pl_ratror) / c.pl_ratror, ratio_pull=(f["ror"] - c.pl_ratror) / np.hypot(sT, eT),
        err_ratio_pct=100 * sT / c.pl_ratror, err_ratio_cat_pct=100 * eT / c.pl_ratror,
        rp=r["rp_rearth"], rp_err=sR, rp_cat=c.pl_rade, rp_cat_err=eR, drp_pct=100 * (r["rp_rearth"] - c.pl_rade) / c.pl_rade, rp_pull=(r["rp_rearth"] - c.pl_rade) / np.hypot(sR, eR),
        rstar_used=r["rstar_rsun"], rstar_implied_by_catalog=c.pl_rade / (c.pl_ratror * 109.076)))
D = pd.DataFrame(rows)
# sai số nhân thêm beta (nhiễu đỏ, Pont+2006) từ figures/paper/figure_stats.json; beta < 1 coi là 1
RN = json.load(open(ROOT / "figures" / "paper" / "figure_stats.json"))["rednoise"]
D["beta"] = D.planet.map(lambda n: RN[n]["beta"])
D["ratio_pull_beta"] = (D.ratio - D.ratio_cat) / np.hypot(np.maximum(D.beta, 1) * D.ratio_err, D.ratio_cat_err)
D["rp_pull_beta"] = (D.rp - D.rp_cat) / np.hypot(np.maximum(D.beta, 1) * D.rp_err, D.rp_cat_err)
D.to_csv(ROOT / "results" / "deviation_vs_catalog.csv", index=False)

# --- bài nguồn của từng giá trị catalog
S = []
for n in names:
    c = M.loc[n]
    S.append(dict(planet=n, discovery_method=c.discoverymethod, disc_year=int(c.disc_year), discovery_paper=unq(c.disc_ref),
                  period_ref=unq(c.pl_orbper_ref), radius_ref=unq(c.pl_rade_ref), ratio_ref=unq(c.pl_ratror_ref), rstar_ref=unq(c.st_rad_ref)))
S = pd.DataFrame(S)
S["ratio_and_radius_from_different_papers"] = S.ratio_ref != S.radius_ref
S.to_csv(ROOT / "results" / "catalog_sources.csv", index=False)

def key(s):      # (4 chữ cái đầu của tác giả đầu, năm): "Bouchy Et Al  2005" và "Bouchy et al. 2005" cùng một khóa
    s = re.sub(r"[^a-z0-9 ]", "", str(s).lower().replace("_", " ")); m = re.match(r"\s*([a-z]+).*?(\d{4})", s)
    return (m.group(1)[:4], m.group(2)) if m else None


summ = dict(
    ratio_abs_min=float(D.dratio_pct.abs().min()), ratio_abs_max=float(D.dratio_pct.abs().max()), rp_abs_min=float(D.drp_pct.abs().min()), rp_abs_max=float(D.drp_pct.abs().max()),
    n_ratio_within2=int((D.ratio_pull.abs() < 2).sum()), n_ratio_within2_beta=int((D.ratio_pull_beta.abs() < 2).sum()), ratio_outside2_beta=D.loc[D.ratio_pull_beta.abs() >= 2, "planet"].tolist(), n_rp_within2=int((D.rp_pull.abs() < 2).sum()), n_period_within2=int((D.P_pull.abs() < 2).sum()),
    ratio_outside2=D.loc[D.ratio_pull.abs() >= 2, "planet"].tolist(), period_outside2=D.loc[D.P_pull.abs() >= 2, "planet"].tolist(),
    n_mixed_sources=int(S.ratio_and_radius_from_different_papers.sum()), mixed=S.loc[S.ratio_and_radius_from_different_papers, "planet"].tolist(),
    n_from_discovery_paper=int(S.apply(lambda r: any(key(r.discovery_paper) == key(r[c]) for c in ("period_ref", "radius_ref", "ratio_ref", "rstar_ref")), axis=1).sum()),
    from_discovery_paper=S.loc[S.apply(lambda r: any(key(r.discovery_paper) == key(r[c]) for c in ("period_ref", "radius_ref", "ratio_ref", "rstar_ref")), axis=1), "planet"].tolist(),
    n_planets=len(D))
json.dump(summ, open(ROOT / "results" / "deviation_summary.json", "w"), indent=1, ensure_ascii=False)

# --- hình: lệch của Rp/R* so với catalog, kết quả của dự án (tròn) và các bài báo đã đọc (thoi); chữ >= 14.4 pt, đúng 740 px
plt.rcParams.update({"font.size": 15, "axes.labelsize": 15, "xtick.labelsize": 14.5, "ytick.labelsize": 14.5, "legend.fontsize": 14.5, "figure.dpi": 100, "savefig.dpi": 100})
pubs = CMP[CMP.planet.isin(names)].copy()
pubs["cat"] = pubs.planet.map(M.pl_ratror)
pubs["d"] = 100 * (pubs.pub_ror - pubs.cat) / pubs.cat
pubs["e"] = 100 * pubs.pub_ror_err / pubs.cat
fig, ax = plt.subplots(figsize=(7.4, 5.1), constrained_layout=True)
ax.axvline(0, color=GREY, lw=1.5, zorder=1)
for i, r in D.iterrows():
    ax.errorbar(r.dratio_pct, i - 0.16, xerr=r.err_ratio_pct, fmt="o", color=NAVY, ms=8, lw=2, capsize=3, zorder=3, label="This project (TESS)" if i == 0 else None)
    for j, p in pubs[pubs.planet == r.planet].iterrows():
        ax.errorbar(p.d, i + 0.2, xerr=p.e, fmt="D", mfc="white", mec=RED, color=RED, ms=7, lw=1.8, capsize=3, zorder=2, label="Published paper" if (i == 0 and j == pubs.index[pubs.planet == r.planet][0]) else None)
    ax.text(1.015, i, f"{r.ratio_pull:+.1f}σ", transform=ax.get_yaxis_transform(), va="center", ha="left", fontsize=14.5, color=RED if abs(r.ratio_pull) >= 2 else "black", fontweight="bold" if abs(r.ratio_pull) >= 2 else "normal")
ax.text(1.015, -0.75, "pull", transform=ax.get_yaxis_transform(), va="center", ha="left", fontsize=14.5, color=GREY)
ax.set_yticks(range(len(D))); ax.set_yticklabels(D.planet); ax.set_ylim(len(D) - 0.4, -1.0)
ax.set_xlim(-18, 15); ax.set_xlabel("Difference from catalog $R_p/R_\\star$ (%)")
ax.grid(axis="x", alpha=0.3)
h, l = ax.get_legend_handles_labels()
ax.legend(h, l, loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=2, frameon=False, handletextpad=0.4, columnspacing=1.2)
fig.savefig(ROOT / "figures" / "paper" / "deviation_vs_catalog.png"); plt.close(fig)

pd.set_option("display.width", 250)
print(D[["planet", "dratio_pct", "ratio_pull", "drp_pct", "rp_pull", "dP_ppm", "P_pull"]].round(2).to_string(index=False))
print(json.dumps(summ, ensure_ascii=False, indent=1))
print(pubs[["planet", "source", "pub_ror", "cat", "d", "e"]].assign(source=pubs.source.str[:28]).round(4).to_string(index=False))
