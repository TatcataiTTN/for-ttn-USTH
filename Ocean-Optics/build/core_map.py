# -*- coding: utf-8 -*-
"""Big 12 for Ocean Optics = 3 key points + 3 formulas + 3 concepts + 3 principles.
Levels in the exam-coverage tables (own assessment): A = full answer from the Big 12; B = Big 12 gives the frame, module facts needed; C = module-specific.
There is NO official exam from the lecturer: coverage numbers refer only to the papers written for this site."""
COLS = ['Key points', 'Formulas', 'Concepts', 'Principles']
ITEMS = [
 dict(id='K1', col=0, title='From water constituents to the colour of the sea',
      st='The ocean is a mixture of <b>water, phytoplankton, non-algal particles (NAP), dissolved organic matter (CDOM) and bubbles</b>. Each one sets the <b>inherent optical properties</b> (a, b, β) → they set the <b>light field</b> (AOPs, reflectance) → that is the <b>ocean-colour signal</b> → biogeochemical variables (Chl, POC, CDOM) come back by <b>inversion</b>. (Slides 3, 5, 8, 9; the AOP link is textbook only.)',
      say='We never measure Chl from space. We measure light leaving the sea; the IOPs link that light to what is in the water.',
      trap='Saying ocean colour is “the reflection of the sea surface” (slide 7 says it is not).', mods=['ma', 'mg'], pages=[3, 5, 7, 8, 9]),
 dict(id='K2', col=0, title='Every product rests on a hypothesis',
      st='Relations between IOPs and Chl, POC or CDOM are <b>statistical</b> (spread of a factor of 2–3), valid for a water type, a region or a season (slides 65–66, 72–77). Case 1 / Case 2 and the <b>optical water classes</b> (slides 14–16) are the hypotheses that decide which relation to use.',
      say='Before using an algorithm, say which water type it assumes and how large the spread around the relation is.',
      trap='Using a Case-1 Chl relation in a river plume.', mods=['ma', 'mf'], pages=[14, 15, 16, 65, 66, 75, 76]),
 dict(id='K3', col=0, title='The ocean is under-sampled: autonomous platforms',
      st='Ships and satellites leave huge gaps in space and time (slides 2, 4, 85); <b>floats, gliders and BGC-Argo</b> add the vertical dimension, work under clouds and in winter, and make seven contributions (slide 101). They carry <b>bio-optical sensors</b>: Chl and CDOM fluorescence, b<sub>bp</sub>, beam-c, irradiance (slides 97–98, 115).',
      say='Satellites see the surface layer when it is clear; platforms see the interior all year.',
      trap='Treating fluorescence as Chl without correcting non-photochemical quenching (slide 80).', mods=['mh', 'mf'], pages=[2, 4, 101, 102, 115]),
 dict(id='F1', col=1, title='Radiative transfer: c = a + b',
      st='The radiative transfer equation: light is <b>lost</b> by absorption and by scattering out of the beam (together the attenuation coefficient <b>c</b>), and <b>gained</b> by scattering in from other directions plus internal sources. A collimated beam decays exponentially with distance. The big equation below is interactive: click any symbol.',
      say='Light is lost by absorption and by scattering out of the beam, and gained by scattering in from other directions.',
      trap='Forgetting that c is attenuation (a + b), not absorption; e.g. using a instead of c in Beer–Lambert for a transmissometer.', mods=['ma', 'me'], pages=[5, 17, 18]),
 dict(id='F2', col=1, title='IOP = Σ (N/V)·Q·S',
      st='Every inherent optical property of particles is a <b>sum over particle classes</b> of number per cubic metre × efficiency factor × geometric area. Large particles scale with area, small particles with volume (slide 64). Click any symbol in the big equation below.',
      say='A property of the water is the sum over particle classes of number × cross-section.',
      trap='Mixing σ (m²) and Q (no unit).', mods=['mf', 'md'], pages=[63, 64]),
 dict(id='F3', col=1, title='Spectral laws: exponential and power law',
      st='Three spectral fingerprints: <b>CDOM and NAP</b> fall exponentially toward the red; <b>particle scattering</b> follows a weak power law; <b>pure-water scattering</b> is almost Rayleigh (λ⁻⁴·³). Click any symbol in the big equations below.',
      say='Dissolved and detrital material fall exponentially toward the red; particle scattering follows a weak power law; molecular scattering a strong one.',
      trap='Writing λ₀ in nm for S′ in µm⁻¹, or forgetting the minus sign.', mods=['mb', 'mc', 'md'], pages=[20, 23, 35, 41, 49]),
 dict(id='C1', col=2, title='IOP versus AOP',
      st='<b>IOPs</b> (a, b, β, c) depend only on the medium, add up over constituents and do not depend on illumination. <b>AOPs</b> (K<sub>d</sub>, R, R<sub>rs</sub>) depend on the medium <i>and</i> on the light field (Sun, sky, depth) but are stable enough to describe a water body (textbook).',
      say='IOPs are what the water is; AOPs are what the light does in it.',
      trap='Calling E<sub>d</sub> an AOP: it changes by a factor of 10 when a cloud passes (textbook).', mods=['ma', 'mg'], pages=[17, 19]),
 dict(id='C2', col=2, title='Case 1, Case 2 and optical water classes',
      st='Case 1: optical properties set mainly by phytoplankton and co-varying CDOM and detritus. Case 2: everything else (mineral particles, CDOM or bubbles not co-varying with Chl). Morel &amp; Prieur 1977 (slide 14). <b>Optical water classes</b> (17 classes, slide 16) describe the continuous variability better than two cases.',
      say='Case 1/2 is a statement about co-variation, not about depth or distance to the coast.',
      trap='“Case 2 = coastal”: slide 15 shows Case 2 also at high latitudes.', mods=['ma', 'mf'], pages=[14, 15, 16]),
 dict(id='C3', col=2, title='Package (discretisation) effect',
      st='Pigments inside a big cell shade each other: <b>Q*<sub>a</sub> = a<sub>φ</sub>/a<sub>sol</sub></b> falls from 1 (no packaging) toward 0 (maximal) (slide 33). That is why the Chl-specific absorption a*<sub>ph</sub> drops by up to a factor of 4 from low to high Chl (slides 32–33).',
      say='A big cell absorbs less per unit of pigment than the same pigment dispersed in solution.',
      trap='Forgetting that photoacclimation (slide 34) also changes a*<sub>ph</sub>.', mods=['mc', 'mf'], pages=[32, 33, 34]),
 dict(id='R1', col=3, title='Additivity',
      st='<b>a = a<sub>w</sub> + a<sub>CDOM</sub> + a<sub>ph</sub> + a<sub>NAP</sub></b>, <b>b = b<sub>w</sub> + b<sub>p</sub></b>, <b>b<sub>b</sub> = b<sub>bw</sub> + b<sub>bp</sub></b> (slide 19). It allows separate models for each constituent and is the basis of every bio-optical model.',
      say='Because IOPs add up, we can model each constituent alone and sum.',
      trap='Adding AOPs (they are not additive).', mods=['ma', 'mc', 'md'], pages=[19, 45, 58]),
 dict(id='R2', col=3, title='Each constituent has a spectral fingerprint',
      st='Water: absorption rises beyond 550 nm (slide 24); phytoplankton: blue (≈ 440) and red (≈ 675) peaks (slide 29); CDOM/NAP: exponential decay with λ (slide 41); particles: weak spectral dependence (slides 49–52). The <b>shape</b> of the spectrum identifies who absorbs or scatters.',
      say='Read the spectrum: slope = CDOM/NAP, peaks = pigments, flat = particles, steep = molecules.',
      trap='Reading amplitude as if it were shape.', mods=['mb', 'mc', 'md'], pages=[24, 29, 41, 49]),
 dict(id='R3', col=3, title='Size and refractive index control particle scattering',
      st='Large particles scatter mainly by <b>diffraction</b> (forward lobe, ∝ area); small ones by refraction/reflection (Rayleigh, ∝ volume) (slides 47, 64). <b>b<sub>bp</sub>/b<sub>p</sub> depends on refractive index first, then size</b> (slide 71): low n (phytoplankton, 1.01–1.09 textbook) gives a small ratio, high n (minerals, 1.15–1.20) a larger one.',
      say='The backscatter ratio tells you whether particles are organic or mineral.',
      trap='Assuming b<sub>bp</sub>/b<sub>p</sub> is a constant (it varies about 10×).', mods=['md', 'mf'], pages=[47, 64, 71, 84]),
]
# (question id, part, level, [Big-12 ids]) — filled by papers.py for the written papers
P1 = []
def stats(parts):
    n = len(parts); a = sum(1 for p in parts if p[2] == 'A'); b = sum(1 for p in parts if p[2] == 'B'); c = n - a - b
    used = {}
    for p in parts:
        for i in p[3]: used[i] = used.get(i, 0) + 1
    return dict(n=n, A=a, B=b, C=c, skeleton=(a + b) / max(n, 1), full=a / max(n, 1), used=used)
def serves(parts, qs=None):
    out = {i['id']: [] for i in ITEMS}
    for q, _, _, ids in parts:
        for i in ids:
            if q not in out[i]: out[i].append(q)
    return out
