# formulas_from_slides.md — formulas as they appear on the lecture slides

All lines below were checked against the page image ("đã đối chiếu với ảnh"). "As printed" means the slide's own notation is kept even where it looks unusual; differences from the textbook are listed in `../textbook/formulas.md` once the crawl is done.

| Slide | Formula (Unicode) | Notes |
|---|---|---|
| 5 | dL(θ,φ)/dr = −c·L(θ,φ) + 2π ∫₀^{4π} β(θ,φ,θ″,φ′) L dω′ + S ; b + a = c | As printed (the 2π factor with 0–4π limits is unusual: see textbook). S = source (internal sources, e.g. fluorescence/Raman). |
| 17 | a(λ) ≡ lim_{Δr→0} (1/Φ_i(λ))·Φ_a(λ)/Δr [m⁻¹] ; β(ψ,λ) ≡ lim_{Δr→0} lim_{ΔΩ→0} Φ_s(ψ,λ)/(Φ_i(λ)·Δr·ΔΩ) [m⁻¹ sr⁻¹] | Definitions of a and the volume scattering function. |
| 18 | b = ∫_{4π} β(θ)dω = 2π∫₀^π β(θ) sinθ dθ ; b_f = 2π∫₀^{π/2} β sinθ dθ ; b_b = 2π∫_{π/2}^{π} β sinθ dθ ; b = b_f + b_b ; c = a + b | Revolution symmetry assumed. |
| 19 | a = a_w + a_CDOM + a_ph + a_NAP ; b = b_w + b_p ; b_b = b_bw + b_bp | Additivity. |
| 20 | β_w(θ,λ,S,T=20 °C) = 1.38 (λ/500 nm)^−4.32 (1 + 0.3 S/37) 10⁻⁴ (1 + cos2θ (1−δ)/(1+δ)), δ = 0.09 | Morel 1974. Printed "cos2θ" with no superscript at 250 dpi. Standard (Morel) angular term is cos²θ. Python check decides (verified.json). Units m⁻¹ sr⁻¹. |
| 23 | β_w = 1.29 (λ/500 nm)^−4.14 (1 + 0.3 S/37) 10⁻⁴ (1 + cos2θ (1−δ)/(1+δ)), δ = 0.051 | Buiteveld et al. 1994. Same printing of the angular term. |
| 33 | Q*_a(λ) = a_φ(λ)/a_sol(λ) ; a_sol(λ) = Σ_i C_i a*_sol,i(λ) | Bricaud et al. 2004. Q*_a → 1: no package effect; → 0: maximal. |
| 31 | a*_ph(λ) = a_ph(λ)/Chl | Chl-specific absorption [m² mg⁻¹]. |
| 41 | a_ds(λ) = a_ds(λ₀) exp(−S′(λ−λ₀)) ; S′ ≈ 0.014 nm⁻¹ (average, Bricaud 1981) ; alternative a_ds ∝ λ^−6.92 (Twardowski 2004) | a_ds ≡ a_ys ≡ a_cdom. |
| 49 | b_p(λ) = b_p(550) (λ/550)^n, n ∈ [−3, 0], mean ≈ −1 | Same form for b_bp. |
| 51 | f(λ) = f₅₅₀ (λ/550)^γ | Snyder et al. 2008 (power-law exponent γ). |
| 52 | fractional difference = (f_obs − f_pred)/f_pred | Goodness of the power law. |
| 53 | Δb_p/a_p = 1 − tanh(0.5 × γ²) | Doxaran et al. 2009. The exponent on γ is read as 2 from the image; the symbol meaning of γ is the spectral slope of b_p (textbook/paper to check). |
| 62 | β_corr(117°, a=0) = β_meas(117°, a)·exp(0.039 …) [cut off] ; β_p(117°,λ) = β(117°,λ) − β_w(117°,λ) ; b_bp = 2π χ β_p(117°) | Boss & Pegau 2001. The exponent's argument is cut off on the slide — not transcribed. |
| 63 | IOP(λ) = Σ_i (N_i/V) σ_IOP,i(λ) = Σ_i (N_i/V) Q_IOP,i(λ) S_i | σ [m²]; Q dimensionless; S = geometric cross-section area [m²]; N/V [m⁻³]. |
| 66 | y = 5.38 x^0.90, R² = 0.94 (c(555) vs particle surface concentration) ; b_p(550) = 0.30 [Chl]^0.7 (s65) | Empirical regressions, not laws. |
| 68 | N(D) = N₀ (D/D₀)^−ξ ; c_p(λ) = A λ^−γ ; ξ = γ + 3 ; ξ = γ + 3 − 0.5 exp(−6γ) | Junge distribution and its link with the attenuation slope (Boss et al. 2001). Checked at 300 dpi. |
| 71 | b_bp/b_p = f(n, ξ) — contour plot only, no equation | Loisel et al. 2007. |
| 74 | POC/SPM = 0.0133 exp{1.27 [a_p(675)/a_p(570)]}, r² = 0.81, n = 44 | Wozniak et al. 2010. |
| 38 | a*_m(300) = 0.033[Fe] + 0.052 (R² = 0.88) ; a*_m(400) = 0.031[Fe] − 0.043 (R² = 0.84) ; a*_m(500) = 0.017[Fe] − 0.036 (R² = 0.59) | Babin & Stramski 2004; [Fe] in %. |
| 48 | R₄₄₃/₅₅₅(140°) = −0.060 (a_NAP/a_ph)(400) + 0.99, r² = 0.72 | Spectral ratio of the phase function at 140°. |
| 105 | ∫ POC dz relation (s83): ∫₀^{1.5Zeu} POC dz = 286 ∫₀^{1.5Zeu} c_p dz + 3163, R² = 0.42, N = 34 | Units not legible; not used quantitatively. |

Formulas deliberately NOT used quantitatively: s71 regression lines (printed equations look like log-form), s83 POC–c_p fit (units illegible).
