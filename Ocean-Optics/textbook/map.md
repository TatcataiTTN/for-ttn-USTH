# map.md — lecture sections → textbook pages (all under https://oceanopticsbook.info/view/)

| Lecture slides | Topic | Textbook page(s) used | What we took from it |
|---|---|---|---|
| 5, 17–19 | RTE, a, β, b, c, additivity | `radiative-transfer-theory/radiative-transfer-equations`, `…/level-2/the-scalar-radiative-transfer-equation`, `inherent-and-apparent-optical-properties/inherent-optical-properties` | Definitions of IOPs; the RTE in standard form (no 2π factor in front of the in-scattering integral) |
| 14–16 | Case 1 / Case 2, optical classes | `inherent-and-apparent-optical-properties/classification-schemes` | Morel & Prieur 1977 quote; modern Case 1/Case 2 definitions; Jerlov and Forel–Ule types |
| 20–27 | Pure water | `optical-constituents-of-the-ocean/water`, `scattering/physics-scattering` (Einstein–Smoluchowski section), `absorption/absorption-by-oceanic-constituents` | n(S,T,λ) of Quan & Fry; Einstein–Smoluchowski VSF; β(90°, 546 nm) = 0.869×10⁻⁴ m⁻¹ sr⁻¹ (ρ = 0.031) vs Morel 1974 ≈ 0.83×10⁻⁴ |
| 28–34 | Phytoplankton absorption | `optical-constituents-of-the-ocean/phytoplankton`, `absorption/absorption-overview` | pigments, in-vivo spectra, package effect (text only) |
| 35–38 | NAP | `optical-constituents-of-the-ocean/non-algal-particles-nap` | exponential NAP spectrum |
| 39–45 | CDOM | `optical-constituents-of-the-ocean/colored-dissolved-organic-matter` | a_g(λ) = a_g(λ_ref)·exp(−S_g(λ−λ_ref)), S_g ≈ 0.014 nm⁻¹ (0.007–0.026) |
| 46–58 | Particle scattering | `scattering/scattering-overview`, `scattering/physics-scattering`, `optical-constituents-of-the-ocean/level-2/particle-size-distributions`, `scattering/petzolds-measurements` | Mie/Rayleigh regimes; Junge distribution (dN/dlogD ∝ D⁻³ ⇔ n(D) ∝ D⁻⁴); refractive-index ranges (phytoplankton 1.01–1.09, detritus/inorganic 1.15–1.20) |
| 59–62 | Measuring IOPs | `inherent-and-apparent-optical-properties/measuring-iops`, `absorption/measurement-of-absorption` | instrument families |
| 63–84 | IOP ↔ biogeochemistry | `optical-constituents-of-the-ocean/level-2/classic-iop-model-case-1-water`, `…/new-iop-model-case-1-water`, `scattering/level-2/chlorophyll-fluorescence` | Case-1 IOP models as a function of Chl; fluorescence |
| — (not in slides) | Light field, AOPs | `inherent-and-apparent-optical-properties/apparent-optical-properties`, `…/reflectances`, `…/k-functions`, `remote-sensing/measures-of-reflectance`, `remote-sensing/ocean-color`, `remote-sensing/terminology`, `photometry-and-visibility/level-2/the-secchi-disk` | K_d ≡ −d ln E_d/dz; E_d(z) = E_d(0)exp(−∫K_d dz′); R = E_u/E_d; R_rs = L_w/E_d (sr⁻¹); Secchi depth z_SD = Γ/(K_dv + c_v) (Γ ≈ 6–9, 8 default), Lee et al. (2015) z_SD = γ/(2.5 K_d(λ_min)); c > K_d |
| 85–120 | Platforms | none (course material only) | not covered by the textbook crawl |

Pages that did not give what their URL suggested: `scattering/level-2/mie-theory-*` (three URLs) all returned the Henyey–Greenstein page, so we did not use them.
Not found in the pages we crawled: an explicit "R ≈ f·b_b/(a+b_b)" statement. We therefore label that relation "classical result (Gordon et al. 1975; Morel & Prieur 1977), not verified on the crawled textbook pages".
