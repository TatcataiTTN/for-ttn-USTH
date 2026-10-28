# -*- coding: utf-8 -*-
"""M6 — Passive remote sensing of aerosols (study guide Ch.6)."""
from lib import *
from qcore import Bank
V = VERIFIED
AN = V['angstrom']

def two6(a, b): return cards(a, b, cols=2)

def build():
    B = Bank('m6', seed=6)
    al = AN['alpha']
    B.add('Name three aerosol properties that can be measured by passive satellite sensors.',
          'Aerosol optical depth AOD, Ångström exponent (particle size), single-scattering albedo ω₀ (absorption)', ['Particle temperature, pressure and density', 'Transmittance, emissivity and brightness temperature', 'Fall speed, electric charge and pH'],
          'Guide 6.1: also aerosol type, refractive index, layer height (ALH) and the UV aerosol index (UVAI). A full answer gives ≥ 3 properties.', 1, 'Properties', origin='goc', src='Study guide Ch.6 (checklist)')
    B.add('How is the aerosol optical depth (AOD) defined?',
          'τ_a = ∫ k_ext,aer(z) dz: the integral of the aerosol extinction coefficient over altitude', ['τ_a = I / I₀, the ratio of intensities', 'τ_a = λ / r, the ratio of wavelength to radius', 'τ_a = σ_s / σ_a, the ratio of scattering to absorption'],
          'Guide 6.1 / Q6(a). AOD is the most robust product and a proxy for aerosol load and PM2.5.', 1, 'Properties', origin='goc', src='Mock exam Q6(a)')
    B.add('How is the Ångström exponent α defined?',
          'τ(λ) = τ(λ₀)·(λ/λ₀)^(−α)', ['τ(λ) = τ(λ₀)·(λ/λ₀)^(+4)', 'τ(λ) = τ(λ₀)·exp(−α·λ)', 'τ(λ) = α/λ'],
          'α measures the spectral dependence of AOD. Rayleigh corresponds to α ≈ 4; coarse aerosol α is near 0; fine aerosol α is large.', 1, 'Ångström', origin='goc', src='Mock exam Q6(a)')
    B.add('What does an Ångström exponent of 1.8 tell you about the particles?',
          'They are fine particles (smoke, urban, sulfate)', ['They are coarse particles (desert dust, sea salt)', 'They do not scatter at all', 'Their size equals the wavelength exactly'],
          'Answer key Q6(a): α ≈ 1.5–2.5 means fine particles; α ≈ 0–0.5 means coarse particles.', 1, 'Ångström', origin='goc', src='Mock exam Q6(a)')
    B.add('Which Ångström exponent is typical of coarse particles such as desert dust and sea salt?',
          'α ≈ 0–0.5', ['α ≈ 1.5–2.5', 'α ≈ 4', 'α ≈ −2'],
          'Coarse particles scatter almost independently of wavelength, so AOD changes very little with λ.', 1, 'Ångström', src='Study guide 6.1')
    B.add(f'AOD is 0.60 at 440 nm and 0.15 at 870 nm. What is the Ångström exponent?',
          f'α ≈ {al:.2f}', ['α ≈ 0.5', 'α ≈ 1.0', 'α ≈ 4.0'],
          f'α = ln(0.60/0.15) / ln(870/440) = {al:.4f}. Cross-checked with a log–log regression (Python). A value near 2 indicates fine particles.', 2, 'Ångström', src='Study guide 6.1 (formula); number computed in Python')
    B.add(f'With α = {al:.2f} and AOD(440) = 0.60, what is the AOD at 550 nm?',
          f'≈ {AN["tau550"]:.2f}', ['≈ 0.75', '≈ 0.60 (unchanged)', '≈ 0.05'],
          f'τ(550) = 0.60 × (550/440)^(−{al:.3f}) = {AN["tau550"]:.4f}. Longer wavelength → smaller AOD.', 2, 'Ångström', src='Number computed in Python')
    B.add('What is the quantity directly measured by passive sensors in aerosol remote sensing?',
          'The top-of-atmosphere spectral reflectance (possibly multi-angle and polarised)', ['The extinction coefficient along a laser beam', 'The temperature of aerosol particles', 'The complex refractive index of the particles'],
          'Guide 6.2: ρ(λ,θ₀,θ,φ) = πI/(μ₀E₀). Aerosols scatter sunlight back to space, so they brighten a dark surface.', 1, 'Principle', origin='goc', src='Study guide Ch.6 (checklist)')
    B.add('What are the four steps of an AOD retrieval such as MODIS Dark Target / Deep Blue?',
          'Cloud screening and pixel selection; surface-reflectance estimate; look-up table from a radiative transfer model; inversion for the best-fit AOD and aerosol model', ['Compute AMF; DOAS fit; subtract the stratosphere; divide for the VCD', 'Emit a pulse; measure the delay; multiply by the speed of light; halve', 'Take logarithms; fit Planck; convert to brightness temperature; correct'],
          'Guide 6.2: the LUT holds TOA reflectance for a set of aerosol models (size distribution, refractive index → ω₀, P(Θ)), AODs and geometries.', 2, 'Principle', origin='goc', src='Study guide Ch.6 (checklist)')
    B.add('Why is it easier to retrieve AOD over the ocean than over a desert in the visible?',
          'The dark ocean lets the aerosol signal dominate; a bright desert masks the aerosol contribution', ['The ocean emits strongly, so it is seen more clearly', 'Deserts have no aerosol to measure', 'The ocean has more cloud than the desert'],
          'Answer key Q6(b). Over bright surfaces use the deep-blue channel (412 nm, dark surfaces), multi-angle/polarisation, or thermal IR.', 2, 'Surface', origin='goc', src='Mock exam Q6(b)')
    B.add('Which strategy is used over bright surfaces such as deserts?',
          'The deep-blue 412 nm channel (surface is dark there), multi-angle/polarisation, or thermal IR', ['Raising the wavelength to 10 µm to increase scattering', 'Assuming zero surface reflectance', 'Using night-time images only'],
          'Guide 6.2 (step 2) and Q6(b). MODIS Deep Blue is an example.', 2, 'Surface', origin='goc', src='Mock exam Q6(b)')
    B.add('What advantage does the passive approach have over active lidar?',
          'Wide swath, daily global coverage, a long time series since 2000, and low cost', ['A vertical profile with 30–60 m resolution', 'Day and night operation over every surface', 'Direct measurement of depolarisation'],
          'Guide 6.3. The two approaches complement each other: passive gives the horizontal map and AOD, active gives the vertical structure (A-Train: MODIS + CALIOP).', 1, 'Passive vs active', origin='goc', src='Mock exam Q6(c)')
    B.add('What is the main limitation of the passive approach?',
          'Little or no vertical information; daytime and cloud-free only; strong dependence on surface reflectance', ['Only a narrow ~100 m swath is covered', 'The lidar ratio has to be assumed to get extinction', 'The revisit time is ~16 days'],
          'Guide 6.3. There is also uncertainty on aerosol type and ω₀ because the problem is ill-posed.', 1, 'Passive vs active', origin='goc', src='Mock exam Q6(c)')
    B.add('What is the main advantage of space lidar (CALIOP, ATLID)?',
          'Vertical profiles, day and night operation including bright surfaces and above clouds, and depolarisation that reveals particle shape', ['Daily global coverage with a swath of thousands of km', 'It needs no model or assumption at all', 'Low cost and low power'],
          'Guide 6.3. Drawbacks: very narrow footprint (~100 m curtain), ~16-day revisit; the lidar ratio must be assumed; low daytime S/N; expensive.', 2, 'Passive vs active', origin='goc', src='Mock exam Q6(c)')
    B.add('Compare MODIS and CALIOP for a Saharan dust plume over the Atlantic: which statement is correct?',
          'MODIS gives a daily AOD map and size information but no altitude; CALIOP gives profiles, day-night data and depolarisation but only a narrow curtain', ['CALIOP gives daily global AOD maps while MODIS gives vertical profiles', 'Both work only in daytime', 'MODIS gives depolarisation and CALIOP gives the horizontal map'],
          'Answer key Q6(c).', 2, 'Passive vs active', origin='goc', src='Mock exam Q6(c)')
    B.add('What is the UV aerosol index (UVAI) used for?',
          'Qualitative detection of absorbing aerosols (smoke, dust), even above clouds', ['Accurate measurement of particle size', 'Measuring aerosol layer height by pulse delay', 'Measuring the optical depth of clouds'],
          'Guide 6.1: UVAI (e.g. OMI) is sensitive to UV absorption and useful when aerosol lies above cloud.', 3, 'Properties', src='Study guide 6.1')
    B.add('Which sensors add information on phase function and refractive index, allowing more properties to be retrieved?',
          'Multi-angle (MISR) and polarimetric (POLDER, SPEXone, HARP2) sensors', ['Only single-channel nadir sensors', 'Only thermal-IR lidars', 'Only passive microwave sensors'],
          'Guide 6.2: multi-angle and polarisation add information on ω₀, size distribution and shape.', 3, 'Principle', src='Study guide 6.2')
    B.essay('(a) Define AOD and the Ångström exponent. What does α = 1.8 tell you about the particles?\n(b) Why is it easier to retrieve AOD over the ocean than over a desert in the visible? Which strategy is used over bright surfaces?\n(c) Compare MODIS (passive) and CALIOP (lidar) for a Saharan dust plume over the Atlantic.',
            '(a) AOD = ∫ k_ext,aer dz; τ(λ) ∝ λ^(−α). α ≈ 1.8 → fine particles (smoke, urban/sulfate).\n(b) Dark ocean → aerosol reflectance dominates the TOA signal; bright desert masks the aerosol. Use deep blue (412 nm), multi-angle/polarisation, or thermal IR.\n'
            '(c) MODIS: wide swath, daily AOD map, size information, but no altitude and daytime only. CALIOP: vertical profile, day and night, depolarisation (non-spherical dust), but a narrow curtain with 16-day revisit.', 3, 'Mock exam', origin='goc', src='Mock exam Q6 (2.5 points) + suggested answer')
    B.essay('Present the principle of passive aerosol remote sensing: measured quantity, retrieval steps, advantages and limits compared with active methods.',
            'Measured: TOA spectral reflectance ρ = πI/(μ₀E₀) (possibly multi-angle, polarised). ρ_TOA = ρ_Rayleigh + ρ_aer + T·ρ_surf/(1 − Sρ_surf); ρ_aer ≈ ω₀τ_a P(Θ)/(4μ₀μ). Steps: cloud screening → surface reflectance → LUT from RT → inversion (least squares/OE) giving AOD(λ), α, fine-mode fraction, (ω₀, type). '
            'Passive: global, daily, long series, but no vertical information, daytime/cloud-free only, depends on the surface. Active: profiles, day-night, but narrow coverage.', 3, 'Overview', origin='goc', src='Study guide Ch.6 (question)')
    B.essay(f'AOD(440) = 0.60 and AOD(870) = 0.15. Compute α and AOD(550); comment on the particle type.',
            f'α = ln(0.60/0.15)/ln(870/440) = {al:.3f}; AOD(550) = 0.60·(550/440)^(−{al:.3f}) = {AN["tau550"]:.3f}. α ≈ 2 → fine particles (smoke, urban, sulfate); AOD falls quickly as wavelength increases.', 2, 'Ångström', src='Study guide 6.1 (extra exercise; numbers checked in Python)')
    sl = [
        cover('Passive remote sensing of aerosols', 'Study guide chapter 6',
              '<b>Atmospheric Remote Sensing</b> · USTH<br>AOD · Ångström · ω₀ · look-up tables · comparison with lidar'),
        S('Aerosol properties measurable from space', cards(
            card('AOD', 'Optical depth, usually at 550 nm. A proxy for aerosol load and PM2.5.'),
            card('Ångström exponent α', 'τ ∝ λ<sup>−α</sup>: α ≈ 0–0.5 coarse; α ≈ 1.5–2.5 fine.'),
            card('Single-scattering albedo ω<sub>0</sub>', 'Amount of absorption; from UV or multi-angle/polarisation.'),
            card('Type and refractive index', 'Dust, smoke, sulfate, sea salt; MISR, POLDER, 3MI.'),
            card('Layer height (ALH)', 'O₂ A-band (TROPOMI), MISR, TIR for dust.'),
            card('UV aerosol index', 'Detects absorbing aerosol, even above clouds.'), cols=3)),
        S('Principle: top-of-atmosphere reflectance', fm('<span class="l">Measured quantity</span>ρ(λ, θ<sub>0</sub>, θ, φ) = π I / (μ<sub>0</sub> E<sub>0</sub>)', 32) +
          fm('<span class="l">Simple model</span>ρ<sub>TOA</sub> = ρ<sub>Rayleigh</sub> + ρ<sub>aer</sub> + T·ρ<sub>surf</sub> / (1 − S ρ<sub>surf</sub>)', 28) +
          fm('ρ<sub>aer</sub> ≈ ω<sub>0</sub> τ<sub>a</sub> P(Θ) / (4 μ<sub>0</sub> μ) &nbsp;(single scattering)', 28)),
        S('Four retrieval steps', cards(card('1. Cloud screening', 'Select cloud-free pixels without sun glint or snow.'), card('2. Surface reflectance', 'Ocean is dark; vegetation uses the 2.1 µm band; deserts use 412 nm.'),
          card('3. Look-up table', 'Radiative transfer for a set of aerosol models, AODs and geometries.'), card('4. Inversion', 'Find the AOD and aerosol model that fit best → α, fine fraction, ω<sub>0</sub>.'), cols=4)),
        S('Ångström exponent', figfit('f9_angstrom', 'Figure 17 (study guide): spectral dependence of optical depth — Rayleigh and Ångström.', 400) + fm(f'α = ln(τ₁/τ₂) / ln(λ₂/λ₁) = {al:.2f} &nbsp;(AOD 0.60 at 440 nm; 0.15 at 870 nm)', 28)),
        S('Effect of the surface', figfit('f16_surface', 'Figure 18 (study guide): TOA reflectance vs AOD — sensitive over dark ocean, almost insensitive over bright desert.', 500)),
        S('Passive vs active: advantages', two6(
            card('Passive (MODIS, VIIRS, MISR, POLDER, TROPOMI)', '• Wide swath, daily global coverage<br>• Long series since 2000<br>• Low cost, many bands<br>• Column: AOD, α, ω<sub>0</sub>'),
            card('Active (CALIOP, ATLID)', '• Vertical profile, 30–60 m<br>• Day and night, bright surfaces, above clouds<br>• Depolarisation → particle shape<br>• Fewer surface assumptions'))),
        S('Passive vs active: limitations', two6(
            card('Passive', '• Little or no vertical information<br>• Daytime and cloud-free only<br>• Depends on surface reflectance<br>• Ill-posed: uncertain type and ω<sub>0</sub>'),
            card('Active', '• ~100 m footprint, ~16-day revisit<br>• Lidar ratio must be assumed<br>• Low S/N in daytime<br>• Expensive, high power'))),
        S('Exam checklist — Chapter 6', chk(['≥ 3 properties: AOD, α / size, ω<sub>0</sub>, type, height, UVAI', 'Measured: TOA spectral reflectance; aerosols brighten a dark surface', 'Method: cloud mask → surface reflectance → LUT → best-fit AOD + model', 'Passive: global, no vertical information; active: profiles, narrow coverage'])),
        S('Key points', dul(['AOD, α, ω<sub>0</sub>, type, layer height', 'Measure reflectance, retrieve with a LUT', 'Bright surfaces are hard: 412 nm, multi-angle, TIR', 'Passive and lidar complement each other (A-Train)']))]
    mod = dict(id='m6', slug='06-passive-aerosol', title='M6 · Passive aerosol sensing', en='Passive remote sensing of aerosols',
               question='<ul><li>What properties of aerosols can be measured from passive satellite sensors (mention at least 3 aerosol properties)?</li><li>Explain the principle of passive remote sensing of aerosols, including the quantity directly measured and how aerosol properties are derived.</li><li>What are the advantages and limitations of this passive approach as compared to active methods?</li></ul>',
               calcs=[('angstrom', 'Ångström and AOD vs wavelength')],
               checklist=['≥3 properties: AOD, Ångström exponent / size (fine-mode fraction), ω₀ / absorption, type, layer height, UV aerosol index.', 'Measured: TOA spectral (multi-angle, polarised) reflectance; aerosols brighten dark surfaces.',
                          'Method: cloud mask → surface reflectance → LUT from RT model → best-fit AOD + aerosol model.', 'Passive: global coverage, no vertical info, daytime/cloud-free only. Active: profiles, day+night, narrow coverage.'],
               summary=['Tính chất đo được: độ dày quang học AOD, số mũ Ångström (kích thước hạt), albedo tán xạ đơn ω₀ (hấp thụ), loại aerosol, độ cao lớp aerosol, chỉ số aerosol UV.', 'Đại lượng đo: hệ số phản xạ phổ (đa góc, phân cực) ở đỉnh khí quyển; aerosol làm bề mặt tối sáng lên.',
                        'Truy hồi: loại mây → ước lượng phản xạ bề mặt → bảng tra (LUT) từ mô hình truyền bức xạ → chọn AOD + mô hình aerosol phù hợp nhất.', 'Thụ động: phủ toàn cầu, nhưng thiếu thông tin thẳng đứng, chỉ ban ngày & trời quang. Chủ động (lidar): có profil, ngày-đêm, nhưng vùng phủ rất hẹp.'],
               sections=[
        ('What can we measure about aerosols?', '<p>Aerosols are suspended particles (dust, smoke, sea salt, sulfate). From space we can measure:</p>' + hx_table(['Property', 'Meaning', 'How measured'], [
            ['AOD τ<sub>a</sub> (e.g. at 550 nm)', 'Aerosol amount in the column; τ<sub>a</sub> = ∫ k<sub>ext,aer</sub>(z) dz; proxy for PM2.5', 'Reflectance — the most robust product'],
            ['Ångström exponent α', 'Particle size: α ≈ 0–0.5 coarse (dust, sea salt); α ≈ 1.5–2.5 fine (smoke, urban); fine-mode fraction', 'Spectral dependence τ ∝ λ<sup>−α</sup>'],
            ['Single-scattering albedo ω<sub>0</sub>', 'Absorption', 'UV (OMI UV Aerosol Index) or multi-angle/polarimetry'],
            ['Type, refractive index, non-sphericity', 'Dust, smoke, sulfate, sea salt', 'Multi-angle and polarimetric sensors: MISR, POLDER/PARASOL, 3MI'],
            ['Layer height (ALH)', 'Transport, radiative effects', 'O₂ A-band (TROPOMI), MISR (stereo), TIR for dust — see module 8'],
            ['UV Absorbing Aerosol Index (UVAI)', 'Qualitative detection of absorbing aerosol', 'UV; useful above clouds']], 'left') +
         lfig('f9_angstrom', 'Figure 17 (study guide): spectral dependence of optical depth — the Ångström exponent separates fine from coarse particles.') +
         f'<div class="ex"><div class="exh">Example · computing α (numbers checked in Python)</div><ol class="steps"><li>AOD(440) = 0.60; AOD(870) = 0.15</li><li>α = ln(0.60/0.15) / ln(870/440) = <b>{al:.3f}</b> → fine particles</li><li>AOD(550) = 0.60 × (550/440)<sup>−{al:.3f}</sup> = <b>{AN["tau550"]:.3f}</b></li></ol></div>'),
        ('Principle of the retrieval', '<p><b>Measured quantity:</b> top-of-atmosphere spectral reflectance ρ(λ, θ₀, θ, φ) = πI/(μ₀E₀) — possibly multi-angle and polarised. Aerosols scatter sunlight back to space, so they brighten a dark surface.</p>' +
         eq('Simple model', 'ρ<sub>TOA</sub>(λ) = ρ<sub>Rayleigh</sub> + ρ<sub>aer</sub> + T(λ) · ρ<sub>surf</sub> / (1 − S ρ<sub>surf</sub>) &nbsp;;&nbsp; ρ<sub>aer</sub> ≈ ω<sub>0</sub> τ<sub>a</sub> P(Θ) / (4 μ<sub>0</sub> μ)') +
         '<ol class="steps"><li><b>Cloud screening</b> and pixel selection (cloud-free, no sun glint, no snow).</li><li><b>Estimate the surface contribution</b>: dark ocean (≈ 0 in red/NIR); vegetation uses relations with the 2.1 µm band; bright deserts use “deep blue” 412 nm where the surface is dark.</li>'
         '<li><b>Look-up table (LUT)</b>: a radiative transfer model computes TOA reflectance for a set of aerosol models (size distribution, refractive index → ω₀, P(Θ)), AOD values and all geometries.</li><li><b>Inversion</b>: find the model + AOD that best match the measured multi-spectral (multi-angle) reflectance (least squares / OE) → AOD(λ), α, fine-mode fraction, (ω₀, type).</li></ol>' +
         lfig('f16_surface', 'Figure 18 (study guide): TOA reflectance vs AOD — sensitive over dark ocean, almost insensitive over bright desert.')),
        ('Passive versus active', hx_table(['', 'Passive (MODIS, VIIRS, MISR, POLDER, TROPOMI, IASI)', 'Active (CALIOP/CALIPSO, ATLID/EarthCARE)'], [
            ['Advantages', '• Wide swath → daily global coverage, km-scale horizontal resolution<br>• Long, mature time series (since 2000)<br>• Low cost, low power, many spectral bands<br>• Column properties (AOD, α, ω₀)', '• Vertical profile (resolution ~30–60 m)<br>• Day and night; over bright surfaces and above clouds<br>• Depolarisation → particle shape (dust vs spherical)<br>• Fewer assumptions on the surface'],
            ['Limitations', '• Little or no vertical information<br>• Daytime only, cloud-free only<br>• Strong dependence on surface reflectance (hard over deserts, snow)<br>• Ill-posed: uncertain type and ω₀; cloud contamination', '• Very narrow footprint (“curtain” ~100 m), revisit ~16 days<br>• The lidar ratio must be assumed → AOD uncertainty<br>• Low S/N in daytime; attenuated by thick layers<br>• Expensive, high power']], 'left') +
         callout('good', 'They complement each other', 'Passive gives the horizontal map and AOD; active gives the vertical structure (A-Train concept: MODIS + CALIOP).'))])
    return mod, sl, B
