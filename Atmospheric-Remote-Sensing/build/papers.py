# -*- coding: utf-8 -*-
"""Đề thi viết bổ sung (Paper 2–5) theo văn phong đề mẫu. Mỗi ý: (nội dung, mức A/B/C, [ý lõi Big 12]).
Mọi con số tính bằng Python tại thời điểm build (kiểm tra chéo bằng công thức thứ hai khi có thể)."""
import math, json, os
H_, C_, KB_ = 6.62607015e-34, 2.99792458e8, 1.380649e-23
V = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'site', 'data', 'verified.json')))
HY, SK, LX, DL = V['hydro'], V['sinks_ex'], V['lidar_ex1'], V['dial']

def lid(K, z, bm, bp, T): return K / z**2 * (bm + bp) * T**2
def lid2(K, z, bm, bp, tau): return K / z**2 * (bm + bp) * math.exp(-2 * tau)   # second implementation
def ang(t1, l1, t2, l2): return math.log(t1 / t2) / math.log(l2 / l1)
def doppler(nu, T, m): return nu / C_ * math.sqrt(2 * math.log(2) * KB_ * T / (m * 1.66053907e-27))

# ---------- numbers shared ----------
p3 = 1013.25 * math.exp(-3 / HY['H_km'])
slant = 0.3 / math.cos(math.radians(45)); Tsl = math.exp(-slant)
wien_sun, wien_earth = 2898 / 5778, 2898 / 288
kc, kd, ko = 1 / (6 / 24), 1 / 3.0, 24 / (50 / 10)          # chem 6 h, rain 3 d, outflow 50 km at 10 km/h
kt = kc + kd + ko; assert abs(1 / kt - 1 / (1 / (6 / 24) + 1 / 3.0 + 1 / ((50 / 10) / 24))) < 1e-12
x_soot, x_drop = 2 * math.pi * 0.1 / 0.55, 2 * math.pi * 10 / 0.55
al_f = ang(0.40, 440, 0.10, 870); t550 = 0.40 * (550 / 440) ** (-al_f)
amf = 1 / math.cos(math.radians(60)) + 1 / math.cos(math.radians(30)); vcd = (8e15 - 3e15) / amf; Dd = 1.5e-19 * 2e16
tir = V['tir']
# lidar variant (paper 4)
K2_, bm2 = 2e5, 1e-6
a2, b2, c2 = lid(K2_, 2e3, bm2, 4e-6, 0.6), lid(K2_, 5e3, bm2, 20e-6, 0.4), lid(K2_, 10e3, bm2, 0.1e-6, 0.25)
assert abs(a2 - lid2(K2_, 2e3, bm2, 4e-6, -math.log(0.6))) < 1e-15 * a2
f1 = math.exp(-2 * 1.0)
al4 = abs(math.log((12 * 9) / (12 * 10))) / (2 * 300)
# drill
d1 = 1.2e-19 * 3e11 * 2e5
d3 = 1 / (2.4e-13 * 1.5e6)
d6 = ang(0.30, 500, 0.10, 870); d6b = 0.30 * (675 / 500) ** (-d6)
d7a, d7b = 2 * math.pi * 0.3 / 0.55, 2 * math.pi * 0.3 / 1.6
d9a = 1 / math.cos(math.radians(50)) + 1 / math.cos(math.radians(20)); d9v = (6e15 - 2e15) / d9a
d10 = doppler(2150, 250, 28.01)
d8 = 2898 / 255; d8m = 5.670374419e-8 * 255**4

def P(text, lv, ids): return (text, lv, ids)
PAPERS = []

# =================== PAPER 2 ===================
PAPERS.append(dict(id='P2', title='Paper 2 — Foundations (Start here, Part A and Part B)', minutes=90, intro='Eight questions on the Big 12 core: hydrostatic law, Beer–Lambert, photon budget, Kirchhoff and Planck, lifetime, ozone chemistry, scattering regimes and averaging kernels.', Q=[
 dict(n=1, ref='pb', pts=2.5, parts=[
   P('(a) State the hydrostatic law and the isothermal pressure profile. Give the scale height H for T = 284 K.', 'A', ['R3']),
   P('(b) Compute the pressure at 3 km and compare with the observed 700 hPa.', 'A', ['R3']),
   P('(c) Explain how the pressure profile gives information on altitude in a spectrum.', 'B', ['R3', 'C3'])],
   key=['(a) dp/dz = −ρg, ρ = pM/(RT) ⇒ p = p₀exp(−z/H), H = RT/(Mg) = 8.314×284/(29×10⁻³×9.81) ≈ %.1f km.' % HY['H_km'],
        '(b) p(3 km) = 1013.25·exp(−3/%.2f) = %.0f hPa; observed 700 hPa (error %.1f%%).' % (HY['H_km'], p3, abs(p3 - 700) / 7),
        '(c) Pressure broadening (Lorentz HWHM ∝ p) makes line wings come from low altitude and line centres from high altitude; the O₂ A band uses the known O₂ profile.']),
 dict(n=2, ref='pa', pts=2.5, parts=[
   P('(a) Write the Beer–Lambert law with the optical depth and transmittance.', 'A', ['F1']),
   P('(b) A layer has vertical optical depth 0.3 and the Sun is at a zenith angle of 45°. Compute the slant optical depth and the direct transmission.', 'A', ['F1']),
   P('(c) In τ = σ·N·L which quantity is the unknown for a remote-sensing retrieval and where do the others come from?', 'A', ['F1', 'K1'])],
   key=['(a) I = I₀e^(−τ), τ = ∫k_ext ds = σNL; t = I/I₀ = e^(−τ).', '(b) τ_slant = 0.3/cos 45° = %.3f; t = e^(−%.3f) = %.3f (%.0f%%).' % (slant, slant, Tsl, Tsl * 100),
        '(c) N: σ comes from spectroscopy (HITRAN, lab cross-sections) and L from the viewing geometry.']),
 dict(n=3, ref='pa', pts=2.5, parts=[
   P('(a) List three gains and two losses of photons along the line of sight.', 'A', ['R1']),
   P('(b) Does scattering destroy photons? Justify.', 'A', ['R1']),
   P('(c) For an opaque gas (τ ≫ 1) and for a transparent gas (τ ≪ 1), what does a thermal-IR sensor see?', 'A', ['F2'])],
   key=['(a) Gains: surface reflection, scattering into the line of sight (single, multiple), thermal emission. Losses: absorption, scattering out of the field of view.', '(b) No: scattering redirects a photon (loss for one direction, gain for another). Absorption converts the energy into heat.',
        '(c) Opaque: only the top layers (e^(−τ(l,L)) small below), saturation. Transparent: I ≈ I(0) + τB, a small emission added to the background.']),
 dict(n=4, ref='m2', pts=2.5, parts=[
   P('(a) State Kirchhoff’s law and the condition for its validity.', 'A', ['R2']),
   P('(b) Compute the wavelength of maximum emission of the Sun (5778 K) and the Earth (288 K).', 'A', ['R2']),
   P('(c) Why does thermal-IR sounding need a thermal contrast between the layer and its background?', 'A', ['R2', 'F2'])],
   key=['(a) ε_λ = α_λ in local thermodynamic equilibrium: what absorbs at λ also emits B_λ(T) there.', '(b) Wien: λmax = 2898/T: Sun %.2f µm, Earth %.2f µm.' % (wien_sun, wien_earth),
        '(c) The layer emits B(T_layer) and attenuates the background B(T_s): if T_layer = T_s the two cancel and the layer is invisible; a cold high layer gives a large signal.']),
 dict(n=5, ref='m1', pts=2.5, parts=[
   P('(a) Define the atmospheric lifetime and the rule for several sinks.', 'A', ['C1']),
   P('(b) A pollutant in a 50 km city is removed by chemistry (τ = 6 h), rain once every 3 days and outflow with a 10 km/h wind. Compute the total loss rate, the lifetime and the share of each pathway.', 'A', ['C1']),
   P('(c) What does this lifetime imply for the satellite map of this pollutant?', 'A', ['C1'])],
   key=['(a) τ = burden/loss rate = 1/k; 1/τ = Σ 1/τᵢ (rates add).', '(b) k_chem = %.1f d⁻¹, k_dep = %.2f d⁻¹, τ_out = 5 h ⇒ k_out = %.1f d⁻¹; k_tot = %.2f d⁻¹ ⇒ τ = %.1f h; shares: outflow %.0f%%, chemistry %.0f%%, rain %.0f%%.' % (kc, kd, ko, kt, 24 / kt, ko / kt * 100, kc / kt * 100, kd / kt * 100),
        '(c) A few hours: removed or exported before mixing → hotspot over the source with a short downwind plume.']),
 dict(n=6, ref='pb', pts=2.5, parts=[
   P('(a) Write the NOx cycle that produces ozone in the troposphere and give the wavelength threshold.', 'A', ['K1', 'R1']),
   P('(b) Why is there no net ozone production without VOC, and what changes this?', 'B', ['R1']),
   P('(c) Explain NOx-limited and VOC-limited regimes and titration.', 'B', ['C1'])],
   key=['(a) NO₂ + hν (λ < 424 nm) → NO + O; O + O₂ + M → O₃; NO + O₃ → NO₂ + O₂.', '(b) NO re-destroys the ozone formed (zero balance); peroxy radicals RO₂/HO₂ from VOC oxidise NO to NO₂ without using O₃ ⇒ net production.',
        '(c) NO-poor air: NOx ↑ ⇒ O₃ ↑ (NOx-limited). NO-rich air (near sources): NOx ↑ ⇒ radical loss and titration NO + O₃ ⇒ O₃ ↓ (VOC-limited).']),
 dict(n=7, ref='m7', pts=2.5, parts=[
   P('(a) Compute the size parameter at 0.55 µm for a soot particle r = 0.1 µm and for a cloud droplet r = 10 µm. Give the regimes.', 'A', ['C2']),
   P('(b) By what factor is 400 nm light scattered more than 650 nm light by air molecules?', 'A', ['C2']),
   P('(c) AOD is 0.40 at 440 nm and 0.10 at 870 nm. Compute the Ångström exponent, the AOD at 550 nm and say what particles dominate.', 'A', ['C2', 'F1', 'C3'])],
   key=['(a) x = 2πr/λ: soot %.2f (Mie), droplet %.0f (geometric optics limit, upper Mie).' % (x_soot, x_drop), '(b) (650/400)⁴ = %.2f ≈ 7 (Rayleigh, σ ∝ λ⁻⁴).' % ((650 / 400)**4),
        '(c) α = ln(0.40/0.10)/ln(870/440) = %.2f; AOD(550) = 0.40·(550/440)^(−%.2f) = %.3f; α ≈ 2 ⇒ fine particles (smoke, urban/sulfate).' % (al_f, al_f, t550)]),
 dict(n=8, ref='m5', pts=2.5, parts=[
   P('(a) Write the averaging-kernel relation between the retrieved, the true and the a-priori profiles.', 'A', ['F3']),
   P('(b) A retrieval has diagonal averaging-kernel elements 0.6, 0.3, 0.1 and 0 for four layers. What are the DOFS and what do they tell you?', 'A', ['F3', 'K3']),
   P('(c) How do you compare a chemistry-transport-model profile with this retrieval?', 'A', ['K3', 'F3'])],
   key=['(a) x̂ = xₐ + A(x − xₐ) + Gε, A = GK.', '(b) DOFS = trace(A) = 0.6 + 0.3 + 0.1 + 0 = 1.0: one independent piece of information, essentially a column weighted to the first layers.', '(c) Smooth the model: x_m,s = xₐ + A(x_m − xₐ), then compare with x̂.'])]))

# =================== PAPER 3 ===================
PAPERS.append(dict(id='P3', title='Paper 3 — Retrieval, ozone and aerosol case studies', minutes=90, intro='Eight questions on DOAS, the cost function, averaging kernels and DOFS, ozone from IASI and GOME-2, AAI and look-up tables, aerosol types, 3D aerosols and thermal-IR dust height.', Q=[
 dict(n=1, ref='m3', pts=2.5, parts=[
   P('(a) A DOAS fit gives a slant column 8×10¹⁵ molecules cm⁻² of which 3×10¹⁵ is stratospheric. For θ₀ = 60° and θ = 30°, compute the geometric AMF and the tropospheric vertical column.', 'A', ['K3', 'F1']),
   P('(b) With σ′ = 1.5×10⁻¹⁹ cm² and SCD = 2×10¹⁶ cm⁻², compute the differential optical depth.', 'A', ['C3', 'F1']),
   P('(c) Why must the AMF be computed with a radiative-transfer model rather than the geometric formula?', 'B', ['K3'])],
   key=['(a) AMF ≈ 1/cos 60° + 1/cos 30° = %.3f; VCD = (8 − 3)×10¹⁵/%.3f = %.2f×10¹⁵ molecules cm⁻².' % (amf, amf, vcd / 1e15), '(b) D = σ′·SCD = %.1e (0.3%% of the signal).' % Dd,
        '(c) The AMF depends on the vertical profile of the absorber, clouds, aerosols and surface albedo; the geometric formula assumes a thin layer high above all scatterers.']),
 dict(n=2, ref='pc', pts=2.5, parts=[
   P('(a) Write the least-squares cost function and name each term.', 'A', ['F3']),
   P('(b) Why is the retrieval iterated and what is the Jacobian?', 'B', ['F3']),
   P('(c) Name the inputs of the forward model.', 'B', ['K1'])],
   key=['(a) J(x) = [y − F(x)]ᵀS_y⁻¹[y − F(x)] + [x − xₐ]ᵀR[x − xₐ]: weighted spectral misfit + constraint toward the a priori (ill-posed).', '(b) F is non-linear in x, so K = ∂F/∂x (sensitivity of the spectrum to the state) is recomputed at each iterate (Gauss–Newton).', '(c) Geometry, T and P profiles, spectroscopic parameters (HITRAN/GEISA), surface properties.']),
 dict(n=3, ref='pc', pts=2.5, parts=[
   P('(a) IASI ozone over land has DOFS ≈ 0.6 up to 6 km and ≈ 1.2 up to 12 km. Interpret.', 'A', ['K3']),
   P('(b) Below 3 km the DOFS are 0.25 (IASI) and 0.35 (IASI+GOME-2) over land. Compute the gain; the height of maximum sensitivity goes from 3.0 to 2.2 km — by how much?', 'A', ['K3']),
   P('(c) Explain how the multispectral retrieval is obtained.', 'B', ['F3', 'K2'])],
   key=['(a) About one independent piece of information in the whole troposphere: it can separate lower from upper troposphere only under favourable thermal conditions.', '(b) 0.35/0.25 − 1 = 40%; 3.0 − 2.2 = 0.8 km = 800 m lower.', '(c) One ozone profile (plus instrument parameters) is fitted to the co-located IR and UV spectra by minimising both residuals simultaneously.']),
 dict(n=4, ref='pc', pts=2.5, parts=[
   P('(a) Compare the sensitivity of UV reflectance and thermal-IR radiance to ozone.', 'B', ['K2']),
   P('(b) Give the main characteristics of IASI and GOME-2.', 'C', ['K2']),
   P('(c) How was IASI+GOME-2 validated and what skill was found?', 'C', ['K3'])],
   key=['(a) UV: stratosphere and total column (tropospheric column up to ≈ 12 km with GOME); IR: free troposphere with a maximum near 3 km.', '(b) IASI: thermal IR, 25 km at nadir, swath ≈ 2000 km, 0.5 cm⁻¹; GOME-2: UV–vis, 40×80 km², swath ≈ 1920 km, ≈ 0.24 nm; two overpasses per day.', '(c) 105 ozonesondes (10 European stations, summer 2009): mean bias ≈ 1%, RMS 17–22%, R 0.76–0.84 after smoothing with the averaging kernels.']),
 dict(n=5, ref='m6', pts=2.5, parts=[
   P('(a) What does AAI > 0.5 indicate and why is it not an AOD?', 'B', ['C3', 'K3']),
   P('(b) Why does AOD retrieval over dark surfaces use look-up tables?', 'B', ['K1']),
   P('(c) Why is a desert harder than the ocean in the visible?', 'B', ['R1', 'C2'])],
   key=['(a) Absorbing aerosols (dust, smoke, ash), mostly elevated; it is a residual that depends on SSA, AOD and height.', '(b) Full radiative transfer for each pixel is too slow; LUTs store pre-computed reflectance per aerosol type, geometry and wavelength.', '(c) The surface reflectance of a desert is large and masks the aerosol term; over dark ocean the aerosol dominates the TOA signal.']),
 dict(n=6, ref='m6', pts=2.5, parts=[
   P('(a) Smoke has AOD 0.80 at 440 nm and 0.20 at 870 nm; dust 0.50 and 0.45. Compute the Ångström exponents.', 'A', ['C2', 'F1']),
   P('(b) Which particles are fine and which coarse? Give the physical reason.', 'A', ['C2']),
   P('(c) Why does the AOD of coarse dust hardly depend on wavelength?', 'A', ['C2'])],
   key=['(a) α_smoke = ln(0.8/0.2)/ln(870/440) = %.2f; α_dust = ln(0.50/0.45)/ln(870/440) = %.2f.' % (ang(0.8, 440, 0.2, 870), ang(0.5, 440, 0.45, 870)), '(b) Smoke is fine (α ≈ 2, r ≈ 0.1 µm, x ≈ 1); dust is coarse (α ≈ 0.2, r ≈ 1 µm, x ≫ 1).', '(c) For x ≫ 1, Q_ext → 2 whatever λ is, so τ ≈ πr²·2·N·L is independent of λ.']),
 dict(n=7, ref='pc', pts=2.5, parts=[
   P('(a) How does AEROIASI retrieve dust and how was it validated?', 'B', ['K2', 'C3']),
   P('(b) How does the O₂ A band give aerosol height (AEROS5P)?', 'B', ['R3', 'C3']),
   P('(c) Give one result from each method.', 'C', ['K2'])],
   key=['(a) 12 micro-windows at 8–12 µm of cloud-free IASI spectra, Tikhonov–Phillips; AERONET: bias < 1%, R = 0.76; CALIOP height: bias < 110 m, R = 0.95.', '(b) O₂ is well mixed; a high scattering layer shortens the photon path, so absorption in the band is weaker; band depth/shape ↔ layer pressure.', '(c) AEROIASI: March 2008 plume at 2–3 km above Beijing mixed to the surface by 3 March. AEROS5P: smoke injected up to 7 km.']),
 dict(n=8, ref='m8', pts=2.5, parts=[
   P('(a) A dust layer (τ = 0.5 at 10 µm) lies at 1 km or 5 km over a 300 K surface. Using the simple model, give the brightness-temperature depression for each.', 'B', ['R2', 'R3']),
   P('(b) Explain the result physically and say when the method fails.', 'A', ['R2', 'R3']),
   P('(c) Name another passive technique that gives plume height.', 'C', ['K2'])],
   key=['(a) Python (model: no scattering, T_layer = T_s − 6.5 K/km): ΔBT(1 km) = %.2f K; ΔBT(5 km) = %.2f K.' % (tir['z1']['dBT'], tir['z5']['dBT']), '(b) The 5 km layer is colder, so thermal contrast with the surface is larger. It fails with low contrast: low layers, night inversions, cold surfaces.', '(c) Multi-angle stereo (MISR), UV aerosol-index height sensitivity, O₂–O₂ band at 477 nm.'])]))

# =================== PAPER 4 ===================
PAPERS.append(dict(id='P4', title='Paper 4 — Lidar and integration', minutes=90, intro='Eight questions on active remote sensing: principle, range, lidar equation, detection range, DIAL, instrument choice and a synthesis question.', Q=[
 dict(n=1, ref='pl', pts=2.5, parts=[
   P('(a) Give two advantages and two limitations of a satellite lidar compared with a passive radiometer.', 'B', ['K2']),
   P('(b) A pulse returns after 20 µs. How far is the scatterer?', 'A', ['K1']),
   P('(c) A 30 ns pulse is emitted. What is the range ambiguity?', 'A', ['K1'])],
   key=['(a) Advantages: direct range, vertical profile at high resolution, particle properties. Limits: only along the laser line (no scanning), one or a few wavelengths.', '(b) R = ct/2 = 3×10⁸ × 20×10⁻⁶ / 2 = 3 km.', '(c) ΔR = cτ_L/2 = %.1f m.' % (C_ * 30e-9 / 2)]),
 dict(n=2, ref='pl', pts=2.5, parts=[
   P('(a) Write the lidar equation and define every term with units.', 'A', ['F1']),
   P('(b) Why is the transmission squared?', 'A', ['F1']),
   P('(c) Sketch the signal versus distance and explain its shape.', 'B', ['F1', 'R1'])],
   key=['(a) P(z) = K/z²·β(z)·T²(z); P in W, K in W m³ sr, β = β_m + β_p in m⁻¹ sr⁻¹, T = exp(−∫α dz) dimensionless.', '(b) The pulse crosses the same path out and back: T² = exp(−2τ) (Beer–Lambert twice).', '(c) Rise from the beam/telescope overlap, then decline from 1/z² and transmission; peaks at layers (clouds, aerosol); noise from the radiometric background.']),
 dict(n=3, ref='pl', pts=2.5, parts=[
   P('(a) K = 2×10⁵ W m³ sr, β_m = 10⁻⁶ m⁻¹ sr⁻¹, limit 1 nW. A particle layer at 2 km (β_p = 4×10⁻⁶, T = 0.6) and a water cloud at 5 km (β_p = 20×10⁻⁶, T = 0.4): signals and detection?', 'A', ['F1']),
   P('(b) A sub-visible cirrus at 10 km (β_p = 0.1×10⁻⁶, T = 0.25): signal and detection?', 'A', ['F1']),
   P('(c) A cloud of optical thickness 1.0 forms at 1 km. Recompute the three signals.', 'A', ['F1', 'R1'])],
   key=['(a) P = K β T²/z²: layer %.0f nW (detected); cloud %.1f nW (detected).' % (a2 * 1e9, b2 * 1e9), '(b) %.3f nW → not detected.' % (c2 * 1e9),
        '(c) Extra factor e^(−2×1.0) = %.3f: layer %.1f nW (detected), cloud %.2f nW (detected), cirrus %.4f nW (not).' % (f1, a2 * 1e9 * f1, b2 * 1e9 * f1, c2 * 1e9 * f1)]),
 dict(n=4, ref='pl', pts=2.5, parts=[
   P('(a) Derive the DIAL expression for the water-vapour extinction coefficient.', 'B', ['C3', 'F1']),
   P('(b) P_ON = 12 and 9 nW, P_OFF = 12 and 10 nW at r₁ and r₂ = r₁ + 300 m. Compute α and q (q = 5×10⁴ α).', 'A', ['C3']),
   P('(c) Why must the ON and OFF wavelengths be close?', 'B', ['C3'])],
   key=['(a) ln of the lidar equation at ON and OFF at r₁, r₂; K and 1/z² cancel; β equal at close λ; α_H₂O = (1/2Δr) ln[P_OFF(r₁)P_ON(r₂)/(P_ON(r₁)P_OFF(r₂))].', '(b) ln(0.9) = −0.1054 ⇒ α = 0.1054/(2×300) = %.2e m⁻¹; q = %.2f g/kg.' % (al4, 5e4 * al4), '(c) So that β, particle extinction and molecular extinction are the same at both and cancel; only the gas absorption differs.']),
 dict(n=5, ref='m6', pts=2.5, parts=[
   P('(a) Compare MODIS and CALIOP for a Saharan dust plume.', 'B', ['K2']),
   P('(b) What does AEROIASI add?', 'B', ['K2']),
   P('(c) What information is carried by the depolarisation of the backscattered light?', 'B', ['C2'])],
   key=['(a) MODIS: wide swath, daily AOD map, size information, no altitude, daytime only. CALIOP: vertical profile, day and night, depolarisation; narrow curtain, 16-day revisit.', '(b) 3D dust for every cloud-free IASI pixel, day and night, with a wide swath (validated against CALIOP height bias < 110 m).', '(c) Non-spherical particles (dust, ice) depolarise; spherical droplets and fine aerosol do not.']),
 dict(n=6, ref='p0', pts=2.5, parts=[
   P('(a) Which tool would you use to monitor the long-term trend of stratospheric ozone? Justify.', 'B', ['K2']),
   P('(b) ... to map NO₂ emissions of individual cities? Justify.', 'B', ['K2']),
   P('(c) ... to follow the diurnal evolution of the boundary-layer height, and ... to see dust height over the ocean at night?', 'B', ['K2'])],
   key=['(a) Solar occultation: self-calibrating (I/I₀), high vertical resolution.', '(b) Nadir UV–visible + DOAS: km-scale horizontal resolution, daily coverage, sensitivity to the boundary layer.', '(c) Ground-based lidar (continuous profile of backscatter); thermal-IR retrieval (AEROIASI) or CALIOP at night.']),
 dict(n=7, ref='p0', pts=2.5, parts=[
   P('(a) Show that the lidar signal is an application of the radiative transfer equation (which terms are kept?).', 'B', ['F2', 'R1']),
   P('(b) Which Big-12 formula governs the lidar transmission, the AOD and the DOAS differential optical depth?', 'A', ['F1']),
   P('(c) Why does the thermal-IR method need a contrast, while the lidar does not?', 'B', ['R2', 'K2'])],
   key=['(a) dI/dl = −k_ext I + J with J = backscattered photons from the laser; the loss term gives T², the source term gives β; thermal emission is negligible.', '(b) Beer–Lambert I = I₀e^(−τ), τ = σNL.', '(c) TIR relies on the emission B(T) of the layer versus the background; the lidar supplies its own light.']),
 dict(n=8, ref='p0', pts=2.5, parts=[
   P('(a) Outline how a satellite tropospheric NO₂ column is derived (chain of the Big 12).', 'B', ['K1', 'F1', 'C3']),
   P('(b) State three limitations of the product.', 'B', ['K3']),
   P('(c) How would you validate it and compare it with a model?', 'B', ['K3', 'F3'])],
   key=['(a) Nadir UV–vis spectrum → DOAS fit (σ′, polynomial) → slant column → remove stratosphere → divide by the tropospheric AMF (radiative transfer; profile, cloud, albedo) → vertical column.', '(b) AMF depends on the assumed profile, clouds and aerosols; weak sensitivity near the surface; short lifetime ⇒ strong local variability.', '(c) Compare with ground-based DOAS/in-situ data, and smooth the model with the averaging kernels (or AMF recalculated with the model profile) before comparing.'])]))

# =================== PAPER 5 : calculation drill ===================
PAPERS.append(dict(id='P5', title='Paper 5 — Calculation drill', minutes=60, intro='Ten short numerical questions (two parts each). Calculator allowed. Every result was recomputed in Python.', Q=[
 dict(n=1, ref='pa', pts=2.5, parts=[P('(a) σ = 1.2×10⁻¹⁹ cm², N = 3×10¹¹ cm⁻³, L = 2 km. Compute τ.', 'A', ['F1']), P('(b) Compute the transmission and say whether the gas is optically thin.', 'A', ['F1'])],
   key=['(a) τ = σNL = 1.2×10⁻¹⁹ × 3×10¹¹ × 2×10⁵ = %.1e.' % d1, '(b) t = e^(−τ) = %.4f (99.3%%): optically thin, I ≈ I(0) + τB.' % math.exp(-d1)]),
 dict(n=2, ref='m2', pts=2.5, parts=[P('(a) τ_vertical = 0.8, θ = 70°. Slant τ?', 'A', ['F1']), P('(b) Direct transmission?', 'A', ['F1'])],
   key=['(a) 0.8/cos 70° = %.3f.' % (0.8 / math.cos(math.radians(70))), '(b) e^(−%.3f) = %.3f.' % (0.8 / math.cos(math.radians(70)), math.exp(-0.8 / math.cos(math.radians(70))))]),
 dict(n=3, ref='m1', pts=2.5, parts=[P('(a) k = 2.4×10⁻¹³ cm³ s⁻¹, [OH] = 1.5×10⁶ cm⁻³. Lifetime of the species in days?', 'A', ['C1']), P('(b) Another sink with τ = 20 d acts in parallel. Total lifetime?', 'A', ['C1'])],
   key=['(a) τ = 1/(k[OH]) = %.2e s = %.1f d.' % (d3, d3 / 86400), '(b) 1/τ = 1/%.1f + 1/20 ⇒ τ = %.1f d.' % (d3 / 86400, 1 / (86400 / d3 + 1 / 20))]),
 dict(n=4, ref='m1', pts=2.5, parts=[P('(a) Wind 4 m/s and lifetime 3 h. E-folding length of a plume?', 'A', ['C1']), P('(b) What lifetime gives an e-folding length of 100 km at 5 m/s?', 'A', ['C1'])],
   key=['(a) L = Uτ = 4 × 10 800 = %.1f km.' % (4 * 10800 / 1e3), '(b) τ = L/U = 100 000/5 = 20 000 s = %.1f h.' % (1e5 / 5 / 3600)]),
 dict(n=5, ref='m6', pts=2.5, parts=[P('(a) AOD(500 nm) = 0.30 and AOD(870 nm) = 0.10. Ångström exponent?', 'A', ['C2']), P('(b) AOD at 675 nm?', 'A', ['C2'])],
   key=['(a) α = ln 3/ln(870/500) = %.2f.' % d6, '(b) 0.30 × (675/500)^(−%.2f) = %.3f.' % (d6, d6b)]),
 dict(n=6, ref='m7', pts=2.5, parts=[P('(a) r = 0.3 µm. Size parameter at 0.55 µm and at 1.6 µm?', 'A', ['C2']), P('(b) Which regime is each, and which wavelength is scattered more efficiently?', 'A', ['C2'])],
   key=['(a) x = %.2f and %.2f.' % (d7a, d7b), '(b) Both are in the Mie regime (x ≈ 1–3); the shorter wavelength has the larger x and larger extinction.']),
 dict(n=7, ref='m2', pts=2.5, parts=[P('(a) T = 255 K. Wien wavelength?', 'A', ['R2']), P('(b) Stefan–Boltzmann emittance?', 'A', ['R2'])],
   key=['(a) 2898/255 = %.2f µm.' % d8, '(b) σT⁴ = 5.67×10⁻⁸ × 255⁴ = %.0f W m⁻².' % d8m]),
 dict(n=8, ref='m3', pts=2.5, parts=[P('(a) θ₀ = 50°, θ = 20°: geometric AMF?', 'A', ['K3']), P('(b) SCD = 6×10¹⁵ with 2×10¹⁵ stratospheric. Tropospheric VCD?', 'A', ['K3', 'F1'])],
   key=['(a) 1/cos 50° + 1/cos 20° = %.3f.' % d9a, '(b) (6 − 2)×10¹⁵/%.3f = %.2e molecules cm⁻² (≈ %.2f DU).' % (d9a, d9v, d9v / 2.687e16)]),
 dict(n=9, ref='pa', pts=2.5, parts=[P('(a) Doppler HWHM of CO (28.01 u) at 2150 cm⁻¹ and 250 K?', 'B', ['R3']), P('(b) Does it depend on pressure? Which broadening dominates near the ground?', 'A', ['R3'])],
   key=['(a) (ν̃/c)√(2 ln2 k_B T/m) = %.4f cm⁻¹.' % d10, '(b) No (temperature only). Near the ground the Lorentz (pressure) width dominates; the crossover is near 20 km.']),
 dict(n=10, ref='pl', pts=2.5, parts=[P('(a) K = 10⁵ W m³ sr, β_m = 10⁻⁶, β_p = 5×10⁻⁶ m⁻¹ sr⁻¹ at 1.5 km, T = 0.8. Signal in nW?', 'A', ['F1']), P('(b) Detected with a 1 nW limit? What if the layer is at 6 km with T = 0.5?', 'A', ['F1'])],
   key=['(a) P = 10⁵/(1500)² × 6×10⁻⁶ × 0.64 = %.1f nW.' % (lid(1e5, 1500, 1e-6, 5e-6, 0.8) * 1e9), '(b) Yes. At 6 km: %.2f nW (still detected, > 1 nW).' % (lid(1e5, 6000, 1e-6, 5e-6, 0.5) * 1e9)])]))
