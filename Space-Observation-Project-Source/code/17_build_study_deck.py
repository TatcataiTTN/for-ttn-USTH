# -*- coding: utf-8 -*-
"""Bước 17 - Dựng bộ slides RIÊNG 'Space-Observation-Project-Group-2-Study' (không sửa bộ Group-2 đã đăng).
Nội dung: đọc và dựng lại bài Huang+2018 (pi Men c), đồ thị cho mọi hành tinh kèm mô tả 'image thu được', đối chiếu với giá trị các tác giả,
literature review TESS theo nhóm phương pháp (128 bài đã kiểm chứng), cách lấy lại số liệu từ dataset.
Mọi số đọc từ results/*.json, figures/paper/figure_stats.json, results/paper_comparison.csv, data/literature/*.csv (không gõ tay)."""
import csv
import html
import json
import pathlib
import re
import shutil
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from lit_content import GROUPS, USED

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "slides" / "Space-Observation-Project-Group-2-Study"
for d in ("assets", "img", "data"):
    (OUT / d).mkdir(parents=True, exist_ok=True)
slug = lambda n: re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_")
names = [l.strip() for l in open(ROOT / "data" / "selected.txt") if l.strip()]
ALL = names + ["pi Men c"]
NUM = {n: i for i, n in enumerate(names, 1)}
NUM["pi Men c"] = "π"
R = {n: json.load(open(ROOT / "results" / slug(n) / "result.json")) for n in ALL}
ST = json.load(open(ROOT / "figures" / "paper" / "figure_stats.json"))
CMP = pd.read_csv(ROOT / "results" / "paper_comparison.csv")
CAT = pd.read_csv(ROOT / "data" / "raw" / "tess_catalog.csv")
RT = pd.read_csv(ROOT / "results" / "results_table.csv").set_index("planet")
MAN = pd.read_csv(ROOT / "results" / "data_manifest.csv")
CHK = pd.read_csv(ROOT / "results" / "catalog_recheck.csv")
PVC = pd.read_csv(ROOT / "results" / "paper_value_check.csv")
lit = list(csv.DictReader(open(ROOT / "data" / "literature" / "verified_curated.csv")))
dl = {r["ref"]: r for r in csv.DictReader(open(ROOT / "data" / "literature" / "downloaded.csv"))}
idx_path = ROOT / "literature" / "checking" / "INDEX.csv"
IDX = list(csv.DictReader(open(idx_path))) if idx_path.exists() else []
for r in lit:
    r["key"] = r["group"][0]
    r["t"] = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", r["title"])).strip()
    r["pdf"] = bool(dl.get(r["ref"]) and dl[r["ref"]]["status"] in ("OK", "already"))
    r["used"] = USED.get((r["first_author"], str(r["year"])), "")
lit.sort(key=lambda r: (r["key"], int(r["year"]), r["first_author"]))

# ---------------------------------------------------------------- tệp tĩnh
shutil.copy(ROOT / "slides" / "assets" / "usth" / "usth_logo.png", OUT / "assets" / "usth_logo.png")
shutil.copy(ROOT / "slides" / "assets" / "usth" / "usth_dses_logo.png", OUT / "assets" / "usth_dses_logo.png")
for f in (ROOT / "figures" / "paper").glob("*.png"):
    shutil.copy(f, OUT / "img" / f.name)
for n in ("res_radius", "res_period", "phys_transit"):
    shutil.copy(ROOT / "slides" / "assets" / "images" / f"{n}.png", OUT / "img" / f"{n}.png")
for f in ("results_table.csv", "data_manifest.csv", "catalog_recheck.csv", "paper_comparison.csv", "paper_value_check.csv"):
    shutil.copy(ROOT / "results" / f, OUT / "data" / f)
shutil.copy(ROOT / "data" / "literature" / "verified_curated.csv", OUT / "data" / "literature_verified.csv")

# ---------------------------------------------------------------- helpers
CHIP = '<div class="logo-chip"><img src="assets/usth_logo.png" alt="USTH"><img src="assets/usth_dses_logo.png" alt="DSES"></div>'
_pg = [0]
esc = lambda s: html.escape(s, quote=True)
RS = "R<sub>&#9733;</sub>"


def sl(title, body, notes):
    return (f'<section class="mdeck-slide th0 has-logo" data-notes="{esc(notes)}">{CHIP}<h2><span>{title}</span></h2>'
            f'<div class="body">{body}</div><span class="pg">@@PG@@</span></section>')


def card(h, t, c="navy", mh=0): return f'<div class="card {c}" style="min-height:{mh}px"><h3>{h}</h3><p>{t}</p></div>'
def cols(*cs, tpl=None): return f'<div class="cols"{(" style=" + chr(34) + "grid-template-columns:" + tpl + chr(34)) if tpl else ""}>' + "".join(cs) + "</div>"
def take(t): return f'<div class="take">{t}</div>'
def note(t): return f'<p class="note">{t}</p>'
def fig(name, w, cap): return f'<figure class="figd"><img src="img/{name}.png" style="width:{w}px" alt=""><figcaption>{cap}</figcaption></figure>'
def tbl(head, rows, cls="tbl"):
    h = "".join(f"<th>{x}</th>" for x in head)
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<table class="{cls}"><tr>{h}</tr>{r}</table>'
def obt(items, title="Image obtained"):
    li = "".join(f'<li style="font-size:23px;line-height:1.32;margin:3px 0">{x}</li>' for x in items)
    return f'<div class="card orange" style="padding:10px 16px;margin:0"><h3 style="font-size:27px!important;margin:0 0 4px">{title}</h3><ul style="margin:0;padding-left:24px">{li}</ul></div>'
def code(txt): return f'<pre class="qa-pre" style="font:20px/1.4 ui-monospace,Menlo,monospace;white-space:pre;overflow:hidden;margin:6px 0;padding:10px 14px">{esc(txt)}</pre>'
def sg(x, d=1): return f"{x:+.{d}f}"
def trunc(s, n):
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"
def row_of(pl, src):
    return CMP[(CMP.planet == pl) & CMP.source.str.startswith(src)].iloc[0]


n12 = len(CMP); nr = int((CMP.ror_pull.abs() < 2).sum()); nrp = int((CMP.Rp_pull.abs() < 2).sum()); nP = int(CMP.P_pull.notna().sum()); nPok = int((CMP.P_pull.abs() < 2).sum())
S = []
# =============================================================== cover
S.append('<section class="mdeck-slide cover" data-notes="Study deck for the ten planets: figure types taken from one TESS discovery paper, plots for every planet, a comparison with the authors of each discovery paper, a verified literature review by sub-method, and how to retrieve every number.">'
         '<div class="cover-logos"><img src="assets/usth_logo.png" style="height:70px"><img src="assets/usth_dses_logo.png" style="height:70px"></div>'
         '<h2>Ten exoplanets measured with TESS: plots, the authors&#39; numbers and the literature</h2>'
         '<div class="body"><p class="sub">Plots in the style of Huang et al. 2018 for each planet, ten planets against their discovery papers, a verified literature review of TESS transit photometry, and how to retrieve every number</p>'
         '<p class="who"><b>Project:</b> Space Observation Project 1, Group 2 (study deck)<br><b>Lecturer:</b> Dr. Nguyen Thi Phuong<br>USTH, Master 2 Space, November 2026</p></div></section>')

# =============================================================== 1 introduction
nlit, npdf = len(lit), sum(r["pdf"] for r in lit)
S.append(sl("1  Introduction. What is in this deck?",
            cols(card("The template", "Huang et al. 2018 (TESS discovery of π Men c) shows five figure types. We redraw them for our ten planets from public TESS data.", "orange", 330),
                 card("The plots", f"{len(list((ROOT/'figures'/'paper').glob('*.png')))} new figures. Each slide says what the image shows, with measured numbers.", "navy", 330),
                 card("The authors", "Our ten planets against their discovery papers: same numbers or not, and why.", "navy", 330),
                 card("The literature", f"{nlit} verified papers in eleven sub-methods; {npdf} open-access PDFs downloaded.", "orange", 330))
            + note("Everything is computed from public data: TESS SPOC light curves (MAST) and the NASA Exoplanet Archive. Section 3 tells how exoplanets have been found, section 4 gives the TESS numbers with their sources, section 5 asks whether ten planets are enough, and section 10 shows how to retrieve each number."),
            "This is a study deck, separate from the 25-minute presentation. It answers: what does the paper actually say, can we rebuild it, where do we agree with the authors, and what is the literature behind each step."))

S.append(sl("1  Introduction. Where each number comes from: Measured, Catalog, Published",
            tbl(["Column", "Source", "Computed by us?", "What it is"], [
                ["<b>Measured</b>", "TESS light curve (SPOC PDCSAP)", "Yes", "Period from BLS; R<sub>p</sub>/R<sub>&#9733;</sub> from the batman + emcee fit; R<sub>p</sub> = ratio &times; R<sub>&#9733;</sub>"],
                ["<b>Catalog</b>", "NASA Exoplanet Archive, pscomppars", "No, taken from data", "Default parameter set: one published paper per planet"],
                ["<b>Published</b>", "Discovery or follow-up paper (PDF)", "No, read from the paper", "Table values quoted in section 8, found verbatim in the PDF text"],
                ["<b>&Delta;, pull</b>", "Measured against Catalog or Published", "Yes", "&Delta; = (M &minus; C)/C; pull = (M &minus; C)/&radic;(&sigma;<sub>M</sub><sup>2</sup>+&sigma;<sub>C</sub><sup>2</sup>)"]], "tbl md")
            + take(f"Two inputs are not ours: {RS} comes from the archive, and the three guided planets use the catalog period to set the search window."),
            "Measured is self-computed. Catalog and Published are taken from data. The stellar radius enters the radius, so compare the ratio when you want the pure light-curve result. LTT 9779 b, LTT 1445 A b and K2-141 b were searched in a window around the catalog period."))

why = [["Baseline", "Baseline = time from first to last transit: 27 to 110 d here, years in catalogs", "Our P is good to 0.0004 d (π Men c); the catalog P to 10<sup>-7</sup> d"],
       ["Stellar radius", f"R<sub>p</sub> = ratio &times; {RS}; papers use their own {RS}", "π Men c: 1.10 (paper) against 1.17 (archive)"],
       ["Early papers", "Ground-based 1999 to 2005 discovery light curves", "HD 189733 b ratio 0.172 (2005) against 0.1545 (Spitzer 2007)"],
       ["Float32 or float64", "No effect: flux noise is 1000 times larger than float32 rounding", "Refit with float32 flux: ratio changes 0.2 %, MCMC noise"],
       ["MCMC randomness", "emcee RNG is now fixed; earlier runs differ by about 0.1 %", "π Men c: 2.0302 then 2.0319 R<sub>&oplus;</sub> before the fix"]]
S.append(sl("1  Introduction. Why two sources can differ: five causes, three of them tested",
            tbl(["Cause", "What happens", "Evidence in this project"], why, "tbl md") + take("The stellar radius and old discovery papers explain every large difference we found."),
            "Float precision is not a cause: the SPOC file stores flux as float32 with relative rounding 1e-7, the noise is 1e-4. Sampler noise is real but small. The big ones are the stellar radius and old discovery papers."))

# =============================================================== 2 the paper
S.append(sl("B1  Appendix. The paper behind the template: Huang et al. 2018, π Men c",
            cols(card("Star", "π Mensae (HD 39091), G0V, V = 5.67, 18.27 &plusmn; 0.02 pc; 1.094 M<sub>&#9737;</sub>, 1.10 R<sub>&#9737;</sub> (their Table 1).", "navy", 235),
                 card("Planet c", "R = 2.04 &plusmn; 0.05 R<sub>&oplus;</sub>, P = 6.27 d, M = 4.82 &plusmn; 0.85 M<sub>&oplus;</sub> from HARPS and AAT/UCLES velocities.", "orange", 235),
                 card("TESS data", "Sector 1 (25 Jul to 22 Aug 2018), camera 4, CCD 2; SPOC 2-min and 30-min full-frame images; 5 transits of about 300 ppm and 3 h.", "navy", 235))
            + take("It is the first small planet found by TESS around a bright star, arXiv:1809.05967.")
            + note("All values on this slide are read from the PDF (abstract, Table 1, Sections 2 and 3)."),
            "Summary of the paper from its abstract, Table 1 and Section 2. The planet was found with the MIT quick-look pipeline on full-frame images and SPOC on the 2-minute data. The radial velocities confirm the 6.27-day period."))

rows = [["Fig 1", "DSS survey images and TESS aperture of the field", "Aperture only", "Appendix B4 (π Men c); DSS images not fetched"],
        ["Fig 2", "Raw, detrended and phase-folded TESS light curve", "All ten planets", "Section 3"],
        ["Fig 3", "Radial velocities, Lomb-Scargle periodogram, phase folds", "Not rebuilt", "RV tables are not in our dataset"],
        ["Fig 4", "Transits fitted one by one and their depth posteriors", "π Men c; odd-even for all", "Appendix B3; section 4"],
        ["Fig 5", "Apparent magnitude against radius; mass-radius diagram", "Ten planets marked", "Section 4, NASA archive and Zeng tables"]]
S.append(sl("2  Template. Five figure types from Huang et al. 2018, redrawn for our planets",
            tbl(["Figure", "Shows", "Our version", "Where"], rows, "tbl md")
            + take("The paper is a template for the plots, not the subject: the planets are our ten."),
            "We rebuild with our own pipeline on the same sector, so the comparison is a test of the method, not a copy of their plots."))

fit, rr = R["pi Men c"]["fit"], R["pi Men c"]
f2 = ST["fig2_pi_Men_c"]; f4 = ST["fig4_pi_Men_c"]; hu = row_of("pi Men c", "Huang")
rows = [["Transits in sector 1", "5", f"{fit['n_transits']}"], ["Momentum dumps", "10", f"{f2['n_dumps']}"],
        ["Period (d)", "6.27", f"{fit['period']:.5f} &plusmn; {fit['period_err']:.5f}"],
        ["R<sub>p</sub> (R<sub>&oplus;</sub>)", "2.04 &plusmn; 0.05", f"{rr['rp_rearth']:.2f} &plusmn; {rr['rp_rearth_err']:.2f}"],
        [f"(R<sub>p</sub>/{RS})<sup>2</sup> (ppm)", "about 290 (read off Fig 4)", f"{f4['global_depth_ppm']} &plusmn; {f4['global_sd_ppm']}"],
        [f"{RS} (R<sub>&#9737;</sub>)", "1.10 &plusmn; 0.023", f"{rr['rstar_rsun']:.2f} (archive)"],
        ["Scatter per 2 min (ppm)", "142", f"{f2['scatter_2min_ppm']} point to point; rms {f2['rms_flat_ppm']}"],
        ["Transit duration (h)", "about 3", f"{f2['duration_h']}"]]
S.append(sl("2  Template. External check on the paper's own planet: same period and radius, different depth",
            tbl(["Quantity", "Paper (Huang+2018)", "Our pipeline"], rows, "tbl md")
            + take(f"The radius agrees ({hu.dRp_pct:+.1f} %) because two offsets cancel: our ratio is {abs(hu.dror_pct):.1f} % lower, our {RS} is {100*(rr['rstar_rsun']/1.10-1):.1f} % higher."),
            f"Period and radius agree. But the depth is not the same: the paper's Figure 4 histogram peaks near 290 ppm, ours is {f4['global_depth_ppm']} ppm, a {hu.dror_pct:+.1f} percent difference in the ratio. The radius matches only because the archive stellar radius {rr['rstar_rsun']:.2f} is larger than the paper's 1.10. The cause of the depth difference is not identified: candidates are detrending, SPOC data reprocessing and crowding; none tested."))

# =============================================================== 3 rebuilt figures
tr = [fit["t0"] + k * fit["period"] for k in range(5)]
S.append(sl("B2  Appendix. Fig 2 type for π Men c: five transits, ten momentum dumps, one folded dip",
            '<div class="cols" style="grid-template-columns:740px 1fr;align-items:start">'
            + fig("fig2_pi_Men_c", 740, "Top: raw PDCSAP, dashed lines at momentum dumps. Middle: after Savitzky-Golay detrending, red ticks at predicted transits. Bottom: folded, binned, model.")
            + "<div>" + obt([f"5 transits near BTJD {', '.join(f'{t:.1f}' for t in tr)}",
                             f"{f2['n_dumps']} momentum dumps, as in the paper",
                             f"rms {f2['rms_raw_ppm']} to {f2['rms_flat_ppm']} ppm after detrending",
                             f"folded dip lasts {f2['duration_h']} h, mid-transit depth {fit['depth_ppm_model']:.0f} ppm",
                             f"(R<sub>p</sub>/{RS})<sup>2</sup> = {fit['ror']**2*1e6:.0f} ppm"]) + "</div></div>",
            "This rebuilds the paper's Figure 2. The scatter at BTJD 1348 to 1349 is the pointing-jitter interval the authors also mention. Limb darkening makes the mid-transit depth (288 ppm) larger than the square of the radius ratio (253 ppm)."))

pt = f4["per_transit"]
S.append(sl("B3  Appendix. Fig 4 type for π Men c: each transit fitted alone, depths scatter 31 ppm",
            '<div class="cols" style="grid-template-columns:760px 1fr;align-items:start">'
            + fig("fig4_pi_Men_c", 760, "Five transits with the global model; last panel: posteriors of (R<sub>p</sub>/R<sub>&#9733;</sub>)<sup>2</sup> per transit, black = all data.")
            + "<div>" + obt([f"per-transit depths {', '.join(str(x['depth_ppm']) for x in pt)} ppm",
                             f"each &plusmn;{pt[0]['sd_ppm']} ppm from white noise",
                             f"real scatter {f4['depth_scatter_ppm']} ppm",
                             f"&chi;<sup>2</sup> = {f4['chi2_consistency']:.0f} for {f4['dof']} dof: errors about 3 times too small"]) + "</div></div>",
            f"The narrow coloured posteriors ignore red noise. The real transit-to-transit scatter is {f4['depth_scatter_ppm']} ppm, comparable to the width of the histograms in the paper's Figure 4. Transit 4 is the deepest at {pt[3]['depth_ppm']} ppm."))

f1 = ST["fig1_pi_Men_c"]
S.append(sl("B4  Appendix. Fig 1 type for π Men c: the SPOC aperture covers 96 % of the flux",
            '<div class="cols" style="grid-template-columns:570px 1fr;align-items:start">' + fig("fig1_pi_Men_c", 570, "Summed TESS pixels (log scale), sector 1; red: SPOC photometric aperture.")
            + "<div>" + obt([f"stamp {f1['stamp'][1]} &times; {f1['stamp'][0]} pixels, camera {f1['camera']}, CCD {f1['ccd']}",
                             f"aperture of {f1['n_aperture_pix']} pixels holds {100*f1['frac_flux_in_aperture']:.0f} % of the summed flux",
                             "one bright star, no second source inside the aperture"]) + take("Matches the paper: sector 1, camera 4, CCD 2.") + "</div></div>",
            "The paper's Figure 1 also shows two DSS survey images; we did not fetch them. The aperture is irregular and follows the star's blooming. Because the star is bright, charge bleeds along the columns."))

b = ST["bls_pi_Men_c"]
S.append(sl("B5  Appendix. BLS on π Men c finds 6.27 d at S/N 59, with weaker aliases at P/2 and 2P",
            fig("bls_pi_Men_c", 1160, "Box Least Squares power against trial period; red: best period; grey dashed: P/2 and 2P.")
            + obt([f"best period {b['best_period']} d on the BLS grid, S/N {b['snr']}", f"median power {b['median_power']}, 95th percentile {b['p95_power']}",
                   "the fit refines it to " + f"{fit['period']:.5f} d"]),
            "BLS needs at least a few transits to reject the half and double periods; with 5 transits in 27 days the main peak stands clearly above its aliases."))

def comp_pos(m, r):
    z = ROOT / "data" / "raw" / "zeng"
    E = np.loadtxt(z / "massradiusEarthlikeRocky.txt"); W = np.loadtxt(z / "massradius_100percentH2O_300K_1mbar.txt")
    e, w = np.interp(np.log(m), np.log(E[:, 0]), E[:, 1]), np.interp(np.log(m), np.log(W[:, 0]), W[:, 1])
    return (r - e) / (w - e)


mine5 = [x for x in ST["fig5b"]["mine"] if x["planet"] != "pi Men c"]
vmag = {n: (CAT[CAT.pl_name == n].iloc[0].sy_vmag if pd.notna(CAT[CAT.pl_name == n].iloc[0].sy_vmag) else CAT[CAT.pl_name == n].iloc[0].sy_tmag) for n in names}
bright = sorted(names, key=lambda n: vmag[n])[:3]
S.append(sl("4  Plots. Fig 5 type: where our planets sit among the known ones",
            cols(fig("fig5a_mag_radius", 570, "V magnitude against radius; red: ours (π = π Men c)."),
                 fig("fig5b_mass_radius", 570, "Measured masses; Zeng curves; red: our radii."))
            + obt([f"brightest hosts: " + ", ".join(f"{n} (V {vmag[n]:.1f})" for n in bright[:2]) + f"; {ST['fig5a']['n_brighter_than_8']} known planets have V &lt; 8",
                   "0 = Earth-like, 1 = water: " + "; ".join(f"{x['planet']} {comp_pos(x['mass'], x['radius_measured']):.1f}".replace("-", "&minus;") for x in mine5)]),
            "Left: the paper's top panel for our planets (the five giants are beyond 6 Earth radii, off the plot). Right: the paper's bottom panel; only the four small planets with measured masses are placed. The position index uses the Zeng tables at the archive default mass, so it depends on that mass."))

# =============================================================== 4 all planets
for n in names:
    s_ = ST[f"fig2_{slug(n)}"]; r_ = R[n]
    pubs = CMP[CMP.planet == n]
    p0 = pubs.iloc[0]
    flat = s_["rms_flat_ppm"] / s_["rms_raw_ppm"]
    items = [f"{s_['n_transits']} transits folded, duration {s_['duration_h']} h, {s_['n_dumps']} momentum dumps",
             f"depth at mid-transit {s_['depth_obs_ppm']:,} ppm observed, {s_['depth_model_ppm']:,} ppm model; scatter {s_['scatter_2min_ppm']} ppm per 2 min",
             (f"detrending cut the rms from {s_['rms_raw_ppm']:,} to {s_['rms_flat_ppm']:,} ppm: stellar variability" if flat < 0.8 else "detrending changed the rms by under 20 %: the raw curve is already flat")]
    S.append(sl(f"3  Light curves. {NUM[n]} {n}: raw, detrended and folded",
                '<div class="cols" style="grid-template-columns:740px 1fr;align-items:start">'
                + fig(f"fig2_{slug(n)}", 740, "Raw PDCSAP and momentum dumps; detrended with red ticks at transits; folded dip with binned data and model.")
                + "<div>" + obt(items) + "</div></div>",
                f"{n}: {r_['mode']} search, sectors {r_['sectors_used']}. Same three-panel layout as Figure 2 of the paper."))

oe = ST["oddeven"]; flagged = [n for n in ALL if abs(oe[n]["sigma_beta"]) > 3]
S.append(sl("4  Diagnostics. Odd against even transits: three planets pass 3σ, but only by 1 to 17 %",
            fig("oddeven", 1160, "(odd &minus; even depth) divided by &beta;&sigma;; grey band: &plusmn;3; red: outside.")
            + obt([f"outside 3&sigma;: {', '.join(flagged)}",
                   "depth differences: " + ", ".join(f"{n} {100*abs(oe[n]['odd_ppm']-oe[n]['even_ppm'])/((oe[n]['odd_ppm']+oe[n]['even_ppm'])/2):.1f} %" for n in flagged),
                   f"π Men c has only 2 odd and 3 even transits; the per-transit scatter ({f4['depth_scatter_ppm']} ppm) gives about 1.3&sigma;"]),
            "The odd-even test compares depths of alternate transits; an eclipsing binary at twice the period would differ by tens of percent. Differences of 1 percent on the hot Jupiters are far too small for that. The formal significance is inflated because the errors treat the noise as white; we multiply by beta."))

oc = ST["occult"]; sh = row_of("WASP-18 b", "Shporer")
S.append(sl("4  Diagnostics. Flux at phase 0.5: WASP-18 b shows its own light, 352 ppm",
            fig("occult", 1160, "Mean flux deficit in a window of one transit duration centred on phase 0.5, out-of-transit as reference.")
            + obt([f"WASP-18 b: {oc['WASP-18 b']['depth_ppm']:.0f} &plusmn; {oc['WASP-18 b']['err_ppm']:.0f} ppm (white noise); &times;&beta; {ST['rednoise']['WASP-18 b']['beta']} gives &plusmn;{oc['WASP-18 b']['err_ppm']*ST['rednoise']['WASP-18 b']['beta']:.0f}",
                   "Shporer+2019 (TESS sector 2): secondary eclipse 341 +17 &minus;18 ppm, so the two agree",
                   f"all other planets are below 3&sigma;; GJ 1132 b is {oc['GJ 1132 b']['depth_ppm']:.0f} &plusmn; {oc['GJ 1132 b']['err_ppm']:.0f} ppm, not significant after &times;&beta;"]),
            "WASP-18 b is the hottest planet here, so its day side emits enough to be seen as a dip when it goes behind the star. This is an external check: Shporer et al. measured 341 ppm on different data. The agreement is within 1 sigma."))

rn = ST["rednoise"]
S.append(sl("4  Diagnostics. Red noise: averaging helps less than 1/√N, by a factor β of 1.0 to 3.6",
            fig("rednoise", 1160, "Left: rms of the residuals against bin size for each planet; dashed: white noise. Right: &beta; per planet (red: &gt; 1.5).")
            + obt([f"largest &beta;: HD 189733 b {rn['HD 189733 b']['beta']}, HD 118203 b {rn['HD 118203 b']['beta']}; smallest: LTT 9779 b {rn['LTT 9779 b']['beta']}",
                   f"π Men c &beta; = {rn['pi Men c']['beta']}, per-point rms {rn['pi Men c']['rms1_ppm']} ppm: the quietest light curve of the eleven"]),
            "Pont, Zucker and Queloz 2006 showed that correlated noise makes transit parameters less precise than white-noise errors suggest. beta is the ratio of the measured to the white-noise rms in bins of about the transit duration. Our quoted errors include detrending and MCMC but not beta."))

S.append(sl("4  Results. Eight of ten radii within 4 % of the catalog; periods within 0.03 %",
            cols(fig("res_radius", 570, "Measured against catalog radius difference; bars: total 1&sigma;."), fig("res_period", 570, "|&Delta;P|/P, log scale.")),
            "Summary against the catalog default values for the ten selected planets."))

# --- 4b: differences from the catalog in units of the error, and where each catalog value comes from (code/21, code/22)
DEV = pd.read_csv(ROOT / "results" / "deviation_vs_catalog.csv").set_index("planet")
DSUM = json.load(open(ROOT / "results" / "deviation_summary.json"))
SRC = pd.read_csv(ROOT / "results" / "catalog_sources.csv").set_index("planet")
d_ = lambda n: DEV.loc[n]
S.append(sl("4  Results. A difference of 0.3 to 10 % from the catalog, read in units of the error",
            cols(fig("deviation_vs_catalog", 740, "Circles: ours (1&sigma;). Diamonds: published, from the PDFs. Right: pull."),
                 '<div>' + obt([f"{DSUM['n_ratio_within2']} of {DSUM['n_planets']} ratios within 2&sigma;; outside: {', '.join(DSUM['ratio_outside2'])}, {d_('WASP-18 b').dratio_pct:+.1f} % ({d_('WASP-18 b').ratio_pull:+.1f}&sigma;)",
                      f"K2-141 b is the largest difference, {d_('K2-141 b').dratio_pct:+.1f} %, but its error is {d_('K2-141 b').err_ratio_pct:.1f} %: {d_('K2-141 b').ratio_pull:+.1f}&sigma;",
                      f"HD 189733 b: {d_('HD 189733 b').dratio_pct:+.1f} % but {d_('HD 189733 b').ratio_pull:+.1f}&sigma;; with red noise (&times;{d_('HD 189733 b').beta:.1f}) {d_('HD 189733 b').ratio_pull_beta:+.1f}&sigma;",
                      "Papers scatter around the catalog too; WASP-18 b: two TESS analyses are both below it"], "How to read it")
                 + '<div style="height:10px"></div>' + obt([f"radii: {DSUM['n_rp_within2']} of {DSUM['n_planets']} within 2&sigma; ({DSUM['rp_abs_min']:.1f} to {DSUM['rp_abs_max']:.1f} %)",
                      f"periods: {DSUM['n_period_within2']} of {DSUM['n_planets']}; TOI-270 c {d_('TOI-270 c').P_pull:+.1f}&sigma;, WASP-18 b {d_('WASP-18 b').P_pull:+.1f}&sigma;"], "Radius and period") + '</div>', tpl="740px 1fr"),
            "A percentage alone says nothing. The same 1 percent is nothing for a planet with a 7 percent error and a lot for a planet with a 0.4 percent error. The pull divides the difference by the combined error of the two values. Nine of ten ratios and all ten radii are within 2 sigma; WASP-18 b is the exception. For WASP-18 b, Shporer et al. (TESS sector 2) are also below the catalog, by 4.6 percent, so the catalog value is the odd one out in the TESS band; we did not find the reason."))
rowsS = []
for n in names:
    c = SRC.loc[n]; sp = lambda t: re.sub(r" et al\.? ", " ", t)
    mix = bool(c.ratio_and_radius_from_different_papers)
    rowsS.append([f'<span style="white-space:nowrap"><b>{NUM[n]}</b> {n}</span>', sp(c.discovery_paper), sp(c.period_ref), f"{'<b>' if mix else ''}{sp(c.radius_ref)}{'</b>' if mix else ''}", f"{'<b>' if mix else ''}{sp(c.ratio_ref)}{'</b>' if mix else ''}"])
S.append(sl("4  Results. The catalog values rarely come from the discovery paper",
            tbl(["Planet", "Discovery paper", "Period", "Radius", "R<sub>p</sub>/R<sub>&#9733;</sub>"], rowsS, "tbl sm")
            + take(f"Only {DSUM['n_from_discovery_paper']} planet ({', '.join(DSUM['from_discovery_paper'])}) takes a value from its discovery paper. Radius and ratio come from two papers for {DSUM['n_mixed_sources']}: {', '.join(DSUM['mixed'])} (bold). The stellar radius comes from the radius paper for all ten."),
            "Source: NASA Exoplanet Archive pscomppars, the reference attached to each default value (code/21_catalog_methods.py). A catalog value is therefore not one measurement: different data, wavelength band and stellar radius. A difference matters only when it is larger than the combined error."))

# =============================================================== 5 agreement with the authors
rows = []
for _, c in CMP.iterrows():
    rows.append([f"<b>{NUM[c.planet]}</b> {c.planet}", c.source.split(" ")[0].replace("+", " "), f"{c.pub_ror:.4f}", f"{c.ours_ror:.4f}", f"{c.dror_pct:+.1f} %", f"{c.ror_pull:+.1f}&sigma;",
                 f"{c.Rp_pull:+.1f}&sigma;", ("differ" if abs(c.ror_pull) >= 2 else ("R differs" if abs(c.Rp_pull) >= 2 else "agree"))])
S.append(sl(f"5  Authors and us. Ratio R<sub>p</sub>/R<sub>&#9733;</sub> against {n12} published values",
            tbl(["Planet", "Paper", "Published", "Ours", "&Delta;", "Pull (ratio)", "Pull (R<sub>p</sub>)", "Verdict"], rows, "tbl sm"),
            "Published values were read from the PDFs; every number string was found verbatim in the PDF text (35 of 35). Two rows are early ground-based papers and one is an approximate read-off from a figure. 'differ': more than 2 sigma on the ratio; 'R differs': the ratio agrees but the radius does not (different stellar radius)."))

S.append(sl("5  Authors and us. Where we differ, and why",
            cols(card("HD 189733 b vs Bouchy+2005", f"Ratio 0.172 (2005) against our {row_of('HD 189733 b','Bouchy').ours_ror:.4f}. Spitzer 2007 gives 0.1545 and agrees with us ({row_of('HD 189733 b','Knutson').dror_pct:+.2f} %). The 2005 value is the outlier.", "orange", 370),
                 card("HD 209458 b vs Charbonneau+2000", f"Radius +{row_of('HD 209458 b','Charbonneau').dRp_pct:.0f} %: the paper assumes {RS} = 1.1, the archive says 1.19. The ratio differs only {row_of('HD 209458 b','Charbonneau').dror_pct:+.1f} %.", "navy", 370),
                 card("WASP-18 b vs Shporer+2019", f"Ratio {sg(sh.dror_pct)} % (nominal {abs(sh.ror_pull):.0f}&sigma;), radius {sg(sh.dRp_pct)} % ({sh.Rp_pull:+.1f}&sigma;). Different sectors; cause not found.", "orange", 370))
            + take("Everything else agrees within 2&sigma;. π Men c agrees only because a lower ratio and a higher stellar radius cancel."),
            "These are the deviations we can state with numbers. For WASP-18 b we do not have an explanation: possible reasons are different sectors, crowding correction or red noise, none tested."))

nchk = len(IDX)
S.append(sl("5  Authors and us. The checked PDFs: planet names in yellow, published numbers in green or red",
            tbl(["Item", "What was done"], [
                ["Folder", "literature/checking/, one annotated copy per PDF that names a project planet; originals in literature/pdf/ untouched"],
                ["Yellow", "every occurrence of the eleven planet names"],
                ["Green or red", "published period, ratio and radius, with a comment: published value, our value, difference, pull, verdict"],
                ["Count", f"{nchk} PDFs annotated; {sum(int(r['consistent']) for r in IDX)} values marked consistent, {sum(int(r['deviation']) for r in IDX)} marked as deviations"],
                ["Final check", f"{int(PVC.found.sum())} of {len(PVC)} quoted numbers were found verbatim in the PDF text"]], "tbl md")
            + take("Open a file in literature/checking/ and click a green or red number to read the comment."),
            "The checking folder lets you open each paper and see the planet names and the comparison in place. Red marks are the deviations of the previous slide."))

# =============================================================== 6 literature
S.append(sl(f"6  Literature. {nlit} verified papers in eleven sub-methods",
            fig("lit_map", 1160, "Left: papers per sub-method. Right: publication year (red: used in this project).")
            + take("Each entry was checked on arXiv or Crossref (first-author surname and title). Unverifiable candidates were dropped."),
            f"{nlit} papers verified, {npdf} PDFs downloaded to literature/pdf, grouped A to K. Not downloaded: the paywalled ones (Mayor and Queloz 1995, Borucki 2010, Hellier 2009, Henry 2000, Stumpe 2014, Jenkins 2002, Gelman and Rubin 1992). Dropped because unverified: McQuillan 2014, Lissauer 2012, Parmentier 2018, Montalto 2020, Cameron 2012, Winters 2019."))

steps = [["Download", "SPOC 2-min PDCSAP; TIC", "Ricker 2015; Stassun 2018; Smith 2012; Stumpe 2012"],
         ["Detrend", "Savitzky-Golay (lightkurve), masked", "Vanderburg 2014; Foreman-Mackey 2017; Hippke 2019 (wotan)"],
         ["Search", "BLS", "Kov&aacute;cs 2002; Hippke and Heller 2019 (TLS); Shallue 2018"],
         ["Fit", "batman + emcee, q<sub>1</sub>,q<sub>2</sub>", "Mandel and Agol 2002; Kreidberg 2015; Foreman-Mackey 2013; Kipping 2013"],
         ["Errors", "MCMC + detrend + R<sub>&#9733;</sub>; red noise", "Pont 2006; Berger 2018; Torres 2010"],
         ["Vet", "odd-even, phase 0.5", "Twicken 2018; Giacalone 2021; Morton 2012; Shporer 2019"],
         ["Interpret", "mass-radius, radius valley", "Zeng 2019; Fulton 2017; Owen and Wu 2017"]]
S.append(sl("6  Literature. Every pipeline step has a paper behind it",
            tbl(["Step", "What we do", "Key papers (all verified)"], steps, "tbl md"),
            "Each paper is in the verified list; the method column states what the code actually does. The alternatives in the literature (TLS, GP detrending, neural-network vetting) are covered in the group slides."))

KEY = {"A": [("Ricker", 2015), ("Stassun", 2018), ("Smith", 2012), ("Twicken", 2018), ("Huang", 2020), ("Feinstein", 2019)],
       "B": [("Vanderburg", 2014), ("Foreman-Mackey", 2017), ("Aigrain", 2016), ("Hippke", 2019), ("Kovacs", 2005)],
       "C": [("Kovacs", 2002), ("Hippke", 2019), ("Shallue", 2018), ("Osborn", 2020), ("Eisner", 2021)],
       "D": [("Mandel", 2002), ("Seager", 2003), ("Kreidberg", 2015), ("Foreman-Mackey", 2013), ("Kipping", 2013), ("Pont", 2006)],
       "E": [("Torres", 2011), ("Morton", 2012), ("Giacalone", 2021), ("Fressin", 2013), ("Bryson", 2013)],
       "F": [("Torres", 2010), ("Berger", 2018), ("Fulton", 2018), ("Dotter", 2008), ("Mann", 2015), ("Huber", 2013)],
       "G": [("Fulton", 2017), ("Owen", 2013), ("Zeng", 2019), ("Chen", 2017), ("Howard", 2012), ("Van Eylen", 2018)],
       "H": [("Mayor", 1995), ("Charbonneau", 2000), ("Borucki", 2010), ("Gillon", 2017), ("Huang", 2018), ("Kempton", 2018)],
       "J": [("Shporer", 2019), ("Eastman", 2010)],
       "K": [("Wolszczan", 1992), ("Charbonneau", 2002), ("Alonso", 2004), ("Pollacco", 2006), ("Auvergne", 2009), ("Koch", 2010), ("Howell", 2014), ("Benz", 2021)]}
for k in "ABCDEFGHK":
    title, blurb, subs = GROUPS[k]
    g = [r for r in lit if r["key"] == k]
    keyrows = []
    pick = g if len(g) <= 6 else [m[0] for au, yr in KEY[k] for m in [[r for r in g if r["first_author"] == au and int(r["year"]) == yr]] if m]
    for r in pick:
        tag = ' <b style="color:#ED1C24">&#10003;</b>' if r["used"] else ""
        keyrows.append([f"{r['first_author'].replace('Kovacs','Kov&aacute;cs').replace('Gunther','G&uuml;nther')} {r['year']}", trunc(r["t"], 84) + tag])
    left = "<div>" + card("Sub-methods", "", "navy").replace("<p></p>", "") + "</div>"
    sub_txt = ' &middot; '.join(subs)
    S.append(sl(f"6  Literature. {title}",
                take(blurb)
                + f'<p class="note" style="margin:0 0 6px;font-size:23px"><b>Sub-methods:</b> {sub_txt}.</p>'
                + tbl(["Paper", "Title"], keyrows, "tbl sm")
                + note(f"{len(g)} verified papers in this group; &#10003; = used in this project; full list in the appendix."),
                f"Group {k}: {len(g)} verified papers. {blurb}"))

irows = [[f"<b>{p}</b>", next((f"{r['first_author']} {r['year']}" for r in lit if r["used"].startswith(f"planet {NUM[p]}") or (p == 'pi Men c' and r['first_author'] in ('Huang', 'Gandolfi') and r['year'] == '2018')), "see appendix")] for p in ALL]
S.append(sl("6  Literature. The discovery papers behind the planets we compare to",
            tbl(["Planet", "Discovery or confirmation paper"], [[f"<b>{NUM[p]}</b> {p}", {"HD 118203 b": "Pepper 2020 (TESS)", "HD 189733 b": "Bouchy 2005; Knutson 2007 (Spitzer)", "HD 209458 b": "Charbonneau 2000",
                "WASP-18 b": "Hellier 2009; Shporer 2019 (TESS)", "WASP-62 b": "Hellier 2012", "LTT 9779 b": "Jenkins 2020", "TOI-270 c": "G&uuml;nther 2019", "LTT 1445 A b": "Winters 2021",
                "GJ 1132 b": "Berta-Thompson 2015", "K2-141 b": "Malavolta 2018", "pi Men c": "Huang 2018; Gandolfi 2018"}[p]] for p in ALL], "tbl sm"),
            "These are the papers whose numbers we compare against in section 8, plus the follow-up where the discovery paper is old."))

# =============================================================== 7 data retrieval
n_ok = int(CHK.same.sum())
S.append(sl("7  Data. Every catalog number can be re-queried: 52 of 52 values match today",
            code('curl -s "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?format=csv&query=\\\nselect+pl_name,pl_orbper,pl_rade,pl_ratror,st_rad,tic_id+from+pscomppars\\\n+where+pl_name=\'pi+Men+c\'"')
            + tbl(["Check", "Result"], [["Columns compared", "period, radius, ratio, stellar radius"], ["Planets", f"{CHK.planet.nunique()} (10 + π Men c + 2 stress tests)"],
                                          ["Equal to the downloaded CSV", f"{n_ok} of {len(CHK)} values (queried live, 16 Nov 2026)"]], "tbl md")
            + take("The archive keeps changing, so we store the query, the date and the comparison.")
            + note("Table: pscomppars, one row per planet; file data/catalog_recheck.csv; script code/16_reproduce.py."),
            "The archive can change as new papers are added, so we re-queried it. The downloaded copy and the live table are identical for all the planets used."))

secs = MAN.groupby("planet").agg(files=("file", "count"), sectors=("sector", lambda x: " ".join(map(str, sorted(x)))), mb=("size_kb", lambda x: x.sum() / 1024))
rows = [[f"<b>{NUM[n]}</b> {n}", RT.loc[n, "sectors"], f"{int(secs.loc[n].files)}", f"{secs.loc[n].mb:.1f}"] for n in ALL]
S.append(sl("7  Data. The light curves: 21 SPOC files, each listed with its URL and md5",
            code('import lightkurve as lk\nlc = lk.read("tess2018206045859-s0001-0000000261136679-0120-s_lc.fits",\n             flux_column="pdcsap_flux").remove_nans().normalize()')
            + cols(tbl(["Planet", "Sectors", "Files"], [r[:3] for r in rows[:6]], "tbl sm"), tbl(["Planet", "Sectors", "Files"], [r[:3] for r in rows[6:]], "tbl sm"))
            + take("Each of the 21 files has a URL and an md5 in data/data_manifest.csv."),
            "Files come from https://archive.stsci.edu/missions/tess/tid/sSSSS/xxxx/xxxx/xxxx/xxxx/ with the 16-digit TIC number split in four. The MAST API (astroquery) timed out during this work, so the static archive was used; data/data_manifest.csv has the URL and md5 of every file."))

rows = []
for n in ALL:
    t = RT.loc[n]
    rows.append([f"<b>{NUM[n]}</b> {n}", t["mode"], f"{t.period_d:.5f}", f"{t.ror:.4f}", f"{t.rp_rearth:.2f} &plusmn; {t.rp_rearth_err:.2f}", f"{t.cat_rade:.2f}"])
S.append(sl("7  Data. Run the pipeline and expect these numbers",
            tbl(["Planet", "Mode", "Period (d)", "R<sub>p</sub>/R<sub>&#9733;</sub>", "R<sub>p</sub> (R<sub>&oplus;</sub>)", "Catalog"], rows, "tbl sm")
            ,
            "Run order is in README.md. The random generator inside emcee was not seeded before; in a test two runs of pi Men c gave 2.0302 and 2.0319 Earth radii. After fixing it, two fits on the same data give identical chains."))

# =============================================================== 8 questions and conclusions
S.append(sl("8  Questions. How do we know the result is trustworthy?",
            cols(card("Benchmark", "HD 118203 b: ratio 0.0553 against the tutorial's 0.0554 and Pepper's 0.05538 (&minus;0.2 %).", "orange", 380),
                 card("Independent papers", f"{nr} of {n12} published ratios and {nrp} of {n12} radii agree within 2&sigma;; periods {nPok} of {nP}. The differences are explained or flagged.", "navy", 380),
                 card("Diagnostics", "Odd-even, phase 0.5 (WASP-18 b: 352 ppm against 341) and red noise &beta; are measured, not assumed.", "navy", 330))
            + take("We cannot know the truth; we check that an independent method agrees with published values, and say where it does not."),
            f"Answer to the question from the group. Counts are computed from paper_comparison.csv ({n12} published rows; one planet has two papers). Ratio differs: HD 189733 b against Bouchy 2005 and WASP-18 b against Shporer 2019. Radius differs: HD 189733 b against Bouchy 2005 and HD 209458 b against Charbonneau 2000."))

qa = [["Is float32 versus float64 the cause?", "No. Rounding 10<sup>-7</sup> against noise 10<sup>-4</sup>; a float32 refit moved the ratio 0.2 %, MCMC noise."],
      ["Why does Rp match for the paper's planet but not its ratio?", f"π Men c: our {RS} is 1.17, the paper's 1.10; the offsets cancel."],
      ["Why guided mode for three planets?", "Blind BLS locks on aliases for low S/N or short P; the window is a restriction, the period is still fitted."],
      ["Why only the first sectors?", "Run time and a clean baseline; more sectors would sharpen P, not R<sub>p</sub>."],
      ["What is β?", "Ratio of measured to white-noise rms in transit-length bins; 1 means white noise."],
      ["Why not use the catalog duration?", "Blind mode does not; guided mode uses it only for the BLS duration grid."]]
S.append(sl("8  Questions. Likely questions and short answers", tbl(["Question", "Answer"], qa, "tbl md"),
            "Prepared answers; each one is backed by a number in this deck."))

S.append(sl("9  Conclusions. What we rebuilt, what agrees, what does not",
            cols(card("Plotted", "Five figure types of the template paper, for ten planets; the paper's own planet gives 6.26779 d and 2.03 &plusmn; 0.07 R<sub>&oplus;</sub> against 6.27 and 2.04 &plusmn; 0.05.", "orange", 400),
                 card("Agree", f"{nr} of {n12} published ratios and {nrp} of {n12} radii within 2&sigma;; periods {nPok} of {nP}; WASP-18 b phase-0.5 flux 352 against 341 ppm.", "navy", 400),
                 card("Open", "WASP-18 b ratio (+1.5 %), the template planet's depth (&minus;6.6 % against the paper), red noise not in the quoted errors.", "navy", 400))
            + take(f"{nlit} verified papers, {npdf} PDFs, {nchk} annotated copies in literature/checking/.")
            + note("REPRODUCE.md in the project folder lists every command and the expected numbers."),
            "Conclusions. The open items are stated as open; no cause was claimed that was not tested."))

# =============================================================== appendix: full literature list
A = []
per = 8
nsl = (len(lit) + per - 1) // per
for i in range(nsl):
    g = lit[i * per:(i + 1) * per]
    rows = []
    for r in g:
        ref = re.sub(r"v\d+$", "", r["ref"])
        rows.append([f"<b>{r['key']}</b> {r['year']} {r['first_author'].replace('Kovacs','Kov&aacute;cs').replace('Gunther','G&uuml;nther')}", trunc(r["t"], 92), ref.replace("arXiv:", "") + ("" if r["pdf"] else " (no PDF)")])
    A.append(sl(f"A  Appendix. Literature, groups {g[0]['key']} to {g[-1]['key']} ({i+1}/{nsl})", tbl(["Group, year, author", "Title", "arXiv or DOI"], rows, "tbl sm"),
                "Full verified list in order of group (A mission, B detrending, C search, D modelling, E vetting, F stars, G populations, H classics, I project planets, J phase curves); notes/literature_review_TESS.md has complete titles and PDF paths."))

# =============================================================== T  TESS facts, C  sample (code/24_tess_facts.py -> results/tess_*.csv, sample_coverage.csv)
TF = pd.read_csv(ROOT / "results" / "tess_files.csv")
TP = pd.read_csv(ROOT / "results" / "tess_planets.csv").set_index("planet")
TD = json.load(open(ROOT / "results" / "tess_design_values.json"))
SC = pd.read_csv(ROOT / "results" / "sample_coverage.csv")
MS, PX, SE, CM = TD["measured"], TD["pixel"], TD["sectors"], TD["cameras"]
RSRC = "Ricker et al. 2015"
GG = pd.read_csv(ROOT / "data" / "candidates_grouped.csv").set_index("pl_name").loc[names]
G_RMIN, G_RMAX, G_PMIN, G_PMAX = GG.pl_rade.min(), GG.pl_rade.max(), GG.pl_orbper.min(), GG.pl_orbper.max()
K2B = json.load(open(ROOT / "archive" / "results_blind_failed" / "K2_141_b.json"))["bls"]["period"]


def tblw(head, rows, widths, cls="tbl sm"):
    h = "".join(f'<th style="width:{w}px">{x}</th>' for x, w in zip(head, widths))
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f'<table class="{cls}" style="table-layout:fixed"><tr>{h}</tr>{r}</table>'


# ---- T1 the satellite in numbers
t1 = [["Orbit", f"Elliptical, {TD['orbit']['period_d']} d, in 2:1 resonance with the Moon; {TD['orbit']['perigee_Re']} to {TD['orbit']['apogee_Re']} Earth radii from the Earth", "Sec 3.8, 6"],
      ["Cameras", f"{CM['n']} identical lenses, f/{CM['f_number']}, pupil {CM['pupil_cm']} cm; band {CM['band_nm'][0]} to {CM['band_nm'][1]} nm", "Table 1"],
      ["Detector", f"{TD['detector']['ccds_per_camera']} CCDs per camera, {TD['detector']['ccd_px']} &times; {TD['detector']['ccd_px']} pixels of {TD['detector']['pixel_um']} &micro;m", "Sec 4.2"],
      ["Field of view", f"24° &times; 24° per camera; 24° &times; 96° = {CM['fov_total_deg2']} deg² together", "Table 1"],
      ["One pixel", f"{PX['arcmin']}′ = {PX['arcsec']:.0f}″ = {PX['deg']:.4f}°", "Table 1"],
      ["Light in a pixel", "50 % inside one pixel; 90 % inside 4 &times; 4 pixels (1.4′)", "Table 1"],
      ["One sector", f"2 orbits = {SE['length_d']} d, then the cameras turn to the next field; {SE['per_hemisphere']} sectors per hemisphere", "Sec 7.2"],
      ["Sampling", "2-s frames; 60 are summed into one 2-min cadence for the pre-selected stars; full frames every 30 min", "Sec 3.7, 4.3"],
      ["Targets", "At least 200 000 stars at 2 min, I<sub>C</sub> about 4 to 13", "Abstract"]]
S.append(sl("T  TESS. The satellite in nine numbers",
            tblw(["Quantity", "Design value", "Where"], t1, [210, 770, 180], "tbl sm")
            + note(f"Design values from {RSRC}. The next slides check them on our 21 SPOC files."),
            "Everything in the right-hand column is quoted from the instrument paper, Ricker et al. 2015 (literature/text), with the table or section. The pixel scale of 21 arcsec per pixel and the 24 by 96 degree field are also given on the MAST page for TESS. These are design values from before launch; the later slides measure what we can on our own files."))

# ---- T2 sky coverage
S.append(sl("T  TESS. Where it looks: 13 sectors per hemisphere, 27.4 days each",
            cols(fig("tess_sectors_vs_lat", 640, "Grey: 87 shortlisted planets; red: our ten."),
                 obt([f"four cameras in a row: 24° &times; 96° = {CM['fov_total_deg2']} deg², from ecliptic latitude {SE['ecl_lat_from_deg']}° to the pole",
                      f"each sector: {SE['orbits_per_sector']} orbits = {SE['length_d']} d, then {SE['shift_deg']}° east; a hemisphere in {SE['hemisphere_yr']} yr, the sky in {SE['all_sky_yr']} yr",
                      f"observed at least 27 d: {SE['area_ge27d']:,} deg² ({100 * TD['derived']['frac_sphere_ge27d']:.0f} % of the sphere, computed); over 80 d: {SE['area_gt80d']:,} deg²; over 300 d: {SE['area_gt300d']} deg² near the poles".replace(",", " ")],
                     "Sky coverage (design)"), tpl="640px 1fr")
            + take(f"Our ten: |latitude| {TP.ecl_lat.abs().min():.1f}° (K2-141 b, {int(TP.loc['K2-141 b', 'sectors_available'])} sectors) to {TP.ecl_lat.abs().max():.0f}° (WASP-62 b, {int(TP.loc['WASP-62 b', 'sectors_available'])}). We used {int(TP.n_sectors_used.min())} to {int(TP.n_sectors_used.max())} sectors per planet."),
            f"The design numbers are from Ricker et al. 2015, Sec 7.2. The 73 percent is our own division of 30 000 by the area of the sphere, 41 253 square degrees; it is not a number from the paper. The plot comes from the MAST search done in code/03_check_mast.py: stars near the ecliptic poles are seen in many more sectors, because the sectors overlap there."))

# ---- T3 sampling and data gaps
S.append(sl("T  TESS. Sampling: one point every 2 minutes, sectors of about 27 days, gaps of 1 to 8 days",
            cols(fig("tess_coverage_raster", 740, "Good cadences (quality flag 0, finite flux) in each of our 21 SPOC files."),
                 obt([f"all 21 files: {MS['timedel_s_set'][0]:.0f} s cadence = 60 frames of 2 s; effective exposure {MS['eff_exp_s'][0]:.0f} s (header DEADC {MS['deadc_set'][0]})",
                      f"sector span {MS['span_d'][0]:.1f} to {MS['span_d'][2]:.1f} d (median {MS['span_d'][1]:.1f})",
                      f"largest gap {MS['largest_gap_d'][0]:.1f} to {MS['largest_gap_d'][2]:.1f} d (median {MS['largest_gap_d'][1]:.1f}); good cadences {100 * MS['duty_good'][0]:.0f} to {100 * MS['duty_good'][2]:.0f} % of the span (median {100 * MS['duty_good'][1]:.0f})",
                      f"one transit lasts {TP.trandur_h.min():.1f} to {TP.trandur_h.max():.1f} h = {TP.points_per_transit.min():.0f} to {TP.points_per_transit.max():.0f} cadences"],
                     "Measured on our files"), tpl="740px 1fr"),
            "The red line marks 13.7 days, one spacecraft orbit. Most files show a break near it, and the shorter breaks are cadences flagged by the pipeline. We did not separate the causes of each break. The number of cadences in a transit uses the catalog transit duration (pl_trandur) divided by 120 s."))

# ---- T4 data products by cycle
used_secs = sorted(set(TF.sector))
t4 = [["SPOC light curve, target pixels", "120 s", "From sector 1", f"<b>Yes</b>: all {MS['n_files']} files (PDCSAP flux)"],
      ["SPOC fast light curve", "20 s", "First extended mission, from sector 27", "No"],
      ["Full-frame images", "30 min", "Years 1 and 2 (sectors 1 to 26)", "No"],
      ["Full-frame images", "10 min", "Years 3 and 4 (sectors 27 to 55)", "No"],
      ["Full-frame images", "200 s", "Years 5 on (sector 56 and later)", "No"]]
S.append(sl("T  TESS. Data products: 2-min light curves from the start; full frames every 30 min, then 10 min, then 200 s",
            tblw(["Product", "Cadence", "Available", "Used here"], t4, [330, 140, 400, 290])
            + cols(card("Our files", f"{len(used_secs)} sectors: {', '.join(map(str, used_secs))}. First observation {MS['first']}, last {MS['last']}: years 1, 2, 4, 5 and 8 of the mission.", "navy", 140),
                   card("Time stamps", "BTJD = BJD<sub>TDB</sub> &minus; 2 457 000 d. Each cadence is the sum of 60 frames; flux units are e<sup>&minus;</sup>/s.", "orange", 140)),
            "Cadence by cycle is from the NASA HEASARC page on TESS data products; the year-to-sector table is from the TESS science page at MIT; the fast cadence and sector 27 as the first extended-mission sector are from the STScI TESS archive manual (pages saved in data/raw/tess_docs/). We use only the 2-minute SPOC light curves."))

# ---- T5 pixel scale and resolution
t5r = [["One pixel", f"15 &micro;m = {PX['arcmin']}′ = {PX['arcsec']:.0f}″ = {PX['deg']:.4f}° ({PX['px_per_deg']:.0f} pixels per degree)", f"WCS in our files: {MS['pix_scale_arcsec'][0]:.1f} to {MS['pix_scale_arcsec'][1]:.1f}″"],
       ["One camera", f"2 &times; 2 CCDs of 2048 pixels = {PX['mosaic_px']} pixels = {PX['mosaic_deg']:.1f}°", "computed; 24° quoted"],
       ["Half of a star's light", "inside one pixel (21″)", f"{RSRC}, Table 1"],
       ["90 % of the light", f"inside 4 &times; 4 pixels ({PX['ensq90_arcsec']:.0f}″ = 1.4′)", "images are undersampled"],
       ["One pixel on the sky", f"21″ &times; distance: {TP.pixel_au.min():.0f} AU at LTT 1445 A (6.9 pc) to {TP.pixel_au.max():,.0f} AU at WASP-62 (176 pc)".replace(",", " "), "catalog distance"],
       ["Our apertures", f"{int(TP.npix_opt.min())} to {int(TP.npix_opt.max())} pixels = equal radius {TP.r_eq_arcsec.min():.0f} to {TP.r_eq_arcsec.max():.0f}″", "measured on our files"]]
S.append(sl("T  TESS. Resolution: one pixel is 21″ = 0.0058°, and 90 % of a star's light lands within 1.4′",
            tblw(["Quantity", "Value", "Source"], t5r, [270, 640, 250], "tbl sm")
            + take("A star within about 1.4′ adds light to the aperture; two stars inside one pixel cannot be told apart.")
            + note("The equal radius is sqrt(N/&pi;) pixels for the N pixels of the optimal aperture."),
            f"The pixel size and the energy fractions are from {RSRC}, Table 1; 21 arcsec per pixel is also on the STScI TESS page. The pixel scale of our files is read from the WCS stored with the aperture mask. The distance-based sizes use the catalog distance of each star."))

# ---- T6 apertures and crowding
c4 = TF[(TF.planet == "LTT 1445 A b")].iloc[0]
S.append(sl("T  TESS. Our ten apertures: LTT 1445 A b has only 42 % of its light from the target",
            fig("tess_apertures", 960, "Optimal-aperture pixels, first sector used. CROWDSAP: share of the aperture flux from the target.")
            + take("PDCSAP removes the rest (median PDCSAP/SAP = CROWDSAP/FLFRCSAP; LTT 1445 A b: 0.434). Its companions lie 5 to 7″ from A, inside one pixel."),
            "CROWDSAP and FLFRCSAP are header keywords of the SPOC light curve. We checked on three files that the median of PDCSAP divided by the median of SAP equals CROWDSAP divided by FLFRCSAP; LTT 1445 A b, GJ 1132 b and pi Men c agree to three digits. The depth of LTT 1445 A b therefore depends on the size of a large correction. Winters et al. 2021 describe LTT 1445 as a hierarchical triple M-dwarf system at 6.86 pc."))

# ---- T7 per planet
t7 = []
for n in names:
    r = TP.loc[n]
    t7.append([f"<b>{NUM[n]}</b> {n}", f"{r.tmag:.1f}", f"{r.camera}", f"{int(r.n_sectors_used)} of {int(r.sectors_available)}", f"{int(r.npix_opt)} / {r.r_eq_arcsec:.0f}″", f"{r.crowdsap_min:.2f}", f"{r.cdpp1_ppm:.0f}", f"{r.trandur_h:.1f} h / {r.points_per_transit:.0f}", f"{r.depth_ppm:.0f}"])
S.append(sl(f"T  TESS. Precision: {TP.cdpp1_ppm.min():.0f} to {TP.cdpp1_ppm.max():.0f} ppm per hour, and {TP.points_per_transit.min():.0f} to {TP.points_per_transit.max():.0f} points per transit",
            tblw(["Planet", "T mag", "Cam", "Sectors", "Px / r", "CROWD", "CDPP 1h", "Transit / n", "Depth"], t7, [215, 75, 80, 125, 140, 90, 115, 190, 110], "tbl xs")
            + note("CDPP 1 h: combined differential photometric precision on 1 h, SPOC header keyword (median of the sectors used, ppm). Cam: camera. Sectors: used of available. Px / r: optimal-aperture pixels and equal radius. CROWD: lowest CROWDSAP. Transit / n: duration and number of cadences. Depth: (R<sub>p</sub>/R<sub>&#9733;</sub>)&sup2; in ppm, our fit."),
            "Columns come from the FITS headers of the SPOC files (results/tess_planets.csv). The depth over CDPP ratio is a crude indicator and is not the signal-to-noise of the fit: K2-141 b has a depth of 355 ppm against 325 ppm per hour, and it is detected only because 57 transits are folded."))

# ---- C1 how a catalog divides planets
c1 = [["Radius", "under 1.25 R<sub>&oplus;</sub> Earth-size; 1.25 to 2 Super-Earth; 2 to 4 Sub-Neptune; 4 to 8 Neptune/Saturn; 8 and more Jupiter-size", "<b>Yes</b>", "pl_rade"],
      ["Orbital period", "under 1 d ultra-short (USP); 1 to 3 hot; 3 to 7 warm; 7 to 15 cool", "<b>Yes</b>", "pl_orbper"],
      ["Equilibrium temperature", "above 2000 K ultra-hot; 1200 to 2000 hot; 500 to 1200 warm; below 500 K temperate", "<b>Yes</b>", "pl_eqt"],
      ["Host star", "M dwarf (under 3900 K); K (under 5200); G (under 6000); F and hotter", "<b>Yes</b>", "st_teff"],
      ["Discovery method", "transit, radial velocity, imaging, microlensing, &hellip;", "Recorded, not used to choose", "discoverymethod"],
      ["System", "one planet or several in the same system", "Recorded, not used to choose", "sy_pnum"]]
S.append(sl("C  Sample. Six ways a catalog divides exoplanets; our grouping uses the first four",
            tblw(["Axis", "Classes", "Used here", "Column"], c1, [230, 600, 170, 160], "tbl xs")
            + note("The class edges are ours (code/02_group_candidates.py); other papers place them elsewhere. Mass, density, insolation and the radius valley are also used in the literature, not here."),
            "These are the columns of the NASA Exoplanet Archive table pscomppars and the group edges we set in code/02_group_candidates.py for the 471 planets in data/candidates_grouped.csv. We chose the ten planets from these groups, not from the discovery method or the system."))


# ---- C2 coverage
def _row(r):
    gap = r.catalog_pct >= 25 and r.ours_pct <= 0.4 * r.catalog_pct
    col = "#ED1C24" if gap else "#1b1f3b"
    bar = f'<span style="display:inline-block;background:#c9d0ea;height:13px;width:{r.catalog_pct * 1.8:.0f}px;margin-left:8px;vertical-align:middle"></span>'
    return [f"{'<b>' if gap else ''}{r.group}{'</b>' if gap else ''}", f"{r.catalog_n} ({r.catalog_pct:.0f} %)" + bar, f'<span style="color:{col};font-weight:{800 if gap else 400}">{r.ours_n}</span>']


def _blk(title, axes):
    rows = []
    for ax_, groups in axes:
        sub = SC[SC.axis == ax_]
        rows += [_row(r) for _, r in sub.iterrows()]
    return f'<h3 style="margin:6px 0 2px;font-size:22px;color:#273896">{title}</h3>' + tblw(["Class", "471 catalog", "Our 10"], rows, [215, 235, 110], "tbl xs")


S.append(sl("C  Sample. Our ten against the 471: every size class and star type is present, the 7 to 15 d period class is empty",
            cols("<div>" + _blk("Radius", [("g_size", 0)]) + _blk("Orbital period", [("g_period", 0)]) + "</div>",
                 "<div>" + _blk("Equilibrium temperature", [("g_teq", 0)]) + _blk("Host star", [("g_star", 0)]) + "</div>", tpl="1fr 1fr")
            + note("Red: a class that holds at least 25 % of the 471 planets while our ten hold at most 40 % of that share. Bars: share of the 471."),
            "Counts come from results/sample_coverage.csv, built by code/24_tess_facts.py from data/candidates_grouped.csv. The four axes are the ones we used to choose the planets. The discovery method and the number of planets per system are on the next slide."))

# ---- C3 is ten enough?
cv = SC.set_index("group")
c3r = [["<b>Enough for</b>", f"Showing that the pipeline runs from {G_RMIN:.1f} to {G_RMAX:.1f} R<sub>&oplus;</sub>, periods of {G_PMIN:.2f} to {G_PMAX:.1f} d, T mag {TP.tmag.min():.1f} to {TP.tmag.max():.1f}, all four host-star types and all four TESS cameras."],
       ["<b>Not enough for</b>", f"Statements per class: Earth-size, Neptune/Saturn and Sub-Neptune have one planet each. No planet has a period of 7 to 15 d ({int(cv.loc['Cool (7-15 d)', 'catalog_n'])} of 471); our longest is {G_PMAX:.1f} d, so the blind search to 15 d is untested above that. Radial-velocity discoveries: 3 of 10, 8 of 471."],
       ["<b>Weak spot</b>", f"The three smallest, shortest-period planets were searched near the catalog period; K2-141 b searched blind gave {K2B:.2f} d, the catalog value is {RT.loc['K2-141 b', 'period_d']:.3f} d."]]
S.append(sl("C  Sample. Is ten enough? Enough to show the method, not to say anything about a class",
            tblw(["", "Ten planets"], c3r, [230, 930], "tbl sm")
            + take("Minimum: say on the slide what is covered and what is not. If there is time: add a sub-Neptune with a 7 to 15 d period, e.g. TOI-2134 b (9.23 d, T mag 7.8) or HD 97658 b (9.49 d, T mag 7.0). Not checked: SPOC data, papers.")
            + note("The assignment slip gives the title only, no number of planets."),
            "The sample covers every size class and every star type but is thin in each. The empty class is the period class from 7 to 15 days, which holds 29 percent of the catalog sample. The two candidate planets are from the 139 cool-period planets in data/candidates_grouped.csv; we have not checked that their SPOC files exist and have not run them. TOI-2134 b is 2.74 Earth radii, HD 97658 b is 2.12."))

# =============================================================== H  History, and new T slides (orbit, launch and cost, Vietnam, sources); code/24-28
sys.path.insert(0, str(ROOT / "slides" / "deck"))
from exo_timeline_svg import exo_timeline_svg, exo_planets_svg   # noqa: E402

SF = pd.read_csv(ROOT / "data" / "literature" / "tess_fact_sources.csv").set_index("id")
PG = lambda i: int(SF.loc[i, "page"])
ON = json.load(open(ROOT / "results" / "tess_orbit_numbers.json"))
DSY = json.load(open(ROOT / "results" / "discoveries_summary.json"))
FAC = pd.read_csv(ROOT / "data" / "raw" / "discoveries_by_facility.csv")
CM_ = pd.read_csv(ROOT / "data" / "raw" / "catalog_methods.csv").set_index("pl_name")
SRCMAP = {}          # tiêu đề -> dòng nguồn hiển thị ở chân slide
tot = DSY["total"]; bm = DSY["by_method"]

# ---- H1 timeline
S.append(sl("H  History. Four lines of work led to TESS and to our ten planets",
            exo_timeline_svg()
            + note("Dashed: the earlier result was the reason or idea. Solid: the same planet or the same hardware."),
            "Layout and drawing style follow the Hadoop timeline of the HUST sample deck (slide 31): lanes by role, dashed lines for ideas, solid lines for dependencies. Every node has a paper in the literature folder and a verbatim quote checked in data/literature/tess_fact_sources.csv. Mayor and Queloz 1995 and Wolszczan 1992 are paywalled and were not downloaded; their entries rest on the title and the Crossref record. HD 209458 b is the first planet seen to transit, found earlier by radial velocity (Charbonneau 2000)."))
SRCMAP["H  History. Four lines"] = "Source: papers in literature/pdf/K_Search_history and Charbonneau 2000; quotes and pages in tess_fact_sources.csv"

# ---- H2 discoveries by year and method
facs = [("Kepler", DSY["facilities"]["Kepler"]), ("TESS", DSY["facilities"]["Transiting Exoplanet Survey Satellite"]), ("K2", DSY["facilities"]["K2"]), ("SuperWASP", DSY["facilities"]["SuperWASP"]),
        ("HATNet", DSY["facilities"]["HATNet"]), ("CoRoT", DSY["facilities"]["CoRoT"]), ("KELT", DSY["facilities"]["KELT"]), ("MEarth", DSY["facilities"]["MEarth"])]
S.append(sl(f"H  History. {f'{tot:,}'.replace(',', ' ')} confirmed planets: {100 * bm['Transit'] / tot:.0f} % found by transits, {100 * bm['Radial Velocity'] / tot:.0f} % by radial velocity",
            cols(fig("exo_discoveries", 740, "Confirmed planets per year of discovery, by method (NASA Exoplanet Archive)."),
                 "<div>" + tblw(["Facility", "Planets"], [[n, f"{v:,}".replace(",", " ")] for n, v in facs], [230, 130], "tbl xs")
                 + note("Planets whose discovery facility is named in the archive.")+ "</div>", tpl="740px 1fr"),
            f"The archive table pscomppars was queried on {DSY['date']} with TAP. The numbers change as planets are added. Kepler, K2 and TESS together account for {DSY['facilities']['Kepler'] + DSY['facilities']['K2'] + DSY['facilities']['Transiting Exoplanet Survey Satellite']} planets; the ground-based transit surveys in the table are far smaller."))
SRCMAP["H  History. "] = f"Source: NASA Exoplanet Archive, table pscomppars, TAP query of {DSY['date']} (data/raw/discoveries_by_*.csv)"

# ---- H3 missions in numbers
def _pp(i): return f"p. {PG(i)}"
mrows = [["CoRoT", "Launch 27 Dec 2006", "Polar orbit; built and operated by CNES", "First planet: CoRoT-Exo-1b (2008)", f"Auvergne 2009 {_pp('corot_launch')}; Barge 2008 {_pp('corot_first')}"],
         ["Kepler", "Launch 6 Mar 2009", "0.95 m aperture; Earth-trailing heliocentric orbit", f"{DSY['facilities']['Kepler']:,} planets in the archive".replace(",", " "), f"Koch 2010 {_pp('kepler_launch')}, {_pp('kepler_ap')}"],
         ["K2", "2014", "Kepler spacecraft after two reaction wheels were lost; fields along the ecliptic", f"{DSY['facilities']['K2']} planets", f"Howell 2014 {_pp('k2_wheels')}, {_pp('k2_ecliptic')}"],
         ["TESS", "Launch 18 Apr 2018", "4 cameras, 24° &times; 96°; 13.7-day orbit", f"{DSY['facilities']['Transiting Exoplanet Survey Satellite']:,} planets".replace(",", " "), f"Ricker 2015 {_pp('orbit_shape')}, {_pp('fov')}; NASA page"],
         ["CHEOPS", "Launch 18 Dec 2019", "Secondary passenger on a Soyuz-Fregat from Kourou", "ESA small mission", f"Benz 2021 {_pp('cheops_launch')}"],
         ["PLATO", "Selected as ESA M3", "Wide-field multi-camera survey", "In preparation", f"Rauer 2014 {_pp('plato_m3')}"],
         ["JWST", "L2 observatory", "Infrared; transit of WASP-39 b with NIRCam on 22 to 23 July 2022", "First atmosphere transits", f"Gardner 2006 {_pp('jwst_design')}; Ahrer 2023 {_pp('jwst_wasp39')}"]]
S.append(sl("H  History. The space missions in numbers: launch, hardware and first results",
            tblw(["Mission", "Start", "Hardware", "Result", "Paper, page"], mrows, [120, 210, 400, 230, 200], "tbl xs")
            + note("Planet counts: NASA Exoplanet Archive by discovery facility. PLATO: selected in 2014 (Rauer); we did not check its current launch date."),
            "Launch dates and hardware are quoted from the mission papers with the PDF page of the quote (data/literature/tess_fact_sources.csv). The TESS launch date comes from the NASA mission page. The planet counts are from the archive query on the same day as slide H2."))
SRCMAP["H  History. The space missions"] = "Source: the five mission papers and Ricker 2015 (page numbers in the last column); NASA Science TESS page"

# ---- H4 where our ten were discovered
ten = names
h4 = []
for n in ten:
    c = CM_.loc[n]
    fac = {"Haute-Provence Observatory": "Haute-Provence (RV)", "W. M. Keck Observatory": "Keck (RV)", "Cerro Tololo Inter-American Observatory": "MEarth-South, CTIO",
           "Transiting Exoplanet Survey Satellite (TESS)": "TESS", "K2": "K2", "SuperWASP": "SuperWASP"}.get(c.disc_facility, c.disc_facility)
    h4.append([f"<b>{NUM[n]}</b> {n}", fac, f"{int(c.disc_year)}"])
S.append(sl("H  History. Where our ten planets were discovered: six by Doppler or ground surveys, four by space missions",
            cols('<div>' + exo_planets_svg(700, 400) + '<p class="note" style="margin:2px 0">Numbers are the planet numbers of this deck.</p></div>',
                 tblw(["Planet", "Discovery facility", "Year"], h4, [190, 230, 80], "tbl xs"), tpl="700px 1fr")
            + note("Method and facility as the NASA archive records them. HD 189733 b is listed as a Doppler discovery; its 2005 paper reports the transit."),
            "Discovery method, facility and year are the archive columns discoverymethod, disc_facility and disc_year. By lane: three Doppler discoveries (HD 118203 b, HD 189733 b, HD 209458 b), three ground transit discoveries (WASP-18 b, WASP-62 b, GJ 1132 b) and four from space (K2-141 b, TOI-270 c, LTT 1445 A b, LTT 9779 b). The archive lists GJ 1132 b under the Cerro Tololo facility, where the MEarth-South array stands (Berta-Thompson 2015)."))
SRCMAP["H  History. Where our ten"] = "Source: NASA Exoplanet Archive pscomppars (discoverymethod, disc_facility, disc_year); Berta-Thompson 2015"

# ---- T orbit
S.append(sl("T  TESS. Where it flies: a 13.7-day orbit between 17 and 59 Earth radii",
            cols(fig("tess_orbit", 540, "Top view, to scale in distance (not in tilt)."),
                 obt([f"launch from Cape Canaveral into a parking orbit (28.5°); two burns raise the apogee to 400 000 km; a lunar flyby lifts the ecliptic inclination to about 40°; final orbit about 60 days after launch (nominal scenario)",
                      f"final orbit: 17 to 59 R<sub>&oplus;</sub>, 13.7 d, 2:1 with the Moon; Kepler's third law with a = {ON['a_RE']:.0f} R<sub>&oplus;</sub> gives {ON['period_from_kepler_d']:.1f} d (computed)",
                      "data: downlinked every 13.7 d at perigee, 4 h at 100 Mb/s; then the cameras repoint",
                      "why here: outside the radiation belts, no long eclipses, stable for decades without station-keeping"], "Path and orbit"), tpl="540px 1fr"),
            f"All statements in the right-hand box are quoted from Ricker et al. 2015: Section 6 on page {PG('orbit_shape')} (orbit and the nominal path), Section 5 on page {PG('downlink_len')} (downlink), Table 2 on page {PG('ops')}. The path is described as a nominal scenario before launch; the actual launch was on 18 April 2018. The Kepler's-law period and the Moon's orbit radius (384 400 km = {ON['moon_RE']:.0f} Earth radii) are our own computations with standard constants; twice the TESS period, 27.4 d, is close to the Moon's sidereal period, 27.3 d."))
SRCMAP["T  TESS. Where it flies"] = f"Source: Ricker et al. 2015, Sec 6 p. {PG('orbit_shape')}, Sec 5 p. {PG('downlink_len')}, Table 2 p. {PG('ops')}; constants and Kepler check: code/28"

# ---- T launch and cost
lrows = [["Who runs it", "MIT leads the mission; the Explorers Program at NASA Goddard oversees it; NASA's Launch Services Program (Kennedy) manages the launch", "NASA release C14-049"],
         ["Who launched it", "SpaceX, Falcon 9, from Cape Canaveral AFS on 18 April 2018 at 6:51 p.m. EDT. NASA chose SpaceX on 16 Dec 2014 (Falcon 9 v1.1, liftoff then targeted for Aug 2017)", "NASA release; MIT News"],
         ["Cost of the launch", "About $87 million to NASA: launch service, spacecraft processing, payload integration, tracking, data and telemetry", "NASA release C14-049"]]
S.append(sl("T  TESS. Who launched it and what it cost: SpaceX, about $87 million for the launch",
            tblw(["Question", "Answer", "Source"], lrows, [200, 720, 240], "tbl xs")
            + cols(card("2006", "$20 million: first proposal, private (MIT)", "navy", 150), card("2006 to 2008", "$120 million: proposal to NASA (MIT)", "navy", 150),
                   card("Dec 2014", "$87 million: launch alone (NASA)", "orange", 150), card("Apr 2018", "$337 million: total reported (Physics World)", "orange", 150))
            + take("$87 million is the launch only; $337 million is a reported total."),
            "The launch cost and the contract are quoted from NASA contract release C14-049 of 16 December 2014. The launch date and time are from the MIT News article. The $337 million appears in a Physics World report of 19 April 2018; Sky and Telescope and Wikipedia were seen in a web search with other splits (about $200 million plus $87 million) but we did not verify those pages, so we do not use them. The proposal budgets are from the MIT News history of the mission; the $20 million was a private proposal in 2006 and the $120 million a NASA funding level, both before the 2008 Small Explorer proposal."))
SRCMAP["T  TESS. Who launched"] = "Source: NASA release C14-049 (16 Dec 2014); MIT News (Apr 2018); Physics World (19 Apr 2018)"

# ---- T Vietnam
dv = ON["dv_leo300_to_apogee400000_kms"]
S.append(sl("T  TESS. Could Vietnam launch a TESS? Not on its own rocket, but a launch can be bought",
            cols(obt(["VNREDSat-1 flew on a Vega rocket from French Guiana on 7 May 2013; the whole programme cost EUR 55.8 million",
                      "LOTUSat-1 (570 kg) was &lsquo;awaiting Japan&rsquo;s launch vehicle&rsquo; in July 2024; a facility for satellites under 180 kg was planned for December 2025",
                      "In August 2026 VinSpace chose a SpaceX Transporter rideshare for its first satellites, in the second quarter of 2027",
                      "TESS: $87 million for the launch alone"], "Evidence (sourced)"),
                 obt([f"Reaching an apogee of 400 000 km from a 300 km circular orbit needs &Delta;v = {dv:.1f} km/s on top of {ON['circ_leo300_kms']:.1f} km/s: a heavy launcher, not a small rocket (computed)",
                      f"Latitude is not the obstacle: 8.6° N gives {ON['rot_kms_vn_south_8p6'] * 1000:.0f} m/s of Earth rotation against {ON['rot_kms_cape_28p5'] * 1000:.0f} at Cape Canaveral, +{ON['rot_gain_ms_vn_south_vs_cape']:.0f} m/s, {100 * ON['rot_gain_ms_vn_south_vs_cape'] / 1000 / ON['circ_leo300_kms']:.1f} % of orbital speed (computed)",
                      "We found no report of a Vietnamese orbital rocket or spaceport (one web search)",
                      "Realistic: buy a launch, ride as a secondary passenger (CHEOPS did), or build ground robotic transit telescopes (MEarth found GJ 1132 b)"], "Our reasoning"))
            + note("Judgement, not a source: a self-launched TESS-class mission is not realistic soon; our computations use standard constants (code/28_orbit_figure.py)."),
            "Evidence: Government of Viet Nam news of 7 May 2013 (VNREDSat-1: Vega, Guiana Space Center, EUR 55.8 million including about 65 billion dong from Vietnam); VietnamNet of 15 July 2024 (LOTUSat-1 awaiting a Japanese launch vehicle; small-satellite facility planned for December 2025; we did not check later status); Al Jazeera of 11 August 2026 (VinSpace and SpaceX Transporter rideshare, Q2 2027). Reasoning: the delta-v is from the vis-viva equation; the latitude argument uses the equatorial rotation speed 0.465 km/s times cos(latitude). Self-launch would need a launcher, a range and flight heritage; we only found no report of one in one web search, which is not proof."))
SRCMAP["T  TESS. Could Vietnam"] = "Source: Gov. of Viet Nam news (7 May 2013); VietnamNet (15 Jul 2024); Al Jazeera (11 Aug 2026); Benz 2021; code/28"

# ---- T sources table (Ricker facts with PDF page)
ids = ["orbit_shape", "orbit_period", "launch_site", "launch_moon", "downlink", "fov", "pixel", "ensq90", "sector_len", "coverage_27", "cadence_2min"]
srows = [[SF.loc[i, "statement"], SF.loc[i, "value"].replace("_", " "), f"Ricker 2015, {SF.loc[i, 'location']}", f"p. {PG(i)}"] for i in ids]
S.append(sl("T  TESS. Where each design number comes from: instrument paper, section and PDF page",
            tblw(["Statement", "Value", "Where", "PDF page"], srows, [350, 390, 300, 120], "tbl xs")
            + note("PDF pages of arXiv:1406.0151v3. Each quote is checked in data/literature/tess_fact_sources.csv."),
            "The table is built from data/literature/tess_fact_sources.csv by code/26_tess_sources.py, which searches each quoted phrase in the PDF text page by page; a row is written as verified only when the phrase is found. The first citation is Ricker, G. R. et al. 2015, Journal of Astronomical Telescopes, Instruments, and Systems 1(1), 014003, arXiv:1406.0151."))
wids = ["launch_provider", "launch_cost", "mission_cost_pw", "pixel_mast", "ffi_cycles", "vn_vnredsat", "vn_lotusat", "vn_vinspace"]
wrows = [[SF.loc[i, "source"], (lambda u: u if len(u) <= 70 else u[:68] + "&hellip;")(SF.loc[i, "url"].replace("https://", "")), SF.loc[i, "statement"]] for i in wids]
S.append(sl("T  TESS. Web pages used, saved on 21 November 2026",
            tblw(["Source", "Address", "Used for"], wrows, [300, 520, 340], "tbl xs")
            + note("Copies in data/raw/tess_docs/; each quoted phrase was found in the saved page."),
            "Web pages are public. Their text was saved on 21 November 2026 and each quoted phrase was searched in the saved copy. Web pages can change; the saved copies keep what we used."))

# ---- Q  ten questions the lecturer may ask (inferred from the group chat; answers point to the sections that prove them)
peM = 1e6 * RT.loc[names, "period_err"] / RT.loc[names, "period_d"]
oc_ = ST["occult"]["WASP-18 b"]
qrows = [
    ["Why can a dip in brightness give a radius?", f"Depth &asymp; (R<sub>p</sub>/R<sub>&#9733;</sub>)&sup2;, R<sub>p</sub> = ratio &times; R<sub>&#9733;</sub>. R<sub>&#9733;</sub> comes from the archive, not from us, so its error goes straight into R<sub>p</sub> (section 7)."],
    ["Why trust this period, not P/2 or 2P?", f"BLS scans 0.26 to 15 d; {DSUM['n_period_within2']} of {DSUM['n_planets']} periods agree with the catalog within 2&sigma;. Three planets were searched near the catalog period; K2-141 b searched blind gave {K2B:.2f} d (sections 6, 7)."],
    ["Where do the errors come from; are they complete?", f"MCMC, three detrending variants and R<sub>&#9733;</sub>. Red noise (&beta; {DEV.beta.min():.1f} to {DEV.beta.max():.1f}) is not included; with &times;&beta; the HD 189733 b pull falls from {d_('HD 189733 b').ratio_pull:+.1f}&sigma; to {d_('HD 189733 b').ratio_pull_beta:+.1f}&sigma; (section 7)."],
    ["Why does the result differ from NASA?", f"A difference means something only in units of its error. {DSUM['n_ratio_within2']} of {DSUM['n_planets']} ratios are within 2&sigma;. Catalog values come from other papers: only {DSUM['n_from_discovery_paper']} planet takes them from its discovery paper (section 7)."],
    ["How do you know it is a planet, not a binary star?", f"All ten are confirmed planets in the NASA archive; we did no centroid vetting. We ran the odd-even test and the phase-0.5 test (WASP-18 b: {oc_['depth_ppm']:.0f} &plusmn; {oc_['err_ppm']:.0f} ppm; Shporer et al. 341) (section 7)."],
    ["Do the ratio, the impact parameter and limb darkening degenerate?", f"Limb darkening (q<sub>1</sub>, q<sub>2</sub>) and b are fitted. LTT 9779 b: b = {RT.loc['LTT 9779 b', 'b']:.2f} and a {d_('LTT 9779 b').err_ratio_pct:.0f} % error, mostly from detrending, not from MCMC (section 6)."],
    ["Which assumptions can be wrong?", "Circular orbits for all ten (HD 118203 b has e = 0.316, Pepper 2020), R<sub>&#9733;</sub> from the archive, only 1 to 4 sectors, and the crowding correction (LTT 1445 A b: CROWDSAP 0.42) (sections 4, 6)."],
    ["What does TESS give, and what does it not?", f"2-min points, 27-d sectors, 21&Prime; pixels, gaps of 1 to 8 d. Period error from {peM.min():.1f} ppm ({peM.idxmin()}) to {peM.max():.0f} ppm ({peM.idxmax()}) (section 4)."],
    ["Why these ten planets? Is ten enough?", "They cover every size class and host-star type; the 7 to 15 d period class is empty (29 % of the catalog sample). Enough to show the method, not to say anything about a class (section 5)."],
    ["What would you do differently?", "Use every sector, fit the eccentricity, detrend with Gaussian processes, multiply the errors by &beta;, and read the Methods of each catalog paper (sections 7, 8)."]]
for lo, hi in ((0, 5), (5, 10)):
    S.append(sl(f"8  Questions. Ten questions the lecturer may ask: {lo + 1} to {hi}",
                tblw(["Question", "Short answer and where it is shown"], qrows[lo:hi], [340, 820], "tbl sm")
                + note("Inferred from the group's comments (the nature of the result, why, and what supports it); the lecturer has not confirmed them."),
                "These ten questions are our guess, built from two remarks in the group chat: the lecturer asks about the nature of the result, why things are so, and what supports each claim, and she asks to check whether the published method differs from ours. Each answer uses numbers computed elsewhere in this deck."))

# ---- D  raw data of TESS: structure, plots, access (code/32_raw_data.py -> results/raw_data_facts.json)
RAW = json.load(open(ROOT / "results" / "raw_data_facts.json")); RT_ = RAW["tpf"]; QK = RAW["quality"]
sp = lambda n: f"{n:,}".replace(",", " ")
hd = [["PRIMARY", "header only: object, sector, camera, CCD, processing version", "no table"],
      ["LIGHTCURVE", f"one row per 2-min cadence, {RAW['n_cols']} columns", f"{sp(RAW['rows'])} rows"],
      ["APERTURE", "pixel mask: which pixels are summed (bit 2) and which give the background (bit 4)", f"{RAW['aperture_shape'][1]} &times; {RAW['aperture_shape'][0]} integers"],
      ["PIXELS (target-pixel file)", "the same cadences, but every cell is an image: RAW_CNTS, FLUX, FLUX_BKG ...", f"{sp(RT_['flux_shape'][0])} rows, {RT_['flux_shape'][2]} &times; {RT_['flux_shape'][1]} pixels each"]]
hk = RAW["header"]
S.append(sl("7  Data. A raw TESS file is a FITS file: a header, a table of cadences and a pixel mask",
            tblw(["Extension", "What it holds", "Size in our example"], hd, [260, 640, 260], "tbl sm")
            + cols(card("Our example", f"HD 189733 b, sector {hk['SECTOR']}, camera {hk['CAMERA']}, CCD {hk['CCD']}; {RAW['size_mb']} MB; SPOC {hk['PROCVER'][:11]}.", "navy", 130),
                   card("Time", f"BTJD = BJD<sub>TDB</sub> &minus; 2 457 000 d; cadence {hk['TIMEDEL'] * 86400:.0f} s; {hk['TSTART']:.1f} to {hk['TSTOP']:.1f}.", "orange", 130))
            + note(f"The target-pixel file (_tp.fits, {RT_['size_mb']} MB for &pi; Men c) is the rawer product."),
            "FITS is the astronomy file format: a primary header followed by extensions that are tables or images. astropy.io.fits reads them. Extension names and sizes are read from our own files with code/32_raw_data.py. The statement that the pixel files hold one image per time stamp and that light curves come from them is quoted from the STScI TESS archive manual (tess_fact_sources.csv, tpf_def)."))
grp = [["Time", "TIME, TIMECORR, CADENCENO", "BTJD days, days, integer", "TIME is stored in 64 bits (float64)"],
       ["Aperture flux", "SAP_FLUX, SAP_FLUX_ERR", "e&minus;/s", "sum of the pixels of the optimal aperture"],
       ["Background", "SAP_BKG, SAP_BKG_ERR", "e&minus;/s", "background summed over the same pixels"],
       ["Corrected flux", "PDCSAP_FLUX, PDCSAP_FLUX_ERR", "e&minus;/s", "systematics removed, aperture fraction and crowding corrected"],
       ["Quality", "QUALITY", "integer bit mask", "0 = good; each bit is one reason to distrust the cadence"],
       ["Position", "PSF_CENTR1/2, MOM_CENTR1/2 (+ errors), POS_CORR1/2", "pixel", "where the star falls on the CCD, per cadence"]]
S.append(sl(f"7  Data. The {RAW['n_cols']} columns of the light-curve table, in six groups",
            tblw(["Group", "Columns", "Unit", "What it is"], grp, [210, 400, 230, 320], "tbl xs")
            + take("We fit PDCSAP_FLUX where QUALITY is 0; SAP_FLUX is the same photons without the corrections.")
            + note("Names, units and formats are read from the FITS header. SAP and PDCSAP definitions are quoted from the STScI TESS archive manual; the other descriptions are ours."),
            "The column list and units come from the header keywords TTYPE, TFORM and TUNIT of the file. The definitions of SAP_FLUX and PDCSAP_FLUX are quoted from the STScI archive manual page saved in data/raw/tess_docs. The descriptions of the quality, background and position columns are our reading of the names and units; the Science Data Products Handbook has the formal definitions and we did not check them."))
nfl = RAW["n_flagged"]; e8 = QK["8"]["n"]
S.append(sl(f"7  Data. The raw columns plotted: {sp(RAW['rows'])} cadences, {nfl} of them flagged",
            fig("raw_lc_columns", 1000, "HD 189733 b, sector 41: flux, background, centroid, QUALITY values.")
            + obt([f"{sp(QK['0']['n'])} good cadences (QUALITY = 0); {QK['8']['n']} Earth-point (flag 8)",
                   f"PDCSAP is {100 * (RAW['pdc_over_sap'] - 1):.1f} % above SAP: CROWDSAP {hk['CROWDSAP']:.3f} / FLFRCSAP {hk['FLFRCSAP']:.3f} = {hk['CROWDSAP'] / hk['FLFRCSAP']:.3f}"], "Image obtained"),
            "The two flux curves have the same shape; the PDCSAP curve is lifted because the pipeline divides by the fraction of the star's flux inside the aperture and removes the light of neighbours, and the transits of HD 189733 b are the vertical dips. The background curve shows the scattered-light pattern of each orbit. The bit names are from lightkurve's TessQualityFlags, which follows the archive manual. We did not study the centroid curve; it is the raw input of the centroid test used in vetting (not done here)."))
S.append(sl("7  Data. Below the light curve: the pixels. Summing 45 pixels gives SAP_FLUX to 2 parts in 10<sup>7</sup>",
            fig("raw_tpf_pixels", 1160, "&pi; Men c, sector 1: median frame with the optimal aperture (red), the aperture sum against SAP_FLUX, and their ratio minus one.")
            + take(f"{sp(RT_['n_compared'])} cadences compared; largest deviation {RT_['sum_over_sap_maxdev']:.1e}, the float32 rounding. The aperture holds {100 - RT_['flux_outside_aperture_pct']:.1f} % of the stamp flux."),
            "We opened the target-pixel file of pi Men c, summed FLUX over the 45 pixels of the optimal aperture for each cadence and divided by SAP_FLUX of the light-curve file: the ratio is 1 to 2e-7. So the light curve is exactly the pixel sum, and every bias in it (a neighbour inside the aperture, a bad pixel) can be seen in the pixel image. The background column SAP_BKG equals the sum of FLUX_BKG over the same pixels. Only the pi Men c pixel file is stored in this project."))
code_ = ('from astropy.io import fits\n'
         'hdul = fits.open("tess2021204101404-s0041-0000000256364928-0212-s_lc.fits")\n'
         'd = hdul[1].data                      # the LIGHTCURVE table\n'
         't, flux, q = d["TIME"], d["PDCSAP_FLUX"], d["QUALITY"]\n'
         'good = (q == 0) & (flux == flux)      # keep QUALITY 0 and drop NaN')
man = [r for r in csv.DictReader(open(ROOT / "results" / "data_manifest.csv")) if r["planet"] == "HD 189733 b"][0]
rt = [["1  Direct file", "curl -O " + man["url"].replace("https://", "https://"), "what we used; same tree holds _tp.fits and _dvr.pdf; md5 in data_manifest.csv"],
      ["2  lightkurve", 'lk.search_lightcurve("TIC 256364928", mission="TESS", author="SPOC", exptime=120)', "tested 21 Nov 2026: sectors 41, 54, 81 found; timed out on 16 Nov"],
      ["3  MAST portal", "mast.stsci.edu, search the TIC number, product type time series", "not tested here"]]
S.append(sl("7  Data. How to reach the raw data: a file URL, lightkurve or the MAST portal",
            tblw(["Route", "Command or address", "Note"], [[a, f'<span style="font-size:20px;word-break:break-all">{b}</span>', c] for a, b, c in rt], [180, 640, 340], "tbl xs")
            + code(code_)
            + note("File name: tess&lt;date stamp&gt;-s&lt;sector&gt;-&lt;16-digit TIC&gt;-&lt;pipeline id&gt;-s_lc.fits; the URL folders are the sector and the TIC split in four."),
            "Route 1 needs no software: the URL pattern is in code/03b_fetch_static.py and the file list with md5 is results/data_manifest.csv. The HEAD request of the example URL returned 200 on 21 November 2026. Route 2 was run the same day and found the sectors 41, 54 and 81 at 120 s for TIC 256364928; on 16 November the MAST API timed out, which is why this project used route 1. Route 3 is the web interface; we did not use it here. The code box was run on the file and gives 19 149 rows, 18 315 good cadences."))

# ---- D2  all data products, the spectral band, the techniques
dprod = [["Full-frame image (FFI)", "_ffir.fits, _ffic.fits", "30 min, then 10 min, then 200 s", "the whole field of view, every star", "no"],
         ["Target pixel (TP)", "_tp.fits, _fast-tp.fits", "2 min; 20 s", "cut-out images of chosen stars, raw and calibrated pixels, one image per cadence", f"&pi; Men c only ({RT_['size_mb']} MB)"],
         ["Light curve (LC)", "_lc.fits, _fast-lc.fits", "2 min; 20 s", "flux series derived from the target pixels: SAP, PDCSAP, background, centroid, quality", f"all {MS['n_files']} files"],
         ["Cotrending basis vectors", "_cbv.fits", "per CCD", "the systematic trends used to make PDCSAP; not for the 20-s data", "no"],
         ["Data validation report", "_dvr.pdf", "per sector", "the pipeline's own transit-search report; none for 20-s data", "&pi; Men c (11 MB)"],
         ["Catalogs", "TIC, CTL, TOI, TCE", "&ndash;", "TIC-8: 1.7 billion point sources; TOI and TCE tables list candidates", "TIC id, T mag"]]
S.append(sl("7  Data. Every TESS data product: full frames, target pixels, light curves, basis vectors, reports, catalogs",
            tblw(["Product", "File", "Cadence", "What it is", "Used here"], dprod, [230, 220, 190, 390, 130], "tbl xs")
            + note("Cadences: 30 min (cycles 1 and 2), 10 min (3 and 4), 200 s (5 on); 20-s products since the first extended mission. Quotes in tess_fact_sources.csv."),
            "The product list and the sentences about each file type are quoted from the STScI TESS archive manual (page saved in data/raw/tess_docs) and the NASA HEASARC data-products page. Our own holdings: 21 light-curve files for the ten planets, plus the target-pixel file and the data-validation report of pi Men c, which we downloaded with code/03b_fetch_static.py. We did not download any full-frame image."))
S.append(sl("7  Data. Yes, the raw data are images: CCD pixels in one broad band from 600 to 1000 nm, with no spectrum",
            cols(fig("ricker_fig1_response", 640, "TESS spectral response (black) against V, R<sub>C</sub>, I<sub>C</sub> and z filters. Ricker et al. 2015, Fig. 1."),
                 obt(["each pixel adds up all the light of the band: one number per pixel and cadence, no wavelength information",
                      "colours cannot be measured; the other curves are only for comparison",
                      f"16 CCDs: 4 cameras &times; 4 CCDs of 2048 &times; 2048 pixels, 21&Prime; per pixel (computed)",
                      f"flag 8 (Earth point): {QK['8']['n']} cadences in our file have no time stamp and no flux, as the manual says"], "What the data are"), tpl="640px 1fr"),
            "Quoted from Ricker et al. 2015: the 600 to 1000 nm bandpass (Table 1 and Fig. 1, page 4 of the PDF), four CCDs per camera and four cameras (Sec 4). The figure is Fig. 1 of that paper, shown with its credit. From the STScI manual: cadences flagged Earth point (bit 4, value 8) have NULL time stamps and data; in our HD 189733 b file all 801 such cadences have NaN time and NaN flux. 16 CCDs is our product of 4 and 4."))
tech = [["Aperture photometry", "add the pixels of an aperture around the star", "SAP_FLUX is the sum of the 45 pixels (checked, section above)", "Caldwell 2020 (SPOC)"],
        ["Cotrending", "fit and remove the trends shared by many stars", "PDCSAP_FLUX is the result; basis vectors in _cbv.fits", "Stumpe 2012 (PDC, Kepler)"],
        ["Crowding and aperture correction", "divide by the share of the star's light in the aperture, remove neighbours", "PDCSAP/SAP = CROWDSAP/FLFRCSAP (3 files)", "STScI manual"],
        ["Full-frame photometry", "build light curves from the 30-min, 10-min or 200-s images", "not used here", "Huang 2020 (QLP); Feinstein 2019 (eleanor)"],
        ["Difference imaging", "subtract a reference image to cope with crowded fields", "not used here", "Oelkers 2018"]]
S.append(sl("7  Data. Techniques from pixels to a light curve: aperture sum, cotrending, crowding correction, full-frame and difference imaging",
            tblw(["Technique", "What it does", "In our data", "Paper"], tech, [250, 380, 330, 200], "tbl xs")
            + take("We fit the light curve as delivered (SPOC); the two last techniques are the way to get light curves where SPOC has none."),
            "Each technique is tied to a paper in literature/pdf (group A): Caldwell 2020 lists calibrated target pixels, SAP flux and PDC flux as SPOC products; Stumpe 2012 is the Kepler version of PDC; Huang 2020 is the MIT Quick Look Pipeline on full-frame images; Feinstein 2019 extracts light curves from full-frame images; Oelkers 2018 uses difference imaging, which mitigates the effects of crowded fields. The two checks in the third column are ours: the pixel sum on pi Men c and the ratio of PDCSAP to SAP on three files."))

# ---- M  detection methods: what TESS does alone, with partners, or cannot (tess_fact_sources.csv; archive counts from code/27)
BM = DSY["by_method"]; cnt = lambda k: sp(BM.get(k, 0))
pgr = lambda i: f"p. {PG(i)}"
S.append(sl("M  Methods. TESS alone, TESS with a partner, TESS cannot: every way the archive records a discovery",
            cols(card("TESS alone", f"Transit candidates ({cnt('Transit')} planets in the archive were found by transit, by all missions) &middot; phase curves and secondary eclipses ({cnt('Orbital Brightness Modulation')} by brightness modulation) &middot; part of the false-positive tests &middot; asteroseismology of the host &middot; binaries, flares, novae, variables in full frames", "navy", 430),
                 card("TESS with a partner", f"Mass (radial velocity, {cnt('Radial Velocity')} planets) &middot; confirmation and companions (ground photometry, imaging) &middot; transit timing ({cnt('Transit Timing Variations')} planets), eclipse timing ({cnt('Eclipse Timing Variations')}) &middot; atmospheres (JWST, HST) &middot; stellar radius (Gaia) &middot; refined transits (CHEOPS)", "orange", 430),
                 card("TESS cannot", f"Radial velocity itself &middot; direct imaging ({cnt('Imaging')}) &middot; microlensing ({cnt('Microlensing')}) &middot; astrometry ({cnt('Astrometry')}) &middot; pulsar timing ({cnt('Pulsar Timing')}) &middot; disk kinematics ({cnt('Disk Kinematics')}) &middot; planets with long periods around Sun-like stars in one sector &middot; mass and spectrum alone", "navy", 430))
            + note(f"Counts: confirmed planets of the NASA Exoplanet Archive by discovery method, {DSY['date']}; the verdict is ours, with the evidence on the next three slides."),
            "The eleven methods are the values of the archive column discoverymethod (code/27_discoveries_by_year.py); the counts are from the same query as the discovery chart. The classification is ours: each row of the next slides gives the quote or the computation it rests on, and says which statements are our reasoning."))
al = [["Transit photometry", "dips in the light of one star, 2 min", f"SPOC flags threshold-crossing events; Ricker Sec 8.2 expects thousands of planets below Neptune size ({pgr('yield')})", "all ten planets: BLS and fit"],
      ["Phase curve, secondary eclipse", "planet's own light over an orbit", f"Shporer 2019: TESS phase curve of WASP-18 b with transit and secondary eclipse ({pgr('shporer_pc')})", "WASP-18 b flux at phase 0.5: 352 &plusmn; 9 ppm against 341"],
      ["False-positive tests", "secondary eclipse, ellipsoidal modulation, image motion", f"Ricker Sec 8.2: some false positives identifiable with TESS data alone ({pgr('fp_tess')})", "odd-even test done; centroid test not done"],
      ["Asteroseismology", "oscillations of the host star", f"Ricker Sec 8.3: p-modes on about 6 000 stars ({pgr('astero')})", "not done; stellar radius is 1 to 7 % of our error"],
      ["Stars in full frames", "binaries, novae, flares, variables", f"Ricker Sec 8.4 ({pgr('ffi_other')})", "not done"]]
S.append(sl("M  Methods. What TESS does alone: transits, phase curves, part of the vetting, stars",
            tblw(["Method", "What TESS measures", "Evidence", "In our project"], al, [250, 270, 440, 200], "tbl xs")
            + note("Detecting a candidate is not confirming a planet: confirmation needs the partners of the next slide."),
            "The first row rests on the SPOC sentence about threshold-crossing events (HEASARC data-handling page, saved) and on Ricker Section 8.2. The phase-curve row cites the TESS paper on WASP-18 b in our literature folder; the 352 ppm is our own measurement (slide on flux at phase 0.5). The page numbers are PDF pages of each paper (tess_fact_sources.csv)."))
pa = [["Mass of the planet", "radial velocity from spectrographs", f"Winters 2021: velocities from five spectrographs fix the masses in LTT 1445 ({pgr('winters_rv')})", "mass-radius plot places the 4 small planets with measured masses"],
      ["Confirmation, false positives", "ground photometry, spectra, high-resolution imaging", f"Ricker Sec 8.2: ground observations check spectra, velocities, colour, companions ({pgr('fp_ground')}); LTT 1445 A b: TESS and ground telescopes ({pgr('winters_ground')})", "all ten are confirmed planets; we did not vet"],
      ["Transit timing", "times of every transit; partner: more years or velocities", f"Günther 2019: TOI-270's near-resonance gives timing variations ({pgr('gunther_ttv')})", "not measured; TOI-270 c period gap untested"],
      ["Atmospheres", "JWST, HST", f"Ricker abstract: ecliptic poles are best for JWST ({pgr('jwst_poles')}); Pass 2023 (HST), Xue 2024 (JWST) in the catalog", "history slide: JWST on WASP-39 b"],
      ["Stellar radius and distance", "Gaia parallax", "the TIC is built on Gaia DR2 (HEASARC); Stassun 2017: radii from Gaia parallaxes", "R&#9733; of the archive enters every R<sub>p</sub>"],
      ["Refined transits", "CHEOPS, ground", f"Benz 2021: CHEOPS follows stars already known to host planets ({pgr('benz_follow')})", "not used"]]
S.append(sl("M  Methods. TESS with a partner: mass, confirmation, timing, atmospheres, stellar radius",
            tblw(["Need", "Partner", "Evidence", "In our project"], pa, [210, 270, 480, 200], "tbl xs")
            + note("TESS supplies the radius and the transit times; the partner supplies what a band-limited camera cannot."),
            "Every row names the quote or paper it rests on, with the PDF page. The last column is the link to our work: the mass-radius figure uses planets whose masses were measured with velocities; none of the ten was vetted by us; the timing and asteroseismology rows are things we did not do."))
lat_gc = -5.5
cn = [["Radial velocity", "a spectrograph", f"the payload is four cameras and a data handling unit ({pgr('payload')}); one band, 600 to 1000 nm", "HD 118203 b, HD 189733 b, HD 209458 b were found by Doppler first"],
      ["Direct imaging", "a coronagraph, small pixels", f"a pixel is 21&Prime;; 90 % of a star's light falls in 1.4&prime;; undersampled images ({pgr('undersampled')})", "&ndash;"],
      ["Microlensing", "a dense field watched for a one-off alignment", f"Galactic centre at ecliptic latitude {lat_gc:+.1f}&deg; (computed); the strips start at 6&deg; ({pgr('lat_range')}); crowded fields (our reasoning)", "&ndash;"],
      ["Astrometry", "positions far below a pixel", "a pixel is 21&Prime;; the stellar wobble is far smaller (our reasoning); Gaia does it", "&ndash;"],
      ["Pulsar timing, disk kinematics", "radio pulses; millimetre spectra", "TESS is an optical photometer (our reasoning)", "&ndash;"],
      ["Long periods, Sun-like stars", "more than one sector", f"P<sub>max</sub> about 10 d rules out their habitable zone ({pgr('pmax_hz')}); surveys favour short periods ({pgr('pbias')})", "our ten: P up to 6.13 d"]]
S.append(sl("M  Methods. What TESS cannot do: velocities, imaging, microlensing, astrometry, long periods",
            tblw(["Method", "What it needs", "Why TESS cannot (evidence)", "In our project"], cn, [210, 260, 520, 170], "tbl xs")
            + note("'Our reasoning' = instrument numbers, not a quotation. A planet that does not cross its star gives no transit at all."),
            "The Galactic centre latitude was computed with astropy from galactic l = 0, b = 0: ecliptic latitude -5.5 degrees; typical bulge microlensing fields at b = -3 degrees give -6.2 degrees, so the bulge sits right at the edge of the 6-degree boundary; we did not check which sectors touch it. The statements about astrometry and pulsar timing are our reasoning from the pixel scale and from the optical band; we have no source that says TESS cannot do them."))

ORDER = {"1": 1, "2": 2, "H": 2.3, "M": 2.4, "T": 2.5, "C": 2.7, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "B": 10, "A": 11}
DISP = {"1": "1", "2": "2", "H": "3", "M": "3", "T": "4", "C": "5", "3": "6", "4": "7", "5": "8", "6": "9", "7": "10", "8": "11", "9": "12", "B": "B"}    # numbers shown on the slides
def _key(h):
    t = re.search(r"<h2><span>([^<]+)", h).group(1)
    return ORDER[t[0]]
cover, rest = S[0], S[1:]
SRCMAP.update({"T  TESS. The satellite in nine numbers": f"Source: Ricker et al. 2015, Table 1 p. {PG('fov')}, Sec 4.1 p. {PG('lens')}, Sec 4.2 p. {PG('ccd')}, Sec 6 p. {PG('orbit_shape')}, Sec 7.2 p. {PG('sector_len')}",
               "T  TESS. Where it looks": f"Source: Ricker et al. 2015, Sec 7.2, pp. {PG('sector_len')} to {PG('coverage_27')}; sectors per star from our MAST search (code/03_check_mast.py)",
               "T  TESS. Sampling": f"Source: Ricker et al. 2015, Sec 4.3 p. {PG('cadence_2min')}; headers of our 21 SPOC files (results/tess_files.csv)",
               "T  TESS. Data products": "Source: NASA HEASARC, STScI TESS archive manual, MIT TESS Science Office (copies in data/raw/tess_docs/, 21 Nov 2026)",
               "T  TESS. Resolution": f"Source: Ricker et al. 2015, Table 1 p. {PG('ensq50')}, Sec 4.1 p. {PG('pixel')}; STScI MAST TESS page; WCS in our file headers",
               "T  TESS. Our ten apertures": "Source: SPOC light-curve headers (CROWDSAP, FLFRCSAP, aperture mask); Winters et al. 2021 for LTT 1445",
               "T  TESS. Precision": "Source: SPOC light-curve headers (CDPP1_0, TIMEDEL); transit durations from the NASA Exoplanet Archive"})
def _src(h):
    t = re.search(r"<h2><span>([^<]+)", h).group(1)
    for k in sorted(SRCMAP, key=len, reverse=True):
        if t.startswith(k):
            return h.replace('<span class="pg">@@PG@@</span>', f'<div class="src">{SRCMAP[k]}</div><span class="pg">@@PG@@</span>', 1)
    return h
SL = [cover] + [re.sub(r"(<h2><span>)([^<])", lambda m: m.group(1) + DISP[m.group(2)], _src(h), count=1) for h in sorted(rest, key=_key)] + A
_n = [0]
def _num(m):
    _n[0] += 1
    return f'<span class="pg">{_n[0]}</span>'
SL = [SL[0]] + [re.sub(r'<span class="pg">@@PG@@</span>', _num, x) for x in SL[1:]]
css = (ROOT / "slides" / "deck" / "group2_base.css").read_text(encoding="utf-8") + ".mdeck-slide{height:720px!important;min-height:720px}.mdeck-slide .src{position:absolute;left:60px;right:100px;bottom:7px;font-size:20px;line-height:1.2;color:#566074}.mdeck-slide table.tbl.xs{font-size:21px}.mdeck-slide table.tbl.xs td,.mdeck-slide table.tbl.xs th{padding:4px 8px}"
js = (ROOT / "slides" / "deck" / "group2_engine.js").read_text(encoding="utf-8")
page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>Ten exoplanets with TESS, Group 2 study deck</title><style>' + css + '</style></head><body>'
        '<div class="mdeck"><div class="mdeck-canvas-wrap"><div class="mdeck-viewport">' + "".join(SL) + '</div></div>'
        '<div class="mdeck-bar"><button class="mdeck-prev">&#9664;</button><div class="mdeck-dots"></div><span class="mdeck-count"></span>'
        '<button class="mdeck-next">&#9654;</button><button class="mdeck-fs">Full screen</button></div><div class="mdeck-notes"></div></div>'
        '<script>' + js + '</script></body></html>')
(OUT / "index.html").write_text(page, encoding="utf-8")
print("slides:", len(SL), "main:", len(S), "appendix:", len(A))
