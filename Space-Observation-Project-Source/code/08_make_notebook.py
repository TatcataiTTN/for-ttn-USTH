"""Bước 8 - Tạo notebook hướng dẫn (tutorial style) đo bán kính + chu kỳ cho MỘT hành tinh (HD 118203 b)."""
import nbformat as nbf, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
C = []
md = lambda s: C.append(nbf.v4.new_markdown_cell(s))
code = lambda s: C.append(nbf.v4.new_code_cell(s))

md("""# Measuring an exoplanet's radius and orbital period with TESS
**Target:** HD 118203 b (the benchmark planet of the *Quick fits for TESS light curves* tutorial, exoplanet-case-studies).  
**Pipeline:** SPOC light curve → flatten → Box Least Squares → transit model (batman) + MCMC (emcee) → physical radius.  
Physics: a transit blocks a fraction δ ≈ (R_p/R_★)² of the starlight, so R_p = (R_p/R_★) · R_★; the time between transits is the period P.""")
code("""import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path.cwd().parent / "code"))
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import transit_pipeline as tp
cat = pd.read_csv("../data/raw/tess_catalog.csv")
row = cat[cat.pl_name == "HD 118203 b"].iloc[0]
tic = int(row.tic_num)
print("TIC", tic, "| Tmag", row.sy_tmag, "| R* =", row.st_rad, "Rsun | catalog P =", row.pl_orbper, "d | catalog Rp =", round(row.pl_rade, 2), "Rearth")""")
md("## 1. Download the TESS SPOC 2-minute light curve (PDCSAP flux)")
code("""lcs, sectors, n_all = tp.load_lightcurve(tic, max_sectors=4)
print("sectors used:", sectors, "of", n_all, "available;", sum(len(l) for l in lcs), "points")
raw = tp.lk.LightCurveCollection(lcs).stitch()
fig, ax = plt.subplots(figsize=(11, 3)); ax.plot(raw.time.value, raw.flux.value, ".", ms=1.5, color="0.4")
ax.set(xlabel="BTJD (d)", ylabel="Normalised flux"); plt.show()""")
md("## 2. Flatten the light curve (remove slow stellar / instrumental trends)\nSavitzky–Golay filter, window 1.5 d; outliers clipped at +5σ.")
code("""lc = tp.flatten(lcs, 1.5).remove_nans().remove_outliers(sigma_upper=5, sigma_lower=50)
t, f, fe = lc.time.value, lc.flux.value, lc.flux_err.value
fig, ax = plt.subplots(figsize=(11, 3)); ax.plot(t, f, ".", ms=1.5, color="navy"); ax.set(xlabel="BTJD (d)", ylabel="Flattened flux"); plt.show()""")
md("## 3. Box Least Squares: find the period, epoch, duration and depth")
code("""bls, per_grid, power = tp.run_bls(t, f, fe)
print(bls)
fig, ax = plt.subplots(figsize=(7, 3.5)); ax.plot(per_grid, power, lw=0.8); ax.axvline(bls.period, color="r", ls="--")
ax.set(xscale="log", xlabel="Trial period (d)", ylabel="BLS SNR"); plt.show()""")
md("## 4. Re-flatten with the transits masked, then fit a physical transit model\nQuadratic limb darkening (Kipping q1, q2), circular orbit; parameters t0, P, R_p/R_★, b, a/R_★. MCMC with `emcee`.")
code("""msk = tp.in_transit_mask(bls.period, bls.t0, 3.0 * bls.duration)
lc2 = tp.flatten(lcs, max(8 * bls.duration, 1.5), mask=msk).remove_nans().remove_outliers(sigma_upper=5, sigma_lower=50)
fit, chain, (tt, ff, fee, mdl, med) = tp.fit_transit(lc2.time.value, lc2.flux.value, lc2.flux_err.value, bls, nstep=1500)
print(f"P = {fit.period:.5f} +/- {fit.period_err:.5f} d   (catalog {row.pl_orbper:.5f})")
print(f"Rp/R* = {fit.ror:.4f} +/- {fit.ror_err:.4f}   (tutorial: 0.0554)")
print(f"b = {fit.b:.2f},  a/R* = {fit.a_rs:.1f},  {fit.n_transits} transits")""")
code("""ph = (tt - fit.t0 + 0.5 * fit.period) % fit.period - 0.5 * fit.period
o = np.argsort(ph)
fig, ax = plt.subplots(figsize=(7, 4.5)); ax.plot(ph * 24, (ff - 1) * 1e3, ".", ms=2, color="0.7")
ax.plot(ph[o] * 24, (mdl[o] - 1) * 1e3, color="r", lw=2); ax.set(xlabel="Hours from mid-transit", ylabel="Flux (ppt)"); plt.show()""")
md("## 5. From Rp/R★ to a physical radius\nThe light curve only gives the *ratio*. The stellar radius R★ (from the catalog) converts it into R⊕. Its uncertainty is usually the limiting factor.")
code("""rp, rp_err, rj, rj_err = tp.physical_radius(fit, float(row.st_rad), float(row.st_raderr1))
print(f"Rp = {rp:.2f} +/- {rp_err:.2f} Rearth = {rj:.2f} Rjup")
print(f"catalog: {row.pl_rade:.2f} Rearth  ->  difference {100*(rp-row.pl_rade)/row.pl_rade:+.1f} %")
print(f"catalog Rp/R*: {row.pl_ratror:.4f}  ->  difference {100*(fit.ror-row.pl_ratror)/row.pl_ratror:+.1f} %")""")
md("""## 6. Compare with the full 10-planet results
The batch pipeline (`code/04_measure_planet.py`) repeats this for every planet and adds the **systematic error** from three detrending variants (half-range of Rp/R★), quadratically summed with the MCMC error.""")
code("""rows = []
for n in [l.strip() for l in open("../data/selected.txt") if l.strip()]:
    r = json.load(open("../results/" + tp.re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_") + "/result.json")) if hasattr(tp, "re") else None
""")
C.pop()
code("""import re
rows = []
for n in [l.strip() for l in open("../data/selected.txt") if l.strip()]:
    r = json.load(open("../results/" + re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_") + "/result.json"))
    rows.append(dict(planet=n, mode=r.get("mode", "blind"), P_meas=round(r["fit"]["period"], 5), P_cat=r["catalog"]["period"],
                     ror=round(r["fit"]["ror"], 4), Rp_meas=round(r["rp_rearth"], 2), Rp_err=round(r["rp_rearth_err"], 2),
                     Rp_cat=r["catalog"]["rade"], dRp_pct=round(r["delta_radius_pct"], 1)))
pd.DataFrame(rows)""")
nb = nbf.v4.new_notebook(); nb.cells = C
nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
nbf.write(nb, ROOT / "notebooks" / "01_measure_one_planet.ipynb")
print("ok")
