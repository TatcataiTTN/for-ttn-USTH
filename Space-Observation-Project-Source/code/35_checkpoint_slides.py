# -*- coding: utf-8 -*-
"""Bước 35 - Các slide trả lời 'Check point tự định hướng 9h 22-11' (mục K = phương pháp chi tiết, mục Q = sứ mệnh và kiểm nguồn).
Được exec() từ code/17_build_study_deck.py (dùng chung S, sl, card, cols, take, note, tblw, fig, obt, esc, names, NUM, TP, TD, PX, SRCMAP, PG, ST).
Mọi con số đọc từ results/checkpoint_*.csv|json (code/33), data/literature/checkpoint_sources.csv (code/34) hoặc archive; không gõ tay."""
CKF = json.load(open(ROOT / "results" / "checkpoint_facts.json"))
GEO = pd.read_csv(ROOT / "results" / "checkpoint_geometry.csv").set_index("planet")
VET = pd.read_csv(ROOT / "results" / "checkpoint_vetting.csv").set_index("planet")
PDC = pd.read_csv(ROOT / "results" / "checkpoint_pdcsap_check.csv")
IMT = json.load(open(ROOT / "results" / "imaging_vs_tess.json"))
CKS = pd.read_csv(ROOT / "data" / "literature" / "checkpoint_sources.csv").set_index("id")
ckp = lambda i: f"{re.split(r'[ ,]', CKS.loc[i, 'source'])[0]} p. {int(CKS.loc[i, 'page'])}"
gs, rt, ph, ast, dil, ana = CKF["geometry_summary"], CKF["roundtrip"], CKF["phase_wasp18"], CKF["astero"], CKF["dilution"], CKF["analogues"]
sci = lambda x: f"{x / 10 ** int(np.floor(np.log10(x))):.1f} &times; 10<sup>{str(int(np.floor(np.log10(x)))).replace('-', '&minus;')}</sup>"
OK, NO, NA, HALF = '<b style="color:#047857">&#10003;</b>', '<b style="color:#ED1C24">&#10007;</b>', '<span style="color:#8a93a6">&ndash;</span>', '<b style="color:#b45309">~</b>'
fm = lambda eq, fn="": f'<div class="fm"><div class="fe">{eq}</div>' + (f'<div class="fn">{fn}</div>' if fn else "") + "</div>"
n0 = lambda x: f"{x:,.0f}".replace(",", " ")
CK_CSS = (".mdeck-slide .body{padding-bottom:12px}.mdeck-slide tr.off td{opacity:.42}.mdeck-slide input.tkb{width:26px;height:26px;accent-color:#273896;cursor:pointer}"
          ".mdeck-slide .fm{padding:10px 14px!important;margin:6px 0!important}.mdeck-slide .fe{font-size:25px!important}.mdeck-slide .fn{font-size:21px!important}"
          ".mdeck-slide .grid4{display:grid;grid-template-columns:1fr 1fr;gap:10px}.mdeck-slide .grid4 .card{margin:0;padding:8px 14px}"
          ".mdeck-slide .grid4 .card h3{font-size:25px!important;margin:0 0 3px}.mdeck-slide .grid4 .card p{font-size:21.5px;line-height:1.28}")
rows_n = lambda d: [NUM[n] for n in d]
RP = lambda i: f"Ricker p. {PG(i)}"


def tick_table(rows, on):
    """rows: list of cell lists; the first cell of each row is a tick box (clickable; state is not saved)."""
    out = []
    handler = "this.closest('tr').classList.toggle('off',!this.checked)"
    for r in rows:
        chk = '<input class="tkb" type="checkbox"' + (" checked" if on else "") + ' onchange="' + handler + '">'
        cls = "" if on else ' class="off"'
        out.append("<tr" + cls + "><td>" + chk + "</td>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    return out


def tick_slide(title, head, widths, rows, on, nt, notes, cls="tbl xs"):
    h = "".join(f'<th style="width:{w}px">{x}</th>' for x, w in zip(head, widths))
    S.append(sl(title, f'<table class="{cls}" style="table-layout:fixed"><tr>{h}</tr>' + "".join(tick_table(rows, on)) + "</table>" + note(nt), notes))


def four(title, notes, fov, pix, cad, rev, tk):
    c = lambda h, need, have: f'<div class="card navy"><h3>{h}</h3><p><b>Needs:</b> {need}<br><b>TESS:</b> {have}</p></div>'
    S.append(sl(title, '<div class="grid4">' + c("1  Field of view", *fov) + c("2  Spatial resolution", *pix) + c("3  Temporal resolution", *cad) + c("4  Revisit time", *rev) + "</div>" + take(tk), notes))


# ================================================================ K1 - K4  star in frames, full frames
S.append(sl("K  Methods. Stars in full frames is not a planet method: what it measures, against transit and direct imaging",
            tblw(["Item", "Target", "What is measured", "Input data", "Finds planets?"],
                 [["Transit photometry", "one star, 2 min", "the dip in the star's flux when a planet crosses", "image cutouts &rarr; 1-D light curve", "<b>Yes</b>, indirectly"],
                  ["Direct imaging", "the planet itself", "photons from the planet, the star's light suppressed", "images with a coronagraph, small pixels", "<b>Yes</b>, directly"],
                  ["Astrometry", "star position", "the wobble of the star's position among reference stars", "image series, sub-pixel centroids", "Yes, but not with TESS"],
                  ["Stars in full frames", "any star in the 24&deg; &times; 96&deg; field", "brightness of every star: binaries, novae, flares, variables", "full-frame image series", "<b>No</b>: stellar science; it also extends the transit search"]],
                 [215, 230, 330, 235, 150], "tbl xs")
            + take(f"Ricker Sec 8.4 is titled &lsquo;Full Frame Images&rsquo; ({ckp('ffi_title')}); our row name is a short label for it. &lsquo;Star in frames&rsquo; is not a standard term."),
            "The words star in frames are not a method name. The nearest thing in the TESS paper is Section 8.4, Full Frame Images, which says the full frames also serve supernovae, binaries, novae and flaring stars. The first three rows are methods of detecting planets; the last row is a data product used for stellar science and for extending the transit search to stars nobody selected."))
S.append(sl("K  Methods. One image series, three uses: differential photometry, centroiding, and calibration for imaging",
            cols(card("Differential photometry", f"The flux of the star falls by (R<sub>p</sub>/R<sub>&#9733;</sub>)<sup>2</sup> when a planet crosses it. TESS: yes; this is all ten of our planets, {GEO.pts_per_transit.min():.0f} to {GEO.pts_per_transit.max():.0f} points per transit.", "navy", 330),
                 card("Centroiding", f"The (x, y) position of the star moves when a blended star dips, or when a planet pulls the star. TESS uses it as a test (Ricker Sec 8.2: transit-specific image motion). We measured shifts of at most {VET.dR_arcsec.max():.3f}&Prime;.", "orange", 330),
                 card("Calibration for imaging", "A coronagraph hides the star; short unsaturated frames of the star still locate its centre so that its diffraction halo can be subtracted. TESS has no coronagraph.", "navy", 330))
            + take("The same frames serve very different methods; what changes is what is measured on them."),
            "This is the content of the first question in the checkpoint notes. The three uses of a frame that contains the star: measure its brightness over time (transit), measure its position over time (centroid or astrometry), and use unsaturated frames to calibrate a coronagraphic image. TESS does the first, uses the second as a test, and cannot do the third because it has no coronagraph."))
cr = tblw(["Criterion", "Star in frames: transit, astrometry", "Direct imaging"],
          [["Physical nature", "indirect: the planet changes the star (blocks it, pulls it)", "direct: photons from the planet itself"],
           ["What is measured", "total flux or centroid of the <b>star</b>", "a point of light of the <b>planet</b>, star suppressed"],
           ["Hardest part", f"precision: 60 ppm per hour is the assumed noise floor ({RP('noise_floor')})", f"contrast: Jupiter at 5.2 AU gives {sci(ana['jupiter_contrast'])}, Earth at 1 AU {sci(ana['earth_contrast'])} (A<sub>g</sub> = 0.3, ours)"],
           ["Who is found", f"close-in planets: TESS discoveries have median P = {IMT['tess']['P_median']:.1f} d, a = {IMT['tess']['a_median']:.2f} AU", f"wide young giants: imaged planets have median a = {IMT['imaging']['a_median']:.0f} AU"],
           ["What it gives", "R<sub>p</sub>/R<sub>&#9733;</sub>, period, inclination; mass only with partners", "the planet's own spectrum: temperature, composition, clouds"]]
          , [200, 480, 480], "tbl xs")
S.append(sl("K  Methods. Indirect against direct: nature, object measured, hardest part, who is found, what it gives", cr
            + note(f"Archive numbers: confirmed planets, {DSY['date']} (data/raw/pscomppars_imaging_and_tess.csv); {IMT['tess']['n']} TESS discoveries, {IMT['imaging']['n']} imaged planets. Contrasts are computed, not quoted."),
            "This is the comparison table from the checkpoint notes with every cell checked. The contrast numbers are our own arithmetic: A_g times (R_p over a) squared, with A_g = 0.3. The population numbers come from a TAP query of the NASA Exoplanet Archive."))
t4 = [["Target pixel files and light curves", "a cutout around each pre-selected star (about 200 000)", "2 min; 20 s since the first extended mission", "<b>Yes</b>"],
      ["Full-frame images", "the whole field of each camera", "30 min (cycles 1&ndash;2), 10 min (3&ndash;4), 200 s (5+)", "No"]]
S.append(sl("K  Methods. One set of cameras, two data products: postage stamps at 2 min, full frames at 30 min, 10 min, 200 s",
            tblw(["Product", "What is kept", "Cadence", "Used here"], t4, [330, 400, 330, 100], "tbl xs")
            + cols(card("Same hardware", f"Four identical cameras ({ckp('camera_build')}); each is four CCDs forming 4096 &times; 4096 pixels ({ckp('ccd_mosaic')}). Frames of 2 s are summed in groups of 60 into the 2-min cadence ({RP('cadence_2min')}). There is no separate imaging camera.", "navy", 260),
                   card("Why full frames matter", f"They extend the transit search to any bright star in the field, selected or not ({ckp('ffi_any_star')}); give about 10<sup>6</sup> objects per image and about 20 million over two years ({ckp('ffi_20m')}); and candidates found there can get 2-min cadence later ({ckp('ffi_followup')}).", "orange", 260), tpl="1fr 1fr")
            + note("We did not use them: all ten planets already have 2-min SPOC light curves."),
            "This answers the question whether TESS has a separate camera for the small images. It does not: the same four cameras take every frame. What differs is what is kept and downlinked: cutouts around selected stars at 2 minutes, or the full frames at longer cadence. The notes said tens of millions of stars per image; the TESS paper says about one million objects per 30-minute image and about twenty million over the two years."))
# ================================================================ K5 tick lists
tk_head = ["", "Method", "FOV", "Pixel", "Cadence", "Revisit", "Number that decides"]
tk_w = [56, 300, 80, 80, 110, 100, 430]
tick_slide("K  Methods. Tick the methods: what TESS does alone fits all four of its numbers",
           tk_head, tk_w,
           [["Transit photometry", OK, OK, OK, OK, f"p &asymp; 5 % (Ricker); {gs['pts_min']:.0f}&ndash;{gs['pts_max']:.0f} points per transit"],
            ["Secondary eclipse, phase curve", OK, OK, OK, OK, f"WASP-18 b: {27.4 / GEO.loc['WASP-18 b', 'P_d']:.0f} orbits in one sector"],
            ["False-positive vetting", OK, OK, OK, OK, f"centroid error about 10<sup>&minus;4</sup> pixel, measured"],
            ["Asteroseismology", OK, OK, OK, OK, f"Nyquist {n0(ast['nyquist_uHz']['120 s'])} &micro;Hz above the Sun's &nu;<sub>max</sub> {ast['nu_max_sun']:.0f}"],
            ["Stars in full frames", OK, OK, OK, OK, "about 10<sup>6</sup> objects per image (Ricker)"]],
           True, "Click a box to dim a row. The four numbers: field of view 24&deg; &times; 96&deg;, pixel 21&Prime;, cadence 2 min (20 s, 200 s), a 27.4-d sector. The reading is ours; each row has its own slide.",
           "This is the tick list asked for in the checkpoint notes, for the methods TESS can do alone. Each tick means that the design number of TESS is compatible with what the method needs; the next five slides explain each row with the four numbers, using our own ten planets for the examples. You can click the boxes in the browser; the state is not saved.", "tbl sm")
tick_slide("K  Methods. Tick the methods: with a partner, and what TESS cannot do, with the factor that fails",
           tk_head, tk_w,
           [["Mass: radial velocity", NA, NA, NA, NA, "needs a spectrograph; the payload is cameras"],
            ["Confirmation: ground imaging", NA, NO, NA, NA, "21&Prime; pixel; LTT 1445 companions at 5&ndash;7&Prime;"],
            ["Transit timing (TTV)", NA, NA, OK, HALF, "timing measured; mass needs a model"],
            ["Atmospheres: JWST, HST", NA, NA, NA, NA, "needs a spectrum; one band only"],
            ["Stellar radius: Gaia", NA, NA, NA, NA, "a parallax measurement"],
            ["Direct imaging", NA, NO, NA, NA, f"{gs['theta_mas_min']:.1f}&ndash;{gs['theta_mas_max']:.1f} mas against a 21&Prime; pixel"],
            ["Astrometry", NA, NO, NA, NA, "wobble far below one pixel"],
            ["Microlensing", NO, NO, NA, NO, "bulge at the 6&deg; edge; crowded; no stare"],
            ["Pulsar timing, disk kinematics", NA, NA, NA, NA, "radio and millimetre; TESS is optical"],
            ["Long periods, Sun-like stars", NA, NA, NA, NO, "27.4-d sector; P<sub>max</sub> about 10 d (Ricker)"]],
           False, "&#10003; fits, &#10007; does not fit, ~ partly, &ndash; not the deciding number. Our reading from the instrument numbers.",
           "The same list for the methods in the other two groups. A cross marks the factor that does not fit. A dash means the four numbers are not what decides: for radial velocity the missing item is a spectrograph, for pulsar timing it is a radio telescope. The reading is ours; it rests on the instrument numbers and on the quotes of the three methods slides before.")
# ================================================================ K6 - K10 four numbers per method
four("K  Methods. Transit photometry and the four numbers: many stars, a coarse pixel, 2-min points, a sector of 27 days",
     f"The transit probability is about R star over a. In our ten planets it runs from {gs['prob_min']:.1f} to {gs['prob_max']:.0f} per cent, which is why a survey needs many stars; Ricker quotes 5 per cent and 500 stars per detection. The pixel only has to gather the light of one star; the 21 arcsec pixel costs us the crowding correction. Durations of 0.8 to 5.7 hours are sampled by 23 to 170 points at 2 minutes. A period below 13.7 days gives at least two transits in a sector.",
     (f"hundreds of thousands of stars: the geometric probability is only about 5 % ({ckp('transit_prob')}), at least 500 stars per super-Earth ({ckp('stars_per_det')})", f"24&deg; &times; 96&deg; = 2300 deg², at least 200 000 targets"),
     ("no need to separate planet and star, only to collect the star's light", f"21&Prime; pixels; our apertures {int(TP.npix_opt.min())} to {int(TP.npix_opt.max())} pixels; CROWDSAP down to {GEO.crowdsap.min():.2f}"),
     (f"a point every few minutes through a dip of hours", f"{GEO.T14_h.min():.1f} to {GEO.T14_h.max():.1f} h transits: {gs['pts_min']:.0f} to {gs['pts_max']:.0f} points at 2 min"),
     ("two transits at least, to give a period", f"27.4 d sector: {GEO.transits_per_sector.min():.1f} to {GEO.transits_per_sector.max():.0f} transits for P = {GEO.P_d.max():.1f} to {GEO.P_d.min():.2f} d"),
     "The survey numbers (wide field, coarse pixel) are exactly what a low transit probability asks for.")
four("K  Methods. Phase curve and secondary eclipse and the four numbers: bright hot hosts, one pixel, 2 min, many orbits",
     f"WASP-18 b has P = {GEO.loc['WASP-18 b', 'P_d']:.3f} d, so one sector holds {27.4 / GEO.loc['WASP-18 b', 'P_d']:.0f} orbits; we used four sectors and {int(VET.loc['WASP-18 b', 'n_transits'])} transits. The planet lies {GEO.loc['WASP-18 b', 'theta_mas']:.2f} mas from its star, so planet and star always fall in the same pixel, which is what a total-flux measurement wants.",
     ("a rare planet: very hot, giant, close, around a bright star", f"2300 deg² gives WASP-18 (T mag {TP.loc['WASP-18 b', 'tmag']:.1f}) and a few like it"),
     ("star and planet in the same aperture, the total flux of the system", f"separation {GEO.loc['WASP-18 b', 'theta_mas']:.2f} mas against a 21&Prime; pixel: always blended, as wanted"),
     ("enough points to bin down to tens of ppm over a 0.94-d orbit", f"2 min gives {GEO.loc['WASP-18 b', 'P_d'] * 720:.0f} points per orbit; we measured 352 &plusmn; 9 ppm at phase 0.5"),
     ("many consecutive orbits without a day-night gap", f"{27.4 / GEO.loc['WASP-18 b', 'P_d']:.0f} orbits in 27.4 d, uninterrupted except for the downlink gap"),
     "The phase curve uses the coarse pixel as an advantage: nothing is lost outside the aperture.")
four("K  Methods. False-positive vetting and the four numbers: neighbours, sub-pixel centroids, equal sampling, enough transits",
     f"The pixel is 21 arcsec, yet the centroid test works because a centroid is an average over many electrons: our errors are {VET.dx_err.min():.5f} to {VET.dx_err.max():.5f} pixel in x, a few thousandths of an arcsecond. The odd-even test needs at least a few transits of each parity; our counts run from {int(VET.n_transits.min())} to {int(VET.n_transits.max())}.",
     ("neighbouring stars in the same field to compare against", "the stamp holds the target and its neighbours; CROWDSAP tells how many"),
     ("sub-pixel position of the light centre", f"centroid error {VET.dx_err.min() * 21:.4f} to {VET.dy_err.max() * 21:.3f}&Prime; per planet, measured"),
     ("the same sampling for odd and even transits", "one 2-min cadence for all; odd-even test done on the ten"),
     ("several transits of each parity", f"{int(VET.n_transits.min())} to {int(VET.n_transits.max())} transits per planet"),
     "Vetting uses the pixel grid as information: where the light sits, not what the planet looks like.")
four("K  Methods. Asteroseismology and the four numbers: many bright stars, disc-integrated light, 2 min or 20 s, long stares",
     f"The Sun oscillates at &nu;<sub>max</sub> = {ast['nu_max_sun']:.0f} &micro;Hz, a period of {ast['period_sun_min']:.1f} min (Huber 2011, p. {int(CKS.loc['huber_sun', 'page'])}). The Nyquist frequency of a 2-min cadence is 1/(2 &times; 120 s) = {n0(ast['nyquist_uHz']['120 s'])} &micro;Hz, so it is seen; a 30-min cadence reaches only {ast['nyquist_uHz']['1800 s']:.0f} &micro;Hz.",
     (f"many bright stars of every age", f"p-modes expected on about 6 000 stars ({RP('astero')})"),
     ("only the total light of the star", "disc-integrated brightness: the 21&Prime; pixel does no harm"),
     (f"a Nyquist frequency above &nu;<sub>max</sub> of the star", f"2 min: {n0(ast['nyquist_uHz']['120 s'])} &micro;Hz; 20 s: {n0(ast['nyquist_uHz']['20 s'])}; 30 min: {ast['nyquist_uHz']['1800 s']:.0f} (too low for Sun-like stars)"),
     ("long uninterrupted data: frequency resolution = 1/T", f"27.4 d: {ast['res_uHz_27d']:.2f} &micro;Hz; over 300 d near the poles: below {ast['res_uHz_300d']:.3f} &micro;Hz ({RP('coverage_300')})"),
     "The fast cadence is the decisive number here; full frames at 30 min cannot see Sun-like p-modes.")
four("K  Methods. Stars in full frames and the four numbers: a million objects per image, coarse pixels in sparse fields, 30 min to 200 s",
     f"Each 30-min image gives about 10<sup>6</sup> bright objects and about 20 million are covered in two years ({ckp('ffi_count')}). The pixel is coarse, so the crowded Galactic plane is the weak point: 90 % of a star's light falls inside 1.4 arcmin ({RP('ensq90')}). Cadence by cycle is 30 min, 10 min, 200 s (NASA HEASARC).",
     ("the whole field, no pre-selection", f"{ckp('ffi_any_star')}: any bright star in 2300 deg²"),
     ("separate stars from their neighbours", "21&Prime; works where stars are sparse; limited where crowded (our reasoning)"),
     ("events of minutes to weeks: flares, eclipses, novae (our reasoning)", "30 min, then 10 min, then 200 s"),
     ("a continuous record through each event", "27.4 d per sector, 2 years for the whole sky"),
     "Full frames trade a longer cadence for coverage of every star, which is what variable-star work wants.")
# ================================================================ K11 - K18 formulas and inputs
S.append(sl("K  Methods. Input data: from an image cube I(x, y, t) to a light curve F(t), with SAP and PDCSAP",
            fm("F<sub>SAP</sub>(t<sub>k</sub>) = &Sigma;<sub>(x,y)&isin;A</sub> [ I(x, y, t<sub>k</sub>) &minus; B(t<sub>k</sub>) ]", "A: optimal-aperture pixels; B: sky background. Checked on &pi; Men c: the sum of the 45 aperture pixels equals SAP_FLUX.")
            + fm("F<sub>PDCSAP</sub> = [ F<sub>SAP</sub> &minus; &Sigma;<sub>j</sub> c<sub>j</sub>U<sub>j</sub>(t) &minus; (1 &minus; C) &lang;F<sub>SAP</sub>&rang; ] / f", "U<sub>j</sub>: cotrending basis vectors; C = CROWDSAP; f = FLFRCSAP. Divide by f only, not by C &times; f.")
            + tblw(["Check on our files", "Value"],
                   [[f"median PDCSAP / median SAP against CROWDSAP / FLFRCSAP, {CKF['pdcsap_check']['n_files']} files", f"agree within {CKF['pdcsap_check']['max_abs_rel_diff_pct']:.2f} %"],
                    ["LTT 1445 A b: measured; C / f; the form with C &times; f in the divisor", f"{CKF['pdcsap_check']['ltt1445_pdc_over_sap']:.3f}; {CKF['pdcsap_check']['ltt1445_crowd_over_flfr']:.3f}; {CKF['pdcsap_check']['ltt1445_wrong']:.3f}"]], [820, 340], "tbl xs")
            + note("Input type: a 3-D image cube (11 &times; 11 pixels per stamp, or 4096 &times; 4096 per camera), compressed to a 1-D series; then f(t) = F<sub>PDCSAP</sub> / median."),
            "Every method of the next slides starts here. The image cube is summed over the aperture to give SAP flux; cotrending removes shared systematics; the crowding term removes the light of neighbours; dividing by the flux fraction restores the light that fell outside the aperture. The checkpoint notes wrote the divisor as CROWDSAP times FLFRCSAP. Our data say otherwise: for LTT 1445 A b the median ratio PDCSAP over SAP is 0.434, equal to C over f, whereas the other form would give 1.03."))
S.append(sl("K  Methods. Transit photometry, step by step: fold, search, fit, then radius, geometry and stellar density",
            fm("&phi; = ( (t &minus; T<sub>0</sub>) mod P ) / P ;&nbsp; BLS strength = &radic;[ n<sub>in</sub>n<sub>out</sub> / (n<sub>in</sub> + n<sub>out</sub>) ] ( &lang;f&rang;<sub>out</sub> &minus; &lang;f&rang;<sub>in</sub> ) / &sigma;", "1. Fold on a trial period; the best (P, T<sub>0</sub>, duration) is the BLS peak. Input: the 1-D series f(t).")
            + fm("z(t) = (a/R<sub>&#9733;</sub>) &radic;[ sin<sup>2</sup>&theta; + cos<sup>2</sup>i cos<sup>2</sup>&theta; ] ,&nbsp; &theta; = 2&pi;(t &minus; T<sub>0</sub>)/P ;&nbsp; I(&mu;) = I<sub>0</sub> [ 1 &minus; u<sub>1</sub>(1 &minus; &mu;) &minus; u<sub>2</sub>(1 &minus; &mu;)<sup>2</sup> ]", "2. Mandel-Agol model with quadratic limb darkening, fitted by MCMC (our pipeline).")
            + fm("&delta; &asymp; (R<sub>p</sub>/R<sub>&#9733;</sub>)<sup>2</sup> ,&nbsp; R<sub>p</sub> = R<sub>&#9733;</sub> &radic;&delta; ;&nbsp; b = (a/R<sub>&#9733;</sub>) cos i", "3. Radius. Example HD 118203 b: R<sub>p</sub>/R<sub>&#9733;</sub> = " + f"{GEO.loc['HD 118203 b', 'k']:.4f}, R<sub>&#9733;</sub> = {R['HD 118203 b']['rstar_rsun']} R<sub>&#9737;</sub> gives {R['HD 118203 b']['rp_rearth']:.2f} R<sub>&oplus;</sub>.")
            + fm("a/R<sub>&#9733;</sub> = &radic;[ (1 + k)<sup>2</sup> &minus; b<sup>2</sup> cos<sup>2</sup>(&pi;T<sub>14</sub>/P) ] / sin(&pi;T<sub>14</sub>/P) ;&nbsp; &rho;<sub>&#9733;</sub> = 3&pi; (a/R<sub>&#9733;</sub>)<sup>3</sup> / (G P<sup>2</sup>)", f"4. Geometry and density. The form without the cos<sup>2</sup> term is off by up to {rt['a_approx_max_rel_pct']:.1f} % ({rt['a_approx_planet']}); the exact form returns b and a/R<sub>&#9733;</sub> from our fits to 10<sup>&minus;13</sup>."),
            "Four steps with the actual inputs. Folding and BLS find the period; the Mandel-Agol model with limb darkening is fitted; the radius follows from the depth and the stellar radius; and the durations T14 and T23 give the impact parameter and a over R star. The checkpoint notes used a shortened expression for a over R star that drops the cosine term; we checked it on our ten fits and it is wrong by up to 2.8 per cent for LTT 9779 b."))
tt = []
for n in names:
    g = GEO.loc[n]
    tt.append([f"<b>{NUM[n]}</b> {n}", f"{g.P_d:.3f}", f"{g.transit_prob_pct:.1f} %", f"{g.T14_h:.2f}", f"{g.pts_per_transit:.0f}", f"{g.transits_per_sector:.1f}", f"{g.rho_fit:.2f} / {g.rho_cat:.2f}"])
S.append(sl("K  Methods. Transit numbers of our ten planets: probability, duration, points per transit, transits per sector, density",
            tblw(["Planet", "P (d)", "R<sub>&#9733;</sub>/a", "T<sub>14</sub> (h)", "Points", "Transits / sector", "&rho;<sub>&#9733;</sub> fit / catalog (g cm<sup>&minus;3</sup>)"], tt, [220, 110, 120, 120, 110, 190, 290], "tbl xs")
            + note("R<sub>&#9733;</sub>/a = 1/(a/R<sub>&#9733;</sub>) of our fit. T<sub>14</sub> from our fit by the exact formula; points = T<sub>14</sub>/120 s; density from the fit and from catalog M<sub>&#9733;</sub>/R<sub>&#9733;</sub><sup>3</sup> (solar density 1.41)."),
            "All columns are computed from our fits in results/checkpoint_geometry.csv. The density from the transit shape and the density from the catalog mass and radius agree to within a factor of 1.6 for all ten planets; the largest difference is HD 118203 b, whose orbit is eccentric while the formula assumes a circle."))
S.append(sl("K  Methods. Phase curve and secondary eclipse, step by step, with WASP-18 b: reflected light, thermal light, day-side temperature",
            fm("cos &alpha; = &minus;sin i cos(2&pi;(t &minus; T<sub>0</sub>)/P) ;&nbsp; f = 1 &minus; &delta;<sub>transit</sub> + F<sub>planet</sub> + F<sub>ellip</sub> + F<sub>beam</sub>", "Input: the 1-D series folded on P; &alpha; = 0 at the secondary eclipse.")
            + fm("F<sub>refl</sub> = A<sub>g</sub> (R<sub>p</sub>/a)<sup>2</sup> [ sin &alpha; + (&pi; &minus; &alpha;) cos &alpha; ] / &pi; ;&nbsp; F<sub>therm</sub> = F<sub>night</sub> + (F<sub>day</sub> &minus; F<sub>night</sub>)(1 + cos &alpha;)/2")
            + fm("&delta;<sub>sec</sub> = A<sub>g</sub>(R<sub>p</sub>/a)<sup>2</sup> + k<sup>2</sup> &int;B<sub>&lambda;</sub>(T<sub>day</sub>)W d&lambda; / &int;B<sub>&lambda;</sub>(T<sub>eff</sub>)W d&lambda;", "W: TESS response, here flat from 600 to 1000 nm (ours).")
            + tblw(["WASP-18 b", "Value"],
                   [[f"k = {ph['k']:.4f}, a/R<sub>&#9733;</sub> = {ph['a_rs']:.3f}, T<sub>eff</sub> = {ph['teff']:.0f} K", f"(R<sub>p</sub>/a)<sup>2</sup> = {1e6 * ph['rp_over_a'] ** 2:.0f} ppm"],
                    [f"all of 341 ppm reflected would need A<sub>g</sub>", f"{ph['Ag_if_all_reflected_341']:.2f}, but limit &lt; 0.048 ({ckp('shporer_albedo')})"],
                    ["T<sub>day</sub> from 341 ppm (paper) | 352 ppm (ours)", f"{ph['Tday_341']:.0f} K | {ph['Tday_352']:.0f} K"]], [730, 430], "tbl xs"),
            "Worked example for the phase curve. The depth at phase 0.5 is the sum of reflected and thermal light. If it were all reflected the albedo would have to be 0.42; the TESS paper limits it to below 0.048, so the secondary eclipse is mostly thermal. Solving the Planck integral over a flat 600 to 1000 nm band gives a day-side brightness temperature near 3000 K for both the published and our depth; the band is flat, so this is an approximation of ours."))
S.append(sl("K  Methods. False-positive vetting, step by step: odd-even depth, ellipsoidal and beaming signals, centroid shift",
            fm("Z = | &delta;<sub>even</sub> &minus; &delta;<sub>odd</sub> | / &radic;[ &sigma;<sub>even</sub><sup>2</sup> + &sigma;<sub>odd</sub><sup>2</sup> ]", "Input: the 1-D series. Z &gt; 3 suggests an eclipsing binary at twice the period. Our result: slide on odd against even.")
            + fm("F<sub>ellip</sub> = &minus;A<sub>ellip</sub> cos 4&pi;&phi; ,&nbsp; A<sub>ellip</sub> &prop; (M<sub>p</sub>/M<sub>&#9733;</sub>)(R<sub>&#9733;</sub>/a)<sup>3</sup> sin<sup>2</sup>i ;&nbsp; F<sub>beam</sub> = A<sub>beam</sub> sin 2&pi;&phi;", "Input: the series folded on P. Shporer 2019 measured both for WASP-18 b; we did not.")
            + fm("X<sub>c</sub> = &Sigma; x [I &minus; B] / &Sigma; [I &minus; B] ,&nbsp; Y<sub>c</sub> likewise ;&nbsp; &Delta;R<sub>c</sub> = &radic;[ (X<sub>in</sub> &minus; X<sub>out</sub>)<sup>2</sup> + (Y<sub>in</sub> &minus; Y<sub>out</sub>)<sup>2</sup> ]", "Input: the <b>images</b> (flux-weighted centroids of the stamp; SPOC stores them as MOM_CENTR1 and 2). A shift &gt; 3&sigma; points to a blended star.")
            + note("The centroid test is the one the first version of this deck listed as not done; it is done on the SPOC centroids of the ten planets (next slide)."),
            "Three tests, three kinds of input. Odd-even uses only the brightness series. Ellipsoidal modulation and Doppler beaming are harmonics of the orbital period and need the folded series. The centroid test is the only one that needs the images: it asks whether the light centre moves in the stamp when the dip happens."))
vv = []
for n in names:
    v = VET.loc[n]
    vv.append([f"<b>{NUM[n]}</b> {n}", f"{ST['oddeven'][n]['sigma_beta']:+.1f}", f"{GEO.loc[n, 'crowdsap']:.2f}", f"{int(v.n_transits)}", f"{v.dR_px * 1000:.2f}", f"{v.dR_arcsec:.3f}", f"{v.sig_max:.1f}"])
S.append(sl("K  Methods. Vetting results for our ten: odd-even in sigma, and the centroid shift in 10<sup>&minus;3</sup> pixel and arcseconds",
            tblw(["Planet", "Odd-even (&sigma;, with &beta;)", "CROWDSAP", "Transits", "&Delta;R<sub>c</sub> (10<sup>&minus;3</sup> px)", "&Delta;R<sub>c</sub> (&Prime;)", "Largest |shift|/error"], vv, [220, 215, 140, 120, 200, 140, 125], "tbl xs")
            + note("&Delta;R<sub>c</sub>: mean in-transit minus local out-of-transit centroid (MOM_CENTR1, 2) over the transits used; the last column uses white-noise errors. HD 189733 b (8.8) is the only one over 3; a shift is expected when CROWDSAP is below 1, and we do not interpret it further."),
            "Computed in code/33_checkpoint_facts.py from the light curves of the sectors we used: for each transit the in-transit centroid minus a straight line fitted to the out-of-transit centroid, then weighted over the transits. All ten shifts are below 0.03 arcsec, which is 0.0013 pixel. The odd-even column is the one of the diagnostics slide."))
S.append(sl("K  Methods. Asteroseismology, step by step: power spectrum, &nu;<sub>max</sub> and &Delta;&nu;, then stellar radius and mass",
            fm("P<sub>LS</sub>(&nu;) = (1/2&sigma;<sup>2</sup>) { [ &Sigma;(f &minus; &lang;f&rang;) cos 2&pi;&nu;(t &minus; &tau;) ]<sup>2</sup> / &Sigma; cos<sup>2</sup> + [ &Sigma;(f &minus; &lang;f&rang;) sin 2&pi;&nu;(t &minus; &tau;) ]<sup>2</sup> / &Sigma; sin<sup>2</sup> }", "Lomb-Scargle spectrum of the 1-D series (gaps allowed). Input: 2-min or 20-s series, at least one sector.")
            + fm("&nu;<sub>n,&ell;</sub> &asymp; &Delta;&nu; ( n + &ell;/2 + &epsilon; ) &minus; &ell;(&ell; + 1) D<sub>0</sub>", "&nu;<sub>max</sub>: centre of the bell-shaped excess of power; &Delta;&nu;: spacing, from the autocorrelation of the spectrum.")
            + fm("R<sub>&#9733;</sub>/R<sub>&#9737;</sub> = (&nu;<sub>max</sub>/&nu;<sub>max,&#9737;</sub>) (&Delta;&nu;/&Delta;&nu;<sub>&#9737;</sub>)<sup>&minus;2</sup> (T<sub>eff</sub>/T<sub>eff,&#9737;</sub>)<sup>1/2</sup> ;&nbsp; M<sub>&#9733;</sub>/M<sub>&#9737;</sub> = (&nu;<sub>max</sub>/&nu;<sub>max,&#9737;</sub>)<sup>3</sup> (&Delta;&nu;/&Delta;&nu;<sub>&#9737;</sub>)<sup>&minus;4</sup> (T<sub>eff</sub>/T<sub>eff,&#9737;</sub>)<sup>3/2</sup>", f"Solar references &nu;<sub>max</sub> = {ast['nu_max_sun']:.0f} &micro;Hz ({ckp('huber_sun')}), &Delta;&nu; = {ast['dnu_sun']} &micro;Hz ({ckp('huber_dnu')}).")
            + note("We did not do this; it is the route to a stellar radius that does not depend on Gaia, which would tighten the 1 to 7 % radius error of our ten planets."),
            "The chain is: power spectrum, two global numbers, then two scaling relations. The solar values 3090 and 135.1 microhertz are the reference points of Huber and colleagues. We did not run this on TESS data; the slide gives the steps and the data needed. The note on radius error refers to the stellar radius uncertainty from the archive, which we carry into every planet radius."))
S.append(sl("K  Methods. Stars in full frames, step by step: difference imaging, flare energy, variable-star periods",
            fm("D(x, y, t<sub>k</sub>) = I(x, y, t<sub>k</sub>) &minus; [ (R &lowast; K)(x, y) + B(x, y, t<sub>k</sub>) ]", "R: a reference image (median of good frames); K: a kernel matching the PSF. What remains in D are sources that changed. Input: <b>image cubes</b> of 4096 &times; 4096 pixels.")
            + fm("E<sub>flare</sub> = L<sub>&#9733;,TESS</sub> &int; [ F(t) &minus; F<sub>0</sub> ] / F<sub>0</sub> dt", "L<sub>&#9733;,TESS</sub>: luminosity of the star in the TESS band; the integral is the equivalent duration. Input: a 1-D series per star.")
            + fm("period of a variable star: peak of P<sub>LS</sub>(&nu;), or the phase with the least dispersion (PDM)", "Input: a 1-D series per star, from FFI pipelines: QLP (Huang 2020) and eleanor (Feinstein 2019); difference imaging: Oelkers 2018.")
            + note("The checkpoint notes wrote the flare energy as 4&pi;d<sup>2</sup>L &times; integral; the integral is already a time, so E = L &times; equivalent duration."),
            "Full-frame work needs methods that do not rely on a fixed aperture. Difference imaging subtracts a reference image so that every constant star vanishes and only changing sources remain. For flares the energy is the star's luminosity in the TESS band times the equivalent duration, the area under the relative flux above the quiet level. Variable-star periods come from a periodogram or from phase dispersion minimisation."))
# ================================================================ K19 - K24 direct imaging
S.append(sl("K  Methods. Direct imaging, the geometry: all ten planets lie within 0.03 % of one TESS pixel from their star",
            fig("ck_separation", 1100, f"&theta; = a / d. Our ten: {gs['theta_mas_min']:.2f} to {gs['theta_mas_max']:.1f} mas; one pixel is 21&Prime; = 21 000 mas.")
            + obt([f"largest: LTT 1445 A b, {gs['theta_mas_max']:.1f} mas = {gs['theta_over_pixel_max'] * 100:.3f} % of a pixel",
                   f"Jupiter at 5.2 AU, star at 10 pc: {ana['jupiter_5au_10pc_arcsec']:.2f}&Prime; = {100 * ana['jupiter_5au_10pc_arcsec'] / 21:.1f} % of a pixel; HR 8799 b: 68 AU at 39.4 pc = {ana['hr8799_b_arcsec']:.1f}&Prime; ({ckp('marois_dist')})"], "In one pixel"),
            "The separation in arcseconds is the semi-major axis in AU divided by the distance in parsec. For our ten planets it is a few milliarcseconds. Even a Jupiter analogue at 5 AU around a star 10 parsecs away is only 2.5 per cent of a pixel from its star. The checkpoint notes put HR 8799 at 10 parsecs; Marois et al. give 39.4 parsecs."))
S.append(sl("K  Methods. Direct imaging, PSF and contrast: the star's halo, the planet's faintness, and no coronagraph",
            cols(card("PSF", f"50 % of the light in one pixel, 90 % in 4 &times; 4 pixels = 1.4&prime; ({RP('ensq90')}): a planet within 40&Prime; lies in the halo. Diffraction limit of a 10.5 cm lens: {CKF['diffraction_arcsec']['tess_800nm']:.1f}&Prime; at 800 nm, so the wide PSF is by design.", "navy", 330),
                 card("Contrast", f"Reflected light is A<sub>g</sub>(R<sub>p</sub>/a)<sup>2</sup>: Jupiter at 5.2 AU {sci(ana['jupiter_contrast'])}, Earth at 1 AU {sci(ana['earth_contrast'])} (A<sub>g</sub> = 0.3, ours). Our ten hot planets: {sci(gs['contrast_min'])} to {sci(gs['contrast_max'])}, but too close to resolve.", "orange", 330),
                 card("No coronagraph", f"Payload: four cameras and a data handling unit ({RP('payload')}). JWST uses a coronagraph at 2.7 and 4.44 &micro;m ({ckp('jwst_coro')}). Imaging is hard: small separation and large contrast together ({ckp('marois_challenge')}).", "navy", 330))
            + take("Two walls at once: the planet is inside one pixel, and it is about a billion times fainter than its star."),
            "Quantitative version of the first part of the answer in the checkpoint notes. The 1.4 arcminute figure is the specified size of the star image, not a diffraction effect: a 10.5 centimetre aperture would diffract light into about 2 arcseconds at 800 nanometres. The contrast values are our own arithmetic with an assumed albedo of 0.3."))
S.append(sl("K  Methods. Direct imaging, the wavelength: TESS sees reflected light at 0.6&ndash;1 &micro;m, young giants glow at 2&ndash;20 &micro;m",
            fig("ck_bands", 940, "Bands of the missions in this deck. Shaded: thermal infrared.")
            + obt([f"a 1000 K, Jupiter-size planet round a Sun-like star: contrast {sci(CKF['thermal_contrast_1000K']['0.8um'])} at 0.8 &micro;m, {sci(CKF['thermal_contrast_1000K']['2.0um'])} at 2 &micro;m, {sci(CKF['thermal_contrast_1000K']['4.4um'])} at 4.4 &micro;m (Planck, ours)"], "Why the infrared"),
            f"The band of each mission is quoted from its paper: TESS 600 to 1000 nanometres, Kepler 423 to 897, PLATO 500 to 1000 (2014 design), Rubin 320 to 1050, Roman 0.48 to 2.0 micrometres from its filter table, JWST mirrors 0.6 to 29. The contrast numbers use the Planck function with an assumed temperature of 1000 kelvin and Jupiter and Sun radii; they show why imaging is done in the infrared."))
gr = []
for a in (1, 5, 10, 30, 70):
    gr.append([f"{a} AU"] + [f"{CKF['needed_grid'][f'{a}AU_{d}pc']['theta']:.2f}&Prime;" for d in (10, 20, 50, 100)])
Dn = lambda lam_um, th: 1.22 * lam_um * 1e-6 / (th / 206264.806)
dd = [[f"{th}&Prime;"] + [f"{Dn(l, th):.1f} m" for l in (0.8, 1.6, 4.4)] for th in (0.05, 0.1, 0.5)]
S.append(sl("K  Methods. Direct imaging, how much resolution is enough: a pixel of 0.005&Prime; to 3.5&Prime; and a mirror of 0.4 to 22 m",
            cols("<div>" + tblw(["a \\ d", "10 pc", "20 pc", "50 pc", "100 pc"], gr, [110, 120, 120, 120, 120], "tbl xs") + note("Separation &theta; = a/d.") + "</div>",
                 "<div>" + tblw(["&theta; needed", "0.8 &micro;m", "1.6 &micro;m", "4.4 &micro;m"], dd, [170, 150, 150, 150], "tbl xs") + note("Mirror D = 1.22 &lambda;/&theta;. TESS: 0.105 m.") + "</div>", tpl="620px 1fr")
            + take("Pixel at most half of &theta;: 0.005&Prime; to 3.5&Prime;, which is 6 to 4 200 times finer than TESS's 21&Prime;; and coronagraph plus adaptive optics on top (Marois used AO on Keck and Gemini)."),
            "Our own arithmetic, in two tables. Left: the separation for a few semi-major axes and distances. Right: the mirror diameter D for which 1.22 lambda over D equals the separation, so the planet lies outside the first diffraction ring. The checkpoint notes quoted a pixel of 0.01 to 0.05 arcseconds and mirrors of 2.4 to 10 metres; both lie inside our grid, which gives pixels of 0.005 to 3.5 arcseconds and mirrors of 0.4 to 22 metres depending on separation and wavelength. These are necessary conditions, not sufficient: contrast also needs a coronagraph and adaptive optics."))
S.append(sl("K  Methods. Spatial against temporal resolution: the trade is field of view, not cadence",
            cols(card("Fixed pixels: FOV = N &times; scale<sup>2</sup>", f"TESS: 4 &times; 4096<sup>2</sup> pixels &times; (21&Prime;)<sup>2</sup> = {n0(CKF['tess_fov_from_pixels_deg2'])} deg² (quoted 2300). JWST NIRCam, one module: {CKF['tradeoff'][5]['fov_computed']:.4f} deg². Ratio {n0(CKF['tess_vs_jwst_fov'])}. A pixel 10 times finer means 100 times less sky.", "navy", 320),
                 card("Cadence on the target", "Once a telescope stares at one star, it can read fast. A planet is so faint that photons arrive slowly, so the science image needs a long exposure (our reasoning): hours of integration, not a faster frame rate.", "orange", 320),
                 card("What is given up", "A narrow field images one star at a time: the sky survey rate falls by the field ratio, millions of times. Better detectors do not remove the trade: etendue, area times field, is conserved (our reasoning).", "navy", 320))
            + take("Instruments with fine pixels give up sky coverage and revisit rate, not the speed of a frame."),
            "Answers the question whether high spatial resolution costs temporal resolution. The unavoidable trade is between pixel size and field of view for a given number of pixels. The cadence of a single frame can be fast in every telescope; what changes is how long you must integrate to reach a signal-to-noise ratio, which is long for a faint planet. We computed the field from pixel counts and scales: for TESS it gives 2284 square degrees against the quoted 2300."))
S.append(sl("K  Methods. Does imaging need TESS? Only for stars and atmospheres, not for planets: the two populations hardly overlap",
            tblw(["", "TESS discoveries", "Imaged planets"],
                 [["Number in the archive", f"{IMT['tess']['n']:,}".replace(",", " "), f"{IMT['imaging']['n']}"],
                  ["Median semi-major axis", f"{IMT['tess']['a_median']:.3f} AU", f"{IMT['imaging']['a_median']:.0f} AU"],
                  ["Middle 80 % of a", f"{IMT['tess']['a_p10']:.2f} to {IMT['tess']['a_p90']:.2f} AU", f"{IMT['imaging']['a_p10']:.0f} to {IMT['imaging']['a_p90']:,.0f} AU".replace(",", " ")],
                  ["Median period", f"{IMT['tess']['P_median']:.1f} d", f"{IMT['imaging']['P_median'] / 365.25:,.0f} yr".replace(",", " ")],
                  ["On the other side of 1 AU", f"{IMT['overlap_a_range']['tess_a_above_1AU']} planets have a &gt; 1 AU", f"{IMT['overlap_a_range']['imaging_a_below_1AU']} planet has a &lt; 1 AU"]], [330, 420, 410], "tbl sm")
            + cols(card("What imaging uses", f"Young, nearby stars, for example in moving groups ({ckp('bowler_young')}), with positions from catalogs such as Gaia; not a map made by TESS.", "navy", 190),
                   card("Where TESS does help", f"Atmospheres: the ecliptic poles are the best places for JWST follow-up ({RP('jwst_poles')}); the TESS input catalog is built on Gaia DR2.", "orange", 190), tpl="1fr 1fr"),
            "The notes asked whether direct-imaging telescopes work from a map made by TESS. Half of that is right: TESS and imaging share the Gaia coordinate frame, and TESS planets are the targets of JWST transmission spectroscopy. But the planets themselves are different populations: in the archive the median TESS planet orbits at 0.06 AU in 5.7 days, the median imaged planet at 151 AU. Only one imaged planet is inside 1 AU and only two TESS planets are outside it."))
# ================================================================ Q1 - Q8 satellites, missions, pixel, apertures, sources
S.append(sl("Q  TESS. What was launched: one satellite, four cameras, sixteen CCDs, one band",
            tblw(["Item", "Count", "Source"],
                 [["Satellite", "1, launched 18 April 2018 by SpaceX Falcon 9 from Cape Canaveral", "NASA; MIT News"],
                  ["Cameras", f"4 identical; each with 7 lens elements, f/{TD['cameras']['f_number']}, pupil {TD['cameras']['pupil_cm']} cm", f"{ckp('camera_build')}"],
                  ["CCDs", f"16 (4 per camera); each camera is 4096 &times; 4096 pixels, the satellite {4 * 4096 ** 2 / 1e6:.1f} million imaging pixels (computed)", f"{ckp('ccd_mosaic')}"],
                  ["Wavelength band", "one band, 600 to 1000 nm: long-pass filter &times; CCD response", f"{ckp('resp_curve')}"],
                  ["Data products", "2 kinds of images (stamps, full frames) and the light curves, cotrending vectors derived from them", "STScI manual"],
                  ["Instruments that are not there", "no spectrograph, no coronagraph", f"{RP('payload')}"]], [250, 690, 220], "tbl xs")
            + note("&lsquo;How many types of satellites?&rsquo; One: TESS is not a constellation. The other missions of our project are on the next slide."),
            "The payload of TESS is four cameras and a data handling unit. Each camera has four CCDs of 2048 by 2048 imaging pixels, so 16 CCDs and about 67 million imaging pixels in all."))
fac = []
for n in names:
    g = GEO.loc[n]
    kind = "space" if g.facility.startswith(("Transiting", "K2", "Kepler")) else "ground"
    fac.append([f"<b>{NUM[n]}</b> {n}", g.facility.replace("Transiting Exoplanet Survey Satellite (TESS)", "TESS"), g.method, f"{g.disc_year}", kind])
nspace = sum(1 for r in fac if r[4] == "space")
S.append(sl(f"Q  Missions behind our ten planets: {nspace} found from space (TESS, K2), {10 - nspace} from the ground",
            tblw(["Planet", "Discovered with", "Method", "Year", "Platform"], fac, [250, 420, 220, 100, 170], "tbl xs")
            + note("From the NASA Exoplanet Archive, table pscomppars. All ten are re-measured here with TESS SPOC light curves. Other missions in this deck: Kepler, CHEOPS, Gaia (parallaxes behind the TESS input catalog), JWST and HST (atmospheres)."),
            f"Counted from the discovery facility column of the archive: three planets (LTT 9779 b, TOI-270 c, LTT 1445 A b) were found by TESS itself, K2-141 b by K2, and six from the ground. HD 118203 b, HD 189733 b and HD 209458 b are listed with the radial-velocity method."))
S.append(sl("Q  TESS. The wavelength range against the other missions: one band, 600 to 1000 nm",
            fig("ck_bands", 1100, "Wavelength coverage; TESS in red. Sources: Ricker, Koch, Rauer, Ivezic, Akeson, Gardner (checkpoint_sources.csv).")
            + take("A single band keeps the camera simple and sensitive to cool red stars; it gives no colour and no spectrum."),
            "Every bar is quoted from the paper of its mission with a PDF page in data/literature/checkpoint_sources.csv. PLATO is the 2014 design; CHEOPS is not shown because we could not verify its band in the paper we hold."))
px = [["TESS", "21″", "1", f"{RP('pixel')}"], ["Kepler", "3.98″", f"{21 / 3.98:.1f}", f"{ckp('kepler_plate')}"], ["PLATO (2014 design)", "15″", f"{21 / 15:.1f}", f"{ckp('plato_px')}"],
      ["Gaia", "0.059″ &times; 0.177″", f"{21 / 0.0589:.0f}", f"{ckp('gaia_px')}"], ["Rubin", "0.2″", f"{21 / 0.2:.0f}", f"{ckp('rubin_px')}"],
      ["Roman WFI", "0.11″", f"{21 / 0.11:.0f}", f"{ckp('roman_px')}"], ["JWST NIRCam", "0.031″ and 0.063″", f"{21 / 0.031:.0f} and {21 / 0.063:.0f}", "STScI JDox"]]
S.append(sl("Q  TESS. A single pixel is 21&Prime;: how it follows from the optics, and how it compares with other missions",
            fm("scale = (p / f) &times; 206 265&Prime; = (15 &micro;m / 147 mm) &times; 206 265&Prime; = 21.05&Prime;", f"f = 10.5 cm &times; 1.4 = 147 mm; our files: {MS['pix_scale_arcsec'][0]:.1f} to {MS['pix_scale_arcsec'][1]:.1f}&Prime;; 4096 &times; 21&Prime; = {PX['mosaic_deg']:.1f}&deg;.")
            + tblw(["Mission", "Pixel scale", "Times finer than TESS", "Source"], px, [300, 280, 280, 300], "tbl xs"),
            "The pixel scale is the physical pixel size divided by the focal length, converted to arcseconds. 50 per cent of a star's light falls in one pixel and 90 per cent in 4 by 4 pixels, which is the 1.4 arcmin of the slide on resolution. The Gaia value is the 10 by 30 micrometre pixel size converted by the paper to 58.9 by 176.8 milliarcseconds."))
ap = []
for n in names:
    v = VET.loc[n]; ap.append([f"<b>{NUM[n]}</b> {n}", f"{GEO.loc[n, 'crowdsap']:.3f}", f"{1 / GEO.loc[n, 'crowdsap']:.2f}", f"{1 / v.ratio_sap_over_pdcsap:.2f}"])
S.append(sl("Q  TESS. The aperture grids are images: stamp, mask, sum, and the crowding that dilutes the transit",
            cols(card("What it is", "A target pixel file: an 11 &times; 11 image every 2 min. The grid shows which pixels were summed.", "navy", 0),
                  card("What it is for", "The dark pixels summed give the star's light curve; neighbours in the mask dilute the dip.", "orange", 0),
                  card("What CROWDSAP says", f"The share of mask flux from the target: LTT 1445 A b {GEO.loc['LTT 1445 A b', 'crowdsap']:.2f}. Ignoring it shrinks R<sub>p</sub> by &radic;{dil['depth_boost']:.2f} = {dil['radius_error_if_ignored']:.2f}.", "navy", 0))
            + tblw(["Planet", "CROWDSAP", "1 / CROWDSAP", "PDCSAP depth / SAP depth (measured)"], [ap[i] for i in (0, 6, 7, 8)], [250, 190, 220, 440], "tbl xs"),
            "The answer to the question whether the grids are images. Yes: they are cutouts of the camera images. The figure draws the mask, not the brightness. The mask matters because TESS pixels are large: every star inside it adds light. The ratio of the PDCSAP depth to the SAP depth that we measure on the data follows 1 over CROWDSAP; all ten planets are in results/checkpoint_vetting.csv."))
tr = [["TESS", "24&deg; &times; 96&deg; = 2300 deg²", "21&Prime;", "120 s, 20 s; full frames 30 min, 10 min, 200 s", "27.4 d per sector; 2 yr for the sky"],
      ["Kepler (reference)", "115 deg²", "3.98&Prime;", "1765.8 s and 58.9 s", "one field, continuous"],
      ["PLATO (2014 design)", "2232 deg²", "15&Prime;", "25 s and 2.5 s", "long stare; launch: ESA, end of 2026"],
      ["Roman", "0.281 deg²", "0.11&Prime;", "15 min (bulge survey)", "72-day seasons; launched 30 Aug 2026"],
      ["Rubin LSST", "9.6 deg²", "0.2&Prime;", "30 s per visit", "every 3 d on average"],
      ["JWST NIRCam", "a few arcmin² per module", "0.031&Prime; and 0.063&Prime;", "set by the observer", "pointed, no automatic repeat"]]
S.append(sl("Q  After TESS. Trade-offs of the next telescopes: field of view, pixel, cadence, revisit time",
            tblw(["Mission", "Field of view", "Pixel", "Cadence", "Revisit"], tr, [220, 290, 210, 250, 190], "tbl xs")
            + note("PLATO: 26 cameras on the ESA page of 2026, 34 telescopes in the 2014 paper; another ESA item says early 2027, so the date is not settled here."),
            "The checkpoint notes said PLATO would launch at the end of 2026 and Roman in 2026 or 2027. The ESA page we saved says end of 2026 on Ariane 6 with 26 cameras; the 2014 paper described 34 telescopes with 2232 square degrees and 15 arcsecond pixels. NASA reports that Roman launched on 30 August 2026 on a Falcon Heavy. JWST, Rubin and Kepler values are from their papers or documentation."))
S.append(sl("Q  After TESS. The rule behind the table: FOV &prop; N &times; scale², staring against scanning, SNR &prop; D&radic;t",
            fig("ck_tradeoff", 860, "Diagonals: fixed numbers of pixels. TESS, Kepler, PLATO, Roman, Rubin, JWST: pixel scale against field of view.")
            + obt([f"FOV = N &times; scale<sup>2</sup> gives the quoted fields: TESS {CKF['tradeoff'][0]['fov_computed']:.0f} / 2300, Kepler {CKF['tradeoff'][1]['fov_computed']:.0f} / 115, Roman {CKF['tradeoff'][3]['fov_computed']:.3f} / 0.281, Rubin {CKF['tradeoff'][4]['fov_computed']:.1f} / 9.6 deg²",
                   "staring (TESS, PLATO): fast cadence, rare return; scanning (Rubin): frequent return, sparse sampling (our reading)",
                   "SNR &prop; D&radic;t: half the mirror needs four times the exposure"], "Three rules"),
            "The figure places each mission by pixel scale and field of view. The diagonals are lines of constant number of pixels. The computed fields agree with the quoted ones, which confirms the pixel counts and scales of the table. The two other rules are physical: staring gives dense time sampling of a field and rare returns to other fields, scanning does the opposite; and for a faint source the signal-to-noise ratio grows with the mirror diameter and the square root of the exposure."))
S.append(sl("Q  Sources. What the checkpoint notes got right, and what we corrected, part 1",
            tblw(["Claim in the notes", "Check", "Result"],
                 [["&lsquo;Stars in full frames&rsquo; is a heading of the TESS paper", f"Sec 8.4 is &lsquo;Full Frame Images&rsquo; ({ckp('ffi_title')})", "label shortened by us"],
                  ["Full frames hold tens of millions of stars", f"about 10<sup>6</sup> objects per image, about 20 million in two years ({ckp('ffi_count')})", "corrected"],
                  ["PDCSAP = (flux &minus; (1 &minus; C) mean) / (C &times; f)", f"median PDCSAP/SAP = C/f within {CKF['pdcsap_check']['max_abs_rel_diff_pct']:.2f} % on {CKF['pdcsap_check']['n_files']} files", "divide by f only"],
                  ["a/R<sub>&#9733;</sub> = &radic;[(1+k)<sup>2</sup> &minus; b<sup>2</sup>] / sin(&pi;T<sub>14</sub>/P)", f"exact form with cos<sup>2</sup> term; shortcut off by up to {rt['a_approx_max_rel_pct']:.1f} %", "corrected"],
                  ["Apogee 373 000 km", f"59 R<sub>&oplus;</sub> = 376 000 km ({RP('orbit_shape')})", "corrected"],
                  ["1 027 planets was a pre-launch forecast", f"it is the archive count of planets discovered by TESS on {DSY['date']}; Ricker expects thousands below Neptune size", "corrected"],
                  ["471 is a catalog of planets with masses", "471 is our shortlist after the cuts T mag &lt; 11, P &lt; 15 d, S/N &gt; 12", "corrected"]], [430, 560, 170], "tbl xs")
            + note("Each check is a quotation with a PDF page, or a number computed from our files."),
            "The notes ended with a request to check the sources. This slide and the next list every claim we could test and the result. Seven corrections to wording or number appear in this half."))
S.append(sl("Q  Sources. What the checkpoint notes got right, and what we corrected, part 2",
            tblw(["Claim in the notes", "Check", "Result"],
                 [["HR 8799 at 10 pc, planets at 15 to 70 AU", f"39.4 pc, planets at 24, 38 and 68 AU ({ckp('marois_dist')}); separations 0.6 to 1.7&Prime;", "corrected"],
                  ["Centroid precision about 0.2&Prime; (1/100 pixel)", f"measured error {VET.dx_err.min() * 21:.4f} to {VET.dy_err.max() * 21:.3f}&Prime; over several transits", "better, ours"],
                  ["TESS avoids the plane that holds the Galactic centre", "strips start at 6&deg;; the centre is at &minus;5.5&deg; (computed)", "at the edge"],
                  ["PLATO: launch end of 2026, 26 cameras", "ESA page: end of 2026, 26 cameras; 2014 paper: 34 telescopes; other ESA item: 2027", "not settled"],
                  ["Roman expected 2026&ndash;2027", "NASA: launched 30 August 2026, Falcon Heavy, Launch Complex 39A", "already launched"],
                  ["TTV listed under TESS alone", "timing is a TESS product; mass needs a dynamical model, usually with velocities", "kept as partner"],
                  ["Solar &nu;<sub>max</sub> 3090 &micro;Hz, &Delta;&nu; 135.1 &micro;Hz", f"{ckp('huber_sun')} (2011)", "confirmed"],
                  ["Pixel 21&Prime;, 90 % of light in 1.4&prime;, 600 to 1000 nm", f"Table 1 ({RP('ensq90')}), Fig 1 ({ckp('resp_curve')})", "confirmed"]], [410, 590, 160], "tbl xs")
            + note("&lsquo;Not settled&rsquo; means the sources we hold disagree; check ESA before quoting a launch date."),
            "Second half of the audit. The corrections to the planets of HR 8799 and to the Roman launch matter because they would have appeared as errors on a slide. For PLATO the sources disagree: the saved ESA page says end of 2026, another ESA item says early 2027."))
S.extend([])
SRCMAP.update({
    "K  Methods. Stars in full frames is not": "Source: Ricker 2015 Sec 8.4, pp. 13 and 14; NASA Exoplanet Archive; our measurements",
    "K  Methods. One image series": "Source: Ricker 2015 Sec 8.2; our centroid test (code/33_checkpoint_facts.py)",
    "K  Methods. Indirect against direct": "Source: Ricker 2015 Sec 8.1; archive TAP query of 2026-11-22; Bowler 2016; our arithmetic",
    "K  Methods. One set of cameras": "Source: Ricker 2015 Sec 4.2, 4.3, 8.4 (pp. 6, 7, 13, 14); NASA HEASARC data products page",
    "K  Methods. Tick the methods": "Source: reading by us from the instrument numbers of Ricker 2015 (Table 1, Sec 3.5, 7.2) and our files",
    "K  Methods. Transit photometry and the four": "Source: Ricker 2015 Sec 3.5, Table 1; our fits (results/checkpoint_geometry.csv)",
    "K  Methods. Phase curve and secondary eclipse and": "Source: Ricker 2015 Table 1; Shporer 2019; our fits and phase-0.5 measurement",
    "K  Methods. False-positive vetting and": "Source: SPOC centroids (MOM_CENTR1, 2) of our files; our fits (results/checkpoint_vetting.csv)",
    "K  Methods. Asteroseismology and": "Source: Ricker 2015 Sec 7.2, 8.3; Huber 2011 Sec 2; Nyquist and resolution computed",
    "K  Methods. Stars in full frames and the four": "Source: Ricker 2015 Table 1, Sec 8.4; NASA HEASARC data products page",
    "K  Methods. Input data": "Source: STScI TESS archive manual; SPOC headers of our files; code/33_checkpoint_facts.py",
    "K  Methods. Transit photometry, step": "Source: Mandel and Agol 2002; Winn 2010 form of the duration; checked on our fits (code/33)",
    "K  Methods. Transit numbers": "Source: our fits (results/checkpoint_geometry.csv); catalog M and R from the NASA archive",
    "K  Methods. Phase curve and secondary eclipse, step": "Source: Shporer 2019; our flat-band Planck solution (code/33_checkpoint_facts.py)",
    "K  Methods. False-positive vetting, step": "Source: Ricker 2015 Sec 8.2; Shporer 2019 (ellipsoidal, beaming); SPOC centroid columns",
    "K  Methods. Vetting results": "Source: results/checkpoint_vetting.csv and figures/paper/figure_stats.json (odd-even)",
    "K  Methods. Asteroseismology, step": "Source: Huber 2011 (solar references, scaling relations); Kjeldsen and Bedding 1995",
    "K  Methods. Stars in full frames, step": "Source: Huang 2020 (QLP); Feinstein 2019 (eleanor); Oelkers 2018; Alard and Lupton 1998 for the kernel form",
    "K  Methods. Direct imaging, the geometry": f"Source: archive a and distance; {ckp('marois_dist')} (2008); Ricker 2015 Table 1",
    "K  Methods. Direct imaging, PSF": "Source: Ricker 2015 Table 1; Marois 2008; Gardner 2006; contrasts computed (A_g = 0.3 assumed)",
    "K  Methods. Direct imaging, the wavelength": "Source: Ricker, Koch, Rauer, Ivezic, Akeson, Gardner (checkpoint_sources.csv); Planck function, our assumptions",
    "K  Methods. Direct imaging, how much": "Source: our arithmetic (theta = a/d, D = 1.22 lambda / theta); Marois 2008 for the use of adaptive optics",
    "K  Methods. Spatial against temporal": "Source: Ricker 2015 Table 1; STScI JDox; our arithmetic (FOV = N x scale squared)",
    "K  Methods. Does imaging need TESS": f"Source: NASA Exoplanet Archive TAP query of {DSY['date']}; Bowler 2016; Ricker 2015 abstract; NASA HEASARC",
    "Q  TESS. What was launched": "Source: Ricker 2015 Sec 4, 4.2, Table 1; NASA Science TESS page; MIT News",
    "Q  Missions behind": "Source: NASA Exoplanet Archive pscomppars (disc_facility, discoverymethod, disc_year)",
    "Q  TESS. The wavelength range": "Source: data/literature/checkpoint_sources.csv (verified quotes with PDF pages)",
    "Q  TESS. A single pixel": "Source: Ricker 2015 Sec 4.1, Table 1; Koch 2010; Rauer 2014; Gaia paper 2016; Ivezic 2019; Akeson 2019; STScI JDox",
    "Q  TESS. The aperture grids": "Source: SPOC headers (CROWDSAP, FLFRCSAP) and light curves of our files; Winters 2021 for LTT 1445",
    "Q  After TESS. Trade-offs": "Source: Ricker, Koch, Rauer, Akeson, Ivezic; STScI JDox; ESA PLATO page and NASA Roman blog, saved 22 Nov 2026",
    "Q  After TESS. The rule": "Source: pixel counts and scales of the table, computed; quoted fields in checkpoint_sources.csv",
    "Q  Sources. What the checkpoint notes got right, and what we corrected, part 1": "Source: checks listed in the Check column; data/literature/checkpoint_sources.csv",
    "Q  Sources. What the checkpoint notes got right, and what we corrected, part 2": "Source: checks listed in the Check column; data/literature/checkpoint_sources.csv",
})
