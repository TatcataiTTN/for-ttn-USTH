# -*- coding: utf-8 -*-
"""Giảm length-bias: rút gọn đáp án ĐÚNG đang dài hơn mọi đáp án sai (nội dung đầy đủ chuyển sang phần giải thích).
Khóa = nguyên văn đáp án đúng; giá trị = bản rút gọn vẫn đúng. WRONG: kéo dài vài đáp án sai quá ngắn."""
SHORT = {
 'pc': {
  'It is the constraint towards the a-priori profile that makes the ill-posed problem solvable': 'The constraint toward the a priori that makes the problem solvable',
  'Measurement geometry, temperature and pressure profiles, and spectroscopic parameters (e.g. HITRAN, GEISA)': 'Geometry, T and P profiles, spectroscopy databases',
  'UV reflectance is sensitive to the stratosphere and the total column; thermal-IR radiance is sensitive to the free troposphere (peak around 3 km for IASI)': 'UV: stratosphere and column; IR: free troposphere (≈ 3 km)',
  'Roughly one independent piece of information in the whole troposphere: it separates the lower from the upper troposphere only in favourable thermal conditions': 'About one piece of information for the whole troposphere',
  'One ozone profile is adjusted to fit the co-located IR and UV spectra simultaneously (minimising both residuals), which enhances sensitivity to the lowermost troposphere': 'A single ozone profile is fitted to the IR and UV spectra at once',
  '+40% over land (and +67% over ocean) in the information on the lowest layers': '+40% over land (and +67% over ocean)',
  'It depends on SSA, AOD and the height of the layer together, so values are not comparable from case to case': 'It depends on SSA, AOD and layer height together',
  'A full radiative-transfer calculation for every pixel is too costly; LUTs store pre-computed reflectances for aerosol types, geometries and wavelengths': 'Full radiative transfer per pixel is too slow',
  'About 0.15 globally, typically varying between 0.05 and 2.0': 'About 0.15, typically 0.05–2.0',
  'The 3D distribution of desert dust (extinction profile at 10 µm) from 12 micro-windows between 8 and 12 µm of cloud-free IASI spectra': 'Dust extinction profiles from IASI at 8–12 µm',
  'The dust plume mixed down to the surface when reached by the boundary layer, whereas the simulated dust stayed in the free troposphere': 'It mixed to the surface; the model kept dust aloft',
  'O₂ is well mixed with a known profile: a higher scattering layer shortens the photon path and weakens the O₂ absorption inside the band': 'O₂ is well mixed, so a higher layer shortens the photon path'},
 'm7': {
  'x = 2πr / λ (r: particle radius, λ: wavelength)': 'x = 2πr/λ', 'x ≈ 57 → upper Mie, approaching geometric optics': 'x ≈ 57, upper Mie / geometric',
  'It has a very strong forward peak and weak side and back lobes (g ≈ 0.6–0.8 for aerosols)': 'A strong forward peak and weak side/back lobes', 'To 2 (the "extinction paradox")': 'To 2',
  '≈ 3.6 (above 2, then it oscillates and converges to 2)': '≈ 3.6, then oscillates to 2', 'As x⁴ (e.g. from x = 0.1 to 0.5 Q_ext grows ~600 times)': 'As x⁴',
  'Geometric optics (very large particles: raindrops; hexagonal ice crystals)': 'Geometric optics (rain and ice)', 'The T-matrix or discrete-dipole methods': 'The T-matrix method',
  'Visible: x ≈ 114, geometric optics; radar: x ≈ 0.02, Rayleigh': 'Visible: x ≈ 114; radar: x ≈ 0.02', 'The long slant path removes blue light by Rayleigh scattering (λ⁻⁴)': 'Blue is removed by Rayleigh scattering',
  'Mie scattering by fine particles depends weakly on wavelength': 'Mie: weak dependence on wavelength', 'D⁶ (Rayleigh regime for radar wavelengths)': 'D⁶ (Rayleigh, radar)'},
 'm3': {
  'Optimal estimation with the Jacobian K and an a priori profile x_a': 'Optimal estimation (Jacobian K + a priori)', 'x̂ = x_a + (KᵀS_ε⁻¹K + S_a⁻¹)⁻¹ KᵀS_ε⁻¹ (y − K·x_a)': 'x̂ = x_a + G(y − K·x_a)',
  'The strength of absorption varying with wavelength (different penetration depths), pressure broadening of lines, and temperature contrast T(z)': 'Absorption depth varies with λ; pressure broadening',
  'The line wings, because pressure broadening makes lines wide in the lower atmosphere': 'The line wings (pressure broadening at low altitude)', 'At 270 nm O₃ absorbs very strongly so photons do not penetrate deep; at 310–330 nm absorption is weak so photons go lower': 'At 270 nm O₃ absorbs strongly, so photons stay high',
  'VCD = 2×10¹⁶ molecules cm⁻² ≈ 0.74 DU': 'VCD = 2×10¹⁶ cm⁻² ≈ 0.74 DU', 'By about 30% — the AMF is usually the largest error source': 'About 30%',
  'Filling-in of Fraunhofer lines by rotational Raman scattering, fitted as a pseudo-absorber': 'Ring effect (Raman filling-in)', 'More absorber along the path and higher pressure (Lorentz broadening)': 'More absorber and higher pressure'},
 'm8': {
  'I ≈ B(T_s)·e^(−τ_aer) + B(T_layer)·(1 − e^(−τ_aer))': 'B_s·e^(−τ) + B_l·(1 − e^(−τ))', 'The 5 km layer, because it is colder (~6.5 K/km) so its thermal contrast with the surface is larger': 'The 5 km layer: colder, more contrast',
  'Because the signal depends on τ_aer × (T_s − T_layer): AOD and height are degenerate, so they must be retrieved together': 'AOD and height are degenerate (τ × ΔT)',
  'It works day and night, over bright deserts where visible methods fail, and is sensitive to coarse particles': 'Works day and night, over bright deserts', 'A high aerosol layer reflects photons early so the path through O₂ is shorter → weaker O₂ absorption (shallower lines)': 'A high layer shortens the O₂ path: weaker absorption',
  '~0.5–1 km (over ocean and dark land)': '~0.5–1 km', 'To distinguish surface PM from elevated transport, long-range transport, radiative effects and aviation safety (volcanic ash)': 'Surface PM vs elevated transport',
  '≈ 0.47 at 6 km versus ≈ 0.88 at 1 km: a higher layer roughly halves the O₂ absorption': '≈ 0.47 at 6 km vs ≈ 0.88 at 1 km', 'Surface cooling and inversions make the layer as warm as the surface, so there is no thermal contrast': 'No thermal contrast (inversion)'},
 'pb': {
  'H = RT/(Mg) ≈ 8.3 km (T = 284 K): the height over which pressure falls by a factor e': 'H = RT/(Mg) ≈ 8.3 km (the e-folding height)', '1 nmol of the species per mole of air (10⁻⁹)': '1 nmol per mole of air', 'τ = 1/k_tot ≈ 4.0 h, shorter than any single lifetime except outflow': 'τ = 1/k_tot ≈ 4.0 h',
  'Peroxy radicals (RO₂, HO₂ from the oxidation of VOCs) convert NO to NO₂ without consuming O₃': 'Peroxy radicals convert NO to NO₂ without using O₃', 'It lowers ozone (titration NO + O₃ → NO₂ + O₂) and limits its production: VOC-limited regime': 'It lowers ozone by titration: VOC-limited regime',
  'NO₂ lives hours to a day and disappears before it spreads; CH₄ lives about 10 years, far longer than the mixing time': 'NO₂ lives hours; CH₄ lives about 10 years', 'It is a source of OH, the main oxidant that breaks down pollutants and greenhouse gases and drives photochemical smog and ozone formation': 'It is a source of OH, the main oxidant'},
 'pl': {
  'The atmosphere is semi-transparent: the pulse is attenuated but continues, and each delay corresponds to a distance R; the signal falls as 1/z² and with transmission': 'Attenuated, not blocked: signal falls as 1/z² and with T',
  'The geometrical overlap between the laser beam and the telescope field of view (0 < overlap < 1)': 'Overlap of the beam and the field of view', 'The pulse crosses the same atmosphere twice: from the laser to the scatterer and back to the telescope': 'The pulse crosses the atmosphere twice (out and back)',
  'It is close to the ON line but not absorbed by the target gas, so it measures the other attenuation (particles, molecules) that cancels in the ratio': 'It is not absorbed by the gas and cancels the rest', 'α = (1/2Δr)·ln[ P_OFF(r₁)·P_ON(r₂) / (P_ON(r₁)·P_OFF(r₂)) ] taken positive': 'α = (1/2Δr)·ln[P_OFF(r₁)P_ON(r₂)/(P_ON(r₁)P_OFF(r₂))]',
  'It gives the vertical profile day and night with depolarisation to flag non-spherical dust, but only along a narrow curtain with 16-day revisit': 'Day and night profile, depolarisation, but a narrow curtain'},
 'p0': {
  'Sources and sinks → light–matter interaction → instrument and geometry → retrieval (inverse problem) → interpretation (sensitivity, validation)': 'Sources/sinks → light–matter → instrument → retrieval → interpretation',
  'Solar occultation: it is self-calibrating (I/I₀ measured in the same view) and has high vertical resolution': 'Solar occultation: self-calibrating, high vertical resolution', 'The a-priori profile plus a smoothed version of the true profile: x̂ = xₐ + A(x − xₐ) + ε': 'The a priori plus a smoothed truth: x̂ = xₐ + A(x − xₐ) + ε',
  'J = α·B(T): the absorption coefficient times the Planck function (Kirchhoff’s law)': 'J = α·B(T) (Kirchhoff)', 'DOFS = trace(A) = 1.0: about one independent piece of information': 'DOFS = trace(A) = 1.0 (one piece of information)',
  'C1: NO₂ lives hours to a day (shorter than transport) whereas CH₄ lives about 10 years (much longer than the mixing time)': 'C1: NO₂ lives hours; CH₄ lives about 10 years'},
}
WRONG = {'m7': {'Rayleigh': 'Rayleigh scattering (molecules)', 'Raman': 'Raman scattering (inelastic)', 'Lower Mie': 'Lower Mie (accumulation mode)'}}
H17 = ('p0', 'H·ln 2 ≈ 5.75 km (the lecture says about 5 km)', 'H·ln 2 ≈ 5.8 km')

import zlib
KEEP = 42

def apply(mid, items):
    miss = []
    sm = dict(SHORT.get(mid, {}))
    if mid == 'p0': sm[H17[1]] = H17[2]
    n = 0
    for it in items:
        c = it['correct']; cur = it['opts'][c]
        if cur in sm:
            new = sm.pop(cur)
            if zlib.crc32(cur.encode('utf-8')) % 100 < KEEP: continue      # keep the original (longest) for ~KEEP% of flagged items: balanced length ranks
            it['explain'] = it['explain'] + '\nFull answer: ' + cur; it['opts'][c] = new; n += 1
        if mid == 'm7' and any(o in WRONG['m7'] for o in it['opts']):
            for i, o in enumerate(it['opts']):
                if i != c and o in WRONG['m7']: it['opts'][i] = WRONG['m7'][o]
    return n, list(sm)
