"""Bước 6 - Hình cho deck, vẽ ĐÚNG kích thước px trên slide 1280x720 (dpi 100, chữ >= 14.4 pt = 20 px).

Ra (figures/):
  <slug>_fold.png      gấp pha + mô hình, mỗi hành tinh        (700 x 470)
  m_lc.png m_bls.png m_fold.png m_post.png   hình phương pháp cho benchmark HD 118203 b
  res_radius.png res_period.png              tổng hợp đo vs catalog (570 x 470)
"""
import json
import pathlib
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import batman

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import transit_pipeline as tp

ROOT = tp.ROOT
FIG = ROOT / "figures"
NAVY, RED = "#273896", "#ED1C24"
plt.rcParams.update({"font.size": 15, "axes.labelsize": 15, "axes.titlesize": 15, "xtick.labelsize": 14.5,
                     "ytick.labelsize": 14.5, "legend.fontsize": 14.5, "figure.dpi": 100, "savefig.dpi": 100})
names = [l.strip() for l in open(ROOT / "data" / "selected.txt") if l.strip()]
slug = lambda n: re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_")


def load(name):
    s = slug(name)
    res = json.load(open(ROOT / "results" / s / "result.json"))
    lc = np.load(ROOT / "data" / "lightcurves" / f"{s}.npz")
    ch = np.load(ROOT / "results" / s / "chain.npy")
    return s, res, lc["t"], lc["f"], ch


def model_curve(med, hours):
    t0, per, ror, b, loga, q1, q2 = med
    a = np.exp(loga)
    p = batman.TransitParams()
    p.t0, p.per, p.rp, p.a, p.inc = 0.0, per, ror, a, np.degrees(np.arccos(min(b / a, 1)))
    p.ecc, p.w, p.limb_dark = 0.0, 90.0, "quadratic"
    sq = np.sqrt(q1)
    p.u = [2 * sq * q2, sq * (1 - 2 * q2)]
    return batman.TransitModel(p, hours / 24).light_curve(p)


def fold_plot(name, size=(6.3, 4.7), fname=None, title=None):
    s, res, t, f, ch = load(name)
    med = np.median(ch, axis=0)
    per, t0 = res["fit"]["period"], res["fit"]["t0"]
    ph = ((t - t0 + 0.5 * per) % per - 0.5 * per) * 24
    dur_h = res["bls"]["duration"] * 24
    half = min(max(3.2 * dur_h, 3.0), 0.5 * per * 24)
    m = np.abs(ph) < half
    fig, ax = plt.subplots(figsize=size, constrained_layout=True)
    ax.plot(ph[m], (f[m] - 1) * 1e3, ".", ms=2.5, color="0.72", rasterized=True)
    nb = 30
    ed = np.linspace(-half, half, nb + 1)
    k = np.digitize(ph[m], ed)
    bx = np.array([ph[m][k == i].mean() for i in range(1, nb + 1) if (k == i).sum() > 3])
    by = np.array([f[m][k == i].mean() for i in range(1, nb + 1) if (k == i).sum() > 3])
    ax.plot(bx, (by - 1) * 1e3, "o", ms=5.5, color="k", label="binned data")
    g = np.linspace(-half, half, 600)
    mm = model_curve(med, g)
    ax.plot(g, (mm - 1) * 1e3, color=RED, lw=2.8, label="transit model")
    ax.set(xlabel="Hours from mid-transit", ylabel="Flux (ppt)")
    ax.legend(loc="lower right", frameon=True)
    if title:
        ax.set_title(title)
    fig.savefig(FIG / (fname or f"{s}_fold.png"))
    plt.close(fig)


# ---------------------------------------------------------------- hình mỗi hành tinh
for n in names:
    try:
        fold_plot(n)
    except Exception as e:
        print("lỗi fold", n, e)

# ---------------------------------------------------------------- hình phương pháp (benchmark)
BENCH = "HD 118203 b"
s, res, t, f, ch = load(BENCH)
tic = res["tic"]
lcs, sectors, _ = tp.load_lightcurve(tic, 4)
raw = tp.lk.LightCurveCollection(lcs).stitch()
fig, ax = plt.subplots(figsize=(11.6, 3.5), constrained_layout=True)
ax.plot(raw.time.value, (raw.flux.value - 1) * 1e3, ".", ms=1.5, color="0.6", label="SPOC PDCSAP (normalised)")
ax.plot(t, (f - 1) * 1e3 - 6, ".", ms=1.5, color=NAVY, label="detrended (offset −6 ppt)")
per, t0 = res["fit"]["period"], res["fit"]["t0"]
tr = t0 + per * np.arange(-50, 50)
tr = tr[(tr > t.min()) & (tr < t.max())]
ax.plot(tr, np.full_like(tr, -9.5), "|", color=RED, ms=14, mew=2.5, label="predicted transits")
ax.set(xlabel="BTJD (days)", ylabel="Flux (ppt)", ylim=(-10.5, 3.5))
ax.legend(loc="lower right", ncol=3, frameon=True)
fig.savefig(FIG / "m_lc.png")
plt.close(fig)

lc1 = tp.flatten(lcs, 1.5).remove_nans().remove_outliers(sigma_upper=5, sigma_lower=50)
bls, pg, pw = tp.run_bls(lc1.time.value, lc1.flux.value, lc1.flux_err.value)
fig, ax = plt.subplots(figsize=(5.7, 4.0), constrained_layout=True)
ax.plot(pg, pw, lw=0.9, color=NAVY)
ip = int(np.argmin(np.abs(pg - bls.period)))
ax.plot([bls.period], [pw.max() * 1.07], "v", color=RED, ms=13)
ax.set(xscale="log", xlabel="Trial period (days)", ylabel="BLS power (SNR)", ylim=(0, pw.max() * 1.28))
ax.set_xticks([0.3, 1, 3, 10]); ax.set_xticklabels(["0.3", "1", "3", "10"])
ax.text(0.03, 0.93, f"best P = {bls.period:.4f} d", transform=ax.transAxes, ha="left", va="top", color=RED, fontsize=15, fontweight="bold")
fig.savefig(FIG / "m_bls.png")
plt.close(fig)

fold_plot(BENCH, size=(5.7, 4.0), fname="m_fold.png")

fig, axs = plt.subplots(1, 2, figsize=(11.6, 3.6), constrained_layout=True)
ror, per_s = ch[:, 2], ch[:, 1]
axs[0].hist(ror, bins=40, color=NAVY)
axs[0].axvline(0.05538, color=RED, lw=2.5, label="tutorial 0.0554")
axs[0].set(xlabel="Rp/R★", ylabel="MCMC samples"); axs[0].legend(loc="upper left")
axs[0].ticklabel_format(useOffset=False)
axs[1].hist(per_s, bins=40, color=NAVY)
axs[1].axvline(6.1349779, color=RED, lw=2.5, label="catalog 6.13498")
axs[1].set(xlabel="Period (days)", ylabel="MCMC samples"); axs[1].legend(loc="upper left")
axs[1].ticklabel_format(useOffset=False)
axs[1].xaxis.set_major_locator(plt.MaxNLocator(4)); axs[0].xaxis.set_major_locator(plt.MaxNLocator(5))
fig.savefig(FIG / "m_post.png")
plt.close(fig)

# ---------------------------------------------------------------- tổng hợp đo vs catalog
R = [json.load(open(ROOT / "results" / slug(n) / "result.json")) for n in names]
num = np.arange(1, len(R) + 1)
fig, ax = plt.subplots(figsize=(5.7, 4.7), constrained_layout=True)
cat_r = np.array([r["catalog"]["rade"] for r in R]); me_r = np.array([r["rp_rearth"] for r in R]); er = np.array([r["rp_rearth_err"] for r in R])
dpc = 100 * (me_r - cat_r) / cat_r; epc = 100 * er / cat_r
ax.axhline(0, color="0.4", lw=1.5, ls="--")
ax.errorbar(num, dpc, yerr=epc, fmt="none", ecolor="0.35", lw=2, capsize=4, zorder=2)
ax.scatter(num, dpc, s=300, color=RED, edgecolor="white", zorder=3)
for x, y, n in zip(num, dpc, num):
    ax.text(x, y, str(n), ha="center", va="center", color="white", fontsize=12, fontweight="bold", zorder=4)
ax.set(xlabel="Planet number", ylabel="(Measured − catalog) / catalog (%)", xticks=num, ylim=(-20, 20))
fig.savefig(FIG / "res_radius.png")
plt.close(fig)

fig, ax = plt.subplots(figsize=(5.7, 4.7), constrained_layout=True)
dp = np.array([abs(r["delta_period_pct"]) for r in R])
ax.bar(num, dp, color=[NAVY if d < 0.05 else RED for d in dp])
ax.set(yscale="log", xlabel="Planet number", ylabel="|ΔP| / P (%)", xticks=num)
ax.set_ylim(1e-5, 1e2)
ax.axhline(0.01, color="0.5", ls="--", lw=1.2)
fig.savefig(FIG / "res_period.png")
plt.close(fig)
print("xong hình")
