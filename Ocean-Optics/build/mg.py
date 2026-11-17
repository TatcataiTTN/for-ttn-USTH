# -*- coding: utf-8 -*-
"""Module G — The light field: AOPs, K_d, reflectance, Secchi depth. TEXTBOOK CONTENT: the lecture file has no slides on this (outline slide 9, item 3)."""
import math
from lib import *
from qcore import Bank
V = VERIFIED
TB = 'Textbook (oceanopticsbook.info, not in the lecture file)'

def build():
    B = Bank('mg', seed=17); A = B.add
    EU = V['euphotic_1pct']; SC = V['secchi_examples']; R = V['R_over_f_bb_a_examples']
    z = lambda k: EU[k]['z1pct']
    A('Which property of an apparent optical property (AOP) distinguishes it from an IOP?',
      'It depends on the medium and on the directional structure of the light field (Sun, sky, depth), yet is stable enough to describe the water body', ['It depends only on the constituents, never on the light', 'It is measured only in the laboratory', 'It is always dimensionless and equal to 1'],
      'Textbook, Apparent Optical Properties: AOPs (1) depend both on the medium (the IOPs) and on the geometric structure of the radiance distribution, and (2) display enough regular features and stability to describe a water body.', 1, 'AOP', origin='bo_sung', src='Textbook: Apparent Optical Properties')
    A('Why is the downwelling irradiance E_d not considered a good AOP?',
      'A passing cloud can change E_d by an order of magnitude within seconds although the water has not changed', ['E_d is not a radiometric quantity', 'E_d cannot be measured', 'E_d is independent of the Sun'],
      'Textbook, Apparent Optical Properties. It satisfies the first part of the definition but not the second (stability).', 1, 'AOP', origin='bo_sung', src='Textbook: Apparent Optical Properties')
    A('How is the diffuse attenuation coefficient K_d defined?',
      'K_d(z,λ) ≡ −d ln E_d(z,λ)/dz', ['K_d = a + b', 'K_d = E_u/E_d', 'K_d = L_w/E_d'],
      'Textbook, K functions: K_d ≡ −d ln E_d/dz; with K_d constant, E_d(z) = E_d(0) exp(−K_d z). It is an AOP: it depends on the Sun angle, unlike c = a + b.', 1, 'K_d', origin='bo_sung', src='Textbook: K functions')
    A('How is the irradiance reflectance R defined?',
      'R(z,λ) ≡ E_u(z,λ)/E_d(z,λ)', ['R = E_d/E_u', 'R = c/a', 'R = b_b/b'],
      'Textbook, Reflectances. The remote-sensing reflectance is R_rs ≡ L_w(in air)/E_d(in air), in sr⁻¹.', 1, 'Reflectance', origin='bo_sung', src='Textbook: Reflectances')
    A('What is the unit of the remote-sensing reflectance R_rs?',
      'sr⁻¹ (radiance divided by irradiance)', ['Dimensionless', 'm⁻¹', 'W m⁻²'],
      'R_rs ≡ L_w/E_d: radiance (W m⁻² sr⁻¹ nm⁻¹) over irradiance (W m⁻² nm⁻¹) = sr⁻¹ (Textbook, Reflectances).', 1, 'Reflectance', origin='bo_sung', src='Textbook: Reflectances')
    A('Which inequality does the textbook give between K_d, the absorption coefficient a and the attenuation coefficient c?',
      'a ≤ K_d μ̄_d ≤ c, and in particular c > K_d', ['K_d > c always', 'K_d = a exactly for all Sun angles', 'K_d < a always'],
      'Textbook, K functions: a ≤ K_d μ̄_d ≤ c (μ̄_d = average cosine of the downwelling light) and K_d ≈ a/μ̄_d; c = K_d only for a collimated vertical beam without scattering.', 2, 'K_d', origin='bo_sung', src='Textbook: K functions')
    A('What is the “penetration depth” of the textbook?',
      '1/K_d: the depth over which most of the surface-layer information in the signal originates', ['K_d × z', 'The depth of the sea bottom', '1/c'],
      'Textbook, K functions: remote sensing of a layer of depth 1/K_d. At depth 1/K_d the irradiance has dropped to 1/e ≈ 37 %.', 1, 'K_d', origin='bo_sung', src='Textbook: K functions')
    A('For K_d = 0.04 m⁻¹ (clear ocean) at which depth does the irradiance fall to 1 % of its surface value?',
      f'≈ {z("0.04"):.0f} m', [f'≈ {1/0.04:.0f} m (the penetration depth)', f'≈ {math.log(10)/0.04:.0f} m (10 % level)', f'≈ {z("0.04")*10:.0f} m'],
      f'z = −ln(0.01)/K_d = 4.605/0.04 = {z("0.04"):.1f} m (closed form and root-finding agree, verified.json). For K_d = 0.1: {z("0.1"):.1f} m; K_d = 0.3: {z("0.3"):.1f} m.', 2, 'Calculation', origin='bo_sung', src='Textbook: K functions')
    A('Which formula for the Secchi depth is given by the classic theory, and which values of Γ?',
      'z_SD = Γ/(⟨K_dv⟩ + ⟨c_v⟩) with Γ ≈ 6–9 (HydroLight default 8)', ['z_SD = K_d + c', 'z_SD = 1/(K_d c)', 'z_SD = Γ × a with Γ = 100'],
      f'Textbook, The Secchi Disk. Example: K_d = 0.1, c = 0.2 m⁻¹ ⇒ z_SD = 8/0.3 = {SC["Kd0.1_c0.2"]:.1f} m (Γ = 6–9 gives {V["secchi_range_gamma_6_9_Kd0p1_c0p2"][0]:.1f}–{V["secchi_range_gamma_6_9_Kd0p1_c0p2"][1]:.1f} m).', 2, 'Secchi', origin='bo_sung', src='Textbook: The Secchi Disk')
    A('What does the Lee et al. (2015) Secchi-depth formula use instead of the photopic K_dv and c_v?',
      'K_d at the wavelength of minimum K_d, and c replaced by 1.5 K_d(λ_min): z_SD = γ/(2.5 K_d(λ_min))', ['Only the absorption of pure water', 'Only the wind speed', 'The sea-surface temperature'],
      'Textbook, The Secchi Disk. The advantage is that K_d(λ_min) can be estimated from multi-/hyperspectral satellite imagery.', 3, 'Secchi', origin='bo_sung', src='Textbook: The Secchi Disk')
    A('Lecture slide 4 mentions Secchi depth data. Which two values of the Secchi depth (m) result from the classic formula with Γ = 8 for (K_d = 0.04, c = 0.10 m⁻¹) and (K_d = 0.3, c = 1.0 m⁻¹)?',
      f'≈ {SC["Kd0.04_c0.1"]:.0f} m and ≈ {SC["Kd0.3_c1.0"]:.1f} m', [f'≈ {SC["Kd0.3_c1.0"]:.0f} m and ≈ {SC["Kd0.04_c0.1"]:.1f} m', '≈ 8 m and ≈ 8 m', '≈ 1 m and ≈ 1 m'],
      f'8/(0.04 + 0.10) = {SC["Kd0.04_c0.1"]:.1f} m; 8/(0.3 + 1.0) = {SC["Kd0.3_c1.0"]:.2f} m (Python, formula vs root finding).', 2, 'Calculation', origin='bo_sung', src='Textbook: The Secchi Disk; Lecture, slide 4')
    A('How do the spectra of R change as Chl increases in Case 1 waters (Morel & Prieur, textbook)?',
      'R in the blue-violet decreases, a minimum forms near 440 nm and the maximum shifts toward 565–570 nm', ['R increases everywhere', 'The maximum moves to 400 nm', 'Nothing changes'],
      'Textbook, Classification Schemes: also a weak minimum near 665 nm, a fluorescence maximum near 685 nm and a hinge point (little change) in the 560–640 nm band.', 2, 'Case 1/2 spectra', origin='bo_sung', src='Textbook: Classification Schemes')
    A('How do R spectra of Case 2 (turbid) waters differ from Case 1?',
      'R is higher, there is no minimum at 440 nm, curves are convex between 400 and 560 nm and R increases with turbidity, especially above 550 nm', ['R is lower and has a sharper minimum at 440 nm', 'R is zero in the blue', 'R is identical to Case 1'],
      'Textbook, Classification Schemes (Morel & Prieur 1977): inverted “U” rather than inverted “V” shape; maximum near 560 nm; waters look blue-green or green, bright and milky.', 2, 'Case 1/2 spectra', origin='bo_sung', src='Textbook: Classification Schemes')
    A('In the classical relation R ≈ f b_b/(a + b_b) (Gordon et al. 1975; not on the crawled textbook pages), how does R react to an increase in a at fixed b_b?',
      'R decreases: more absorption means less light leaves the sea', ['R increases', 'R is unchanged', 'R becomes negative'],
      f'With f = 1: clear water (a = 0.02, b_b = 0.002 m⁻¹) R/f = {R["clear_a0.02_bb0.002"]:.3f}; turbid (a = 0.5, b_b = 0.05) {R["turbid_a0.5_bb0.05"]:.3f}. Qualitative reasoning only: the relation is not verified on the textbook pages we crawled.', 3, 'IOP–AOP link', origin='bo_sung', src='Classical result, flagged in textbook/map.md')

    B.essay('(a) Define K_d and write the irradiance profile. (b) Compute the depth of the 1 % light level for K_d = 0.04 and 0.3 m⁻¹. (c) Explain why K_d is an AOP while c is an IOP. (Textbook content.)',
            f'(a) K_d ≡ −d ln E_d/dz; E_d(z) = E_d(0) exp(−K_d z). (b) z = 4.605/K_d: {z("0.04"):.0f} m and {z("0.3"):.1f} m. (c) c = a + b depends only on the medium; K_d depends also on the angular distribution of light (a ≤ K_d μ̄_d ≤ c) and so changes with Sun angle.',
            2, 'K_d', origin='bo_sung', src='Textbook: K functions')
    B.essay('Describe the classic Secchi-depth formula and the Lee et al. (2015) alternative. Which one can be applied from satellite data, and why? Compute z_SD for K_d = 0.1 and c = 0.2 m⁻¹ with Γ = 6, 8, 9.',
            f'Classic: z_SD = Γ/(K_dv + c_v), Γ ≈ 6–9 (8 default), needs iteration because K_dv and c_v are averages to z_SD. Lee et al.: z_SD = γ/(2.5 K_d(λ_min)), with c replaced by 1.5 K_d; K_d(λ_min) can be estimated from satellite multispectral data. Numbers: {V["secchi_range_gamma_6_9_Kd0p1_c0p2"][0]:.1f}, {SC["Kd0.1_c0.2"]:.1f}, {V["secchi_range_gamma_6_9_Kd0p1_c0p2"][1]:.1f} m.',
            3, 'Secchi', origin='bo_sung', src='Textbook: The Secchi Disk')

    NOTE = 'Textbook, not in the lecture'
    sl = [
        S('Light field: IOPs and AOPs', cards(card('IOPs', 'a, b, β, c<br>medium only'), card('AOPs', 'K<sub>d</sub>, R, R<sub>rs</sub><br>medium + light field'), card('Not in the lecture file', 'Outline slide 9 lists “Link between IOPs and the light field” but no slide covers it; this is textbook content'))),
        S('K<sub>d</sub>, euphotic and Secchi depth', EQS_('kd')),
        S('Reflectances', EQS_('refl')),
        S('Diffuse attenuation and reflectance', dtable(tbl(['Quantity', 'Definition', 'Unit'], [['K<sub>d</sub>', '−d ln E<sub>d</sub>/dz', 'm⁻¹'], ['E<sub>d</sub>(z)', 'E<sub>d</sub>(0) exp(−K<sub>d</sub> z)', 'W m⁻² nm⁻¹'], ['R', 'E<sub>u</sub> / E<sub>d</sub>', '—'], ['R<sub>rs</sub>', 'L<sub>w</sub> / E<sub>d</sub>', 'sr⁻¹']]), 'xl') + callout('info', 'Source', 'Textbook (oceanopticsbook.info): K functions and Reflectances; not in the lecture file')),
        S('Penetration and euphotic depth', img('euphotic_secchi', 700, cap='Own computation (textbook formulas): 1 % light depth = 4.6/K<sub>d</sub>; Secchi = 8/(K<sub>d</sub>+c)')),
        S('Euphotic depth: numbers', dtable(tbl(['K<sub>d</sub> (m⁻¹)', '1 % depth (m)', '1/K<sub>d</sub> (m)'], [[k, f'{EU[k]["z1pct"]:.1f}', f'{EU[k]["penetration_1_over_Kd"]:.1f}'] for k in ('0.03', '0.04', '0.1', '0.3', '1.0')]), 'xl')),
        S('Secchi depth', dtable(tbl(['Formula', 'Note'], [['z<sub>SD</sub> = Γ / (K<sub>dv</sub> + c<sub>v</sub>)', 'Γ ≈ 6–9, default 8'], ['z<sub>SD</sub> = γ / (2.5 K<sub>d</sub>(λ<sub>min</sub>))', 'Lee et al. 2015; satellite-friendly'], ['Example K<sub>d</sub> = 0.1, c = 0.2', f'z<sub>SD</sub> = {SC["Kd0.1_c0.2"]:.1f} m (Γ = 8)']]), 'xl') + callout('info', 'Textbook note', 'Γ varies from about 6 to 9 with the water reflectance; the formula must be iterated because K<sub>dv</sub> and c<sub>v</sub> are averaged to z<sub>SD</sub>')),
        S('Case 1 versus Case 2 reflectance', cards(card('Case 1', 'Blue minimum at 440 nm; maximum shifts to 565–570 nm as Chl rises; fluorescence peak 685 nm'), card('Case 2', 'Higher R, no 440 nm minimum, convex shape, maximum ≈ 560 nm, R rises with turbidity'), cols=2)),
        S('Key points', dul(['AOPs depend on the light field; IOPs do not', 'K<sub>d</sub> is the decay rate of E<sub>d</sub> with depth; 1 % depth = 4.6/K<sub>d</sub>', 'R<sub>rs</sub> = L<sub>w</sub>/E<sub>d</sub> in sr⁻¹', 'Secchi: z = Γ/(K<sub>d</sub> + c), Γ ≈ 8'], xl=True)),
    ]
    mod = dict(id='mg', slug='07-light-field', title='G · Light field (textbook)', en='AOPs, K_d, reflectance, Secchi depth, IOP–AOP link: NOT in the lecture file, from the textbook',
               qtitle='Guiding question: how do IOPs become the light field and the signal a satellite sees? (textbook, not in the lecture file)',
               question='<div class="callout warn"><b class="t">Source label</b>The lecture outline (slide 9) lists “Link between IOPs and the light field”, but the 120-slide file contains no slide on it. This module is built from the Ocean Optics Web Book (oceanopticsbook.info, CC BY 2.0) and is labelled as textbook content throughout.</div><p>AOPs are the radiometric quantities that describe the light field in the water (K_d, reflectance). They depend on the IOPs and on the Sun and sky.</p>',
               sections=[
                ('IOP versus AOP', '<p><b>Apparent optical properties</b> depend both on the medium (the IOPs) and on the angular structure of the radiance, and are stable enough to describe a water body. E<sub>d</sub> alone is not stable: a cloud can change it by an order of magnitude within seconds (textbook, <i>Apparent Optical Properties</i>).</p>'),
                ('K_d, reflectance and penetration', '<p>' + 'The diffuse attenuation coefficient and the profile of downwelling irradiance (textbook, <i>K functions</i>):</p>' + EQ('kd') +
                 '<p>Reflectance (textbook, <i>Reflectances</i>):</p>' + EQ('refl') + '<p>Qualitatively the reflectance follows the classical relation below (Gordon et al., 1975; <b>not found on the pages we crawled</b>, so used only for reasoning):</p>' + EQ('gordon')
                 + f'<p><b>Numbers (Python).</b> 1 % light depth = 4.605/K<sub>d</sub>: {z("0.03"):.0f}, {z("0.04"):.0f}, {z("0.1"):.0f}, {z("0.3"):.1f} m for K<sub>d</sub> = 0.03, 0.04, 0.1, 0.3 m⁻¹.</p>'),
                ('Secchi depth', '<p>Classic theory z<sub>SD</sub> = Γ/(K<sub>dv</sub> + c<sub>v</sub>) and the Lee et al. (2015) alternative z<sub>SD</sub> = γ/(2.5 K<sub>d</sub>(λ<sub>min</sub>)) are both in the K<sub>d</sub> equation above; the second can be used from satellite imagery (textbook, <i>The Secchi Disk</i>). Example: K<sub>d</sub> = 0.1, c = 0.2 m⁻¹ gives '
                 + f'{SC["Kd0.1_c0.2"]:.1f} m.</p>')],
               checklist=['Define IOP vs AOP and say why E_d is not an AOP.', 'Write K_d, E_d(z), R and R_rs with units.', 'Compute z_1% = 4.6/K_d and a Secchi depth.', 'Describe Case 1 and Case 2 reflectance spectra.', 'Say clearly that this module is not in the lecture file.'],
               summary=['AOP phụ thuộc cả môi trường lẫn trường sáng; K_d = −d ln E_d/dz.', 'Độ sâu 1 % = 4,6/K_d; Secchi = Γ/(K_d + c), Γ ≈ 8.', 'Mô-đun này lấy từ giáo trình, KHÔNG có trong file slide.'],
               calcs=[('euphotic', 'Euphotic and Secchi depth')], quiz_n=10,
               v2=dict(we_title='Clear versus turbid', we=KL(r'K_d=0.04\ \mathrm{m^{-1}}:\ \ z_{1\%%}=%.0f\ \mathrm{m}\qquad K_d=0.3\ \mathrm{m^{-1}}:\ \ z_{1\%%}=%.0f\ \mathrm{m}' % (z("0.04"), z("0.3")), cap='Same formula, 7.5 times different depth.'),
                       qa=[('Is K_d an IOP?', 'No, it depends on the Sun angle (textbook).'), ('Which wavelength matters for Secchi depth in the Lee model?', 'The wavelength of minimum K_d.')],
                       hooks=[('IOP = water; AOP = water + light.', 'IOP = nước; AOP = nước + ánh sáng.')]))
    return mod, sl, B
