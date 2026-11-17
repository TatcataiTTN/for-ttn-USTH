# -*- coding: utf-8 -*-
"""Module E — Measuring IOPs (slides 59-62)."""
import math
from lib import *
from qcore import Bank
from ma import LS
V = VERIFIED

def build():
    B = Bank('me', seed=15); A = B.add
    BL = V['beer_lambert_T']; cT = V['c_from_T_25cm']
    A('What does a beam transmissometer such as the C-star (slide 60) measure?',
      'The attenuation coefficient c = a + b', ['Only the absorption coefficient a', 'Only the backscattering coefficient b_b', 'The Chl concentration directly'],
      'Slide 59–60: “The attenuation coefficient”. Light leaves the beam by absorption and by scattering out of it; the instrument measures the transmitted fraction over a known path, T = e^(−c L).', 1, 'Attenuation', src='Lecture, slides 59–60')
    A('What is the problem of a real transmissometer pointed out on slide 60?',
      'Some scattered light also reaches the detector, because the ideal acceptance angle of 0° would collect no light', ['The LED emits too much heat', 'The water absorbs the instrument', 'The path length is always zero'],
      'Slide 60: “some scattered light also reach the detector (the theoretically ideal attenuation meter will have an acceptance angle of 0° (but 0° = no light)).” So the measured c is slightly smaller than the true c; scattering is mainly forward, which makes the error larger for large particles.', 2, 'Attenuation', src='Lecture, slide 60')
    A('How does the two-tube instrument of slide 61 separate absorption from attenuation?',
      'One tube has absorbing walls (all scattered photons are absorbed: it measures attenuation); the other has reflecting walls (scattered photons are transmitted: it measures absorption)', ['One tube measures scattering and the other measures temperature', 'Both tubes measure absorption at different depths', 'One tube is for CDOM and the other for salt'],
      'Slide 61 text. Then b = c − a. The reflecting tube still loses some scattered photons, a known source of error (not shown on the slide).', 1, 'ac meter', src='Lecture, slide 61')
    A('What do you measure when a 0.2 µm filter is placed at the entrance of the absorption meter (slide 61)?',
      'Only the CDOM absorption (plus water)', ['The phytoplankton absorption only', 'The scattering by particles only', 'Nothing, the meter is blocked'],
      'Slide 61: “if you put a filter (0.2 µm) at the entrance to filter particles, then you only measure the CDOM absorption” (a_cdom + a_w; a_w can be subtracted using a pure-water reference). Particulate absorption a_p is then the difference between unfiltered and filtered measurements.', 2, 'ac meter', src='Lecture, slide 61')
    A('Which instrument geometry is used for particulate backscattering on slide 62?',
      'An LED and a detector arranged so that the scattering volume is viewed at about 117°', ['A detector at 0° behind the LED', 'A detector at 180° exactly', 'A pair of mirrors at 45°'],
      'Slide 62 (Boss & Pegau, 2001): the LED beam and the detector field of view cross at the particle volume at 117°.', 1, 'Backscatter', src='Lecture, slide 62')
    A('How does the lecture obtain b_bp from the signal at 117° (slide 62)?',
      'β_p(117°) = β(117°) − β_w(117°); then b_bp = 2π χ β_p(117°) with a factor χ', ['b_bp = β(117°) exactly', 'b_bp = c − a', 'b_bp = 4π β_w(117°)'],
      'Slide 62: subtract the pure-water contribution, then extrapolate to the whole backward hemisphere with the factor χ (χ(θ) curves shown for Petzold phase functions; ≈ 1.0–1.1 at 117°, read from graph).', 2, 'Backscatter', src='Lecture, slide 62')
    A('A transmissometer reads T = 0.90 over a 0.25 m path. Which c does this correspond to?',
      f'≈ {cT["0.9"]:.2f} m⁻¹', [f'≈ {-math.log(0.9):.2f} m⁻¹ (path length forgotten)', '≈ 0.10 m⁻¹ (1 − T)', f'≈ {1/0.25*0.9:.2f} m⁻¹ (T/L)'],
      f'c = −ln(T)/L = −ln(0.90)/0.25 = {cT["0.9"]:.3f} m⁻¹ (Python; the path length of 0.25 m is an illustrative choice, not a lecture value).', 2, 'Calculation', src='Lecture, slide 60 (principle)')
    A('What T does a path of 0.25 m give for c = 1.0 m⁻¹?',
      f'T = e^(−0.25) ≈ {BL["c1.0_L0.25"]:.3f}', [f'T ≈ {math.exp(-1):.3f}', f'T ≈ {1-0.25:.2f}', f'T ≈ {math.exp(0.25):.2f}'],
      f'T = exp(−cL) = {BL["c1.0_L0.25"]:.4f}; Python: closed form and numerical integration of dI/dx = −cI agree to 10⁻⁷.', 1, 'Calculation', src='Lecture, slides 5, 60')
    A('Slide 62 gives χ ≈ 1.1 at 117° and a measured β_p(117°) = 1.0 × 10⁻³ m⁻¹ sr⁻¹. Which b_bp does this give?',
      f'≈ {V["bbp_example_chi1p1_beta1e-3"]*1e3:.1f} × 10⁻³ m⁻¹', [f'≈ {V["bbp_example_chi1p1_beta1e-3"]*1e2:.1f} × 10⁻² m⁻¹', '≈ 1.1 × 10⁻³ m⁻¹ (2π omitted)', f'≈ {V["bbp_example_chi1p1_beta1e-3"]*4:.2f} × 10⁻³ m⁻¹'],
      f'b_bp = 2π × 1.1 × 1.0×10⁻³ = {V["bbp_example_chi1p1_beta1e-3"]:.2e} m⁻¹. χ ≈ 1.1 is a value read from a graph (≈ 10 %), used here as an illustrative parameter.', 3, 'Calculation', src='Lecture, slide 62')
    A('Why is a beam transmissometer at 660 nm sometimes used for particles (slide 66, 105)?',
      'At 660 nm absorption by water and pigments is small enough that c_p is close to particle scattering and is related to POC', ['Because 660 nm is where CDOM absorbs most', 'Because 660 nm is the Sun’s peak', 'Because water is perfectly transparent at 660 nm'],
      'Slide 65 caption: attenuation at 660 nm can be taken as the scattering coefficient “since absorption is very weak at 660 nm”. Slide 66 shows c_p(660) vs POC. Strictly, water absorption is not negligible at 660 nm (a_w on slide 24 rises steeply beyond 600 nm, ≈ 0.4 m⁻¹ read from the graph), so it must be subtracted.', 3, 'c_p and POC', src='Lecture, slides 65–66, 105')
    B.essay('Explain how a, c and b_bp are measured in situ (slides 59–62). For each instrument state the principle, the main error and what a 0.2 µm filter changes.',
            'c: transmissometer, T = e^(−cL); error: scattered light reaching the detector (finite acceptance angle, slide 60). a: tube with reflecting walls, scattered photons are transmitted; c with absorbing walls; b = c − a (slide 61). A 0.2 µm filter at the inlet gives CDOM absorption only (slide 61). b_bp: LED/detector crossing at 117°, β_p = β − β_w, b_bp = 2πχβ_p(117°) (slide 62).',
            2, 'Instruments', src='Lecture, slides 59–62')
    B.essay('A transmissometer with a 0.25 m path reads 0.90 and then 0.50. Compute c in both cases, and compute the ratio of scattering to attenuation if the absorption meter gives a = 0.10 m⁻¹ in the second case.',
            f'c = −ln(T)/L: {cT["0.9"]:.2f} m⁻¹ and {cT["0.5"]:.2f} m⁻¹. In the second case b = c − a = {cT["0.5"]-0.1:.2f} m⁻¹; b/c = {(cT["0.5"]-0.1)/cT["0.5"]:.2f}. The 0.25 m path is illustrative.',
            2, 'Calculation', src='Lecture, slides 59–61')

    sl = [
        S('Measuring the attenuation coefficient', cols(LS(60, 430), dul(['Beam transmissometer (C-star)', 'T = e<sup>−cL</sup>', 'Scattered light reaches the detector', 'Ideal acceptance angle 0° = no light']), flex=[3, 2])),
        S('Transmission versus attenuation', img('beer_lambert', 700, cap='Own computation: T = exp(−cL) for three path lengths')),
        S('Absorption and attenuation tubes', cols(LS(61, 430), dul(['Absorbing walls → c', 'Reflecting walls → a', 'b = c − a', '0.2 µm filter → CDOM only']), flex=[3, 2])),
        S('Backscattering sensor', cols(LS(62, 430), dul(['LED + detector, 117°', 'β<sub>p</sub> = β − β<sub>w</sub>', '<b>b<sub>bp</sub> = 2π χ β<sub>p</sub>(117°)</b>']), flex=[3, 2])),
        S('Instruments at a glance', dtable(tbl(['Quantity', 'Instrument', 'Main limit'], [['c', 'Transmissometer', 'Acceptance angle'], ['a', 'Reflecting-wall tube', 'Lost scattered photons'], ['b<sub>bp</sub>', '117° sensor', 'χ and water subtraction'], ['a<sub>cdom</sub>', '0.2 µm filtered inlet', 'Particle leakage']]), 'xl') + callout('info', 'Rule', 'Every instrument sees only part of the light: always state its geometry (acceptance angle, 117°, wall type)')),
        S('Key points', dul(['c from T = e<sup>−cL</sup>; a from reflecting tube', 'b = c − a', '0.2 µm filter: CDOM absorption only', 'b<sub>bp</sub> = 2π χ β<sub>p</sub>(117°)'], xl=True)),
    ]
    mod = dict(id='me', slug='05-measuring-iops', title='E · Measuring IOPs', en='Transmissometers, ac-type meters, backscattering sensors (slides 59–62)',
               qtitle='Guiding question: which instruments give c, a and b_bp, and what do they miss?',
               question='<p>IOPs are measured in situ with optical meters. Three families appear in the lecture: transmissometers (c), absorption meters with reflecting walls (a) and backscattering sensors (b_bp).</p>',
               sections=[
                ('Attenuation and absorption', '<p>A <b>transmissometer</b> sends a collimated beam through a known path and measures the transmitted fraction, T = e<sup>−cL</sup>, hence c = a + b (slide 60). Real instruments have a finite acceptance angle, so some scattered light reaches the detector and c is slightly underestimated. The <b>two-tube instrument</b> (slide 61) combines a tube with absorbing walls (attenuation) and a tube with reflecting walls (absorption); b = c − a. A 0.2 µm filter at the inlet gives CDOM absorption only.</p>'
                 + eq('Beer–Lambert', 'T = exp(−c L), &nbsp; c = −ln(T)/L') + f'<p>Example (Python, illustrative 0.25 m path): T = 0.90 ⇒ c = {cT["0.9"]:.2f} m⁻¹; T = 0.50 ⇒ c = {cT["0.5"]:.2f} m⁻¹.</p>'),
                ('Backscattering', '<p>A backscattering sensor measures β at a single angle (117°) and extrapolates to the backward hemisphere (slide 62, Boss &amp; Pegau 2001):</p>'
                 + eq('Slide 62', 'β<sub>p</sub>(117°,λ) = β(117°,λ) − β<sub>w</sub>(117°,λ); &nbsp; b<sub>bp</sub> = 2π χ β<sub>p</sub>(117°)') +
                 '<p class="note">The first line of slide 62, a correction of the measured signal for attenuation, is cut off on the slide and is not transcribed.</p>')],
               checklist=['Say what a transmissometer measures and its main error.', 'Explain the two-tube principle and b = c − a.', 'Say what the 0.2 µm filter does.', 'Write b_bp = 2πχβ_p(117°) and the water subtraction.', 'Convert T to c for a given path length.'],
               summary=['Máy đo truyền qua cho c = a + b; ống phản xạ cho a; b = c − a.', 'Lọc 0,2 µm: chỉ đo hấp thụ CDOM.', 'b_bp = 2π χ β_p(117°).'],
               calcs=[('beer', 'Beer–Lambert / c from T')], quiz_n=10,
               v2=dict(we_title='From T to c', we=f'<p>T = 0.90 over 0.25 m ⇒ c = −ln(0.90)/0.25 = {cT["0.9"]:.3f} m⁻¹. With a = 0.10 m⁻¹ measured separately, b = c − a = {cT["0.9"]-0.1:.3f} m⁻¹.</p>',
                       qa=[('Why does the transmissometer underestimate c?', 'A finite acceptance angle lets forward-scattered photons reach the detector (slide 60).'), ('Which quantity needs χ?', 'b_bp, to extrapolate from 117° to the whole backward hemisphere (slide 62).')],
                       hooks=[('Absorbing wall = c; reflecting wall = a.', 'Thành hấp thụ → c; thành phản xạ → a.')]))
    return mod, sl, B
