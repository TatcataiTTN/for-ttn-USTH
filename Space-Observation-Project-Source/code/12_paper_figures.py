"""Bước 12 - Dựng lại các hình của Huang et al. 2018 (arXiv:1809.05967, pi Men c) bằng pipeline của dự án, rồi mở rộng.

Hình (figures/paper/, vẽ đúng px, dpi 100, chữ >= 14.4 pt):
  fig2_<slug>.png      thô PDCSAP + vạch momentum dump | sau làm phẳng | gấp pha (bài báo Fig 2)       (mọi hành tinh)
  fig4_pi_Men_c.png    từng transit riêng + hậu nghiệm (Rp/R*)^2 của từng transit (bài báo Fig 4)
  fig1_pi_Men_c.png    ảnh TESS tổng + khẩu độ SPOC (bài báo Fig 1, nửa TESS)
  fig5a_mag_radius.png độ sáng biểu kiến theo bán kính, mọi hành tinh chuyển tiếp đã biết (Fig 5 trên)
  fig5b_mass_radius.png khối lượng - bán kính hành tinh nhỏ + đường mật độ không đổi (Fig 5 dưới)
  oddeven.png          độ sâu transit lẻ vs chẵn, 10+1 hành tinh (phép thử dương tính giả cổ điển)
  occult.png           độ sâu tại pha 0.5 (nhật thực thứ cấp / phản xạ)
  rednoise.png         rms phần dư theo cỡ bin (Pont 2006) và hệ số beta
  bls_pi_Men_c.png     chu kỳ đồ BLS + các alias P/2, 2P
Số đo dùng để mô tả hình ghi vào figures/paper/figure_stats.json (không gõ tay).
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
from scipy.optimize import minimize_scalar

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import transit_pipeline as tp

ROOT = tp.ROOT
OUT = ROOT / "figures" / "paper"
OUT.mkdir(parents=True, exist_ok=True)
NAVY, RED = "#273896", "#ED1C24"
plt.rcParams.update({"font.size": 15, "axes.labelsize": 15, "axes.titlesize": 15, "xtick.labelsize": 14.5,
                     "ytick.labelsize": 14.5, "legend.fontsize": 14.5, "figure.dpi": 100, "savefig.dpi": 100})
slug = lambda n: re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_")
NAMES = [l.strip() for l in open(ROOT / "data" / "selected.txt") if l.strip()]
STATS = {}
CAT = pd.read_csv(ROOT / "data" / "raw" / "pscomppars_transit_all.csv")


def load(name):
    s = slug(name)
    res = json.load(open(ROOT / "results" / s / "result.json"))
    lc = np.load(ROOT / "data" / "lightcurves" / f"{s}.npz")
    ch = np.load(ROOT / "results" / s / "chain.npy")
    return s, res, lc["t"], lc["f"], lc["fe"], ch


def model(med, t, t0=None, per=None, ror=None):
    _, p0, r0, b, loga, q1, q2 = med
    t0 = med[0] if t0 is None else t0
    per = p0 if per is None else per
    ror = r0 if ror is None else ror
    a = np.exp(loga)
    p = batman.TransitParams()
    p.t0, p.per, p.rp, p.a, p.inc = t0, per, ror, a, np.degrees(np.arccos(min(b / a, 1)))
    p.ecc, p.w, p.limb_dark = 0.0, 90.0, "quadratic"
    sq = np.sqrt(q1)
    p.u = [2 * sq * q2, sq * (1 - 2 * q2)]
    return batman.TransitModel(p, t, supersample_factor=3, exp_time=2 / 1440).light_curve(p)


def local_files(tic, suffix, sectors=None):
    """Tìm file SPOC đã tải về máy (cache lightkurve hoặc kho tĩnh), không gọi mạng."""
    t16 = f"{int(tic):016d}"
    fs = sorted(set(tp.CACHE.rglob(f"*-{t16}-*{suffix}")))
    out = []
    for f in fs:
        sec = int(re.search(r"-s(\d{4})-", f.name).group(1))
        if sectors is None or sec in sectors:
            out.append(f)
    return out


def raw_and_dumps(res):
    """PDCSAP chuẩn hoá + giờ momentum dump (bit 32 của quality flag), đọc từ file cục bộ."""
    lk = tp.lk
    coll = [lk.read(str(f), flux_column="pdcsap_flux", quality_bitmask="none") for f in local_files(res["tic"], "_lc.fits", res["sectors_used"])]
    traw, fraw, dumps = [], [], []
    for lc in coll:
        q = np.asarray(lc.quality)
        t = lc.time.value
        dumps += list(t[(q & 32) > 0])
        good = (q == 0) & np.isfinite(lc.flux.value)
        traw.append(t[good]); fraw.append(lc.flux.value[good] / np.nanmedian(lc.flux.value[good]))
    d = np.array(sorted(dumps))
    if len(d):                                          # gộp các cadence liên tiếp của cùng một lần dump
        d = d[np.insert(np.diff(d) > 0.2, 0, True)]
    return np.concatenate(traw), np.concatenate(fraw), d


def binned(x, y, width):
    k = np.floor((x - x.min()) / width).astype(int)
    u = np.unique(k)
    return np.array([x[k == i].mean() for i in u if (k == i).sum() > 3]), np.array([y[k == i].mean() for i in u if (k == i).sum() > 3])


# ------------------------------------------------------------------ Fig 2: thô | làm phẳng | gấp pha
def fig2(name, size=(7.4, 4.7), tag=""):
    s, res, t, f, fe, ch = load(name)
    med = np.median(ch, axis=0)
    per, t0 = res["fit"]["period"], res["fit"]["t0"]
    traw, fraw, dumps = raw_and_dumps(res)
    dur_h = res["bls"]["duration"] * 24
    fig = plt.figure(figsize=size, constrained_layout=True)
    gs = fig.add_gridspec(3, 1, height_ratios=[1, 1, 1.15])
    a1 = fig.add_subplot(gs[0]); a2 = fig.add_subplot(gs[1], sharex=a1); a3 = fig.add_subplot(gs[2])
    ylo = min(np.percentile((fraw - 1) * 1e6, 0.5), np.percentile((f - 1) * 1e6, 0.5))
    for a, tt, ff, c in ((a1, traw, fraw, "0.55"), (a2, t, f, NAVY)):
        a.plot(tt, (ff - 1) * 1e6, ".", ms=1.6, color=c, alpha=0.5, rasterized=True)
        bx, by = binned(tt, ff, 30 / 1440)
        a.plot(bx, (by - 1) * 1e6, ".", ms=3, color="k", alpha=0.7)
    for d in dumps:
        a1.axvline(d, color="k", ls="--", lw=1.1)
    tr = t0 + per * np.arange(-3000, 3000)
    tr = tr[(tr > t.min()) & (tr < t.max())]
    a2.plot(tr, np.full_like(tr, (np.percentile((f - 1) * 1e6, 0.2)) * 1.05), "|", color=RED, ms=14, mew=2.4)
    a2.set_xlabel("BTJD (days)"); fig.supylabel("Flux deviation (ppm)", fontsize=15)
    plt.setp(a1.get_xticklabels(), visible=False)
    a1.text(0.01, 0.80, f"raw, {len(dumps)} momentum dumps (dashed)", transform=a1.transAxes, fontsize=14.5, bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
    a2.text(0.01, 0.80, "detrended", transform=a2.transAxes, fontsize=14.5, bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
    ph = ((t - t0 + 0.5 * per) % per - 0.5 * per) * 24
    half = min(max(3.2 * dur_h, 3.0), 0.5 * per * 24)
    m = np.abs(ph) < half
    a3.plot(ph[m], (f[m] - 1) * 1e6, ".", ms=2.5, color="0.72", rasterized=True)
    bx, by = binned(ph[m], f[m], 2 * half / 36)
    a3.plot(bx, (by - 1) * 1e6, "o", ms=5.5, color="k", label="binned")
    g = np.linspace(-half, half, 600)
    a3.plot(g, (model(med, g / 24, t0=0.0) - 1) * 1e6, color=RED, lw=2.8, label="model")
    a3.set(xlabel="Hours from mid-transit", ylabel="Flux (ppm)")
    a3.legend(loc="lower right", frameon=True, ncol=2)
    fig.savefig(OUT / f"fig2_{s}{tag}.png")
    plt.close(fig)
    rms_raw = float(np.std((fraw - 1) * 1e6)); rms_flat = float(np.std((f - 1) * 1e6))
    inb = np.abs(ph) < dur_h / 2 * 0.6
    depth_obs = float(-(np.mean(f[inb]) - np.median(f[np.abs(ph) > dur_h])) * 1e6)
    STATS[f"fig2_{s}"] = dict(name=name, n_dumps=int(len(dumps)), rms_raw_ppm=round(rms_raw), rms_flat_ppm=round(rms_flat),
                              depth_obs_ppm=round(depth_obs), depth_model_ppm=round(float(res["fit"]["ror"] ** 2 * 1e6)),
                              n_transits=int(res["fit"]["n_transits"]), duration_h=round(dur_h, 2),
                              scatter_2min_ppm=round(float(np.std(np.diff(f)) / np.sqrt(2) * 1e6)))


# ------------------------------------------------------------------ Fig 4: từng transit + hậu nghiệm (Rp/R*)^2
def fig4(name="pi Men c"):
    s, res, t, f, fe, ch = load(name)
    med = np.median(ch, axis=0)
    per, t0 = res["fit"]["period"], res["fit"]["t0"]
    n = np.round((t - t0) / per)
    ep = [int(e) for e in np.unique(n) if np.sum((n == e) & (np.abs(t - (t0 + e * per)) < res["bls"]["duration"] * 0.6)) > 20]
    ncol = 3; nrow = int(np.ceil((len(ep) + 1) / ncol))
    fig, axs = plt.subplots(nrow, ncol, figsize=(7.6, 2.4 * nrow), constrained_layout=True, sharey=False)
    axs = axs.ravel()
    cols = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
    grid = np.linspace(0.6 * med[2], 1.6 * med[2], 400)
    post = {}
    stats = []
    for k, e in enumerate(ep):
        tc = t0 + e * per
        w = np.abs(t - tc) < 1.0
        tt, ff, ee = t[w], f[w], fe[w]
        ax = axs[k]
        ax.plot(tt - tc, (ff - 1) * 1e6, ".", ms=3, color="0.6", rasterized=True)
        ax.plot(tt - tc, (model(med, tt) - 1) * 1e6, color=cols[k % 6], lw=3)
        ax.set(xlabel="Days from mid-transit" if k >= ncol else "", ylim=(-900, 700))
        if k % ncol == 0: ax.set_ylabel("Δ flux (ppm)")
        ax.text(0.04, 0.05, f"transit {k+1}", transform=ax.transAxes, fontsize=14.5)
        chi = []
        for r in grid:
            mdl = model(med, tt, ror=r)
            off = np.sum((ff - mdl) / ee**2) / np.sum(1 / ee**2)           # hằng số nền biên hoá giải tích
            chi.append(np.sum(((ff - mdl - off) / ee) ** 2))
        chi = np.array(chi); pr = np.exp(-0.5 * (chi - chi.min())); pr /= np.trapezoid(pr, grid ** 2 * 1e6)
        post[k] = pr
        d = grid ** 2 * 1e6
        mean = float(np.trapezoid(d * pr, d)); sd = float(np.sqrt(np.trapezoid((d - mean) ** 2 * pr, d)))
        stats.append(dict(transit=k + 1, epoch=int(e), depth_ppm=round(mean), sd_ppm=round(sd)))
    ax = axs[len(ep)]
    for k in post:
        ax.plot(grid ** 2 * 1e6, post[k], color=cols[k % 6], lw=2)
    glob = ch[:, 2] ** 2 * 1e6
    h, ed = np.histogram(glob, bins=40, density=True)
    ax.step(0.5 * (ed[1:] + ed[:-1]), h, color="k", lw=2.4, where="mid")
    ax.set(xlabel="(Rp/R★)² (ppm)", ylabel="PDF", xlim=(150, 400))
    for j in range(len(ep) + 1, len(axs)):
        axs[j].axis("off")
    fig.savefig(OUT / "fig4_pi_Men_c.png")
    plt.close(fig)
    ds = np.array([x["depth_ppm"] for x in stats]); es = np.array([x["sd_ppm"] for x in stats])
    wmean = float(np.sum(ds / es**2) / np.sum(1 / es**2))
    chi2 = float(np.sum(((ds - wmean) / es) ** 2))
    STATS["fig4_pi_Men_c"] = dict(per_transit=stats, global_depth_ppm=round(float(np.median(glob))), global_sd_ppm=round(float(np.std(glob))),
                                  chi2_consistency=round(chi2, 2), dof=len(ds) - 1, depth_scatter_ppm=round(float(np.std(ds, ddof=1))), depth_mean_ppm=round(float(np.mean(ds))))


# ------------------------------------------------------------------ Fig 1: ảnh TESS tổng + khẩu độ
def fig1(name="pi Men c"):
    s, res, *_ = load(name)
    lk = tp.lk
    tpf = lk.read(str(local_files(res["tic"], "_tp.fits", res["sectors_used"][:1])[0]))
    img = np.nansum(tpf.flux.value, axis=0)
    mask = tpf.pipeline_mask
    fig, ax = plt.subplots(figsize=(5.7, 4.3), constrained_layout=True)
    ax.imshow(np.log10(np.clip(img, 1, None)), origin="lower", cmap="gray_r")
    ys, xs = np.where(mask)
    for y, x in zip(ys, xs):
        ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, fill=False, ec=RED, lw=2.2))
    ax.set(xlabel="Pixel column", ylabel="Pixel row", xticks=range(0, img.shape[1], 2), yticks=range(0, img.shape[0], 4))
    fig.savefig(OUT / "fig1_pi_Men_c.png")
    plt.close(fig)
    STATS["fig1_pi_Men_c"] = dict(stamp=list(img.shape), n_aperture_pix=int(mask.sum()), sector=int(tpf.sector),
                                  camera=int(tpf.camera), ccd=int(tpf.ccd),
                                  frac_flux_in_aperture=round(float(img[mask].sum() / img.sum()), 3))


# ------------------------------------------------------------------ Fig 5 trên/dưới
MR = pd.read_csv(ROOT / "data" / "raw" / "pscomppars_mass_radius.csv").drop_duplicates("pl_name")


def fig5(mine):
    """mine: [(tên, bán kính đo R⊕, độ sáng)]; 5a độ sáng-bán kính, 5b khối lượng-bán kính (chỉ khối lượng ĐO, có sai số)."""
    c = MR[np.isfinite(MR.pl_rade) & (MR.pl_rade < 6.2)]
    v = c.sy_vmag.fillna(c.sy_tmag)
    ang = 2 * c.st_rad * 6.957e8 / (c.sy_dist * 3.0857e16) * 206265e3   # đường kính góc của sao (mas)
    fig, ax = plt.subplots(figsize=(5.7, 3.7), constrained_layout=True)
    ax.scatter(c.pl_rade, v, s=np.clip(ang * 4, 3, 220), facecolors="none", edgecolors=NAVY, linewidths=0.7, alpha=0.6)
    off = []
    for i, (n, r, vm) in enumerate(mine, 1):
        if r > 6.2:
            off.append(n); continue
        ax.scatter([r], [vm], s=190, color=RED, edgecolor="white", zorder=5)
        ax.text(r, vm, "π" if n == "pi Men c" else str(i), ha="center", va="center", color="white", fontsize=11, fontweight="bold", zorder=6)
    ax.set(xlabel="Planet radius (R⊕)", ylabel="Apparent magnitude", xlim=(0, 6.2), ylim=(17, 4))
    fig.savefig(OUT / "fig5a_mag_radius.png")
    plt.close(fig)
    STATS["fig5a"] = dict(n_planets=int(len(c)), n_brighter_than_8=int((v < 8).sum()),
                          n_brighter_than_8_and_smaller_than_3=int(((v < 8) & (c.pl_rade < 3)).sum()),
                          n_brighter_than_6_5=int((v < 6.5).sum()), off_chart=off)

    m = MR[(MR.pl_bmassprov == "Mass") & np.isfinite(MR.pl_bmasse) & np.isfinite(MR.pl_rade) & (MR.pl_rade < 4) & (MR.pl_bmasse < 20)].copy()
    m["fm"] = (m.pl_bmasseerr1.abs() + m.pl_bmasseerr2.abs()) / 2 / m.pl_bmasse
    m["fr"] = (m.pl_radeerr1.abs() + m.pl_radeerr2.abs()) / 2 / m.pl_rade
    m = m[np.isfinite(m.fm) & np.isfinite(m.fr)]
    good = (m.fm < 0.25) & (m.fr < 0.1)
    fig, ax = plt.subplots(figsize=(5.7, 3.7), constrained_layout=True)
    for sel, col, al in ((~good, "0.8", 0.5), (good, "0.25", 0.9)):
        x = m[sel]
        ax.errorbar(x.pl_bmasse, x.pl_rade, xerr=x.pl_bmasse * x.fm, yerr=x.pl_rade * x.fr, fmt=".", ms=4, color=col, ecolor=col, elinewidth=0.8, alpha=al, zorder=1 if col == "0.8" else 2)
    Z = ROOT / "data" / "raw" / "zeng"
    for f, lab, col in (("massradiusFe", "100% Fe", "#e8742c"), ("massradiusEarthlikeRocky", "Earth-like", "#6b8e23"), ("massradiusmgsio3", "100% MgSiO₃", "#1f8a8a"),
                        ("massradius_50percentH2O_300K_1mbar", "50% H₂O", "#4169e1"), ("massradius_100percentH2O_300K_1mbar", "100% H₂O", "#273896")):
        t = np.loadtxt(Z / f"{f}.txt")
        ax.plot(t[:, 0], t[:, 1], color=col, lw=2.3, label=lab)
    for i, (n, r, vm) in enumerate(mine, 1):
        pass
    ax.set(xscale="log", xlabel="Mass (M⊕)", ylabel="Radius (R⊕)", xlim=(0.5, 20), ylim=(0.6, 4))
    ax.set_xticks([1, 2, 5, 10, 20]); ax.set_xticklabels(["1", "2", "5", "10", "20"])
    ax.legend(loc="upper left", fontsize=11.5, ncol=2, frameon=True)
    return fig, ax, m, good


# ------------------------------------------------------------------ lẻ/chẵn, pha 0.5, nhiễu đỏ
def per_planet_tests(names):
    odd, occ, beta = {}, {}, {}
    for n in names:
        s, res, t, f, fe, ch = load(n)
        med = np.median(ch, axis=0)
        per, t0 = res["fit"]["period"], res["fit"]["t0"]
        ep = np.round((t - t0) / per).astype(int)
        out = []
        for par in (1, 0):
            sel = (ep % 2 == par) & (np.abs(t - (t0 + ep * per)) < 2.5 * res["bls"]["duration"] + 0.1)
            if sel.sum() < 30:
                out.append((np.nan, np.nan)); continue
            tt, ff, ee = t[sel], f[sel], fe[sel]
            chi = lambda r: np.sum(((ff - model(med, tt, ror=r)) / ee) ** 2)
            o = minimize_scalar(chi, bounds=(0.3 * med[2], 2.0 * med[2]), method="bounded", options=dict(xatol=1e-7))
            h = 0.02 * o.x
            c2 = (chi(o.x + h) - 2 * o.fun + chi(o.x - h)) / h**2        # đạo hàm bậc hai của chi^2 theo ror
            sr = np.sqrt(2.0 / c2)                                       # Δchi^2 = 1
            out.append((float(o.x**2 * 1e6), float(2 * o.x * sr * 1e6)))
        odd[n] = out
        # pha 0.5
        ph = ((t - t0) / per) % 1.0
        dur = res["bls"]["duration"] / per
        inocc = np.abs(ph - 0.5) < dur / 2
        oot = (np.abs(ph - 0.5) > dur) & (np.abs(ph) > dur) & (np.abs(ph - 1) > dur)
        if inocc.sum() > 20:
            dep = float((np.mean(f[oot]) - np.mean(f[inocc])) * 1e6)
            err = float(np.std(f[oot]) / np.sqrt(inocc.sum()) * 1e6)
        else:
            dep, err = np.nan, np.nan
        occ[n] = (dep, err)
        # nhiễu đỏ: phần dư theo cỡ bin
        mdl = model(med, t)
        r = f - mdl
        oot_r = r[np.abs(((t - t0 + 0.5 * per) % per) - 0.5 * per) > 1.5 * res["bls"]["duration"]]
        sig1 = np.std(oot_r)
        Ns = np.unique(np.round(np.logspace(0, np.log10(min(len(oot_r) // 8, 400)), 14)).astype(int))
        rms = []
        for N in Ns:
            k = len(oot_r) // N
            rms.append(np.std(oot_r[:k * N].reshape(k, N).mean(axis=1)))
        rms = np.array(rms)
        exp = sig1 / np.sqrt(Ns)                                   # nhiễu trắng
        sel = (Ns >= max(2, int(0.5 * res["bls"]["duration"] / (2 / 1440)))) & (Ns <= int(2 * res["bls"]["duration"] / (2 / 1440)) + 1)
        sel = sel if sel.sum() else (Ns > 1)
        b = float(np.median(rms[sel] / exp[sel]))
        beta[n] = dict(N=Ns, rms=rms, white=exp, beta=b, sig1=float(sig1))
    return odd, occ, beta


def main():
    names = NAMES + ["pi Men c"]
    for n in names:
        try:
            fig2(n)
            print("fig2", n, flush=True)
        except Exception as e:
            print("lỗi fig2", n, e)
    try:
        fig4(); print("fig4")
    except Exception as e:
        print("lỗi fig4", e)
    try:
        fig1(); print("fig1")
    except Exception as e:
        print("lỗi fig1", e)

    # Fig 5
    mine_mag = []
    for n in names:
        row = CAT[CAT.pl_name == n].iloc[0]
        r = json.load(open(ROOT / "results" / slug(n) / "result.json"))["rp_rearth"]
        mine_mag.append((n, r, row.sy_vmag if np.isfinite(row.sy_vmag) else row.sy_tmag))
    fig, ax, m, good = fig5(mine_mag)
    inmass = []
    for i, n in enumerate(names, 1):
        row = MR[MR.pl_name == n]
        if len(row) and np.isfinite(row.iloc[0].pl_bmasse) and row.iloc[0].pl_bmasse < 20 and row.iloc[0].pl_bmassprov == "Mass":
            row = row.iloc[0]
            r = json.load(open(ROOT / "results" / slug(n) / "result.json"))
            ax.errorbar([row.pl_bmasse], [r["rp_rearth"]], yerr=[r["rp_rearth_err"]], fmt="o", color=RED, ms=14, mec="white", capsize=4, zorder=5)
            ax.text(row.pl_bmasse, r["rp_rearth"], "π" if n == "pi Men c" else str(i), ha="center", va="center", color="white", fontsize=11, fontweight="bold", zorder=6)
            inmass.append(dict(planet=n, mass=float(row.pl_bmasse), radius_measured=round(r["rp_rearth"], 2)))
    fig.savefig(OUT / "fig5b_mass_radius.png")
    plt.close(fig)
    STATS["fig5b"] = dict(n_planets=int(len(m)), n_precise=int(good.sum()), mine=inmass)

    odd, occ, beta = per_planet_tests(names)
    # lẻ/chẵn
    fig, ax = plt.subplots(figsize=(11.6, 3.9), constrained_layout=True)
    sig_w = [(odd[n][0][0] - odd[n][1][0]) / np.hypot(odd[n][0][1], odd[n][1][1]) for n in names]
    sig = [x / max(beta[n]["beta"], 1.0) for x, n in zip(sig_w, names)]      # sai số nhân β (nhiễu đỏ, Pont 2006)
    ax.axhspan(-3, 3, color="0.9")
    ax.axhline(0, color="0.4", lw=1.5, ls="--")
    ax.scatter(range(1, len(names) + 1), sig, s=170, color=[RED if abs(x) > 3 else NAVY for x in sig], zorder=3)
    ax.set_xticks(range(1, len(names) + 1)); ax.set_xticklabels([("π Men c" if n == "pi Men c" else n.replace(" ", "\n", 1)) for n in names], fontsize=11)
    ax.set(ylabel="(odd − even depth) / (β·σ)", ylim=(-6, 6))
    fig.savefig(OUT / "oddeven.png"); plt.close(fig)
    STATS["oddeven"] = {n: dict(odd_ppm=round(odd[n][0][0]), even_ppm=round(odd[n][1][0]), odd_err=round(odd[n][0][1], 1), even_err=round(odd[n][1][1], 1), sigma_white=round(float(w), 2), sigma_beta=round(float(s_), 2), beta=round(beta[n]["beta"], 2)) for n, s_, w in zip(names, sig, sig_w)}

    fig, ax = plt.subplots(figsize=(11.6, 3.9), constrained_layout=True)
    x = np.arange(1, len(names) + 1)
    dd = np.array([occ[n][0] for n in names]); ee = np.array([occ[n][1] for n in names])
    ax.errorbar(x, dd, yerr=ee, fmt="o", color=NAVY, ms=10, capsize=5, lw=2)
    ax.axhline(0, color="0.4", ls="--")
    ax.set_xticks(x); ax.set_xticklabels([("π Men c" if n == "pi Men c" else n.replace(" ", "\n", 1)) for n in names], fontsize=11)
    ax.set(ylabel="Flux deficit at phase 0.5 (ppm)")
    fig.savefig(OUT / "occult.png"); plt.close(fig)
    STATS["occult"] = {n: dict(depth_ppm=round(float(a), 1), err_ppm=round(float(b), 1)) for n, (a, b) in zip(names, zip(dd, ee))}

    fig, axs = plt.subplots(1, 2, figsize=(11.6, 4.0), constrained_layout=True, gridspec_kw=dict(width_ratios=[1.35, 1]))
    cmap = plt.get_cmap("tab20")
    for i, n in enumerate(names):
        b = beta[n]
        axs[0].loglog(b["N"], b["rms"] / b["sig1"], "-", color=cmap(i), lw=1.8)
    Nn = np.logspace(0, 2.6, 20)
    axs[0].loglog(Nn, 1 / np.sqrt(Nn), "k--", lw=2.4, label="white noise 1/√N")
    axs[0].set(xlabel="Points per bin (2 min each)", ylabel="rms / rms(1)"); axs[0].legend(loc="lower left")
    bt = [beta[n]["beta"] for n in names]
    axs[1].barh(range(len(names)), bt, color=[RED if b_ > 1.5 else NAVY for b_ in bt])
    axs[1].axvline(1, color="k", ls="--", lw=1.5)
    axs[1].set_yticks(range(len(names))); axs[1].set_yticklabels([("π Men c" if n == "pi Men c" else n) for n in names], fontsize=11)
    axs[1].set(xlabel="β (red-noise factor)")
    fig.savefig(OUT / "rednoise.png"); plt.close(fig)
    STATS["rednoise"] = {n: dict(beta=round(beta[n]["beta"], 2), rms1_ppm=round(beta[n]["sig1"] * 1e6)) for n in names}

    # BLS pi Men c
    s, res, t, f, fe, ch = load("pi Men c")
    bls, pg, pw = tp.run_bls(t, f, fe)
    fig, ax = plt.subplots(figsize=(11.6, 3.4), constrained_layout=True)
    ax.plot(pg, pw, lw=1.1, color=NAVY)
    P = res["fit"]["period"]
    for mult, lab in ((0.5, "P/2"), (1, "P"), (2, "2P")):
        ax.axvline(P * mult, color=RED if mult == 1 else "0.5", ls="--", lw=1.6)
        ax.text(P * mult, pw.max() * 1.02, lab, ha="center", color=RED if mult == 1 else "0.35", fontsize=14.5)
    ax.set(xscale="log", xlabel="Trial period (days)", ylabel="BLS power (SNR)", ylim=(0, pw.max() * 1.15))
    ax.set_xticks([0.5, 1, 2, 5, 10]); ax.set_xticklabels(["0.5", "1", "2", "5", "10"])
    fig.savefig(OUT / "bls_pi_Men_c.png"); plt.close(fig)
    ip = np.argmax(pw)
    STATS["bls_pi_Men_c"] = dict(best_period=round(float(pg[ip]), 4), snr=round(float(pw[ip]), 1),
                                 median_power=round(float(np.median(pw)), 2), p95_power=round(float(np.percentile(pw, 95)), 2))
    json.dump(STATS, open(OUT / "figure_stats.json", "w"), indent=1, default=float)
    print("xong", len(STATS), "mục thống kê")


if __name__ == "__main__":
    main()
