# -*- coding: utf-8 -*-
"""M3 — Passive remote sensing of trace gases: measured quantity, column, profile (study guide Ch.3)."""
from lib import *
from m1 import ul_
from qcore import Bank
V = VERIFIED

def build():
    B = Bank('m3', seed=3)
    A = V['amf']; du = V['DU']
    B.add('What quantity do passive satellite sensors directly measure for trace-gas remote sensing?',
          'The spectral radiance reaching the sensor, over many wavelength channels', ['The gas concentration at each altitude', 'The corrected vertical gas column', 'The molecular temperature of the target gas'],
          'A passive sensor does not emit radiation and does not measure concentration directly; concentration is "retrieved" by inverting a radiative transfer model. Guide 3.1.', 1, 'Measured quantity', origin='goc', src='Study guide Ch.3 (checklist)')
    B.add('In the UV–visible–SWIR (solar backscatter) range, which quantity is normally used for the retrieval?',
          'The reflectance R(λ) = π·I(λ) / (μ₀·E₀(λ)), i.e. radiance normalised by the solar irradiance', ['The brightness temperature T_B of the atmosphere', 'The transmission I/I₀ through the limb', 'The Ångström exponent of the aerosol'],
          'Guide 3.1: measure the Earthshine radiance and normalise by the solar irradiance → reflectance. Instruments: GOME-2, OMI, TROPOMI, OCO-2.', 1, 'Measured quantity', src='Study guide 3.1')
    B.add('In the thermal infrared, in what form is the radiation often expressed, and which instruments measure it?',
          'As brightness temperature; IASI, AIRS, CrIS', ['As reflectance; OMI, GOME-2', 'As transmission; SAGE, ACE-FTS', 'As optical depth; MODIS, VIIRS'],
          'Guide 3.1: TIR measures radiance emitted by the surface and atmosphere, often expressed as T_B. Occultation measures I/I₀ (ACE-FTS, SAGE).', 1, 'Measured quantity', src='Study guide 3.1')
    B.add('In the forward model y = F(x, b) + ε, what do the symbols mean?',
          'y is the measured spectrum, x the state (gas amounts), b other parameters (temperature, surface, clouds, aerosols), ε the error', ['y is the state, x the measured spectrum, b the noise, ε a constant', 'y is the AMF, x the SCD, b the VCD, ε the scattering', 'y is the a priori, x the Jacobian, b the gain, ε the DOFS'],
          'A retrieval inverts F to find x from y. Guide 3.1.', 2, 'Measured quantity', src='Study guide 3.1')
    B.add('How is the vertical column density VCD defined, and in which units is it usually given?',
          'VCD = ∫ n(z) dz, in molecule cm⁻² (or Dobson Units for O₃)', ['VCD = ∫ n(s) ds along the light path, in µm', 'VCD = SCD · AMF, in W m⁻²', 'VCD = n(0) at the ground, in ppm'],
          'Guide 3.2: 1 DU = 2.69×10¹⁶ molecule cm⁻². The SCD is the integral along the light path.', 1, 'Total column', src='Study guide 3.2')
    B.add(f'An O₃ column is 300 DU. Convert it to molecule cm⁻² (1 DU ≈ 2.69×10¹⁶).',
          f'≈ {du["example_300DU"]:.2e} molecule cm⁻²'.replace('e+18', '×10¹⁸'), ['≈ 8.1×10¹⁶ molecule cm⁻²', '≈ 1.1×10¹⁴ molecule cm⁻²', '≈ 2.69×10¹⁹ molecule cm⁻²'],
          f'300 × 2.687×10¹⁶ = {du["example_300DU"]:.3e} (Python). With 2.69×10¹⁶ it gives 8.07×10¹⁸.', 2, 'Total column', src='Study guide 3.2 (DU constant); number computed in Python')
    B.add('What are the three main steps of a DOAS retrieval of the tropospheric NO₂ column?',
          '(1) spectral fit → slant column SCD; (2) remove the stratospheric part; (3) divide by the tropospheric AMF to get the VCD', ['(1) compute AMF; (2) filter clouds; (3) fit a Planck function', '(1) choose an a priori; (2) compute the Jacobian; (3) compute DOFS', '(1) measure transmission; (2) take the logarithm; (3) plot a curve of growth'],
          'Answer key Q3(a): fit ln(I₀/I) = Σσᵢ′SCDᵢ + polynomial; remove the stratosphere (reference sector, chemistry-transport model); VCD = (SCD − SCD_strat)/AMF_trop.', 2, 'DOAS', origin='goc', src='Mock exam Q3(a)')
    B.add('Why does DOAS use differential cross-sections σ′ and a polynomial?',
          'The polynomial absorbs the smooth part (Rayleigh, Mie, surface); σ′ fits the narrow structures characteristic of the gas', ['To remove all instrument noise completely', 'To convert wavelength to frequency', 'To turn the solution into an identity matrix'],
          'Guide 3.2: ln(I₀/I) = Σ σᵢ′ SCDᵢ + Σ aₚλᵖ. The smooth part is separated; the rapidly varying (molecular) part is fitted by least squares.', 2, 'DOAS', src='Study guide 3.2')
    B.add('How is the air mass factor AMF defined?',
          'AMF = SCD / VCD, reflecting the length of the light path', ['AMF = VCD / SCD, reflecting the background concentration', 'AMF = I₀ / I, reflecting the transmittance', 'AMF = τ / ω₀, reflecting the scattering fraction'],
          'AMF depends on viewing/solar geometry, surface albedo, clouds, aerosols and the a priori profile shape. Geometric approximation: AMF ≈ 1/cos θ₀ + 1/cos θ.', 1, 'AMF', src='Study guide 3.2')
    B.add(f'Use the geometric approximation AMF ≈ 1/cos θ₀ + 1/cos θ with θ₀ = 60° and θ = 30°. What is the value?',
          f'≈ {A["amf"]:.2f}', ['≈ 1.50', '≈ 2.00', '≈ 5.20'],
          f'1/cos 60° = 2; 1/cos 30° = 1.1547 → sum {A["amf"]:.4f}. (When both angles are 0: AMF = 2.)', 2, 'AMF', src='Study guide 3.2; number computed in Python')
    B.add(f'SCD = 8×10¹⁵, stratospheric SCD_strat = 3×10¹⁵ molecule cm⁻², tropospheric AMF = {A["amf"]:.2f}. What is the tropospheric VCD?',
          f'≈ {A["vcd"]:.2e} molecule cm⁻²'.replace('e+15', '×10¹⁵'), ['≈ 2.5×10¹⁵ molecule cm⁻² (forgot to subtract the stratosphere)', '≈ 1.6×10¹⁶ molecule cm⁻² (multiplied instead of dividing)', '≈ 5.0×10¹⁵ molecule cm⁻² (forgot to divide by the AMF)'],
          f'VCD = (SCD − SCD_strat)/AMF = 5×10¹⁵ / {A["amf"]:.4f} = {A["vcd"]:.3e}. Recomputed in Python.', 2, 'AMF', src='Study guide 3.2 (VCD formula); number computed in Python')
    B.add('Why does the AMF depend on the a priori profile shape and on clouds?',
          'Because the sensitivity to the light varies with altitude — low near the ground, shielded below clouds, enhanced above — so the result depends on where the gas is assumed to be', ['Because clouds and the a priori change the real number of gas molecules in the atmosphere', 'Because the AMF depends only on the satellite orbit configuration', 'Because clouds emit thermal radiation instead of the gas'],
          'Answer key Q3(b): AMF = SCD/VCD measures the light-path length; its sensitivity varies with altitude, so a vertical-distribution assumption is needed.', 2, 'AMF', origin='goc', src='Mock exam Q3(b)')
    B.add('Which standard method does Rodgers’ approach use to retrieve a vertical profile?',
          'Optimal estimation with the Jacobian K and an a priori profile x_a', ['Multiple linear regression without a priori', 'Fourier transform of the emission spectrum', 'Direct measurement with a telescope'],
          'Guide 3.3: minimise χ² = (y−F(x))ᵀS_ε⁻¹(y−F(x)) + (x−x_a)ᵀS_a⁻¹(x−x_a). The problem is ill-posed, so regularisation is needed.', 2, 'Profile', src='Study guide 3.3')
    B.add('What is the linear solution of optimal estimation?',
          'x̂ = x_a + (KᵀS_ε⁻¹K + S_a⁻¹)⁻¹ KᵀS_ε⁻¹ (y − K·x_a)', ['x̂ = x_a · K / y', 'x̂ = (y − x_a) · S_a · S_ε', 'x̂ = K⁻¹ y with no a priori'],
          'Here x_a is the a priori, S_a its covariance, S_ε the measurement-noise covariance. For nonlinear problems iterate with Gauss–Newton.', 3, 'Profile', src='Study guide 3.3')
    B.add('Where does the information on altitude come from when a sensor looks straight down (nadir)? Choose the most complete answer.',
          'The strength of absorption varying with wavelength (different penetration depths), pressure broadening of lines, and temperature contrast T(z)', ['Only from the time delay of a laser pulse', 'Only from a viewing angle that changes tangentially', 'Only from the size of the pixel on the ground'],
          'Guide 3.4: UV (BUV/SBUV: 270 nm sensitive to the upper stratosphere, 310–330 nm down to the troposphere); TIR (line width ∝ pressure: line centre probes high, wings probe low); T(z) gives emission contrast. Limb sounders use geometry.', 2, 'Vertical information', origin='goc', src='Mock exam Q3(c)')
    B.add('In the thermal infrared, which part of a spectral line probes low altitudes?',
          'The line wings, because pressure broadening makes lines wide in the lower atmosphere', ['The line centre, because low pressure makes lines narrow', 'The whole line equally', 'None — lines carry no altitude information'],
          'Lorentz width ∝ pressure: the strongly absorbing line centre saturates high up and probes high altitudes; the weakly absorbing wings penetrate to lower levels. Guide 3.4.', 3, 'Vertical information', src='Study guide 3.4')
    B.add('Why is 270 nm radiation sensitive to the upper stratosphere while 310–330 nm reaches the troposphere (BUV method)?',
          'At 270 nm O₃ absorbs very strongly so photons do not penetrate deep; at 310–330 nm absorption is weak so photons go lower', ['Because O₃ exists only above 40 km, where 270 nm sees it', 'Because 310–330 nm radiation is totally reflected by clouds', 'Because 270 nm has a longer wavelength and penetrates deeper'],
          'Guide 3.4: different absorption strengths → different penetration depths → weighting functions peaking at different altitudes.', 3, 'Vertical information', src='Study guide 3.4')
    B.add('In which case does the sensor NOT measure concentration directly and must retrieve it?',
          'In every passive remote-sensing case: it measures radiance and inverts a radiative transfer model', ['Only when there are clouds', 'Only in the thermal infrared', 'Only in limb mode'],
          'The core principle of Ch.3: the measured quantity is spectral radiance, not concentration.', 1, 'Measured quantity', src='Study guide 3.1')
    B.essay('(a) Explain the three steps of a DOAS retrieval of the tropospheric NO₂ column from a nadir UV–visible spectrometer.\n(b) Why does the AMF depend on the a priori profile shape and on clouds?\n(c) Give two physical reasons why a nadir sounder has information on the vertical distribution of a gas.',
            '(a) 1) Least-squares fit of ln(I₀/I) = Σσᵢ′SCDᵢ + polynomial → SCD. 2) Remove the stratospheric part (reference sector or chemistry-transport model). 3) Divide by the tropospheric AMF from a radiative transfer model → VCD.\n'
            '(b) AMF = SCD/VCD is the light-path length; sensitivity varies with altitude (low near the surface, shielded below clouds, enhanced above), so the result depends on where the gas is assumed to be.\n'
            '(c) Absorption strength varying with λ (different penetration depths); pressure broadening of lines; temperature contrast T(z) in the TIR.', 3, 'Mock exam', origin='goc', src='Mock exam Q3 (2.5 points) + suggested answer')
    B.essay('Describe the principle of retrieving the total column and the profile of a trace gas; where does the altitude information come from?',
            'Measured: spectral radiance I(λ) (or reflectance, brightness temperature), not concentration. Column: DOAS → SCD, VCD = SCD/AMF. Profile: y = y₀ + K(x − x₀) + ε, K = ∂F/∂x (Jacobian/weighting functions); ill-posed, so regularise with optimal estimation (Rodgers). '
            'Altitude information: absorption strength vs λ, pressure broadening, temperature contrast, limb/occultation geometry.', 3, 'Overview', origin='goc', src='Study guide Ch.3 (question)')
    B.essay(f'Compute the geometric AMF and the VCD: θ₀ = 60°, θ = 30°, SCD = 8×10¹⁵, SCD_strat = 3×10¹⁵ molecule cm⁻².',
            f'AMF ≈ 1/cos 60° + 1/cos 30° = 2 + 1.1547 = {A["amf"]:.4f}. VCD = (SCD − SCD_strat)/AMF = 5×10¹⁵ / {A["amf"]:.4f} ≈ {A["vcd"]:.3e} molecule cm⁻². In DU (if it were O₃): divide by 2.687×10¹⁶.', 3, 'AMF', src='Study guide 3.2 (extra exercise; numbers checked in Python)')
    sl = [
        cover('Trace-gas retrieval: column and profile', 'Study guide chapter 3',
              '<b>Atmospheric Remote Sensing</b> · USTH<br>Spectral radiance · DOAS · AMF · optimal estimation'),
        S('Measured quantity: radiance, not concentration', cards(
            card('UV – visible – SWIR', 'Backscattered solar radiance → reflectance R(λ).<br>GOME-2, OMI, TROPOMI, OCO-2'),
            card('Thermal infrared', 'Emitted radiance, expressed as brightness temperature T<sub>B</sub>.<br>IASI, AIRS, CrIS'),
            card('Occultation', 'Transmission I/I<sub>0</sub> of the Sun or a star through the limb.<br>ACE-FTS, SAGE'), cols=3)),
        S('Forward model and retrieval', fm('<span class="l">Forward model</span>y = F(x, b) + ε', 38) +
          legend([('y', 'measured spectrum'), ('x', 'state: the gas amount to find'), ('b', 'temperature, surface, clouds, aerosols'), ('ε', 'measurement error')], 2) +
          fm('<span class="l">Reflectance</span>R(λ) = π I(λ) / (μ<sub>0</sub> E<sub>0</sub>(λ))', 32)),
        S('Lecture slides: GOME and TROPOMI', cols(figfit('s1_gome', 'Figure 8: GOME — solar irradiance and Earth radiance; their ratio is the reflectance.', 500, 560, 'jpg', 'slides'),
                                           figfit('s2_tropomi', 'Figure 9: TROPOMI L1b radiance of one pixel (hyperspectral) vs broad VIIRS channels.', 500, 560, 'jpg', 'slides'))),
        S('Total column: DOAS step 1', fm('<span class="l">Spectral fit → slant column</span>ln( I<sub>0</sub>(λ) / I(λ) ) = Σ<sub>i</sub> σ<sub>i</sub>′(λ) · SCD<sub>i</sub> + Σ<sub>p</sub> a<sub>p</sub> λ<sup>p</sup>', 30) +
          figfit('f13_doas', 'Figure 10: DOAS — remove the smooth part, fit the narrow structures with laboratory cross-sections.', 380) + '<p class="note">SCD = ∫ n ds along the light path; σ′ comes from the laboratory.</p>'),
        S('Total column: AMF and VCD', fm('<span class="l">Vertical column</span>VCD = (SCD − SCD<sub>strat</sub>) / AMF<sub>trop</sub> &nbsp;,&nbsp; AMF = SCD / VCD', 30) +
          fm('<span class="l">Geometric approximation</span>AMF ≈ 1/cos θ<sub>0</sub> + 1/cos θ', 30) +
          callout('info', f'Example θ₀ = 60°, θ = 30°', f'AMF = 2 + 1.155 = <b>{A["amf"]:.2f}</b>; SCD = 8×10<sup>15</sup>, SCD<sub>strat</sub> = 3×10<sup>15</sup> → VCD ≈ <b>{A["vcd"]/1e15:.2f}×10<sup>15</sup></b> molecule cm<sup>−2</sup>')),
        S('Profile: optimal estimation', fm('<span class="l">Linearisation</span>y = y<sub>0</sub> + K (x − x<sub>0</sub>) + ε &nbsp;,&nbsp; K = ∂F/∂x', 28) +
          fm('<span class="l">Solution</span>x̂ = x<sub>a</sub> + (K<sup>T</sup>S<sub>ε</sub><sup>−1</sup>K + S<sub>a</sub><sup>−1</sup>)<sup>−1</sup> K<sup>T</sup>S<sub>ε</sub><sup>−1</sup> (y − K x<sub>a</sub>)', 26) +
          '<p class="note">x<sub>a</sub>: a priori profile · S<sub>a</sub>: its covariance · S<sub>ε</sub>: measurement-noise covariance. The problem is ill-posed, so it must be regularised.</p>'),
        S('Where does altitude information come from?', cols(figfit('f6_wf', 'Figure 12: weighting functions peak at different altitudes.', 480, 480),
          ulb(['<b>Absorption strength</b> vs λ: different penetration depths', '<b>Pressure broadening</b>: line centre sees high, wings see low', '<b>Temperature T(z)</b> gives emission contrast', '<b>Limb geometry</b>: tangent height'], 27, 20), flex=[0.8, 1.2])),
        S('Wavelength windows for each species', figfit('s3_wavelengths', 'Figure 11 (lecture slide): wavelength windows for SO₂, HCHO, BrO, NO₂, O₃, OClO, O₂–O₂, H₂O, O₂, aerosol.', 520, 700, 'jpg', 'slides')),
        S('Exam checklist — Chapter 3', chk(['Measured quantity = spectral radiance (reflectance, T<sub>B</sub>, transmission), not concentration', 'Column: DOAS → SCD; AMF from a radiative transfer model → VCD = SCD/AMF',
            'Profile: forward model + Jacobian K + optimal estimation with an a priori', 'Altitude information: λ, pressure broadening, temperature contrast, limb geometry'])),
        S('Key points', dul(['Measure radiance; retrieve by inverting a radiative transfer model', 'Column: SCD from DOAS, then divide by AMF', 'Profile: optimal estimation with a priori x<sub>a</sub>', 'Altitude information from λ, pressure, temperature, geometry']))]
    mod = dict(id='m3', slug='03-passive-trace-gas', title='M3 · Trace-gas retrieval', en='Passive remote sensing of trace gases',
               question='<ul><li>What is the quantity directly measured by passive satellite sensors for remote sensing of atmospheric trace gases?</li><li>Explain the principle to derive the abundance of a trace gas in terms of (i) integrated concentration over the atmospheric column and (ii) vertical profile of gas concentration.</li><li>Where is the information on the vertical distribution of the gas coming from?</li></ul>',
               calcs=[('doas', 'DOAS: AMF → VCD → DU')],
               checklist=['Measured quantity = spectral radiance (reflectance / brightness temperature / transmission), NOT concentration.', 'Column: DOAS fit → SCD; AMF from RT model → VCD = SCD/AMF.',
                          'Profile: forward model + Jacobian K + Optimal Estimation with a priori.', 'Vertical information: different penetration depths vs λ, pressure broadening of lines, temperature contrast, limb geometry.'],
               summary=['Cảm biến thụ động đo bức xạ phổ (radiance) — không đo nồng độ trực tiếp; nồng độ được “truy hồi” bằng cách nghịch đảo mô hình truyền bức xạ.', 'Cột tổng: DOAS → cột nghiêng SCD; hệ số khối khí AMF → cột thẳng đứng VCD = SCD/AMF.',
                        'Profil thẳng đứng: ước lượng tối ưu (Optimal Estimation) dùng ma trận Jacobian K và profil tiên nghiệm.', 'Thông tin độ cao đến từ: độ hấp thụ mạnh/yếu theo bước sóng, mở rộng vạch theo áp suất, tương phản nhiệt độ, và hình học quan sát limb.'],
               sections=[
        ('The measured quantity', '<p>A passive sensor <b>does not emit light</b>; it only records the <b>spectral radiance I(λ)</b> (W m⁻² sr⁻¹ µm⁻¹) arriving from one viewing direction, in many wavelength channels (a spectrum). Gas concentration is <b>never</b> measured directly.</p>' +
         hx_table(['Spectral range', 'Quantity', 'Instruments'], [['UV – visible – SWIR (backscattered sunlight)', 'Radiance normalised to reflectance R(λ) = π I / (μ₀ E₀)', 'GOME-2, OMI, TROPOMI, OCO-2'],
                                                          ['Thermal infrared', 'Brightness temperature T_B', 'IASI, AIRS, CrIS'], ['Occultation', 'Transmission I/I₀', 'ACE-FTS, SAGE']], 'left') +
         eq('Forward model', 'y = F(x, b) + ε') + '<p>A retrieval <b>inverts</b> the radiative transfer model F to find the state x (gas amount) from the measured spectrum y, while b (temperature, surface, clouds, aerosols) are other parameters.</p>' +
         lfig('s1_gome', 'Figure 8 (lecture-slide photo): GOME — solar irradiance and Earth radiance; their ratio is the reflectance.', ext='jpg', folder='slides', w=560) +
         lfig('s2_tropomi', 'Figure 9 (lecture-slide photo): TROPOMI L1b radiance of one pixel (hyperspectral) vs the broad VIIRS channels.', ext='jpg', folder='slides', w=560)),
        ('(i) Total column: DOAS', '<p>The <b>vertical column</b> is VCD = ∫ n(z) dz (molecule cm⁻²; O₃ uses Dobson Units, 1 DU = 2.69×10¹⁶ molecule cm⁻²). The standard UV–visible method is <b>DOAS</b> (Differential Optical Absorption Spectroscopy), in three steps:</p>'
         '<ol class="steps"><li><b>Spectral fit → slant column (SCD).</b> From Beer–Lambert, the optical depth is split into a rapidly varying part (molecular absorption structures) and a smooth part (Rayleigh, Mie, surface).</li>'
         '<li><b>Air mass factor (AMF).</b> A radiative transfer model computes AMF = SCD / VCD, depending on geometry, albedo, clouds, aerosols and the a priori profile shape.</li>'
         '<li><b>Stratosphere–troposphere separation</b> (for tropospheric gases): reference sector over a clean ocean, or chemistry-transport model assimilation.</li></ol>' +
         eq('Spectral fit', 'ln( I<sub>0</sub>(λ) / I(λ) ) = Σ<sub>i</sub> σ<sub>i</sub>′(λ) · SCD<sub>i</sub> + Σ<sub>p</sub> a<sub>p</sub> λ<sup>p</sup> &nbsp;;&nbsp; SCD = ∫ n ds') + eq('Tropospheric column', 'VCD = (SCD − SCD<sub>strat</sub>) / AMF<sub>trop</sub> &nbsp;;&nbsp; AMF ≈ 1/cos θ<sub>0</sub> + 1/cos θ (geometric approximation)') +
         lfig('f13_doas', 'Figure 10 (study guide): DOAS — the smooth part is removed; narrow structures are fitted with laboratory cross-sections to give the SCD.') +
         f'<div class="ex"><div class="exh">Example · AMF and VCD (numbers checked in Python)</div><ol class="steps"><li>θ₀ = 60°, θ = 30° → AMF = 2 + 1.1547 = <b>{A["amf"]:.4f}</b></li><li>SCD = 8×10¹⁵; SCD<sub>strat</sub> = 3×10¹⁵ molecule cm⁻²</li><li>VCD = 5×10¹⁵ / {A["amf"]:.4f} = <b>{A["vcd"]:.3e}</b> molecule cm⁻²</li></ol></div>' +
         lfig('s3_wavelengths', 'Figure 11 (lecture-slide photo): wavelength windows chosen for each species (SO₂, HCHO, BrO, NO₂, O₃, OClO, O₂–O₂, H₂O, O₂, aerosol).', ext='jpg', folder='slides', w=620) +
         '<p><b>Alternative approaches:</b> optimal estimation with scaling of an a priori profile (CO in SWIR/TIR), or ratio methods for greenhouse gases (XCO₂ = CO₂ column / dry-air column, using the O₂ A-band).</p>'),
        ('(ii) Vertical profile: optimal estimation', '<p>Divide the atmosphere into N layers, state x = (x₁…x_N). Linearise around a reference:</p>' + eq('Linearisation', 'y = y<sub>0</sub> + K (x − x<sub>0</sub>) + ε &nbsp;;&nbsp; K = ∂F/∂x (Jacobian, weighting functions)') +
         '<p>The problem is <b>ill-posed</b>: more unknowns than independent pieces of information, plus noise — so it must be regularised. The standard method is <b>optimal estimation</b> (Rodgers):</p>' +
         eq('Cost function', 'χ² = (y − F(x))<sup>T</sup> S<sub>ε</sub><sup>−1</sup> (y − F(x)) + (x − x<sub>a</sub>)<sup>T</sup> S<sub>a</sub><sup>−1</sup> (x − x<sub>a</sub>)') +
         eq('Linear solution', 'x̂ = x<sub>a</sub> + (K<sup>T</sup> S<sub>ε</sub><sup>−1</sup> K + S<sub>a</sub><sup>−1</sup>)<sup>−1</sup> K<sup>T</sup> S<sub>ε</sub><sup>−1</sup> (y − K x<sub>a</sub>)') +
         '<p>x<sub>a</sub>: a priori profile; S<sub>a</sub>: its covariance; S<sub>ε</sub>: measurement-noise covariance. If nonlinear, iterate with Gauss–Newton. Other methods: Tikhonov regularisation, onion peeling for limb data.</p>'),
        ('Where does the vertical information come from?', '<p>From the fact that <b>different measurements are sensitive to different altitudes</b>, i.e. their weighting functions K(z) peak at different heights:</p>' +
         hx_table(['Source of information', 'How it works', 'Example'], [
             ['Absorption strength vs λ (nadir)', 'Strong absorption → photons do not penetrate deep → signal from high altitudes; weak absorption → from lower layers', 'O₃ in the UV: 270 nm sees the upper stratosphere; 310–330 nm reaches the troposphere (BUV/SBUV)'],
             ['Pressure and temperature dependence of line shapes (TIR)', 'Line width ∝ pressure: line centre probes high, wings probe low; T(z) creates emission contrast', 'IASI O₃/CO profiles'],
             ['Viewing geometry (limb, occultation)', 'Each line of sight has a tangent height; scanning the limb gives 1–3 km vertical resolution', 'Onion peeling'],
             ['Other', 'Temperature-dependent cross-sections, multiple angles, Raman/Rayleigh scattering', 'A little extra information']], 'left') +
         lfig('f6_wf', 'Figure 12 (study guide): weighting functions peak at different altitudes for different absorption strengths.', w=460))])
    return mod, sl, B
