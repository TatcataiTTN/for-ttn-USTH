# -*- coding: utf-8 -*-
"""Start here — the Big 12: 3 key points, 3 formulas, 3 concepts, 3 principles."""
import math
from lib import *
from qcore import Bank
import core_map as CM, papers as PP
V = VERIFIED
SRC = 'Big 12 (course synthesis)'

def _all_parts():
    allp = [(q, p, l, ids) for (q, p, l, ids) in CM.P1]
    for pp in PP.PAPERS:
        for q in pp['Q']:
            for i, x in enumerate(q['parts']): allp.append((f'{pp["id"]}Q{q["n"]}', chr(97 + i), x[1], x[2]))
    return allp

def build():
    B = Bank('p0', seed=51)
    A = B.add
    # ---- the gate: one question per item (first 12) ----
    A('Which chain summarises the whole course?',
      'Sources and sinks → light–matter interaction → instrument and geometry → retrieval (inverse problem) → interpretation (sensitivity, validation)', ['Instrument → data download → map → conclusion, because the physics is built into the satellite', 'Emission inventory → chemistry-transport model → comparison with in-situ data only', 'Spectrum → library lookup → concentration, because retrieval is only table lookup'],
      'K1: we never measure a concentration; we measure light that crossed the atmosphere, and we invert the link between the two.', 1, 'K1', origin='goc', src=SRC + ' · K1')
    A('Which tool is best for the long-term trend of stratospheric ozone with the highest accuracy, and why?',
      'Solar occultation: it is self-calibrating (I/I₀ measured in the same view) and has high vertical resolution', ['Nadir thermal infrared: it has the widest swath and the best horizontal resolution', 'A ground-based lidar: it is the only instrument that reaches the stratosphere', 'A geostationary UV imager: it observes every hour'],
      'K2 and mock exam Q4(b): choose the tool by the target and give the reason. Occultation: self-calibration, trend quality; nadir: km-scale maps; geostationary: diurnal cycle.', 1, 'K2', origin='goc', src='Mock exam Q4(b) · K2')
    A('What is a retrieved vertical profile?',
      'The a-priori profile plus a smoothed version of the true profile: x̂ = xₐ + A(x − xₐ) + ε', ['The true profile at the altitude of each layer, with a random error ε', 'A direct measurement of concentration at each altitude, limited only by noise', 'The a-priori profile alone, because the measurement is too noisy to change it'],
      'K3 and F3: the averaging kernel A smooths the truth; rows with width larger than a layer mean poor vertical resolution; DOFS = trace(A).', 1, 'K3', origin='goc', src='Mock exam Q5(a) · K3')
    A('A beam crosses a layer with vertical optical depth 0.5 and the Sun is at 60° from the zenith. What fraction of the direct beam is transmitted?',
      'e^(−0.5/cos 60°) = e^(−1) ≈ 0.37 (37%)', ['e^(−0.5) ≈ 0.61, forgetting the slant path', 'e^(−0.5·cos 60°) ≈ 0.78, multiplying instead of dividing by cos θ', '1 − e^(−1) ≈ 0.63, the fraction that is absorbed'],
      'F1: slant τ = τ_vertical/cos θ = 1.0 ⇒ t = e^(−1) = 0.368. Mock exam Q2(c). Python.', 1, 'F1', origin='goc', src='Mock exam Q2(c) · F1')
    A('For a layer of gas without scattering in local thermodynamic equilibrium, what is the source function J?',
      'J = α·B(T): the absorption coefficient times the Planck function (Kirchhoff’s law)', ['J = s·I, the scattering coefficient times the radiance', 'J = −k_ext·I, the extinction term with the opposite sign', 'J = B(T_s), the surface emission only'],
      'F2: dI/dl = −k_ext·I + J. In LTE emission coefficient = absorption coefficient, so the layer emits like a grey body.', 1, 'F2', origin='goc', src='Part A.3 · F2')
    A('What are the DOFS of a retrieval and what is their value for a diagonal averaging kernel (0.6, 0.3, 0.1, 0)?',
      'DOFS = trace(A) = 1.0: about one independent piece of information', ['DOFS = determinant of A = 0, because one element is zero', 'DOFS = 4, the number of layers of the retrieval grid', 'DOFS = 0.6, the largest element of A'],
      'F3 and Q5(b): DOFS count the independent pieces of information; trace(A) = 0.6 + 0.3 + 0.1 + 0 = 1.0.', 1, 'F3', origin='goc', src='Mock exam Q5(b) · F3')
    A('A pollutant has chemical lifetime 6 h, a rain lifetime of 3 days and an outflow lifetime of 5 h. What is its overall lifetime?',
      f'τ = 1/(1/τ₁ + 1/τ₂ + 1/τ₃) ≈ {24/PP.kt:.1f} h: rates add, so it is shorter than every single lifetime', ['τ = 6 + 72 + 5 = 83 h, the sum of the lifetimes', 'τ = 72 h, set by the slowest sink', 'τ = (6 + 72 + 5)/3 ≈ 28 h, the average lifetime'],
      f'C1: k_chem = 4.0, k_dep = 0.33, k_out = 4.8 d⁻¹; k_tot = {PP.kt:.2f} d⁻¹. Mock exam Q1(a). Python.', 2, 'C1', origin='goc', src='Mock exam Q1(a) · C1')
    A('For which particle in the visible (λ = 0.55 µm) is the size parameter x = 2πr/λ about 2.3 (Mie regime)?',
      'A sulfate particle of radius 0.2 µm', ['An N₂ molecule of radius 0.2 nm (x ≈ 0.002)', 'A dust particle of radius 5 µm (x ≈ 57)', 'A cloud droplet of radius 10 µm (x ≈ 114)'],
      'C2 and Q7(a): x = 2π × 0.2/0.55 = 2.28. Molecules are Rayleigh, sulfate Mie, coarse dust and droplets in the geometric-optics limit. Python.', 1, 'C2', origin='goc', src='Mock exam Q7(a) · C2')
    A('In a DOAS fit, why is a low-order polynomial included?',
      'To absorb the slowly varying broadband effects (Rayleigh, Mie, surface) so that only the narrow gas fingerprint σ′ remains', ['To fit the narrow absorption lines more sharply than the laboratory spectra', 'To convert the slant column into a vertical column', 'To remove the stratospheric part of the column'],
      'C3: use a difference (or ratio) so that what you do not know cancels. DOAS: σ = σ_b + σ′; D = σ′·SCD.', 1, 'C3', origin='goc', src='Part A.6 · C3')
    A('Does scattering destroy photons along the line of sight?',
      'No: it redirects them (a loss for one direction, a gain for another); only absorption destroys the photon', ['Yes: every scattering event converts the photon energy to heat', 'Yes, but only for Rayleigh scattering; Mie scattering preserves photons', 'No, because scattering is never a loss for any direction'],
      'R1: the photon budget has gains (reflection, scattering in, emission) and losses (absorption, scattering out of the field of view).', 1, 'R1', origin='goc', src='Part A.2 · R1')
    A('Why does a thermal-IR sounder see a cold dust layer at 5 km better than a layer at 1 km with the same AOD?',
      'The signal depends on the thermal contrast with the surface; the colder, higher layer gives a larger brightness-temperature depression (and ε = α, Kirchhoff)', ['Because the layer at 5 km has a larger optical depth for the same AOD', 'Because the surface emits less at 5 km altitude', 'Because scattering by the dust dominates the thermal signal at high altitude'],
      f'R2 and Q8(b): Python model (τ = 0.5, T_s = 300 K): ΔBT = {V["tir"]["z1"]["dBT"]:.2f} K for 1 km and {V["tir"]["z5"]["dBT"]:.2f} K for 5 km.', 2, 'R2', origin='goc', src='Mock exam Q8(b) · R2')
    A('Why do line widths versus altitude carry information on the vertical distribution of an absorber?',
      'The Lorentz width ∝ pressure, which falls exponentially with height: line centre ↔ high altitude, wings ↔ low altitude', ['Because the Doppler width grows with pressure at low altitude', 'Because the lines shift in wavelength as the altitude increases', 'Because the line intensity is independent of temperature and pressure'],
      'R3 and Q10(b): p = p₀exp(−z/H), HWHM_L ∝ p. With known p and T profiles, the shape of a line gives the profile.', 2, 'R3', origin='goc', src='Mock exam Q10(b) · R3')
    # ---- extras ----
    A('Why is the transmission squared in the lidar equation P = K/z²·β·T²?',
      'The pulse crosses the path twice (out and back), so Beer–Lambert is applied twice: T² = e^(−2τ)', ['Because there are two types of scatterers, molecules and particles', 'Because the telescope is twice as large as the laser beam', 'Because the extinction is the square of the backscatter'],
      'F1 applied to an active instrument. Exercise 1 of the lecture: 98 nW only with T².', 2, 'F1', origin='goc', src='Lecture slide 216 · F1')
    A('The sky is blue and clouds are white. Which Big-12 concept explains both?',
      'The size parameter x = 2πr/λ: molecules (x ≪ 1) scatter ∝ λ⁻⁴; droplets (x ≫ 1) scatter all colours equally', ['Kirchhoff’s law: the sky emits blue light', 'The hydrostatic law: pressure is higher at low altitude', 'The lifetime of molecules, which is shorter than that of droplets'],
      'C2: (650/400)⁴ ≈ 7: blue is scattered about 7 times more than red by molecules; Q_ext → 2 for large droplets.', 1, 'C2', origin='goc', src='Mock exam Q7(b) · C2')
    A('NO₂ appears in hotspots while CH₄ is almost uniform. Which Big-12 item explains this?',
      'C1: NO₂ lives hours to a day (shorter than transport) whereas CH₄ lives about 10 years (much longer than the mixing time)', ['F3: NO₂ has a larger averaging kernel than CH₄', 'R3: NO₂ is heavier than CH₄ and stays near the ground', 'K2: the satellite has a better pixel size at the NO₂ wavelength'],
      'Mock exam Q1(c).', 1, 'C1', origin='goc', src='Mock exam Q1(c) · C1')
    A('How do you compare a chemistry-transport-model profile with a satellite retrieval?',
      'Smooth the model first: x_m,s = xₐ + A(x_m − xₐ), then compare with x̂', ['Compare the raw model profile directly with x̂ at each altitude', 'Divide the retrieved profile by the model profile', 'Replace the a priori by the model profile and repeat the fit without A'],
      'K3 and F3: the retrieval has limited vertical resolution; applying A to the model removes the smoothing and a-priori effects. Mock exam Q5(c).', 2, 'K3', origin='goc', src='Mock exam Q5(c) · K3')
    A('For an isothermal atmosphere with H = 8.3 km, by how much must you climb for the pressure to halve?',
      f'H·ln 2 ≈ {V["hydro"]["half_km"]:.2f} km (the lecture says about 5 km)', ['H/2 ≈ 4.15 km', '2H ≈ 16.6 km', 'H·ln 10 ≈ 19 km'],
      'R3: p = p₀exp(−z/H) = p₀/2 for z = H ln 2. Python.', 2, 'R3', src='Lecture slide 8 · R3')
    A('In DIAL, which quantity cancels in the double ratio of ON and OFF signals?',
      'The calibration constant K, the 1/z² factor and the backscatter β (C3: the two-wavelength trick)', ['The water-vapour extinction, because both wavelengths see it', 'The range Δr, because it is the same for both', 'Nothing cancels: the retrieval needs the absolute calibration'],
      'C3: DOAS, DIAL, Ångström, AAI and the O₂ A band all work by a difference or ratio of two wavelengths.', 2, 'C3', origin='goc', src='Lecture slide 231 · C3')
    A('What does a transparent gas (τ ≪ 1) do to a thermal-IR spectrum, according to the integrated RTE?',
      'I ≈ I(0) + τ·B: a small emission added on top of the background', ['I ≈ B(T) of the top layers only, because deeper layers are hidden', 'I ≈ 0, because the gas absorbs the whole background', 'I ≈ I(0)·e^(+τ), the background is amplified'],
      'F2: transparent gas ⇒ I ≈ I(0) + τB; opaque (τ ≫ 1) ⇒ only the top layers are seen (saturation).', 2, 'F2', origin='goc', src='Part A.3 · F2')
    A('Which of the Big-12 items must you quote to justify the choice of a nadir UV–visible instrument for mapping city NO₂?',
      'K2 (tool by target: km-scale maps, daily coverage, boundary-layer sensitivity) with C1 (short lifetime) and C3 (DOAS)', ['Only R3, because pressure sets the horizontal resolution', 'Only F3, because the averaging kernel fixes the pixel size', 'Only R2, because NO₂ emits thermal infrared radiation'],
      'Mock exam Q4(b) and Q1(c) combined.', 2, 'K2', origin='goc', src='Mock exam Q4(b) · K2')
    # ---- essays ----
    B.essay('Explain the whole course in five minutes using the Big 12: the chain, the three formulas, the three concepts and the three principles. Give one number for each.',
            'Chain (K1): sources/sinks → light–matter → instrument → retrieval → interpretation. Formulas: F1 I = I₀e^(−τ), τ = σNL (e.g. τ = 0.1 for N = 5×10¹³ cm⁻³, σ = 2×10⁻²⁰ cm², L = 1 km); F2 dI/dl = −k_ext I + J with J = αB(T); F3 x̂ = xₐ + A(x − xₐ) + ε (DOFS = trace A). Concepts: C1 lifetime (CO ≈ 58 d with k = 2×10⁻¹³, [OH] = 10⁶); C2 size parameter (x = 2.3 for r = 0.2 µm at 0.55 µm); C3 two-wavelength trick (DOAS D = σ′·SCD = 2×10⁻³). Principles: R1 photon budget (scattering redirects); R2 Kirchhoff + Planck (λmax 10 µm for 288 K); R3 hydrostatic layering (H ≈ 8.3 km). K2 tool by target; K3 products are smoothed.',
            3, 'Big 12', origin='bo_sung', src=SRC)
    B.essay('You are given a retrieved ozone profile from IASI and a model profile from CHIMERE. Using the Big 12, explain what you must check and do before comparing them.',
            'K3/F3: ask the sensitivity (DOFS, altitude of the AK maximum, a-priori contribution from the row sums); smooth the model: x_m,s = xₐ + A(x_m − xₐ); then compare with x̂ and quote bias, RMS and correlation. C1: for a short-lived species the model resolution and emissions matter more; K2: IASI (thermal IR) is most sensitive near 3 km and needs thermal contrast; F1/F2: errors in the forward model (spectroscopy, temperature profile) enter the retrieval.',
            3, 'Big 12', origin='bo_sung', src=SRC)
    B.essay('For each of the four categories (key points, formulas, concepts, principles) pick the item you consider the most frequently needed on an exam and justify it with the questions of the mock papers.',
            'Use the usage count of the coverage table: F1 (Beer–Lambert) and K2 (tool by target) appear in the most parts; C3 (two-wavelength trick) and R3 (hydrostatic layering) link Q3, Q8 and Q10; C1 is the single item for Q1; R2 links Q2, Q8, Q9. The justification must cite the specific questions (e.g. F1: Q2, Q6, Q9, Q10).',
            2, 'Big 12', origin='bo_sung', src=SRC)

    parts = _all_parts(); st = CM.stats(parts); st1 = CM.stats(CM.P1)
    used = sorted(st['used'].items(), key=lambda kv: -kv[1])
    # ---- coverage table for Paper 1 ----
    ids = [i['id'] for i in CM.ITEMS]; rank = {'A': 3, 'B': 2, 'C': 1}
    rows = ''
    for q in range(1, 11):
        best = {}
        for (qq, pt, lv, its) in CM.P1:
            if qq == f'Q{q}':
                for i in its:
                    if rank[lv] > rank.get(best.get(i, ''), 0): best[i] = lv
        rows += f'<tr><th>Q{q}</th>' + ''.join(f'<td class="{best[i]}">{best[i]}</td>' if i in best else '<td></td>' for i in ids) + '</tr>'
    cov = ('<table class="cov"><tr><th></th>' + ''.join(f'<th>{i}</th>' for i in ids) + '</tr>' + rows + '</table>' +
           '<p style="font-size:.9rem">Green A = a part of the question can be answered completely from that item; yellow B = the item gives the skeleton and module facts are needed; red C = module-specific detail with the item only as a frame.</p>')
    grid = ''
    for c in range(4):
        grid += f'<h3 style="margin-top:22px">{CM.COLS[c]} — ' + ['what the course is about', 'the maths you must be able to write', 'the ideas you must be able to explain', 'the laws behind everything'][c] + '</h3><div class="b12">'
        for it in CM.ITEMS:
            if it['col'] != c: continue
            grid += (f'<div class="b12c c{c}"><h3><span class="id">{it["id"]}</span>{it["title"]}</h3><p>{it["st"]}</p><p class="say"><b>In 20 seconds:</b> {it["say"]}</p><p class="trap"><b>Typical trap:</b> {it["trap"]}</p>'
                     f'<p style="font-size:.88rem"><b>Go deeper:</b> ' + ' · '.join(f'<a href="../{ {m[0]: m[1] for m in MODULES}[m_] }/index.html">{ {m[0]: m[2] for m in MODULES}[m_] }</a>' for m_ in it['mods']) + '</p></div>')
        grid += '</div>'
    sl = [
        cover('The Big 12', 'Start here · before the modules, before the exams', '<b>Atmospheric Remote Sensing</b> · USTH<br>3 key points · 3 formulas · 3 concepts · 3 principles'),
        S('Why twelve ideas?', ulb(['Every exam question reuses a few ideas', f'On the five written papers the Big 12 gives the skeleton of {st["skeleton"]*100:.0f}% of the parts', 'Master them first, then add module facts', 'Pass the 12-question check before the mock exams'], 34, 40)),
        S('The map of the Big 12', figfit('f31_big12_map', 'Key points, formulas, concepts and principles, with the questions of the official mock exam that use them.', 520)),
        S('3 key points', cards(card('K1 · Photons → amount', 'Sources and sinks → light–matter → instrument → retrieval → interpretation.'), card('K2 · Tool by target', 'Wavelength × geometry × platform; always give the reason.'), card('K3 · Products are smoothed', 'Averaging kernel, DOFS, a priori, AMF dependence.'), cols=3)),
        S('3 formulas', cards(card('F1 · Beer–Lambert', 'I = I₀e<sup>−τ</sup>, τ = σNL; slant τ/cos θ; AOD, DOAS, lidar T².'), card('F2 · RTE', 'dI/dl = −k<sub>ext</sub>I + J; J = αB(T); attenuated background + attenuated emission.'), card('F3 · Retrieval', 'x̂ = xₐ + A(x − xₐ) + ε; DOFS = tr(A); cost function J(x).'), cols=3)),
        S('3 concepts', cards(card('C1 · Lifetime', 'τ = 1/Σk; hours → hotspots; years → uniform.'), card('C2 · Scattering regimes', 'x = 2πr/λ: Rayleigh λ⁻⁴, Mie forward peak, geometric Q → 2.'), card('C3 · Two-λ trick', 'DOAS, DIAL, Ångström, AAI, O₂ A band.'), cols=3)),
        S('3 principles', cards(card('R1 · Photon budget', 'Absorption destroys; scattering redirects.'), card('R2 · Kirchhoff + Planck', 'ε = α; thermal contrast; λ<sub>max</sub> = 2898/T.'), card('R3 · Hydrostatic layering', 'p = p₀e<sup>−z/H</sup>; H ≈ 8.3 km; line width ∝ p.'), cols=3)),
        S('Each paper at a glance', dtable(tbl(['Paper', 'Parts', 'A', 'B', 'C', 'Skeleton'], [[pp['id'], str(s_['n']), str(s_['A']), str(s_['B']), str(s_['C']), f'{s_["skeleton"]*100:.0f}%'] for pp, s_ in [(dict(id='P1'), st1)] + [(pp, CM.stats([(f'Q{q["n"]}', 'x', x[1], x[2]) for q in pp['Q'] for x in q['parts']])) for pp in PP.PAPERS]]), 'mid')),
        S('How to answer: four steps', chk(['Name the Big-12 item the question asks about', 'Write the formula, define each symbol and the units', 'Insert numbers and give an order of magnitude', 'Add the reason in one sentence (physics, trade-off, limit)'])),
        S('Typical traps', ulb(['Adding lifetimes instead of rates', 'One-way T in the lidar equation (it is T²)', 'Forgetting 1/cos θ and 1 km = 10⁵ cm', 'Comparing a model with a retrieval without the averaging kernel', 'Saying scattering destroys photons'], 33, 36)),
        S('Exam checklist — Big 12', chk(['K1–K3: chain, tool by target, smoothed products', 'F1–F3: Beer–Lambert, RTE with J = αB, x̂ = xₐ + A(x − xₐ)', 'C1–C3: lifetime, size parameter, two-wavelength trick', 'R1–R3: photon budget, Kirchhoff + Planck, hydrostatic layering', 'Pass the 12-question check (10/12)'])),
        S('Key points', dul(['Twelve ideas, four groups', 'Skeleton of most exam parts', 'Then Part A, Part B, chapters, Parts C and D', 'Then the five papers']))]
    top = ', '.join(f'<b>{k}</b> ({v})' for k, v in used[:5])
    mod = dict(id='p0', slug='start-here', title='Start here · The Big 12', en='The 12 ideas to master before the modules and the exams',
               qtitle='Read this first (15 minutes), then pass the check at the bottom (10/12)',
               question=f'<p>The course looks wide (atmosphere, chemistry, radiative transfer, retrieval, aerosols, lidar), but almost every exam question is built from twelve ideas: <b>3 key points</b>, <b>3 formulas</b>, <b>3 concepts</b> and <b>3 principles</b>. Learn them in this order <i>before</i> the modules and <i>before</i> the mock exams. On the five written papers of this site the Big 12 gives the skeleton of <b>{st["skeleton"]*100:.0f}%</b> of the {st["n"]} parts and the complete answer of <b>{st["full"]*100:.0f}%</b>; on the official sample (Paper 1) the figures are {st1["skeleton"]*100:.0f}% and {st1["full"]*100:.0f}%. These percentages are my own assessment of each part, not a promise about the real exam.</p>',
               calcs=[('opt', 'Optical depth and transmission'), ('lifetime', 'Lifetime and parallel sinks'), ('size', 'Size parameter'), ('ak', 'Averaging kernel and DOFS')],
               quiz_n=12, quiz_title='Big 12 check — reach 10/12',
               checklist=['I can say the chain K1 in one sentence and give the reason for the tool choice K2.', 'I can write F1, F2, F3 from memory and define every symbol.', 'I can compute τ, t, the lifetime of parallel sinks, x = 2πr/λ and DOFS with a calculator.', 'I can explain why lifetime sets the map pattern (C1), why x sets the colour of sky and clouds (C2), and why two wavelengths cancel the unknowns (C3).', 'I can state R1, R2, R3 and one consequence of each.', 'I scored at least 10/12 on the Big 12 check.'],
               summary=['Mười hai ý cốt lõi: 3 điểm chính (K), 3 công thức (F), 3 khái niệm (C), 3 nguyên lý (R).', 'K1 chuỗi từ photon tới nồng độ; K2 chọn công cụ theo mục tiêu; K3 sản phẩm luôn bị làm trơn (AK, a priori).', 'F1 Beer–Lambert (τ = σNL); F2 RTE (J = αB); F3 x̂ = xₐ + A(x − xₐ) + ε.', 'C1 thời gian sống và trộn lẫn; C2 chế độ tán xạ theo x = 2πr/λ; C3 mẹo hai bước sóng (DOAS, DIAL, Ångström).', 'R1 cân bằng photon; R2 Kirchhoff + Planck; R3 phân tầng thủy tĩnh p = p₀e^(−z/H).'],
               sections=[
        ('The Big 12 on one page', f'<p>Twelve ideas, in four groups of three. Each card in the next section gives the statement, a 20-second explanation and the most common trap. The figure shows which questions of the official mock exam use each item.</p>' + lfig('f31_big12_map', 'The Big 12 and the official mock-exam questions that rely on them (computed from the coverage table below).') +
         '<p><b>How to use this page:</b> (1) read the 12 cards once (15 minutes); (2) take the 12-question check at the bottom and reach 10/12; (3) only then go to Part A, Part B and the chapters; (4) do the mock papers; use the A/B/C tags in the exam to see which part relies on the Big 12 alone.</p>'),
        ('The 12 cards', f'<p>Each card says what it is, how to say it in 20 seconds, the typical trap, and where to go deeper.</p>' + grid),
        ('How well do the 12 ideas cover the exams?', f'<p>Every sub-question of the five written papers was tagged with the Big-12 items it needs and a level: <b>A</b> the Big 12 alone gives the full answer, <b>B</b> the Big 12 gives the skeleton but module facts (a number, a name, an instrument) are needed, <b>C</b> module-specific. Counting all {st["n"]} parts of Papers 1–5:</p>' +
         hx_table(['Level', 'Parts', 'Share'], [['A — complete from the Big 12', str(st['A']), f'{st["A"]/st["n"]*100:.0f}%'], ['B — skeleton + module facts', str(st['B']), f'{st["B"]/st["n"]*100:.0f}%'], ['C — module-specific', str(st['C']), f'{st["C"]/st["n"]*100:.0f}%'], ['A + B — the Big 12 is present', str(st['A'] + st['B']), f'{st["skeleton"]*100:.0f}%']], 'left') +
         f'<p>Most-used items across the papers: {top}.</p><h3>Official Paper 1: which item serves which question</h3>' + cov +
         f'<div class="callout warn"><b class="t">Honest limits</b>The levels A/B/C are my own assessment of the wording and the model answers, made by one person. They cover the questions on this site (the official sample plus the new papers that I wrote in the same style); the real exam may contain parts I cannot foresee. Treat “≥ 90%” as “the Big 12 is present in {st["skeleton"]*100:.0f}% of the practice parts”, not as a guarantee. The 10% that the Big 12 does not cover are module facts: instrument names and numbers (e.g. IASI sensitivity peak, MISR stereo, geostationary revisit).</div>'),
        ('Suggested route', '<ol class="steps"><li><b>Hour 0 — Start here</b>: read the 12 cards, pass the check (10/12).</li><li><b>Part A and Part B</b>: radiative transfer, optical depth, line profiles, DOAS; atmosphere, sinks, ozone chemistry.</li><li><b>Chapters 1–4</b>: sinks, light–matter, trace-gas retrieval, geometries.</li><li><b>Chapters 5–8</b>: averaging kernels, passive aerosol, scattering regimes, aerosol altitude.</li><li><b>Part C and Part D</b>: satellite case studies and lidar (new lecture material).</li><li><b>Mock exams</b>: Paper 5 (drill) → Paper 2 → Paper 3 → Paper 4 → Paper 1 (official, timed). Self-grade with the answer keys.</li></ol>'),
    ])
    return mod, sl, B
