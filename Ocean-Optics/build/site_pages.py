# -*- coding: utf-8 -*-
"""Site-level pages for Ocean Optics: home, calculators, mock exams, formulas, lecture slides, sources and limits."""
import random, json, os
from lib import *
import papers as PP
import core_map as CM
LENRANK = {}

def inp(i, label, v, step='any', w=None):
    st = f' style="width:{w}px"' if w else ''
    return f'<label>{label}<input id="{i}" type="number" step="{step}" value="{v}"{st}></label>'

def calculators_page():
    def box(cid, title, intro, inputs, out, cv=False):
        c = f'<canvas id="{out[:2]}_cv" width="760" height="300"></canvas>' if cv else ''
        return f'<section class="calc" id="{cid}"><h2>{title}</h2><p>{intro}</p><div>{inputs}</div><div class="res" id="{out}"></div>{c}</section>'
    sel = '<label>Formula<select id="vw_f"><option value="morel">Morel 1974 (slide 20)</option><option value="buiteveld">Buiteveld 1994 (slide 23)</option></select></label>'
    body = ('<p class="crumbs"><a href="index.html">Home</a> › Calculators</p><h1>Practice calculators</h1>'
            '<p class="lead">Ten tools that run in your browser (no server). Every formula comes from the lecture or the textbook (named in each box); results are tested automatically against Python — see <code>tests/test_calc.js</code> and <code>data/verified.json</code>.</p>') + \
        box('beer', '1 · Beer–Lambert and attenuation (modules A, E)', 'T = e<sup>−cL</sup>; c = −ln T/L (slide 5 without gain terms). Defaults: c = 1 m⁻¹, L = 0.25 m (illustrative path).', inp('be_c', 'c (m⁻¹)', 1) + inp('be_L', 'Path L (m)', 0.25) + inp('be_T', 'Measured T (for reverse)', 0.9), 'be_out', True) + \
        box('vsfw', '2 · Pure-water VSF and b<sub>w</sub> (module B)', 'β<sub>w</sub> = A(λ/500)<sup>e</sup>(1 + 0.3S/37)·10⁻⁴[1 + cos²θ(1−δ)/(1+δ)] (slides 20, 23); b<sub>w</sub> = 2πβ(90°)(2 + 2k/3).', inp('vw_l', 'λ (nm)', 500) + inp('vw_s', 'Salinity S', 37) + sel, 'vw_out', True) + \
        box('expabs', '3 · CDOM / NAP exponential absorption (module C)', 'a(λ) = a(λ₀)exp[−S(λ−λ₀)]. CDOM S′ ≈ 0.014, NAP S ≈ 0.011 nm⁻¹ (slides 35, 41).', inp('ea_a', 'a(λ₀) (m⁻¹)', 0.3) + inp('ea_l0', 'λ₀ (nm)', 412) + inp('ea_s', 'S (nm⁻¹)', 0.014) + inp('ea_l', 'λ (nm)', 443), 'ea_out', True) + \
        box('package', '4 · Package effect Q*<sub>a</sub> (module C)', 'Q*<sub>a</sub>(ρ) = (3/2)[1 + 2e<sup>−ρ</sup>/ρ + 2(e<sup>−ρ</sup>−1)/ρ²]/ρ for a homogeneous sphere (Morel &amp; Bricaud 1981 form; ρ = intracellular absorption × diameter, illustrative). Concept: slide 33.', inp('pk_r', 'ρ', 1), 'pk_out') + \
        box('bplaw', '5 · Particle scattering power law (module D)', 'b<sub>p</sub>(λ) = b<sub>p</sub>(550)(λ/550)<sup>n</sup> (slide 49). n = 0, −1, −3.', inp('bl_b', 'b<sub>p</sub>(550) (m⁻¹)', 1) + inp('bl_n', 'n', -1) + inp('bl_l', 'λ (nm)', 440), 'bl_out', True) + \
        box('sumns', '6 · IOP = Σ N·Q·S (modules F)', 'c = (N/V)·Q·πr² for one population (slide 63).', inp('sn_r', 'Radius r (µm)', 5) + inp('sn_n', 'N/V (m⁻³)', '1e7') + inp('sn_q', 'Q', 2), 'sn_out') + \
        box('bpchl', '7 · b<sub>p</sub> from Chl (module F)', 'b<sub>p</sub>(550) = 0.30·Chl<sup>0.7</sup> (slide 65, Loisel &amp; Morel 1998; Case-1 regression).', inp('bc_chl', 'Chl (mg m⁻³)', 1), 'bc_out') + \
        box('euphotic', '8 · Euphotic and Secchi depth (module G, textbook)', 'z<sub>1%</sub> = 4.605/K<sub>d</sub>; z<sub>SD</sub> = Γ/(K<sub>d</sub> + c), Γ ≈ 6–9 (Textbook: K functions; The Secchi Disk).', inp('eu_k', 'K<sub>d</sub> (m⁻¹)', 0.1) + inp('eu_c', 'c (m⁻¹)', 0.2) + inp('eu_g', 'Γ', 8), 'eu_out') + \
        box('pocspm', '9 · POC/SPM from particle absorption ratio (module F)', 'POC/SPM = 0.0133·exp(1.27 R), R = a<sub>p</sub>(675)/a<sub>p</sub>(570) (slide 74).', inp('pm_r', 'R', 1), 'pm_out') + \
        box('mixing', '10 · CDOM–salinity conservative mixing (module F)', 'a(S) = a<sub>fresh</sub>(1 − S/36) + a<sub>ocean</sub>S/36 (idea of slide 77; illustrative end members).', inp('mx_s', 'Salinity S', 18) + inp('mx_f', 'a<sub>fresh</sub>(355) (m⁻¹)', 10) + inp('mx_o', 'a<sub>ocean</sub>(355) (m⁻¹)', 0.1), 'mx_out')
    write('calculators.html', page('Calculators', body, 0, desc='Ocean Optics calculators that run in the browser', scripts=['theme.js', 'calc.js']))

def exam_sets(all_items, nsets=12, per=15):
    rng = random.Random(2026)
    by = {}
    for it in all_items: by.setdefault(it['mod'], []).append(it)
    for k in by: rng.shuffle(by[k])
    sets = []; ptr = {k: 0 for k in by}; mods = sorted(by)
    for s in range(nsets):
        pick = []; order = mods[s % len(mods):] + mods[:s % len(mods)]
        while len(pick) < per:
            progressed = False
            for m in order:
                if len(pick) >= per: break
                if ptr[m] < len(by[m]): pick.append(by[m][ptr[m]]); ptr[m] += 1; progressed = True
            if not progressed:       # banks exhausted: wrap around so every set has 15 questions
                ptr = {k: 0 for k in by}
        rng.shuffle(pick)
        sets.append([dict(q=p['q'], opts=p['opts'], correct=p['correct'], explain=p['explain'], src=f"{p['mod'].upper()} · {p['src']}") for p in pick])
    return sets

def _paper_html(pp):
    ids = {m[0]: m[1] for m in MODULES}
    qs = ''
    Q = pp['Q']; tot = sum(q['pts'] for q in Q)
    for q in Q:
        parts = ''.join(f'<p>{t}<span class="core" title="A = answerable from the Big 12; B = Big 12 frame + module facts; C = module-specific"> <b class="lv {l}">{l}</b> {" ".join(i)}</span></p>' for t, l, i in q['parts'])
        key = ''.join(f'<p>{k}</p>' for k in q['key'])
        qs += (f'<div class="qitem mock" data-q="{q["n"]}"><b>Question {q["n"]} ({q["pts"]:g} pts)</b> — <a href="lessons/{ids[q["ref"]]}/index.html">review {label(q["ref"])}</a>{parts}'
               f'<details class="ans"><summary>Show suggested answer key</summary><div class="keyans">{key}</div></details>'
               f'<label class="selfgrade">Self-grade (0–{q["pts"]:g}): <input type="number" min="0" max="{q["pts"]:g}" step="0.25" class="sg" data-q="{q["n"]}" value=""></label></div>')
    st = CM.stats([(f'{pp["id"]}Q{q["n"]}', 'x', x[1], x[2]) for q in Q for x in q['parts']])
    cov = (f'<p class="note"><b>Big-12 coverage of this paper</b> (own assessment of {st["n"]} parts): {st["A"]} answerable from the Big 12 alone (A), {st["B"]} need Big 12 + module facts (B), {st["C"]} module-specific (C) → frame of <b>{st["skeleton"]*100:.0f}%</b>, full answer of <b>{st["full"]*100:.0f}%</b> of the parts. These papers were written by me; they are not the lecturer’s exam.</p>')
    instr = '<ul><li>Answer in English, define symbols and units.</li><li>Give formulas, orders of magnitude and one-line justifications.</li><li>Numerical keys come from Python (data/verified.json).</li></ul>'
    return (f'<section class="paper" id="{pp["id"].lower()}" data-key="mock:{pp["id"].lower()}" data-seconds="{pp["minutes"]*60}">'
            f'<h2>{pp["title"]}</h2><p>{pp["intro"]}</p><div class="callout"><b class="t">Instructions</b>{instr}<p>{pp["minutes"]} minutes, closed book, calculator allowed. Tags: level A/B/C and the Big-12 items each part relies on.</p></div>{cov}'
            f'<div class="sim"><div class="simh">Clock and total score</div><span class="quiz-score mk_timer">Time: {pp["minutes"]}:00</span> <button class="btn mk_start">Start</button> <button class="btn alt mk_stop">Stop</button> <button class="btn alt mk_reset">Reset</button> '
            f'<span class="quiz-score mk_total" data-max="{tot:g}" style="margin-left:14px">Total: 0/{tot:g}</span></div>{qs}</section>')

def exam_page(all_items):
    sets = exam_sets(all_items, nsets=12)
    data = json.dumps(dict(sets=sets), ensure_ascii=False).replace('</', '<\\/')
    allp = PP.all_parts(); st = CM.stats(allp)
    chips = ''.join(f'<a href="#{pp["id"].lower()}">{pp["title"].split(" — ")[0]} · {pp["title"].split(" — ")[1].split(" (")[0]}</a>' for pp in PP.PAPERS) + '<a href="#mcq">MCQ practice</a>'
    papers = ''.join(_paper_html(pp) for pp in PP.PAPERS)
    body = f'''<p class="crumbs"><a href="index.html">Home</a> › Mock exams</p><h1>Mock exams</h1>
<p class="lead">Five written papers ({len(PP.PAPERS)*4} questions, {st["n"]} parts) and twelve multiple-choice practice exams (15 questions, 30 minutes). <b>No exam from the lecturer was available</b>: everything here was written for this site from the 120 slides and the textbook.</p>
<div class="paperhd">{chips}</div>
<div class="callout"><b class="t">How good is the Big 12 as a shortcut? (honest numbers)</b><p>Across the {st["n"]} parts of the five papers: <b>{st["A"]}</b> answerable from the Big 12 alone, <b>{st["B"]}</b> need the Big 12 plus module facts, <b>{st["C"]}</b> are module-specific. The Big 12 gives the frame of <b>{st["skeleton"]*100:.0f}%</b> of the parts. This is my own assessment of my own papers; it says nothing certain about the real exam.</p></div>
{papers}
<h2 id="mcq">Multiple-choice practice (15 questions, 30 minutes)</h2>
<p>Twelve sets, each drawing from all {len(MODULES)-1} modules. Submit to see your score and an explanation for every question.</p><div id="exam"></div>
<script id="exam-data" type="application/json">{data}</script>'''
    write('exam.html', page('Mock exams', body, 0, desc='Five written mock papers and twelve multiple-choice practice exams', scripts=['theme.js', 'exam.js', 'mock.js', 'gate.js']))

def reference_page():
    rows = [
     ('RTE', 'dL/dr = −cL + (in-scattering with β) + S; c = a + b', 'Lecture', '5', 'ma'),
     ('IOP definitions', 'a(λ) = lim Φ_a/(Φ_i Δr) [m⁻¹]; β(ψ,λ) = lim Φ_s/(Φ_i Δr ΔΩ) [m⁻¹ sr⁻¹]', 'Lecture', '17', 'ma'),
     ('Scattering', 'b = 2π∫β sinθ dθ; b_f: 0→π/2; b_b: π/2→π; c = a + b', 'Lecture', '18', 'ma'),
     ('Additivity', 'a = a_w + a_CDOM + a_ph + a_NAP; b = b_w + b_p; b_b = b_bw + b_bp', 'Lecture', '19', 'ma'),
     ('Beer–Lambert', 'L = L₀ e^(−cr); T = e^(−cL); c = −ln T/L', 'Lecture + Home-made check', '5, 60', 'me'),
     ('Pure-water VSF (Morel)', 'β_w = 1.38(λ/500)^−4.32 (1+0.3S/37) 10⁻⁴ [1 + cos²θ(1−δ)/(1+δ)], δ = 0.09 (printed “cos2θ”; read as cos²θ)', 'Lecture', '20', 'mb'),
     ('Pure-water VSF (Buiteveld)', '1.29, λ^−4.14, δ = 0.051', 'Lecture', '23', 'mb'),
     ('b_w closed form', 'b_w = 2πβ(90°)(2 + 2k/3), k = (1−δ)/(1+δ); b_bw = b_w/2', 'Home-made check', '—', 'mb'),
     ('Einstein–Smoluchowski', 'β(ψ) = (2π²kT/(λ⁴β_T)) n²(∂n/∂P)² (6+6ρ)/(6−7ρ) [1 + (1−ρ)/(1+ρ) cos²ψ]; β(90°, 546) = 0.869×10⁻⁴', 'Textbook: Physics of Scattering', '—', 'mb'),
     ('Package effect', 'Q*_a = a_φ/a_sol; a_sol = Σ C_i a*_sol,i', 'Lecture', '33', 'mc'),
     ('Package, sphere', 'Q*_a(ρ) = (3/2)[1 + 2e^−ρ/ρ + 2(e^−ρ−1)/ρ²]/ρ', 'Home-made check (Morel & Bricaud 1981 form)', '—', 'mc'),
     ('CDOM / NAP', 'a(λ) = a(λ₀) exp[−S(λ−λ₀)]; S′ ≈ 0.014 (CDOM), S ≈ 0.011 (NAP) nm⁻¹; a ∝ λ^−6.92 alternative', 'Lecture; Textbook: CDOM', '35, 41', 'mc'),
     ('Particle scattering', 'b_p(λ) = b_p(550)(λ/550)^n, n ∈ [−3, 0], mean −1', 'Lecture', '49', 'md'),
     ('Absorption effect on b_p', 'Δb_p/a_p = 1 − tanh(0.5 γ²)', 'Lecture', '53', 'md'),
     ('Backscatter retrieval', 'β_p(117°) = β − β_w; b_bp = 2π χ β_p(117°)', 'Lecture', '62', 'me'),
     ('IOP and particles', 'IOP = Σ (N_i/V) σ_i = Σ (N_i/V) Q_i S_i', 'Lecture', '63', 'mf'),
     ('PSD and attenuation slope', 'N(D) = N₀(D/D₀)^−ξ; c_p = Aλ^−γ; ξ = γ + 3; ξ = γ + 3 − 0.5 exp(−6γ)', 'Lecture; Mie check', '68', 'mf'),
     ('Particles and Chl', 'b_p(550) = 0.30 Chl^0.7; POC/SPM = 0.0133 exp(1.27 a_p(675)/a_p(570))', 'Lecture', '65, 74', 'mf'),
     ('K_d, reflectance', 'K_d ≡ −d ln E_d/dz; E_d(z) = E_d(0)e^(−K_d z); R = E_u/E_d; R_rs = L_w/E_d [sr⁻¹]; a ≤ K_d μ̄_d ≤ c', 'Textbook', '—', 'mg'),
     ('Euphotic / Secchi', 'z_1% = 4.605/K_d; z_SD = Γ/(K_dv + c_v), Γ ≈ 6–9; Lee et al.: z_SD = γ/(2.5 K_d(λ_min))', 'Textbook', '—', 'mg'),
    ]
    ids = {m[0]: m[1] for m in MODULES}
    tb = ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td><span class="tag">{c}</span></td><td>{d}</td><td><a href="lessons/{ids[m]}/index.html">{label(m)}</a></td></tr>' for a, b, c, d, m in rows)
    gl = [('IOP', 'Inherent optical property (a, b, β, c, b_b)'), ('AOP', 'Apparent optical property (K_d, R, R_rs)'), ('VSF', 'Volume scattering function β(ψ,λ)'), ('CDOM', 'Coloured dissolved organic matter (yellow substance)'),
          ('NAP', 'Non-algal particles (detritus, minerals)'), ('POC', 'Particulate organic carbon'), ('SPM', 'Suspended particulate matter'), ('DOC', 'Dissolved organic carbon'), ('PSD', 'Particle size distribution'),
          ('BGC-Argo', 'Biogeochemical Argo floats'), ('OWC', 'Optical water class'), ('Chl', 'Chlorophyll a concentration (mg m⁻³)')]
    g = ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td></tr>' for a, b in gl)
    body = f'''<p class="crumbs"><a href="index.html">Home</a> › Formulas</p><h1>Formulas and acronyms</h1>
<p class="lead">Every formula carries its source label: <b>Lecture</b> (slide number), <b>Textbook</b> (oceanopticsbook.info, CC BY 2.0) or <b>Home-made check</b> (Python).</p>
<table class="lg"><tr><th>Name</th><th>Formula</th><th>Source</th><th>Slide</th><th>Module</th></tr>{tb}</table>
<h2>Acronyms</h2><table class="lg"><tr><th>Term</th><th>Meaning</th></tr>{g}</table>'''
    write('reference.html', page('Formulas', body, 0, desc='Formulas and acronyms with sources', scripts=['theme.js']))

def resources_page():
    d = VERIFIED
    body = f'''<p class="crumbs"><a href="index.html">Home</a> › Sources and limits</p><h1>Sources, checks and limits</h1>
<h2>Sources</h2><ul>
<li><b>Lecture:</b> <i>Marine Optics</i>, Hubert Loisel, Laboratoire d’Océanologie et de Géosciences (LOG), file “Optique-marine-English-UBATUBA”, 120 slides. Slide figures shown here are small selected pages with credit to the lecturer; each slide also credits its original authors (Bricaud, Babin, Snyder, Boss, Claustre…).</li>
<li><b>Textbook:</b> <a href="https://oceanopticsbook.info/">Ocean Optics Web Book</a>, footer: “2020 Creative Commons Attribution license” (CC BY 2.0). We cite page titles and URLs and <b>do not copy its images</b>; all curves on this site are our own computations.</li>
<li><b>Home-made checks:</b> <code>build/verify_numbers.py</code> → <code>data/verified.json</code>: {d["n_checks"]} cross-checks, {d["n_ok"]} passed, discrepancies: {len(d["discrepancies"])}.</li></ul>
<h2>What was verified, and how</h2><ul>
<li>Pure-water b<sub>w</sub>: numerical integration vs closed form; exponent ratios vs numerical integral of the whole VSF.</li>
<li>Mie computations (Bohren–Huffman series with spherical Bessel functions): Q<sub>sca</sub> by series vs angular quadrature; Rayleigh limit vs closed form; Q<sub>ext</sub> vs anomalous diffraction; Junge ensemble exponents by two fitting methods.</li>
<li>Exponential laws: log-fit vs nonlinear fit; Beer–Lambert: closed form vs ODE; package effect: closed form vs ray-path quadrature; euphotic/Secchi: closed form vs root finding.</li>
<li>Browser calculators are tested in Node against Python (<code>tests/test_calc.js</code>).</li></ul>
<h2>Where the lecture and the textbook disagree (kept, not hidden)</h2><ul>
<li><b>Radiative transfer equation:</b> slide 5 prints a factor 2π before the scattering integral; the textbook writes ∫β L dω′ over 4π without it.</li>
<li><b>Pure-water VSF:</b> the slide formula at 546 nm, S = 0 gives β(90°) = {d["beta90_546_morel_S0"]*1e4:.3f}×10⁻⁴ m⁻¹ sr⁻¹ (Morel form) and {d["beta90_546_buiteveld_S0"]*1e4:.3f}×10⁻⁴ (Buiteveld form); the textbook quotes 0.869×10⁻⁴ (its own computation from listed constants gives {d["es_beta90_546_textbook_constants"]*1e4:.3f}×10⁻⁴, 1.7 % lower) and recalls 0.83×10⁻⁴ for Morel (1974). We did not find the convention that reconciles them.</li>
<li><b>Angular term:</b> the slide prints “cos2θ”; we read cos²θ because it reproduces b<sub>w</sub>(500) ≈ 3×10⁻³ m⁻¹ read from slide 24 ({d["bw500_S37_cos_sq"]*1e3:.2f}×10⁻³), while cos(2θ) would give {d["bw500_S37_cos2"]*1e3:.2f}×10⁻³. Evidence, not proof.</li>
<li><b>Depolarisation:</b> 0.09 (Morel) and 0.051 (Buiteveld) on the slides vs ρ = 0.031 (Zhang et al. 2019) in the textbook.</li>
<li><b>Junge slope:</b> the lecture uses N(D) ∝ D<sup>−ξ</sup> with ξ = γ + 3; the textbook’s Junge law is dN/dlogD ∝ D<sup>−3</sup> ⇔ n(D) ∝ D<sup>−4</sup>, so the same distribution has ξ = 4 in the lecture notation.</li></ul>
<h2>Honest limits</h2><ul>
<li><b>No sample exam, no syllabus.</b> The lecturer’s exam is unknown. “Coverage” numbers describe only the five papers I wrote; they are not a prediction.</li>
<li><b>All questions are mine.</b> No original questions existed, so every item is labelled “bo_sung” (added) and carries its slide or textbook source.</li>
<li><b>No AOP slides in the lecture file.</b> Outline slide 9 lists “Link between IOPs and the light field”, but module G is textbook-only and labelled so. The relation R ≈ f b<sub>b</sub>/(a+b<sub>b</sub>) was not found on the crawled textbook pages and is only used qualitatively (classical result, Gordon et al. 1975).</li>
<li><b>Values read from graphs</b> are approximate (≈ 10–20 %) and always labelled; some slides (s4, 6, 7 images, 73, 78 and the small web-viewer screenshots 116–118) were not read in detail and are used only through their text.</li>
<li><b>Mie spheres</b> are a model; they are used to check exponents and trends, not to claim measured values. Simple models are illustrations, not data.</li>
<li>Progress is stored in your browser (localStorage). No Chinese version. Slide images remain the property of their authors.</li></ul>'''
    write('resources.html', page('Sources and limits', body, 0, desc='Sources, checks and limits', scripts=['theme.js']))

def index_page(stats):
    n_s = sum(s['slides'] for s in stats); n_m = sum(s['mcq'] for s in stats); n_e = sum(s['ess'] for s in stats)
    cards = ''
    for (mid, slug, title, en), st in zip(MODULES, stats):
        hot = ' style="border-color:#ED1C24;border-width:3px"' if mid == 'p0' else ''
        cards += (f'<a class="mod-card"{hot} href="lessons/{slug}/index.html"><div class="num">{label(mid)}</div><h3>{esc(title)}</h3><p>{esc(en)}</p>'
                  f'<p class="tag">{st["slides"]} slides</p><p class="tag">{st["mcq"]} MCQ</p><p class="tag">{st["ess"]} essays</p></a>')
    L = LENRANK; d = VERIFIED
    audit = (f'<p>Answer-position audit over {int(L.get("n", 0))} multiple-choice questions: A/B/C/D = ' + ' / '.join(f'{p*100:.0f}%' for p in L.get('pos', [0, 0, 0, 0])) +
             f'; correct answer is the longest option in {L.get("longest", 0)*100:.0f}% and the shortest in {L.get("shortest", 0)*100:.0f}% of cases.</p>') if L else ''
    body = f'''<p class="crumbs">Home</p>
<div class="usth-banner"><img src="assets/images/usth_logo.png" alt="USTH"><div><div class="t">Ocean Optics — self-study and exam practice</div><div class="s">Based on the lecture “Marine Optics” (H. Loisel) and the Ocean Optics Web Book · USTH</div></div></div>
<p class="lead">Start here plus {len(MODULES)-1} modules, {n_s} slides, {n_m} multiple-choice questions with explanations, {n_e} essay questions, 10 browser calculators, 5 written mock papers and 12 multiple-choice mock exams. Everything is in English; short Vietnamese hints are given as memory aids.</p>
<div class="callout"><b class="t">Start here</b>Read the <a href="lessons/start-here/index.html"><b>Big 12</b></a> (15 minutes) and pass the 12-question check before the modules. The lecture slides contain many graphs that are explained in words in each module.</div>
<h2>Modules</h2><div class="grid">{cards}</div>
<h2>Tools</h2><p><a class="btn" href="calculators.html">Calculators</a> <a class="btn" href="exam.html">Mock exams</a> <a class="btn" href="reference.html">Formulas</a> <a class="btn" href="lecture-slides.html">Lecture slides</a> <a class="btn" href="resources.html">Sources and limits</a></p>
<h2>Status and limits</h2><ul>
<li>Sources are only the lecture (120 slides) and the textbook; <b>no sample exam, no syllabus</b>: the coverage numbers refer to the papers written here.</li>
<li>Numbers were recomputed in Python with two independent methods ({d["n_ok"]}/{d["n_checks"]} cross-checks passed); simple models (Mie spheres, package sphere) are illustrations, not data.</li>
<li>Values read from graphs are approximate and labelled; the module on the light field (G) is textbook-only because the lecture file has no slide on it.</li>
<li>Lecture and textbook differ in a few places (RTE factor 2π, pure-water β values, depolarisation); see <a href="resources.html">Sources and limits</a>.</li>
<li>Progress is saved in your browser only. Slide images belong to their authors; the textbook is CC BY 2.0 and its images are not copied.</li></ul>
{audit}'''
    write('index.html', page('Home', body, 0, desc='Ocean Optics self-study site for USTH', scripts=['theme.js']))

def lecture_gallery_page():
    import lecture_pages as LP
    chips = '<button class="btn" data-g="all">All</button> ' + ' '.join(f'<button class="btn alt" data-g="{k}">{t}</button>' for k, t, m in LP.GROUPS)
    cells = ''.join(f'<figure class="ph" data-g="{g}"><a href="assets/images/lecture/full/p{p:03d}.jpg" target="_blank" rel="noopener"><img src="assets/images/lecture/thumb/p{p:03d}.jpg" loading="lazy" alt="{esc(t)}"></a><figcaption><b>Slide {p}</b> {esc(t)}</figcaption></figure>' for p, g, t in LP.P)
    body = f'''<p class="crumbs"><a href="index.html">Home</a> › Lecture slides</p><h1>Lecture slides ({len(LP.P)} selected pages)</h1>
<p class="lead">Selected pages of “Marine Optics” (H. Loisel, LOG), grouped by topic. Click a page to enlarge. Descriptions are ours; the original figures are credited on each slide.</p>
<div class="row">{chips}</div><div class="phgrid" id="gal">{cells}</div>
<script>(function(){{var b=document.querySelectorAll('[data-g]');[].forEach.call(document.querySelectorAll('button[data-g]'),function(x){{x.onclick=function(){{var g=x.getAttribute('data-g');[].forEach.call(document.querySelectorAll('figure.ph'),function(f){{f.style.display=(g==='all'||f.getAttribute('data-g')===g)?'':'none'}})}}}})}})();</script>'''
    write('lecture-slides.html', page('Lecture slides', body, 0, desc='Selected lecture slides', scripts=['theme.js']))
