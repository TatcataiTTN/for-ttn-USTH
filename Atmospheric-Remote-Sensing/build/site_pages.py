# -*- coding: utf-8 -*-
"""Site-level pages (English): home, calculators, mock exam, formulas & acronyms, resources."""
import random, json, os
from lib import *
import mock_exam as ME
from lib import PHOTOS

def inp(i, label, v, step='any', w=None):
    st = f' style="width:{w}px"' if w else ''
    return f'<label>{label}<input id="{i}" type="number" step="{step}" value="{v}"{st}></label>'

def calculators_page():
    def box(cid, title, intro, inputs, out, cv=False):
        c = f'<canvas id="{out[:2]}_cv" width="760" height="300"></canvas>' if cv else ''
        return f'<section class="calc" id="{cid}"><h2>{title}</h2><p>{intro}</p><div>{inputs}</div><div class="res" id="{out}"></div>{c}</section>'
    body = '<p class="crumbs"><a href="index.html">Home</a> › Calculators</p><h1>Practice calculators</h1>' \
           '<p class="lead">Twelve tools that run in your browser (no server). All formulas come from the study guide; the results are tested automatically against Python (466 comparisons, including the averaging-kernel matrices) — see <code>tests/test_calc.js</code> and the notebook.</p>' + \
        box('lifetime', '1 · Lifetime and parallel sinks (Ch. 1)', 'τ<sub>chem</sub> = 1/(k·[OH]); parallel sinks 1/τ = Σ 1/τ<sub>i</sub>. Defaults are the CO + OH example of the mock exam.',
            inp('lt_k', 'k (cm³ s⁻¹)', '2e-13') + inp('lt_oh', '[OH] (cm⁻³)', '1e6') + inp('lt_t1', 'τ₁ (days)', 2) + inp('lt_t2', 'τ₂ (days)', 3) + inp('lt_t3', 'τ₃ (days)', 6), 'lt_out') + \
        box('plume', '2 · Lifetime from a plume (Ch. 1)', 'C(x) ∝ exp(−x/(U·τ)) ⇒ τ = L/U, where L is the observed e-folding length.', inp('pl_U', 'Wind speed U (m/s)', 5) + inp('pl_L', 'E-folding length L (km)', 50), 'pl_out', True) + \
        box('beer', '3 · Beer–Lambert and zenith angle (Ch. 2)', 'τ<sub>slant</sub> = τ<sub>vertical</sub>/cos θ; T = e<sup>−τ</sup>. Defaults: mock exam Q2(c).', inp('be_tau', 'Vertical τ', 0.5) + inp('be_sza', 'Zenith angle θ (deg)', 60), 'be_out', True) + \
        box('planck', '4 · Planck, Wien, Stefan–Boltzmann (Ch. 2)', 'Try 5778 K (Sun) and 288 K (Earth): λ<sub>max</sub> is about 0.50 µm and 10.06 µm.', inp('pk_T', 'Temperature T (K)', 288) + inp('pk_lam', 'Wavelength λ (µm)', 10), 'pk_out', True) + \
        box('doas', '5 · DOAS: AMF, VCD and Dobson Units (Ch. 3)', 'AMF ≈ 1/cos θ₀ + 1/cos θ; VCD = (SCD − SCD<sub>strat</sub>)/AMF. Enter SCD in units of 10¹⁵ molecule cm⁻².',
            inp('do_sza', 'Solar zenith θ₀ (deg)', 60) + inp('do_vza', 'Viewing zenith θ (deg)', 30) + inp('do_scd', 'SCD (×10¹⁵)', 8) + inp('do_str', 'Stratospheric SCD (×10¹⁵)', 3), 'do_out') + \
        box('ak', '6 · Averaging kernel and DOFS (Ch. 5)', '12-level model: K = Gaussians of width w levels; S<sub>ε</sub> = σ<sub>ε</sub>²I; a-priori correlated with height. A = (KᵀS<sub>ε</sub>⁻¹K + S<sub>a</sub>⁻¹)⁻¹KᵀS<sub>ε</sub>⁻¹K; DOFS = tr(A).',
            inp('ak_w', 'Kernel width w (levels)', 3) + inp('ak_se', 'σ<sub>ε</sub> (noise)', 0.1) + inp('ak_sa', 'σ<sub>a</sub> (a priori)', 1) + inp('ak_L', 'Correlation length', 3), 'ak_out', True) + \
        box('angstrom', '7 · Ångström exponent and AOD vs wavelength (Ch. 6)', 'α = ln(τ₁/τ₂)/ln(λ₂/λ₁); τ(λ) = τ₁(λ/λ₁)<sup>−α</sup>. Defaults: 0.60 at 440 nm and 0.15 at 870 nm.',
            inp('an_t1', 'AOD₁', 0.6) + inp('an_l1', 'λ₁ (nm)', 440) + inp('an_t2', 'AOD₂', 0.15) + inp('an_l2', 'λ₂ (nm)', 870) + inp('an_lq', 'AOD at λ (nm)', 550), 'an_out', True) + \
        box('size', '8 · Size parameter and scattering regime (Ch. 7)', 'x = 2πr/λ. Try r = 0.0002 µm (N₂), 0.2 µm (sulfate), 5 µm (dust) at λ = 0.55 µm.', inp('sz_r', 'Radius r (µm)', 0.2) + inp('sz_lam', 'Wavelength λ (µm)', 0.55), 'sz_out') + \
        box('tir', '9 · Brightness-temperature depression vs dust-layer height (Ch. 8)', 'I = B(T<sub>s</sub>)e<sup>−τ</sup> + B(T<sub>layer</sub>)(1 − e<sup>−τ</sup>) at 10 µm; T<sub>layer</sub> = T<sub>s</sub> − lapse × z. Simple model: no scattering, no water vapour.',
            inp('ti_Ts', 'Surface T (K)', 300) + inp('ti_tau', 'Aerosol τ (10 µm)', 0.5) + inp('ti_lap', 'Lapse rate (K/km)', 6.5), 'ti_out', True) + \
        box('opt', '10 · Optical depth and transmission, σ·N·L (Part A.4)', 'τ = σ·N·L, t = e<sup>−τ</sup>. Defaults: mock exam Q9(c) (σ = 2×10⁻²⁰ cm², N = 5×10¹³ cm⁻³, L = 1 km). Try the NO₂ example: σ = 1.5e-19, N = 5e11.',
            inp('op_s', 'σ (cm²)', '2e-20') + inp('op_n', 'N (molecule cm⁻³)', '5e13') + inp('op_l', 'L (km)', 1), 'op_out') + \
        box('lines', '11 · Doppler and Lorentz line widths vs altitude (Part A.5)', 'HWHM<sub>D</sub> = (ν̃/c)√(2 ln2·k<sub>B</sub>T/m); HWHM<sub>L</sub> = γ₀(P/P₀)(296/T)<sup>n</sup>. Isothermal pressure with scale height H.',
            inp('ln_nu', 'Wavenumber ν̃ (cm⁻¹)', 2927) + inp('ln_m', 'Molar mass (u)', 16.04) + inp('ln_T', 'T (K)', 250) + inp('ln_H', 'Scale height H (km)', 7) + inp('ln_g', 'γ₀ (cm⁻¹ atm⁻¹)', 0.07), 'ln_out', True) + \
        box('ddoas', '12 · DOAS differential optical depth (Part A.6)', 'D = σ′·SCD (fraction of signal ≈ D). Default: mock exam Q10(c).', inp('dd_s', 'σ′ (cm²)', '2e-19') + inp('dd_c', 'SCD (molecule cm⁻²)', '1e16'), 'dd_out')
    write('calculators.html', page('Calculators', body, 0, desc='Atmospheric remote sensing calculators that run in the browser', scripts=['theme.js', 'calc.js']))

def exam_sets(all_items, nsets=8, per=15):
    rng = random.Random(2026)
    by = {}
    for it in all_items: by.setdefault(it['mod'], []).append(it)
    for k in by: rng.shuffle(by[k])
    sets = []; ptr = {k: 0 for k in by}; mods = sorted(by)
    for s in range(nsets):
        pick = []
        order = mods[s % len(mods):] + mods[:s % len(mods)]
        while len(pick) < per:
            for m in order:
                if len(pick) >= per: break
                if ptr[m] < len(by[m]): pick.append(by[m][ptr[m]]); ptr[m] += 1
            if all(ptr[m] >= len(by[m]) for m in mods): break
        rng.shuffle(pick)
        sets.append([dict(q=p['q'], opts=p['opts'], correct=p['correct'], explain=p['explain'], src=f"{p['mod'].upper()} · {p['src']}") for p in pick])
    return sets

def exam_page(all_items):
    sets = exam_sets(all_items)
    data = json.dumps(dict(sets=sets), ensure_ascii=False).replace('</', '<\\/')
    qs = ''
    for q in ME.Q:
        parts = ''.join(f'<p>{p}</p>' for p in q['parts'])
        key = ''.join(f'<p>{k}</p>' for k in q['key'])
        qs += (f'<div class="qitem mock" data-q="{q["n"]}"><b>Question {q["n"]} ({q["pts"]} pts)</b> — <a href="lessons/{MODULES[q["ch"]][1]}/index.html">review {q.get("ref") or "Ch. " + str(q["ch"])}</a>{parts}'
               f'<details class="ans"><summary>Show suggested answer key</summary><div class="keyans">{key}</div></details>'
               f'<label class="selfgrade">Self-grade (0–{q["pts"]}): <input type="number" min="0" max="{q["pts"]}" step="0.25" class="sg" data-q="{q["n"]}" value=""></label></div>')
    instr = '<ul>' + ''.join(f'<li>{i}</li>' for i in ME.INSTR) + '</ul>'
    grading = '<ul>' + ''.join(f'<li>{g}</li>' for g in ME.GRADING) + '</ul>'
    body = f'''<p class="crumbs"><a href="index.html">Home</a> › Mock exam</p><h1>Mock exam</h1>
<p class="lead">Two parts: the <a href="#mock">original mock exam (120 minutes, 10 written questions, 25 points)</a> and <a href="#mcq">multiple-choice practice exams (15 questions, 30 minutes)</a> generated from the question banks of the 8 modules.</p>
<h2 id="mock">Original mock exam v2 (120 minutes, 10 questions, 25 points)</h2>
<div class="callout"><b class="t">Instructions</b>{instr}<p>Closed book, calculator allowed.</p></div>
<div class="sim"><div class="simh">Clock and total score</div><span class="quiz-score" id="mk_timer">Time: 120:00</span>
<button class="btn" id="mk_start">Start</button> <button class="btn alt" id="mk_stop">Stop</button> <button class="btn alt" id="mk_reset">Reset</button>
<span class="quiz-score" id="mk_total" data-max="{sum(q["pts"] for q in ME.Q):g}" style="margin-left:14px">Total: 0/{sum(q["pts"] for q in ME.Q):g}</span></div>
{qs}
<div class="callout good"><b class="t">Grading hints</b>{grading}</div>
<h2 id="mcq">Multiple-choice practice (15 questions, 30 minutes)</h2>
<p>Eight sets, each drawing questions from all 9 modules (Part A and chapters 1–8). Submit to see your score and an explanation for every question.</p><div id="exam"></div>
<script id="exam-data" type="application/json">{data}</script>'''
    write('exam.html', page('Mock exam', body, 0, desc='Original mock exam and multiple-choice practice exams', scripts=['theme.js', 'exam.js', 'mock.js']))

def reference_page():
    F = [('Lifetime', 'τ = M / L ; 1/τ = Σ 1/τᵢ ; τ_chem = 1/(k[OH])', 'Ch.1'), ('Beer–Lambert', 'I = I₀ exp(−τ), τ = ∫ (σ_a + σ_s) n ds ; T = e^(−τ)', 'Ch.2'),
         ('Planck / Wien', 'B_λ(T) = 2hc²/λ⁵ · 1/(e^(hc/λkT) − 1) ; λ_max T = 2898 µm K', 'Ch.2'), ('Stefan–Boltzmann', 'M = σ_SB T⁴', 'Ch.2'),
         ('RTE', 'dI/ds = −k_e I + k_a B(T) + (k_s/4π) ∫ P(Θ) I(Ω′) dΩ′', 'Ch.2'), ('DOAS', 'ln(I₀/I) = Σ σᵢ′ SCDᵢ + polynomial ; VCD = SCD / AMF', 'Ch.3'),
         ('Optimal estimation', 'x̂ = x_a + G(y − K x_a) ; A = GK ; DOFS = tr(A)', 'Ch.3, 5'), ('Averaging kernel', 'x̂ = x_a + A(x − x_a) + Gε', 'Ch.5'),
         ('Size parameter, Rayleigh', 'x = 2πr/λ ; σ ∝ r⁶/λ⁴ ; Q_ext → 2 (x ≫ 1)', 'Ch.7'), ('Ångström', 'τ(λ) = τ(λ₀)(λ/λ₀)^−α', 'Ch.6'),
         ('Single-scattering albedo', 'ω₀ = σ_s / (σ_s + σ_a)', 'Ch.2, 6'), ('Dobson Unit', '1 DU = 2.69 × 10¹⁶ molecules cm⁻²', 'Ch.3'),
         ('TIR with an aerosol layer', 'I ≈ B(T_s) e^(−τ_aer) + B(T_layer) (1 − e^(−τ_aer))', 'Ch.8'),
         ('RTE (lecture)', 'dI/dl = −k_ext·I + J ; k_ext = α_gas + s_gas + α_aer + s_aer', 'Part A.1'), ('Gas layer, no scattering', 'J = α·B(T) ; I(L) = I(0)e^(−τ(0,L)) + ∫ B(T(l)) e^(−τ(l,L)) dτ', 'Part A.3'),
         ('Surface boundary', 'I(0) = ε_s B(T_s) + (1 − ε_s) I_s ; 1 − ε_s = albedo', 'Part A.3'), ('Optical depth', 'τ = Σ ∫ σᵢ Nᵢ dl ; homogeneous τ = σ·N·L ; t = e^(−τ)', 'Part A.4'),
         ('Line widths', 'Doppler ∝ ν̃√(T/m) ; Lorentz ∝ P (T₀/T)ⁿ ; Voigt = both', 'Part A.5'), ('DOAS (differential)', 'σ = σ_b + σ′ ; D = ln(I′₀/I) = σ′·c·L', 'Part A.6')]
    A = [('AOD', 'Aerosol Optical Depth'), ('AMF / SCD / VCD', 'Air Mass Factor / Slant / Vertical Column Density'), ('AK, DOFS', 'Averaging Kernel, Degrees Of Freedom for Signal'),
         ('DOAS', 'Differential Optical Absorption Spectroscopy'), ('TOA', 'Top Of Atmosphere'), ('RTE', 'Radiative Transfer Equation'), ('LUT', 'Look-Up Table'),
         ('ALH', 'Aerosol Layer Height'), ('UVAI', 'UV Absorbing Aerosol Index'), ('TROPOMI, OMI, GOME-2', 'UV–vis–SWIR nadir spectrometers'), ('IASI, AIRS, CrIS', 'Thermal-IR nadir sounders'),
         ('MLS, MIPAS, OSIRIS', 'Limb sounders'), ('SAGE, ACE-FTS', 'Solar occultation instruments'), ('CALIOP, ATLID', 'Space lidars (active)')]
    t1 = hx_table(['Concept', 'Formula / value', 'Chapter'], [[a, f'<span class="mono">{b}</span>', c] for a, b, c in F], 'left')
    t2 = hx_table(['Acronym', 'Meaning'], [[a, b] for a, b in A], 'left')
    body = f'''<p class="crumbs"><a href="index.html">Home</a> › Formulas & acronyms</p><h1>Formulas and acronyms</h1>
<p class="lead">The formula sheet and acronyms of the study guide v2 (Part C), with a quick filter.</p>
<p><input id="flt" placeholder="Filter by keyword…" style="width:100%;max-width:420px;padding:6px 10px;font:inherit;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--text)"></p>
<h2>Key formulas</h2><div id="t1">{t1}</div><h2>Acronyms</h2><div id="t2">{t2}</div>
<script>document.getElementById('flt').addEventListener('input',function(){{var q=this.value.toLowerCase();document.querySelectorAll('#t1 tr,#t2 tr').forEach(function(r,i){{if(r.querySelector('th'))return;r.style.display=r.textContent.toLowerCase().indexOf(q)<0?'none':''}})}});</script>'''
    write('reference.html', page('Formulas and acronyms', body, 0, desc='Key formulas and acronyms for atmospheric remote sensing', scripts=['theme.js']))

def resources_page():
    figs = [('f1_lifetime', 'Lifetime vs spatial scale of variability (Ch. 1)'), ('f12_plume', 'NO₂ plume decay gives τ (Ch. 1)'), ('f18_decay', 'First-order decay e^(−t/τ) (Ch. 1)'),
            ('f2_interactions', 'Absorption, scattering, emission, Beer–Lambert (Ch. 2)'), ('f8_planck', 'Planck curves of the Sun and the Earth (Ch. 2)'), ('f11_phase', 'Phase functions from Mie theory (Ch. 2, 7)'),
            ('f6_wf', 'Weighting functions vs altitude (Ch. 3)'), ('f13_doas', 'The DOAS principle (Ch. 3)'), ('f3_geometries', 'Nadir / limb / occultation (Ch. 4)'), ('f15_tradeoff', 'Horizontal vs vertical resolution (Ch. 4)'),
            ('f4_avk', 'Ideal and realistic averaging kernels (Ch. 5)'), ('f14_colavk', 'Column averaging kernels (Ch. 5)'), ('f9_angstrom', 'Spectral dependence of AOD (Ch. 6)'), ('f16_surface', 'Effect of surface brightness (Ch. 6)'),
            ('f19_budget', 'Photon gains and losses along the line of sight (Part A.2)'), ('f20_line_widths', 'Doppler, Lorentz, Voigt widths vs altitude (Part A.5)'), ('f21_doas_principle', 'DOAS principle: I₀, I′₀, D (Part A.6)'), ('f22_rte_layers', 'Integrated RTE for a gas layer (Part A.3)'), ('f23_concept_map', 'Concept map of the 8 questions and Part A'), ('f24_o3_transmission', 'Transmittance through ozone at four UV wavelengths (Ch. 2)'),
            ('f5_regimes', 'Scattering regimes vs size parameter x (Ch. 7)'), ('f10_mie_qext', 'Q_ext from Mie theory (Ch. 7)'), ('f7_altitude', 'Principles of aerosol height retrieval (Ch. 8)'), ('f17_height_sens', 'Sensitivity vs layer height (Ch. 8)')]
    sl = [(k, PHOTOS[k]) for k in PHOTOS]
    sl_old = [('s1_gome', 'GOME: solar irradiance and Earth radiance'), ('s2_tropomi', 'TROPOMI L1b one pixel vs VIIRS'), ('s3_wavelengths', 'Wavelength windows for each species'), ('s4_solar', 'Solar spectrum at TOA and at sea level')]
    gal = ''.join(f'<figure class="lf" style="display:inline-block;width:48%;vertical-align:top"><a href="assets/images/fig/{n}.png"><img src="assets/images/fig/{n}.png" loading="lazy" alt="{esc(c)}"></a><figcaption>{c}</figcaption></figure>' for n, c in figs)
    gal2 = ''.join(f'<figure class="lf" style="display:inline-block;width:48%;vertical-align:top"><a href="assets/images/slides/{n}.jpg"><img src="assets/images/slides/{n}.jpg" loading="lazy" alt="{esc(c)}"></a><figcaption>{c}</figcaption></figure>' for n, c in sl)
    body = f'''<p class="crumbs"><a href="index.html">Home</a> › Resources</p><h1>Source documents and figures</h1>
<p class="lead">The study pack supplied by the student, kept unchanged so you can download, print or edit it.</p>
<div class="grid">
<a class="mod-card" href="resources/De_cuong_Remote_Sensing_Atmosphere_v2.pdf"><div class="num">PDF · v2</div><h3>Study guide v2 (40 pages)</h3><p>Part A core knowledge, 8 questions with worked examples, Q&amp;A and memory hooks, Part C formula sheet.</p></a>
<a class="mod-card" href="resources/De_cuong_Remote_Sensing_Atmosphere_v2.docx"><div class="num">DOCX · v2</div><h3>Study guide v2 (Word)</h3><p>Editable version.</p></a>
<a class="mod-card" href="resources/De_thi_mau_Remote_Sensing_v2.pdf"><div class="num">PDF · v2</div><h3>Mock exam v2 (4 pages)</h3><p>10 questions, 25 points, 120 minutes, suggested answers.</p></a>
<a class="mod-card" href="resources/De_thi_mau_Remote_Sensing_v2.docx"><div class="num">DOCX · v2</div><h3>Mock exam v2 (Word)</h3><p>Editable version.</p></a>
<a class="mod-card" href="resources/De_cuong_Remote_Sensing_Atmosphere.pdf"><div class="num">PDF · v1</div><h3>Study guide v1 (25 pages)</h3><p>First version, kept for reference.</p></a>
<a class="mod-card" href="resources/De_thi_mau_Remote_Sensing.pdf"><div class="num">PDF · v1</div><h3>Mock exam v1 (8 questions, 20 points)</h3><p>First version, kept for reference.</p></a>
<a class="mod-card" href="resources/README_Study_Guide_v2.md"><div class="num">MD</div><h3>README of study pack v2</h3><p>What is new in v2, folder layout, figure and slide-photo lists.</p></a>
<a class="mod-card" href="slides-gallery.html"><div class="num">11 photos</div><h3>Lecture slide gallery</h3><p>All class photos of slides and blackboard, with links to the matching lessons.</p></a>
<a class="mod-card" href="notebooks/verify_numbers.ipynb"><div class="num">IPYNB</div><h3>Number-verification notebook</h3><p>Python recomputes every number used on this site (executed, results saved).</p></a>
</div>
<h2>24 figures drawn by code (study guide v2)</h2><p style="font-size:.88rem;color:var(--muted)">Planck, Mie and line-width plots (f8, f10, f11, f20) are computed from the real equations; the others are schematic illustrations, as stated in the guide.</p>{gal}
<h2>11 lecture-slide photos</h2><p><a href="slides-gallery.html">Open the lecture slide gallery →</a></p>{gal2}'''
    write('resources.html', page('Resources', body, 0, desc='Study guide, mock exam and figures', scripts=['theme.js']))

def index_page(stats, ncalc=12):
    cards = ''
    for (mid, slug, title, en), st in zip(MODULES, stats):
        cards += (f'<a class="mod-card" href="lessons/{slug}/index.html"><div class="num">{label(mid)}</div><h3>{esc(title)}</h3><p>{esc(en)}</p>'
                  f'<p class="tag">{st["slides"]} slides</p><p class="tag">{st["mcq"]} MCQ</p><p class="tag">{st["ess"]} essays</p></a>')
    tot = lambda k: sum(s[k] for s in stats)
    body = f'''<div class="usth-banner"><img src="assets/images/usth_logo.png" alt="USTH"><div><div class="t">Atmospheric Remote Sensing</div><div class="s">Satellite Remote Sensing of Atmospheric Composition · self-study and exam preparation — USTH</div></div></div>
<p class="lead">Nine modules built on study guide v2: a Part A core-knowledge toolbox (radiative transfer, optical depth, line profiles, DOAS) and the eight theory questions: sinks and lifetime, light–matter interaction, trace-gas retrieval, pointing geometries, averaging kernels, passive aerosol sensing, scattering regimes and aerosol altitude. Each module has a lesson, slides, a question bank with explanations, and calculators checked against Python.</p>
<div class="kpis"><div class="kpi"><b>9</b><span>modules (Part A + 8 chapters)</span></div><div class="kpi"><b>{tot("slides")}</b><span>slides</span></div><div class="kpi"><b>{tot("mcq")}</b><span>multiple-choice questions</span></div><div class="kpi"><b>{tot("ess")}</b><span>essay questions</span></div><div class="kpi"><b>{ncalc}</b><span>calculators</span></div><div class="kpi"><b>11</b><span>lecture photos</span></div><div class="kpi"><b>8</b><span>15-question practice exams</span></div></div>
<h2>Modules</h2><div class="grid">{cards}</div>
<h2>Suggested study path</h2>
<ol class="steps"><li><b>Start with Part A</b> (core knowledge), then read a lesson (plain-language part first, then formulas, worked example, Q&amp;A and memory hooks) and watch its slides and lecture photos.</li><li><b>Take the quick quiz</b> at the bottom, then open the <b>question bank</b>; filter by “Original” to do the mock-exam questions first.</li><li><b>Practise the numbers</b> in the <a href="calculators.html">calculators</a> with the values from the mock exam.</li><li><b>Written practice</b>: draft the 10 questions of the <a href="exam.html">mock exam</a> in 120 minutes, then compare with the suggested answers and self-grade.</li><li>Finish with a <a href="exam.html#mcq">30-minute multiple-choice set</a>; for every mistake, go back to the matching module.</li></ol>
<h2>Status and limits (honest notes)</h2>
<ul><li><b>Single source</b>: the study pack v2 supplied by the student (40-page guide, mock exam with 10 questions, 24 figures, 11 lecture photos, plotting code); v1 is kept in Resources. No textbook came with it, so the site cites no book page numbers and adds no knowledge beyond the guide, except calculations explicitly labelled as home-made and computed in Python.</li>
<li><b>Numbers</b>: every calculated value is recomputed in Python (numpy/scipy) by two independent methods; the JavaScript calculators are compared with Python in 466 checks. The simple models (TIR brightness-temperature depression, O₂ above the layer, the 12-level averaging-kernel simulation, the line-width model)  are illustrations, not measured data.</li>
<li><b>Questions</b>: “Original” questions come from the mock exam, the exam checklists and the guide’s own content (each has its source); “Added” questions are extra items based on the guide. Answer positions and lengths were audited for bias.</li>
<li><b>Language</b>: English by default, as the course is taught in English. Each lesson also keeps the short Vietnamese summary from the study guide. No Chinese version.</li>
<li><b>Figures</b>: the 24 figures and 11 lecture photos come from the original pack; wide ones are scaled down on slides, so text inside a figure can be smaller than 20 px (all HTML slide text is ≥ 20 px).</li>
<li><b>One discrepancy found</b>: the guide’s Ch.8 worked example quotes brightness-temperature depressions of ≈ 7 K (4 km) and ≈ 2 K (1 km) for τ = 0.7; our simple blackbody-layer model gives larger values (see Chapter 8). The guide says its numbers are orders of magnitude; the trend is the same. Everything else in the v2 worked examples reproduced exactly (e.g. NO₂ τ = 0.0075, ozone transmission 9% and 79%, α = 2.0 and 0.15, DOFS ≈ 1.0, limb path 226 km).</li><li>Progress is stored in your browser’s <code>localStorage</code> (lost if you clear site data or use a private window).</li></ul>'''
    write('index.html', page('Home', body, 0, desc='Atmospheric Remote Sensing self-study system, USTH', scripts=['theme.js']))


def gallery_page():
    where = {'s1_gome': ('m3', 'Ch.3'), 's2_tropomi': ('m3', 'Ch.3'), 's3_wavelengths': ('m3', 'Ch.3'), 's4_solar': ('m2', 'Ch.2'), 's5_rte_equation': ('pa', 'Part A.1'), 's6_gains_losses': ('pa', 'Part A.2'),
             's7_rte_gas_layer': ('pa', 'Part A.3'), 's8_optical_depth': ('pa', 'Part A.4'), 's9_blackboard': ('pa', 'Part A.4'), 's10_line_widths': ('pa', 'Part A.5'), 's11_doas': ('pa', 'Part A.6')}
    slug = {m[0]: m[1] for m in MODULES}
    cells = ''.join(f'<figure class="ph"><a href="assets/images/slides/full/{k}.jpg" target="_blank" rel="noopener"><img src="assets/images/slides/{k}.jpg" loading="lazy" alt="{esc(v)}"></a>'
                    f'<figcaption><b>{i+1}.</b> {v}<br><a href="lessons/{slug[where[k][0]]}/index.html#photos">→ {where[k][1]}</a></figcaption></figure>' for i, (k, v) in enumerate(PHOTOS.items()))
    body = f'<p class="crumbs"><a href="index.html">Home</a> › Lecture slide gallery</p><h1>Lecture slide gallery</h1><p class="lead">All 11 photos of the lecture slides and blackboard from the study pack, in lecture order. Click a photo for the full-resolution picture (4000×3000); each caption links to the lesson that uses it.</p><div class="phgrid">{cells}</div>'
    write('slides-gallery.html', page('Lecture slide gallery', body, 0, desc='Photos of the lecture slides and blackboard', scripts=['theme.js']))
