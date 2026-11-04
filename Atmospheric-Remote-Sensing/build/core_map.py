# -*- coding: utf-8 -*-
"""Big 12 = 3 key points + 3 formulas + 3 concepts + 3 principles; ma trận: mỗi ý nhỏ của đề thi mẫu dựa vào ý lõi nào.
Mức độ (đánh giá thủ công, xem ghi chú trên site): A = trả lời trọn vẹn từ lõi; B = lõi cho khung, cần thêm dữ kiện của module; C = đặc thù module."""
COLS = ['Key points', 'Formulas', 'Concepts', 'Principles']
ITEMS = [
 dict(id='K1', col=0, title='From photons to concentration',
      st='We never measure a concentration. We measure <b>light that crossed the atmosphere</b>. The whole course is one chain: <b>sources and sinks</b> (lifetime) → <b>light–matter interaction</b> (absorb, scatter, emit) → <b>instrument and geometry</b> → <b>retrieval</b> (inverse problem) → <b>interpretation</b> (sensitivity, validation).',
      say='A sensor records radiance. The radiative transfer equation links radiance to the amount of gas or aerosol on the path. Retrieval inverts that link, and the answer always carries the instrument’s sensitivity.',
      trap='Treating a retrieved number as the truth: it is an estimate x̂ built from the measurement <i>and</i> an a-priori.', mods=['m1', 'm2', 'm3'], pages=[62, 54, 55]),
 dict(id='K2', col=0, title='Pick the tool by the target',
      st='Wavelength, geometry and platform decide what you can see. <b>UV–visible nadir</b>: columns of NO₂, O₃, HCHO, aerosol, km-scale maps. <b>Thermal IR nadir</b>: CO, O₃, dust, day and night, needs thermal contrast. <b>Limb / occultation</b>: stratospheric profiles, high vertical resolution, coarse horizontal. <b>Lidar</b>: vertical profile of aerosol and cloud along one line.',
      say='There is always a trade-off: vertical versus horizontal resolution, global coverage versus sensitivity near the surface, passive (wide swath, no height) versus active (height, narrow curtain).',
      trap='Giving a tool without the reason. Always say <i>why</i> (resolution, calibration, coverage, contrast).', mods=['m4', 'm6', 'pl'], pages=[67, 78, 58, 61]),
 dict(id='K3', col=0, title='Every product is a smoothed estimate',
      st='A retrieved profile is the a-priori plus a <b>smoothed</b> version of the truth. The <b>averaging kernel</b> A tells you where the instrument sees (rows), its vertical resolution (width) and the <b>DOFS = trace(A)</b> (number of independent pieces of information). The <b>air mass factor</b> inherits the same dependence on the assumed profile.',
      say='Before using a satellite product say: how many independent layers (DOFS), at what altitude is it most sensitive, and how much of it comes from the a-priori?',
      trap='Comparing a model profile directly with a satellite retrieval. Smooth the model first with the averaging kernels.', mods=['m3', 'm5', 'pc'], pages=[118, 120, 121, 112]),
 dict(id='F1', col=1, title='Beer–Lambert: I = I₀·e^(−τ)',
      st='<b>τ = ∫ k<sub>ext</sub> ds = σ·N·L</b>, transmittance <b>t = e<sup>−τ</sup></b>, slant path τ/cos θ. The same law gives AOD, the Ångström exponent (τ ∝ λ<sup>−α</sup>), DOAS (D = σ′·SCD), the slant-column AMF, and the lidar transmission (T²: the pulse goes and comes back).',
      say='Light is attenuated exponentially with optical depth; σ comes from spectroscopy, L from geometry, so measuring τ gives the unknown N.',
      trap='Units (1 km = 10⁵ cm), forgetting 1/cos θ, using one-way T in the lidar equation, writing e<sup>+τ</sup>.', mods=['pa', 'm2', 'm6', 'pl'], pages=[100, 82, 158, 216]),
 dict(id='F2', col=1, title='RTE: dI/dl = −k_ext·I + J',
      st='Extinction (absorption + scattering) removes photons; the source function <b>J</b> adds them. Without scattering, in LTE: <b>J = α·B(T)</b> and <b>I(L) = I(0)·e<sup>−τ(0,L)</sup> + ∫ B(T(l))·e<sup>−τ(l,L)</sup> dτ</b> with the surface term I(0) = ε<sub>s</sub>B(T<sub>s</sub>) + (1 − ε<sub>s</sub>)I<sub>s</sub>. Transparent gas (τ ≪ 1): I ≈ I(0) + τB; opaque gas: only the top layers are seen.',
      say='The signal at the sensor is the attenuated background plus the attenuated emission of every layer; the factor e^(−τ(l,L)) is the weighting function of altitude.',
      trap='Forgetting that the emission of a layer is itself attenuated by the gas above it.', mods=['pa', 'm2', 'm8'], pages=[96, 97, 98, 99]),
 dict(id='F3', col=1, title='Retrieval: x̂ = xₐ + A(x − xₐ) + ε',
      st='Minimise <b>J(x) = [y − F(x)]ᵀS<sub>y</sub>⁻¹[y − F(x)] + [x − x<sub>a</sub>]ᵀR[x − x<sub>a</sub>]</b> (ill-posed → constraint). Linearised: <b>x̂ = x<sub>a</sub> + A(x − x<sub>a</sub>) + Gε, A = GK = ∂x̂/∂x</b>, DOFS = tr(A). Model comparison: x<sub>m,s</sub> = x<sub>a</sub> + A(x<sub>m</sub> − x<sub>a</sub>).',
      say='K (Jacobian) says how the spectrum reacts to the profile; G inverts it with a constraint; A says how the true profile is smoothed into the retrieval.',
      trap='Believing A is the identity: rows broader than a layer mean poor vertical resolution; row sum &lt; 1 means a-priori contribution.', mods=['m3', 'm5', 'pc'], pages=[115, 117, 118, 121]),
 dict(id='C1', col=2, title='Lifetime and mixing',
      st='<b>τ = burden / loss rate = 1/k′</b>. Parallel sinks add as <b>rates</b>: 1/τ = Σ 1/τ<sub>i</sub>; the dominant sink is the one with the largest k. Short-lived species (NO₂, hours to 1 day; SO₂) trace their <b>sources</b> as hotspots; long-lived species (CO ≈ 2 months, CH₄ ≈ 10 years) are <b>well mixed</b> and show small variations. Plume e-folding length L = U·τ.',
      say='Compare the lifetime with the mixing time: shorter than transport → local map of sources; much longer → uniform field.',
      trap='Adding lifetimes instead of rates; forgetting to convert seconds to days (5×10⁶ s ≈ 58 d).', mods=['m1', 'pb'], pages=[38, 40, 49, 50]),
 dict(id='C2', col=2, title='Scattering regimes (size parameter)',
      st='<b>x = 2πr/λ</b>. <b>Rayleigh</b> (x ≪ 1, molecules): σ ∝ λ⁻⁴, symmetric phase function, blue sky (400 nm is ≈ 7 times 650 nm). <b>Mie</b> (x ≈ 1): aerosols, forward peak, α ≈ 0–2. <b>Geometric</b> (x ≫ 1, droplets, crystals): Q → 2, independent of λ, white clouds. Ångström <b>α ≈ 1–2 fine, 0–0.5 coarse</b>.',
      say='Compare the particle size with the wavelength. That one number explains the colour of the sky, the colour of clouds and why dust and smoke have different AOD spectra.',
      trap='Mixing radius and diameter; calling a 0.2 µm sulfate particle “Rayleigh”.', mods=['m7', 'm6', 'm2'], pages=[84, 85, 86, 87, 91]),
 dict(id='C3', col=2, title='The two-wavelength trick',
      st='Whenever something is unknown, use a <b>difference or a ratio of two wavelengths</b> so it cancels: <b>DOAS</b> (σ = σ<sub>b</sub> + σ′, polynomial removes broadband), <b>DIAL</b> (ON/OFF line), <b>Ångström</b> (τ(λ₁)/τ(λ₂)), <b>AAI</b> (UV pair), <b>O₂ A-band</b> (in-band versus continuum).',
      say='What the target changes quickly with wavelength is the fingerprint; everything that changes slowly (Rayleigh, aerosol, surface) is absorbed by a polynomial or cancelled in the ratio.',
      trap='Forgetting the broadband polynomial in DOAS; using ON only in DIAL.', mods=['pa', 'm3', 'm6', 'm8', 'pl'], pages=[110, 111, 159, 165, 231]),
 dict(id='R1', col=3, title='Photon budget',
      st='Along the line of sight <b>gains</b> are surface reflection, single and multiple scattering <i>into</i> the beam, and thermal emission; <b>losses</b> are absorption and scattering <i>out of</i> the field of view. <b>Absorption destroys the photon; scattering only redirects it.</b>',
      say='Every RTE term is either an income or an expense of photons on the path to the sensor.',
      trap='Saying scattering “destroys” light; forgetting multiple scattering in clouds and thick aerosol.', mods=['pa', 'm2'], pages=[81, 82, 83]),
 dict(id='R2', col=3, title='Kirchhoff and Planck',
      st='In local thermodynamic equilibrium <b>ε<sub>λ</sub> = α<sub>λ</sub></b>: what absorbs also emits, with the Planck function <b>B(λ,T)</b>. Wien: <b>λ<sub>max</sub> = 2898/T</b> (Sun ≈ 0.5 µm, Earth ≈ 10 µm); Stefan: M = σT⁴. A thermal signal exists only where the layer is <b>at a different temperature from its background</b>.',
      say='Thermal IR carries both concentration and temperature information, and needs thermal contrast: a cold, high layer shows up; a layer as warm as the surface is invisible.',
      trap='Saying a dust layer at 1 km gives a larger brightness-temperature depression than one at 5 km with the same AOD.', mods=['m2', 'm8', 'pa'], pages=[65, 82, 187]),
 dict(id='R3', col=3, title='Hydrostatic layering',
      st='<b>p = p₀·e<sup>−z/H</sup></b>, H = RT/(Mg) ≈ 8 km: pressure halves every ≈ 5.75 km (H ln 2). Temperature falls ≈ 6.5 K/km in the troposphere. Consequences: <b>Lorentz line width ∝ p</b> (altitude information in the line wings), <b>O₂ is well mixed</b> (A-band measures photon path), thermal contrast grows with height, air density sets lidar molecular backscatter.',
      say='Pressure, density and temperature change with altitude in a known way, so altitude leaves a signature in the spectrum.',
      trap='Using an isothermal atmosphere for temperature-contrast questions (it gives 304 hPa at 10 km instead of the real 265 hPa).', mods=['pb', 'pa', 'm8'], pages=[8, 106, 200]),
]
BY = {i['id']: i for i in ITEMS}

# ---------------- đề thi mẫu gốc (Paper 1): (câu, ý, mức, [ý lõi]) ----------------
P1 = [('Q1', 'a', 'A', ['C1']), ('Q1', 'b', 'A', ['C1']), ('Q1', 'c', 'A', ['C1']),
      ('Q2', 'a', 'A', ['F1', 'R1']), ('Q2', 'b', 'A', ['R2']), ('Q2', 'c', 'A', ['F1']),
      ('Q3', 'a', 'B', ['C3', 'F1', 'K1']), ('Q3', 'b', 'B', ['K3']), ('Q3', 'c', 'B', ['K2', 'R3']),
      ('Q4', 'a', 'B', ['K2']), ('Q4', 'b', 'B', ['K2']), ('Q4', 'c', 'C', ['K2']),
      ('Q5', 'a', 'A', ['F3']), ('Q5', 'b', 'B', ['K3', 'F3']), ('Q5', 'c', 'A', ['K3', 'F3']),
      ('Q6', 'a', 'A', ['F1', 'C2']), ('Q6', 'b', 'B', ['C2', 'R1']), ('Q6', 'c', 'B', ['K2']),
      ('Q7', 'a', 'A', ['C2']), ('Q7', 'b', 'A', ['C2']), ('Q7', 'c', 'B', ['C2']),
      ('Q8', 'a', 'B', ['R3', 'C3']), ('Q8', 'b', 'B', ['R2', 'R3']), ('Q8', 'c', 'C', ['K2']),
      ('Q9', 'a', 'A', ['R1', 'F2']), ('Q9', 'b', 'A', ['F2', 'R2']), ('Q9', 'c', 'A', ['F1']),
      ('Q10', 'a', 'B', ['R3']), ('Q10', 'b', 'A', ['R3']), ('Q10', 'c', 'A', ['C3', 'F1'])]

def stats(parts):
    n = len(parts); a = sum(1 for p in parts if p[2] == 'A'); b = sum(1 for p in parts if p[2] == 'B'); c = n - a - b
    used = {}
    for p in parts:
        for i in p[3]: used[i] = used.get(i, 0) + 1
    return dict(n=n, A=a, B=b, C=c, skeleton=(a + b) / n, full=a / n, used=used)

def serves(parts, qs):
    """Với mỗi ý lõi: danh sách câu (trong parts) dùng nó."""
    out = {i['id']: [] for i in ITEMS}
    for q, _, _, ids in parts:
        for i in ids:
            if q not in out[i]: out[i].append(q)
    return out
