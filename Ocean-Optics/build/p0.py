# -*- coding: utf-8 -*-
"""Start here — the Big 12 for Ocean Optics: 3 key points, 3 formulas, 3 concepts, 3 principles."""
import math
from lib import *
from qcore import Bank
import core_map as CM
V = VERIFIED
SRC = 'Big 12 (course synthesis)'

def build():
    import papers as PP
    B = Bank('p0', seed=51); A = B.add
    parts = PP.all_parts(); st = CM.stats(parts)
    # ---- the gate: one question per Big-12 item (first 12) ----
    A('Which chain summarises the whole course?',
      'Water constituents → IOPs → light field (AOPs) → ocean-colour signal → biogeochemical variables, by inversion', ['Satellite → download → map → conclusion', 'Sun → atmosphere → clouds → rain', 'Ship → bottle → laboratory → report'],
      'K1 (slides 3, 5, 8, 9). We never measure Chl from space; we measure light leaving the sea and link it to the constituents through the IOPs.', 1, 'K1', src=SRC + ' · K1')
    A('A published relation links b_p to Chl. What must you check before using it in a new region?',
      'The water type it was built for (Case 1/Case 2 or optical class) and the spread around the relation (a factor 2–3)', ['Nothing: relations are physical laws', 'Only the date of the paper', 'Only the colour of the figure'],
      'K2 (slides 14–16, 65–66, 72–77): relations are regional/seasonal regressions.', 1, 'K2', src=SRC + ' · K2')
    A('Why are floats and gliders needed in addition to ocean-colour satellites?',
      'The ocean is under-sampled: satellites see the surface layer through clear skies, platforms add depth and work under clouds and in winter', ['Satellites cannot see the sea', 'Floats are cheaper than any ship', 'Satellites measure only temperature'],
      'K3 (slides 2, 4, 85, 101–103).', 1, 'K3', src=SRC + ' · K3')
    A('Which equation expresses attenuation in the radiative transfer equation?',
      'c = a + b, with L = L₀ e^(−c r) for a collimated beam', ['c = a − b', 'c = b_b/b', 'c = a × b'],
      'F1 (slide 5): loss by absorption and by scattering out of the beam.', 1, 'F1', src=SRC + ' · F1')
    A('What is the meaning of IOP(λ) = Σ (N/V) Q S?',
      'An IOP is the sum over particle classes of number per m³ × efficiency factor × geometric area', ['An IOP is the sum of the concentrations in mg m⁻³', 'An IOP is the ratio of two irradiances', 'An IOP is the Sun angle times the area'],
      'F2 (slide 63).', 1, 'F2', src=SRC + ' · F2')
    A('A CDOM sample has a(412) = 0.30 m⁻¹ and S′ = 0.014 nm⁻¹. What is a(443)?',
      f'≈ {0.3*V["cdom_ratio_443_from_412_S014"]:.2f} m⁻¹ (exponential decrease toward the red)', [f'≈ {0.3/V["cdom_ratio_443_from_412_S014"]:.2f} m⁻¹', '≈ 0.30 m⁻¹', '≈ 0.03 m⁻¹'],
      f'F3: a(443) = 0.30 exp(−0.014 × 31) = {0.3*V["cdom_ratio_443_from_412_S014"]:.3f} (Python).', 1, 'F3', src=SRC + ' · F3')
    A('Which of these is an IOP?',
      'The scattering coefficient b', ['The diffuse attenuation coefficient K_d', 'The reflectance R', 'The downwelling irradiance E_d'],
      'C1: IOPs depend only on the medium (slide 11); K_d, R and E_d depend on the light field (textbook).', 1, 'C1', src=SRC + ' · C1')
    A('What is a Case 2 water?',
      'A water whose optical properties are not determined mainly by phytoplankton and co-varying CDOM/detritus (minerals, CDOM or bubbles vary independently)', ['A water deeper than 200 m', 'A water within 10 km of the coast', 'A water with no CDOM'],
      'C2 (slide 14; textbook Classification Schemes). Slide 15: Case 2 also appears at high latitudes.', 1, 'C2', src=SRC + ' · C2')
    A('What happens to the chlorophyll-specific absorption a*_ph when cells get larger?',
      'It decreases, because of the package effect (Q*_a falls from 1 toward 0)', ['It increases proportionally', 'It stays constant', 'It becomes negative'],
      'C3 (slides 32–33).', 1, 'C3', src=SRC + ' · C3')
    A('Which relation shows additivity of IOPs?',
      'a = a_w + a_CDOM + a_ph + a_NAP', ['a = a_w × a_ph', 'a = c/b', 'a = b_b − b_f'],
      'R1 (slide 19).', 1, 'R1', src=SRC + ' · R1')
    A('Which spectral signature points to CDOM or NAP rather than to phytoplankton?',
      'A smooth exponential increase toward short wavelengths without pigment peaks', ['Narrow peaks at 443 and 675 nm', 'A sharp absorption step at 580 nm', 'A flat spectrum'],
      'R2 (slides 29, 35, 41).', 1, 'R2', src=SRC + ' · R2')
    A('What does a high b_bp/b_p suggest, all else equal?',
      'Particles with a higher refractive index (minerals, detritus) rather than living phytoplankton', ['Pure water', 'Only large organic cells', 'A cloud above the sea'],
      'R3 (slides 71, 84; textbook indices 1.01–1.09 vs 1.15–1.20).', 1, 'R3', src=SRC + ' · R3')
    # extra, deeper questions
    A('A student says: “ocean colour is the colour you see when you look at the sea.” What is wrong, according to slide 7?',
      'Reflection of Sun and sky light changes the colour at the surface but is not ocean-colour radiometry, which comes from photons interacting with in-water components', ['Nothing is wrong', 'Ocean colour is measured only at night', 'Ocean colour is the colour of the sky'],
      'K1 and slide 7.', 2, 'K1', src=SRC + ' · K1')
    A('Which two numbers do you need to convert T measured over L into c?',
      'T and L, with c = −ln T/L', ['T and the Sun angle', 'L and the salinity', 'T and the Chl'],
      'F1 (Beer–Lambert).', 1, 'F1', src=SRC + ' · F1')
    B.essay('Explain the whole course in five minutes using the Big 12: the chain, the three formulas, the three concepts and the three principles. Give one number for each.',
            f'Chain (K1). Formulas: c = a + b with T = e^(−cL) (e.g. c = 1 m⁻¹, L = 0.25 m ⇒ T = {V["beer_lambert_T"]["c1.0_L0.25"]:.2f}); IOP = ΣNQS ({V["sum_N_sigma_c_example"]:.2e} m⁻¹ for 10⁷ m⁻³ spheres, r = 5 µm); exponential/power laws (a_cdom(443) = {0.3*V["cdom_ratio_443_from_412_S014"]:.2f} from 0.30 at 412; b_p(440)/b_p(550) = {V["bp_440_over_550"]["-1"]:.2f} for n = −1). Concepts: IOP vs AOP, Case 1/2 (Case 1 = 81–87 %), package effect (Q* from 1 toward 0). Principles: additivity, spectral fingerprints, size/index control of scattering.',
            3, 'Big 12', src=SRC)
    B.essay('For each of the four categories (key points, formulas, concepts, principles) pick the item you consider the most often needed on an exam and justify it with the written papers of this site.',
            'Use the usage count of the coverage table on this page: the items with the highest counts are the best candidates. State that the counts describe only the papers written for this site (no exam from the lecturer was available).',
            2, 'Big 12', src=SRC)

    ids = [i['id'] for i in CM.ITEMS]; used = sorted(st['used'].items(), key=lambda kv: -kv[1]); top = ', '.join(f'<b>{k}</b> ({v})' for k, v in used[:5])
    grid = ''
    for c in range(4):
        grid += f'<h3 style="margin-top:22px">{CM.COLS[c]} — ' + ['what the course is about', 'the maths you must be able to write', 'the ideas you must be able to explain', 'the laws behind everything'][c] + '</h3>'
        for it in CM.ITEMS:
            if it['col'] != c: continue
            mm = ' · '.join(f'<a href="../{ {m[0]: m[1] for m in MODULES}[m_] }/index.html">{ {m[0]: m[2] for m in MODULES}[m_] }</a>' for m_ in it['mods'])
            grid += (f'<div class="b12c c{c}"><h3><span class="id">{it["id"]}</span>{it["title"]}</h3><p>{it["st"]}</p><p class="say"><b>In 20 seconds:</b> {it["say"]}</p><p class="trap"><b>Typical trap:</b> {it["trap"]}</p>'
                     f'<p style="font-size:.88rem"><b>Go deeper:</b> {mm}. <b>Slides:</b> {", ".join(map(str, it["pages"]))}</p></div>')
    ROWS = []
    for pp in PP.PAPERS:
        s_ = CM.stats([(pp['id'] + 'Q' + str(q['n']), 'x', x[1], x[2]) for q in pp['Q'] for x in q['parts']])
        ROWS.append([pp['id'], str(s_['n']), str(s_['A']), str(s_['B']), str(s_['C']), '%.0f%%' % (s_['skeleton'] * 100)])
    sl = [
        cover('The Big 12', 'Start here · before the modules, before the exams', '<b>Ocean Optics</b> · USTH<br>3 key points · 3 formulas · 3 concepts · 3 principles'),
        S('Why twelve ideas?', ulb(['Every module reuses a few ideas', f'In the {len(PP.PAPERS)} written papers of this site the Big 12 gives the frame of {st["skeleton"]*100:.0f} % of the parts', 'No exam of the lecturer was available', 'Master them first, then the modules'], 34, 42)),
        S('3 key points', cards(card('K1 · From water to colour', 'Constituents → IOPs → light field → signal → biogeochemistry'), card('K2 · A hypothesis behind every product', 'Water type, region, spread ×2–3'), card('K3 · An under-sampled ocean', 'Floats, gliders, BGC-Argo'))),
        S('3 formulas', cards(card('F1 · c = a + b', 'dL/dr = −cL + scattering in + S; T = e<sup>−cL</sup>'), card('F2 · IOP = Σ N Q S', 'number × efficiency × area'), card('F3 · Spectral laws', 'a ∝ exp[−S(λ−λ₀)]; b<sub>p</sub> ∝ λ<sup>n</sup>; β<sub>w</sub> ∝ λ<sup>−4.3</sup>'))),
        S('F1 · The radiative transfer equation', EQS_('rte', fs=26)),
        S('F2 · IOP = Σ N Q S', EQS_('iop_sum')),
        S('3 concepts', cards(card('C1 · IOP vs AOP', 'Medium only versus medium + light'), card('C2 · Case 1/Case 2, classes', 'Co-variation with phytoplankton; 17 classes'), card('C3 · Package effect', 'Q*<sub>a</sub> from 1 to 0'))),
        S('3 principles', cards(card('R1 · Additivity', 'a, b and b<sub>b</sub> add over constituents'), card('R2 · Spectral fingerprints', 'Slope, peaks, flat, steep'), card('R3 · Size and index', 'Forward vs backward; b<sub>bp</sub>/b<sub>p</sub>'))),
        S('Each paper at a glance', dtable(tbl(['Paper', 'Parts', 'A', 'B', 'C', 'Frame'], ROWS), 'xl')),
        S('How to answer: four steps', chk(['Name the Big-12 item the question asks about', 'Write the formula and define each symbol and unit', 'Insert numbers; give an order of magnitude', 'Say which water type or assumption you used'])),
        S('Typical traps', ulb(['Using a instead of c in Beer–Lambert', 'Calling E<sub>d</sub> or K<sub>d</sub> an IOP', 'Case 2 = coastal', 'Treating regressions as laws', 'Fluorescence = Chl'], 34, 36)),
        S('Exam checklist — Big 12', chk(['K1–K3: chain, hypothesis, under-sampling', 'F1–F3: c = a + b, ΣNQS, spectral laws', 'C1–C3: IOP/AOP, Case 1/2, package effect', 'R1–R3: additivity, fingerprints, size and index'])),
        S('Key points', dul(['Twelve ideas, four groups', 'Frame of most exam parts (own papers)', 'Then modules A to H', 'Then the five written papers'], xl=True)),
    ]
    mod = dict(id='p0', slug='start-here', title='Start here · The Big 12', en='The 12 ideas to master before the modules: 3 key points, 3 formulas, 3 concepts, 3 principles',
               qtitle='Read this first (15 minutes), then pass the check at the bottom (10/12)',
               question='<p>Ocean Optics looks wide (water, absorption, scattering, instruments, biogeochemistry, platforms) but it is built from twelve ideas: <b>3 key points</b>, <b>3 formulas</b>, <b>3 concepts</b> and <b>3 principles</b>. They were chosen from the 120 lecture slides and the Ocean Optics Web Book. Read them, then take the 12-question check.</p>',
               calcs=[('beer', 'Beer–Lambert'), ('expabs', 'CDOM/NAP exponential'), ('bplaw', 'b_p power law'), ('sumns', 'ΣNQS')],
               quiz_n=12, quiz_title='Big 12 check — reach 10/12',
               checklist=['I can say the chain K1 and why “colour” is not surface reflection.', 'I can write F1, F2, F3 and define each symbol.', 'I can say IOP vs AOP, Case 1/2 and the package effect.', 'I can name the three principles with an example each.'],
               summary=['Mười hai ý cốt lõi: 3 điểm chính (K), 3 công thức (F), 3 khái niệm (C), 3 nguyên lý (R).', 'Không có đề mẫu của thầy: các tỉ lệ độ phủ chỉ tính trên đề do mình soạn.'],
               sections=[
                ('The Big 12 on one page', '<p>Twelve ideas in four groups of three. Each card below gives the statement, a 20-second explanation and the most common trap.</p>'
                 '<p><b>How to use this page:</b> (1) read the 12 cards (15 minutes); (2) take the check at the bottom and reach 10/12; (3) go to modules A–H; (4) try the written papers.</p>'),
                ('The 12 cards', grid),
                ('The three formulas, interactive', '<p>Click any coloured symbol to see its meaning, unit and the numbers that go into it.</p>' + EQ('rte') + EQ('iop_sum') + EQ('spectral')),
                ('How well do the 12 ideas cover the exams? (honest numbers)', f'<p>Every part of the {len(PP.PAPERS)} written papers of this site was tagged with the Big-12 items it needs and a level: <b>A</b> the Big 12 gives the full answer, <b>B</b> frame + module facts, <b>C</b> module-specific. Across all {st["n"]} parts: <b>{st["A"]}</b> A, <b>{st["B"]}</b> B, <b>{st["C"]}</b> C → the Big 12 gives the frame of <b>{st["skeleton"]*100:.0f} %</b> and the full answer of <b>{st["full"]*100:.0f} %</b>.</p>'
                 + hx_table(['Paper', 'Parts', 'A', 'B', 'C', 'Frame'], ROWS) +
                 f'<p>Most-used items: {top}.</p>'
                 '<div class="callout warn"><b class="t">Honest limits</b>There is <b>no sample exam from the lecturer</b>. The levels A/B/C are my own assessment of papers that I wrote myself from the slides and the textbook, so the percentages say how well the Big 12 serves <i>these</i> papers, not the real exam. They are not a promise about the real exam.</div>')])
    return mod, sl, B
