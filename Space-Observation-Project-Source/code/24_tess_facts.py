# -*- coding: utf-8 -*-
"""Bước 24 - Thông tin về TESS: (a) số thiết kế đọc từ bài Ricker+2015 và trang NASA/STScI, (b) số ĐO TRÊN 21 file SPOC của dự án (header FITS),
(c) độ phủ của 10 hành tinh so với 471 hành tinh trong catalog theo từng cách chia.
Đầu vào : results/data_manifest.csv, data/mast_cache/**/*_lc.fits, data/candidates_grouped.csv, data/shortlist_mast.csv, results/*/result.json
Đầu ra  : results/tess_files.csv, results/tess_planets.csv, results/tess_design_values.json, results/sample_coverage.csv,
          figures/paper/tess_apertures.png, tess_coverage_raster.png, tess_sectors_vs_lat.png
Mọi con số thiết kế ghi kèm nguồn và dòng trong literature/text/Ricker_2015_*.txt hoặc data/raw/tess_docs/*."""
import json
import pathlib
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy.io import fits
import astropy.units as u

ROOT = pathlib.Path(__file__).resolve().parents[1]
slug = lambda n: re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_")
NAVY, RED, GREY, LIGHT = "#273896", "#ED1C24", "#6b7280", "#c9d0ea"
names = [l.strip() for l in open(ROOT / "data" / "selected.txt") if l.strip()]
ALL = names + ["pi Men c"]
MAN = pd.read_csv(ROOT / "results" / "data_manifest.csv")
G = pd.read_csv(ROOT / "data" / "candidates_grouped.csv").set_index("pl_name")
SHORT = pd.read_csv(ROOT / "data" / "shortlist_mast.csv")
plt.rcParams.update({"font.size": 15, "axes.labelsize": 15, "xtick.labelsize": 14.5, "ytick.labelsize": 14.5, "legend.fontsize": 14.5, "figure.dpi": 100, "savefig.dpi": 100})
files = {p.name: p for p in (ROOT / "data" / "mast_cache").rglob("*_lc.fits")}

# ------------------------------------------------------------------ (b) header của từng file SPOC
rows, masks = [], {}
for _, m in MAN.iterrows():
    h = fits.open(files[m.file]); H0, H1, H2 = h[0].header, h[1].header, h[2].header
    d = h[1].data; t = np.asarray(d["TIME"], float); q = np.asarray(d["QUALITY"]); f = np.asarray(d["PDCSAP_FLUX"], float)
    good = np.isfinite(t) & np.isfinite(f) & (q == 0)
    tg = t[good]; gaps = np.diff(tg); big = np.argsort(gaps)[::-1][:3]
    ap = np.asarray(h[2].data); n_opt = int(((ap & 2) > 0).sum())
    cd = abs(float(H2["CDELT1"]) * float(H2["CDELT2"]) * abs(float(H2["PC1_1"]) * float(H2["PC2_2"]) - float(H2["PC1_2"]) * float(H2["PC2_1"])))
    scale = 3600 * np.sqrt(cd)                                   # cung giây / pixel, từ WCS của mặt nạ khẩu độ
    span = H1["TSTOP"] - H1["TSTART"]; n_exp = span / H1["TIMEDEL"]
    c = SkyCoord(H0["RA_OBJ"] * u.deg, H0["DEC_OBJ"] * u.deg).barycentricmeanecliptic
    r = dict(planet=m.planet, sector=int(H0["SECTOR"]), camera=int(H0["CAMERA"]), ccd=int(H0["CCD"]), tmag=H0["TESSMAG"], date_obs=H0["DATE-OBS"][:10],
             ra=H0["RA_OBJ"], dec=H0["DEC_OBJ"], ecl_lon=c.lon.deg, ecl_lat=c.lat.deg, tstart=H1["TSTART"], tstop=H1["TSTOP"], span_d=span,
             timedel_s=H1["TIMEDEL"] * 86400, int_time_s=H1["INT_TIME"], frametim_s=H1["FRAMETIM"], num_frm=int(H1["NUM_FRM"]), deadc=H1["DEADC"],
             exposure_d=H1["EXPOSURE"], eff_exp_per_cadence_s=H1["EXPOSURE"] / n_exp * 86400,
             n_cadences=len(t), n_good=int(good.sum()), duty_good=good.sum() / n_exp, largest_gap_d=float(gaps[big[0]]), gap_start=float(tg[big[0]]),
             crowdsap=H1["CROWDSAP"], flfrcsap=H1["FLFRCSAP"], npix_opt=n_opt, stamp=f"{ap.shape[1]}x{ap.shape[0]}", pix_scale_arcsec=scale,
             r_eq_arcsec=np.sqrt(n_opt / np.pi) * scale, cdpp05_ppm=H1.get("CDPP0_5"), cdpp1_ppm=H1.get("CDPP1_0"), cdpp2_ppm=H1.get("CDPP2_0"), pdcvar=H1.get("PDCVAR"))
    rows.append(r); masks[(m.planet, int(H0["SECTOR"]))] = ap
F = pd.DataFrame(rows)
F.to_csv(ROOT / "results" / "tess_files.csv", index=False)

# ------------------------------------------------------------------ theo hành tinh
P = []
for n in names:        # pi Men c không có trong candidates_grouped.csv (không có sy_dist, thời lượng transit), nên bảng theo hành tinh chỉ có 10 hành tinh
    pass
for n in names:
    r = json.load(open(ROOT / "results" / slug(n) / "result.json")); fl = F[F.planet == n].sort_values("sector"); a = fl.iloc[0]; g = G.loc[n]
    dist = g.sy_dist
    P.append(dict(planet=n, sectors_used=" ".join(map(str, fl.sector)), n_sectors_used=len(fl), sectors_available=r.get("sectors_available"), camera=" ".join(map(str, sorted(set(fl.camera)))),
                  tmag=a.tmag, ecl_lat=a.ecl_lat, dist_pc=dist, pixel_au=a.pix_scale_arcsec * dist, npix_opt=int(fl.npix_opt.median()), r_eq_arcsec=fl.r_eq_arcsec.median(),
                  crowdsap_min=fl.crowdsap.min(), crowdsap_max=fl.crowdsap.max(), flfrcsap=fl.flfrcsap.median(), cdpp1_ppm=fl.cdpp1_ppm.median(),
                  trandur_h=g.pl_trandur, points_per_transit=g.pl_trandur * 3600 / a.timedel_s, depth_ppm=1e6 * r["fit"]["ror"] ** 2, first_obs=fl.date_obs.min()))
PL = pd.DataFrame(P)
PL["snr_1h_transit"] = PL.depth_ppm / PL.cdpp1_ppm      # độ sâu / CDPP 1 giờ: chỉ số thô, không phải S/N của fit
PL.to_csv(ROOT / "results" / "tess_planets.csv", index=False)

# ------------------------------------------------------------------ (a) số thiết kế (nguồn: bài Ricker+2015; trang NASA/STScI) và số tính từ chúng
R = "Ricker+2015 (literature/text/Ricker_2015_*.txt)"
pix_arcsec = 0.35 * 60                       # Ricker Table 1: one pixel = 0.35 arcmin
cap = lambda a_deg2: np.degrees(np.arccos(1 - np.radians(1) ** 2 * a_deg2 / (2 * np.pi)))   # nửa góc mở của chỏm cầu có diện tích a (độ^2); chỉ để tham khảo
D = dict(
    orbit=dict(period_d=13.7, perigee_Re=17, apogee_Re=59, resonance="2:1 with the Moon", downlink="every 13.7 d at perigee", src=R + " Sec 6, lines 236, 324, 343"),
    cameras=dict(n=4, fov_each_deg=(24, 24), fov_total_deg=(24, 96), fov_total_deg2=2300, pupil_cm=10.5, f_number=1.4, band_nm=(600, 1000), src=R + " Table 1, Sec 4.1"),
    detector=dict(ccds_per_camera=4, ccd_px=2048, pixel_um=15, src=R + " Sec 4.2, line 280"),
    pixel=dict(arcmin=0.35, arcsec=pix_arcsec, deg=pix_arcsec / 3600, px_per_deg=3600 / pix_arcsec, mosaic_px=2 * 2048, mosaic_deg=2 * 2048 * pix_arcsec / 3600,
               ensq50="50 % of the energy within 1 pixel (0.35 arcmin)", ensq90="90 % within 4x4 pixels (1.4 arcmin)", ensq90_arcsec=4 * pix_arcsec,
               src=R + " Table 1 (lines 300-301); 21 arcsec/pixel also on archive.stsci.edu/missions-and-data/tess"),
    sectors=dict(length_d=27.4, orbits_per_sector=2, per_hemisphere=13, ecl_lat_from_deg=6, shift_deg=27, hemisphere_yr=1, all_sky_yr=2,
                 area_ge27d=30000, area_gt80d=2800, area_gt300d=900, sphere_deg2=4 * np.pi * (180 / np.pi) ** 2, src=R + " Sec 7.2, lines 383-436"),
    sampling=dict(frames_s=2, frames_per_2min=60, targets_2min=200000, ffi_primary_min=30, noise_floor_ppm_per_hour=60, src=R + " lines 40-41, 318, 522, 598"),
    cadence_by_cycle=dict(ffi="30 min (cycles 1-2), 10 min (cycles 3-4), 200 s (cycles 5+)", lc="2 min since the primary mission; 20 s since the first extended mission",
                          src="heasarc.gsfc.nasa.gov/docs/tess/data-products.html (data/raw/tess_docs/)"),
    year_sectors={"1": "S1-13", "2": "S14-26", "3": "S27-39", "4": "S40-55", "5": "S56-69", "6": "S70-83", "7": "S84-96", "8": "S97-107"},
    derived=dict(frac_sphere_ge27d=30000 / (4 * np.pi * (180 / np.pi) ** 2), cap_deg_2800=float(cap(2800)), cap_deg_900=float(cap(900)),
                 note="derived here from the areas quoted by Ricker+2015, not quoted by them"),
    measured=dict(n_files=len(F), timedel_s_set=sorted(set(F.timedel_s.round(3))), span_d=(F.span_d.min(), F.span_d.median(), F.span_d.max()),
                  largest_gap_d=(F.largest_gap_d.min(), F.largest_gap_d.median(), F.largest_gap_d.max()), duty_good=(F.duty_good.min(), F.duty_good.median(), F.duty_good.max()),
                  deadc_set=sorted(set(F.deadc.round(3))), eff_exp_s=(F.eff_exp_per_cadence_s.min(), F.eff_exp_per_cadence_s.max()), pix_scale_arcsec=(F.pix_scale_arcsec.min(), F.pix_scale_arcsec.max()),
                  cameras=sorted(set(F.camera)), sectors=sorted(set(F.sector)), first=F.date_obs.min(), last=F.date_obs.max(), src="header of the 21 SPOC files in results/data_manifest.csv"))
json.dump(D, open(ROOT / "results" / "tess_design_values.json", "w"), indent=1, ensure_ascii=False, default=float)

# ------------------------------------------------------------------ (c) độ phủ của mẫu theo từng cách chia
cov = []
order = {"g_size": ["Earth-size", "Super-Earth", "Sub-Neptune", "Neptune/Saturn", "Jupiter-size"], "g_period": ["USP (<1 d)", "Hot (1-3 d)", "Warm (3-7 d)", "Cool (7-15 d)"],
         "g_teq": ["Ultra-hot (>2000 K)", "Hot (1200-2000 K)", "Warm (500-1200 K)", "Temperate (<500 K)"], "g_star": ["M dwarf", "K dwarf", "G (Sun-like)", "F/hotter"]}
sel = G.loc[names]
for ax_, groups in order.items():
    for grp in groups:
        nc = int((G[ax_] == grp).sum()); ns = int((sel[ax_] == grp).sum())
        cov.append(dict(axis=ax_, group=grp, catalog_n=nc, catalog_pct=100 * nc / len(G), ours_n=ns, ours_pct=100 * ns / len(sel)))
cov.append(dict(axis="discoverymethod", group="Transit", catalog_n=int((G.discoverymethod == "Transit").sum()), catalog_pct=100 * (G.discoverymethod == "Transit").mean(), ours_n=int((sel.discoverymethod == "Transit").sum()), ours_pct=100 * (sel.discoverymethod == "Transit").mean()))
cov.append(dict(axis="discoverymethod", group="Radial Velocity", catalog_n=int((G.discoverymethod == "Radial Velocity").sum()), catalog_pct=100 * (G.discoverymethod == "Radial Velocity").mean(), ours_n=int((sel.discoverymethod == "Radial Velocity").sum()), ours_pct=100 * (sel.discoverymethod == "Radial Velocity").mean()))
cov.append(dict(axis="sy_pnum", group="more than one planet in the system", catalog_n=int((G.sy_pnum > 1).sum()), catalog_pct=100 * (G.sy_pnum > 1).mean(), ours_n=int((sel.sy_pnum > 1).sum()), ours_pct=100 * (sel.sy_pnum > 1).mean()))
cov.append(dict(axis="radius_valley", group="1.5-2.0 R_earth", catalog_n=int(G.pl_rade.between(1.5, 2.0).sum()), catalog_pct=100 * G.pl_rade.between(1.5, 2.0).mean(), ours_n=int(sel.pl_rade.between(1.5, 2.0).sum()), ours_pct=100 * sel.pl_rade.between(1.5, 2.0).mean()))
COV = pd.DataFrame(cov); COV.to_csv(ROOT / "results" / "sample_coverage.csv", index=False)

# ------------------------------------------------------------------ hình 1: mặt nạ khẩu độ thật của 10 hành tinh
fig, axs = plt.subplots(2, 5, figsize=(9.6, 4.3), constrained_layout=True)
for ax, n in zip(axs.ravel(), names):
    fl = F[F.planet == n].sort_values("sector").iloc[0]; ap = masks[(n, int(fl.sector))]
    img = np.where((ap & 2) > 0, 2, np.where((ap & 1) > 0, 1, 0))
    ax.imshow(img, cmap=matplotlib.colors.ListedColormap(["white", LIGHT, NAVY]), vmin=0, vmax=2, origin="lower", interpolation="nearest", aspect="equal")
    ax.set_xticks(np.arange(-0.5, ap.shape[1], 1), minor=True); ax.set_yticks(np.arange(-0.5, ap.shape[0], 1), minor=True)
    ax.grid(which="minor", color="white", lw=0.6); ax.tick_params(which="both", length=0, labelbottom=False, labelleft=False)
    ax.set_title(n, fontsize=14.5, pad=3)
    ax.set_xlabel(f"{int(fl.npix_opt)} px, r = {fl.r_eq_arcsec:.0f}″\nCROWDSAP {fl.crowdsap:.3f}", fontsize=14.5, labelpad=3)
    for s in ax.spines.values(): s.set_visible(False)
from matplotlib.patches import Patch
fig.legend(handles=[Patch(color=NAVY, label="optimal aperture (summed)"), Patch(color=LIGHT, label="downloaded pixel"), Patch(facecolor="white", edgecolor=GREY, label="not downloaded")], loc="outside lower center", ncol=3, frameon=False)
fig.savefig(ROOT / "figures" / "paper" / "tess_apertures.png"); plt.close(fig)

# ------------------------------------------------------------------ hình 2: dữ liệu có mặt theo thời gian trong từng file (khoảng trống = chuyển quỹ đạo, momentum dump, mất dữ liệu)
fig, ax = plt.subplots(figsize=(7.4, 5.2), constrained_layout=True)
Fs = F.sort_values(["planet", "sector"]).reset_index(drop=True)
Fs["order"] = Fs.planet.map({n: i for i, n in enumerate(ALL)}); Fs = Fs.sort_values(["order", "sector"]).reset_index(drop=True)
for i, r in Fs.iterrows():
    h = fits.open(files[MAN[(MAN.planet == r.planet) & (MAN.sector == r.sector)].file.iloc[0]]); d = h[1].data
    t = np.asarray(d["TIME"], float); ok = np.isfinite(t) & np.isfinite(np.asarray(d["PDCSAP_FLUX"], float)) & (np.asarray(d["QUALITY"]) == 0)
    bins = np.arange(0, np.ceil(r.span_d) + 0.1, 0.1); cnt, _ = np.histogram(t[ok] - r.tstart, bins)
    runs = np.flatnonzero(np.diff(np.r_[0, cnt > 0, 0]))
    for a_, b_ in zip(runs[::2], runs[1::2]):
        ax.barh(i, (b_ - a_) * 0.1, left=a_ * 0.1, height=0.78, color=NAVY, lw=0)
ax.set_yticks(range(len(Fs))); ax.set_yticklabels([f"{r.planet} S{r.sector}" for _, r in Fs.iterrows()]); ax.set_ylim(len(Fs) - 0.4, -1.7)
ax.set_xlabel("Days since the start of the sector"); ax.set_xlim(0, 28.5); ax.axvline(13.7, color=RED, lw=1.5, ls="--")
ax.text(13.95, -1.05, "13.7 d: one orbit", color=RED, fontsize=14.5, va="center")
fig.savefig(ROOT / "figures" / "paper" / "tess_coverage_raster.png"); plt.close(fig)

# ------------------------------------------------------------------ hình 3: số sector SPOC 2 phút theo vĩ độ hoàng đạo (87 hành tinh trong shortlist) và 10 hành tinh của ta
S2 = SHORT.copy(); S2["abs_lat"] = S2.elat.abs()
fig, ax = plt.subplots(figsize=(6.4, 4.2), constrained_layout=True)
ax.scatter(S2.abs_lat, S2.n_sectors, s=46, color=LIGHT, edgecolor=GREY, lw=0.6, label=f"{len(S2)} shortlisted planets", zorder=2)
mine = PL
ax.scatter(mine.ecl_lat.abs(), mine.sectors_available, s=90, color=RED, zorder=3, label="our ten")
for n_, dx, dy in (("K2-141 b", 12, 30), ("WASP-62 b", -112, -6), ("WASP-18 b", -110, 10)):      # chỉ gắn nhãn 3 điểm; bảng đầy đủ nằm trên slide
    r = mine[mine.planet == n_].iloc[0]
    ax.annotate(n_, (abs(r.ecl_lat), r.sectors_available), xytext=(dx, dy), textcoords="offset points", fontsize=14.5, color="black", arrowprops=dict(arrowstyle="-", color=GREY, lw=1))
ax.axvline(6, color=GREY, lw=1.2, ls="--"); ax.text(7, ax.get_ylim()[1] * 0.97, "6°: strips start", color=GREY, fontsize=14.5, va="top")
ax.set(xlabel="|ecliptic latitude| (deg)", ylabel="SPOC 2-min sectors available", xlim=(0, 92)); ax.grid(alpha=0.3); ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.86), frameon=True)
fig.savefig(ROOT / "figures" / "paper" / "tess_sectors_vs_lat.png"); plt.close(fig)

pd.set_option("display.width", 260); pd.set_option("display.max_columns", 40)
print(F[["planet", "sector", "camera", "ccd", "date_obs", "span_d", "largest_gap_d", "duty_good", "crowdsap", "npix_opt", "r_eq_arcsec", "pix_scale_arcsec", "cdpp1_ppm", "eff_exp_per_cadence_s"]].round(3).to_string(index=False))
print(PL[["planet", "sectors_used", "sectors_available", "camera", "tmag", "ecl_lat", "dist_pc", "pixel_au", "crowdsap_min", "trandur_h", "points_per_transit", "depth_ppm", "cdpp1_ppm", "snr_1h_transit"]].round(2).to_string(index=False))
print(json.dumps(D["measured"], default=float)); print(json.dumps(D["derived"], default=float)); print(COV.round(1).to_string(index=False))
