# -*- coding: utf-8 -*-
"""Module D — Particle scattering (slides 46-58; sizes and Mie in 63-71 are used here and in F)."""
import math
from lib import *
from qcore import Bank
from ma import LS
V = VERIFIED

def build():
    B = Bank('md', seed=14); A = B.add
    E = V['junge_ensemble_m105']; R = V['bbp_over_bp_vs_index_and_slope']
    n4, n5, n35 = E['4.0']['n_bp'], E['5.0']['n_bp'], E['3.5']['n_bp']
    q440 = V['bp_440_over_550']
    A('What does slide 46 say about the volume scattering function of particles?',
      'It is strongly forward-peaked (mainly diffraction, so very sensitive to size), with notable differences between particle types in the backward direction (> 90°)', ['It is isotropic like that of pure water', 'It is strongly backward-peaked', 'It cannot be defined for particles'],
      'Slide 46 (Morel, 1973): “Strong forward scattering from particles (mainly due to diffraction, so very sensitive to size). Similar shape, but notable differences in the backward direction (> 90°). Still very few in situ measurements.”', 1, 'Particle VSF', src='Lecture, slide 46')
    A('On slide 46 it is said that one cannot, from an in-situ measurement of the VSF, separate the contribution of different particle types. What does this imply?',
      'The measured particulate VSF is a sum over all particles, so attributing it to phytoplankton, minerals or detritus needs additional information', ['Particles do not scatter', 'The VSF is the same for all particles', 'Only absorption can be measured'],
      'Slide 46: “For particulate scattering it is impossible to distinguish from in situ measurement the respective contribution of different types of particles.” This is the root of the phytoplankton-backscattering question of slides 54–57.', 2, 'Particle VSF', src='Lecture, slide 46')
    A('Slide 47 compares Rayleigh and Mie scattering patterns. Which statement matches it?',
      'Rayleigh scattering is nearly symmetric forward/backward; Mie scattering becomes more forward-peaked as the particle gets larger', ['Rayleigh scattering is strongly forward; Mie is isotropic', 'All patterns are identical', 'Larger particles scatter more backward than smaller ones'],
      'Slide 47: three drawings — Rayleigh (symmetric), Mie small particle (forward lobe larger than backward), Mie large particle (very strong narrow forward lobe).', 1, 'Rayleigh vs Mie', src='Lecture, slides 47, 64')
    A('According to slide 64, how does the scattering response of large and small particles scale?',
      'Large particles: diffraction/geometric optics, proportional to cross-sectional area; small particles: Rayleigh, proportional to volume', ['Large: proportional to volume; small: proportional to area', 'Both proportional to the diameter', 'Both independent of size'],
      'Slide 64: large particles — diffraction dominates, geometric optics, response ∝ cross-sectional area (sensitive to shape); small particles — refraction/reflection, Rayleigh, response ∝ volume (insensitive to shape); in between, Mie scattering for a sphere.', 1, 'Rayleigh vs Mie', src='Lecture, slide 64')
    A('Which model does the lecture use for the spectral dependence of particulate scattering (slide 49)?',
      'b_p(λ) = b_p(550) (λ/550)^n, with n between 0 and −3 and a mean around −1', ['b_p(λ) = b_p(550) exp[−0.014(λ − 550)]', 'b_p(λ) = b_p(550) (λ/550)^+4', 'b_p(λ) = constant × λ^−4.32 for all particles'],
      'Slide 49. The same form applies to b_bp. “In absence of absorption processes this spectral dependency is related to size. Absorption can affect the spectral shape of the scattering coefficients.”', 1, 'Spectral shape', src='Lecture, slide 49')
    A('A water has b_p(550) = 1.0 m⁻¹ and n = −1. What is b_p(440)?',
      f'≈ {q440["-1"]:.2f} m⁻¹', [f'≈ {1/q440["-1"]:.2f} m⁻¹ (exponent sign reversed)', '≈ 1.00 m⁻¹ (no spectral dependence)', f'≈ {q440["-3"]:.2f} m⁻¹ (n = −3 used)'],
      f'(440/550)^(−1) = {q440["-1"]:.3f}. For n = 0 the ratio is 1; for n = −3 it is {q440["-3"]:.3f} (Python).', 1, 'Calculation', src='Lecture, slide 49')
    A('Which spectral exponent does a Junge size distribution N(D) ∝ D^−ξ with ξ = 4 give for b_p (Mie spheres, m = 1.05, D from 0.1 to 100 µm)?',
      f'n ≈ {n4:.2f}, i.e. b_p ∝ λ^−1 (attenuation slope γ = ξ − 3 = 1)', ['n ≈ +1', 'n ≈ −4', 'n ≈ 0 for every ξ'],
      f'Home-made Mie computation (Bohren–Huffman series, spherical Bessel functions; two-point and least-squares exponents agree): n = {n35:.2f}, {n4:.2f}, {n5:.2f} for ξ = 3.5, 4, 5. This reproduces ξ = γ + 3 (slide 68) and the “mean n ≈ −1” of slide 49. A model, not data.', 3, 'Mie check', origin='bo_sung', src='Lecture, slides 49, 68; home-made Mie')
    A('Slide 51 (Snyder et al., 2008) shows the power-law exponent of b_p and b_bp. Which statement fits?',
      'The exponent of b_p is scattered around about −0.3 while that of b_bp clusters near −1', ['Both exponents are exactly +1', 'b_p has exponent −4 and b_bp has 0', 'No exponent can be derived'],
      'Slide 51: left panel b_p exponent between about −1 and +1 (centre ≈ −0.3, read from the graph); right panel b_bp exponent mostly between −1.5 and −0.5, around −1.', 2, 'Spectral shape', src='Lecture, slide 51')
    A('What does slide 52 show about the quality of a power-law description of b_p and b_bp?',
      'The fractional differences are small (mostly within ±0.1), so a power law describes them well to first order', ['The fractional difference is always larger than 100 %', 'A power law fails completely for b_bp', 'Only the units are discussed'],
      'Slide 52: (f_obs − f_pred)/f_pred is within about ±0.1 for b_p and close to 0 for b_bp, with a few outliers (up to 0.6, read from graph).', 2, 'Spectral shape', src='Lecture, slide 52')
    A('What is the effect of particle absorption on b_p according to slide 53 (Doxaran et al., 2009)?',
      'It makes measured b_p 5–30 % lower than a power law fitted in the near-infrared and extrapolated to 440 nm', ['It makes b_p 5–30 % higher', 'It makes b_p exactly zero in the blue', 'It has no effect'],
      'Slide 53 text; correction Δb_p/a_p = 1 − tanh(0.5 γ²) (γ read as the spectral exponent). Absorption inside particles reduces the apparent scattering near absorption bands.', 2, 'Absorption effect', src='Lecture, slide 53')
    A('What is the main finding on slide 57 about phytoplankton and backscattering (Dall’Olmo et al., 2009)?',
      'Phytoplankton backscattering is much higher than expected from Mie theory (only a few percent), and particles larger than 3 µm contribute a median of about 50 % of b_bp', ['Phytoplankton do not backscatter at all', 'Phytoplankton backscattering is exactly what Mie theory predicts', 'Only particles smaller than 0.2 µm backscatter'],
      'Slide 57 text; red lines (cultures) are 10–100× above the black Mie-model lines for σ_bb and b_bp/b_p (read from graph). Slide 54: the data are new because suitable sensors only appeared recently.', 2, 'Phytoplankton b_bp', src='Lecture, slides 54, 57')
    A('Which relative refractive indices does the textbook give for living phytoplankton and for detritus/inorganic particles?',
      'About 1.01–1.09 for phytoplankton and 1.15–1.20 for detritus and inorganic particles', ['1.50–1.60 for phytoplankton and 1.00 for minerals', '0.50–0.90 for phytoplankton', '1.33 for all particles'],
      'Textbook, Water: “living phytoplankton typically have low indices of refraction, in the range 1.01 to 1.09 relative to … pure seawater; detritus and inorganic particles generally have high indices, in the range 1.15 to 1.20.”', 2, 'b_bp/b_p', origin='bo_sung', src='Textbook: Water')
    A('How does b_bp/b_p at 550 nm change with the relative refractive index in a Mie computation for a Junge distribution (ξ = 4)?',
      f'It increases: {R["1.02"]["4.0"]:.4f} at m = 1.02, {R["1.1"]["4.0"]:.4f} at 1.10 and {R["1.2"]["4.0"]:.4f} at 1.20', [f'It decreases from {R["1.2"]["4.0"]:.4f} to {R["1.02"]["4.0"]:.4f}', 'It is constant at 0.01', 'It is exactly 0.5 as for pure water'],
      'Own Mie ensemble (D = 0.1–100 µm). It reproduces the order of magnitude and the trend of slide 71 (“b_bp/b_p depends on refractive index first and size second”); the absolute values depend on the size range chosen, so this is an illustration.', 3, 'b_bp/b_p', origin='bo_sung', src='Lecture, slide 71; home-made Mie')
    A('A scattering budget in Case 1 water (slide 58, left) is dominated by what?',
      'Particles; the contribution of pure water is below ≈ 5 %', ['Pure water, which gives about 90 %', 'CDOM, which scatters most', 'Air bubbles'],
      'Slide 58 (read from graph): total b ≈ 0.18 m⁻¹ at 400 nm, almost equal to the Chl-related curve, with water ≈ 0.005 m⁻¹. In Case 2 the scale is 10× larger (0–3 m⁻¹) and minerals are the biggest term.', 2, 'Budget', src='Lecture, slide 58')
    A('What does slide 48 (lower right) show about the spectral ratio 443/555 of the particulate phase function at 140°?',
      'It decreases linearly as a_NAP/a_ph(400) increases: R = −0.060 (a_NAP/a_ph) + 0.99, r² = 0.72', ['It increases linearly with a_NAP/a_ph', 'It is unrelated to a_NAP/a_ph', 'It equals exactly 1 always'],
      'Slide 48 caption: Fig. 15, R₄₄₃/₅₅₅(140°) in the 0–4 m layer versus a_NAP/a_ph(400). The relation is a regression, not a law.', 3, 'Particle VSF', src='Lecture, slide 48')

    B.essay('(a) Describe the VSF of particles and compare with pure water. (b) Write the spectral model for b_p and give the range and mean of n. (c) Explain how absorption can alter the spectral shape (slide 53).',
            f'(a) Strong forward peak from diffraction, sensitive to size; differences between particle types in the backward direction; water is nearly symmetric (slides 20, 46–47). (b) b_p(λ) = b_p(550)(λ/550)^n; n between 0 and −3, mean ≈ −1 (slide 49); b_p(440)/b_p(550) = {q440["0"]:.2f}, {q440["-1"]:.2f}, {q440["-3"]:.2f} for n = 0, −1, −3. (c) Absorption inside particles lowers the measured b_p by 5–30 % relative to a near-IR power law extrapolated to 440 nm (Doxaran et al., 2009), correction Δb_p/a_p = 1 − tanh(0.5γ²).',
            2, 'Particle scattering', src='Lecture, slides 46–53')
    B.essay('What fraction of the particulate backscattering comes from phytoplankton? Summarise slides 54–57, explain the disagreement with Mie theory and say what b_bp/b_p reveals about particle type (use slides 71 and 84).',
            'Slide 54: new data because backscattering sensors appeared recently. Slide 57: phytoplankton b_bp is much higher than Mie theory suggests (only a few %); fractionation experiments give a median 50 % from particles larger than 3 µm (Dall’Olmo et al., 2009). Slide 71: b_bp/b_p depends on refractive index first, then size; low POC/Chl = lower ratio. Slide 84 (Boss et al. 2004): bloom with low b_bp/b_p (≈ 0.006) versus nepheloid layer with high b_bp/b_p (0.012–0.018) = resuspended sediments.',
            3, 'Phytoplankton b_bp', src='Lecture, slides 54–57, 71, 84')

    sl = [
        S('Strong forward scattering by particles', cols(LS(48, 430), dul(['Diffraction dominates', 'Mie theory reproduces data', 'Differences in the backward part']), flex=[3, 2])),
        S('Rayleigh and Mie patterns', cols(LS(47, 430), dul(['Rayleigh: symmetric', 'Small Mie particle: forward lobe', 'Large particle: narrow forward peak']), flex=[3, 2])),
        S('Large and small particles', cols(LS(64, 430), dul(['Large: ∝ area (geometric)', 'Small: ∝ volume (Rayleigh)', 'In between: Mie']), flex=[3, 2])),
        S('Spectral power law', cols(LS(49, 400), dul(['b<sub>p</sub>(λ) = b<sub>p</sub>(550)(λ/550)<sup>n</sup>', 'n between 0 and −3', 'mean ≈ −1']), flex=[3, 2])),
        S('Power law and size distribution', EQS_('powerlaw')),
        S('Shape of the power law', img('bp_power', 700, cap='Own computation: b<sub>p</sub>(λ)/b<sub>p</sub>(550) for n = 0, −1, −3')),
        S('Measured exponents', cols(LS(51, 430, 'Lecture slide 51 (Snyder et al., 2008)'), dul(['b<sub>p</sub>: scattered about −0.3', 'b<sub>bp</sub>: near −1', 'Power law good to ±0.1 (slide 52)']), flex=[3, 2])),
        S('Size controls the exponent (Mie check)', img('junge_exponent', 700, cap='Own Mie computation: exponent versus Junge slope ξ; dashed = −(ξ−3), i.e. ξ = γ + 3 (slide 68)')),
        S('Backscatter ratio versus refractive index', img('bbp_index', 700, cap='Own Mie computation, Junge distributions: b<sub>bp</sub>/b<sub>p</sub> rises with refractive index (slide 71)')),
        S('Phytoplankton and backscattering', cols(LS(57, 430), dul(['Much higher than Mie predicts', 'Particles &gt; 3 µm: ≈ 50 % of b<sub>bp</sub>', 'Dall’Olmo et al., 2009']), flex=[3, 2])),
        S('Scattering budget', cols(LS(58, 430), dul(['Particles dominate in both cases', 'Water &lt; 5 %', 'Case 2: ×10 larger']), flex=[3, 2])),
        S('Key points', dul(['Particles: forward-peaked VSF (diffraction)', 'b<sub>p</sub> ∝ λ<sup>n</sup>, n ≈ −1 on average', 'Size → exponent; index → b<sub>bp</sub>/b<sub>p</sub>', 'Phytoplankton backscatter more than Mie says'], xl=True)),
    ]
    mod = dict(id='md', slug='04-particle-scattering', title='D · Particle scattering', en='VSF of particles, b_p, b_bp, spectral shape, size and refractive index (slides 46–58)',
               qtitle='Guiding question: how do particles scatter, and what do the shape and spectrum of scattering reveal?',
               question='<p>Particles (phytoplankton, detritus, minerals, bacteria) dominate scattering in most waters. Their VSF is forward-peaked; the spectral shape of b_p and b_bp and the ratio b_bp/b_p carry information on size and refractive index.</p>',
               sections=[
                ('The VSF of particles', '<p>Particle scattering is strongly <b>forward</b>, mainly by diffraction, which makes it very sensitive to size. Differences between particle types show up mostly in the backward direction (> 90°), which is also the direction measured by backscattering sensors (slide 46). Large particles scatter ∝ area, small ones ∝ volume (slide 64).</p>'),
                ('Spectral dependence', '<p>The lecture models b<sub>p</sub> and b<sub>bp</sub> as power laws:</p>' + EQ('powerlaw') +
                 f'<p><b>Mie check (Python, own).</b> A Junge distribution of non-absorbing spheres (m = 1.05, D = 0.1–100 µm) gives n = {n35:.2f}, {n4:.2f}, {n5:.2f} for ξ = 3.5, 4, 5, i.e. n ≈ −(ξ − 3): this is the relation ξ = γ + 3 of slide 68. Particle absorption lowers b<sub>p</sub> by 5–30 % (slide 53). Snyder et al. (2008, slide 51) find b<sub>p</sub> exponents near −0.3 and b<sub>bp</sub> exponents near −1; a power law fits within about ±10 % (slide 52).</p>'),
                ('Backscattering ratio', f'<p><b>b<sub>bp</sub>/b<sub>p</sub></b> depends on refractive index first, then size (slide 71). Textbook indices: phytoplankton 1.01–1.09, detritus/minerals 1.15–1.20. In our Mie runs (ξ = 4) the ratio rises from {R["1.02"]["4.0"]:.4f} (m = 1.02) to {R["1.2"]["4.0"]:.4f} (m = 1.20). Phytoplankton cultures backscatter much more than Mie theory predicts, and particles larger than 3 µm provide a median 50 % of b<sub>bp</sub> (slide 57). In the field, b<sub>bp</sub>/b<sub>p</sub> separates a bloom (low) from a nepheloid layer (high) (slide 84).</p>'
                 '<div class="callout warn"><b class="t">Limit</b>Mie spheres are a model. The absolute b<sub>bp</sub>/b<sub>p</sub> depends on the size range and shape; only the trends are compared with the slides.</div>')],
               checklist=['Describe the forward peak and the Rayleigh/Mie patterns (slides 46–47, 64).', 'Write the power law and give n ∈ [−3, 0], mean −1.', 'Explain how absorption modifies b_p (slide 53).', 'State what controls b_bp/b_p (index, then size) and typical values for organic vs mineral particles.', 'Summarise the phytoplankton–b_bp question (slides 54–57).'],
               summary=['Tán xạ hạt chủ yếu về phía trước (nhiễu xạ); b_p ∝ λ^n, n trung bình ≈ −1.', 'b_bp/b_p phụ thuộc chiết suất trước, kích thước sau.', 'Thực vật phù du tán xạ ngược nhiều hơn lý thuyết Mie dự đoán.'],
               calcs=[('bplaw', 'b_p(λ) power law'), ('sumns', 'IOP = Σ N·Q·S')], quiz_n=10,
               v2=dict(we_title='Power law from 550 to 440 nm', we=f'<p>b<sub>p</sub>(550) = 1.0 m⁻¹, n = −1 ⇒ b<sub>p</sub>(440) = (440/550)<sup>−1</sup> = {q440["-1"]:.2f} m⁻¹; n = −3 ⇒ {q440["-3"]:.2f} m⁻¹. Small particles (steep n) scatter much more in the blue.</p>',
                       qa=[('Why is the VSF so forward-peaked?', 'Diffraction around particles larger than the wavelength (slides 46, 64).'), ('Which particles have a higher b_bp/b_p?', 'Those with a higher refractive index (minerals, detritus) (slide 71).')],
                       hooks=[('Big and forward; small and symmetric.', 'Hạt lớn: về phía trước; hạt nhỏ: đối xứng.'), ('Index first, size second.', 'Chiết suất trước, kích thước sau.')]))
    return mod, sl, B
