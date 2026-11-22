# -*- coding: utf-8 -*-
"""Bước 34 - Nguồn của các thông số trong các slide trả lời 'Check point 9h 22-11': đoạn nguyên văn trong PDF (kèm trang PDF) hoặc trang web đã lưu.
Một dòng chỉ verified=True khi đoạn nguyên văn tìm thấy đúng trong văn bản nguồn. Ra: data/literature/checkpoint_sources.csv. Không tải gì mới.
Chạy: .venv/bin/python code/34_checkpoint_sources.py"""
import csv
import glob
import html
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
LIT = ROOT / "literature" / "pdf"
fix = lambda t: re.sub(r"\s+", " ", t.replace("◦", "°").replace("−", "-").replace("–", "-").replace("’", "'").replace(" ", " ")).strip()


def pdf_pages(path):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout).group(1))
    return [fix(subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), path, "-"], capture_output=True, text=True).stdout) for i in range(1, n + 1)]


def web_text(name):
    t = open(ROOT / "data" / "raw" / "instrument_docs" / name, encoding="utf-8", errors="ignore").read()
    t = re.sub(r"(?s)<(script|style).*?</\1>", " ", t)
    return fix(html.unescape(re.sub(r"<[^>]+>", " ", t)))


one = lambda pat: glob.glob(str(LIT / pat))[0]
SRC = {
    "Ricker": (one("A_Mission_data/Ricker_2015_*.pdf"), "Ricker, G. R. et al. 2015, JATIS 1, 014003 (arXiv:1406.0151)"),
    "Koch": (one("K_Search_history/Koch_2010_*.pdf"), "Koch, D. G. et al. 2010, ApJL 713, L79 (Kepler mission design)"),
    "Rauer": (one("K_Search_history/Rauer_2014_*.pdf"), "Rauer, H. et al. 2014, Exp. Astron. 38, 249 (PLATO 2.0; 2014 design)"),
    "Akeson": (one("L_Instruments/arXiv_1902.05569.pdf"), "Akeson, R. et al. 2019, arXiv:1902.05569 (WFIRST overview)"),
    "Ivezic": (one("L_Instruments/arXiv_0805.2366.pdf"), "Ivezic, Z. et al. 2019, ApJ 873, 111 (LSST)"),
    "Gaia": (one("L_Instruments/arXiv_1609.04153.pdf"), "Gaia Collaboration, Prusti, T. et al. 2016, A&A 595, A1"),
    "Gardner": (one("K_Search_history/Gardner_2006_*.pdf"), "Gardner, J. P. et al. 2006, Space Sci. Rev. 123, 485 (JWST)"),
    "Marois": (one("K_Search_history/Marois_2008_*.pdf"), "Marois, C. et al. 2008, Science 322, 1348 (HR 8799)"),
    "Bowler": (one("L_Instruments/arXiv_1605.02731.pdf"), "Bowler, B. P. 2016, PASP 128, 102001 (imaging extrasolar giant planets)"),
    "Huber": (one("L_Instruments/arXiv_1109.3460.pdf"), "Huber, D. et al. 2011, ApJ 743, 143 (testing scaling relations)"),
    "Shporer": (one("J_Phase_curves_timing/Shporer_2019_*.pdf"), "Shporer, A. et al. 2019, AJ 157, 178 (WASP-18 b phase curve)"),
}
PAGES = {k: pdf_pages(v[0]) for k, v in SRC.items()}
WEB = {"jdox": ("jdox_nircam_detector.html", "STScI JWST User Documentation, NIRCam detector overview, saved 22 Nov 2026"),
       "esa": ("esa_plato_ariane6.html", "ESA, 'Planet hunter Plato to fly on Ariane 6', saved 22 Nov 2026"),
       "roman": ("nasa_roman_launch_blog.html", "NASA Roman blog, 'NASA's Roman Space Telescope launches', 30 Aug 2026, saved 22 Nov 2026")}
WT = {k: web_text(v[0]) for k, v in WEB.items()}

# (id, source key, topic, statement, value, location, quote)
F = [
    ("ffi_title", "Ricker", "Data", "Sec 8.4 of the TESS paper is titled 'Full Frame Images'", "8.4 Full Frame Images", "Sec 8.4", "8.4 Full Frame Images"),
    ("stamps_200k", "Ricker", "Data", "200 000 pre-selected stars are read at 2 min", "200 000", "Sec 8.4", "In addition to monitoring 200,000 pre-selected stars with a 2 min cadence"),
    ("ffi_any_star", "Ricker", "Data", "FFIs extend the transit search to any bright star in the field, selected or not", "any star in the field", "Sec 8.4", "The FFIs will expand the transit search to any star in the fields of view that is sufficiently bright, regardless of whether it was selected ahead of time"),
    ("ffi_followup", "Ricker", "Data", "FFI candidates can be given shorter cadence in an extended mission", "2 min later", "Sec 8.4", "could be selected for shorter-cadence observations during an extended mission"),
    ("ffi_other2", "Ricker", "Data", "FFIs also serve supernovae, GRB afterglows, AGN, asteroids, binaries, novae, flares, variables", "time-domain science", "Sec 8.4", "near-Earth asteroids, eclipsing and close binaries, novae, flaring stars, and other variable stars"),
    ("ffi_count", "Ricker", "Data", "Each 30-min FFI gives about a million bright objects; about 20 million over two years", "1e6 per FFI", "Sec 8.4", "for approximately 106 bright galaxies and stars"),
    ("ffi_20m", "Ricker", "Data", "About 20 million bright objects in the two-year survey", "20 million", "Sec 8.4", "approximately 20 million bright objects"),
    ("ccd_mosaic", "Ricker", "Cameras", "Four CCDs abutted give 4096 x 4096 pixels per camera", "4096 x 4096", "Sec 4.2", "creating an effective 4096 × 4096 imaging array"),
    ("camera_build", "Ricker", "Cameras", "Each camera: seven optical elements and four CCDs", "7 elements, 4 CCDs", "Sec 4", "a lens assembly with seven optical elements, and a detector assembly with four CCDs"),
    ("transit_prob", "Ricker", "Transit", "Geometric transit probability about 5 % and occurrence rate about 5 % give a 0.2 % yield", "5 % x 5 %", "Sec 3.5", "the product of the occurrence rate (∼5%) and the geometric transit probability (∼5%)"),
    ("stars_per_det", "Ricker", "Transit", "At least 500 stars must be monitored for each super-Earth detection", "500", "Sec 3.5", "TESS needs to monitor at least 500 stars for each super-Earth detection"),
    ("resp_curve", "Ricker", "Cameras", "TESS response = long-pass filter x detector quantum efficiency", "600 to 1000 nm", "Fig 1", "defined as the product of the long-pass filter transmission curve and the detector quantum efficiency curve"),
    ("kepler_plate", "Koch", "Kepler", "Kepler plate scale", "3.98 arcsec/pixel", "Table", "3.98 arcsec/pixel"),
    ("kepler_lc", "Koch", "Kepler", "Kepler long cadence", "1765.80 s", "Table", "1765.80 sec"),
    ("kepler_sc", "Koch", "Kepler", "Kepler short cadence", "58.86 s", "Table", "58.86 sec"),
    ("kepler_band", "Koch", "Kepler", "Kepler bandpass", "423 to 897 nm", "Sec 2", "423 to 897 nm"),
    ("kepler_fov", "Koch", "Kepler", "Kepler field of view", "115 sq. degrees", "Table", "115 sq. degrees"),
    ("plato_fov", "Rauer", "PLATO", "PLATO 2.0 (2014 design): field of view", "2232 deg2", "Abstract", "a wide field-of-view (2232 deg2)"),
    ("plato_tel", "Rauer", "PLATO", "PLATO 2.0 (2014 design): number of telescopes", "34", "Abstract", "34 small aperture telescopes"),
    ("plato_px", "Rauer", "PLATO", "PLATO 2.0 (2014 design): pixel scale", "15 arcsec/px", "Table", "15 arcsec/px"),
    ("plato_band", "Rauer", "PLATO", "PLATO 2.0 (2014 design): spectral range", "500-1000 nm", "Table", "500-1000 nm"),
    ("roman_fov", "Akeson", "Roman", "Roman WFI field of view", "0.281 deg2", "Abstract", "0.281 deg2 field of view"),
    ("roman_px", "Akeson", "Roman", "Roman WFI pixel scale", "0.11 arcsec", "Table", "Pixel scale: 0.11"),
    ("roman_mass", "Akeson", "Roman", "Roman is a 2.4 m telescope", "2.4 m", "Sec 1", "2.4m telescope"),
    ("roman_cad", "Akeson", "Roman", "Bulge microlensing survey: 15-min cadence", "15 min", "Sec 3", "minute cadence needed to detect Mars-mass planetary microlensing events"),
    ("roman_season", "Akeson", "Roman", "Bulge microlensing survey: seasons of 72 days", "72 d", "Sec 3", "seasons each lasting 72 days"),
    ("rubin_fov", "Ivezic", "Rubin", "Rubin field of view", "9.6 deg2", "Sec 1", "9.6 deg2 field of view"),
    ("rubin_px", "Ivezic", "Rubin", "Rubin pixel size", "0.2 arcsec", "Sec 3", "0.2×0.2 arcsec2 pixels"),
    ("rubin_visit", "Ivezic", "Rubin", "Rubin visit exposure", "30 s", "Sec 3", "visit exposure time of 30 seconds"),
    ("rubin_revisit", "Ivezic", "Rubin", "Rubin mean revisit", "3 days", "Sec 3", "A revisit time of 3 days on average"),
    ("rubin_band", "Ivezic", "Rubin", "Rubin wavelength range", "320-1050 nm", "Sec 1", "320-1050 nm"),
    ("gaia_px", "Gaia", "Gaia", "Gaia astrometric pixel", "58.9 mas x 176.8 mas", "Sec 3", "58.9 mas × 176.8 mas on the sky"),
    ("jwst_band", "Gardner", "JWST", "JWST mirrors give a bandpass of 0.6 to 29 um", "0.6 to 29 um", "Sec 3", "providing a broad spectral bandpass, from 0.6 to 29 µm"),
    ("jwst_coro", "Gardner", "JWST", "JWST makes coronagraphic images of nearby stars at 2.7 and 4.44 um", "2.7, 4.44 um", "Sec 7", "JWST will make coronagraphic images at 2.7 µm and 4.44 µm of nearby stars"),
    ("marois_challenge", "Marois", "Imaging", "Imaging is hard because of small separation and large contrast", "separation + contrast", "p. 1", "small angular separation and large luminosity contrast"),
    ("marois_dist", "Marois", "Imaging", "HR 8799 lies 39.4 pc from Earth", "39.4 pc", "p. 1", "located 39.4 pc"),
    ("marois_sep", "Marois", "Imaging", "A planet of HR 8799 at 68 AU projected separation", "68 AU", "p. 1", "68 AU projected separation"),
    ("bowler_young", "Bowler", "Imaging", "Young stars are the attractive targets for imaging planets", "young stars", "Sec 2", "Young stars are therefore attractive targets"),
    ("huber_sun", "Huber", "Asteroseismology", "Solar reference nu_max = 3090 uHz", "3090 +- 30 uHz", "Sec 2", "νmax,⊙ = 3090 ± 30µHz"),
    ("huber_dnu", "Huber", "Asteroseismology", "Solar reference large separation = 135.1 uHz", "135.1 +- 0.1 uHz", "Sec 2", "135.1 ± 0.1µHz"),
    ("shporer_albedo", "Shporer", "Phase curve", "WASP-18 b day side is dominated by thermal emission; albedo limit 0.048 (2 sigma)", "A_g < 0.048", "Abstract", "dominated by thermal emission, leading to an upper limit on the geometric albedo in the TESS band of 0.048 (2σ)"),
    ("shporer_341", "Shporer", "Phase curve", "WASP-18 b secondary eclipse depth", "341 +17 -18 ppm", "Sec 4", "We measure a secondary eclipse depth of 341+17"),
]
W = [("jdox_px", "jdox", "JWST", "NIRCam pixel scales", "0.031 and 0.063 arcsec", "Detector overview", '0.6-2.3 µm observations (0.031"/pixel) and two for 2.4-5.0 µm (0.063"/pixel)'),
     ("esa_cams", "esa", "PLATO", "PLATO uses 26 cameras on more than 200 000 stars", "26 cameras", "page text", "Plato will use 26 cameras to look at more than 200 000 stars"),
     ("esa_launch", "esa", "PLATO", "PLATO launch on Ariane 6, end of 2026 (ESA page; other ESA material says 2027)", "end of 2026", "page text", "French Guiana, end of 2026"),
     ("roman_launch", "roman", "Roman", "Roman launched on a Falcon Heavy from Launch Complex 39A, 30 Aug 2026", "30 Aug 2026", "blog text", "Launch Complex 39A")]
out = []
for i, key, topic, st, val, loc, q in F:
    path, cit = SRC[key]
    qq = fix(q)
    pg = next((n for n, t in enumerate(PAGES[key], 1) if qq in t), None)
    out.append(dict(id=i, topic=topic, statement=st, value=val, source=cit, location=loc, page=pg or "", quote=q, verified=pg is not None))
for i, key, topic, st, val, loc, q in W:
    name, cit = WEB[key]
    ok = fix(q) in WT[key]
    out.append(dict(id=i, topic=topic, statement=st, value=val, source=cit, location=loc, page="", quote=q, verified=ok))
with open(ROOT / "data" / "literature" / "checkpoint_sources.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
bad = [o["id"] for o in out if not o["verified"]]
print(len(out), "facts;", "NOT verified:", bad)
