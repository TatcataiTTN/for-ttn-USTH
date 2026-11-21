"""Bước 5 - Hình tổng quan (nhóm hóa) cho deck: R-P, bản đồ bầu trời hoàng đạo, khoảng cách - loại sao.
Đọc: data/raw/tess_catalog.csv, data/candidates_grouped.csv, data/selected.txt (thứ tự = số hiệu 1..N)
Ra:  figures/ov_radius_period.png, ov_sky_map.png, ov_distance_star.png (kích thước đúng px của ô slide)
"""
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[0]))
ROOT = pathlib.Path(__file__).resolve().parents[1]
STYLE = dict(base=15, tick=14.5)
plt.rcParams.update({"font.size": 15, "axes.labelsize": 15, "xtick.labelsize": 14.5, "ytick.labelsize": 14.5,
                     "figure.dpi": 100, "savefig.dpi": 100, "legend.fontsize": 14.5})

NAVY, RED = "#273896", "#ED1C24"
cat = pd.read_csv(ROOT / "data" / "raw" / "tess_catalog.csv")
pool = pd.read_csv(ROOT / "data" / "candidates_grouped.csv")
sel_names = [l.strip() for l in open(ROOT / "data" / "selected.txt") if l.strip()]
sel = pd.concat([cat[cat.pl_name == n].iloc[:1] for n in sel_names]).reset_index(drop=True)
sel["num"] = np.arange(1, len(sel) + 1)
OUT = ROOT / "figures"


def number_markers(ax, x, y, nums, fs=12.5, **kw):
    for xi, yi, n in zip(x, y, nums):
        ax.scatter([xi], [yi], s=330, color=RED, edgecolor="white", linewidth=1.5, zorder=5, **kw)
        ax.text(xi, yi, str(n), ha="center", va="center", color="white", fontsize=fs, fontweight="bold", zorder=6)


# ---------------------------------------------------------------- 1) bán kính - chu kỳ
fig, ax = plt.subplots(figsize=(11.6, 5.3), constrained_layout=True)
ok = cat.dropna(subset=["pl_rade", "pl_orbper"])
ax.scatter(ok.pl_orbper, ok.pl_rade, s=6, color="0.78", label=f"All with TIC ({len(ok)})", zorder=1)
ax.scatter(pool.pl_orbper, pool.pl_rade, s=14, color=NAVY, alpha=0.55, label=f"Measurable ({len(pool)})", zorder=2)
for y, lab in [(1.25, "Earth"), (2.0, "Super-Earth"), (4.0, "Sub-Neptune"), (8.0, "Neptune/Saturn")]:
    ax.axhline(y, color="0.6", lw=0.8, ls="--", zorder=0)
for x in [1, 3, 7]:
    ax.axvline(x, color="0.6", lw=0.8, ls="--", zorder=0)
number_markers(ax, sel.pl_orbper, sel.pl_rade, sel.num)
ax.set(xscale="log", yscale="log", xlim=(0.22, 40), ylim=(0.7, 30),
       xlabel="Orbital period (days)", ylabel="Planet radius (R$_\\oplus$)")
ax.set_xticks([0.3, 1, 3, 10, 30]); ax.set_xticklabels(["0.3", "1", "3", "10", "30"])
ax.set_yticks([1, 2, 4, 8, 16]); ax.set_yticklabels(["1", "2", "4", "8", "16"])
for y, t in [(0.95, "Earth-size"), (1.6, "Super-Earth"), (2.8, "Sub-Neptune"), (5.6, "Neptune/Saturn"), (20, "Jupiter-size")]:
    ax.text(0.235, y, t, fontsize=13.5, color="0.35", va="center")
for x, t in [(0.58, "USP"), (1.7, "Hot"), (4.6, "Warm"), (17, "Cool")]:
    ax.text(x, 0.76, t, fontsize=13.5, color="0.35", ha="center")
ax.legend(loc="lower right", frameon=True, bbox_to_anchor=(1.0, 0.1), fontsize=14.4, borderpad=0.4, labelspacing=0.3, handletextpad=0.2)
fig.savefig(OUT / "ov_radius_period.png"); plt.close(fig)

# ---------------------------------------------------------------- 2) bản đồ bầu trời (hoàng đạo)
fig = plt.figure(figsize=(11.6, 5.3), constrained_layout=True)
ax = fig.add_subplot(111, projection="mollweide")
def lon(e):  # elon 0..360 -> -pi..pi
    return np.radians(((e + 180) % 360) - 180)
oks = cat.dropna(subset=["elon", "elat"])
ax.scatter(lon(oks.elon), np.radians(oks.elat), s=3, color="0.75", zorder=1)
ax.scatter(lon(pool.elon), np.radians(pool.elat), s=10, color=NAVY, alpha=0.6, zorder=2)
for sgn in (+1, -1):                                   # vùng quan sát liên tục (CVZ) |β| > 78°
    th = np.linspace(-np.pi, np.pi, 100)
    ax.fill_between(th, np.radians(78) * sgn, np.radians(90) * sgn, color=RED, alpha=0.12, zorder=0)
ax.axhline(0, color="0.5", lw=1, zorder=0)
number_markers(ax, lon(sel.elon), np.radians(sel.elat), sel.num, fs=11.5)
ax.grid(True, color="0.85")
ax.set_xticklabels([]); ax.set_yticks(np.radians([-60, -30, 0, 30, 60])); ax.set_yticklabels([f"{d}°" for d in (-60, -30, 0, 30, 60)])
ax.text(np.radians(-125), np.radians(80), "CVZ north (|β|>78°)", ha="center", va="center", fontsize=13, color=RED)
ax.text(np.radians(-125), np.radians(-80), "CVZ south", ha="center", va="center", fontsize=13, color=RED)
fig.savefig(OUT / "ov_sky_map.png"); plt.close(fig)

# ---------------------------------------------------------------- 3) khoảng cách - loại sao
fig, ax = plt.subplots(figsize=(11.6, 5.3), constrained_layout=True)
ok = cat.dropna(subset=["st_teff", "sy_dist"])
ax.scatter(ok.st_teff, ok.sy_dist, s=5, color="0.78", zorder=1)
ax.scatter(pool.st_teff, pool.sy_dist, s=12, color=NAVY, alpha=0.55, zorder=2)
for x in (3900, 5200, 6000):
    ax.axvline(x, color="0.6", lw=0.8, ls="--")
for x, t in [(3150, "M"), (4500, "K"), (5600, "G"), (7500, "F / hotter")]:
    ax.text(x, 3000, t, ha="center", fontsize=15, color="0.35", fontweight="bold")
for y in (50, 150):
    ax.axhline(y, color="0.6", lw=0.8, ls="--")
number_markers(ax, sel.st_teff, sel.sy_dist, sel.num)
ax.set(yscale="log", xlim=(2800, 9800), ylim=(5, 4500),
       xlabel="Host star effective temperature (K)", ylabel="Distance (pc)")
ax.set_yticks([10, 50, 150, 500, 2000]); ax.set_yticklabels(["10", "50", "150", "500", "2000"])
fig.savefig(OUT / "ov_distance_star.png"); plt.close(fig)
print("ok", len(sel), "hành tinh được đánh số")
