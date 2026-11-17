# formulas.md — textbook formulas used (restated; Ocean Optics Web Book, CC BY 2.0)

| Page (URL under /view/) | Formula | Compared with the lecture |
|---|---|---|
| optical-constituents-of-the-ocean/water | n(S,T,λ) = n₀ + (n₁+n₂T+n₃T²)S + n₄T² + (n₅+n₆S+n₇T)/λ + n₈/λ² + n₉/λ³ (Quan & Fry 1995); a = 4πk/λ | not in lecture |
| scattering/physics-scattering | β(ψ) = (2π²kT/(λ⁴β_T))·n²(∂n/∂P)_T²·(6+6ρ)/(6−7ρ)·[1 + (1−ρ)/(1+ρ)·cos²ψ] ; at 20 °C, 546 nm, ρ = 0.031: β(90°) = 0.869×10⁻⁴ m⁻¹ sr⁻¹ (Morel 1974: 0.83) | Same angular form (1 + cos²ψ·(1−δ)/(1+δ)) as the lecture's Morel/Buiteveld formula; lecture prints "cos2θ" (probably cos²θ). The lecture depolarisation values (0.09 Morel, 0.051 Buiteveld) differ from the book's 0.031 (Zhang et al. 2019). |
| optical-constituents-of-the-ocean/colored-dissolved-organic-matter | a_g(λ) = a_g(λ_ref)·exp(−S_g(λ−λ_ref)); S_g ≈ 0.014 nm⁻¹, range 0.007–0.026 | Lecture s41: same law, S′ = 0.014 (Bricaud 1981). Consistent. |
| optical-constituents-of-the-ocean/level-2/particle-size-distributions | dN/dlogD ∝ D⁻³ ⇔ n(D) = dN/dD ∝ D⁻⁴ (Junge) | Lecture s68: N(D) = N₀(D/D₀)^−ξ and ξ = γ + 3. The slope convention (n(D) vs dN/dlogD) differs by 1: Junge = ξ 4 in the lecture notation. |
| optical-constituents-of-the-ocean/level-2/classic-iop-model-case-1-water | B_p = b_bp/b_p (particle backscatter fraction), Fournier–Forand phase function | Lecture s71 b_bp/b_p |
| inherent-and-apparent-optical-properties/k-functions | K_d ≡ −d ln E_d/dz ; E_d(z) = E_d(0)·exp(−K_d z) ; a ≤ K_d μ̄_d ≤ c ; c > K_d ; K_d ≈ a/μ̄_d ; penetration depth 1/K_d | not in lecture |
| inherent-and-apparent-optical-properties/reflectances | R(z,λ) ≡ E_u/E_d ; R_rs ≡ L_w(in air)/E_d(in air) [sr⁻¹] | not in lecture |
| photometry-and-visibility/level-2/the-secchi-disk | z_SD = Γ/(⟨K_dv⟩+⟨c_v⟩), Γ ≈ 6–9 (HydroLight default 8); Lee et al. 2015: z_SD = γ/(2.5 K_d(λ_min)) | lecture s4 mentions Secchi depth only qualitatively |
| inherent-and-apparent-optical-properties/classification-schemes | Case 1: optical properties determined primarily by phytoplankton and co-varying CDOM and detritus; Case 2: everything else (mineral particles, CDOM, microbubbles not covarying) | consistent with s14 |
