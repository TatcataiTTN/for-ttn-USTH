# -*- coding: utf-8 -*-
"""Bước 33 - Số liệu cho các slide trả lời 'Check point tự định hướng 9h 22-11' (câu hỏi về Star in frames, chụp ảnh trực tiếp,
độ phân giải, bốn yếu tố FOV/pixel/cadence/revisit, công thức từng phương pháp). Mọi con số tính từ results/*.csv|json, data/ và các tệp FITS
đã tải; hằng số vật lý ghi rõ. Ra: results/checkpoint_facts.json, results/checkpoint_vetting.csv, figures/paper/ck_*.png.
Chạy: .venv/bin/python code/33_checkpoint_facts.py"""
import glob
import json
import pathlib
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.io import fits
from scipy.optimize import brentq

ROOT = pathlib.Path(__file__).resolve().parents[1]
slug = lambda n: re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_")
names = [l.strip() for l in open(ROOT / "data" / "selected.txt") if l.strip()]
G = pd.read_csv(ROOT / "data" / "candidates_grouped.csv").set_index("pl_name").loc[names]
R = {n: json.load(open(ROOT / "results" / slug(n) / "result.json")) for n in names}
RT = pd.read_csv(ROOT / "results" / "results_table.csv").set_index("planet")
TP = pd.read_csv(ROOT / "results" / "tess_planets.csv").set_index("planet")
TF = pd.read_csv(ROOT / "results" / "tess_files.csv")
TD = json.load(open(ROOT / "results" / "tess_design_values.json"))
PIX = 21.0                       # arcsec, Ricker 2015 Table 1 (0.35 arcmin)
AU_PER_PC = 206264.806           # 1 pc = 206265 AU (definition of the parsec)
AU_PER_REARTH, AU_PER_RSUN = 4.2635e-5, 0.0046547
G_SI, RHO_SUN = 6.674e-11, 1.41  # SI; mean solar density g/cm3
F = {}

# ------------------------------------------------------------------ 1. geometry, probability, timing, direct-imaging numbers
rows = []
for n in names:
    r, g = R[n], G.loc[n]
    P, k, b, aRs = r["fit"]["period"], r["fit"]["ror"], r["fit"]["b"], r["fit"]["a_rs"]
    cosi = b / aRs; sini = np.sqrt(1 - cosi ** 2)
    x14 = np.sqrt((1 + k) ** 2 - b ** 2) / (aRs * sini)
    T14 = P / np.pi * np.arcsin(x14)
    x23 = (1 - k) ** 2 - b ** 2
    T23 = P / np.pi * np.arcsin(np.sqrt(x23) / (aRs * sini)) if x23 > 0 else np.nan
    # round trip with the formulas of the notes (Winn 2010): b and a/R* from T14, T23
    if np.isfinite(T23):
        s = np.sin(np.pi * T23 / P) ** 2 / np.sin(np.pi * T14 / P) ** 2
        b_back = np.sqrt(((1 - k) ** 2 - s * (1 + k) ** 2) / (1 - s))
        a_exact = np.sqrt((1 + k) ** 2 - b_back ** 2 * np.cos(np.pi * T14 / P) ** 2) / np.sin(np.pi * T14 / P)
        a_approx = np.sqrt((1 + k) ** 2 - b_back ** 2) / np.sin(np.pi * T14 / P)
    else:
        b_back = a_exact = a_approx = np.nan
    a_au = g.pl_orbsmax if np.isfinite(g.pl_orbsmax) else (g.st_mass * (P / 365.25) ** 2) ** (1 / 3)
    d_pc = g.sy_dist
    rp_au = r["rp_rearth"] * AU_PER_REARTH
    theta = a_au / d_pc                                      # arcsec
    rho_fit = 3 * np.pi * aRs ** 3 / (G_SI * (P * 86400) ** 2) / 1000      # g/cm3
    rho_cat = g.st_mass / g.st_rad ** 3 * RHO_SUN
    rows.append(dict(planet=n, P_d=P, a_au=a_au, d_pc=d_pc, theta_arcsec=theta, theta_mas=theta * 1000, theta_over_pixel=theta / PIX,
                     pixel_au=PIX * d_pc, contrast_Ag03=0.3 * (rp_au / a_au) ** 2, transit_prob_pct=100 / aRs, k=k, b=b, a_rs=aRs,
                     T14_h=T14 * 24, T14_spoc_h=TP.loc[n, "trandur_h"], T23_h=T23 * 24 if np.isfinite(T23) else np.nan,
                     b_back=b_back, a_rs_back_exact=a_exact, a_rs_back_approx=a_approx,
                     pts_per_transit=T14 * 86400 / 120, transits_per_sector=27.4 / P, rho_fit=rho_fit, rho_cat=rho_cat,
                     crowdsap=TP.loc[n, "crowdsap_min"], flfrcsap=TP.loc[n, "flfrcsap"], cdpp1=TP.loc[n, "cdpp1_ppm"],
                     facility=g.disc_facility, method=g.discoverymethod, disc_year=int(g.disc_year)))
GEO = pd.DataFrame(rows).set_index("planet")
GEO.to_csv(ROOT / "results" / "checkpoint_geometry.csv")
F["geometry_summary"] = dict(theta_mas_min=GEO.theta_mas.min(), theta_mas_max=GEO.theta_mas.max(), theta_over_pixel_max=GEO.theta_over_pixel.max(),
                             contrast_min=GEO.contrast_Ag03.min(), contrast_max=GEO.contrast_Ag03.max(),
                             pts_min=GEO.pts_per_transit.min(), pts_max=GEO.pts_per_transit.max(),
                             prob_min=GEO.transit_prob_pct.min(), prob_max=GEO.transit_prob_pct.max(),
                             T14_rel_diff_max_pct=float((100 * (GEO.T14_h / GEO.T14_spoc_h - 1)).abs().max()))
ok = GEO.dropna(subset=["a_rs_back_exact"])
F["roundtrip"] = dict(n=len(ok), b_max_abs=float((ok.b_back - ok.b).abs().max()), a_exact_max_rel_pct=float((100 * (ok.a_rs_back_exact / ok.a_rs - 1)).abs().max()),
                      a_approx_max_rel_pct=float((100 * (ok.a_rs_back_approx / ok.a_rs - 1)).abs().max()), a_approx_planet=str((100 * (ok.a_rs_back_approx / ok.a_rs - 1)).abs().idxmax()))

# analogues, parsec arithmetic (our computation, A_g = 0.3 assumed)
rj_au, re_au = 7.1492e7 / 1.495978707e11, AU_PER_REARTH
F["analogues"] = dict(jupiter_5au_10pc_arcsec=5.2 / 10, jupiter_contrast=0.3 * (rj_au / 5.2) ** 2, earth_1au_10pc_arcsec=1.0 / 10, earth_contrast=0.3 * (re_au / 1.0) ** 2,
                      hr8799_b_arcsec=68 / 39.4, hr8799_d_arcsec=24 / 39.4)
grid = {}
for a in (1, 5, 10, 30, 70):
    for d in (10, 20, 50, 100):
        th = a / d
        grid[f"{a}AU_{d}pc"] = dict(theta=th, px_needed=th / 2, times_finer_than_tess=PIX / (th / 2))
F["needed_grid"] = grid

# diffraction limits, 1.22 lambda / D
dif = lambda lam_m, D: 1.22 * lam_m / D * 206264.806
F["diffraction_arcsec"] = dict(tess_600nm=dif(600e-9, 0.105), tess_800nm=dif(800e-9, 0.105), tess_1000nm=dif(1000e-9, 0.105),
                               jwst_4p44um=dif(4.44e-6, 6.5), jwst_2p7um=dif(2.7e-6, 6.5), tess_pixel=PIX)
F["jwst_pixel_ratio"] = dict(sw=PIX / 0.031, lw=PIX / 0.063)

# thermal contrast by wavelength (Planck), our own assumption: planet 1000 K, Rp = 1 R_J, star 5772 K, R = 1 R_sun
h, c, kB = 6.62607e-34, 2.99792458e8, 1.380649e-23
B = lambda lam, T: 2 * h * c ** 2 / lam ** 5 / np.expm1(h * c / (lam * kB * T))
k_jup_sun = (7.1492e7 / 6.957e8) ** 2
F["thermal_contrast_1000K"] = {f"{l}um": float(k_jup_sun * B(l * 1e-6, 1000) / B(l * 1e-6, 5772)) for l in (0.8, 2.0, 4.4, 10.0)}

# ------------------------------------------------------------------ 2. WASP-18 b worked example for the phase curve
w = GEO.loc["WASP-18 b"]; gw = G.loc["WASP-18 b"]
lam = np.linspace(600e-9, 1000e-9, 401)
band = lambda T: np.trapezoid(B(lam, T), lam)
def tday(depth_ppm, Ag=0.0):
    rp_over_a = w.k / w.a_rs
    refl = Ag * rp_over_a ** 2
    target = (depth_ppm * 1e-6 - refl) / w.k ** 2 * band(gw.st_teff)
    return brentq(lambda T: band(T) - target, 500, 6000)
F["phase_wasp18"] = dict(k=w.k, a_rs=w.a_rs, teff=float(gw.st_teff), rp_over_a=w.k / w.a_rs,
                         Ag_if_all_reflected_341=341e-6 / (w.k / w.a_rs) ** 2, Ag_if_all_reflected_352=352e-6 / (w.k / w.a_rs) ** 2,
                         refl_ppm_at_Ag_0p048=0.048 * (w.k / w.a_rs) ** 2 * 1e6,
                         Tday_341=tday(341), Tday_352=tday(352), Tday_341_Ag0p048=tday(341, 0.048))

# ------------------------------------------------------------------ 3. asteroseismology numbers
nu_max_sun, dnu_sun = 3090.0, 135.1                      # microHz, Huber et al. 2011
nyq = lambda cad_s: 1e6 / (2 * cad_s)
Tobs = {n: TP.loc[n, "sectors_available"] * 27.4 for n in names}
F["astero"] = dict(nu_max_sun=nu_max_sun, dnu_sun=dnu_sun, period_sun_min=1e6 / nu_max_sun / 60,
                   nyquist_uHz={"20 s": nyq(20), "120 s": nyq(120), "200 s": nyq(200), "600 s": nyq(600), "1800 s": nyq(1800)},
                   res_uHz_27d=1e6 / (27.4 * 86400), res_uHz_300d=1e6 / (300 * 86400), res_uHz_356d=1e6 / (13 * 27.4 * 86400), sun_R=1.0, sun_M=1.0)

# ------------------------------------------------------------------ 4. resolution / field trade-off (FOV = N_pix x scale^2)
A2D = 1 / 3600 ** 2 * (1 / 1)                            # arcsec^2 -> deg^2 : 1 deg^2 = 3600^2 arcsec^2 (as unit-sky area: 1 deg = 3600 arcsec)
to_deg2 = lambda npix, scale: npix * scale ** 2 / 3600 ** 2
mis = [("TESS", 4 * 4096 ** 2, PIX, 2300, "120 s, 20 s; full frame 1800/600/200 s", "continuous 27.4 d per sector"),
       ("Kepler", 42 * 2200 * 1024, 3.98, 115, "1765.8 s, 58.86 s", "one field, continuous"),
       ("PLATO (2014 design)", None, 15.0, 2232, "25 s, 2.5 s", "long stare"),
       ("Roman WFI", 18 * 4088 ** 2, 0.11, 0.281, "15 min (bulge survey)", "72-day seasons"),
       ("Rubin LSST", 3.2e9, 0.2, 9.6, "30 s per visit", "every 3 d on average"),
       ("JWST NIRCam (1 module, SW)", 4 * 2048 ** 2, 0.031, None, "set by the observer", "pointed, no repeat")]
F["tradeoff"] = [dict(name=n, npix=npx, scale=s, fov_computed=(to_deg2(npx, s) if npx else None), fov_quoted=q, cadence=cd, revisit=rv) for n, npx, s, q, cd, rv in mis]
F["tess_fov_from_pixels_deg2"] = to_deg2(4 * 4096 ** 2, PIX)
F["fov_loss_10x_finer"] = 100.0
F["tess_vs_jwst_fov"] = to_deg2(4 * 4096 ** 2, PIX) / to_deg2(4 * 2048 ** 2, 0.031)
F["snr_scaling"] = dict(double_D=2.0, four_times_exposure=2.0, exposure_for_10x_fainter_at_fixed_D_s_ratio=100.0)

# ------------------------------------------------------------------ 5. light-curve checks: PDCSAP formula, dilution, centroid shift
def lc_path(tic, sector):
    f = glob.glob(str(ROOT / "data" / "mast_cache" / "mastDownload" / "TESS" / f"*s{sector:04d}-{tic:016d}-*" / "*_lc.fits"))
    return f[0] if f else None

def window_stats(t, y, tc, T14, base_poly=1):
    dt = t - tc
    inn = np.abs(dt) < 0.25 * T14
    out = (np.abs(dt) > 0.75 * T14) & (np.abs(dt) < 3 * T14)
    return dt, inn, out

def depth_one(t, f, tc, T14, cad_d):
    dt, inn, out = window_stats(t, f, tc, T14)
    exp_in = 0.5 * T14 / cad_d
    if inn.sum() < max(3, 0.6 * exp_in) or (out & (dt < 0)).sum() < 8 or (out & (dt > 0)).sum() < 8:
        return None
    co = np.polyfit(dt[out], f[out], 1)
    res = f[out] - np.polyval(co, dt[out])
    sig = res.std() / np.sqrt(inn.sum())
    base = np.polyval(co, dt[inn])
    return 1e6 * (1 - np.mean(f[inn] / base)), 1e6 * sig / np.mean(base)

def shift_one(t, x, tc, T14, cad_d):
    dt, inn, out = window_stats(t, x, tc, T14)
    exp_in = 0.5 * T14 / cad_d
    if inn.sum() < max(3, 0.6 * exp_in) or (out & (dt < 0)).sum() < 8 or (out & (dt > 0)).sum() < 8:
        return None
    co = np.polyfit(dt[out], x[out], 1)
    res = x[out] - np.polyval(co, dt[out])
    return float(np.mean(x[inn] - np.polyval(co, dt[inn]))), float(res.std() / np.sqrt(inn.sum()))

def wmean(v):
    v = [(a, s) for a, s in v if s > 0]
    if not v:
        return np.nan, np.nan, 0
    a = np.array([x[0] for x in v]); s = np.array([x[1] for x in v]); wgt = 1 / s ** 2
    m = float((a * wgt).sum() / wgt.sum()); e = float(1 / np.sqrt(wgt.sum()))
    chi = float((((a - m) / s) ** 2).sum() / max(len(a) - 1, 1)) if len(a) > 1 else 1.0
    return m, e * max(1.0, np.sqrt(chi)), len(a)

vet = []; ratio_checks = []
for n in names:
    P, t0, T14 = R[n]["fit"]["period"], R[n]["fit"]["t0"], GEO.loc[n, "T14_h"] / 24
    tic = int(RT.loc[n, "tic"]); secs = [int(s) for s in str(R[n]["sectors_used"]).replace("[", "").replace("]", "").split(",") if s.strip()]
    dS, dP, dX, dY, dEv, dOd = [], [], [], [], [], []
    for s in secs:
        p = lc_path(tic, s)
        if p is None:
            continue
        d = fits.open(p)[1].data
        ok = (d["QUALITY"] == 0) & np.isfinite(d["TIME"]) & np.isfinite(d["SAP_FLUX"]) & np.isfinite(d["PDCSAP_FLUX"])
        ratio_checks.append((n, s, float(np.nanmedian(d["PDCSAP_FLUX"][ok]) / np.nanmedian(d["SAP_FLUX"][ok])),
                             float(fits.getheader(p, 1)["CROWDSAP"] / fits.getheader(p, 1)["FLFRCSAP"])))
        t = d["TIME"][ok]; sap = d["SAP_FLUX"][ok]; pdc = d["PDCSAP_FLUX"][ok]
        cx = d["MOM_CENTR1"][ok]; cy = d["MOM_CENTR2"][ok]
        good = np.isfinite(cx) & np.isfinite(cy)
        cad = 120 / 86400
        for e in range(int(np.floor((t.min() - t0) / P)), int(np.ceil((t.max() - t0) / P)) + 1):
            tc = t0 + e * P
            if tc < t.min() or tc > t.max():
                continue
            a = depth_one(t, sap, tc, T14, cad); b = depth_one(t, pdc, tc, T14, cad)
            if a and b:
                dS.append(a[::1]); dP.append(b); (dEv if e % 2 == 0 else dOd).append(b)
            xs = shift_one(t[good], cx[good], tc, T14, cad); ys = shift_one(t[good], cy[good], tc, T14, cad)
            if xs and ys:
                dX.append(xs); dY.append(ys)
    mS, eS, nS = wmean([(a, s) for a, s in dS]); mP, eP, nP = wmean(dP)
    mE, eE, nE = wmean(dEv); mO, eO, nO = wmean(dOd)
    mx, ex, nx = wmean(dX); my, ey, ny = wmean(dY)
    dR = float(np.hypot(mx, my)) if np.isfinite(mx) else np.nan
    vet.append(dict(planet=n, n_transits=nP, depth_sap_ppm=mS, depth_pdcsap_ppm=mP, ratio_sap_over_pdcsap=mS / mP if mP else np.nan,
                    crowdsap=GEO.loc[n, "crowdsap"], depth_even_ppm=mE, depth_odd_ppm=mO,
                    dx_px=mx, dx_err=ex, dy_px=my, dy_err=ey, dR_px=dR, dR_arcsec=dR * PIX,
                    sig_max=float(max(abs(mx) / ex, abs(my) / ey)) if np.isfinite(mx) and ex > 0 and ey > 0 else np.nan))
VET = pd.DataFrame(vet).set_index("planet"); VET.to_csv(ROOT / "results" / "checkpoint_vetting.csv")
rc = pd.DataFrame(ratio_checks, columns=["planet", "sector", "pdc_over_sap", "crowd_over_flfr"])
rc["rel_diff_pct"] = 100 * (rc.pdc_over_sap / rc.crowd_over_flfr - 1)
rc["wrong_formula_ratio"] = 1.0 / TP.loc[rc.planet, "flfrcsap"].values
rc.to_csv(ROOT / "results" / "checkpoint_pdcsap_check.csv", index=False)
F["pdcsap_check"] = dict(n_files=len(rc), max_abs_rel_diff_pct=float(rc.rel_diff_pct.abs().max()),
                         ltt1445_pdc_over_sap=float(rc[rc.planet == "LTT 1445 A b"].pdc_over_sap.mean()),
                         ltt1445_crowd_over_flfr=float(rc[rc.planet == "LTT 1445 A b"].crowd_over_flfr.mean()),
                         ltt1445_wrong=float(rc[rc.planet == "LTT 1445 A b"].wrong_formula_ratio.mean()))
F["dilution"] = dict(ltt1445_crowdsap=float(GEO.loc["LTT 1445 A b", "crowdsap"]), depth_boost=float(1 / GEO.loc["LTT 1445 A b", "crowdsap"]),
                     radius_error_if_ignored=float(np.sqrt(1 / GEO.loc["LTT 1445 A b", "crowdsap"])),
                     depth_ratio_measured=float(VET.loc["LTT 1445 A b", "ratio_sap_over_pdcsap"]))

# ------------------------------------------------------------------ 6. revisit: sectors per planet and gaps
rev = []
for n in names:
    s = TF[TF.planet == n].sort_values("tstart")
    gaps = (s.tstart.values[1:] - s.tstop.values[:-1]) if len(s) > 1 else np.array([])
    rev.append(dict(planet=n, files=len(s), first=s.date_obs.iloc[0][:7], last=s.date_obs.iloc[-1][:7], max_gap_d=float(gaps.max()) if len(gaps) else 0.0,
                    span_d=float(s.tstop.max() - s.tstart.min()), sectors_available=int(TP.loc[n, "sectors_available"]), sectors_used=int(TP.loc[n, "n_sectors_used"])))
REV = pd.DataFrame(rev).set_index("planet"); REV.to_csv(ROOT / "results" / "checkpoint_revisit.csv")

json.dump(F, open(ROOT / "results" / "checkpoint_facts.json", "w"), indent=1, default=float)

# ------------------------------------------------------------------ figures (display size, dpi 100, text >= 20 px = 14.4 pt)
NAVY, RED, GREY = "#273896", "#ED1C24", "#6b7280"
plt.rcParams.update({"font.size": 14.5, "figure.dpi": 100, "savefig.dpi": 100, "axes.spines.top": False, "axes.spines.right": False})
FIG = ROOT / "figures" / "paper"

# (a) separation against pixel
g = GEO.sort_values("theta_arcsec")
fig, ax = plt.subplots(figsize=(11.6, 4.6), constrained_layout=True)
ax.barh([f"{n}" for n in g.index], g.theta_arcsec, color=NAVY, height=0.6)
ax.set_xscale("log"); ax.set_xlim(1e-4, 100); ax.set_xlabel("star-planet separation  a / d  (arcsec)")
from matplotlib.lines import Line2D
refs = ((21, "TESS pixel 21″", RED), (1.92, "TESS diffraction limit 1.9″", "#b45309"), (0.52, "Jupiter at 5.2 AU, star at 10 pc: 0.52″", GREY), (0.031, "JWST NIRCam pixel 0.031″", "#047857"))
for xv, lab, col in refs:
    ax.axvline(xv, color=col, lw=2.4, ls="--")
ax.legend(handles=[Line2D([0], [0], color=c, lw=2.4, ls="--", label=l) for _, l, c in refs], loc="lower right", frameon=True, fontsize=14.5, framealpha=0.95)
fig.savefig(FIG / "ck_separation.png"); plt.close(fig)

# (b) FOV against pixel scale
fig, ax = plt.subplots(figsize=(11.6, 4.8), constrained_layout=True)
pts = [("TESS", PIX, 2300, RED, (14, -8, "left")), ("Kepler", 3.98, 115, GREY, (-12, 10, "right")), ("PLATO (2014 design)", 15.0, 2232, "#b45309", (-12, 12, "right")),
       ("Roman", 0.11, 0.281, "#047857", (12, 4, "left")), ("Rubin", 0.2, 9.6, NAVY, (12, 4, "left")), ("JWST NIRCam, one module", 0.031, 0.0012, "#7c3aed", (12, 4, "left"))]
for nme, sc, fv, col, (dx, dy, ha) in pts:
    ax.scatter(sc, fv, s=150, color=col, zorder=3)
    ax.annotate(nme, (sc, fv), xytext=(dx, dy), textcoords="offset points", ha=ha, color=col, fontsize=14.5)
sx = np.array([0.02, 80])
for npx, lab in ((1e7, "10⁷ pixels"), (1e8, "10⁸"), (1e9, "10⁹"), (1e10, "10¹⁰")):
    ax.plot(sx, npx * sx ** 2 / 3600 ** 2, color="#cbd5e1", lw=1.6, zorder=1)
    ax.text(0.5, npx * 0.5 ** 2 / 3600 ** 2 * 1.35, lab, color=GREY, fontsize=14.5, ha="left", va="bottom", rotation=0)
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(0.02, 60); ax.set_ylim(5e-4, 1e4)
ax.set_xlabel("pixel scale (arcsec per pixel): finer to the left"); ax.set_ylabel("field of view (deg²)")
fig.savefig(FIG / "ck_tradeoff.png"); plt.close(fig)

# (c) wavelength bands (only those verified in data/literature/checkpoint_sources.csv)
bands = [("TESS", 0.6, 1.0, RED), ("Kepler", 0.423, 0.897, GREY), ("PLATO (2014 design)", 0.5, 1.0, "#b45309"),
         ("Rubin ugrizy", 0.32, 1.05, NAVY), ("Roman WFI", 0.48, 2.0, "#047857"), ("JWST mirror", 0.6, 29.0, "#7c3aed")]
fig, ax = plt.subplots(figsize=(11.6, 4.4), constrained_layout=True)
for i, (nme, a_, b_, col) in enumerate(bands[::-1]):
    ax.barh(i, b_ - a_, left=a_, color=col, height=0.55); ax.text(b_ * 1.08, i, f"{nme}  {a_:g}–{b_:g} µm", va="center", color=col, fontsize=14.5)
ax.axvspan(2.0, 20.0, color="#fde68a", alpha=0.35, zorder=0); ax.text(2.1, -0.75, "thermal infrared: young giant planets glow (2 to 20 µm)", fontsize=14.5, color="#92400e", va="center")
ax.set_ylim(-1.1, 5.5); ax.set_xscale("log"); ax.set_xlim(0.3, 400); ax.set_yticks([]); ax.set_xlabel("wavelength (µm)")
fig.savefig(FIG / "ck_bands.png"); plt.close(fig)
print(json.dumps({k: F[k] for k in ("geometry_summary", "roundtrip", "pdcsap_check", "dilution", "phase_wasp18", "astero", "thermal_contrast_1000K", "diffraction_arcsec", "tess_vs_jwst_fov")}, indent=1, default=float))
print(VET.round(3).to_string()); print(REV.to_string())
