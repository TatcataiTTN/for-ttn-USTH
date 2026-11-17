# -*- coding: utf-8 -*-
"""Module C — Absorption by phytoplankton, non-algal particles and CDOM (slides 28-45)."""
import math
from lib import *
from qcore import Bank
from ma import LS
V = VERIFIED

def build():
    B = Bank('mc', seed=13); A = B.add
    c443, n443, r350 = V['cdom_ratio_443_from_412_S014'], V['nap_ratio_443_from_412_S011'], V['cdom_ratio_350_over_440_S014']
    nr350 = V['nap_ratio_350_over_440_S011']; PK = V['package_Qstar']
    A('Which wavelengths are the two main absorption peaks of chlorophyll a in the lecture (slide 28)?',
      'About 443 nm (blue) and 675 nm (red)', ['About 550 nm and 800 nm', 'About 350 nm and 1000 nm', 'About 600 nm only'],
      'Slide 28 lists Chl a (443 and 675 nm), carotenoids (450–500 nm), Chl c (465 and 635 nm) and phaeopigments (degradation products). Slide 29 shows the in-vivo pigment spectra (Bricaud et al., 2004).', 1, 'Phytoplankton', src='Lecture, slides 28–29')
    A('Where do carotenoids absorb, and what changes from oligotrophic to eutrophic water according to slide 28?',
      'They absorb at 450–500 nm; their variable proportion is responsible for blue/green changes between oligotrophic (Chl < 0.1 mg m⁻³) and eutrophic (Chl > 1 mg m⁻³) waters', ['They absorb only above 600 nm and are absent from oligotrophic water', 'They absorb at 675 nm like Chl a and never vary', 'They do not absorb light'],
      'Slide 28 text. On slide 29 all carotenoids absorb broadly from about 450 to 520 nm and are close to zero above ≈ 550 nm.', 2, 'Phytoplankton', src='Lecture, slides 28–29')
    A('What is the package (discretisation) effect?',
      'Pigments packed inside a large cell absorb less per unit pigment than the same pigment dispersed in solution, because of self-shading', ['An increase of absorption when cells form chains', 'The absorption of light by the plastic of the sample bottle', 'The scattering of light by the cell wall'],
      'Slide 33: Q*_a(λ) = a_φ(λ)/a_sol(λ) “decreases from 1 (no package effect) to 0 (maximal package effect)”. Cell size increases with Chl (slide 33, size index), so a*_ph decreases with Chl (slide 32).', 1, 'Package effect', src='Lecture, slides 32–33')
    A('Slide 32 shows that a*_ph varies by about a factor of 4. Which two explanations does the slide propose?',
      'The discretisation (package) effect and/or the internal pigment concentration', ['Salinity and temperature only', 'Solar zenith angle and cloud cover', 'The colour of the sampling filter and the sea state'],
      'Slide 32: “Variability of a*_phy (a factor of 4): Discretisation effect or/and internal pigment concentration?”. Slide 34 adds photoadaptation: a high-light acclimated cell has a lower a*_ph.', 2, 'Package effect', src='Lecture, slides 32–34')
    A('How does Chl-specific absorption a*_ph(440) change from low Chl (0.03 mg m⁻³) to high Chl (≈ 10 mg m⁻³) on slide 32?',
      'It decreases (from roughly 0.1 to 0.02 m² mg⁻¹, read from the graph)', ['It increases by a factor of 4', 'It is constant', 'It oscillates with the Sun angle'],
      'Slide 32 (Bricaud et al., 1995): a*_ph(412) and a*_ph(443) fall from about 0.1–0.15 m² mg⁻¹ at Chl ≈ 0.05 to about 0.01–0.02 at Chl ≈ 10–20 (values read from graph, ±20 %). a_φ itself still increases with Chl (slide 72), but less than proportionally.', 2, 'Package effect', src='Lecture, slides 32, 72')
    A('For a spherical cell, Q*_a = (3/2) Q_a(ρ)/ρ with ρ = (intracellular absorption) × (cell diameter). What is Q*_a for ρ = 1?',
      f'≈ {PK["1.0"]:.2f}', [f'≈ {PK["0.05"]:.2f}', f'≈ {PK["5.0"]:.2f}', '≈ 1.50'],
      f'Closed form (Morel & Bricaud 1981) = {PK["1.0"]:.3f}, confirmed by numerical ray-path integration through the sphere (verified.json). ρ is an illustrative parameter, not a lecture number. Q*_a → 1 for small ρ and decreases toward 0 for large ρ.', 3, 'Package effect', origin='bo_sung', src='Lecture slide 33 (concept); home-made check')
    A('How does the lecture describe the absorption by non-algal particles (NAP) in the spectrum?',
      'It increases exponentially from long to short wavelengths; on average S = 0.011 nm⁻¹', ['It has a narrow peak at 675 nm', 'It is constant with wavelength', 'It increases from blue to red'],
      'Slide 35 (OCR text): “Absorption exponentially increase from long to short wavelengths. On average S = 0.011 (Roesler et al., 1989; Bricaud et al., 1998)”; measured on filters using the Kishino et al. (1985) technique. Slides 36–38 show the spectra.', 1, 'NAP', src='Lecture, slides 35–38')
    A('On slide 38, what does the linear regression of a*_m (mass-specific absorption) on [Fe] show for mineral particles?',
      'Absorption in the UV/blue increases with iron content (R² = 0.88 at 300 nm, 0.84 at 400 nm, 0.59 at 500 nm)', ['Absorption decreases with iron content at all wavelengths', 'There is no relation', 'The relation is perfect (R² = 1) at every wavelength'],
      'Slide 38 (Babin & Stramski 2004): a*(300) = 0.033[Fe] + 0.052; a*(400) = 0.031[Fe] − 0.043; a*(500) = 0.017[Fe] − 0.036, [Fe] in %.', 2, 'NAP', src='Lecture, slide 38')
    A('What size of matter is called “coloured dissolved organic matter” on slide 41?',
      'Matter with a diameter smaller than 0.2 µm (it passes through the filter)', ['Matter larger than 100 µm', 'Only the matter in the sediment', 'Only living cells'],
      'Slide 41 definition: “matter with diameter lower than 0.2 µm”; consistent with slide 61: a 0.2 µm filter at the entrance of the meter gives only CDOM absorption.', 1, 'CDOM', src='Lecture, slides 41, 61')
    A('Which model describes CDOM absorption in the lecture, and with which average slope?',
      'a(λ) = a(λ₀) exp[−S′(λ − λ₀)] with S′ ≈ 0.014 nm⁻¹ on average', ['a(λ) = a(λ₀)(λ/λ₀)^+2 with no free parameter', 'a(λ) = a(λ₀) exp[+S′(λ − λ₀)]', 'a(λ) = constant × cos λ'],
      'Slide 41 (Bricaud et al., 1981); the textbook (Colored Dissolved Organic Matter) agrees: S_g most commonly ≈ 0.014 nm⁻¹, varying from 0.007 to 0.026. Twardowski et al. (2004) alternative: a_ds ∝ λ^−6.92.', 1, 'CDOM', src='Lecture, slide 41; Textbook: Colored Dissolved Organic Matter')
    A('A water has a_cdom(412) = 0.30 m⁻¹ and S′ = 0.014 nm⁻¹. What is a_cdom(443)?',
      f'≈ {0.3*c443:.3f} m⁻¹', [f'≈ {0.3/c443:.3f} m⁻¹ (wrong sign in the exponent)', '≈ 0.30 m⁻¹ (no spectral change)', f'≈ {0.3*math.exp(-0.014*431):.4f} m⁻¹ (λ₀ forgotten)'],
      f'a(443) = 0.30 × exp(−0.014 × 31) = 0.30 × {c443:.3f} = {0.3*c443:.3f} m⁻¹ (Python, closed form vs log-fit).', 2, 'Calculation', src='Lecture, slide 41')
    A('How much larger is a_cdom(350) than a_cdom(440) for S′ = 0.014 nm⁻¹, and how much for NAP with S = 0.011 nm⁻¹?',
      f'CDOM: ×{r350:.2f}; NAP: ×{nr350:.2f}', [f'CDOM: ×{nr350:.2f}; NAP: ×{r350:.2f}', 'Both ×1.26 (the ratio of wavelengths)', f'CDOM: ×{math.exp(0.014*9):.2f}; NAP: ×{math.exp(0.011*9):.2f}'],
      f'exp(S × 90 nm): exp(1.26) = {r350:.2f} and exp(0.99) = {nr350:.2f}. The steeper CDOM slope makes it dominate the UV–blue compared with NAP (Python).', 2, 'Calculation', src='Lecture, slides 35, 41')
    A('Which kind of CDOM has a high slope S′, according to slide 41?',
      'CDOM dominated by fulvic acid (marine origin); low S′ means humic acid (terrestrial)', ['CDOM dominated by humic acid (terrestrial)', 'CDOM produced by bubbles', 'CDOM with no organic carbon'],
      'Slide 41: “High S′: CDOM dominated by fulvic acid (marine origin). Low S′: CDOM dominated by humic acid (terrestrial).” Slide 42 (right) shows that the slope tends to decrease as a_cdom(443) increases.', 2, 'CDOM', src='Lecture, slides 41–42')
    A('Why are a_cdom and a_nap combined into a_cdm in algorithms (slide 43)?',
      'Their spectral shapes are similar, and a_cdm is dominated about 90 % by CDOM at global scale (Siegel et al., 2002)', ['They are identical in magnitude everywhere', 'Because NAP does not absorb', 'Because CDOM and NAP both fluoresce at 685 nm'],
      'Slide 43: “Due to their similar spectral shapes, a_cdom and a_nap are gathered to form a_cdm (for algorithm applications). a_cdm is dominated at 90 % by CDOM at global scale (Siegel et al., 2002).”', 1, 'a_cdm', src='Lecture, slide 43')
    A('In the global maps of slide 44 (Bricaud et al., 2012), what pattern do the subtropical gyres show?',
      'Lowest Chl and a_cdm and highest S_cdm', ['Highest Chl and a_cdm and lowest S_cdm', 'High a_cdm and high Chl', 'No difference from coastal waters'],
      'Slide 44, May 2007: gyres in violet (Chl < 0.05), a_cdm(443) < 0.01 m⁻¹ (dark blue) and S_cdm ≈ 0.02–0.03 nm⁻¹ (orange); coasts and high latitudes show high a_cdm and lower S_cdm.', 2, 'a_cdm', src='Lecture, slide 44')
    A('Slide 45 compares the absorption budget in Case 1 and Case 2. Which statement is correct?',
      'In Case 1 the total has a minimum in the blue at ≈ 0.03 m⁻¹ set by water and Chl; in Case 2 the scale is 10 times larger and the minimum moves to ≈ 570 nm', ['In both cases the total minimum is at 700 nm', 'Case 2 absorbs ten times less than Case 1', 'Water is the dominant absorber at 400 nm in Case 2'],
      'Slide 45 (read from graph, ±10 %): Case 1 y-axis 0–0.08 m⁻¹, Case 2 y-axis 0–0.8 m⁻¹; in Case 2 mineral (“Min”) and CDOM absorption are large in the blue.', 3, 'Budget', src='Lecture, slide 45')
    B.essay('(a) Name the absorbing constituents of sea water and give for each its spectral signature. (b) Explain the package effect and why a*_ph decreases with Chl. (c) Compute a_cdom(443) from a_cdom(412) = 0.30 m⁻¹ (S′ = 0.014) and the ratio a_cdom(350)/a_cdom(440).',
            f'(a) Water (rises beyond 550 nm), phytoplankton (peaks ≈ 443 and 675 nm, carotenoids 450–500), NAP and CDOM (exponential increase to the blue; slopes 0.011 and 0.014 nm⁻¹) (slides 24, 28–29, 35, 41). (b) Q*_a = a_φ/a_sol falls from 1 toward 0 as cells get larger; Chl and cell size increase together (slide 33), so a*_ph falls (slide 32). (c) 0.30·e^(−0.014·31) = {0.3*c443:.3f} m⁻¹; e^(0.014·90) = {r350:.2f}.',
            2, 'Absorption', src='Lecture, slides 24, 28–41')
    B.essay('Compare the absorption budget of a Case 1 and of a Case 2 water (slide 45). Which constituents control the spectrum in each case and where is the minimum of the total absorption?',
            'Case 1 (y-scale 0–0.08 m⁻¹): water and Chl a set the spectrum, minimum ≈ 0.03 m⁻¹ near 400–420 nm; Chl bumps at ≈ 440 and 675 nm; CDOM decays with λ. Case 2 (y-scale 0–0.8 m⁻¹): mineral particles and CDOM raise the blue absorption, the total decreases to a minimum ≈ 0.2 m⁻¹ near 570 nm, then water increases it again. Values are read from the graph (±10 %).',
            2, 'Budget', src='Lecture, slide 45')

    sl = [
        S('Phytoplankton pigments', cols(LS(29, 430, 'Lecture slide 29 (Bricaud et al., 2004)'), dul(['Chl a: 443 and 675 nm', 'Carotenoids: 450–500 nm', 'Chl c: 465 and 635 nm', 'Phaeopigments']), flex=[3, 2])),
        S('Variability of specific absorption', cols(LS(32, 430, 'Lecture slide 32 (Bricaud et al., 1995; 2004)'), dul(['a*<sub>ph</sub> varies by ≈ ×4', 'Falls as Chl increases', 'Package effect or pigment content?']), flex=[3, 2])),
        S('The package effect', cols(LS(33, 430), dul(['Q*<sub>a</sub> = a<sub>φ</sub>/a<sub>sol</sub>', '1 = no packaging', '→ 0 = maximal packaging', 'Cells larger at high Chl']), flex=[3, 2])),
        S('Package factor of a sphere', img('package_effect', 700, cap='Own computation: Q*<sub>a</sub> versus ρ = (intracellular absorption) × (diameter); verified by two methods')),
        S('Non-algal particles', cols(LS(37, 430, 'Lecture slide 37 (Babin &amp; Stramski, 2004)'), dul(['Exponential increase to the blue', 'S ≈ 0.011 nm⁻¹ (slide 35)', 'Iron content raises UV–blue absorption (slide 38)']), flex=[3, 2])),
        S('CDOM absorption model', cols(LS(41, 430), dul(['a(λ) = a(λ₀) exp[−S′(λ−λ₀)]', 'S′ ≈ 0.014 nm⁻¹', 'High S′: fulvic (marine)', 'Low S′: humic (terrestrial)']), flex=[3, 2])),
        S('Spectral shapes of CDOM and NAP', img('exp_absorption', 1160, cap='Own computation, normalised at 440 nm: exponential laws S = 0.014 and 0.011 nm⁻¹ and the λ<sup>−6.92</sup> alternative')),
        S('Absorption budget in two water types', cols(LS(45, 430), dul(['Case 1: minimum in the blue', 'Case 2: ×10 larger scale', 'Case 2 minimum near 570 nm', 'Water + Chl + CDOM + NAP']), flex=[3, 2])),
        S('Key points', dul(['Chl a peaks 443 and 675 nm', 'Package effect: Q*<sub>a</sub> from 1 to 0', 'CDOM S′ = 0.014; NAP S = 0.011 nm⁻¹', 'a<sub>cdm</sub> = a<sub>cdom</sub> + a<sub>nap</sub>, ≈ 90 % CDOM'], xl=True)),
    ]
    mod = dict(id='mc', slug='03-absorption', title='C · Absorption', en='Phytoplankton, non-algal particles, CDOM and a_cdm (slides 28–45)',
               qtitle='Guiding question: who absorbs light in the sea, at which wavelengths, and how does packaging change it?',
               question='<p>Absorption by phytoplankton, non-algal particles (NAP) and coloured dissolved organic matter (CDOM) is added to that of water (module B). Each has a distinct spectral signature, which is what allows us to separate them.</p>',
               sections=[
                ('Phytoplankton absorption and the package effect', '<p>Pigments absorb in the blue (Chl a 443 nm, carotenoids 450–500 nm, Chl c 465 nm) and Chl a, b, c also in the red (675, 650, 635 nm) (slides 28–29). The Chl-specific absorption a*<sub>ph</sub> = a<sub>ph</sub>/Chl falls with Chl because of the <b>package effect</b>:</p>'
                 + eq('Slide 33', 'Q*<sub>a</sub>(λ) = a<sub>φ</sub>(λ)/a<sub>sol</sub>(λ); &nbsp; a<sub>sol</sub>(λ) = Σ<sub>i</sub> C<sub>i</sub> a*<sub>sol,i</sub>(λ)') +
                 f'<p>Home-made check for a homogeneous sphere (Morel &amp; Bricaud 1981 form, verified by ray-path integration): Q*<sub>a</sub> = {PK["0.2"]:.2f}, {PK["1.0"]:.2f}, {PK["5.0"]:.2f} for ρ = 0.2, 1, 5. ρ is an illustrative parameter. Photoacclimation also lowers a*<sub>ph</sub> at high light (slide 34).</p>'),
                ('Non-algal particles and CDOM', '<p>NAP (detritus, heterotrophic bacteria, minerals) and CDOM both increase exponentially toward short wavelengths (slides 35, 41): '
                 + eq('Exponential model', 'a(λ) = a(λ₀) exp[−S(λ − λ₀)]; &nbsp; S′<sub>CDOM</sub> ≈ 0.014 nm⁻¹; &nbsp; S<sub>NAP</sub> ≈ 0.011 nm⁻¹') +
                 f'</p><p><b>Numerical examples (Python).</b> a<sub>cdom</sub>(443)/a<sub>cdom</sub>(412) = {c443:.3f}; NAP: {n443:.3f}; a(350)/a(440) = {r350:.2f} for CDOM and {nr350:.2f} for NAP. Because the shapes are close, algorithms use a<sub>cdm</sub> = a<sub>cdom</sub> + a<sub>nap</sub>, about 90 % CDOM at global scale (slide 43).</p>'),
                ('Budget in Case 1 and Case 2', '<p>Slide 45 compares the contribution of water, Chl, CDOM and minerals to the total absorption in Case 1 (axis 0–0.08 m⁻¹) and Case 2 (axis 0–0.8 m⁻¹). In Case 1, water and Chl control the spectrum; in Case 2, minerals and CDOM raise the blue absorption and move the minimum of the total toward ≈ 570 nm (read from graph, ±10 %).</p>')],
               checklist=['Name the pigment peaks (Chl a 443/675, carotenoids 450–500, Chl c 465/635).', 'Define Q*_a and explain why a*_ph decreases with Chl.', 'Write the exponential model; give S′ ≈ 0.014 (CDOM) and S ≈ 0.011 (NAP).', 'Explain a_cdm = a_cdom + a_nap.', 'Describe the absorption budget of Case 1 vs Case 2.'],
               summary=['Sắc tố hấp thụ xanh (443 nm) và đỏ (675 nm); hiệu ứng gói làm a*_ph giảm khi Chl tăng.', 'CDOM và NAP hấp thụ tăng theo hàm mũ về phía xanh (S′ ≈ 0,014; S ≈ 0,011).', 'a_cdm ≈ 90 % là CDOM ở quy mô toàn cầu.'],
               calcs=[('expabs', 'CDOM/NAP exponential absorption'), ('package', 'Package effect Q*_a')], quiz_n=10,
               v2=dict(we_title='From 412 to 443 nm', we=f'<p>a<sub>cdom</sub>(412) = 0.30 m⁻¹, S′ = 0.014 nm⁻¹ ⇒ a<sub>cdom</sub>(443) = 0.30·e<sup>−0.014·31</sup> = {0.3*c443:.3f} m⁻¹. The e-folding distance is 1/S′ = 71 nm: every 71 nm toward the red the absorption drops by a factor e.</p>',
                       qa=[('Why does a*_ph drop when Chl rises?', 'Cells are larger and pigments shade each other (package effect, slides 32–33).'), ('How is NAP measured?', 'On filters with the Kishino et al. (1985) technique (slide 35).')],
                       hooks=[('CDOM and NAP: exponential, steep to the blue.', 'CDOM, NAP: hàm mũ, dốc về phía xanh.'), ('Big cell = less absorption per pigment.', 'Tế bào lớn hấp thụ ít hơn trên mỗi sắc tố.')]))
    return mod, sl, B
