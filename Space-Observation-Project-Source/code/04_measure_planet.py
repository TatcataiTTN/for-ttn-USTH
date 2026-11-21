"""Bước 4 - Đo bán kính + chu kỳ của MỘT hành tinh từ ánh sáng TESS, rồi so với catalog.

Chạy:  python code/04_measure_planet.py "HD 118203 b" [--sectors 4]
Ra:    results/<slug>/result.json   figures/<slug>_fit.png   data/lightcurves/<slug>.npz
"""
import argparse
import json
import pathlib
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import transit_pipeline as tp

ROOT = tp.ROOT


def slug(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")


def measure(name: str, max_sectors: int = 4, nstep: int = 2500, guided: bool = False):
    cat = pd.read_csv(ROOT / "data" / "raw" / "tess_catalog.csv")
    row = cat[cat.pl_name == name].iloc[0]
    tic = int(row.tic_num)
    s = slug(name)
    (ROOT / "results" / s).mkdir(parents=True, exist_ok=True)

    lcs, sectors, n_all = tp.load_lightcurve(tic, max_sectors)
    # lượt 1: làm phẳng thô -> BLS. Thử 3 cửa sổ (0.4/1.0/1.5 ngày), lấy cửa sổ cho SNR BLS cao nhất:
    # sao hoạt động (AU Mic...) cần cửa sổ ngắn, sao yên tĩnh thì cửa sổ dài giữ nguyên độ sâu transit.
    best = None
    for w1 in (0.4, 1.0, 1.5):
        lc1 = tp.flatten(lcs, w1).remove_nans().remove_outliers(sigma_upper=5, sigma_lower=50)
        if guided:   # tìm quanh chu kỳ đã biết (+-3%), lưới thời lượng mịn hơn: đo lại/hiệu chỉnh, không phải tìm mù
            P0 = float(row.pl_orbper)
            r = tp.run_bls(lc1.time.value, lc1.flux.value, lc1.flux_err.value, pmin=0.97 * P0, pmax=1.03 * P0,
                           durations=float(row.pl_trandur) / 24 * np.array([0.6, 0.8, 1.0, 1.25, 1.5]))
        else:
            r = tp.run_bls(lc1.time.value, lc1.flux.value, lc1.flux_err.value)
        if best is None or r[0].snr > best[0][0].snr:
            best = (r, w1)
    (bls, per_grid, power), w_first = best
    # lượt 2: làm phẳng lại có che transit, chạy 3 biến thể (mask, cửa sổ) để ước lượng sai số hệ thống
    VARIANTS = [(2.0, 4, 0.75), (2.5, 6, 1.0), (3.0, 8, 1.5)]   # (mask x dur, cửa sổ x dur, cửa sổ tối thiểu ngày)
    fits = []
    for k, (mm, wm, wmin) in enumerate(VARIANTS):
        msk = tp.in_transit_mask(bls.period, bls.t0, mm * bls.duration)
        lc2 = tp.flatten(lcs, max(wm * bls.duration, min(wmin, w_first)), mask=msk).remove_nans().remove_outliers(
            sigma_upper=5, sigma_lower=50)
        t, f, fe = lc2.time.value, lc2.flux.value, lc2.flux_err.value
        fits.append(tp.fit_transit(t, f, fe, bls, nstep=nstep))
        if k == len(VARIANTS) - 1:                   # biến thể RỘNG NHẤT làm kết quả chính (ít ăn độ sâu nhất)
            np.savez_compressed(ROOT / "data" / "lightcurves" / f"{s}.npz", t=t, f=f, fe=fe)
    fit, chain, (tt, ff, fee, mdl, med) = fits[-1]
    rors = np.array([x[0].ror for x in fits])
    ror_sys = 0.5 * (rors.max() - rors.min())
    per_sys = 0.5 * (max(x[0].period for x in fits) - min(x[0].period for x in fits))
    ror_tot = float(np.hypot(fit.ror_err, ror_sys))
    fit.ror_err_stat, fit.ror_err = fit.ror_err, ror_tot
    rstar, rstar_e = float(row.st_rad), (None if pd.isna(row.st_raderr1) else float(row.st_raderr1))
    re_, re_err, rj, rj_err = tp.physical_radius(fit, rstar, rstar_e)

    out = dict(
        name=name, tic=tic, sectors_used=sectors, sectors_available=n_all, mode="guided" if guided else "blind",
        bls=tp.asdict(bls), fit=tp.asdict(fit), ror_err_stat=fit.ror_err_stat, ror_err_sys=float(ror_sys),
        ror_variants=[float(x) for x in rors], period_err_sys=float(per_sys),
        rstar_rsun=rstar, rstar_err=rstar_e,
        rp_rearth=re_, rp_rearth_err=re_err, rp_rjup=rj, rp_rjup_err=rj_err,
        catalog=dict(period=float(row.pl_orbper), rade=float(row.pl_rade),
                     ror=float(row.pl_ratror) if pd.notna(row.pl_ratror) else None,
                     trandep_ppm=float(row.pl_trandep) * 1e4, disc_year=int(row.disc_year)),
    )
    out["delta_period_pct"] = 100 * (fit.period - row.pl_orbper) / row.pl_orbper
    out["delta_radius_pct"] = 100 * (re_ - row.pl_rade) / row.pl_rade
    out["delta_ror_pct"] = (100 * (fit.ror - row.pl_ratror) / row.pl_ratror) if pd.notna(row.pl_ratror) else None
    out["rstar_implied_by_catalog"] = float(row.pl_rade / (row.pl_ratror * 109.076)) if pd.notna(row.pl_ratror) else None
    (ROOT / "results" / s / "result.json").write_text(json.dumps(out, indent=2, default=float))

    # ---------------- hình 4 ô
    plt.rcParams.update({"font.size": 11})
    fig, ax = plt.subplots(2, 2, figsize=(14, 8.2), constrained_layout=True)
    a = ax[0, 0]
    a.plot(t, (f - 1) * 1e3, ".", ms=1.2, color="0.35")
    tr = fit.t0 + fit.period * np.arange(-3000, 3000)
    tr = tr[(tr > t.min()) & (tr < t.max())]
    a.plot(tr, np.full_like(tr, a.get_ylim()[0] * 0.9), "|", color="crimson", ms=10)
    a.set(xlabel="BTJD (days)", ylabel="Relative flux (ppt)", title=f"TESS SPOC light curve, sectors {sectors}")
    a = ax[0, 1]
    a.plot(per_grid, power, lw=0.7, color="navy")
    a.axvline(bls.period, color="crimson", ls="--", lw=1)
    a.set(xlabel="Trial period (days)", ylabel="BLS power (SNR)", xscale="log",
          title=f"BLS: P = {bls.period:.4f} d, SNR = {bls.snr:.0f}")
    a = ax[1, 0]
    ph = (tt - fit.t0 + 0.5 * fit.period) % fit.period - 0.5 * fit.period
    o = np.argsort(ph)
    a.plot(ph * 24, (ff - 1) * 1e3, ".", ms=2, color="0.7")
    nb = 40
    edges = np.linspace(ph.min(), ph.max(), nb + 1)
    idx = np.digitize(ph, edges)
    bx = [ph[idx == k].mean() for k in range(1, nb + 1) if (idx == k).sum() > 3]
    by = [ff[idx == k].mean() for k in range(1, nb + 1) if (idx == k).sum() > 3]
    a.plot(np.array(bx) * 24, (np.array(by) - 1) * 1e3, "o", ms=4, color="k", label="binned mean")
    a.plot(ph[o] * 24, (mdl[o] - 1) * 1e3, color="crimson", lw=2, label="batman model")
    a.set(xlabel="Hours from mid-transit", ylabel="Flux (ppt)",
          title=f"Phase-folded: Rp/R* = {fit.ror:.4f} ± {fit.ror_err:.4f} (incl. systematics)")
    a.legend(loc="lower right")
    a = ax[1, 1]
    a.axis("off")
    txt = (f"{name}  (TIC {tic})\n\n"
           f"Period (measured) {fit.period:.5f} ± {fit.period_err:.5f} d\n"
           f"Period (catalog)  {row.pl_orbper:.5f} d   (Δ = {out['delta_period_pct']:+.3f} %)\n\n"
           f"Rp/R*           {fit.ror:.4f} ± {fit.ror_err:.4f}\n"
           f"R* (TIC/NASA)   {rstar:.3f} R☉\n"
           f"Rp (measured)   {re_:.2f} ± {re_err:.2f} R⊕  ({rj:.2f} R_J)\n"
           f"Rp (catalog)    {row.pl_rade:.2f} R⊕   (Δ = {out['delta_radius_pct']:+.1f} %)\n\n"
           f"b = {fit.b:.2f} ± {fit.b_err:.2f},  a/R* = {fit.a_rs:.1f} ± {fit.a_rs_err:.1f}\n"
           f"{fit.n_transits} transits, {fit.n_points} points, χ²_red = {fit.chi2_red:.2f}")
    a.text(0.0, 1.0, txt, va="top", family="monospace", fontsize=12)
    fig.savefig(ROOT / "figures" / f"{s}_fit.png", dpi=130)
    plt.close(fig)
    np.save(ROOT / "results" / s / "chain.npy", chain[::10].astype("float32"))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--sectors", type=int, default=4)
    ap.add_argument("--nstep", type=int, default=2500)
    ap.add_argument("--guided", action="store_true")
    a = ap.parse_args()
    o = measure(a.name, a.sectors, a.nstep, a.guided)
    print(json.dumps({k: o[k] for k in ["name", "rp_rearth", "rp_rearth_err", "delta_period_pct", "delta_radius_pct"]}, indent=1))
    print("P  đo:", round(o["fit"]["period"], 5), " catalog:", o["catalog"]["period"])
    print("Rp đo:", round(o["rp_rearth"], 2), "±", round(o["rp_rearth_err"], 2), " catalog:", o["catalog"]["rade"])
