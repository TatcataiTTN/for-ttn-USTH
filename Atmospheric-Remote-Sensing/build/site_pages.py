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
           '<p class="lead">Sixteen tools that run in your browser (no server). All formulas come from the study guide; the results are tested automatically against Python (including the averaging-kernel matrices) — see <code>tests/test_calc.js</code> and the notebook.</p>' + \
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
        box('ddoas', '12 · DOAS differential optical depth (Part A.6)', 'D = σ′·SCD (fraction of signal ≈ D). Default: mock exam Q10(c).', inp('dd_s', 'σ′ (cm²)', '2e-19') + inp('dd_c', 'SCD (molecule cm⁻²)', '1e16'), 'dd_out') + \
        box('lidar', '13 · Lidar equation: can the lidar detect it? (Part D)', 'P(z) = K/z² · (β<sub>m</sub> + β<sub>p</sub>) · T². Defaults: lecture exercise 1(a) — particle layer at 1 km.',
            inp('li_K', 'K (W m³ sr)', '1e5') + inp('li_z', 'Distance z (km)', 1) + inp('li_bm', 'β<sub>m</sub> (m⁻¹ sr⁻¹)', '1e-6') + inp('li_bp', 'β<sub>p</sub> (m⁻¹ sr⁻¹)', '1e-6') + inp('li_T', 'One-way transmission T', 0.7) + inp('li_min', 'Detection limit (nW)', 1), 'li_out') + \
        box('dial', '14 · Water-vapour DIAL (Part D)', 'α<sub>H₂O</sub> = (1/2Δr)·ln[P<sub>OFF</sub>(r₁)·P<sub>ON</sub>(r₂) / (P<sub>ON</sub>(r₁)·P<sub>OFF</sub>(r₂))]; q (g/kg) = 5×10⁴·α. Defaults: lecture exercise 2.',
            inp('di_on1', 'P<sub>ON</sub>(r₁) (nW)', 10) + inp('di_on2', 'P<sub>ON</sub>(r₂) (nW)', 7) + inp('di_off1', 'P<sub>OFF</sub>(r₁) (nW)', 10) + inp('di_off2', 'P<sub>OFF</sub>(r₂) (nW)', 8) + inp('di_dr', 'Δr (m)', 500) + inp('di_f', 'q/α factor (g/kg per m⁻¹)', '5e4'), 'di_out') + \
        box('hydro', '15 · Hydrostatic pressure and scale height (Part B)', 'p = p₀·exp(−z/H), H = RT/(Mg) ≈ 8.3 km at 284 K (isothermal). Real atmosphere: 265 hPa at 10 km because T falls with height.',
            inp('hy_p0', 'Surface pressure (hPa)', 1013.25) + inp('hy_T', 'Mean T (K)', 284) + inp('hy_z', 'Altitude z (km)', 10), 'hy_out', True) + \
        box('sinks', '16 · Which sink dominates? (Part B / Ch. 1)', 'Rates k = 1/τ add up; the share of each pathway is k<sub>i</sub>/k<sub>tot</sub>. Defaults: lecture example (chemistry 1 d, rain once a week, outflow of a 100 km city at 20 km/h = 5 h).',
            inp('sk_c', 'τ<sub>chem</sub> (days)', 1) + inp('sk_d', 'τ<sub>dep</sub> (days)', 7) + inp('sk_o', 'τ<sub>out</sub> (hours)', 5), 'sk_out')
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

def _ref(q):
    ids = {m[0]: m[1] for m in MODULES}
    if 'ch' in q:
        mid = 'pa' if q['ch'] == 0 else f"m{q['ch']}"
        return ids[mid], (q.get('ref') or f"Ch. {q['ch']}")
    return ids[q['ref']], label(q['ref'])

def _paper_html(pid, title, minutes, intro, Q, instr, parts_levels, legacy_key=False):
    """One written paper: clock, self-grade per question, answer key, level A/B/C and Big-12 items for every part."""
    import core_map as CM
    qs = ''
    tot = sum(q['pts'] for q in Q)
    for q in Q:
        lv = parts_levels[q['n']]
        parts = ''.join(f'<p>{t}<span class="core" title="A = answerable from the Big 12; B = Big 12 skeleton + module facts; C = module-specific"> <b class="lv {l}">{l}</b> {" ".join(ids)}</span></p>' for t, (l, ids) in zip(q['parts'], lv))
        key = ''.join(f'<p>{k}</p>' for k in q['key'])
        qs += (f'<div class="qitem mock" data-q="{q["n"]}"><b>Question {q["n"]} ({q["pts"]:g} pts)</b> — <a href="lessons/{_ref(q)[0]}/index.html">review {_ref(q)[1]}</a>{parts}'
               f'<details class="ans"><summary>Show suggested answer key</summary><div class="keyans">{key}</div></details>'
               f'<label class="selfgrade">Self-grade (0–{q["pts"]:g}): <input type="number" min="0" max="{q["pts"]:g}" step="0.25" class="sg" data-q="{q["n"]}" value=""></label></div>')
    st = CM.stats([(f'Q{q["n"]}', 'x', l, ids) for q in Q for (l, ids) in parts_levels[q['n']]])
    cov = (f'<p class="note"><b>Big-12 coverage of this paper</b> (own assessment of {st["n"]} parts): {st["A"]} answerable from the Big 12 alone (A), {st["B"]} need Big 12 + module facts (B), {st["C"]} module-specific (C) → '
           f'Big 12 gives the skeleton of <b>{st["skeleton"]*100:.0f}%</b> and the full answer of <b>{st["full"]*100:.0f}%</b> of the parts.</p>')
    return (f'<section class="paper" id="{pid}" data-key="{"mock-selfgrade" if legacy_key else "mock:" + pid}" data-seconds="{minutes*60}">'
            f'<h2>{title}</h2><p>{intro}</p><div class="callout"><b class="t">Instructions</b>{instr}<p>{minutes} minutes, closed book, calculator allowed. Tags after each part: level A/B/C and the Big-12 items it relies on.</p></div>{cov}'
            f'<div class="sim"><div class="simh">Clock and total score</div><span class="quiz-score mk_timer">Time: {minutes}:00</span> <button class="btn mk_start">Start</button> <button class="btn alt mk_stop">Stop</button> <button class="btn alt mk_reset">Reset</button>'
            f'<span class="quiz-score mk_total" data-max="{tot:g}" style="margin-left:14px">Total: 0/{tot:g}</span></div>{qs}</section>')

def paper_levels_p1():
    import core_map as CM
    out = {}
    for (q, part, lv, ids) in CM.P1: out.setdefault(int(q[1:]), []).append((lv, ids))
    return out

def exam_page(all_items):
    import papers as PP, core_map as CM
    sets = exam_sets(all_items, nsets=12)
    data = json.dumps(dict(sets=sets), ensure_ascii=False).replace('</', '<\\/')
    instr = '<ul>' + ''.join(f'<li>{i}</li>' for i in ME.INSTR) + '</ul>'
    grading = '<ul>' + ''.join(f'<li>{g}</li>' for g in ME.GRADING) + '</ul>'
    p1 = _paper_html('p1', 'Paper 1 — Original mock exam v2 (official sample)', 120, 'The mock exam supplied with the study guide: 10 questions (Part A: Q9–Q10; chapters 1–8: Q1–Q8).', ME.Q, instr, paper_levels_p1(), legacy_key=True)
    others = ''
    for pp in PP.PAPERS:
        lv = {q['n']: [(x[1], x[2]) for x in q['parts']] for q in pp['Q']}
        Qd = [dict(n=q['n'], ref=q['ref'], pts=q['pts'], parts=[x[0] for x in q['parts']], key=q['key']) for q in pp['Q']]
        others += _paper_html(pp['id'].lower(), pp['title'], pp['minutes'], pp['intro'], Qd, instr, lv)
    chips = ''.join(f'<a href="#{pid}">{t}</a>' for pid, t in [('p1', 'Paper 1 · official'), ('p2', 'Paper 2 · foundations'), ('p3', 'Paper 3 · retrieval & aerosols'), ('p4', 'Paper 4 · lidar & integration'), ('p5', 'Paper 5 · calculation drill'), ('mcq', 'MCQ sets')])
    allparts = list(CM.P1) + [(f'{pp["id"]}Q{q["n"]}', 'x', x[1], x[2]) for pp in PP.PAPERS for q in pp['Q'] for x in q['parts']]
    st = CM.stats(allparts)
    body = f'''<p class="crumbs"><a href="index.html">Home</a> › Mock exams</p><h1>Mock exams</h1>
<p class="lead">Five written papers (Paper 1 is the official sample, Papers 2–5 are new: 34 questions, {st["n"]} parts in total) and twelve multiple-choice practice exams (15 questions, 30 minutes) generated from the question banks of all {len(MODULES)} modules. <b>Do the <a href="lessons/start-here/index.html">Big 12</a> first.</b></p>
<div class="paperhd">{chips}</div>
<div class="callout"><b class="t">How good is the Big 12 as a shortcut? (honest numbers)</b><p>Across all {st["n"]} parts of the five papers: <b>{st["A"]}</b> are answerable from the Big 12 alone, <b>{st["B"]}</b> need the Big 12 plus module facts, <b>{st["C"]}</b> are module-specific. The Big 12 gives the skeleton of <b>{st["skeleton"]*100:.0f}%</b> of the parts and the complete answer of <b>{st["full"]*100:.0f}%</b>. On the official Paper 1 alone: {CM.stats(CM.P1)["skeleton"]*100:.0f}% skeleton, {CM.stats(CM.P1)["full"]*100:.0f}% complete. These levels are my own assessment; the real exam is unknown.</p></div>
{p1}
{others}
<h2 id="mcq">Multiple-choice practice (15 questions, 30 minutes)</h2>
<p>Twelve sets, each drawing questions from all {len(MODULES)} modules. Submit to see your score and an explanation for every question.</p><div id="exam"></div>
<div class="callout good"><b class="t">Grading hints</b>{grading}</div>
<script id="exam-data" type="application/json">{data}</script>'''
    write('exam.html', page('Mock exams', body, 0, desc='Five written mock papers and twelve multiple-choice practice exams', scripts=['theme.js', 'exam.js', 'mock.js', 'gate.js']))

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
         ('Line widths', 'Doppler ∝ ν̃√(T/m) ; Lorentz ∝ P (T₀/T)ⁿ ; Voigt = both', 'Part A.5'), ('DOAS (differential)', 'σ = σ_b + σ′ ; D = ln(I′₀/I) = σ′·c·L', 'Part A.6'),
         ('Hydrostatic law', 'dp/dz = −ρg ; p = p₀exp(−z/H) ; H = RT/(Mg) ≈ 8.3 km (284 K) ; half pressure every H ln 2 ≈ 5.75 km', 'Part B'),
         ('Sinks (rates add)', 'k_tot = Σkᵢ ; τ = 1/k_tot ; share_i = kᵢ/k_tot ; τ_out = size/wind', 'Part B, Ch.1'),
         ('Photon energy', 'E = hc/λ : 2.92 eV at 424 nm (NO₂ photolysis), 5.17 eV at 240 nm (O₂)', 'Part B'),
         ('Cost function', 'J(x) = [y − F(x)]ᵀS_y⁻¹[y − F(x)] + [x − xₐ]ᵀR[x − xₐ]', 'Part C'),
         ('Gauss–Newton', 'xᵢ₊₁ = xᵢ + (KᵢᵀS_e⁻¹Kᵢ + C)⁻¹[KᵢᵀS_e⁻¹(y − F(xᵢ)) − C(xᵢ − xₐ)]', 'Part C'),
         ('Lidar range', 'R = c·t/2 ; ΔR = c·τ_L/2', 'Part D'),
         ('Lidar equation', 'P(z) = K/z² · β(z) · T²(z) ; β = β_m + β_p ; T = exp(−∫α dz)', 'Part D'),
         ('DIAL', 'α_H₂O = (1/2Δr)·ln[P_OFF(r₁)P_ON(r₂)/(P_ON(r₁)P_OFF(r₂))] ; q(g/kg) = 5×10⁴ α(m⁻¹)', 'Part D'),
         ('Big 12 · F1, F2, F3', 'I = I₀e^(−τ) ; dI/dl = −k_ext I + J ; x̂ = xₐ + A(x − xₐ) + ε', 'Start here')]
    A = [('AOD', 'Aerosol Optical Depth'), ('AMF / SCD / VCD', 'Air Mass Factor / Slant / Vertical Column Density'), ('AK, DOFS', 'Averaging Kernel, Degrees Of Freedom for Signal'),
         ('DOAS', 'Differential Optical Absorption Spectroscopy'), ('TOA', 'Top Of Atmosphere'), ('RTE', 'Radiative Transfer Equation'), ('LUT', 'Look-Up Table'),
         ('ALH', 'Aerosol Layer Height'), ('UVAI', 'UV Absorbing Aerosol Index'), ('TROPOMI, OMI, GOME-2', 'UV–vis–SWIR nadir spectrometers'), ('IASI, AIRS, CrIS', 'Thermal-IR nadir sounders'),
         ('MLS, MIPAS, OSIRIS', 'Limb sounders'), ('SAGE, ACE-FTS', 'Solar occultation instruments'), ('CALIOP, ATLID', 'Space lidars (active)'), ('DIAL', 'Differential Absorption Lidar'), ('IASI+GOME-2', 'Multispectral IR+UV ozone retrieval (lecture)'), ('AEROIASI, AEROS5P', '3D aerosol retrievals from IASI (thermal IR) and TROPOMI (O₂ A band)'),
         ('CHIMERE', 'Regional chemistry-transport model'), ('VOC, NOx', 'Volatile organic compounds; NO + NO₂'), ('PSC', 'Polar stratospheric cloud'), ('LMT', 'Lowermost troposphere (< 3 km)'), ('HONO', 'Nitrous acid, a source of OH'), ('AERONET', 'Ground sun-photometer network (AOD)')]
    t1 = hx_table(['Concept', 'Formula / value', 'Chapter'], [[a, f'<span class="mono">{b}</span>', c] for a, b, c in F], 'left')
    t2 = hx_table(['Acronym', 'Meaning'], [[a, b] for a, b in A], 'left')
    body = f'''<p class="crumbs"><a href="index.html">Home</a> › Formulas & acronyms</p><h1>Formulas and acronyms</h1>
<p class="lead">The formula sheet and acronyms of the study guide v2 (Part C) plus the formulas of the lecture master (Parts B, C, D and the Big 12), with a quick filter.</p>
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
            ('f25_hydrostatic', 'Hydrostatic law: model against lecture table (Part B)'), ('f26_sinks_pathways', 'Loss pathways of a city plume (Part B)'), ('f27_o3_cycle', 'Tropospheric ozone: NOx cycle and peroxy radicals (Part B)'),
            ('f30_multispectral', 'IASI, GOME-2 and IASI+GOME-2: DOFS and height of peak sensitivity (Part C)'), ('f28_lidar_exercise', 'Lidar exercise 1 signals against the detection limit (Part D)'), ('f29_dial', 'Water-vapour DIAL (Part D)'), ('f31_big12_map', 'The Big 12 map (Start here)'),
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
<a class="mod-card" href="lecture-slides.html"><div class="num">137 pages</div><h3>Lecture pages (Cuesta master course)</h3><p>137 selected pages of the lecture “Remote Sensing of the Atmosphere: a focus on air composition”, grouped by topic and linked to the lessons.</p></a>
<a class="mod-card" href="slides-gallery.html"><div class="num">11 photos</div><h3>Lecture slide gallery</h3><p>All class photos of slides and blackboard, with links to the matching lessons.</p></a>
<a class="mod-card" href="notebooks/verify_numbers.ipynb"><div class="num">IPYNB</div><h3>Number-verification notebook</h3><p>Python recomputes every number used on this site (executed, results saved).</p></a>
</div>
<h2>31 figures drawn by code (24 from study guide v2, 7 new)</h2><p style="font-size:.88rem;color:var(--muted)">Planck, Mie and line-width plots (f8, f10, f11, f20) are computed from the real equations; the others are schematic illustrations, as stated in the guide.</p>{gal}
<h2>11 lecture-slide photos</h2><p><a href="slides-gallery.html">Open the lecture slide gallery →</a></p>{gal2}'''
    write('resources.html', page('Resources', body, 0, desc='Study guide, mock exam and figures', scripts=['theme.js']))

LENRANK = dict(n=0, pos=[.25] * 4, longest=.25, shortest=.25)

def index_page(stats, ncalc=16):
    import core_map as CM, papers as PP
    cards = ''
    for (mid, slug, title, en), st in zip(MODULES, stats):
        hot = ' style="border-color:#ED1C24;border-width:3px"' if mid == 'p0' else ''
        cards += (f'<a class="mod-card"{hot} href="lessons/{slug}/index.html"><div class="num">{label(mid)}</div><h3>{esc(title)}</h3><p>{esc(en)}</p>'
                  f'<p class="tag">{st["slides"]} slides</p><p class="tag">{st["mcq"]} MCQ</p><p class="tag">{st["ess"]} essays</p></a>')
    tot = lambda k: sum(s_[k] for s_ in stats)
    allp = list(CM.P1) + [(f'{pp["id"]}Q{q["n"]}', 'x', x[1], x[2]) for pp in PP.PAPERS for q in pp['Q'] for x in q['parts']]
    cs = CM.stats(allp); nq = len(ME.Q) + sum(len(pp['Q']) for pp in PP.PAPERS)
    body = f'''<div class="usth-banner"><img src="assets/images/usth_logo.png" alt="USTH"><div><div class="t">Atmospheric Remote Sensing</div><div class="s">Satellite Remote Sensing of Atmospheric Composition · self-study and exam preparation — USTH</div></div></div>
<div class="callout" style="border-left:6px solid #ED1C24"><b class="t">Start here: the Big 12</b><p style="font-size:1.05rem;margin:6px 0">Before the modules and before the exams, master <b>3 key points, 3 formulas, 3 concepts and 3 principles</b>. On the {nq} written questions of this site they give the skeleton of <b>{cs["skeleton"]*100:.0f}%</b> of the {cs["n"]} parts. <a class="btn" href="lessons/start-here/index.html">Open the Big 12 →</a></p></div>
<p class="lead">Thirteen modules built on study guide v2 and on the lecture master (J. Cuesta): the Big 12, Part A core toolbox, Part B atmosphere and ozone chemistry, the eight theory chapters, Part C satellite case studies and Part D lidar. Each module has a lesson, slides, a question bank with explanations and sources, and lecture pages. Five written mock papers and twelve multiple-choice exams close the loop.</p>
<div class="kpis"><div class="kpi"><b>{len(MODULES)}</b><span>modules</span></div><div class="kpi"><b>{tot("slides")}</b><span>slides</span></div><div class="kpi"><b>{tot("mcq")}</b><span>multiple-choice questions</span></div><div class="kpi"><b>{tot("ess")}</b><span>essay questions</span></div><div class="kpi"><b>5</b><span>written mock papers ({nq} questions)</span></div><div class="kpi"><b>{ncalc}</b><span>calculators</span></div><div class="kpi"><b>137</b><span>lecture pages</span></div><div class="kpi"><b>31</b><span>figures</span></div></div>
<h2>Modules</h2><div class="grid">{cards}</div>
<h2>Suggested study path</h2>
<ol class="steps"><li><b>Start here</b>: read the 12 cards (15 minutes) and pass the 12-question check (10/12).</li><li><b>Part A and Part B</b>, then the eight chapters: read the plain-language part, the formulas, the worked example, Q&amp;A and memory hooks; look at the slides and the lecture pages.</li><li><b>Parts C and D</b>: the lecture’s satellite case studies and lidar (new material, with the lecture exercises solved).</li><li><b>Practise the numbers</b> in the <a href="calculators.html">calculators</a>, then take the <a href="exam.html">mock papers</a>: Paper 5 (drill), Papers 2–4, finally Paper 1 (official) under time.</li></ol>
<h2>Status and limits (honest notes)</h2>
<ul><li><b>Sources</b>: (1) the study pack v2 supplied by the student (guide, mock exam, 24 figures, 11 class photos); (2) the lecture master “Remote Sensing of the Atmosphere: a focus on air composition” (J. Cuesta, UPEC; 233 pages), read by text layer plus OCR; 137 selected pages are shown with credit and every number taken from them is cited by slide number. No textbook was supplied, so there are no book page numbers.</li>
<li><b>Numbers</b>: every calculated value is recomputed in Python (numpy/scipy) with two independent methods; the JavaScript calculators are compared with Python in 478 checks. The simple models (TIR brightness-temperature depression, O₂ above the layer, the 12-level averaging-kernel simulation, the line-width model) are illustrations, not measured data.</li>
<li><b>Big 12 coverage</b>: the “{cs["skeleton"]*100:.0f}% skeleton / {cs["full"]*100:.0f}% complete” figures are my own A/B/C assessment of {cs["n"]} parts of the five papers; Papers 2–5 were written by me in the style of the official paper. The real exam is unknown.</li>
<li><b>Questions</b>: “Original” questions come from the mock exam, the checklists, the guide and the lecture slides (each has its source); “Added” questions are extra items. Bias audit over all {LENRANK["n"]} multiple-choice questions: the correct answer is at position A/B/C/D in {LENRANK["pos"][0]*100:.0f}/{LENRANK["pos"][1]*100:.0f}/{LENRANK["pos"][2]*100:.0f}/{LENRANK["pos"][3]*100:.0f}% of the questions, and is the longest option in {LENRANK["longest"]*100:.0f}% and the shortest in {LENRANK["shortest"]*100:.0f}% (unbiased would be 25% each). Length is only roughly balanced.</li>
<li><b>Language</b>: English by default; each lesson keeps the short Vietnamese summary. No Chinese version.</li>
<li><b>Figures</b>: 24 from the original pack, 7 new (hydrostatic law, sinks, ozone cycle, multispectral ozone, lidar exercise, DIAL, Big 12 map); wide figures are scaled on slides, so text inside a figure can be smaller than 20 px (all HTML slide text is ≥ 20 px).</li>
<li><b>Discrepancies found</b>: guide v2 Ch.8 quotes brightness-temperature depressions of ≈ 7 K (4 km) and ≈ 2 K (1 km); our simple model gives larger values (same trend). Lecture exercise 1(d): the printed solution is 8.6 nW; recomputation with exp(−2τ) gives 9.0 nW (same conclusion). The lecture slide says pressure halves every “≈ 5 km”; H ln 2 = 5.75 km.</li>
<li><b>Copyright</b>: the lecture pages belong to their author and are shown for private study with credit; the full lecture PDF is not republished.</li></ul>'''
    write('index.html', page('Home', body, 0, desc='Atmospheric Remote Sensing self-study system, USTH', scripts=['theme.js', 'gate.js']))


def gallery_page():
    where = {'s1_gome': ('m3', 'Ch.3'), 's2_tropomi': ('m3', 'Ch.3'), 's3_wavelengths': ('m3', 'Ch.3'), 's4_solar': ('m2', 'Ch.2'), 's5_rte_equation': ('pa', 'Part A.1'), 's6_gains_losses': ('pa', 'Part A.2'),
             's7_rte_gas_layer': ('pa', 'Part A.3'), 's8_optical_depth': ('pa', 'Part A.4'), 's9_blackboard': ('pa', 'Part A.4'), 's10_line_widths': ('pa', 'Part A.5'), 's11_doas': ('pa', 'Part A.6')}
    slug = {m[0]: m[1] for m in MODULES}
    cells = ''.join(f'<figure class="ph"><a href="assets/images/slides/full/{k}.jpg" target="_blank" rel="noopener"><img src="assets/images/slides/{k}.jpg" loading="lazy" alt="{esc(v)}"></a>'
                    f'<figcaption><b>{i+1}.</b> {v}<br><a href="lessons/{slug[where[k][0]]}/index.html#photos">→ {where[k][1]}</a></figcaption></figure>' for i, (k, v) in enumerate(PHOTOS.items()))
    body = f'<p class="crumbs"><a href="index.html">Home</a> › Lecture photos</p><h1>Lecture photos</h1><p class="lead">All 11 photos of the lecture slides and blackboard from the study pack, in lecture order. Click a photo for the full-resolution picture (4000×3000); each caption links to the lesson that uses it. The 137 pages of the lecture master are in <a href="lecture-slides.html">Lecture pages</a>.</p><div class="phgrid">{cells}</div>'
    write('slides-gallery.html', page('Lecture photos', body, 0, desc='Photos of the lecture slides and blackboard', scripts=['theme.js']))

def lecture_gallery_page():
    import lecture_pages as LP
    slug = {m[0]: (m[1], m[2]) for m in MODULES}
    secs = ''; toc = ''
    for key, title, mid in LP.GROUPS:
        pg = [(p, t) for p, g, t in LP.P if g == key]
        cells = ''.join(f'<figure class="ph" data-t="{esc(t.lower())} p{p}"><a href="assets/images/lecture/full/p{p:03d}.jpg" target="_blank" rel="noopener"><img src="assets/images/lecture/thumb/p{p:03d}.jpg" loading="lazy" alt="{esc(t)}"></a><figcaption><b>p.{p}</b> {esc(t)}</figcaption></figure>' for p, t in pg)
        secs += f'<section class="lgrp"><h2 id="{key}">{esc(title)} <small>({len(pg)} pages)</small></h2><p style="font-size:.9rem">Used in <a href="lessons/{slug[mid][0]}/index.html#lecpages">{esc(slug[mid][1])}</a></p><div class="phgrid">{cells}</div></section>'
        toc += f'<a href="#{key}">{esc(title)}</a> · '
    body = f'''<p class="crumbs"><a href="index.html">Home</a> › Lecture pages</p><h1>Lecture pages — Cuesta master course</h1>
<p class="lead">{len(LP.P)} selected pages of the lecture “Remote Sensing of the Atmosphere: a focus on air composition” (Juan Cuesta, Université Paris-Est Créteil, Master Space 2026–2027; 233 pages in total). The pages were rendered, read by text layer and OCR, and chosen for exam relevance. Click a page to enlarge. Page numbers match the PDF.</p>
<p style="font-size:.9rem">© The lecture belongs to its author; pages are shown here for private study with credit. Only selected pages are shown; the full PDF is not republished.</p>
<p><input id="lf" placeholder="Filter pages by keyword or number (e.g. lidar, 216, ozone)…" style="width:100%;max-width:460px;padding:6px 10px;font:inherit;border:1px solid var(--border);border-radius:8px;background:var(--bg);color:var(--text)"></p>
<p>{toc}</p>{secs}
<script>document.getElementById('lf').addEventListener('input',function(){{var q=this.value.toLowerCase().trim();document.querySelectorAll('figure.ph').forEach(function(f){{f.style.display=!q||f.getAttribute('data-t').indexOf(q)>=0?'':'none'}});document.querySelectorAll('.lgrp').forEach(function(g){{g.style.display=[].some.call(g.querySelectorAll('figure.ph'),function(f){{return f.style.display!=='none'}})?'':'none'}})}});</script>'''
    write('lecture-slides.html', page('Lecture pages', body, 0, desc='Selected pages of the lecture master course', scripts=['theme.js']))
