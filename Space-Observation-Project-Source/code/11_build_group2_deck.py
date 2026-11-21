# -*- coding: utf-8 -*-
"""Bước 11 - Dựng deck 'Space-Observation-Project-Group-2' theo mẫu USTH (deck Gia-Lam-Slides + skill build-complete-self-study-system).
Ra: Space-Observation-Project-Group-2/{index.html, assets/, img/, demo/, notebooks/}.  Số liệu lấy từ results/*/result.json."""
import html
import json
import pathlib
import re
import shutil

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "slides" / "Space-Observation-Project-Group-2"
for d in ("assets", "img", "demo", "notebooks"):
    (OUT / d).mkdir(parents=True, exist_ok=True)

slug = lambda n: re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_")
names = [l.strip() for l in open(ROOT / "data" / "selected.txt") if l.strip()]
stress = [l.strip() for l in open(ROOT / "data" / "stress_tests.txt") if l.strip()]
cat = pd.read_csv(ROOT / "data" / "raw" / "tess_catalog.csv")
grp = pd.read_csv(ROOT / "data" / "candidates_grouped.csv").set_index("pl_name")
R = {n: json.load(open(ROOT / "results" / slug(n) / "result.json")) for n in names + stress}
C = {n: cat[cat.pl_name == n].iloc[0] for n in names + stress}
NUM = {n: i for i, n in enumerate(names, 1)}
n_all, n_pool = len(cat), len(grp)
short = lambda s: re.sub(r"\s*\(.*\)", "", s)

# ---------------------------------------------------------------- tệp tĩnh
shutil.copy(ROOT / "slides" / "assets" / "usth" / "usth_logo.png", OUT / "assets" / "usth_logo.png")
shutil.copy(ROOT / "slides" / "assets" / "usth" / "usth_dses_logo.png", OUT / "assets" / "usth_dses_logo.png")
for f in (ROOT / "slides" / "assets" / "images").glob("*.png"):
    if f.name.startswith("usth"):
        continue
    shutil.copy(f, OUT / "img" / f.name)
shutil.copytree(ROOT / "slides" / "demo", OUT / "demo", dirs_exist_ok=True)
shutil.copy(ROOT / "notebooks" / "01_measure_one_planet.ipynb", OUT / "notebooks" / "01_measure_one_planet.ipynb")

# ---------------------------------------------------------------- helpers HTML (cùng class với deck Gia-Lam)
CHIP = '<div class="logo-chip"><img src="assets/usth_logo.png" alt="USTH"><img src="assets/usth_dses_logo.png" alt="DSES"></div>'
_pg = [0]


def esc(s): return html.escape(s, quote=True)


def sl(title, body, notes, appendix=False):
    _pg[0] += 1
    return (f'<section class="mdeck-slide th0 has-logo" data-notes="{esc(notes)}">{CHIP}<h2><span>{title}</span></h2>'
            f'<div class="body">{body}</div><span class="pg">{_pg[0]}</span></section>')


def card(h, t, c="navy", mh=0): return f'<div class="card {c}" style="min-height:{mh}px"><h3>{h}</h3><p>{t}</p></div>'
def cols(*cs): return '<div class="cols">' + "".join(cs) + "</div>"
def take(t): return f'<div class="take">{t}</div>'
def note(t): return f'<p class="note">{t}</p>'
def fig(name, w, cap): return f'<figure class="figd"><img src="img/{name}.png" style="width:{w}px" alt=""><figcaption>{cap}</figcaption></figure>'
def tbl(head, rows, cls="tbl"):
    h = "".join(f"<th>{x}</th>" for x in head)
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<table class="{cls}"><tr>{h}</tr>{r}</table>'
def pill(t, c="old"): return f'<span class="pill {c}">{t}</span>'
def fm(eq, fn=""): return f'<div class="fm"><div class="fe">{eq}</div>' + (f'<div class="fn">{fn}</div>' if fn else "") + "</div>"
def flow(steps, hl=(), tall=False):
    out = []
    for i, s in enumerate(steps):
        out.append(f'<div class="step{" hl" if i in hl else ""}"><span>{s}</span></div>')
        if i < len(steps) - 1: out.append('<div class="arrow">&#8594;</div>')
    return f'<div class="flow{" tall" if tall else ""}">' + "".join(out) + "</div>"
def sgn(x, d=1):
    return f"{0.0:.{d}f}%" if abs(x) < 0.5 * 10 ** (-d) else f"{x:+.{d}f}%"
def pct(a, b): return 100 * (a - b) / b
def rp_err_pct(n): return 100 * R[n]["rp_rearth_err"] / R[n]["rp_rearth"]


S = []
# =============================================================== 1 cover
S.append('<section class="mdeck-slide cover" data-notes="25 minutes for slides 1 to 26; the appendix is for questions. Follow the course report: introduction (what, why), methods (where, how), results, discussion, conclusions. Say at the start that the pipeline is validated on the tutorial planet and that the failures are shown on purpose.">'
         '<div class="cover-logos"><img src="assets/usth_logo.png" style="height:70px"><img src="assets/usth_dses_logo.png" style="height:70px"></div>'
         '<h2>Measuring exoplanet radii and orbital periods with TESS</h2><div class="body"><p class="sub">Ten planets, one pipeline: from public light curves to planet sizes, grouped by size, orbit, star, distance and sky position</p>'
         '<p class="who"><b>Project:</b> Space Observation Project 1, Group 2<br><b>Lecturer:</b> Dr. Nguyen Thi Phuong<br>USTH, Master 2 Space, 25 November 2026</p></div></section>')

# =============================================================== 2-3 introduction
S.append(sl("1  Introduction. What? One question, three checks",
            take("From a raw TESS light curve, how closely can we recover a planet's orbital period and radius, and for which kinds of planet does it fail?")
            + cols(card("Period", f"All ten periods agree with the NASA Exoplanet Archive to 0.03 % or better.", "orange", 270),
                   card("Radius", "Eight of ten radii agree within 4 %; the largest gap is 7.3 % (K2-141 b). Every gap is within 1.4σ.", "navy", 270),
                   card("Coverage", "Ten planets from 1.1 to 15.7 R⊕ and 0.28 to 6.1 d, plus two stress tests that fail.", "navy", 270))
            + note("We measure; the catalog is only the answer key. A radius needs the stellar radius, which does not come from the light curve."),
            "One question, three checks: period, radius, coverage. The numbers on this slide are the final results, shown first so the audience knows where we are going."))

S.append(sl("1  Introduction. Why? A transit gives a ratio, and the course formulas turn it into a size",
            fig("phys_transit", 1160, "Two transits of a planet crossing the stellar disc: spacing gives the period, depth the radius ratio, width the geometry.")
            + cols(fm("&Delta;L / L = ( R<sub>p</sub> / R<sub>&#9733;</sub> )<sup>2</sup>", "Depth; so R<sub>p</sub> = R<sub>&#9733;</sub> &radic;(&Delta;L/L)."),
                   fm("P<sub>transit</sub> = R<sub>&#9733;</sub> / a", "Geometric probability that the orbit is aligned."),
                   fm("T &asymp; ( P / &pi; ) ( R<sub>&#9733;</sub> / a )", "Duration of a central transit.")),
            "These three formulas are the course formulas on transits (lecture review, section C). Example from the review: depth 0.64 %, R star 0.8 solar radii gives Rp/R star 0.08 and Rp 0.064 solar radii. Our pipeline does this fit properly, with limb darkening and MCMC, instead of reading the depth by eye."))

# =============================================================== 4-7 methods: where / which
need = ["pl_orbper", "pl_rade", "st_rad", "pl_trandep", "pl_trandur", "sy_dist", "st_teff", "sy_tmag"]
f0 = cat.dropna(subset=need); f1 = f0[f0.sy_tmag < 11]; f2 = f1[f1.pl_orbper < 15]; f3 = f2[f2.pl_trandep > 0.05]
S.append(sl("2  Methods. Where? From 4,826 archive planets to ten",
            flow([f"{n_all:,}<br>with TIC ID", f"{len(f0):,}<br>complete entry", f"{len(f1):,}<br>Tmag &lt; 11", f"{len(f2):,}<br>P &lt; 15 d",
                  f"{len(f3):,}<br>depth &gt; 500 ppm", f"{n_pool}<br>S/N &gt; 12", "10 + 2<br>chosen"], hl=(5, 6), tall=True)
            + note("Estimated S/N: depth divided by a simple one-hour noise model scaled with Tmag and the number of transits per sector.") + take("Every cut keeps planets that a single 27-day TESS sector can measure: bright star, at least two transits, a deep dip.")
            + note("Source: NASA Exoplanet Archive, table pscomppars (TAP), transiting planets with a TIC identifier; light curves: TESS SPOC 2-minute PDCSAP from MAST."),
            "Funnel. Tmag below 11 keeps the noise low, P below 15 days gives two or more transits in one sector, and the estimated S over N above 12 uses a simple noise model. Ten plus two: ten representatives and two stress-test planets."))

ax_rows = [("Size", "Earth-size &lt; 1.25 · Super-Earth &lt; 2 · Sub-Neptune &lt; 4 · Neptune/Saturn &lt; 8 · Jupiter-size &ge; 8 R<sub>&oplus;</sub>"),
           ("Orbit", "USP &lt; 1 d · Hot 1 to 3 d · Warm 3 to 7 d · Cool 7 to 15 d"),
           ("Star", "M &lt; 3900 K · K &lt; 5200 K · G &lt; 6000 K · F or hotter"),
           ("Distance", "Near &lt; 50 pc · Mid 50 to 150 pc · Far &gt; 150 pc"),
           ("Sky", "CVZ |&beta;| &gt; 78&deg; · High 54 to 78&deg; · Low &lt; 54&deg; (ecliptic latitude)"),
           ("System", "Single or multi-planet; found by TESS or before TESS")]
S.append(sl("2  Methods. Which? Six axes decide the representatives",
            tbl(["Axis", "Classes"], ax_rows) + take("Rule: each representative must add a class not yet covered, and have SPOC 2-minute data."),
            "Size, orbit, star, distance, sky position and system type. The sky axis matters for TESS: the continuous viewing zone near the ecliptic poles is observed for about a year, low latitudes for one or two sectors."))

S.append(sl("2  Methods. Which? The ten planets span every size and orbit class",
            fig("ov_radius_period", 1160, "Grey: all 4,825 transiting planets with a TIC ID and radius. Blue: the 471 measurable ones. Red numbers: our ten planets."),
            "Read the figure left to right: ultra-short periods on the left. Numbers 4 and 6 are the USP gas giants and Neptune; 8 and 9 are the small planets of M dwarfs. The sky map and the distance-star plane are in the appendix (A3, A4)."))

rows = [[f"<b>{NUM[n]}</b> {n}", short(grp.loc[n].g_size), short(grp.loc[n].g_period), short(grp.loc[n].g_star), f"{C[n].sy_dist:.0f}", short(grp.loc[n].g_sky), short(grp.loc[n].g_system)] for n in names]
S.append(sl("2  Methods. Which? Ten representatives and the group each one covers",
            tbl(["Planet", "Size", "Orbit", "Star", "pc", "Sky", "System"], rows, "tbl md"),
            "This table is the map for the next ten slides. Planet 5 is the southern continuous viewing zone target, planet 8 is the nearest system, planet 9 the smallest planet."))

# =============================================================== 8-9 methods: how
S.append(sl("2  Methods. How? The tutorial recipe, rebuilt with batman and emcee",
            flow(["Download<br>SPOC PDCSAP", "Flatten<br>Savitzky-Golay", "BLS<br>P, t<sub>0</sub>, depth", "Fit transit<br>batman + emcee", "&times; R<sub>&#9733;</sub><br>radius"], hl=(2, 3))
            + cols(card("Same as the tutorial", "Quick fits for TESS light curves: SPOC PDCSAP, remove NaNs and outliers, BLS, mask the transits, fit a limb-darkened model."),
                   card("Our changes", "PyMC3 and exoplanet replaced by batman and emcee (same Mandel-Agol model). Three detrending variants give a systematic error.", "orange"),
                   card("Radius", "Light curve gives R<sub>p</sub>/R<sub>&#9733;</sub>; R<sub>&#9733;</sub> comes from the archive; total error adds MCMC, detrending and R<sub>&#9733;</sub>."))
            + note("Search modes: blind = BLS over 0.26 to 15 d; guided = within &plusmn;3 % of the catalog period, durations scaled from the catalog duration (appendix A10)."),
            "Walk the five boxes. The tutorial uses PyMC3 and exoplanet; we use batman and emcee because they install cleanly; the physical model is the same and the benchmark confirms it. Be explicit about blind and guided: seven planets are blind, three guided."))

S.append(sl("2  Methods. How? BLS finds the period, the model fit finds the radius ratio",
            cols(fig("m_bls", 570, "BLS power against trial period, HD 118203 b: best P = 6.1351 d."),
                 fig("m_fold", 570, "Folded transit, binned means and best-fit model."))
            + take("Blind BLS recovers the catalog period of the benchmark to 10<sup>-5</sup> before any fit; the fit then gives R<sub>p</sub>/R<sub>&#9733;</sub> = 0.0553."),
            "Left: BLS slides a box over the folded curve for each trial period. Right: the transit model with quadratic limb darkening, seven free parameters, 32 walkers. The raw and detrended curves are in appendix A5."))

# =============================================================== 10 benchmark
b = R["HD 118203 b"]
S.append(sl("3  Results. Benchmark: HD 118203 b reproduces the tutorial",
            fig("m_post", 1160, "MCMC posteriors of R<sub>p</sub>/R<sub>&#9733;</sub> and the period; red lines: tutorial value 0.0554 and catalog period 6.13498 d.")
            + note(f"The radius gap is a stellar-radius effect: the catalog radius implies R<sub>&#9733;</sub> = {b['rstar_implied_by_catalog']:.2f} R<sub>&#9737;</sub>, the archive table lists {b['rstar_rsun']:.2f}.") + take(f"R<sub>p</sub>/R<sub>&#9733;</sub> = {b['fit']['ror']:.4f} &plusmn; {b['fit']['ror_err']:.4f} (tutorial 0.0554); P = {b['fit']['period']:.5f} d (catalog {b['catalog']['period']:.5f})."),
            f"The catalog radius is {abs(b['delta_radius_pct']):.1f} percent above ours because the catalog radius implies a stellar radius of {b['rstar_implied_by_catalog']:.2f} solar radii, while the summary table lists {b['rstar_rsun']:.2f}. That is why we also compare the ratio."))

# =============================================================== 11-20 planets
TITLE = {}
for n in names:
    r = R[n]; f = r["fit"]; ror = f["ror"]
    TITLE[n] = {
        "HD 118203 b": f"Same planet as the tutorial: R<sub>p</sub>/R<sub>&#9733;</sub> within 0.2 %",
        "HD 189733 b": f"Brightest star, {f['n_transits']} transits: R<sub>p</sub>/R<sub>&#9733;</sub> good to {100*r['ror_err_stat']/ror:.1f} %",
        "HD 209458 b": f"First transiting planet: radius within {abs(r['delta_radius_pct']):.1f} %",
        "WASP-18 b": f"{f['period']*24:.1f} h orbit, {f['n_transits']} transits: R<sub>&#9733;</sub> limits the radius",
        "WASP-62 b": f"Southern CVZ target: {len(r['sectors_used'])} of {r['sectors_available']} sectors, radius within {abs(r['delta_radius_pct']):.1f} %",
        "LTT 9779 b": f"Hot-Neptune desert: b = {f['b']:.2f} inflates the error to {rp_err_pct(n):.0f} %",
        "TOI-270 c": f"Sub-Neptune of an M dwarf: {r['rp_rearth']:.2f} R<sub>&oplus;</sub> within {abs(r['delta_radius_pct']):.1f} %",
        "LTT 1445 A b": f"Nearest system, {f['n_transits']} transits: {r['rp_rearth']:.2f} &plusmn; {r['rp_rearth_err']:.2f} R<sub>&oplus;</sub>",
        "GJ 1132 b": f"Earth-size planet from a {ror**2*1e3:.1f} ppt dip: {r['rp_rearth']:.2f} &plusmn; {r['rp_rearth_err']:.2f} R<sub>&oplus;</sub>",
        "K2-141 b": f"A {ror**2*1e6:.0f} ppm dip every {f['period']*24:.1f} h: radius {abs(r['delta_radius_pct']):.0f} % low",
    }[n]


def comment(n):
    r, c = R[n], C[n]; f = r["fit"]; ror = f["ror"]
    return {
        "HD 118203 b": f"The catalog radius implies R<sub>&#9733;</sub> = {r['rstar_implied_by_catalog']:.2f} R<sub>&#9737;</sub>, not the table's {r['rstar_rsun']:.2f}: the {abs(r['delta_radius_pct']):.1f} % gap is the star, not the light curve.",
        "HD 189733 b": f"Tmag {c.sy_tmag:.1f}, {c.sy_dist:.0f} pc. One sector is enough; R<sub>&#9733;</sub> ({100*(r['rstar_err'] or 0)/r['rstar_rsun']:.1f} %) dominates the error.",
        "HD 209458 b": f"{f['n_transits']} transits in sector {r['sectors_used'][0]}; MCMC and detrending errors are below 0.4 %.",
        "WASP-18 b": f"R<sub>p</sub>/R<sub>&#9733;</sub> good to {100*r['ror_err_stat']/ror:.1f} %, yet R<sub>p</sub> is only good to {rp_err_pct(n):.1f} % because of R<sub>&#9733;</sub>.",
        "WASP-62 b": f"Ecliptic latitude {c.elat:.0f}&deg;: {r['sectors_available']} sectors exist, we use the first {len(r['sectors_used'])}.",
        "LTT 9779 b": "Grazing geometry makes R<sub>p</sub>/R<sub>&#9733;</sub> and b degenerate: the least certain radius of the ten.",
        "TOI-270 c": f"R<sub>&#9733;</sub> = {r['rstar_rsun']:.2f} R<sub>&#9737;</sub>; {f['n_transits']} transits; a three-planet system.",
        "LTT 1445 A b": f"{c.sy_dist:.1f} pc. Only {f['n_transits']} transits and R<sub>&#9733;</sub> = {r['rstar_rsun']:.2f} R<sub>&#9737;</sub> (7 % error).",
        "GJ 1132 b": f"R<sub>&#9733;</sub> = {r['rstar_rsun']:.2f} R<sub>&#9737;</sub>; {f['n_transits']} transits; the {abs(r['delta_radius_pct']):.1f} % gap is {abs((r['rp_rearth']-r['catalog']['rade'])/r['rp_rearth_err']):.1f}&sigma;.",
        "K2-141 b": f"BLS S/N only {r['bls']['snr']:.0f}: the edge of what one sector can do; found only with the guided search.",
    }[n]


for n in names:
    r, g = R[n], grp.loc[n]; f = r["fit"]
    mode = pill("blind search", "new") if r["mode"] == "blind" else pill("guided search", "bor")
    dP = pct(f["period"], r["catalog"]["period"])
    rows = [["Period (d)", f"{f['period']:.5f}", f"{r['catalog']['period']:.5f}", sgn(dP, 4 if abs(dP) < 0.1 else 2)],
            ["R<sub>p</sub>/R<sub>&#9733;</sub>", f"{f['ror']:.4f}", f"{r['catalog']['ror']:.4f}", sgn(r["delta_ror_pct"])],
            ["R<sub>p</sub> (R<sub>&oplus;</sub>)", f"{r['rp_rearth']:.2f} &plusmn; {r['rp_rearth_err']:.2f}", f"{r['catalog']['rade']:.2f}", sgn(r["delta_radius_pct"])]]
    right = (f'<div style="margin-bottom:8px">{pill(short(g.g_size))} {pill(short(g.g_period))} {pill(short(g.g_star))} {mode}</div>'
             + tbl(["", "Measured", "Catalog", "&Delta;"], rows, "tbl sm")
             + f'<p class="note" style="margin:8px 0 0;font-size:22px">{f["n_transits"]} transits, sectors {", ".join(map(str, r["sectors_used"]))}</p>'
             + f'<div class="take" style="font-size:25px">{comment(n)}</div>')
    S.append(sl(f"3  Results. {NUM[n]} {n}. {TITLE[n]}",
                '<div class="cols" style="grid-template-columns:630px 1fr;align-items:start">' + fig(f"{slug(n)}_fold", 630, "Folded TESS data, binned means and best-fit model.") + f"<div>{right}</div></div>",
                f"Group: {short(g.g_size)}, {short(g.g_period)}, {short(g.g_star)}, {C[n].sy_dist:.0f} pc, sky {short(g.g_sky)}. Measured {r['rp_rearth']:.2f} R earth against catalog {r['catalog']['rade']:.2f}; search mode {r['mode']}. About one minute."))

# =============================================================== 21-22 summary
S.append(sl("3  Results. Radii differ from the catalog by at most 7.3 %, periods by 0.03 %",
            cols(fig("res_radius", 570, "Radius difference to the catalog; bars: total 1&sigma; error."),
                 fig("res_period", 570, "|&Delta;P|/P (log scale); dashed line: 0.01 %.")),
            "Left: every radius is consistent with zero within 1.4 sigma. The big error bars are LTT 9779 b and LTT 1445 A b. Right: periods; the worst is K2-141 b at 0.03 percent."))

rows = []
for n in names:
    r = R[n]; f = r["fit"]; z = (r["rp_rearth"] - r["catalog"]["rade"]) / r["rp_rearth_err"]
    rows.append([f"<b>{NUM[n]}</b> {n}", (lambda v: "0" if round(v) == 0 else f"{v:+.0f}")(1e6*(f['period']-r['catalog']['period'])/r['catalog']['period']), f"{r['rp_rearth']:.2f} &plusmn; {r['rp_rearth_err']:.2f}", f"{r['catalog']['rade']:.2f}", sgn(r["delta_radius_pct"]), f"{z:+.1f}&sigma;"])
S.append(sl("3  Results. Summary of the ten measurements",
            tbl(["Planet", "&Delta;P (ppm)", "R<sub>p</sub> measured (R<sub>&oplus;</sub>)", "R<sub>p</sub> catalog", "&Delta;R<sub>p</sub>", "Pull"], rows, "tbl md"),
            "Pull is the difference divided by our total error. All pulls are between minus 1.4 and plus 0.8."))

# =============================================================== 23-24 discussion
rows = []
for n in names:
    r = R[n]; ror = r["fit"]["ror"]; rs = 100 * (r["rstar_err"] or 0) / r["rstar_rsun"]
    rows.append([f"<b>{NUM[n]}</b> {n}", f"{100*r['ror_err_stat']/ror:.1f}", f"{100*r['ror_err_sys']/ror:.1f}", f"{rs:.1f}", f"{rp_err_pct(n):.1f}"])
S.append(sl("4  Discussion. The stellar radius and the detrending set the error, not photon noise",
            tbl(["Planet", "R<sub>p</sub>/R<sub>&#9733;</sub> MCMC %", "R<sub>p</sub>/R<sub>&#9733;</sub> detrend %", "R<sub>&#9733;</sub> %", "Total R<sub>p</sub> %"], rows, "tbl md"),
            "Systematic error is half the range of Rp over R star across three detrending variants. For bright stars the MCMC error is below half a percent; the stellar radius is 1 to 7 percent. LTT 9779 b and K2-141 b are limited by the dip itself."))

a, d_ = R["AU Mic b"], R["DS Tuc A b"]
S.append(sl("4  Discussion. Where the method fails: three lessons",
            cols(card("Blind search can lock on noise", "K2-141 b: blind BLS gave 5.70 d instead of 0.280 d. The browser demo returns 2&times;P for LTT 1445 A b. Narrow the range (5 to 6 d, or 0.26 to 0.5 d) and both are fixed.", "orange", 350),
                 card("Active stars break detrending", f"AU Mic b (spots, flares): R<sub>p</sub>/R<sub>&#9733;</sub> = {a['fit']['ror']:.2f} &plusmn; {a['fit']['ror_err']:.2f} against 0.050. DS Tuc A b: systematic error &plusmn;{d_['ror_err_sys']:.2f}.", "navy", 350),
                 card("Few transits cap the accuracy", f"AU Mic b has {a['fit']['n_transits']} transits in one sector, with timing variations; LTT 1445 A b only {R['LTT 1445 A b']['fit']['n_transits']}. More sectors would help.", "navy", 350))
            + note("AU Mic b and DS Tuc A b are reported as failures and are not among the ten."),
            "Be honest here. Guided mode is not cheating: it restricts the search window, the period and radius are still measured from the data, and every planet slide says which mode was used. Next step for active stars: Gaussian-process detrending, as in the stellar-variability tutorial."))

# =============================================================== 25 demo
S.append(sl("4  Discussion. Live demo: repeat the measurement in your browser",
            '<div class="cols" style="grid-template-columns:660px 1fr">' + fig("demo_shot", 660, "demo/index.html runs entirely in the browser (JavaScript).") +
                 '<div>' + card("Steps", "1 Pick a planet. 2 BLS searches the periods. 3 Fit the transit. 4 Compare with the NASA archive and with our MCMC.", "orange")
                 + card("Try", "K2-141 b: set the BLS range to 0.26 to 0.5 d. LTT 1445 A b: 5 to 6 d.") + note("Files: demo/index.html and notebooks/01_measure_one_planet.ipynb in this folder.") + '</div></div>',
            "Open demo/index.html. HD 189733 b: BLS in a few seconds gives 2.21858 d. Then K2-141 b with the default range to show the failure, narrow the range to see 0.28035 d. The demo uses fixed limb darkening, so radii are a few percent less accurate than the pipeline."))

# =============================================================== 26 conclusions
S.append(sl("5  Conclusions and perspectives",
            cols(card("What we showed", "Periods of ten planets (0.28 to 6.1 d) within 0.03 % and radii (1.1 to 15.7 R<sub>&oplus;</sub>) within 4 % for eight of ten, from public data and one pipeline.", "orange", 350),
                 card("What limits it", "Stellar radius (up to 7 %), detrending (about 1 %), the number of transits, and blind search at short periods or low S/N.", "navy", 350),
                 card("Next", "Fit stellar density and eccentricity, search for TTVs, stack more sectors, Gaussian-process detrending for active stars.", "navy", 350))
            + take("A radius from a light curve is a ratio times a stellar radius; the ratio is the part TESS measures best."),
            "Close with the take-away. Thank the audience and open the floor. The appendix has terms, data, the course-formula check, formulas, stress tests and references."))

# =============================================================== APPENDIX
A = []
_ap = [0]


def ap(title, body, notes):
    _ap[0] += 1
    return sl(f"A{_ap[0]}  Appendix. {title}", body, notes)


A.append(ap("Terms used in this talk", tbl(["Term", "Meaning"], [
    ["TESS, sector", "NASA survey satellite; it stares at one 24 by 96 degree field for about 27 days (a sector)"],
    ["SPOC, PDCSAP", "Science pipeline of TESS; flux after systematics removal (2-minute cadence)"],
    ["TIC, Tmag", "TESS Input Catalog identifier and TESS-band magnitude of the star"],
    ["BLS", "Box Least Squares: searches for periodic box-shaped dips"],
    ["R<sub>p</sub>/R<sub>&#9733;</sub>, b", "Planet to star radius ratio; impact parameter (0 = central transit)"],
    ["Limb darkening", "The stellar disc is darker at the edge; it rounds the transit bottom (Kipping q<sub>1</sub>, q<sub>2</sub>)"],
    ["USP, CVZ", "Ultra-short period (P &lt; 1 d); TESS continuous viewing zone (|ecliptic latitude| &gt; 78&deg;)"],
    ["Pull", "(measured &minus; catalog) divided by our total 1&sigma; error"]], "tbl md"), "Glossary for questions."))

A.append(ap("Data and what each source is used for", tbl(["Source", "Access", "Use"], [
    ["TESS SPOC 2-min light curves", "MAST, lightkurve (PDCSAP flux)", "The measurements: 1 to 4 consecutive sectors per planet"],
    ["NASA Exoplanet Archive, pscomppars", "TAP query, transiting planets", "4,826 planets: periods, radii, R<sub>&#9733;</sub>, T<sub>eff</sub>, distance, coordinates"],
    ["TIC identifiers, Tmag", "pscomppars columns", "Cross-match to MAST; brightness cut"],
    ["Course notes (M1 Exoplanets)", "Lecture review, transit method", "Formulas for depth, probability and duration (A6)"],
    ["Tutorial: Quick fits for TESS light curves", "exoplanet-case-studies", "Recipe and benchmark values for HD 118203 b"]], "tbl"),
    "All data are public. The catalog values are used only as an answer key, except R star which the radius needs."))

A.append(ap("Sky map of the ten planets", fig("ov_sky_map", 1160, "Ecliptic coordinates (Mollweide). Pink bands: continuous viewing zones; the grey patch is the Kepler field."),
            "Planet 5 (WASP-62 b) sits in the southern CVZ; planet 1 in the northern high-latitude region; the rest at low latitudes."))
A.append(ap("Distance and host star", fig("ov_distance_star", 1160, "Host effective temperature against distance; dashed lines: spectral-type and distance classes."),
            "From the 6.9 pc M dwarf of LTT 1445 A to the 176 pc F star WASP-62."))
A.append(ap("Light curve and detrending, HD 118203 b", fig("m_lc", 1160, "Sectors 15 and 16: PDCSAP flux (top), flattened curve (offset), predicted transits in red.")
            + take("Savitzky-Golay window 1.5 d, outliers clipped at +5&sigma;; re-run with the transits masked so the filter cannot absorb the depth."),
            "Three detrending variants (mask 2 to 3 durations, window 4 to 8 durations, minimum window 0.75 to 1.5 d) give the systematic error. The widest variant is the primary result because narrow windows eat depth."))

# --- course check
cc = []
for n in names:
    r = R[n]; c = C[n]; a_rs = r["fit"]["a_rs"]; P = r["fit"]["period"]
    cc.append([f"<b>{NUM[n]}</b> {n}", f"{a_rs:.1f}", f"{100/a_rs:.1f} %", f"{P/np.pi/a_rs*24:.2f}", f"{c.pl_trandur:.2f}"])
A.append(ap("Course formulas checked on the fitted orbits", tbl(["Planet", "a/R<sub>&#9733;</sub> (fit)", "R<sub>&#9733;</sub>/a", "T = (P/&pi;)(R<sub>&#9733;</sub>/a) (h)", "T catalog (h)"], cc, "tbl md"),
            "The fitted a over R star gives the geometric transit probability and a central-transit duration from the course formula. Nine planets agree within 10 %. LTT 9779 b does not: its fit has b = 0.91, so a/R star is degenerate with b and the central-transit formula over-predicts the duration by a factor of about four."))

A.append(ap("Formulas: transit model and period search", fm("F(t) = 1 &minus; &Delta;F( z(t), R<sub>p</sub>/R<sub>&#9733;</sub>, u<sub>1</sub>, u<sub>2</sub> ) ;&nbsp; z = (a/R<sub>&#9733;</sub>) &radic;[ sin<sup>2</sup>&phi; + cos<sup>2</sup>i cos<sup>2</sup>&phi; ] ,&nbsp; &phi; = 2&pi;(t &minus; t<sub>0</sub>)/P",
                                                       "Mandel-Agol quadratic limb darkening (batman); b = (a/R<sub>&#9733;</sub>) cos i; circular orbit.")
            + fm("u<sub>1</sub> = 2&radic;q<sub>1</sub> q<sub>2</sub> ,&nbsp; u<sub>2</sub> = &radic;q<sub>1</sub> (1 &minus; 2q<sub>2</sub>)", "Kipping parametrisation, q<sub>1</sub>, q<sub>2</sub> uniform in (0, 1).")
            + fm("BLS: SNR(P, T, t<sub>0</sub>) = &delta; &radic;N<sub>in</sub> / &sigma;", "Trial periods 0.26 to 15 d; durations 0.02 to 0.25 d; boxes longer than 20 % of P are rejected.")
            + fm("ln L = &minus;&frac12; &Sigma; ( f<sub>i</sub> &minus; F(t<sub>i</sub>) )<sup>2</sup> / &sigma;<sup>2</sup>", "&sigma; from the out-of-transit MAD; emcee, 32 walkers, 1,500 burn-in, 2,500 steps.") + take("Same physical model as the tutorial (Mandel-Agol, limb darkening); only the sampler differs."),
            "Reference slide for questions on the model."))

A.append(ap("Formulas: radius and the error budget", fm("R<sub>p</sub> = ( R<sub>p</sub>/R<sub>&#9733;</sub> ) &times; R<sub>&#9733;</sub> &times; 109.076 R<sub>&oplus;</sub>/R<sub>&#9737;</sub>")
            + fm("&sigma;<sub>ratio</sub><sup>2</sup> = &sigma;<sub>MCMC</sub><sup>2</sup> + &sigma;<sub>sys</sub><sup>2</sup> ,&nbsp; &sigma;<sub>sys</sub> = &frac12; ( max &minus; min ) of R<sub>p</sub>/R<sub>&#9733;</sub> over 3 detrendings")
            + fm("&sigma;<sub>Rp</sub> / R<sub>p</sub> = &radic;[ ( &sigma;<sub>ratio</sub> / ratio )<sup>2</sup> + ( &sigma;<sub>R&#9733;</sub> / R<sub>&#9733;</sub> )<sup>2</sup> ]")
            + fm("pull = ( R<sub>p,meas</sub> &minus; R<sub>p,cat</sub> ) / &sigma;<sub>Rp</sub>&nbsp;;&nbsp; &Delta;P/P = ( P<sub>meas</sub> &minus; P<sub>cat</sub> ) / P<sub>cat</sub>", "Course example: depth 0.64 %, R<sub>&#9733;</sub> = 0.8 R<sub>&#9737;</sub> gives R<sub>p</sub>/R<sub>&#9733;</sub> = 0.08 and R<sub>p</sub> = 0.064 R<sub>&#9737;</sub>.") + take("A 7 % error on R<sub>&#9733;</sub> is a 7 % error on R<sub>p</sub>, whatever the light curve quality.") + note("Ratio errors come from the posterior (16th to 84th percentile) and from three detrending variants; R<sub>&#9733;</sub> error from the archive."),
            "Errors in quadrature; the stellar radius uncertainty is taken from the archive."))

rows = [["K2-141 b, blind", "BLS 0.26 to 15 d", "P = 5.70 d (truth 0.280 d); R<sub>p</sub> = 21 R<sub>&oplus;</sub>", "Fixed by guided search"],
        ["LTT 1445 A b, demo", "Browser BLS 0.26 to 15 d", "P = 10.55 d = 2&times;P", "Range 5 to 6 d gives 5.35878 d"],
        ["AU Mic b, guided", "&plusmn;3 % of 8.46 d", f"P = {a['fit']['period']:.2f} d, R<sub>p</sub>/R<sub>&#9733;</sub> = {a['fit']['ror']:.2f} &plusmn; {a['fit']['ror_err']:.2f}", "Spots and flares; 3 transits; excluded"],
        ["DS Tuc A b, guided", "&plusmn;3 % of 8.14 d", f"R<sub>p</sub>/R<sub>&#9733;</sub> = {d_['fit']['ror']:.3f} &plusmn; {d_['fit']['ror_err']:.3f}", "Detrending systematic too large; excluded"]]
A.append(ap("Stress tests and failures", tbl(["Case", "Setting", "Outcome", "Verdict"], rows, "tbl") + note("First-pass JSON of the blind failures is kept in archive/results_blind_failed/."),
            "These are the numbers behind the failure slide."))

rows = [[f"<b>{NUM[n]}</b> {n}", R[n]["mode"], ("0.26 to 15 d, 7 durations" if R[n]["mode"] == "blind" else "&plusmn;3 % of catalog P, durations 0.6 to 1.5 &times; catalog T")] for n in names]
A.append(ap("Search mode used for each planet", tbl(["Planet", "Mode", "BLS window"], rows, "tbl md"),
            "Blind for seven planets, guided for LTT 9779 b, LTT 1445 A b and K2-141 b. In guided mode the period, epoch, depth and radius are still measured from the data."))

refs = ["Ricker et al. 2015, TESS mission, JATIS 1, 014003", "Jenkins et al. 2016, SPOC pipeline, SPIE 9913", "Lightkurve Collaboration 2018, Lightkurve, ascl:1812.013",
        "Kovacs, Zucker and Mazeh 2002, BLS, A&amp;A 391, 369", "Mandel and Agol 2002, transit light curves, ApJ 580, L171", "Kreidberg 2015, batman, PASP 127, 1161",
        "Foreman-Mackey et al. 2013, emcee, PASP 125, 306", "Kipping 2013, limb-darkening priors, MNRAS 435, 2152", "Akeson et al. 2013, NASA Exoplanet Archive, PASP 125, 989",
        "exoplanet-case-studies: Quick fits for TESS light curves and Fitting TESS data"]
A.append(ap("References", '<ul style="margin:0;padding-left:30px">' + "".join(f"<li>{x}</li>" for x in refs) + "</ul>", "Sources."))

SL = S + A
# ---------------------------------------------------------------- CSS = CSS của deck Gia-Lam (cùng họ template USTH) + phần bổ sung
css = (ROOT / "slides" / "deck" / "group2_base.css").read_text(encoding="utf-8")
js = (ROOT / "slides" / "deck" / "group2_engine.js").read_text(encoding="utf-8")
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Measuring exoplanet radii and periods with TESS, Group 2</title><style>' + css + '</style></head><body>'
        '<div class="mdeck"><div class="mdeck-canvas-wrap"><div class="mdeck-viewport">' + "".join(SL) + '</div></div>'
        '<div class="mdeck-bar"><button class="mdeck-prev">&#9664;</button><div class="mdeck-dots"></div><span class="mdeck-count"></span>'
        '<button class="mdeck-next">&#9654;</button><button class="mdeck-fs">Full screen</button></div><div class="mdeck-notes"></div></div>'
        '<script>' + js + '</script></body></html>')
(OUT / "index.html").write_text(page, encoding="utf-8")
print("slides:", len(SL), "main:", len(S))
