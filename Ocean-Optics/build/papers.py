# -*- coding: utf-8 -*-
"""Five written papers written for this site (there is NO official exam from the lecturer).
Each part: (text, level A/B/C, [Big-12 ids]). Levels are the author's own assessment. All numbers come from verified.json."""
import math, json, os
_H = os.path.dirname(os.path.abspath(__file__)); _S = os.path.join(_H, '..', 'site')
V = json.load(open(os.path.join(_S if os.path.isdir(_S) else os.path.join(_H, '..'), 'data', 'verified.json')))
BL, cT = V['beer_lambert_T'], V['c_from_T_25cm']
W = V['pure_water_bw']; b37, b0 = W['morel_500_S37']['b_w'], W['morel_500_S0']['b_w']
c443 = V['cdom_ratio_443_from_412_S014']; r350 = V['cdom_ratio_350_over_440_S014']; nr350 = V['nap_ratio_350_over_440_S011']
q = V['bp_440_over_550']; EU = V['euphotic_1pct']; SC = V['secchi_examples']; PK = V['package_Qstar']
cex = V['sum_N_sigma_c_example']; bpc = V['bp550_from_chl']; pm = V['poc_spm_from_ap_ratio']
ti = lambda x: f'{x:.3g}'

PAPERS = [
 dict(id='P1', title='Paper 1 — Light in water and pure water (modules A, B)', minutes=60,
      intro='Four questions on the RTE, IOPs, water types and pure water. Review modules A and B.', Q=[
  dict(n=1, ref='ma', pts=2.5, parts=[
      ('(a) Write the radiative transfer equation of the lecture and name each term.', 'A', ['F1', 'K1']),
      ('(b) Define a, β, b, b_f, b_b and c with their units.', 'A', ['F1']),
      ('(c) State the additivity principle for a, b and b_b and say what it allows.', 'A', ['R1'])],
      key=['(a) dL/dr = −cL + (in-scattering with β) + S; c = a + b: loss by absorption, loss by scattering out, gain by scattering in, S internal source (slide 5).',
           '(b) a (m⁻¹); β (m⁻¹ sr⁻¹); b = 2π∫β sinθ dθ; b_f from 0 to π/2; b_b from π/2 to π; c = a + b (slides 17–18).',
           '(c) a = a_w + a_CDOM + a_ph + a_NAP; b = b_w + b_p; b_b = b_bw + b_bp; allows one model per constituent (slide 19).']),
  dict(n=2, ref='ma', pts=2.5, parts=[
      ('(a) Distinguish IOPs from AOPs, with two examples of each.', 'A', ['C1']),
      ('(b) A student says that ocean colour is the colour of the sea surface seen from a boat. Correct this.', 'B', ['K1']),
      ('(c) A collimated beam travels 1 m in water with c = 0.5 m⁻¹. Which fraction remains?', 'A', ['F1'])],
      key=['(a) IOPs (a, b, β, c): medium only, additive, independent of illumination; AOPs (K_d, R, R_rs): medium + light field (slide 11; textbook).',
           '(b) Sun/sky reflection changes the surface colour but is not ocean-colour radiometry, which comes from photon–constituent interactions in the water (slide 7).',
           f'(c) e^(−0.5) = {math.exp(-0.5):.3f}.']),
  dict(n=3, ref='mb', pts=2.5, parts=[
      ('(a) Write the Morel (1974) VSF of pure sea water and list what changed in Buiteveld et al. (1994).', 'C', ['F3']),
      ('(b) By which factor does pure water scatter more at 450 nm than at 550 nm (exponent −4.32)?', 'B', ['F3', 'R2']),
      ('(c) Explain why the open ocean looks blue using a_w and b_w.', 'B', ['R2'])],
      key=['(a) β_w = 1.38(λ/500)^−4.32(1+0.3S/37)10⁻⁴[1+cos²θ(1−δ)/(1+δ)], δ = 0.09; Buiteveld: 1.29, −4.14, δ = 0.051 (slides 20, 23).',
           f'(b) (550/450)^4.32 = {V["ratio_450_550_morel"]:.2f}.',
           '(c) a_w is minimum in the blue and rises beyond 550 nm (slide 24) while b_w ∝ λ^−4.3: red is absorbed, blue is scattered back (qualitative; slides 24, 20).']),
  dict(n=4, ref='ma', pts=2.5, parts=[
      ('(a) Define Case 1 and Case 2 waters. Why is “Case 2 = coastal” wrong?', 'A', ['C2']),
      ('(b) What do the optical water classes add?', 'B', ['C2', 'K2'])],
      key=['(a) Case 1: determined mainly by phytoplankton and co-varying CDOM/detritus; Case 2: everything else. Slide 15: Case 1 = 81–87 %, Case 2 also at high latitudes.',
           '(b) 17 classes describe the continuum of variability better than two boxes (slide 16); they help choose the right algorithm.'])]),
 dict(id='P2', title='Paper 2 — Absorption (module C)', minutes=60,
      intro='Four questions on pigment, NAP and CDOM absorption. Review module C.', Q=[
  dict(n=1, ref='mc', pts=2.5, parts=[
      ('(a) Give the main pigment absorption peaks of phytoplankton.', 'B', ['R2']),
      ('(b) Explain the package effect and define Q*_a.', 'A', ['C3']),
      ('(c) Why does a*_ph decrease when Chl increases?', 'B', ['C3', 'K2'])],
      key=['(a) Chl a 443 and 675 nm; carotenoids 450–500; Chl c 465 and 635 (slide 28).',
           '(b) Pigments in large cells shade each other; Q*_a = a_φ/a_sol, from 1 (no package effect) toward 0 (slide 33).',
           '(c) Cell size grows with Chl (slide 33), so absorption per unit Chl falls up to a factor ≈ 4 (slide 32).']),
  dict(n=2, ref='mc', pts=2.5, parts=[
      ('(a) Write the exponential model of CDOM absorption and give the mean slope.', 'A', ['F3']),
      ('(b) a_cdom(412) = 0.30 m⁻¹, S′ = 0.014 nm⁻¹. Compute a_cdom(443).', 'A', ['F3']),
      ('(c) What does a high or low S′ tell you about the CDOM?', 'C', ['R2'])],
      key=['(a) a(λ) = a(λ₀)exp[−S′(λ−λ₀)], S′ ≈ 0.014 nm⁻¹ (slide 41).',
           f'(b) 0.30 × e^(−0.014×31) = {0.3*c443:.3f} m⁻¹.',
           '(c) High S′: fulvic acid, marine; low S′: humic acid, terrestrial (slide 41).']),
  dict(n=3, ref='mc', pts=2.5, parts=[
      ('(a) Compare the spectra of NAP and CDOM and explain a_cdm.', 'B', ['R2', 'R1']),
      ('(b) Compute a(350)/a(440) for CDOM (S′ = 0.014) and NAP (S = 0.011).', 'A', ['F3'])],
      key=['(a) Both exponential toward short λ with similar shapes, so algorithms use a_cdm = a_cdom + a_nap, ≈ 90 % CDOM globally (slides 35, 41, 43).',
           f'(b) CDOM e^(1.26) = {r350:.2f}; NAP e^(0.99) = {nr350:.2f}.']),
  dict(n=4, ref='mc', pts=2.5, parts=[
      ('(a) Compare the absorption budget of Case 1 and Case 2 waters (slide 45).', 'B', ['R1', 'C2']),
      ('(b) Explain why the minimum of the total moves to the green-yellow in Case 2.', 'C', ['R2'])],
      key=['(a) Case 1: water + Chl, minimum ≈ 0.03 m⁻¹ in the blue; Case 2: scale ×10, minerals and CDOM large in the blue.',
           '(b) Minerals and CDOM raise absorption in the blue, so the minimum of the sum shifts to ≈ 570 nm (read from graph).'])]),
 dict(id='P3', title='Paper 3 — Particle scattering and instruments (modules D, E)', minutes=60,
      intro='Four questions on particle scattering and measurements. Review modules D and E.', Q=[
  dict(n=1, ref='md', pts=2.5, parts=[
      ('(a) Compare the VSF of particles with that of pure water.', 'B', ['R3']),
      ('(b) How do large and small particles scatter (area or volume)?', 'A', ['R3', 'F2']),
      ('(c) Write the spectral model for b_p and give n.', 'A', ['F3'])],
      key=['(a) Particles: strong forward peak (diffraction); water: nearly symmetric (slides 20, 46–47).',
           '(b) Large: diffraction, ∝ cross-sectional area; small: Rayleigh, ∝ volume (slide 64).',
           '(c) b_p(λ) = b_p(550)(λ/550)^n, n ∈ [−3, 0], mean ≈ −1 (slide 49).']),
  dict(n=2, ref='md', pts=2.5, parts=[
      ('(a) b_p(550) = 1.0 m⁻¹. Compute b_p(440) for n = 0, −1, −3.', 'A', ['F3']),
      ('(b) How does particle absorption change the spectral shape?', 'C', ['R2']),
      ('(c) Relate the Junge slope ξ and the attenuation slope γ.', 'B', ['R3'])],
      key=[f'(a) {q["0"]:.2f}, {q["-1"]:.2f}, {q["-3"]:.2f}.', '(b) It lowers b_p by 5–30 % in the blue relative to a near-IR power law (slide 53).', '(c) ξ = γ + 3 (slide 68); our Mie check gives n = −1.01 for ξ = 4.']),
  dict(n=3, ref='md', pts=2.5, parts=[
      ('(a) What controls b_bp/b_p? Give typical indices for organic and mineral particles.', 'A', ['R3']),
      ('(b) What do slides 54–57 say about the phytoplankton contribution to b_bp?', 'C', ['R3', 'K2'])],
      key=['(a) Refractive index first, then size (slide 71); textbook: phytoplankton 1.01–1.09, detritus/minerals 1.15–1.20.',
           '(b) Much higher than Mie predicts; particles > 3 µm give a median 50 % of b_bp (slide 57).']),
  dict(n=4, ref='me', pts=2.5, parts=[
      ('(a) Explain how c and a are measured and why b = c − a.', 'B', ['F1']),
      ('(b) A 0.25 m transmissometer gives T = 0.90. Compute c.', 'A', ['F1']),
      ('(c) Write the b_bp retrieval from a 117° sensor.', 'C', ['F1'])],
      key=['(a) Transmissometer: T = e^(−cL); tube with reflecting walls gives a (slides 60–61).',
           f'(b) c = −ln(0.90)/0.25 = {cT["0.9"]:.3f} m⁻¹.',
           '(c) β_p = β − β_w; b_bp = 2πχβ_p(117°) (slide 62).'])]),
 dict(id='P4', title='Paper 4 — IOPs, biogeochemistry and platforms (modules F, H)', minutes=60,
      intro='Four questions on the link between IOPs and biogeochemistry and on autonomous platforms. Review modules F and H.', Q=[
  dict(n=1, ref='mf', pts=2.5, parts=[
      ('(a) Write IOP = Σ(N/V)σ = Σ(N/V)QS and define the symbols.', 'A', ['F2']),
      ('(b) 10⁷ m⁻³ spheres, r = 5 µm, Q = 2: compute c.', 'A', ['F2']),
      ('(c) Why can small particles dominate the scattering although each is small?', 'B', ['F2', 'R3'])],
      key=['(a) N/V (m⁻³), σ (m²), Q (dimensionless), S (m²) (slide 63).',
           f'(b) c = 10⁷ × 2 × π(5×10⁻⁶)² = {cex:.2e} m⁻¹.',
           '(c) The total cross-section is N times σ; numbers can compensate for size (illustrative: 10¹¹ small vs 10⁶ large).']),
  dict(n=2, ref='mf', pts=2.5, parts=[
      ('(a) Use b_p(550) = 0.30 Chl^0.7 to compute b_p for Chl = 0.1, 1, 10 and discuss the validity.', 'B', ['K2']),
      ('(b) POC/SPM = 0.0133 exp(1.27 R). Compute it for R = 1 and 2 and interpret R.', 'C', ['K2', 'R2'])],
      key=[f'(a) {bpc["0.1"]:.3f}, {bpc["1.0"]:.2f}, {bpc["10.0"]:.2f} m⁻¹; Case-1 regression with spread ×2–3 (slide 65).',
           f'(b) {pm["1.0"]:.3f} and {pm["2.0"]:.3f}; R = a_p(675)/a_p(570) increases with the organic share (slide 74).']),
  dict(n=3, ref='mf', pts=2.5, parts=[
      ('(a) What are the links between CDOM and Chl, DOC and salinity?', 'B', ['K2', 'R2']),
      ('(b) Explain non-photochemical quenching and its consequence for fluorescence.', 'C', ['K3']),
      ('(c) How does b_bp/b_p separate a bloom from a nepheloid layer?', 'B', ['R3'])],
      key=['(a) Weak/regional with Chl; regional linear with DOC; near-conservative mixing with salinity (slides 75–77).',
           '(b) Photoprotective response: fluorescence falls at mid-day while Chl does not (slide 80).',
           '(c) Bloom: low b_bp/b_p ≈ 0.006; nepheloid layer 0.012–0.018 (slide 84).']),
  dict(n=4, ref='mh', pts=2.5, parts=[
      ('(a) List the seven contributions of autonomous platforms (slide 101).', 'B', ['K3']),
      ('(b) Compare the sensors of a bio-optical float and a glider.', 'B', ['K3']),
      ('(c) Give the Argo and BGC-Argo counts and their dates.', 'C', ['K3'])],
      key=['(a) Extend satellite signal inward; validate L2/L3 products; validate primary-production models; validate coupled models; assimilation; trends; interior patterns.',
           '(b) Float: radiometer 412/490/532, transmissometer 660, Chl/CDOM fluorometers, backscatter 555; glider: b_bp ×2, fluorescence, E_d/L_u at 4 λ, CTD, O₂ (slides 97–98).',
           '(c) 4153 Argo floats on 30 June 2025 (slide 113); 788 operational BGC floats in May 2025, oxygen 782, b_bp 551, Chl 551, full BGC 77 (slide 115).'])]),
 dict(id='P5', title='Paper 5 — Calculation drill (all modules)', minutes=90,
      intro='Numerical questions only. All keys come from Python (data/verified.json).', Q=[
  dict(n=1, ref='ma', pts=2.5, parts=[
      ('(a) A 0.25 m transmissometer gives T = 0.50. Compute c.', 'A', ['F1']),
      ('(b) a = 0.10 m⁻¹ in the same water: compute b and b/c.', 'A', ['F1']),
      ('(c) Which fraction of the beam remains after 10 m if c = 0.2 m⁻¹?', 'A', ['F1'])],
      key=[f'(a) c = −ln 0.5/0.25 = {cT["0.5"]:.3f} m⁻¹.', f'(b) b = {cT["0.5"]-0.1:.3f} m⁻¹; b/c = {(cT["0.5"]-0.1)/cT["0.5"]:.2f}.', f'(c) e^(−2) = {math.exp(-2):.3f}.']),
  dict(n=2, ref='mb', pts=2.5, parts=[
      ('(a) Compute b_w(500 nm) for S = 37 from the Morel formula (closed form: 2πβ(90°)(2 + 2k/3)).', 'B', ['F3']),
      ('(b) Compute the change between S = 0 and S = 37.', 'A', ['F3']),
      ('(c) Compute the ratio of scattering at 450 and 550 nm for exponents −4.32 and −4.14.', 'A', ['F3'])],
      key=[f'(a) {b37:.3e} m⁻¹.', f'(b) {b0:.3e} → {b37:.3e}: +30 %.', f'(c) {V["ratio_450_550_morel"]:.3f} and {V["ratio_450_550_buiteveld"]:.3f}.']),
  dict(n=3, ref='md', pts=2.5, parts=[
      ('(a) a_cdom(412) = 0.30, S′ = 0.014 nm⁻¹: compute a_cdom(443).', 'A', ['F3']),
      ('(b) b_p(550) = 0.5 m⁻¹, n = −1: compute b_p(440).', 'A', ['F3']),
      ('(c) Compute the attenuation of 10⁷ m⁻³ spheres r = 5 µm, Q = 2.', 'A', ['F2'])],
      key=[f'(a) {0.3*c443:.3f} m⁻¹.', f'(b) {0.5*q["-1"]:.3f} m⁻¹.', f'(c) {cex:.2e} m⁻¹.']),
  dict(n=4, ref='mg', pts=2.5, parts=[
      ('(a) K_d = 0.04 m⁻¹: compute the 1 % light depth and the penetration depth.', 'B', ['C1']),
      ('(b) K_d = 0.1, c = 0.2 m⁻¹: compute the Secchi depth with Γ = 8 (textbook formula).', 'B', ['C1']),
      ('(c) Compute Q*_a for ρ = 1 (sphere model) and interpret.', 'B', ['C3'])],
      key=[f'(a) {EU["0.04"]["z1pct"]:.1f} m and {EU["0.04"]["penetration_1_over_Kd"]:.0f} m.', f'(b) {SC["Kd0.1_c0.2"]:.1f} m.', f'(c) {PK["1.0"]:.2f}: about 30 % less absorption than the same pigment dispersed.'])]),
]

def all_parts():
    out = []
    for pp in PAPERS:
        for qq in pp['Q']:
            for i, x in enumerate(qq['parts']): out.append((f'{pp["id"]}Q{qq["n"]}', chr(97 + i), x[1], x[2]))
    return out
