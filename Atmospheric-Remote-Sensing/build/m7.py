# -*- coding: utf-8 -*-
"""M7 — Scattering regimes of light by particles (study guide Ch.7)."""
from lib import *
from qcore import Bank
V = VERIFIED
SZ = V['size']; MQ = V['mie_qext_m133']

def build():
    B = Bank('m7', seed=7)
    B.add('How is the size parameter x defined?',
          'x = 2πr / λ (r: particle radius, λ: wavelength)', ['x = λ / (2πr)', 'x = r · λ', 'x = 4π r² / λ'],
          'The scattering regime is set by x and the complex refractive index m = n + ik. Study guide Ch.7.', 1, 'Size parameter', origin='goc', src='Study guide Ch.7 (checklist)')
    B.add('What are the three scattering regimes by size parameter?',
          'Rayleigh (x ≪ 1), Mie (x ≈ 0.1–50), geometric optics (x ≫ 1)', ['Rayleigh (x ≫ 1), Mie (x ≈ 1), geometric optics (x ≪ 1)', 'Raman, Rayleigh, Brillouin', 'Nadir, limb, occultation'],
          'Guide Ch.7: Rayleigh x < ~0.1; Mie x ≈ 0.1–50; geometric optics x > ~50–100.', 1, 'Regimes', origin='goc', src='Study guide Ch.7 (checklist)')
    B.add('Compute the size parameter of an N₂ molecule (r ≈ 0.2 nm) at λ = 0.55 µm and give the regime.',
          f'x ≈ {SZ["N2"]:.3f} → Rayleigh', [f'x ≈ {SZ["sulfate"]:.1f} → Mie', f'x ≈ {SZ["dust"]:.0f} → upper Mie / geometric optics', 'x ≈ 0.5 → Mie'],
          f'x = 2π × 2×10⁻⁴ µm / 0.55 µm = {SZ["N2"]:.5f} ≪ 1 (Python).', 1, 'Size parameter', origin='goc', src='Mock exam Q7(a)(i)')
    B.add('Compute the size parameter of a sulfate particle r = 0.2 µm at λ = 0.55 µm and give the regime.',
          f'x ≈ {SZ["sulfate"]:.1f} → Mie', [f'x ≈ {SZ["N2"]:.3f} → Rayleigh', f'x ≈ {SZ["dust"]:.0f} → geometric optics', 'x ≈ 0.023 → Rayleigh'],
          f'x = 2π × 0.2 / 0.55 = {SZ["sulfate"]:.4f}. Of order 1–2, so this is the Mie (resonance) regime.', 1, 'Size parameter', origin='goc', src='Mock exam Q7(a)(ii)')
    B.add('Compute the size parameter of a dust particle r = 5 µm at λ = 0.55 µm and give the regime.',
          f'x ≈ {SZ["dust"]:.0f} → upper Mie, approaching geometric optics', [f'x ≈ {SZ["N2"]:.3f} → Rayleigh', f'x ≈ {SZ["sulfate"]:.1f} → lower Mie', 'x ≈ 570 → pure geometric optics'],
          f'x = 2π × 5 / 0.55 = {SZ["dust"]:.2f}. Mie theory still applies (for spheres) but geometric optics is a good approximation for the largest ones. Non-spherical dust needs T-matrix.', 2, 'Size parameter', origin='goc', src='Mock exam Q7(a)(iii)')
    B.add('What is the scattering regime of coarse aerosols (dust, sea salt, r ≈ 1–10 µm) for visible light?',
          f'Upper Mie (x ≈ {SZ["coarse_1"]:.0f}–{SZ["coarse_10"]:.0f}), near geometric optics; Ångström α ≈ 0–0.5', ['Rayleigh, because the particles are smaller than the wavelength', 'Raman, because the particles change the wavelength', 'Pure geometric optics, with no need for Mie'],
          f'x = 2π × (1 to 10) / 0.55 = {SZ["coarse_1"]:.1f} to {SZ["coarse_10"]:.1f}. Guide 7.4.', 2, 'Coarse aerosol', origin='goc', src='Study guide 7.4 (the chapter’s own question)')
    B.add('What are the size and wavelength dependences of Rayleigh scattering?',
          'σ_s ∝ r⁶ / λ⁴', ['σ_s ∝ r² / λ²', 'σ_s ∝ r / λ', 'σ_s ∝ r⁴ λ⁶'],
          'σ_s = (8π/3) k⁴ r⁶ |(m²−1)/(m²+2)|². Doubling the radius gives 2⁶ = 64 times more; halving the wavelength gives 2⁴ = 16 times more.', 2, 'Rayleigh', src='Study guide 7.1')
    B.add('If the radius of a Rayleigh particle doubles (λ fixed), by how much does the scattering cross-section increase?',
          '64 times (2⁶)', ['4 times (2²)', '16 times (2⁴)', '8 times (2³)'],
          'σ_s ∝ r⁶, so (2r)⁶ / r⁶ = 64.', 2, 'Rayleigh', src='Study guide 7.1 (computed)')
    B.add('Why is the sky blue but clouds white?',
          'Molecules (x ≪ 1) scatter ∝ λ⁻⁴ so blue is scattered more; cloud droplets (x ≫ 1) have Q_ext ≈ 2 independent of λ, so all colours are scattered equally → white', ['The sky reflects the colour of the ocean; clouds reflect ice', 'Molecules absorb red light and cloud droplets absorb blue light', 'Clouds emit white thermal radiation and the sky emits blue'],
          'Answer key Q7(b).', 1, 'Rayleigh and Mie', origin='goc', src='Mock exam Q7(b)')
    B.add('What is the Rayleigh phase function?',
          'P(Θ) = ¾(1 + cos²Θ): symmetric forward/backward, light scattered at 90° fully polarised', ['P(Θ) = 1/(4π): isotropic', 'A sharp, strong forward peak with weak backward lobes', 'P(Θ) = cos³Θ with a forward lobe only'],
          'Guide 7.1. Large particles have a strong forward peak.', 1, 'Rayleigh', origin='goc', src='Mock exam Q7(c)')
    B.add('How does the phase function of a large particle (Mie or geometric) differ from Rayleigh?',
          'It has a very strong forward peak and weak side and back lobes (g ≈ 0.6–0.8 for aerosols)', ['It is symmetric forward/backward like Rayleigh', 'It is isotropic at all angles', 'It has only backscatter'],
          'Answer key Q7(c).', 2, 'Mie', origin='goc', src='Mock exam Q7(c)')
    B.add('To what value does the extinction efficiency Q_ext = σ_ext / (πr²) tend for very large x?',
          'To 2 (the "extinction paradox")', ['To 0', 'To 1', 'To infinity'],
          f'Half is diffraction, half is reflection/refraction; independent of wavelength. Mie calculation for a water droplet m = 1.33: Q_ext(x=200) = {MQ["200"]:.2f}, Q_ext(x=50) = {MQ["50"]:.2f}.', 2, 'Mie', src='Study guide 7.2–7.3; Q_ext computed in Python')
    B.add(f'For a water droplet (m = 1.33), what peak value does the Mie Q_ext reach near x ≈ 5?',
          f'≈ {MQ["5"]:.1f} (above 2, then it oscillates and converges to 2)', ['≈ 0.01 (very small)', '≈ 2.0 exactly with no oscillation', '≈ 10'],
          f'Python (Bohren–Huffman): Q_ext(0.5) = {MQ["0.5"]:.4f}; (1) = {MQ["1"]:.3f}; (2) = {MQ["2"]:.3f}; (5) = {MQ["5"]:.3f}; (10) = {MQ["10"]:.3f}; (50) = {MQ["50"]:.3f}. It oscillates and approaches 2.', 3, 'Mie', src='Number computed in Python (own Lorenz–Mie code)')
    B.add('In the Rayleigh regime, how does Q_ext grow with x?',
          f'As x⁴ (e.g. from x = 0.1 to 0.5 Q_ext grows ~600 times)', ['Linearly with x', 'It decreases as x⁻¹', 'It does not change with x'],
          f'Guide Figure 20: x⁴ in the Rayleigh regime. Mie calculation: Q_ext(0.1) = {MQ["0.1"]:.2e}; Q_ext(0.5) = {MQ["0.5"]:.2e}; ratio ≈ {MQ["0.5"]/MQ["0.1"]:.0f} (5⁴ = 625).', 3, 'Rayleigh', src='Study guide Figure 20; numbers computed in Python')
    B.add('To which regime do the rainbow at 42° and the halo at 22° belong?',
          'Geometric optics (very large particles: raindrops; hexagonal ice crystals)', ['Rayleigh', 'Raman', 'Lower Mie'],
          'Guide 7.3: raindrops → rainbow 42°; hexagonal ice crystals → halo 22°; very strong forward diffraction peak.', 2, 'Geometric optics', src='Study guide 7.3')
    B.add('For non-spherical particles such as dust, which method replaces Lorenz–Mie?',
          'The T-matrix or discrete-dipole methods', ['Rayleigh–Jeans theory', 'The Beer–Lambert law', 'The Planck function'],
          'Guide 7.2/7.4: Mie is for homogeneous spheres; dust and ice need spheroids/T-matrix.', 3, 'Mie', src='Study guide 7.2, 7.4')
    B.essay('(a) Compute the size parameter x of (i) an N₂ molecule (r ≈ 0.2 nm), (ii) a sulfate particle r = 0.2 µm, (iii) a dust particle r = 5 µm, all at λ = 0.55 µm; give the regime of each.\n(b) Why is the sky blue but clouds white?\n(c) Sketch the phase function in the Rayleigh regime and for a large particle.',
            f'(a) x = 2πr/λ: (i) {SZ["N2"]:.4f} → Rayleigh; (ii) {SZ["sulfate"]:.2f} → Mie; (iii) {SZ["dust"]:.1f} → upper Mie / geometric optics limit.\n(b) Molecules: σ ∝ λ⁻⁴, so blue is scattered more. Cloud droplets x ≫ 1: Q_ext ≈ 2 independent of λ → all colours equal → white.\n'
            '(c) Rayleigh: ¾(1 + cos²Θ), symmetric forward/back. Large particle: a strong forward peak with weak side/back lobes.', 3, 'Mock exam', origin='goc', src='Mock exam Q7 (2.5 points) + suggested answer')
    B.essay('What is the scattering regime of coarse aerosols in visible light? What follows for AOD and the phase function?',
            f'r ≈ 1–10 µm and λ = 0.55 µm give x ≈ {SZ["coarse_1"]:.0f}–{SZ["coarse_10"]:.0f}: the upper part of the Mie regime, approaching geometric optics. Consequences: AOD is almost wavelength independent (α ≈ 0–0.5), strong forward scattering, Q_ext ≈ 2. Non-spherical dust: Mie is only an approximation; use spheroids/T-matrix.', 2, 'Coarse aerosol', origin='goc', src='Study guide 7.4')
    sl = [
        cover('Scattering regimes of light by particles', 'Study guide chapter 7',
              '<b>Atmospheric Remote Sensing</b> · USTH<br>Rayleigh · Mie · geometric optics · coarse aerosols'),
        S('Size parameter x = 2πr / λ', fm('x = 2π r / λ &nbsp;&nbsp; (r: particle radius) &nbsp;&nbsp; + &nbsp; complex refractive index m = n + ik', 32) +
          figfit('f5_regimes', 'Figure 19 (study guide): scattering regimes as a function of x (visible light, λ ≈ 0.5 µm).', 330)),
        S('Three scattering regimes', dtable(tbl(['Regime', 'x', 'Particles', 'Features'], [
            ['Rayleigh', '≪ 1 (< 0.1)', 'Molecules, very fine particles', 'σ ∝ r<sup>6</sup>/λ<sup>4</sup>; symmetric'],
            ['Mie', '≈ 0.1–50', 'Aerosols, cloud droplets', 'Weak λ dependence; forward peak'],
            ['Geometric optics', '≫ 1 (> 50–100)', 'Raindrops, ice crystals', 'Q<sub>ext</sub> → 2; independent of λ']]), 'xl') + '<p class="note" style="margin-top:26px">The regime is set by <b>x = 2πr/λ</b> and the complex refractive index <b>m = n + ik</b>.</p>'),
        S('Rayleigh: molecules and very fine particles', fm('σ<sub>s</sub> = (8π/3) k<sup>4</sup> r<sup>6</sup> |(m² − 1)/(m² + 2)|² ∝ r<sup>6</sup> / λ<sup>4</sup>', 28) + fm('P(Θ) = ¾ (1 + cos²Θ)', 32) +
          ulb(['Double the radius → <b>64 times</b> (2<sup>6</sup>)', 'Halve λ → <b>16 times</b> (2<sup>4</sup>)', 'Blue sky, red sunsets'], 28, 10)),
        S('Mie: particles of wavelength size', cols(ulb(['Maxwell solution for a sphere (Lorenz–Mie)', 'Q<sub>ext</sub> oscillates with x and tends to 2', 'Weak λ dependence (Ångström α ≈ 0–2)', 'Forward peak: g ≈ 0.6–0.8', 'Non-spherical: T-matrix'], 27, 14),
          dtable(tbl(['x', 'Q<sub>ext</sub> (m = 1.33)'], [['0.1', f'{MQ["0.1"]:.1e}'], ['1', f'{MQ["1"]:.3f}'], ['5', f'{MQ["5"]:.2f}'], ['10', f'{MQ["10"]:.2f}'], ['50', f'{MQ["50"]:.2f}'], ['200', f'{MQ["200"]:.2f}']]), 'mid'), flex=[1.1, 1])),
        S('Extinction efficiency vs x', figfit('f10_mie_qext', 'Figure 20 (study guide): Q_ext vs x (Lorenz–Mie): x⁴ (Rayleigh), resonances (Mie), limit 2 (geometric).', 470) + '<p class="note">The previous table was computed independently in Python with Lorenz–Mie and matches the figure.</p>'),
        S('Geometric optics: very large particles', cards(card('Raindrops', 'Rainbow at 42°.'), card('Hexagonal ice crystals', 'Halo at 22°.'), card('Q<sub>ext</sub> → 2', 'Half diffraction, half reflection/refraction; white because it does not depend on λ.'), cols=3)),
        S('Coarse aerosol in visible light', fm(f'λ = 0.55 µm: &nbsp; r = 1 µm → x ≈ {SZ["coarse_1"]:.0f} &nbsp;;&nbsp; r = 10 µm → x ≈ {SZ["coarse_10"]:.0f}', 30) +
          ulb(['Upper Mie regime, approaching geometric optics', 'AOD almost independent of λ: α ≈ 0–0.5', 'Strong forward scattering; Q<sub>ext</sub> ≈ 2', 'Dust is non-spherical: spheroids, T-matrix'], 29, 16)),
        S('Three particles from the mock exam', dtable(tbl(['Particle', 'r', 'x at 0.55 µm', 'Regime'], [
            ['N₂ molecule', '0.2 nm', f'{SZ["N2"]:.4f}', 'Rayleigh'], ['Sulfate', '0.2 µm', f'{SZ["sulfate"]:.2f}', 'Mie'], ['Dust', '5 µm', f'{SZ["dust"]:.1f}', 'Upper Mie / geometric']]), 'xl') + '<p class="note" style="margin-top:30px">x = 2πr/λ with λ = 0.55 µm. Even the finest coarse aerosol (1 µm) already has x ≈ 11.</p>'),
        S('Exam checklist — Chapter 7', chk(['Size parameter x = 2πr/λ (and refractive index m)', 'Rayleigh x ≪ 1: λ<sup>−4</sup>, symmetric phase function', 'Mie x ~ 1: forward peak, Q<sub>ext</sub> oscillates → 2', 'Geometric optics x ≫ 1: independent of λ', 'Coarse aerosol in visible: x ~ 10–100, α ≈ 0'])),
        S('Key points', dul(['The regime is set by x = 2πr/λ', 'Rayleigh: λ<sup>−4</sup> → blue sky', 'Mie: fine aerosols, forward peak', 'Coarse aerosol: x ≈ 10–100, α ≈ 0']))]
    mod = dict(id='m7', slug='07-scattering-regimes', title='M7 · Scattering regimes', en='Scattering regimes of light by particles',
               question='<ul><li>What are the different regimes of scattering of light by particles?</li><li>Explain each of them and under which conditions they are encountered.</li><li>What is the regime for coarse aerosols scattering visible light?</li></ul>',
               calcs=[('size', 'Size parameter and scattering regime')],
               checklist=['Size parameter x = 2πr/λ (+ refractive index m).', 'Rayleigh x ≪ 1 (molecules), λ⁻⁴, symmetric P(Θ).', 'Mie x ~ 1 (fine aerosols), Lorenz–Mie theory, forward peak, Q_ext oscillates → 2.', 'Geometric optics x ≫ 1 (raindrops, ice), wavelength-independent.', 'Coarse aerosol in visible: x ~ 10–100 → Mie (large-particle limit, near geometric optics), α ≈ 0.'],
               summary=['Chế độ tán xạ phụ thuộc thông số kích thước x = 2πr/λ.', 'Rayleigh (x ≪ 1): phân tử khí, ∝ λ⁻⁴, trời xanh. Mie (x ≈ 1): aerosol mịn, tán xạ mạnh về phía trước. Quang hình (x ≫ 1): giọt mưa, tinh thể băng, không phụ thuộc bước sóng.', 'Aerosol thô (bụi, muối biển, r ≈ 1–10 µm) với ánh sáng khả kiến: x ≈ 10–100 → chế độ Mie (phần trên, tiến gần quang hình), số mũ Ångström ≈ 0.'],
               sections=[
        ('Big or small compared with the wavelength?', '<p>How light scatters depends on the <b>particle size compared with the wavelength</b>. Air molecules are far smaller than the wavelength; aerosol particles are comparable to it; raindrops are thousands of times larger. Two numbers decide the regime: the size parameter and the complex refractive index m = n + ik.</p>' +
         eq('Size parameter', 'x = 2π r / λ') + lfig('f5_regimes', 'Figure 19 (study guide): scattering regimes vs x for visible light (λ ≈ 0.5 µm).') +
         hx_table(['Regime', 'Condition', 'Encountered for', 'Features'], [['Rayleigh', 'x ≪ 1 (typically < 0.1)', 'Air molecules N₂, O₂ (UV–IR); very fine aerosol r < 0.03 µm in the visible; cloud droplets for microwave/radar', 'σ ∝ r⁶/λ⁴; P(Θ) = ¾(1 + cos²Θ)'],
                                                              ['Mie (resonance)', 'x ≈ 0.1–50', 'Accumulation-mode aerosol (0.1–1 µm) in the visible; cloud droplets in the IR; also coarse aerosol', 'Lorenz–Mie; Q_ext oscillates then → 2; α ≈ 0–2; forward peak (g ≈ 0.6–0.8)'],
                                                              ['Geometric optics', 'x ≫ 1 (typically > 50–100)', 'Raindrops, large cloud droplets, ice crystals, large dust in the visible', 'Rays: reflection, refraction, diffraction; Q_ext → 2; independent of λ']], 'left')),
        ('Rayleigh: molecules and very fine particles', '<p>A particle much smaller than the wavelength behaves as an <b>oscillating dipole</b> in a uniform field.</p>' + eq('Cross-section and phase function', 'σ<sub>s</sub> = (8π/3) k⁴ r⁶ |(m² − 1)/(m² + 2)|² ∝ r⁶ / λ⁴ &nbsp;;&nbsp; P(Θ) = ¾ (1 + cos²Θ)') +
         '<ul><li>Strong λ⁻⁴ dependence → blue sky, red sunsets.</li><li>Forward and backward scattering are symmetric; light scattered at 90° is fully polarised.</li></ul>' +
         '<div class="ex"><div class="exh">Example · numbers</div><ul><li>Double the radius (λ fixed): σ increases 2⁶ = <b>64</b> times.</li><li>Halve the wavelength: σ increases 2⁴ = <b>16</b> times.</li><li>450 nm compared with 650 nm: (650/450)⁴ = <b>4.35</b> times.</li></ul></div>'),
        ('Mie and geometric optics', '<p><b>Mie</b> (x ≈ 0.1–50) is the exact solution of Maxwell’s equations for a homogeneous sphere, as an infinite series of multipoles. The extinction efficiency Q<sub>ext</sub> = σ<sub>ext</sub>/(πr²) oscillates with x and tends to 2 for large x (“extinction paradox”). The weak wavelength dependence makes haze and clouds white/grey; the forward peak is strong (g ≈ 0.6–0.8) and the angular structure complex (glory, rainbow). Non-spherical particles (dust, ice) need T-matrix or discrete-dipole methods.</p>'
         f'<div class="ex"><div class="exh">Q<sub>ext</sub> computed in Python (Lorenz–Mie, water droplet m = 1.33)</div>' + hx_table(['x', '0.1', '0.5', '1', '2', '5', '10', '50', '200'], [['Q<sub>ext</sub>'] + [f'{MQ[k]:.3g}' for k in ['0.1', '0.5', '1', '2', '5', '10', '50', '200']]]) +
         '<p style="margin:4px 0">Check: at x = 0.05 the result matches the Rayleigh formula within 2%; at x = 200 the value ≈ 2.06 (≈ 2).</p></div>' + lfig('f10_mie_qext', 'Figure 20 (study guide): Q_ext vs x — x⁴ (Rayleigh), resonances (Mie), limit Q_ext → 2 (geometric optics).') +
         '<p><b>Geometric optics</b> (x ≫ 1): light is treated as rays (Snell, Fresnel) plus diffraction. Q<sub>ext</sub> → 2 (half diffraction, half reflection/refraction), independent of wavelength, so clouds are white; phenomena: rainbow 42°, halo 22° around hexagonal ice crystals; very strong forward diffraction peak.</p>'),
        ('Coarse aerosol in visible light', '<p>Mineral dust and sea salt have r ≈ 1–10 µm; at λ ≈ 0.55 µm:</p>' + eq('Size parameter', f'x = 2π × (1 to 10 µm) / 0.55 µm ≈ <b>{SZ["coarse_1"]:.0f} to {SZ["coarse_10"]:.0f}</b>') +
         '<p>→ the <b>upper part of the Mie regime</b>, approaching geometric optics (Mie still applies; geometric optics is a good approximation for the largest particles). Consequences: AOD nearly independent of wavelength (<b>α ≈ 0–0.5</b>), strong forward scattering, Q<sub>ext</sub> ≈ 2. Dust is non-spherical, so Mie for spheres is only an approximation.</p>' +
         f'<div class="ex"><div class="exh">Example · mock exam Q7(a), numbers checked in Python</div>' + hx_table(['Particle', 'r', 'x at 0.55 µm', 'Regime'], [['N₂ molecule', '0.2 nm', f'{SZ["N2"]:.4f}', 'Rayleigh'], ['Sulfate', '0.2 µm', f'{SZ["sulfate"]:.2f}', 'Mie'], ['Dust', '5 µm', f'{SZ["dust"]:.1f}', 'Upper Mie / near geometric']]) + '</div>' +
         callout('info', 'Blue sky, white clouds', 'Molecules (Rayleigh, ∝ λ⁻⁴) scatter blue more than red. Cloud droplets (x ≫ 1) scatter all colours equally (Q<sub>ext</sub> ≈ 2), so clouds are white.'))])
    return mod, sl, B
