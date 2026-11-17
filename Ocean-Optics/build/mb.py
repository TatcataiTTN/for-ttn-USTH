# -*- coding: utf-8 -*-
"""Module B — Pure water (slides 20-27)."""
import math
from lib import *
from qcore import Bank
from ma import LS
V = VERIFIED

def build():
    B = Bank('mb', seed=12); A = B.add
    W = V['pure_water_bw']
    b500_37, b500_0 = W['morel_500_S37']['b_w'], W['morel_500_S0']['b_w']
    r_m, r_b, r_r = V['ratio_450_550_morel'], V['ratio_450_550_buiteveld'], V['ratio_450_550_rayleigh_lam4']
    A('What physical cause of scattering by pure sea water does slide 20 give (Einstein–Smoluchowski theory)?',
      'Fluctuations of the density of the medium, accentuated by fluctuations of the ionic concentration', ['Scattering by dust and phytoplankton that cannot be removed', 'Reflection of light on the walls of the instrument', 'Absorption followed by re-emission as fluorescence'],
      'Slide 20: “Calculated from the Einstein–Smoluchowski theory (scattering is due to the fluctuation of density of the medium, which is accentuated by the fluctuation of the ionic concentration).” The textbook adds that β_w is one of the few IOPs that can be computed from fundamental physics.', 1, 'Pure water VSF', src='Lecture, slide 20; Textbook: Physics of Scattering')
    A('In the Morel (1974) formula of slide 20, which factor makes the scattering of sea water larger than that of fresh water?',
      'The factor (1 + 0.3 S/37), which gives +30 % at S = 37', ['The factor (λ/500 nm)^−4.32', 'The factor 10⁻⁴', 'The depolarisation term (1−δ)/(1+δ)'],
      'Slide 20 writes “S impact: 30 %”: (1 + 0.3·37/37) = 1.30. The salinity term is fixed from laboratory experiments, the λ-dependence is a fit to theoretical calculations.', 1, 'Pure water VSF', src='Lecture, slide 20')
    A('What is the wavelength dependence of the pure-water volume scattering function in the Morel (1974) formula, and what replaced it in Buiteveld et al. (1994)?',
      'β_w ∝ λ^−4.32 in Morel 1974, becoming λ^−4.14 in Buiteveld 1994', ['β_w ∝ λ^+4.32, then λ^+4.14', 'β_w ∝ λ^−1 in both formulas', 'β_w ∝ λ^−2 in Morel, λ^0 in Buiteveld'],
      'Slides 20 and 23. The change comes from the reformulation of the refractive index and from accounting for the compressibility isotherm of water (slide 23).', 1, 'Pure water VSF', src='Lecture, slides 20, 23')
    A('What is the depolarisation factor δ in the Morel (1974) and in the Buiteveld et al. (1994) formulas?',
      '0.09 in Morel (1974); 0.051 in Buiteveld et al. (1994)', ['0.051 in Morel (1974); 0.09 in Buiteveld et al. (1994)', '0.5 in both', '0.0 in both'],
      'Slide 20 (δ = 0.09) and slide 23 (δ = 0.051, in red). The textbook, using Zhang et al. (2019), gives a depolarisation ratio ρ = 0.031 for pure water at 546 nm.', 2, 'Pure water VSF', src='Lecture, slides 20, 23; Textbook: Physics of Scattering')
    A('In the pure-water VSF of slide 22, where is β_w smallest and where largest?',
      'Smallest near 90°, largest at 0° and 180° (a symmetric U-shape)', ['Smallest at 0°, largest at 90°', 'Smallest at 180°, largest at 0° (strongly forward-peaked)', 'Constant at all angles'],
      'Slide 22: three parallel curves (350, 450, 550 nm; shorter wavelength higher) with a minimum at ψ = 90°. The (1 + cos²θ·(1−δ)/(1+δ)) factor makes forward and backward equal, so b_bw = b_w/2.', 1, 'Pure water VSF', src='Lecture, slide 22')
    A('What does the symmetry of the pure-water VSF imply for the ratio b_bw/b_w?',
      f'b_bw/b_w = 0.5 (half of the scattering is backward)', ['b_bw/b_w = 0.01, as for particles', 'b_bw/b_w = 1', 'b_bw/b_w = 0.09, the depolarisation factor'],
      f'Because β_w(θ) = β_w(π − θ), the integral from π/2 to π is half of the total: Python gives b_bw/b_w = {V["bbw_over_bw_500"]:.3f} (verified.json). Particles are much more forward-peaked (module D).', 2, 'Pure water VSF', src='Lecture, slides 20, 22')
    A('Pure water scatters more at 450 nm than at 550 nm. With the exponent −4.32 of slide 20, by what factor?',
      f'≈ {r_m:.2f}', [f'≈ {(550/450):.2f} (simple ratio of wavelengths)', f'≈ {(550/450)**2:.2f} (inverse square)', f'≈ {(550/450)**8:.1f} (exponent mis-applied twice)'],
      f'(550/450)^4.32 = {r_m:.3f}. With −4.14: {r_b:.3f}; with a pure Rayleigh λ⁻⁴: {r_r:.3f}. Python, two methods (closed form and numerical integration of the whole VSF) agree (data/verified.json).', 2, 'Calculation', src='Lecture, slides 20, 23')
    A('Using the slide-20 formula with S = 37 and the cos²θ reading of the angular term, which is the order of magnitude of b_w(500 nm)?',
      f'≈ {b500_37*1e3:.1f} × 10⁻³ m⁻¹', [f'≈ {b500_37*1e2:.1f} × 10⁻² m⁻¹', f'≈ {b500_37:.1f} m⁻¹', f'≈ {b500_37*1e5:.1f} × 10⁻⁵ m⁻¹'],
      f'b_w = 2π∫β sinθ dθ = 2πβ(90°)(2 + 2k/3), k = (1−δ)/(1+δ). Python: {b500_37:.3e} m⁻¹ (quad and closed form agree). This is consistent with the b_w curve of slide 24, which is near 3×10⁻³ m⁻¹ at 500 nm (read from the graph, about 10 % accuracy).', 2, 'Calculation', src='Lecture, slides 20, 24')
    A('How much does b_w(500 nm) change between fresh water (S = 0) and sea water (S = 37) in the slide-20 formula?',
      f'It increases by 30 % (from {b500_0*1e3:.2f} to {b500_37*1e3:.2f} × 10⁻³ m⁻¹)', ['It doubles', 'It decreases by 30 %', 'It does not change'],
      f'The salinity factor is (1 + 0.3 S/37) = 1.30 at S = 37, so {b500_0:.3e} → {b500_37:.3e} m⁻¹.', 1, 'Calculation', src='Lecture, slide 20')
    A('Slide 24 shows the spectra of a_w and b_w for pure sea water between 400 and 700 nm. Which statement is correct?',
      'a_w has a minimum in the blue (≈ 0.005 m⁻¹ near 415 nm) and rises strongly beyond 550 nm, while b_w decreases smoothly with wavelength', ['a_w and b_w both increase with wavelength', 'b_w is larger than a_w at every wavelength', 'a_w is constant and b_w has absorption bands'],
      'Slide 24 (Pope & Fry 1997 for a_w; Morel 1974 for b_w). Values are read from a log graph (±10–20 %). The curves cross near 430–440 nm.', 1, 'Spectra', src='Lecture, slide 24')
    A('Why can the lecture say “It is never finished!!” about pure-water absorption (slides 25–26)?',
      'Different data sets disagree in the blue/UV and new measurements in very clear waters (2007) gave values lower than those accepted', ['Because pure water changes colour every year', 'Because the Sun has changed its spectrum', 'Because the formula for scattering was proven wrong in 2007'],
      'Slide 25: Zheng & Fry, Pope & Fry, Smith & Baker, Quickenden & Irvin and Boivin et al. differ in the UV and blue (Smith & Baker is about three times higher near 415 nm). Slide 26: Morel et al. (2007) found a_tot as low as 0.045 m⁻¹ at 310 nm, half the value generally accepted for pure water.', 2, 'Spectra', src='Lecture, slides 25–26')
    A('According to the abstract on slide 26 (Morel et al., 2007), which statement is correct for the South Pacific gyre?',
      'The total absorption has a flat minimum of about 0.007 m⁻¹ around 410–420 nm, about twice that of pure water', ['The total absorption is zero in the visible', 'The backscattering is dominated by phytoplankton in the UV', 'The particulate absorption is 85 % of the total absorption'],
      'Slide 26: a_tot ≈ 0.007 m⁻¹ at 410–420 nm; particulate absorption represents only ≈ 15 % of a_tot in the 305–420 nm domain; backscattering is totally dominated by water molecules in the UV.', 2, 'Spectra', src='Lecture, slide 26')
    A('What does slide 21 show about the dependence of pure-water backscattering on temperature and salinity?',
      'Backscattering relative to S = 38.4, T = 20 °C varies between about 0.75 and 1.1; salinity matters more than temperature', ['It is independent of both', 'It varies by a factor of 100', 'It depends on temperature only'],
      'Slide 21: colour maps of b_bw(443) and b_bw(547) divided by the value at T = 20 °C, S = 38.4 for T = 0–40 °C and S = 0–40 g kg⁻¹; the ratio is lowest (≈ 0.75) at S = 0.', 2, 'Temperature and salinity', src='Lecture, slide 21')
    A('The textbook computes β_w(90°, 546 nm) from Einstein–Smoluchowski theory. Which value does it give?',
      '0.869 × 10⁻⁴ m⁻¹ sr⁻¹ (close to the often-cited 0.83 × 10⁻⁴ of Morel 1974)', ['8.69 m⁻¹ sr⁻¹', '0.869 × 10⁻⁴ m⁻¹ without sr⁻¹', '0.869 × 10⁻² m⁻¹ sr⁻¹'],
      f'Textbook, Physics of Scattering, with ρ = 0.031 (Zhang et al. 2019). Our recomputation from the listed constants gives {V["es_beta90_546_textbook_constants"]:.3e} (1.7 % lower than the stated value). The slide-20 formula at 546 nm, S = 0 gives {V["beta90_546_morel_S0"]:.3e}: the lecture formula is about 10 % above the textbook value (see Sources & limits).', 3, 'Textbook vs lecture', origin='bo_sung', src='Textbook: Physics of Scattering')
    A('Why is the pure-water VSF of the lecture said to come from theory, while a_w cannot?',
      'Scattering by pure water follows from fundamental physics (density fluctuations), whereas absorption must be measured', ['Because absorption is always zero', 'Because scattering was measured in space', 'Because absorption can be computed exactly from Maxwell’s equations in any liquid'],
      'Textbook (Physics of Scattering): scattering by pure water is one of the few IOPs that can be computed from fundamental physics; absorption coefficients are obtained from measurements — hence the data-set differences of slides 25–26.', 3, 'Textbook vs lecture', origin='bo_sung', src='Textbook: Physics of Scattering')
    B.essay('(a) Write the Morel (1974) and the Buiteveld et al. (1994) formulas for β_w and list what changed. (b) Compute b_w at 500 nm for S = 37 from the Morel formula. (c) Compare the scattering of pure water at 450 and 550 nm.',
            f'(a) β_w = 1.38 (λ/500)^−4.32 (1+0.3S/37) 10⁻⁴ [1 + cos²θ (1−δ)/(1+δ)], δ = 0.09; Buiteveld: 1.29, −4.14, δ = 0.051 (slides 20, 23). (b) b = 2πβ(90°)(2 + 2k/3), k = 0.835: b_w(500) = {b500_37:.2e} m⁻¹ (S = 37; {b500_0:.2e} for S = 0). (c) (550/450)^4.32 = {r_m:.2f} (4.14: {r_b:.2f}).',
            2, 'Pure water VSF', src='Lecture, slides 20, 23')
    B.essay('Explain with the lecture why “pure water” is not a closed question: summarise slides 24–26 and the value of the clearest ocean waters. What does this mean for algorithms that need a_w?',
            'Slide 24: Pope & Fry (1997) a_w, Morel (1974) b_w. Slide 25: five data sets disagree in the blue/UV (Smith & Baker higher by ≈ 3× near 415 nm). Slide 26: Morel et al. (2007) in hyper-oligotrophic South Pacific waters: a_tot ≈ 0.007 m⁻¹ at 410–420 nm, ≈ 0.045 m⁻¹ at 310 nm (half the accepted value for pure water). Consequence: algorithms that subtract a_w inherit its uncertainty, largest in the blue/UV.',
            2, 'Spectra', src='Lecture, slides 24–26')

    sl = [
        S('Pure sea water: scattering formula', cols(LS(20, 420), dul(['Fit to theoretical calculations', 'Salinity factor fixed from lab experiments', 'Einstein–Smoluchowski: density fluctuations', 'Next slides: term by term']), flex=[3, 2])),
        S('Revision by Buiteveld et al. (1994)', cols(LS(23, 420), dul(['Amplitude: 1.38 → <b>1.29</b>', 'Spectral exponent: −4.32 → <b>−4.14</b>', 'Depolarisation: 0.09 → <b>0.051</b>', 'Refractive index and compressibility']), flex=[3, 2])),
        S('Buiteveld formula, term by term', EQS_('vsf_buit', fs=28)),
        S('Einstein–Smoluchowski scattering', EQS_('es', fs=30)),
        S('Morel (1974) formula, term by term', EQS_('vsf_main')),
        S('Total scattering of water', EQS_('bw_closed')),
        S('Pure-water VSF versus angle', img('vsf_water', 700, cap='Own computation from the slide-20 formula, S = 37 (compare lecture slide 22)')),
        S('Temperature and salinity effect', cols(LS(21, 420), dul(['Ratio to T = 20 °C, S = 38.4', 'Range 0.75 – 1.10', 'Salinity matters most', '+30 % for S = 37 (slide 20)']), flex=[3, 2])),
        S('Scattering of pure water: numbers', Ks(r'b_w(500\,\mathrm{nm},S=37)=' + sci(b500_37, 2) + r'\ \mathrm{m^{-1}}', r'b_w(500\,\mathrm{nm},S=0)=' + sci(b500_0, 2) + r'\ \mathrm{m^{-1}}\quad(+30\%\ \text{with salt})', r'b_{bw}/b_w=0.5\quad\text{(half is backward)}', r'\frac{b_w(450)}{b_w(550)}=\left(\frac{550}{450}\right)^{4.32}=%.2f' % r_m, r'\text{with the revised exponent }4.14:\ \ %.2f' % r_b, cap='Meaning: sea water scatters 30 % more than fresh water, half of it backward, and blue light about 2.4 times more than green.')),
        S('Pure-water absorption and scattering spectra', cols(LS(24, 430), dul(['Absorption minimum ≈ 0.005 m⁻¹ near 415 nm', 'Absorption rises beyond 550 nm', 'Scattering falls smoothly with λ', 'Curves cross near 430–440 nm']), flex=[3, 2])),
        S('Absorption in the blue and UV is uncertain', cols(LS(25, 430), dul(['Five data sets', 'Smith &amp; Baker ≈ 3× higher at 415 nm', 'New UV data (1994)']), flex=[3, 2])),
        S('The clearest natural waters', cols(LS(26, 430), dul(['Total absorption ≈ 0.007 m⁻¹ at 410–420 nm', '0.045 m⁻¹ at 310 nm', 'Half the accepted pure-water value', 'Particles ≈ 15 % of the total']), flex=[3, 2])),
        S('Key points', dul(['Scattering almost Rayleigh (λ⁻⁴·³); half of it backward', 'Salinity: +30 %; temperature: weak', 'Absorption minimum in the blue, strong rise in the red', 'Blue/UV absorption: data sets still disagree'], xl=True)),
    ]
    mod = dict(id='mb', slug='02-pure-water', title='B · Pure water', en='Pure-water absorption and scattering (slides 20–27)',
               qtitle='Guiding question: what are a_w and b_w, and how well do we know them?',
               question='<p>Water itself absorbs and scatters. In the clearest waters it dominates; everywhere else it is the baseline to which the other constituents are added (additivity). This module covers the pure-water VSF formulas of the lecture, their spectral dependence and the uncertainty on a_w.</p>',
               sections=[
                ('Scattering by pure water', '<p>Pure water scatters because its molecules move: density, and therefore the refractive index, fluctuate on scales much smaller than the wavelength (Einstein–Smoluchowski theory). The lecture gives the fitted VSF (slide 20, Morel 1974):</p>'
                 + EQ('vsf_morel') +
                 '<p>and its revision after 20 years (slide 23, Buiteveld et al. 1994). The slide prints the angular term as “cos2θ”; we read it as cos²θ (see below).</p>' + EQ('vsf_buit') + EQ('bw_closed') +
                 f'<div class="callout good"><b class="t">Home-made check (Python)</b>Integrating β<sub>w</sub> over 4π gives b<sub>w</sub>(500) = {b500_37*1e3:.2f}×10⁻³ m⁻¹ for S = 37, near the 3×10⁻³ m⁻¹ read from the b<sub>w</sub> curve of slide 24. The literal cos(2θ) would give {V["bw500_S37_cos2"]*1e3:.2f}×10⁻³ m⁻¹, too low, which supports the cos²θ reading. This is evidence, not proof.</div>'),
                ('Scattering from first principles', '<p>The textbook (<i>Physics of Scattering</i>) derives the same scattering from density fluctuations:</p>' + EQ('es')),
                ('Absorption by pure water', '<p>a<sub>w</sub> is low in the blue and rises quickly beyond 550 nm (slide 24, Pope &amp; Fry 1997). In the blue and UV, data sets differ (slide 25) and the 2007 study of the clearest waters (slide 26) suggests that true values can be lower than those accepted. For scattering we can compute from physics; for absorption we depend on measurements (textbook).</p>'
                 + EQ('a_water')),
                ('Numbers (all verified in Python)', f'<ul><li>Ratio of scattering 450 nm / 550 nm: {r_m:.2f} (−4.32), {r_b:.2f} (−4.14), {r_r:.2f} (λ⁻⁴).</li><li>b<sub>w</sub>(500) = {b500_37:.2e} m⁻¹ (S = 37); {b500_0:.2e} m⁻¹ (S = 0): +30 %.</li><li>Scattering length 1/b<sub>w</sub>(500, S=37) ≈ {V["tau_water_scattering_length_m_500_S37"]:.0f} m.</li><li>b<sub>bw</sub>/b<sub>w</sub> = 0.5 for the symmetric VSF.</li></ul>'
                 f'<div class="callout warn"><b class="t">Lecture vs textbook (not hidden)</b>The textbook quotes β<sub>w</sub>(90°, 546 nm) = 0.869×10⁻⁴ m⁻¹ sr⁻¹ (ρ = 0.031) and recalls 0.83×10⁻⁴ for Morel (1974). The slide-20 formula at 546 nm, S = 0 gives {V["beta90_546_morel_S0"]*1e4:.3f}×10⁻⁴ (Buiteveld form: {V["beta90_546_buiteveld_S0"]*1e4:.3f}×10⁻⁴). Our reading of the slide is that its constants include the S-dependent factor as printed; we did not find which convention makes the numbers agree, so we report the difference.</div>')],
               checklist=['Write the Morel formula, say which parts are theory and which laboratory (slide 20).', 'List the changes of Buiteveld et al. 1994 (1.29, −4.14, δ = 0.051).', 'Compute a ratio of scattering at two wavelengths with the exponent.', 'Sketch a_w and b_w (400–700 nm) and say where they cross.', 'Say why a_w in the blue/UV is still uncertain.'],
               summary=['β_w ∝ λ^−4.32 (Morel 1974), λ^−4.14 (Buiteveld 1994); muối làm tăng 30 %.', 'a_w cực tiểu ở vùng xanh, tăng mạnh sau 550 nm.', 'Hấp thụ của nước tinh khiết ở xanh/UV vẫn còn bất định.'],
               calcs=[('vsfw', 'Pure-water VSF and b_w')], quiz_n=10,
               v2=dict(we_title='Scattering ratio', we=KL(r'\frac{b_w(450)}{b_w(550)}=\left(\frac{550}{450}\right)^{4.32}=%.2f' % r_m, r'\text{revised exponent: }\left(\frac{550}{450}\right)^{4.14}=%.2f' % r_b, cap='The 3 % difference is smaller than the uncertainty on most field measurements.'),
                       qa=[('Is salinity or temperature more important for b_w?', 'Salinity (+30 % at S = 37; slide 20), temperature has a weak effect (slide 21).'), ('Where do a_w and b_w cross?', 'Near 430–440 nm on slide 24.')],
                       hooks=[('Blue sea = molecules scatter blue (λ^−4.3) and absorb red.', 'Biển xanh: phân tử tán xạ xanh, hấp thụ đỏ.')]))
    return mod, sl, B
