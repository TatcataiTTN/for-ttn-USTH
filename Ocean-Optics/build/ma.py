# -*- coding: utf-8 -*-
"""Module A — Light in water and the inherent optical properties (slides 2-19; Case 1/2 slides 14-16)."""
import math
from lib import *
from qcore import Bank
V = VERIFIED
def LS(n, h=470, cap=None):
    return (f'<figure class="fig ctr"><img src="../assets/images/lecture/full/p{n:03d}.jpg" alt="" style="height:{h}px">'
            f'<div class="cap">{cap or "Lecture slide " + str(n)}</div></figure>')

def build():
    B = Bank('ma', seed=11); A = B.add
    L = 'Lecture'; T = 'Textbook'
    A('Which equation does the lecture present as the theoretical frame for the interaction of light and matter in the water body?',
      'The radiative transfer equation, dL/dr = −cL + (scattering into the beam) + S', ['The Beer–Lambert law E(z) = E(0)exp(−Kz), which has no scattering term', 'The Planck function B(λ,T) for the emission of the water', 'The Snell–Descartes law n₁ sinθ₁ = n₂ sinθ₂ at the sea surface'],
      'Slide 5: “The radiative transfer equation provides the theoretical frame to understand light and matter interaction in the water body.” Loss by absorption and scattering (c = a + b), gain by scattering from other directions, plus a source term S.', 1, 'RTE', src='Lecture, slide 5')
    A('In the radiative transfer equation of slide 5, which combination of coefficients multiplies −L?',
      'The attenuation coefficient c = a + b', ['The absorption coefficient a only', 'The backscattering coefficient b_b only', 'The scattering coefficient b only'],
      'Light leaves the beam by absorption (a) and by scattering out of the beam (b); the sum is c. Slide 5: “b + a = c”.', 1, 'RTE', src='Lecture, slide 5')
    A('Which units does the lecture give for the absorption coefficient a and the volume scattering function β?',
      'a in m⁻¹; β in m⁻¹ sr⁻¹', ['a in m⁻¹ sr⁻¹; β in m⁻¹', 'a and β both in m⁻¹', 'a in m² ; β in m² sr⁻¹'],
      'Slide 17: a(λ) in m⁻¹, β(ψ,λ) in m⁻¹ sr⁻¹ (power scattered per unit solid angle, per metre, per unit incident flux). Integrating β over 4π steradians gives b in m⁻¹.', 1, 'IOP definitions', src='Lecture, slide 17')
    A('Which formula gives the total scattering coefficient when the volume scattering function has revolution symmetry?',
      'b = 2π ∫₀^π β(θ) sinθ dθ', ['b = ∫₀^π β(θ) dθ without the sinθ factor', 'b = 2π ∫₀^{π/2} β(θ) cosθ dθ', 'b = β(90°), the value at right angle'],
      'Slide 18: b = ∫_{4π} β dω = 2π∫β(θ)sinθ dθ. The sinθ comes from the solid-angle element dω = 2π sinθ dθ. b_f uses the limits 0–π/2, b_b π/2–π.', 1, 'IOP definitions', src='Lecture, slide 18')
    A('How is the backscattering coefficient b_b defined on slide 18?',
      'b_b = 2π ∫ from π/2 to π of β(θ) sinθ dθ', ['b_b = 2π ∫ from 0 to π/2 of β(θ) sinθ dθ', 'b_b = b − a', 'b_b = β(180°) multiplied by 4π'],
      'Backscattering is the part of b scattered into the backward hemisphere (θ > 90°). The forward part b_f uses 0 to π/2, and b = b_f + b_b.', 1, 'IOP definitions', src='Lecture, slide 18')
    A('Which of the following is an inherent optical property?',
      'The absorption coefficient a(λ)', ['The diffuse attenuation coefficient K_d', 'The remote-sensing reflectance R_rs', 'The downwelling irradiance E_d'],
      'Slide 11: IOPs depend only on the in-water constituents. K_d, R_rs and E_d depend on the illumination (Sun angle, sky, clouds) and are apparent optical properties (textbook, Apparent Optical Properties).', 1, 'IOP vs AOP', src='Lecture, slide 11; Textbook: Apparent Optical Properties')
    A('A water body has the same IOPs when the Sun is at the zenith and when it is at 60°. What property of IOPs does this illustrate?',
      'They do not depend on the illumination conditions above the water', ['They are proportional to the cosine of the solar zenith angle', 'They are only defined at noon', 'They change with the sky but not with the constituents'],
      'Slide 11: “IOPs only depend on the in-water constituents and do not depend on the above-water illumination conditions. For a given water body, IOPs are the same for a sun at zenith and at 60°.”', 1, 'IOP vs AOP', src='Lecture, slide 11')
    A('Which relation expresses the additivity principle for the total absorption coefficient?',
      'a = a_w + a_CDOM + a_ph + a_NAP', ['a = a_w × a_CDOM × a_ph × a_NAP', 'a = a_w + b_p + b_bp', 'a = c − b_bw'],
      'Slide 19. Additivity is what allows separate models for each constituent of sea water. Also b = b_w + b_p and b_b = b_bw + b_bp.', 1, 'Additivity', src='Lecture, slide 19')
    A('Which list gives the optically significant components named on slide 12?',
      'Pure sea water, suspended particles (larger than ≈ 0.2 µm), dissolved matter (CDOM) and air bubbles', ['Pure sea water, Sun, sky and the sea bottom', 'Chlorophyll, nitrate, phosphate and silicate only', 'Plankton, fish, whales and seabirds'],
      'Slide 12: pure sea water; suspended particles (phytoplankton, bacteria, detritus, mineral particles); dissolved matter (coloured dissolved organic matter or yellow substance); air bubbles.', 1, 'Constituents', src='Lecture, slide 12')
    A('Slide 7 says that the colour you see from a boat at the sea surface is NOT ocean colour radiometry. Why?',
      'It comes from reflection of sun and sky light, not from interactions of photons with in-water components', ['It is produced only by the sea bottom in shallow water', 'It is measured in the infrared, not in the visible', 'It only exists at night'],
      'Slide 7: ocean colour radiometry is the spectral variation of the water-leaving signal in the visible; “the reflection of sun and sky light changes the color you observed at the sea surface. This is not ocean color radiometry, as it is not related to interactions between photons and in-water components.”', 1, 'Ocean colour', src='Lecture, slide 7')
    A('What is the definition of Case 1 waters used today (Gordon & Morel 1983; Morel 1988)?',
      'Waters whose optical properties are determined primarily by phytoplankton and co-varying CDOM and detritus', ['Waters closer than 200 km to the coast', 'Waters shallower than 200 m', 'Waters without any phytoplankton'],
      'Textbook, Classification Schemes: Case 1 = determined primarily by phytoplankton and co-varying CDOM and detritus degradation products; Case 2 = everything else (mineral particles, CDOM or microbubbles not co-varying with phytoplankton). It is about co-variation, not distance or depth.', 1, 'Case 1/2', src='Lecture, slide 14; Textbook: Classification Schemes')
    A('On the P–Y–S triangle of slide 14, which corner stands for the “suspended material” that varies independently of phytoplankton?',
      'S (suspended material)', ['P (phytoplankton)', 'Y (yellow substances), which is the same as the sea bottom', 'There is no such corner'],
      'Slide 14: corners P = phytoplankton, Y = yellow substances (CDOM), S = suspended material. Case 1 is the band near P; Case 2 covers the rest of the triangle, where Y and S vary independently of P.', 2, 'Case 1/2', src='Lecture, slide 14')
    A('The maps of slide 15 (Matsushita et al., 2012) give the percentage of Case-1 waters per season. Which statement matches them?',
      'Case 1 covers 81–87 % of the ocean surface depending on the season, and Case 2 is not limited to the coast', ['Case 1 covers about 30 % and Case 2 about 70 % of the ocean', 'Case 2 waters are only found within 10 km of the coast', 'The percentage of Case 1 is exactly 100 % in every season'],
      'Slide 15 reads: spring 2003 83 %, summer 2003 81 %, autumn 2003 87 %, winter 2004 87 %. Green (Case 2) pixels appear along coasts and also at high latitudes.', 2, 'Case 1/2', src='Lecture, slide 15')
    A('Why does the lecture show the “Optical Water Class” framework (slide 16) after Case 1/Case 2?',
      'It describes the optical variability and complexity of natural waters better than just two cases', ['It replaces the radiative transfer equation', 'It only applies to fresh water lakes', 'It is a classification of ships'],
      'Slide 16: “The Optical Water Class framework is more suitable to account for the optical variability and complexity of natural waters” (Loisel et al., 2023); the map shows 17 classes (violet = clearest gyres, red/green = coastal and polar).', 2, 'Water classes', src='Lecture, slide 16')
    A('A collimated beam crosses a path of 1 m in water with c = 0.5 m⁻¹ and no source. Which fraction is left in the beam?',
      f'e^(−0.5) ≈ {math.exp(-0.5):.2f}', ['e^(−1) ≈ 0.37, using the path in the exponent only', '1 − e^(−0.5) ≈ 0.39, the fraction that is lost', '0.5, because c is a fraction'],
      'Solution of dL/dr = −cL: L = L₀ e^(−c r) = e^(−0.5) = 0.607 (Python, data/verified.json). Beer–Lambert uses c = a + b, because scattered photons also leave the beam.', 2, 'Calculation', src='Lecture, slide 5 (RTE without gain terms)')
    A('A volume has a = 0.08 m⁻¹ and b = 0.12 m⁻¹. Which is the attenuation coefficient c, and which fraction of c is due to absorption?',
      'c = 0.20 m⁻¹, and absorption is 40 % of the attenuation', ['c = 0.08 m⁻¹, and absorption is 100 %', 'c = 0.20 m⁻¹, and absorption is 60 %', 'c = 0.04 m⁻¹, the average of a and b'],
      'c = a + b = 0.20 m⁻¹ (slide 18); a/c = 0.08/0.20 = 0.40. The ratio b/c = 0.60 is the single-scattering albedo of the volume (textbook definition).', 2, 'Calculation', src='Lecture, slide 18')
    A('Why does the lecture say that, in Case 2 waters, one cannot predict a and b from the chlorophyll concentration alone?',
      'Mineral particles and CDOM vary independently of phytoplankton, so Chl no longer controls the optical properties', ['Chlorophyll does not absorb light', 'Case 2 waters contain no phytoplankton', 'The Sun does not illuminate Case 2 waters'],
      'Case 2 means other constituents (minerals, CDOM) that do not co-vary with phytoplankton influence the optics (textbook definition, slide 14 triangle). This is why Case-1 relations such as b_p = 0.30 Chl^0.7 (slide 65) cannot be used in a river plume.', 2, 'Case 1/2', src='Lecture, slides 14 and 65; Textbook: Classification Schemes')
    A('Slide 10 gives reasons to care about IOPs. Which of the following is one of them?',
      'IOPs are proxies of biogeochemical parameters (Chl, CDOM, POC, PIC, size, …) and can be measured at high frequency or retrieved from space', ['IOPs give the temperature of the water directly', 'IOPs are constant in time and space', 'IOPs replace the need for any in-situ sampling'],
      'Slide 10: IOPs control light propagation (primary production, visibility, UV impact…), change the heating rate of the water column, act as proxies of biogeochemical parameters, can be measured at high frequency and retrieved from space.', 1, 'Why IOPs', src='Lecture, slide 10')
    A('Which statement about the Secchi-depth and satellite data on slide 4 is correct?',
      'About half a million Secchi/Chl points were collected over 100 years, while SeaWiFS collects about as many observations every ~30 seconds', ['Secchi disks have collected more data than all satellites together', 'Satellites collect data only once a year', 'Secchi data cover the whole ocean evenly'],
      'Slide 4 (Boyce et al., Nature, 2010): roughly ½ million data points over 100 years, with spatial bias and major gaps (“pin-pricks”); SeaWiFS collects roughly ½ million independent observations about every 30 seconds.', 1, 'Sampling', src='Lecture, slide 4')

    B.essay('(a) State the radiative transfer equation as given in the lecture and name each term. (b) Define a, β, b, b_f, b_b and c. (c) State the additivity principle and say why it matters.',
            'Answer key. (a) dL(θ,φ)/dr = −c L + (scattering into the beam from all directions, with β) + S: loss by absorption (a), loss by scattering out of the beam (b), gain by scattering into the beam, S internal sources (slide 5). (b) a = fraction of incident flux absorbed per unit path (m⁻¹); β = scattered power per unit solid angle, per metre, per incident flux (m⁻¹ sr⁻¹); b = 2π∫β sinθ dθ; b_f from 0 to π/2, b_b from π/2 to π; c = a + b (slides 17–18). (c) a = a_w + a_CDOM + a_ph + a_NAP, b = b_w + b_p, b_b = b_bw + b_bp (slide 19); lets us build separate models for each constituent and sum them.',
            2, 'RTE and IOPs', src='Lecture, slides 5, 17–19')
    B.essay('Explain the difference between IOPs and AOPs with two examples each. Why is E_d not a good AOP? (Textbook content, not in the lecture file.)',
            'IOPs: a, b, β, c, depend only on the medium; they add up over constituents (slides 11, 19). AOPs: K_d, R (= E_u/E_d), R_rs depend on the medium and on the light field but are stable enough to describe a water body. E_d satisfies the first part of the definition but a cloud can change it by an order of magnitude within seconds while the water does not change, so it is not stable (Textbook, Apparent Optical Properties).',
            2, 'IOP vs AOP', origin='bo_sung', src='Textbook: Apparent Optical Properties; Lecture slide 11')
    B.essay('Describe Case 1 and Case 2 waters, then explain why the lecture introduces optical water classes. Use the numbers of slide 15 to correct the idea that Case 2 means coastal.',
            'Case 1: optical properties determined mainly by phytoplankton and co-varying CDOM and detritus; Case 2: everything else, with minerals/CDOM/bubbles not co-varying (Morel & Prieur 1977; textbook). Classes: 17 optical classes describe a continuum (slide 16). Slide 15: Case 1 = 83 % (spring 2003), 81 % (summer), 87 % (autumn), 87 % (winter 2004); the green Case-2 pixels also appear at high latitudes, so Case 2 is not just coastal.',
            2, 'Case 1/2', src='Lecture, slides 14–16')

    # ---------------- slides ----------------
    sl = [
        S('Why light–water interaction matters', cards(card('Light-dependent processes', 'Photosynthesis, visibility, predator–prey relations, vertical migration (slide 3)'), card('In-situ studies', 'Biogeochemical and physical processes at high frequency and over long periods (slide 3)'), card('Space', 'Exploitation of the ocean-colour signal from space (slide 3)'))),
        S('Ocean colour is not surface reflection', ulb(['Ocean colour: spectral variations of the <b>water-leaving signal</b> in the visible', 'Sun and sky reflection changes the colour at the surface but is <b>not</b> ocean colour', 'It comes from photons interacting with in-water components (slide 7)', 'Marine optics links components → IOPs → light field (slide 8)'], 34, 38)),
        S('Radiative transfer in a water slab', cols(LS(5, 430), dul(['Loss by absorption (a)', 'Loss by scattering (b)', 'Gain by scattering (b)', '<b>c = a + b</b>', 'Source term S (fluorescence, Raman…)']), flex=[3, 2])),
        S('Absorption and the volume scattering function', cols(LS(17, 430), dul(['<b>a</b> in m⁻¹', '<b>β(ψ,λ)</b> in m⁻¹ sr⁻¹: angular distribution of scattered power', 'Everything else is derived from a and β']), flex=[3, 2])),
        S('Scattering coefficients', dtable(tbl(['Quantity', 'Definition', 'Unit'], [['b', '2π ∫₀^π β(θ) sinθ dθ', 'm⁻¹'], ['b<sub>f</sub>', '2π ∫₀^{π/2} β(θ) sinθ dθ', 'm⁻¹'], ['b<sub>b</sub>', '2π ∫<sub>π/2</sub>^π β(θ) sinθ dθ', 'm⁻¹'], ['c', 'a + b = a + b<sub>f</sub> + b<sub>b</sub>', 'm⁻¹']]), 'xl') + callout('info', 'Reminder', 'a, b, c in m⁻¹; β in m⁻¹ sr⁻¹; b<sub>f</sub> and b<sub>b</sub> split the same b at 90°')),
        S('Additivity of IOPs', cards(card('Absorption', 'a = a<sub>w</sub> + a<sub>CDOM</sub> + a<sub>ph</sub> + a<sub>NAP</sub>'), card('Scattering', 'b = b<sub>w</sub> + b<sub>p</sub>'), card('Backscattering', 'b<sub>b</sub> = b<sub>bw</sub> + b<sub>bp</sub>'))),
        S('Optically significant constituents', cards(card('Pure sea water', 'Molecules and salt'), card('Particles &gt; 0.2 µm', 'Phytoplankton, bacteria, detritus, minerals'), card('Dissolved matter', 'CDOM (yellow substance)'), card('Air bubbles', 'Near the surface'), cols=4)),
        S('Case 1 and Case 2 waters', cols(LS(14, 430, 'Lecture slide 14 (IOCCG, 2000)'), dul(['<b>P</b> phytoplankton', '<b>Y</b> yellow substances', '<b>S</b> suspended material', 'Case 1: band near P', 'Case 2: Y and S vary independently']), flex=[3, 2])),
        S('Case 1 share of the ocean', cols(LS(15, 430, 'Lecture slide 15 (Matsushita et al., 2012)'), dul(['Spring 2003: <b>83 %</b>', 'Summer 2003: <b>81 %</b>', 'Autumn 2003: <b>87 %</b>', 'Winter 2004: <b>87 %</b>', 'Case 2 also at high latitudes']), flex=[3, 2])),
        S('Optical water classes', cols(LS(16, 430, 'Lecture slide 16 (Loisel et al., 2023)'), dul(['17 classes', 'Violet: clearest gyres', 'Green/red: coastal, polar', 'A continuum, not two boxes']), flex=[3, 2])),
        S('Key points', dul(['c = a + b; β in m⁻¹ sr⁻¹', 'IOPs: independent of illumination, additive', 'Ocean colour ≠ surface reflection', 'Case 1/2 = co-variation; 17 optical classes'], xl=True)),
    ]
    k_ = math.exp(-0.5)
    mod = dict(id='ma', slug='01-light-in-water', title='A · Light in water & IOPs', en='Radiative transfer, a, b, c, the volume scattering function, additivity, Case 1/Case 2 (slides 2–19)',
               qtitle='Guiding question: what does light do in sea water, and what do we call the properties that describe it?',
               question='<p>Light entering the sea is absorbed and scattered. This module defines the quantities that describe those two processes (<b>a</b>, <b>β</b>, <b>b</b>, <b>c</b>), explains why they add up, and introduces the water types (Case 1, Case 2, optical classes) used to choose a model.</p>',
               sections=[
                ('Plain words: what happens to a photon in the sea', '<p>A photon in water has two possible fates in a short path: it can be <b>absorbed</b> (its energy becomes heat or chemical energy) or <b>scattered</b> (it changes direction). The lecture (slide 5) writes this as the <b>radiative transfer equation</b>: along a path <i>dr</i> the radiance L is reduced by absorption and scattering out (together c = a + b) and increased by scattering in from all other directions, plus internal sources S.</p>'
                 + eq('Slide 5 (as printed)', 'dL(θ,φ)/dr = −c L(θ,φ) + 2π ∫<sub>0</sub><sup>4π</sup> β(θ,φ,θ″,φ′) L dω′ + S &nbsp;&nbsp; <b>b + a = c</b>') +
                 '<p class="note">Note: the slide prints a factor 2π in front of the integral. The textbook (Radiative Transfer Equations) writes the in-scattering term as ∫β L dω′ over 4π without it; we keep the slide form for the course and mention the difference.</p>'),
                ('The two main IOPs and what is derived from them', '<p>Slide 17: the two main IOPs are the <b>absorption coefficient a</b> (m⁻¹) and the <b>volume scattering function β(ψ,λ)</b> (m⁻¹ sr⁻¹, the angular distribution of scattered power). Everything else follows (slide 18):</p>'
                 + eq('Derived quantities', 'b = ∫<sub>4π</sub> β dω = 2π∫<sub>0</sub><sup>π</sup> β sinθ dθ; &nbsp; b<sub>f</sub>: 0 → π/2; &nbsp; b<sub>b</sub>: π/2 → π; &nbsp; <b>c = a + b</b>') +
                 f'<p><b>Numerical example.</b> With c = 0.5 m⁻¹ a collimated beam keeps e<sup>−0.5</sup> = {k_:.3f} of its power after 1 m (L = L₀e<sup>−cr</sup>, verified in Python).</p>'),
                ('IOP versus AOP, and additivity', '<p><b>IOPs depend only on the constituents</b> and not on illumination: for one water body they are the same for a Sun at the zenith and at 60° (slide 11). <b>AOPs</b> (K<sub>d</sub>, reflectance, …) depend on the medium and on the light field (textbook: <i>Apparent Optical Properties</i>, oceanopticsbook.info). IOPs are <b>additive</b>:</p>'
                 + eq('Slide 19', 'a = a<sub>w</sub> + a<sub>CDOM</sub> + a<sub>ph</sub> + a<sub>NAP</sub>; &nbsp; b = b<sub>w</sub> + b<sub>p</sub>; &nbsp; b<sub>b</sub> = b<sub>bw</sub> + b<sub>bp</sub>') +
                 '<p>This allows a separate model for each constituent (modules B–D) and is why the lecture goes constituent by constituent.</p>'),
                ('Case 1, Case 2 and optical classes', '<p>Morel &amp; Prieur (1977) separated waters in which phytoplankton dominate the optics (Case 1) from those in which other constituents matter (Case 2). The modern wording (textbook, <i>Classification Schemes</i>): Case 1 = optical properties determined primarily by phytoplankton and co-varying CDOM and detritus; Case 2 = everything else. Slide 15 shows that Case 1 covers 81–87 % of the ocean depending on the season; slide 16 introduces 17 <b>optical water classes</b> (Loisel et al., 2023) for a finer description.</p>'
                 '<div class="callout warn"><b class="t">Not verified</b>The numerical meaning of each of the 17 classes (for example the Chl range) is not on the slide, so it is not given here.</div>')],
               checklist=['Write the RTE of slide 5 and name the terms; state c = a + b.', 'Give the units of a, β, b, c and the integrals defining b, b_f, b_b.', 'State additivity for a, b and b_b.', 'Say why IOPs do not depend on the Sun angle and name two AOPs.', 'Define Case 1 / Case 2 (co-variation) and say why “Case 2 = coastal” is wrong (slide 15).'],
               summary=['c = a + b; β (m⁻¹ sr⁻¹) là hàm tán xạ thể tích; b = 2π∫β sinθ dθ.', 'IOP không phụ thuộc chiếu sáng và cộng tính; AOP thì có phụ thuộc.', 'Case 1 = đồng biến với thực vật phù du; Case 2 = còn lại; 17 lớp quang học.'],
               calcs=[('beer', 'Beer–Lambert attenuation')], quiz_n=10,
               v2=dict(we_title='Attenuation of a beam', we=f'<p>a = 0.08 m⁻¹, b = 0.12 m⁻¹ ⇒ c = 0.20 m⁻¹. Over 5 m the beam keeps e<sup>−1.0</sup> = {math.exp(-1):.3f} = 37 %. If only absorption acted (a = 0.08), 67 % would remain: scattering out of the beam is the larger loss here.</p>',
                       qa=[('Why can a transmissometer not measure absorption?', 'Because scattered photons are also removed from the beam; it measures c = a + b (slide 60).'), ('Is E_d an IOP?', 'No: it depends on the Sun and the clouds; it is not even a good AOP (textbook).')],
                       hooks=[('IOPs = what the water is; AOPs = what the light does in it.', 'IOP là bản chất nước; AOP là phản ứng của ánh sáng.'), ('Case 1/2 = co-variation, not geography.', 'Case 1/2 là đồng biến, không phải địa lý.')]),
               photos=None)
    return mod, sl, B
