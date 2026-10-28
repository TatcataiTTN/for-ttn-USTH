# -*- coding: utf-8 -*-
"""M2 — Interaction between light and matter (study guide Ch.2)."""
from lib import *
from lib import _PIL
from m1 import ul_
from qcore import Bank
V = VERIFIED

def build():
    B = Bank('m2', seed=2)
    be = V['beer']; w = V['wien']; st = V['stefan']
    B.add('Write the Beer–Lambert law for a beam crossing an absorbing and scattering medium.',
          'I = I₀ · e^(−τ), with τ = ∫ (k_a + k_s) ds the optical depth along the path',
          ['I = I₀ · (1 − τ), with τ the total number of molecules on the path', 'I = I₀ / τ², with τ the wavelength divided by the particle size', 'I = I₀ + τ · B(T), with B the Planck function'],
          'dI = −k_e·I·ds with k_e = k_a + k_s = Σ σᵢ nᵢ, so I = I₀ exp(−τ). The transmittance is T = I/I₀ = e^(−τ).',
          1, 'Beer–Lambert', origin='goc', src='Mock exam Q2(a)')
    B.add('What is the transmittance T of a layer of optical depth τ?',
          'T = e^(−τ)', ['T = 1 / τ', 'T = 1 − τ²', 'T = τ · e'],
          'T = I/I₀ = exp(−τ). For τ = 1, T = 0.37; for τ = 3, T = 0.05.', 1, 'Beer–Lambert', origin='goc', src='Mock exam Q2(a)')
    B.add('What does Kirchhoff’s law (local thermodynamic equilibrium, LTE) state?',
          'At each wavelength emissivity equals absorptivity: ε_λ = α_λ',
          ['The sum of absorption and scattering is zero at every wavelength', 'Emissivity is inversely proportional to the temperature of the body', 'The emitted intensity equals the solar intensity at the top of the atmosphere'],
          'A gas that absorbs at a wavelength also emits B_λ(T) there. Thermal-IR spectra therefore carry information on both concentration and temperature.',
          1, 'Emission', origin='goc', src='Mock exam Q2(b)')
    B.add('Why does Kirchhoff’s law matter for thermal-infrared remote sensing?',
          'Because a gas absorbing in a line also emits in it, so the spectrum encodes both the gas amount and the temperature of the emitting layer',
          ['Because it proves the atmosphere does not emit in the infrared, so only reflection is measured', 'Because it lets scattering be neglected in all cases', 'Because it says the surface temperature always equals the stratospheric temperature'],
          'Answer key Q2(b): ε_λ = α_λ, so information on T(z) and n(z) both sit in the TIR spectrum.', 2, 'Emission', origin='goc', src='Mock exam Q2(b)')
    B.add('A beam crosses a layer of vertical optical depth τ = 0.5 at a solar zenith angle of 60°. What fraction of the direct beam is transmitted?',
          f'≈ {be["T"]*100:.0f}% (slant τ = 1.0)', ['≈ 61% (used τ = 0.5 without the angle correction)', '≈ 22% (multiplied instead of dividing by cos 60°)', '≈ 50% (slant τ taken as one half)'],
          f'τ_slant = τ_vertical / cos θ = 0.5 / 0.5 = 1.0, so T = e^(−1) = {be["T"]:.4f}. Recomputed in Python.', 1, 'Beer–Lambert', origin='goc', src='Mock exam Q2(c)')
    B.add('Which three mechanisms change the intensity of radiation reaching the sensor?',
          'Absorption, scattering and emission (plus surface reflection)', ['Diffraction, interference and polarisation', 'Photolysis, deposition and transport', 'Nadir, limb and occultation'],
          'Guide Ch.2: absorption + scattering = extinction; emission and scattering into the beam add radiation.', 1, 'Three mechanisms', origin='goc', src='Study guide Ch.2 (checklist)')
    B.add('Electronic transitions cause absorption in which spectral region, and for which gases?',
          'UV–visible; e.g. O₃ (Hartley–Huggins 250–350 nm), NO₂ (400–450 nm), SO₂ (300–320 nm)',
          ['Infrared; e.g. CO₂ at 15 µm and O₃ at 9.6 µm', 'Microwave; e.g. O₂ at 60 GHz and ClO', 'X-rays; e.g. N₂ and Ar'],
          'Electronic → UV/visible. Vibrational–rotational → infrared (CO₂ 15 and 4.3 µm; O₃ 9.6 µm; CH₄ 7.7 and 2.3 µm; CO 4.6 and 2.3 µm). Pure rotational → microwave/far-IR.',
          1, 'Absorption', src='Study guide 2.1')
    B.add('Which broadening mechanism dominates the line shape in the lower atmosphere?',
          'Lorentz (pressure) broadening', ['Doppler (temperature) broadening', 'Zeeman broadening by the magnetic field', 'Stark broadening by electric fields'],
          'Guide 2.1: Lorentz (pressure) dominates in the low atmosphere; Doppler (temperature) dominates at high altitude.', 2, 'Absorption', src='Study guide 2.1')
    B.add('What are the wavelength dependence and phase function of Rayleigh scattering?',
          'σ_R ∝ λ⁻⁴ and P(Θ) = ¾(1 + cos²Θ), symmetric forward/backward', ['σ_R ∝ λ⁻¹ and a sharp forward peak', 'σ_R independent of λ and an isotropic phase function', 'σ_R ∝ λ⁴ and a backward-only peak'],
          'Guide 2.2: molecules (x ≪ 1) scatter ∝ λ⁻⁴, hence the blue sky and red sunsets; forward and backward scattering are symmetric.', 1, 'Scattering', src='Study guide 2.2')
    B.add('How many times stronger is Rayleigh scattering at 450 nm than at 650 nm?',
          f'≈ {V["rayleigh_450_650"]:.1f} times ((650/450)⁴)', ['≈ 1.4 times ((650/450)¹)', '≈ 2.1 times ((650/450)²)', '≈ 0.23 times (scattering is weaker at 450 nm)'],
          f'σ ∝ λ⁻⁴, so the ratio is (650/450)⁴ = {V["rayleigh_450_650"]:.3f}. This is why blue light is scattered more than red.', 2, 'Scattering', src='Study guide 2.2 (number computed in Python)')
    B.add('Rotational Raman scattering by N₂ and O₂ causes which effect that matters for UV–vis DOAS retrievals?',
          'The Ring effect: filling-in of the Fraunhofer lines', ['The greenhouse effect: heat trapped in the troposphere', 'The Doppler effect: wavelength shift of lines', 'The Faraday effect: rotation of the polarisation plane'],
          'Raman scattering is inelastic (changes wavelength), so it fills in the solar Fraunhofer lines. Guide 2.2.', 3, 'Scattering', src='Study guide 2.2')
    B.add('How is the single-scattering albedo ω₀ defined, and what does ω₀ = 1 mean?',
          'ω₀ = σ_s / (σ_s + σ_a); ω₀ = 1 means the particles only scatter and do not absorb', ['ω₀ = σ_a / (σ_s + σ_a); ω₀ = 1 means the particles only absorb', 'ω₀ = σ_s · σ_a; ω₀ = 1 means the particle size equals the wavelength', 'ω₀ = τ_a / τ_s; ω₀ = 1 means there is no aerosol'],
          'Guide 2.2: ω₀ ≈ 1 for non-absorbing particles; about 0.85 for smoke, i.e. about 15% of the extinction is absorption.', 2, 'Scattering', src='Study guide 2.2')
    B.add('Wien’s displacement law gives roughly which wavelength of maximum emission for the Sun (≈ 5778 K)?',
          f'≈ {w["sun"]["lam_max_um"]:.2f} µm (visible)', ['≈ 10 µm (thermal infrared)', '≈ 0.05 µm (far ultraviolet)', '≈ 5 µm (mid-infrared)'],
          f'λ_max = 2898 µm·K / T = 2898/5778 = {w["sun"]["lam_max_um"]:.3f} µm. Python also finds the numerical maximum of the Planck function at {w["sun"]["lam_max_numeric_um"]:.3f} µm.', 1, 'Emission', src='Study guide 2.3')
    B.add('For the Earth at about 288 K, where is the emission maximum?',
          f'≈ {w["earth"]["lam_max_um"]:.1f} µm (thermal infrared)', ['≈ 0.5 µm (green)', '≈ 1.0 µm (near-infrared)', '≈ 100 µm (microwave)'],
          f'2898/288 = {w["earth"]["lam_max_um"]:.2f} µm. This is why the 8–12 µm atmospheric window is so important for thermal remote sensing.', 1, 'Emission', src='Study guide 2.3')
    B.add('In which spectral regions does thermal emission dominate, and where does solar reflection dominate?',
          'Thermal emission for λ > about 4 µm; solar reflection in the UV–visible–near-IR', ['Thermal emission in the UV; solar reflection in the far infrared', 'Both are equal at all wavelengths', 'Thermal emission only by day; reflection only by night'],
          'Guide 2.3, Figure 6: the Planck curves of the Sun and of the Earth cross near 4 µm.', 2, 'Emission', src='Study guide 2.3, Figure 6')
    B.add('By the Stefan–Boltzmann law M = σT⁴, what is the emitted power of a black body at 288 K?',
          f'≈ {st["M_earth"]:.0f} W m⁻²', ['≈ 240 W m⁻²', '≈ 1 361 W m⁻²', '≈ 5.67 W m⁻²'],
          f'M = 5.67×10⁻⁸ × 288⁴ = {st["M_earth"]:.1f} W m⁻². Computed in Python.', 2, 'Emission', src='Study guide 2.3 (formula); number computed in Python')
    B.add('In the radiative transfer equation, what does the term k_a·B_λ(T) describe?',
          'Thermal emission by the medium, added to the beam', ['Loss of energy by scattering out of the beam', 'Scattering from all other directions into the line of sight', 'Reflection from a Lambertian surface'],
          'RTE: dI/ds = −k_e I + k_a B + (k_s/4π)∫P I dΩ′. Term 1 = extinction; term 2 = emission; term 3 = scattering into the line of sight.', 2, 'RTE', src='Study guide 2.5')
    B.add('To which case does the Schwarzschild equation apply?',
          'Thermal IR without scattering: TOA radiance is the attenuated surface emission plus the emission of each layer weighted by its transmission to space',
          ['UV with strong multiple scattering', 'Active laser remote sensing (lidar)', 'Solar occultation through the limb'],
          'I(TOA) = ε_s B(T_s) T(0,∞) + ∫ B(T(z)) ∂T(z,∞)/∂z dz. Guide 2.5.', 3, 'RTE', src='Study guide 2.5')
    B.add('For a Lambertian surface, how is the reflected radiance computed?',
          'I = A·F₀·cos θ₀ / π', ['I = A·F₀·cos θ₀ · π', 'I = F₀ / (A·cos θ₀)', 'I = A · B(T)'],
          'A is the surface albedo, F₀ the solar flux and θ₀ the solar zenith angle. Lambertian means isotropic reflection.', 3, 'RTE', src='Study guide 2.5')
    B.essay('(a) Write the Beer–Lambert law and define optical depth and transmittance.\n(b) Explain Kirchhoff’s law and why it matters for thermal-infrared remote sensing.\n(c) A beam crosses a layer with τ = 0.5 at a solar zenith angle of 60°. What percentage of the direct beam is transmitted?',
            '(a) dI = −k_e I ds, I = I₀ e^(−τ), τ = ∫(k_a + k_s) ds = ∫Σσᵢnᵢ ds; T = I/I₀ = e^(−τ).\n(b) In LTE, ε_λ = α_λ: a gas absorbing at λ also emits B_λ(T) there → TIR spectra carry information on both concentration and temperature.\n'
            f'(c) Slant τ = 0.5 / cos 60° = 1.0 → T = e^(−1) = {be["T"]:.3f} ≈ 37%.', 3, 'Mock exam', origin='goc', src='Mock exam Q2 (2.5 points) + suggested answer')
    B.essay('Describe the three mechanisms of light–matter interaction and the main equations of each.',
            'Absorption: E = hν = E₂ − E₁; k_a = σ_a(λ)·n; spectral fingerprint (electronic UV-vis, vibrational–rotational IR, pure rotational microwave). Scattering: direction change without wavelength change; phase function P(Θ); Rayleigh (x ≪ 1, ∝ λ⁻⁴), Mie (x ~ 1), Raman (Ring); ω₀ = σ_s/(σ_s + σ_a). '
            'Emission: B_λ(T) = (2hc²/λ⁵)/(exp(hc/λk_BT) − 1); Kirchhoff ε = α; Wien λ_max T = 2898 µm·K; Stefan–Boltzmann M = σT⁴. Together: Beer–Lambert and the RTE.', 2, 'Three mechanisms', origin='goc', src='Study guide Ch.2 (question)')
    B.essay('Write the full radiative transfer equation and identify each term; give two simplified cases used in remote sensing.',
            'dI/ds = −k_e I + k_a B_λ(T) + (k_s/4π)∫P(Θ) I(Ω′) dΩ′: extinction (loss), thermal emission (gain), scattering from other directions into the line of sight (gain). '
            'Simplifications: (1) thermal IR without scattering → Schwarzschild equation; (2) UV–visible solar → DOAS: ln(I₀/I) = Σσᵢ·SCDᵢ + smooth polynomial; Lambertian surface: I = A F₀ cos θ₀/π.', 3, 'RTE', origin='goc', src='Study guide 2.5')
    # -------- slides --------
    sl = [
        cover('Interaction between light and matter', 'Study guide chapter 2',
              '<b>Atmospheric Remote Sensing</b> · USTH<br>Absorption · scattering · emission · Beer–Lambert · radiative transfer equation'),
        S('Three mechanisms change the radiation', cards(
            card('Absorption', 'A photon is absorbed when E = hν = E₂ − E₁.<br>Each gas has a <b>fingerprint</b> σ(λ).'),
            card('Scattering', 'Direction changes, wavelength does not.<br>Rayleigh (molecules), Mie (particles).'),
            card('Emission', 'A body at temperature T emits ε·B<sub>λ</sub>(T).<br>Dominant for λ &gt; ~4 µm.'), cols=3) +
          '<p class="note" style="margin-top:14px"><b>Absorption + scattering = extinction</b>; emission and scattering into the line of sight add radiation.</p>'),
        S('Absorption: three kinds of transition', dtable(tbl(['Transition', 'Spectral region', 'Examples'], [
            ['Electronic', 'UV – visible', 'O₃ Hartley–Huggins 250–350 nm; NO₂ 400–450 nm; SO₂ 300–320 nm'],
            ['Vibrational–rotational', 'Infrared', 'CO₂ 15 and 4.3 µm; O₃ 9.6 µm; CH₄ 7.7 and 2.3 µm; CO 4.6 µm'],
            ['Pure rotational', 'Microwave / far-IR', 'H₂O, O₂ 60 GHz, ClO']]), 'xl') +
          '<p class="note" style="margin-top:20px">k<sub>a</sub>(λ) = σ<sub>a</sub>(λ)·n. Lines are broadened by <b>pressure</b> (Lorentz, low atmosphere) and by <b>temperature</b> (Doppler, high altitude).</p>'),
        S('Scattering: Rayleigh, Mie and Raman', cols(
            ulb(['<b>Rayleigh</b> (molecules, x ≪ 1): σ ∝ λ<sup>−4</sup> → blue sky', '<b>Mie</b> (aerosols, x ~ 1): weak λ dependence, forward peak', '<b>Raman</b>: inelastic → Ring effect'], 34, 50),
            fm('<span class="l">Rayleigh phase function</span>P(Θ) = ¾ (1 + cos²Θ)', 32) + fm('<span class="l">Single-scattering albedo</span>ω<sub>0</sub> = σ<sub>s</sub> / (σ<sub>s</sub> + σ<sub>a</sub>)', 32) +
            '<p class="note" style="font-size:28px">ω₀ = 1: no absorption; ω₀ ≈ 0.85: smoke (about 15% absorption).</p>', flex=[1.15, 1])),
        S('Phase functions from Mie theory', figfit('f11_phase', 'Figure 5 (study guide): phase functions from Mie theory — symmetric for molecules, forward-peaked for large particles.', 440) +
          '<p class="note">The larger the particle, the more the scattering is concentrated forward (asymmetry parameter g ≈ 0.6–0.8 for aerosols).</p>'),
        S('Emission: Planck, Wien, Kirchhoff', figfit('f8_planck', 'Figure 6 (study guide): Planck curves of the Sun (about 5778 K) and the Earth (about 288 K).', 420) +
          fm(f'λ<sub>max</sub>T = 2898 µm·K → Sun ≈ {w["sun"]["lam_max_um"]:.2f} µm; Earth ≈ {w["earth"]["lam_max_um"]:.1f} µm', 28)),
        S('Beer–Lambert: exponential extinction', fm('<span class="l">Extinction law</span>dI<sub>λ</sub> = −k<sub>e</sub> I<sub>λ</sub> ds &nbsp;,&nbsp; k<sub>e</sub> = k<sub>a</sub> + k<sub>s</sub> = Σ σ<sub>i</sub> n<sub>i</sub>', 30) +
          fm('I<sub>λ</sub>(s) = I<sub>λ</sub>(0) · e<sup>−τ</sup> &nbsp;,&nbsp; τ = ∫ k<sub>e</sub> ds &nbsp;,&nbsp; T = e<sup>−τ</sup>', 32) +
          legend([('τ', 'optical depth'), ('T', 'transmittance'), ('τ<sub>slant</sub>', 'τ<sub>vertical</sub> / cos θ'), ('Example', f'τ = 0.5, θ = 60° → τ<sub>slant</sub> = 1 → T = {be["T"]:.2f}')], 2)),
        S('The three mechanisms in one figure', figfit('f2_interactions', 'Figure 4 (study guide): absorption, scattering, emission and the Beer–Lambert exponential.', 420) +
          ulb(['Absorption and scattering remove energy from the beam', 'Emission and scattering from other directions add energy to the beam'], 30, 14)),
        S('The radiative transfer equation (RTE)', fm('dI<sub>λ</sub>/ds = −k<sub>e</sub> I<sub>λ</sub> + k<sub>a</sub> B<sub>λ</sub>(T) + (k<sub>s</sub>/4π) ∫ P(Θ) I<sub>λ</sub>(Ω′) dΩ′', 28) +
          cards2(330, card('Term 1: extinction', 'Energy lost by absorption and by scattering out of the beam'), card('Term 2: emission', 'The medium emits thermal radiation following Planck'),
                card('Term 3: scattering in', 'Light from all other directions scattered into the line of sight'), cols=3)),
        S('Simplified cases in remote sensing', cols(
            fm('<span class="l">Thermal IR (Schwarzschild)</span>I(TOA) = ε<sub>s</sub> B(T<sub>s</sub>) T(0,∞) + ∫ B(T(z)) ∂T(z,∞)/∂z dz', 27) +
            '<p style="font-size:33px">Attenuated surface emission plus the emission of each layer, weighted by its transmission to space.</p>',
            fm('<span class="l">UV – visible solar (DOAS)</span>ln(I<sub>0</sub>/I) = Σ σ<sub>i</sub>′ SCD<sub>i</sub> + polynomial', 27) +
            '<p style="font-size:33px">Lambertian surface: I = A F<sub>0</sub> cos θ<sub>0</sub> / π.</p>') + callout('info', 'Remember', 'DOAS for UV–visible (backscattered sunlight); Schwarzschild for thermal IR without scattering.')),
        S('Exam checklist — Chapter 2', chk([
            'Three mechanisms: absorption (σ(λ)), scattering (Rayleigh/Mie, P(Θ), ω₀), emission (Planck, Kirchhoff)',
            'Beer–Lambert: I = I₀ e<sup>−τ</sup>, τ = ∫ k<sub>e</sub> ds, k<sub>e</sub> = k<sub>a</sub> + k<sub>s</sub>',
            'Write the full RTE and identify each term; Schwarzschild for TIR',
            'Draw: absorbing slab, scattering particle with arrows in all directions, emitting layer, exponential curve'])),
        S('Key points', dul(['Absorption + scattering = extinction (Beer–Lambert I = I₀e<sup>−τ</sup>)', 'Emission follows Planck; Kirchhoff ε = α', 'RTE: extinction − emission + scattering into the line of sight', 'Rayleigh ∝ λ<sup>−4</sup> gives the blue sky']))]
    mod = dict(id='m2', slug='02-light-matter', title='M2 · Light–matter interaction', en='Interaction between light and matter',
               question='<ul><li>Describe the main physical mechanisms of interaction between light and matter that modify the intensity of radiation reaching a radiometric sensor.</li><li>Provide a clear description, the main equations, and schematics of each of these mechanisms.</li></ul>',
               calcs=[('beer', 'Beer–Lambert and zenith angle'), ('planck', 'Planck, Wien and brightness temperature')],
               checklist=['Three mechanisms: absorption (quantised transitions, σ(λ) fingerprint), scattering (Rayleigh/Mie, phase function, ω₀), emission (Planck, Kirchhoff).',
                          'Beer–Lambert: I = I₀ e^−τ, τ = ∫ k_e ds, k_e = k_a + k_s.', 'Write the full RTE and identify each term; Schwarzschild for thermal IR.',
                          'Draw: absorbing slab, scattering particle with arrows in all directions, emitting layer, exponential decay curve.'],
               summary=['Ba cơ chế: hấp thụ (chuyển mức năng lượng điện tử, dao động, quay → mỗi khí có dấu vân tay phổ), tán xạ (đổi hướng photon: Rayleigh ∝ λ⁻⁴, Mie), phát xạ nhiệt (Planck, Kirchhoff ε = α).',
                        'Hấp thụ + tán xạ = suy giảm (extinction), tuân theo định luật Beer–Lambert I = I₀·e^(−τ).', 'Phương trình truyền bức xạ: suy giảm − phát xạ + tán xạ vào hướng nhìn.'],
               sections=[
        ('The three mechanisms, in plain words', '<p>Light travelling from its source (the Sun or the ground) to the sensor is changed in <b>three ways</b>. <b>Absorption</b> is like tinted glass swallowing some light. <b>Scattering</b> is like fog bending rays into other directions. <b>Emission</b> is the warm atmosphere itself glowing in the infrared.</p>'
         '<p>Absorption and scattering both <b>remove</b> energy from the beam (together called <i>extinction</i>); emission and scattering from other directions <b>add</b> energy. Surface reflection also matters for the radiance seen from space.</p>' +
         lfig('f2_interactions', 'Figure 4 (study guide): the three mechanisms and the Beer–Lambert law.') +
         model_en('<p>Radiation travelling from the source (Sun or Earth surface) to the sensor is modified by three processes: absorption and scattering (which together form extinction) remove energy from the beam, while emission and scattering into the beam add energy. Surface reflection also matters for the radiance seen from space.</p>')),
        ('Absorption', '<p>A molecule absorbs a photon when its energy matches a transition: <b>E = hν = E₂ − E₁</b>. Every gas has its own absorption spectrum σ(λ) — the “fingerprint” used to identify it.</p>' +
         hx_table(['Transition type', 'Spectral region', 'Examples'], [['Electronic', 'UV – visible', 'O₃ Hartley–Huggins 250–350 nm; NO₂ 400–450 nm; SO₂ 300–320 nm'],
                                                       ['Vibrational–rotational', 'Infrared', 'CO₂ 15 µm and 4.3 µm; O₃ 9.6 µm; CH₄ 7.7 and 2.3 µm; CO 4.6 and 2.3 µm; H₂O'],
                                                       ['Pure rotational', 'Microwave / far-IR', 'H₂O, O₂ 60 GHz, ClO']], 'left') +
         eq('Absorption coefficient', 'k<sub>a</sub>(λ) = σ<sub>a</sub>(λ) · n &nbsp; (n: number density, molecule cm⁻³)') +
         '<p>The line shape depends on <b>pressure</b> (Lorentz broadening, dominant in the lower atmosphere) and <b>temperature</b> (Doppler broadening, dominant at high altitude).</p>'),
        ('Scattering', '<p>A photon is redirected but <b>keeps its wavelength</b> (elastic). The angular distribution is the phase function P(Θ). The regime depends on the size parameter x = 2πr/λ (see module 7).</p>' +
         hx_table(['Type', 'Particles', 'Features'], [['Rayleigh (x ≪ 1)', 'Molecules N₂, O₂', 'σ ∝ λ⁻⁴; symmetric P(Θ) = ¾(1 + cos²Θ); blue sky'],
                                               ['Mie (x ~ 1)', 'Aerosols, cloud droplets', 'Weak λ dependence (τ ∝ λ^−α); strong forward peak'],
                                               ['Raman (inelastic)', 'N₂, O₂ (rotational)', 'Changes wavelength; causes the Ring effect (fills in Fraunhofer lines) in DOAS']], 'left') +
         eq('Single-scattering albedo', 'ω<sub>0</sub> = σ<sub>s</sub> / (σ<sub>s</sub> + σ<sub>a</sub>) &nbsp; (= 1 for non-absorbing particles; ≈ 0.85 for smoke)') +
         f'<div class="ex"><div class="exh">Example · Rayleigh</div><p>Scattering at 450 nm compared with 650 nm = (650/450)⁴ = <b>{V["rayleigh_450_650"]:.2f}</b> times, which is why blue light is scattered more than red.</p></div>' +
         lfig('f11_phase', 'Figure 5 (study guide): phase functions computed with Mie theory.')),
        ('Emission', '<p>Any body with T &gt; 0 K emits. A black body follows the Planck function; real media emit ε·B. In LTE, <b>Kirchhoff’s law</b> holds: ε<sub>λ</sub> = α<sub>λ</sub> — a gas that absorbs at a wavelength also emits at that wavelength.</p>' +
         eq('Planck', 'B<sub>λ</sub>(T) = (2hc² / λ⁵) · 1 / (exp(hc / λk<sub>B</sub>T) − 1)') + eq('Wien and Stefan–Boltzmann', 'λ<sub>max</sub> · T = 2898 µm·K &nbsp;;&nbsp; M = σ<sub>SB</sub> T⁴') +
         f'<div class="ex"><div class="exh">Example · numbers checked in Python</div><ul><li>Sun (5778 K): λ<sub>max</sub> = {w["sun"]["lam_max_um"]:.2f} µm (visible).</li><li>Earth (288 K): λ<sub>max</sub> = {w["earth"]["lam_max_um"]:.1f} µm (thermal IR); M = {st["M_earth"]:.0f} W m⁻².</li></ul></div>'
         '<p>Emission dominates for λ &gt; ~4 µm (thermal IR, microwave), while reflected sunlight dominates in the UV – visible – near-IR.</p>' + lfig('f8_planck', 'Figure 6 (study guide): Planck curves of the Sun and the Earth.')),
        ('Beer–Lambert and optical depth', eq('Extinction', 'dI<sub>λ</sub> = −k<sub>e</sub>(λ) I<sub>λ</sub> ds &nbsp;;&nbsp; k<sub>e</sub> = k<sub>a</sub> + k<sub>s</sub> = Σ σ<sub>i</sub> n<sub>i</sub>') +
         eq('Solution', 'I<sub>λ</sub>(s) = I<sub>λ</sub>(0) · e<sup>−τ<sub>λ</sub></sup> &nbsp;;&nbsp; τ<sub>λ</sub> = ∫ k<sub>e</sub>(λ,s) ds &nbsp;;&nbsp; T = e<sup>−τ</sup>') +
         '<p>Slant path: τ<sub>slant</sub> = τ<sub>vertical</sub> / cos θ (plane-parallel atmosphere).</p>' +
         f'<div class="ex"><div class="exh">Example 1 · mock exam Q2(c)</div><ol class="steps"><li>τ<sub>vertical</sub> = 0.5; θ = 60°; cos 60° = 0.5</li><li>τ<sub>slant</sub> = 0.5 / 0.5 = 1.0</li><li>T = e<sup>−1</sup> = <b>{be["T"]:.4f}</b> ≈ 37%</li></ol></div>' +
         lfig('s4_solar', 'Figure 7 (study guide, lecture-slide photo): solar irradiance at the top of the atmosphere vs sea level — the difference is absorption (O₃, O₂, H₂O, CO₂) and scattering.', ext='jpg', folder='slides', w=640)),
        ('The radiative transfer equation (RTE)', eq('RTE', 'dI<sub>λ</sub>/ds = −k<sub>e</sub> I<sub>λ</sub> + k<sub>a</sub> B<sub>λ</sub>(T) + (k<sub>s</sub>/4π) ∫ P(Θ) I<sub>λ</sub>(Ω′) dΩ′') +
         '<ul><li><b>Term 1</b> = extinction (loss).</li><li><b>Term 2</b> = thermal emission (gain).</li><li><b>Term 3</b> = light from other directions scattered into the line of sight (gain).</li></ul>'
         '<h3>Two simplified cases in common use</h3>' + eq('Thermal IR without scattering (Schwarzschild)', 'I<sub>λ</sub>(TOA) = ε<sub>s</sub> B<sub>λ</sub>(T<sub>s</sub>) T<sub>λ</sub>(0,∞) + ∫ B<sub>λ</sub>(T(z)) ∂T<sub>λ</sub>(z,∞)/∂z dz') +
         eq('UV – visible (DOAS)', 'ln(I<sub>0</sub>/I) = Σ σ<sub>i</sub>′ · SCD<sub>i</sub> + smooth polynomial') + '<p>Lambertian surface: I = A·F<sub>0</sub>·cos θ<sub>0</sub> / π (A: albedo).</p>')])
    return mod, sl, B
