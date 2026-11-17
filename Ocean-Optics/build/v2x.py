# -*- coding: utf-8 -*-
"""Study guide v2 additions for chapters 1-8: worked example, quick Q&A, memory hooks, extra figures/photos, extra questions."""
from lib import *
V = VERIFIED
P = V['plume72']; OZ = V['ozone']; MC = V['megacity']; LM = V['limb']; TL = V['two_layer']
AS = V['ang_smoke']; AD = V['ang_dust']; DR = V['droplet']; T3 = V['tir310']; O8 = V['o2_scale8']
SRC = 'Study guide v2, worked example'

def we(title, items): return title, '<ol class="steps">' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'

DATA = {
 'm1': dict(we=we('lifetime of NO₂ from a satellite plume', [
        f'TROPOMI NO₂ line density downwind of a power plant falls to 1/e at x = {P["x_km"]} km; wind U = 5 m/s = {P["U_kmh"]:.0f} km/h.', f'τ = x / U = {P["x_km"]} / {P["U_kmh"]:.0f} = <b>{P["tau_h"]:.0f} hours</b> — a typical daytime NO₂ lifetime.',
        'The same SO₂ molecule lives ~1–2 days in the boundary layer but months in the stratosphere after a volcanic eruption (no rain, little cloud chemistry): lifetime depends on where the molecule is.']),
    qa=[('Why does SO₂ live longer in the stratosphere?', 'No wet deposition, no clouds for aqueous oxidation, slower OH reaction.'), ('Can a short-lived species appear everywhere on a map?', 'Only if its sources are everywhere (e.g. HCHO over all forests): the map still shows sources.'),
        ('What is steady state?', 'Production = loss, burden constant, so τ = M/P = M/L.'), ('Why is CO a good tracer of long-range transport?', 'τ ≈ 2 months: longer than intercontinental transport (1–2 weeks) but shorter than hemispheric mixing, so plumes stay visible.')],
    hooks=[('An ink drop in a stirred tank: if the ink fades in 1 second you only see colour at the spot (short τ → you see the source); if it never fades the whole tank is coloured (long τ → well mixed).', 'Giọt mực trong bể nước đang khuấy.'),
           ('Cigarette smoke in a room with an extractor fan: a strong fan (strong sink) keeps smoke around the smoker; switch it off and smoke fills the room.', 'Khói thuốc trong phòng có quạt hút.')],
    mcq=[('A TROPOMI NO₂ line density falls to 1/e at x = 72 km downwind of a power plant; the wind is 18 km/h. What is the NO₂ lifetime?', f'{P["tau_h"]:.0f} hours', ['1 hour', '16 hours', '1 296 hours'], 'τ = x/U = 72 km / 18 km h⁻¹ = 4 h. Guide v2 worked example.', 2, 'Calculation'),
         ('Why is CO a good tracer of long-range transport?', 'Its lifetime (~2 months) is longer than intercontinental transport (1–2 weeks) but shorter than hemispheric mixing, so plumes remain visible', ['Its lifetime is a few hours, so it marks only the source', 'Its lifetime is a century, so it is perfectly uniform', 'It does not react with OH'], 'Guide v2, Ch.1 Quick Q&A.', 2, 'Orders of magnitude')]),
 'm2': dict(we=we('UV light through the ozone layer', [
        f'Ozone column 300 DU = 300 × 2.69×10¹⁶ ≈ {OZ["column"]:.1e} molecules cm⁻²; sun at 60° + nadir view → air mass ≈ 1/cos 60° + 1 = <b>{OZ["airmass"]:.0f}</b>.',
        f'310 nm: σ ≈ 1×10⁻¹⁹ cm² → τ<sub>slant</sub> ≈ <b>{OZ["310"]["tau"]:.1f}</b> → T = e<sup>−τ</sup> ≈ <b>{OZ["310"]["T"]*100:.0f}%</b>. 330 nm: σ ≈ 1×10⁻²⁰ cm² → τ ≈ {OZ["330"]["tau"]:.2f} → T ≈ <b>{OZ["330"]["T"]*100:.0f}%</b>.',
        'Wavelengths below 300 nm barely reach the ground; the strong change of σ with λ is exactly what gives altitude information (chapter 3).']),
    fig=('f24_o3_transmission', 'Figure 20 (study guide v2): transmittance through ozone at four UV wavelengths.'),
    qa=[('Does scattering destroy photons?', 'No: it redirects them — a loss for one direction, a gain for another (Part A.2).'), ('Why is thermal emission negligible in the UV–visible?', 'B(λ, T ≈ 250–300 K) is practically zero below ≈ 3 µm.'),
        ('Single-scattering albedo of pure Rayleigh scattering?', 'ω₀ = 1 (no absorption).'), ('Which gas dominates absorption at 9.6 µm? At 15 µm?', 'O₃ at 9.6 µm, CO₂ at 15 µm.'), ('What does τ = 1 mean physically?', 'The beam is reduced to 1/e ≈ 37%: the “depth” from which most photons come.')],
    hooks=[('Absorption is a toll booth keeping the money (energy becomes heat); scattering is a traffic officer sending cars down another road (cars are not lost); emission is new cars joining from a side road.', 'Hấp thụ = trạm thu phí; tán xạ = cảnh sát giao thông; phát xạ = xe mới nhập vào.'),
           ('Beer–Lambert: each km of fog stops the same fraction of the cars still left, not the same number → exponential decrease.', 'Mỗi km sương mù chặn cùng một tỉ lệ số xe còn lại.')],
    photos=['s4_solar', 's6_gains_losses', 's5_rte_equation'],
    mcq=[('A 300 DU ozone column is viewed with the sun at 60° and a nadir view. What is the air mass used in the guide’s worked example?', f'≈ {OZ["airmass"]:.0f} (1/cos 60° + 1)', ['≈ 1', '≈ 2.5', '≈ 6'], 'Slant path in: 1/cos 60° = 2; out: 1 (nadir) → 3. Guide v2 worked example.', 2, 'Beer–Lambert'),
         ('With that air mass, what fraction of 310 nm light (σ ≈ 1×10⁻¹⁹ cm²) is transmitted through 300 DU of ozone?', f'≈ {OZ["310"]["T"]*100:.0f}%', ['≈ 79%', '≈ 50%', '≈ 0.1%'], f'τ = σ·N·AMF = 1×10⁻¹⁹ × 8.06×10¹⁸ × 3 = {OZ["310"]["tau"]:.2f}; T = e^(−τ) = {OZ["310"]["T"]:.3f} (Python). At 330 nm (σ ≈ 1×10⁻²⁰) T ≈ {OZ["330"]["T"]*100:.0f}%.', 2, 'Beer–Lambert'),
         ('Which gas dominates absorption at 9.6 µm and which at 15 µm?', 'O₃ at 9.6 µm; CO₂ at 15 µm', ['CO₂ at 9.6 µm; O₃ at 15 µm', 'H₂O at both', 'CH₄ at 9.6 µm; N₂O at 15 µm'], 'Guide v2, Ch.2 Quick Q&A.', 1, 'Absorption')]),
 'm3': dict(we=we('tropospheric NO₂ column over a megacity', [
        f'DOAS fit gives a tropospheric slant column SCD<sub>trop</sub> = 2.4×10¹⁶ molecules cm⁻²; radiative transfer gives AMF<sub>trop</sub> = 1.2.', f'VCD = SCD / AMF = 2.4×10¹⁶ / 1.2 = <b>2×10¹⁶</b> molecules cm⁻² (≈ <b>{MC["du"]:.2f} DU</b>) — typical of a polluted megacity.',
        f'If clouds or a wrong profile shape change the AMF by 30%, the VCD changes by 30% (e.g. {MC["vcd_amf30"]:.2e} for AMF = 1.56) → the AMF is usually the largest error source.']),
    fig=('f21_doas_principle', 'Figure 10 (study guide v2): DOAS principle — I₀, I′₀ and the differential absorption D.'),
    qa=[('Why measure the solar irradiance I₀ every day?', 'To remove Fraunhofer lines and instrument effects: the ratio I/I₀ is the reflectance.'), ('Why only the differential cross-section?', 'Broad features cannot be separated from Rayleigh, Mie and surface effects; the polynomial absorbs them.'),
        ('How does a limb spectrum change with tangent height?', 'Lower tangent height → more absorber and higher pressure → deeper and wider lines (lecture slide, Part A.5).'), ('What is the Ring effect?', 'Filling-in of Fraunhofer lines by rotational Raman scattering; it must be fitted as a pseudo-absorber in DOAS.'),
        ('What does an optimal-estimation retrieval need besides the spectrum?', 'A forward model, the Jacobian K, an a priori profile x_a and the covariances S_a and S_ε.')],
    hooks=[('SCD is the amount of gas along the slanted light path (a spiral staircase); VCD is the amount straight up (a lift). AMF = the ratio of the two paths.', 'SCD và VCD: cầu thang xoắn và thang máy.'),
           ('Altitude information from the spectrum: strongly absorbing wavelengths are a weak torch in thick fog (it lights only the top layer); weakly absorbing wavelengths are a headlight reaching the bottom.', 'Bước sóng hấp thụ mạnh như đèn pin yếu trong sương dày.')],
    photos=['s1_gome', 's2_tropomi', 's3_wavelengths', 's11_doas', 's10_line_widths'],
    mcq=[('A DOAS fit gives SCD_trop = 2.4×10¹⁶ molecules cm⁻² and the AMF is 1.2. What is the VCD and about how many Dobson Units is it?', f'VCD = 2×10¹⁶ molecules cm⁻² ≈ {MC["du"]:.2f} DU', ['2.9×10¹⁶ molecules cm⁻² ≈ 1.1 DU', '2×10¹⁶ molecules cm⁻² ≈ 7.4 DU', '5×10¹⁵ molecules cm⁻² ≈ 0.19 DU'], f'VCD = 2.4×10¹⁶/1.2 = 2×10¹⁶; ÷ 2.687×10¹⁶ per DU = {MC["du"]:.3f} DU (Python).', 2, 'AMF'),
         ('If clouds change the AMF by 30%, how does the VCD change?', 'By about 30% — the AMF is usually the largest error source', ['By 3%', 'It does not change', 'By a factor of 30'], 'VCD = SCD/AMF is inversely proportional to AMF. Guide v2 worked example.', 2, 'AMF'),
         ('What is the Ring effect in DOAS?', 'Filling-in of Fraunhofer lines by rotational Raman scattering, fitted as a pseudo-absorber', ['Broadening of lines by pressure', 'Reflection of light by cloud rings', 'A polynomial term for the surface albedo'], 'Guide v2, Ch.3 Quick Q&A.', 2, 'DOAS'),
         ('Why does a lower tangent height give deeper and wider lines in a limb spectrum?', 'More absorber along the path and higher pressure (Lorentz broadening)', ['Because the Sun is brighter at low heights', 'Because the Doppler width grows with pressure', 'Because lines move to longer wavelengths'], 'Guide v2, Ch.3 Quick Q&A and Part A.5.', 3, 'Vertical information')]),
 'm4': dict(we=we('why limb sounding has a long path and coarse horizontal resolution', [
        f'Path through a layer of thickness H at the tangent point: L ≈ √(8·R·H). With R = 6371 km and H = 1 km → <b>L ≈ {LM["L"]:.0f} km</b>.', f'Nadir: the same 1 km layer is crossed over ≈ 1 km (× air mass factor) → the limb path is ≈ 100–200 times longer ({LM["ratio"]:.0f}× in this estimate): much stronger signal, but averaged over ≈ 200–300 km horizontally.',
        'Coverage: solar occultation gives ≈ 15 orbits × 2 = ~30 profiles/day; TROPOMI (2600 km swath, 5.5 × 3.5 km² pixels) gives millions of pixels/day.']),
    qa=[('Why can limb sounders not see the boundary layer?', 'Clouds and the very long, opaque path in the lower troposphere block the line of sight.'), ('Why is occultation self-calibrating?', 'The same instrument measures I₀ outside the atmosphere a few minutes earlier; only the ratio I/I₀ is used.'),
        ('Which geometry for CO₂ point sources?', 'Nadir with small pixels (OCO-2, CO2M): sources need horizontal detail.'), ('Why does a geostationary instrument need larger optics?', f'It is ≈ 36 000 km away instead of ≈ 800 km: ≈ {LM["geo_ratio"]:.0f} times further.')],
    hooks=[('Nadir is looking at the bottom of a lake from a boat: you see where things are but not at what depth. Limb is looking sideways through fog at the horizon: you see each layer, but everything along the ray is blended. Occultation is watching the sunset through sunglasses: compare brightness before and during.', 'Nadir như nhìn xuống đáy hồ; limb như nhìn ngang qua lớp sương; che khuất như nhìn mặt trời lặn qua kính râm.')],
    photos=[],
    mcq=[('Estimate the path length through a 1 km thick layer at the tangent point of a limb view (L ≈ √(8·R·H), R = 6371 km).', f'≈ {LM["L"]:.0f} km', ['≈ 1 km', '≈ 71 km', '≈ 6 371 km'], f'L = √(8 × 6371 × 1) = {LM["L"]:.1f} km (Python). About two hundred times the nadir path through the same layer. Guide v2 worked example.', 3, 'Comparison'),
         ('Why does a geostationary instrument need larger optics than a LEO instrument?', f'It is about 36 000 km away instead of ≈ 800 km, i.e. ≈ {LM["geo_ratio"]:.0f} times further', ['It is closer to the Earth', 'It looks through the limb', 'It must observe at night'], 'Guide v2, Ch.4 Quick Q&A.', 2, 'Orbits'),
         ('Why can limb sounders not see the boundary layer?', 'Clouds and the very long, opaque path in the lower troposphere block the line of sight', ['The Sun is too bright there', 'The boundary layer has no gases', 'The Earth’s curvature hides it from every sensor'], 'Guide v2, Ch.4 Quick Q&A.', 2, 'Comparison')]),
 'm5': dict(we=we('one column measurement, two layers', [
        'State x = (x₁, x₂), measurement y = x₁ + x₂ → K = [1 1]; a priori S<sub>a</sub> = I (variance 1), noise S<sub>ε</sub> = 0.01.', f'A = S<sub>a</sub>Kᵀ(K S<sub>a</sub> Kᵀ + S<sub>ε</sub>)⁻¹K = [1 1]ᵀ[1 1] / {TL["denom"]:.2f} ≈ [[{TL["A"][0][0]:.2f}, {TL["A"][0][1]:.2f}], [{TL["A"][1][0]:.2f}, {TL["A"][1][1]:.2f}]].',
        f'DOFS = trace(A) ≈ <b>{TL["dofs"]:.2f}</b> ≈ 1: one column measurement gives one piece of information. Each layer retrieval = half of the total → the layers cannot be separated.']),
    qa=[('A level has an averaging-kernel row with area 0.2: meaning?', '80% of the retrieved value at that level comes from the a priori.'), ('Can an averaging kernel be negative?', 'Yes: oscillations appear when the retrieval sharpens a broad sensitivity.'),
        ('Why not use a very large S_a to reduce the a-priori influence?', 'The retrieval then amplifies noise and oscillates (ill-posed problem).'), ('What does a column averaging kernel > 1 above a cloud mean?', 'Enhanced light path above the bright cloud: the column is over-sensitive at that altitude.')],
    hooks=[('The averaging kernel is a blurred photograph: in an ideal photo every point is sharp (delta function); in a real one each point becomes a smear (broad kernel). DOFS = the number of points you can still tell apart in the blurred photo.', 'Averaging kernel như ảnh chụp bị nhoè.')],
    photos=[],
    mcq=[('A single column measurement y = x₁ + x₂ (K = [1 1]) constrains two layers with S_a = I and S_ε = 0.01. What is DOFS?', f'≈ {TL["dofs"]:.1f}: one independent piece of information, so the two layers cannot be separated', ['≈ 2', '≈ 0', '≈ 4'], f'A = S_a Kᵀ(K S_a Kᵀ + S_ε)⁻¹ K has all elements {TL["A"][0][0]:.4f} (denominator {TL["denom"]:.2f}); trace = {TL["dofs"]:.4f} (Python). Guide v2 worked example.', 2, 'DOFS'),
         ('A kernel row has area 0.2. What does that mean?', '80% of the retrieved value at that level comes from the a priori', ['80% comes from the measurement', 'The noise is 20%', 'The vertical resolution is 0.2 km'], 'Guide v2, Ch.5 Quick Q&A.', 2, 'Averaging kernel'),
         ('Why is a very large S_a not a cure for a-priori influence?', 'The retrieval then amplifies noise and oscillates (ill-posed problem)', ['It makes the kernel an identity matrix', 'It lowers DOFS to zero', 'It removes the smoothing error and the noise error together'], 'Guide v2, Ch.5 Quick Q&A.', 3, 'Averaging kernel')]),
 'm6': dict(we=we('Ångström exponent from two AODs', [
        'α = −ln(τ₁/τ₂) / ln(λ₁/λ₂).', f'Smoke: AOD(440) = 0.8, AOD(870) = 0.2 → α = ln 4 / ln(870/440) = 1.386 / 0.682 ≈ <b>{AS["alpha"]:.1f}</b> → fine particles.', f'Dust: AOD(440) = 0.50, AOD(870) = 0.45 → α = ln 1.11 / 0.682 ≈ <b>{AD["alpha"]:.2f}</b> → coarse particles.']),
    qa=[('Why use the 2.1 µm band over land?', 'Fine aerosols are almost transparent there, and the surface reflectance at 2.1 µm predicts the visible one.'), ('Why does polarisation help?', 'Light scattered by fine particles is strongly polarised while surfaces polarise little → separates aerosol from surface.'),
        ('Can visible passive sensors retrieve aerosols at night?', 'No sunlight → no; only thermal IR (dust) or lidar.'), ('What is the UV Aerosol Index sensitive to?', 'Absorbing aerosols (smoke, dust), even above clouds; it increases with layer height.')],
    hooks=[('Looking for smoke on a dark or a bright background: smoke over a dark lake is easy to see; smoke over white snow is almost invisible (white writing on white paper) — which is why AOD over deserts is hard to measure.', 'Khói trên nền tối dễ thấy, trên tuyết trắng gần như vô hình.')],
    photos=[],
    mcq=[('Smoke has AOD(440) = 0.8 and AOD(870) = 0.2. What is the Ångström exponent?', f'α ≈ {AS["alpha"]:.1f}, fine particles', ['α ≈ 0.15, coarse particles', 'α ≈ 4, molecules', 'α ≈ 0.5'], f'α = ln 4 / ln(870/440) = {AS["alpha"]:.3f} (Python). Guide v2 worked example.', 2, 'Ångström'),
         ('Dust has AOD(440) = 0.50 and AOD(870) = 0.45. What is the Ångström exponent?', f'α ≈ {AD["alpha"]:.2f}, coarse particles', ['α ≈ 2.0, fine particles', 'α ≈ 1.0', 'α ≈ 4'], f'α = ln(0.50/0.45)/ln(870/440) = {AD["alpha"]:.3f} (Python).', 2, 'Ångström'),
         ('Why is the 2.1 µm band used over land?', 'Fine aerosols are almost transparent there and the surface reflectance at 2.1 µm predicts the visible one', ['Because water vapour absorbs strongly there', 'Because dust is invisible at 2.1 µm so it can be masked', 'Because the Sun emits most light there'], 'Guide v2, Ch.6 Quick Q&A.', 2, 'Surface'),
         ('Why does polarisation help separate aerosol from surface?', 'Light scattered by fine particles is strongly polarised while most surfaces polarise little', ['Surfaces polarise more than particles', 'Polarisation removes clouds only', 'Polarisation gives the layer height directly'], 'Guide v2, Ch.6 Quick Q&A.', 3, 'Principle')]),
 'm7': dict(we=we('the same particle in different regimes', [
        f'Cloud droplet r = 10 µm: visible (λ = 0.55 µm) → x ≈ <b>{DR["x_vis"]:.0f}</b> → geometric optics (white clouds).', f'Same droplet seen by a cloud radar (λ = 3 mm) → x ≈ <b>{DR["x_radar"]:.2f}</b> → Rayleigh → radar reflectivity ∝ r⁶ (∝ D⁶).', 'Lesson: the regime depends on the ratio r/λ, not on the particle alone.']),
    qa=[('Why are sunsets red?', 'The long slant path removes blue light by Rayleigh scattering (λ⁻⁴).'), ('Why is polluted haze white-grey?', 'Mie scattering by fine particles depends weakly on λ.'), ('What is the extinction paradox?', 'For x ≫ 1, Q_ext → 2: a large particle removes twice its geometric cross-section (diffraction + geometric part).'), ('Can Mie theory be used for dust?', 'Only approximately: dust is non-spherical → spheroids or T-matrix.')],
    hooks=[('Ocean waves meeting an obstacle: a small bamboo pole (Rayleigh) is passed almost unchanged; a rock the size of a wavelength (Mie) creates complex interference; a long dyke (geometric optics) casts a clear “shadow” behind it.', 'Sóng biển gặp vật cản.')],
    photos=[],
    mcq=[('A cloud droplet with r = 10 µm is seen in visible light (0.55 µm) and by a cloud radar (λ = 3 mm). What are the regimes?', f'Visible: x ≈ {DR["x_vis"]:.0f}, geometric optics; radar: x ≈ {DR["x_radar"]:.2f}, Rayleigh', ['Both Mie', 'Visible: Rayleigh; radar: geometric optics', 'Both geometric optics'], f'x = 2π×10/0.55 = {DR["x_vis"]:.1f}; x = 2π×10/3000 = {DR["x_radar"]:.4f} (Python). The regime depends on r/λ.', 2, 'Size parameter'),
         ('Why are sunsets red?', 'The long slant path removes blue light by Rayleigh scattering (λ⁻⁴)', ['Red light is emitted by the Sun at sunset only', 'Ozone absorbs blue only at sunset', 'Clouds reflect red light'], 'Guide v2, Ch.7 Quick Q&A.', 1, 'Rayleigh'),
         ('Why is polluted haze white-grey?', 'Mie scattering by fine particles depends weakly on wavelength', ['Because haze absorbs all colours equally', 'Because haze emits white light', 'Because Rayleigh scattering dominates'], 'Guide v2, Ch.7 Quick Q&A.', 2, 'Mie'),
         ('Radar reflectivity of raindrops scales as which power of the drop diameter?', 'D⁶ (Rayleigh regime for radar wavelengths)', ['D²', 'D⁴', 'D⁰, independent of size'], 'Rayleigh: σ ∝ r⁶. Guide v2 worked example.', 3, 'Rayleigh')]),
 'm8': dict(we=we('thermal contrast and O₂ path', [
        f'TIR: surface 310 K, dust layer at 4 km → T ≈ 310 − 6.5×4 ≈ <b>{T3["z4"]["Tl"]:.0f} K</b> → contrast ≈ 26 K. The guide quotes a brightness-temperature depression of ≈ 7 K for a 10 µm AOD of 0.7.', 'Same layer at 1 km → contrast ≈ 6.5 K → depression ≈ 2 K (guide): low layers are hard to detect.',
        f'O₂ A-band: fraction of the O₂ column above a layer at z ≈ e<sup>−z/8 km</sup>: 6 km → <b>{O8["6"]:.2f}</b>, 1 km → <b>{O8["1"]:.2f}</b> → a higher layer roughly halves the O₂ absorption seen.',
        f'<i>Check:</i> our blackbody-layer model (no scattering, no water vapour, emissivity 1 − e<sup>−τ</sup>) gives {T3["z4"]["dBT"]:.1f} K at 4 km and {T3["z1"]["dBT"]:.1f} K at 1 km for τ = 0.7 — larger than the guide’s order-of-magnitude numbers, because real dust, water vapour and the atmospheric window reduce the signal. The trend (higher layer → larger depression, about 3–4× between 1 and 4 km) is the same.']),
    qa=[('Why the O₂ A-band and not a H₂O band?', 'O₂ is well mixed with a known profile; H₂O is highly variable.'), ('Why does the TIR method fail at night over deserts?', 'Surface cooling and inversions make the layer as warm as the surface → no thermal contrast.'),
        ('How does a bright surface affect the O₂ A-band method?', 'Many photons reach the surface (long path), diluting the aerosol signal.'), ('How can the passive results be validated?', 'With lidar profiles (CALIOP, EarthCARE, ground lidars).')],
    hooks=[('TIR: guess the height of a mountain from the temperature at its top (the higher, the colder). O₂ band: guess the depth at which light “bounces back” from the amount of O₂ (like ink) it has travelled through.', 'TIR: đoán độ cao ngọn núi bằng nhiệt độ; dải O₂: đoán độ sâu nơi ánh sáng bật lại.')],
    photos=[],
    mcq=[('In the guide’s worked example, what fraction of the O₂ column lies above a layer at 6 km compared with 1 km (e^(−z/8 km))?', f'≈ {O8["6"]:.2f} at 6 km versus ≈ {O8["1"]:.2f} at 1 km: a higher layer roughly halves the O₂ absorption', ['≈ 0.88 at 6 km versus ≈ 0.47 at 1 km', '≈ 1.0 at both', '≈ 0.02 at 6 km versus ≈ 0.5 at 1 km'], f'e^(−6/8) = {O8["6"]:.3f}; e^(−1/8) = {O8["1"]:.3f} (Python).', 2, 'O₂ A-band'),
         ('Why does the TIR method fail at night over deserts?', 'Surface cooling and inversions make the layer as warm as the surface, so there is no thermal contrast', ['Deserts emit no infrared at night', 'Dust disappears at night', 'The O₂ band is too deep at night'], 'Guide v2, Ch.8 Quick Q&A.', 2, 'TIR'),
         ('Why use the O₂ A-band and not an H₂O band for height?', 'O₂ is well mixed with a known profile; H₂O is highly variable', ['H₂O does not absorb in the near-IR', 'O₂ is much more abundant than H₂O in every layer', 'H₂O lines are too narrow'], 'Guide v2, Ch.8 Quick Q&A.', 2, 'O₂ A-band'),
         ('How can passive aerosol-height results be validated?', 'With lidar profiles (CALIOP, EarthCARE, ground lidars)', ['With the same passive sensor on another day', 'With rain gauges', 'They cannot be validated'], 'Guide v2, Ch.8 Quick Q&A.', 1, 'Other')]),
}

def apply(mid, mod, slides, B):
    d = DATA.get(mid)
    if not d: return mod, slides
    for (q, c, w, ex, lv, tp) in d['mcq']:
        B.add(q, c, w, ex, lv, tp, origin='goc', src=SRC + ' / Quick Q&A (study guide v2)')
    t, html = d['we']
    mod['v2'] = dict(we_title=t, we=html, qa=d['qa'], hooks=d['hooks'])
    if d.get('photos'): mod['photos'] = d['photos']
    if d.get('fig'):
        n, cap = d['fig']; mod['v2']['we'] += lfig(n, cap)
    items = [x for x in re.findall(r'<li>(.*?)</li>', html, re.S) if 'Check:' not in x][:3]
    new = [S('Worked example: ' + t, ulb(items, 34, 52)),
           S('Quick Q&A', cards2(560, *[card(q, a) for q, a in d['qa'][:4]], cols=2)),
           ]
    if d.get('fig'): new.insert(1, S('Figure: ' + d['fig'][1].split(':')[0][:30], figfit(d['fig'][0], d['fig'][1], 520)))
    i = next(k for k, s in enumerate(slides) if 'Exam checklist' in s[:300])
    slides = slides[:i] + new + slides[i:]
    return mod, slides
import re
