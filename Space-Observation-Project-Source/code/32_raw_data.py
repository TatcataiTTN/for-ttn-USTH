# -*- coding: utf-8 -*-
"""Bước 32 - Dữ liệu GỐC của TESS: cấu trúc file SPOC (light curve _lc.fits và target pixel _tp.fits), vẽ các cột thô, kiểm tra SAP_FLUX = tổng pixel trong khẩu độ.
Vẽ: figures/paper/raw_lc_columns.png (HD 189733 b, sector 41: 19 149 hàng), raw_tpf_pixels.png (pi Men c, sector 1: ảnh pixel, tổng khẩu độ = SAP_FLUX).
Ra thêm: results/raw_data_facts.json (mọi con số dùng trên slide). Định nghĩa cờ chất lượng lấy từ lightkurve.utils.TessQualityFlags (mô tả trong sổ tay archive của STScI)."""
import glob
import json
import pathlib
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
from matplotlib.patches import Rectangle

warnings.filterwarnings("ignore")
import lightkurve as lk

ROOT = pathlib.Path(__file__).resolve().parents[1]
NAVY, RED, GREY = "#273896", "#ED1C24", "#9aa3b5"
plt.rcParams.update({"font.size": 15, "axes.labelsize": 15, "xtick.labelsize": 14.5, "ytick.labelsize": 14.5, "legend.fontsize": 14.5, "figure.dpi": 100, "savefig.dpi": 100})
LC = glob.glob(str(ROOT / "data" / "mast_cache" / "**" / "*s0041*256364928*_lc.fits"), recursive=True)[0]
TPL = ROOT / "data" / "mast_cache" / "static" / "261136679" / "tess2018206045859-s0001-0000000261136679-0120-s_lc.fits"
TPT = ROOT / "data" / "mast_cache" / "static" / "261136679" / "tess2018206045859-s0001-0000000261136679-0120-s_tp.fits"
FL = {int(k): v for k, v in lk.utils.TessQualityFlags.STRINGS.items()}

# ------------------------------------------------------------------ file 1: light curve of HD 189733 b
h = fits.open(LC); H0, H1, H2 = h[0].header, h[1].header, h[2].header; d = h[1].data
t = np.asarray(d["TIME"], float); q = np.asarray(d["QUALITY"]); sap = np.asarray(d["SAP_FLUX"], float); pdc = np.asarray(d["PDCSAP_FLUX"], float)
bkg = np.asarray(d["SAP_BKG"], float); c1 = np.asarray(d["MOM_CENTR1"], float); c2 = np.asarray(d["MOM_CENTR2"], float)
cols = [dict(name=H1[f"TTYPE{i}"], fmt=H1[f"TFORM{i}"], unit=H1.get(f"TUNIT{i}", "")) for i in range(1, H1["TFIELDS"] + 1)]
qv = {int(v): int((q == v).sum()) for v in np.unique(q)}
facts = dict(file=pathlib.Path(LC).name, size_mb=round(pathlib.Path(LC).stat().st_size / 1e6, 2), hdus=[dict(name=x.name, kind=type(x).__name__) for x in h], rows=int(len(d)), n_cols=len(cols), cols=cols,
             aperture_shape=list(h[2].data.shape), aperture_bits={"collected(1)": int(((h[2].data & 1) > 0).sum()), "optimal(2)": int(((h[2].data & 2) > 0).sum()), "background(4)": int(((h[2].data & 4) > 0).sum())},
             header={k: H0.get(k) for k in ("OBJECT", "TICID", "SECTOR", "CAMERA", "CCD", "ORIGIN", "PROCVER", "DATA_REL", "DATE")} | {k: H1.get(k) for k in ("TSTART", "TSTOP", "TIMEDEL", "EXPOSURE", "CROWDSAP", "FLFRCSAP", "PDCVAR", "CDPP1_0", "BJDREFI", "TIMESYS")},
             n_finite_time=int(np.isfinite(t).sum()), n_finite_sap=int(np.isfinite(sap).sum()), n_finite_pdc=int(np.isfinite(pdc).sum()), n_flagged=int((q != 0).sum()),
             quality={str(k): dict(n=v, name=FL.get(k, "combination: " + " + ".join(FL[b] for b in FL if k & b))) for k, v in qv.items()},
             dtypes=dict(TIME=str(d["TIME"].dtype), PDCSAP_FLUX=str(d["PDCSAP_FLUX"].dtype), QUALITY=str(d["QUALITY"].dtype)),
             med_sap=float(np.nanmedian(sap)), med_pdc=float(np.nanmedian(pdc)), pdc_over_sap=float(np.nanmedian(pdc) / np.nanmedian(sap)), med_bkg=float(np.nanmedian(bkg)))
fig, axs = plt.subplots(2, 2, figsize=(10.0, 4.6), constrained_layout=True, gridspec_kw=dict(width_ratios=[1.05, 1]))
a = axs[0, 0]; bad = q != 0
a.plot(t, sap / 1e5, ".", ms=1.2, color=GREY, label="SAP"); a.plot(t, pdc / 1e5, ".", ms=1.2, color=NAVY, label="PDCSAP")
a.plot(t[bad], sap[bad] / 1e5, "x", ms=4, color=RED, label="flagged")
a.set(ylabel="Flux (10$^5$ e$^-$/s)", xticklabels=[], ylim=(2.70, 3.05)); a.legend(loc="upper center", frameon=False, markerscale=4, ncol=3, fontsize=14.5, handletextpad=0.1, columnspacing=0.6, borderpad=0.2)
a = axs[1, 0]; a.plot(t, bkg / 1e3, ".", ms=1.2, color=NAVY); a.set(ylabel="SAP_BKG (10$^3$ e$^-$/s)", xlabel="TIME (BTJD = BJD − 2 457 000)")
a = axs[0, 1]; a.plot(t, c1 - np.nanmedian(c1), ".", ms=1.2, color=NAVY, label="MOM_CENTR1"); a.plot(t, c2 - np.nanmedian(c2), ".", ms=1.2, color=RED, label="MOM_CENTR2")
a.set(ylabel="Centroid (pixel)", xticklabels=[], ylim=(-0.06, 0.2)); a.legend(loc="upper center", frameon=False, markerscale=4, ncol=2, fontsize=14.5, handletextpad=0.1, columnspacing=0.6, borderpad=0.2)
a = axs[1, 1]; keys = sorted(qv, key=lambda k: qv[k])
lab = ["0  good" if k == 0 else f"{k}  {FL[k]}" if k in FL else f"{k} = " + "+".join(str(b) for b in FL if k & b) for k in keys]
a.barh(range(len(keys)), [qv[k] for k in keys], color=[NAVY if k == 0 else RED for k in keys]); a.set_xscale("log"); a.set_yticks(range(len(keys))); a.set_yticklabels(lab, fontsize=14.5)
for i, k in enumerate(keys): a.text(qv[k] * 1.25, i, f"{qv[k]:,}".replace(",", " "), va="center", fontsize=14.5)
a.set(xlabel="Cadences (log scale)", xlim=(0.7, 6e5))
fig.savefig(ROOT / "figures" / "paper" / "raw_lc_columns.png"); plt.close(fig)

# ------------------------------------------------------------------ file 2: target pixels of pi Men c
lc2 = fits.open(TPL)[1].data; tp = fits.open(TPT); dp = tp[1].data; ap = tp[2].data; opt = (ap & 2) > 0
fl = dp["FLUX"]; ssum = np.nansum(np.where(opt[None], fl, 0), axis=(1, 2)); ok = np.isfinite(ssum) & np.isfinite(lc2["SAP_FLUX"]) & (dp["CADENCENO"] == lc2["CADENCENO"]); ratio = ssum[ok] / lc2["SAP_FLUX"][ok]
frame = np.nanmedian(fl, axis=0)
facts["tpf"] = dict(file=TPT.name, size_mb=round(TPT.stat().st_size / 1e6, 1), hdus=[dict(name=x.name, kind=type(x).__name__) for x in tp], flux_shape=list(fl.shape), n_pixels=int(fl.shape[1] * fl.shape[2]), n_optimal=int(opt.sum()), n_bkg=int(((ap & 4) > 0).sum()),
                    cols=[dict(name=tp[1].header[f"TTYPE{i}"], fmt=tp[1].header[f"TFORM{i}"], unit=tp[1].header.get(f"TUNIT{i}", "")) for i in range(1, tp[1].header["TFIELDS"] + 1)],
                    sum_over_sap_median=float(np.median(ratio)), sum_over_sap_maxdev=float(np.max(np.abs(ratio - 1))), n_compared=int(ok.sum()), median_bkg_in_aperture=float(np.nanmedian(dp["FLUX_BKG"][:, opt].sum(axis=1))), sap_bkg_median=float(np.nanmedian(lc2["SAP_BKG"])),
                    peak_pixel=float(np.nanmax(frame)), total_aperture_flux=float(np.nansum(frame[opt])), flux_outside_aperture_pct=float(100 * (np.nansum(frame) - np.nansum(frame[opt])) / np.nansum(frame)))
fig, axs = plt.subplots(1, 3, figsize=(11.6, 4.2), constrained_layout=True, gridspec_kw=dict(width_ratios=[0.8, 1.2, 1.2]))
a = axs[0]; im = a.imshow(np.log10(np.clip(frame, 1, None)), origin="lower", cmap="viridis", aspect="equal")
for (r_, c_) in zip(*np.nonzero(opt)): a.add_patch(Rectangle((c_ - 0.5, r_ - 0.5), 1, 1, fill=False, ec=RED, lw=1.6))
a.set(xlabel="Column (pixel)", ylabel="Row (pixel)", title="median frame"); fig.colorbar(im, ax=a, shrink=0.8, label="log$_{10}$ e$^-$/s")
tt = np.asarray(dp["TIME"], float)
a = axs[1]; a.plot(tt[ok], ssum[ok] / 1e5, ".", ms=1.5, color=NAVY, label="sum of 45 pixels (TPF)"); a.plot(tt[ok], np.asarray(lc2["SAP_FLUX"], float)[ok] / 1e5, ".", ms=0.8, color=RED, label="SAP_FLUX (LC)")
a.set(xlabel="TIME (BTJD)", ylabel="Flux (10$^5$ e$^-$/s)"); a.legend(loc="lower left", frameon=True, markerscale=6, fontsize=14.5)
a = axs[2]; a.plot(tt[ok], (ratio - 1) * 1e7, ".", ms=1.5, color=NAVY); a.axhline(0, color=GREY, lw=1)
a.set(xlabel="TIME (BTJD)", ylabel="sum / SAP_FLUX − 1  (10$^{-7}$)")
fig.savefig(ROOT / "figures" / "paper" / "raw_tpf_pixels.png"); plt.close(fig)
json.dump(facts, open(ROOT / "results" / "raw_data_facts.json", "w"), indent=1, ensure_ascii=False, default=float)
print(json.dumps({k: facts[k] for k in ("rows", "n_cols", "n_finite_pdc", "n_flagged", "quality", "pdc_over_sap", "aperture_bits")}, indent=0)[:900]); print(facts["tpf"]["sum_over_sap_maxdev"], facts["tpf"]["flux_outside_aperture_pct"], facts["tpf"]["n_compared"])
