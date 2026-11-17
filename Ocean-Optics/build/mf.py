# -*- coding: utf-8 -*-
"""Module F — From IOPs to biogeochemical variables (slides 63-84)."""
import math
from lib import *
from qcore import Bank
from ma import LS
V = VERIFIED

def build():
    B = Bank('mf', seed=16); A = B.add
    bp = V['bp550_from_chl']; pm = V['poc_spm_from_ap_ratio']; mix = V['cdom_mixing_example']
    c_ex, c_mie, c_two = V['sum_N_sigma_c_example'], V['sum_N_sigma_c_with_mie_Q'], V['two_populations_total_c']
    two = V['two_populations_example']
    A('What does the formula IOP(λ) = Σ (N_i/V) σ_i(λ) = Σ (N_i/V) Q_i(λ) S_i (slide 63) say?',
      'An IOP is the sum over particle classes of number per m³ times cross-section, itself efficiency Q times geometric area S', ['An IOP is the product of the Chl concentration and the Sun angle', 'An IOP is the average of the particle diameters', 'An IOP is the square root of the volume of the sample'],
      'Slide 63: N/V in m⁻³, σ (IOP cross-section) in m², Q (efficiency factor, dimensionless), S (geometrical area) in m². Q is “the ratio of the radiant flux absorbed or scattered by a particle to the radiant flux incident onto the geometrical cross section of this particle”.', 1, 'ΣNσ', src='Lecture, slide 63')
    A('A population has N/V = 10⁷ m⁻³ spheres of radius 5 µm with Q = 2. What is its contribution to the attenuation coefficient?',
      f'≈ {c_ex*1e3:.2f} × 10⁻³ m⁻¹', [f'≈ {c_ex*1e2:.2f} × 10⁻² m⁻¹ (area of the diameter used)', f'≈ {c_ex*1e6:.2f} m⁻¹ (units of µm kept)', f'≈ {c_ex/2*1e3:.2f} × 10⁻³ m⁻¹ (Q = 1)'],
      f'c = (N/V) Q π r² = 10⁷ × 2 × π (5×10⁻⁶)² = {c_ex:.3e} m⁻¹ (Python). With the Mie efficiency of a 5 µm sphere of index 1.05 at 550 nm (Q = {V["mie_qext_r5um_550nm_m105"]:.2f}, not 2) the result would be {c_mie:.2e} m⁻¹.', 2, 'Calculation', src='Lecture, slide 63')
    A('Two populations: small (r = 0.5 µm, N = 10¹¹ m⁻³, Q = 0.9) and large (r = 10 µm, N = 10⁶ m⁻³, Q = 2). Which one contributes more to c, and by what factor?',
      f'The small population, ≈ {two["small"]["c_m1"]/two["large"]["c_m1"]:.1f} times more ({two["small"]["c_m1"]*1e3:.1f} vs {two["large"]["c_m1"]*1e3:.2f} × 10⁻³ m⁻¹)', ['The large population, by a factor 10', 'Both contribute equally', 'The large one, because Q is larger'],
      f'σ = QπR²: small {two["small"]["sigma_m2"]:.2e} m², large {two["large"]["sigma_m2"]:.2e} m²; times N: {two["small"]["c_m1"]:.2e} and {two["large"]["c_m1"]:.2e} m⁻¹ (total {c_two:.2e}). Numerous small particles often dominate the total cross-section (illustrative numbers).', 3, 'Calculation', origin='bo_sung', src='Lecture, slide 63')
    A('According to slide 64, which particle size range obeys geometric optics and which Rayleigh scattering?',
      'Large particles: geometric optics with diffraction (response ∝ area); small particles: Rayleigh (response ∝ volume)', ['Large: Rayleigh; small: geometric', 'Both: geometric optics', 'Both: Rayleigh'],
      'Slide 64; sphere in between: Mie scattering; analytical solutions exist for spheroids too.', 1, 'Size', src='Lecture, slide 64')
    A('Which empirical relation between particulate scattering and chlorophyll is quoted on slide 65 (Loisel & Morel, 1998)?',
      'b_p(550) = 0.30 [Chl]^0.7', ['b_p(550) = 30 [Chl]^−2', 'b_p(550) = [Chl] exactly', 'b_p(550) = 0.30 exp(−0.014 [Chl])'],
      f'Slide 65: b_p(550) = 0.30(±0.15)[Chl]^0.7(±0.1). Python: {bp["0.1"]:.3f}, {bp["1.0"]:.2f}, {bp["10.0"]:.2f} m⁻¹ for Chl = 0.1, 1, 10 mg m⁻³. A relation with spread, valid for Case-1 waters.', 1, 'b_p vs Chl', src='Lecture, slide 65')
    A('If Chl increases tenfold, by what factor does b_p(550) = 0.30 Chl^0.7 increase?',
      f'≈ {V["bp550_tenfold_chl_factor"]:.1f} (less than proportionally)', ['10 (proportional)', '≈ 1.7', '≈ 0.2'],
      f'10^0.7 = {V["bp550_tenfold_chl_factor"]:.2f} (Python, two evaluations agree). An exponent below 1 means that particles per unit Chl decrease as Chl increases.', 2, 'b_p vs Chl', src='Lecture, slide 65')
    A('What is the main result of slide 66 on attenuation and scattering?',
      'c_p and b_p follow particle load (POC, surface area, SPM) with scatter of about a factor 2–3 across regions', ['They are unrelated to POC and SPM', 'They only depend on temperature', 'They are exactly proportional with R² = 1'],
      'Slide 66: c_p(660) vs POC (HOTS, BOFS: parallel bounding lines), c(555) vs particle surface concentration (y = 5.38 x^0.90, R² = 0.94), b_p(555) vs SPM across several seas, b(546) vs suspended calcite. The spread is read from the graph.', 2, 'b_p vs POC', src='Lecture, slide 66')
    A('On slide 68, Junge distribution N(D) = N₀ (D/D₀)^−ξ and c_p(λ) = A λ^−γ are related by what?',
      'ξ = γ + 3 (and, for small γ, ξ = γ + 3 − 0.5 exp(−6γ))', ['ξ = γ', 'ξ = 3γ', 'ξ = γ − 3'],
      f'Slide 68 (Boss et al., 2001), checked at 300 dpi. Home-made Mie check: for ξ = 4 we obtain n = {V["junge_ensemble_m105"]["4.0"]["n_bp"]:.2f} (γ = 1).', 2, 'Size', src='Lecture, slide 68')
    A('Slide 71 says that b_bp/b_p depends on refractive index first and size second. Which samples have the higher ratio?',
      'High POC/Chl samples (triangles), whose particles are more inorganic/higher-index', ['Low POC/Chl samples', 'Both have exactly the same ratio', 'Only samples at 0 °C'],
      'Slide 71 (Loisel et al., 2007): triangles (high POC/Chl) lie at b_bp/b_p ≈ 0.015–0.035, dots (low POC/Chl) at ≈ 0.005–0.015 (read from graph). Contours show index 1.02–1.20.', 2, 'b_bp/b_p', src='Lecture, slide 71')
    A('Slide 72 shows a_p(440) and a_φ(440) versus Chl for N = 1166 samples. What is the main message?',
      'Both increase with Chl along a log–log line with r² ≈ 0.90–0.91, spread within a factor ≈ 2', ['They decrease with Chl', 'They are independent of Chl', 'They are exactly proportional to Chl'],
      'Slide 72 (Bricaud et al. 1995): a(440) ≈ 0.003 at Chl = 0.02 to ≈ 0.3 at Chl = 20 (read from graph).', 1, 'a_ph vs Chl', src='Lecture, slide 72')
    A('Slide 74 relates POC/SPM to the ratio a_p(675)/a_p(570). What is the relation and what does it mean?',
      'POC/SPM = 0.0133 exp{1.27 [a_p(675)/a_p(570)]}: the red-to-green absorption ratio indexes how organic the particles are', ['POC/SPM = 1.27 a_p(675)', 'POC/SPM is independent of the spectrum', 'POC/SPM = a_p(570)/a_p(675) exactly'],
      f'Slide 74 (Wozniak et al. 2010, r² = 0.81, n = 44). Python: ratio 1 → {pm["1.0"]:.3f}; ratio 2 → {pm["2.0"]:.3f}. Chl absorbs at 675 nm; minerals do not.', 2, 'POC/SPM', src='Lecture, slide 74')
    A('Why does the lecture ask “a_cdom vs Chl and DOC ????” (slide 75)?',
      'Because a_cdom correlates with Chl and DOC only regionally or in subsets; across all data the relation is weak', ['Because a_cdom is always proportional to Chl', 'Because DOC is not organic', 'Because Chl is a dissolved substance'],
      'Slide 75: a_cdom(443) vs Chl scatters over about 1.5 decades; a_cdom(355) vs DOC is linear in some regions (Rhine plume) and shows no relation in others. Slide 41: “No robust relationships with Chl (or a_phy) (except locally)”.', 2, 'CDOM vs DOC', src='Lecture, slides 41, 75')
    A('What differs between regional DOC : a_cdom relations on slide 76 (Mannino, 2012)?',
      'Their slopes: DOC per unit a_cdom increases from north (Gulf of Maine) to south, reflecting source material and photo-oxidation/seasonal change', ['All lines are identical', 'The slope is negative', 'They are unrelated to source materials'],
      'Slide 76: R² between 0.88 and 0.97 for each region/season; bullets on source materials (terrestrial DOM less degraded in the Gulf of Maine) and seasonal shift from accumulation of DOC (net community production) and photo-oxidation of CDOM.', 2, 'CDOM vs DOC', src='Lecture, slide 76')
    A('What does slide 77 (Blough & Del Vecchio, 2002) show for a_cdom(355) versus salinity?',
      'a_cdom decreases from ≥ 10 m⁻¹ in fresh water to ≈ 0.1 m⁻¹ or less in oceanic water: near-conservative mixing of end members that vary between systems', ['a_cdom increases with salinity', 'a_cdom is independent of salinity', 'a_cdom is the same in rivers and in gyres'],
      f'Slide 77 text. For linear mixing between end members 10 and 0.1 m⁻¹ (S_sea = 36, illustrative), a(18) = {mix["18"]:.2f} m⁻¹ (midpoint, Python). Curves bending below the line indicate non-conservative loss (photo-oxidation).', 2, 'CDOM vs salinity', src='Lecture, slide 77')
    A('What are the three main factors that influence Chl fluorescence (slide 78)?',
      'Chl-a concentration, pigment packaging and the photoprotective response (quenching)', ['Salinity, temperature and pressure', 'Sun angle, sea state and wind', 'Nitrate, phosphate and silicate'],
      'Slide 78. Slide 80: non-photochemical quenching is “a photoprotective response aimed at preventing high-light damage”.', 1, 'Fluorescence', src='Lecture, slides 78, 80')
    A('Slide 80 shows fluorescence versus HPLC Chl through a day. What happens around mid-day?',
      'Fluorescence drops (≈ 0.7 → 0.4) while the Chl concentration does not, because of non-photochemical quenching', ['Chl concentration drops by half and fluorescence stays constant', 'Both rise', 'Both are unrelated to light'],
      'Slide 80 (13 Mar 2008 data; credits Kiefer 1973b, Loftus & Seliger 1975): solar PAR peaks near 1150 µmol m⁻² s⁻¹; fluorescence recovers at night. So fluorescence must be corrected (see also Sackmann et al. 2008, slides 110–111).', 2, 'Fluorescence', src='Lecture, slides 80, 110–111')
    A('Slides 81–83 show diel cycles. Which signal has a clear day–night cycle that fluorescence misses?',
      'The particle attenuation c_p (and b_bp): it grows during the day and decays at night', ['The salinity', 'The pure-water absorption', 'The Earth–Sun distance'],
      'Slide 81: fluorescence shows a deep Chl maximum with no day–night cycle, while attenuation has maxima during the day; in density coordinates the deep maximum stays at density ≈ 24.5 kg m⁻³. Slide 82 explains: balance of production and losses (grazing, sinking, aggregation) plus a physiological cycle.', 2, 'Diel', src='Lecture, slides 81–83')
    A('What does slide 84 (Boss et al., 2004) show about the bloom and the nepheloid layer?',
      'The bloom has high c_p, Chl and b_bp but low b_bp/b_p (≈ 0.006); the near-bottom nepheloid layer has high b_bp/b_p (0.012–0.018)', ['The bloom has the highest b_bp/b_p', 'There is no change in b_bp/b_p', 'The nepheloid layer has the lowest density'],
      'Slide 84, section of 27 July 2000: b_bp/b_p separates organic-rich bloom water from sediment-dominated bottom water. Values read from the colour scales.', 2, 'b_bp/b_p', src='Lecture, slide 84')

    B.essay('(a) State IOP = Σ(N/V)σ = Σ(N/V)QS and define each symbol. (b) Compute the attenuation of 10⁷ m⁻³ spheres of radius 5 µm with Q = 2. (c) Explain why b_p grows less than proportionally with Chl (b_p = 0.30 Chl^0.7).',
            f'(a) N/V particles per m³; σ cross-section (m²); Q efficiency factor; S geometric area (slide 63). (b) c = 10⁷ × 2 × π(5×10⁻⁶)² = {c_ex:.2e} m⁻¹. (c) A tenfold Chl increase gives 10^0.7 = {V["bp550_tenfold_chl_factor"]:.1f}× more scattering: particle number and size per unit Chl change with trophic state (slide 65).',
            2, 'ΣNσ', src='Lecture, slides 63–65')
    B.essay('Discuss the link between CDOM absorption and (i) Chl, (ii) DOC, (iii) salinity using slides 75–77. What does it mean for a satellite algorithm estimating DOC from a_cdom?',
            'Chl: weak, regional only (slide 75). DOC: linear in each region/season with R² 0.88–0.97 but with slopes that change (slide 76), so one global relation is not possible. Salinity: near-conservative mixing between a high-CDOM fresh end member (≥ 10 m⁻¹ at 355 nm) and low-CDOM ocean (≤ 0.1 m⁻¹) (slide 77), end members vary between systems. A DOC algorithm needs a regional/seasonal calibration.',
            3, 'CDOM', src='Lecture, slides 75–77')
    B.essay('Explain fluorescence quenching and the diurnal cycle of attenuation (slides 78–83). How can b_bp/b_p (slide 84) help separate bloom from resuspension?',
            'Fluorescence depends on Chl, pigment packaging and non-photochemical quenching; at mid-day fluorescence falls ≈ 40 % while Chl does not (slide 80). Attenuation c_p and b_bp show growth by day and loss by night while fluorescence does not (slide 81–83). b_bp/b_p is low (≈ 0.006) in organic-rich bloom and high (0.012–0.018) in resuspended sediments (slide 84; index first, size second, slide 71).',
            2, 'Fluorescence and diel cycles', src='Lecture, slides 78–84')

    sl = [
        S('IOP from particle properties', cols(LS(63, 400), dul(['Sum over particle classes', 'Number × efficiency × area', 'σ in m², Q dimensionless', 'N/V in m⁻³']), flex=[3, 2])),
        S('IOP = Σ N Q S, symbol by symbol', EQS_('iop_sum')),
        S('Large and small particles', cols(LS(64, 430), dul(['Large: diffraction, ∝ area', 'Small: Rayleigh, ∝ volume']), flex=[3, 2])),
        S('Scattering and attenuation versus Chl', cols(LS(65, 430), dul(['Power law of Chl, exponent 0.7', 'Spread ≈ ×2–3', 'Case-1 relation']), flex=[3, 2])),
        S('Scattering from Chl, symbol by symbol', EQS_('bp_chl', fs=40)),
        S('Scattering versus particle load', cols(LS(66, 430), dul(['POC, particle surface, SPM', 'Roughly linear on log–log', 'Regional differences']), flex=[3, 2])),
        S('Size and the attenuation slope', cols(LS(68, 430), dul(['Junge power-law size distribution', 'Attenuation spectrum power law', 'The two slopes are linked by ξ = γ + 3']), flex=[3, 2])),
        S('Size distribution and attenuation slope', EQS_('powerlaw', fs=30)),
        S('Particle absorption and POC', cols(LS(74, 430), dul(['Red-to-green absorption ratio R', 'Exponential in R', 'r² = 0.81, n = 44']), flex=[3, 2])),
        S('POC/SPM, symbol by symbol', EQS_('poc_spm', fs=40)),
        S('CDOM versus DOC and salinity', cols(LS(77, 430), dul(['Fresh water ≥ 10 m⁻¹', 'Oceanic ≤ 0.1 m⁻¹', 'Near-conservative mixing', 'DOC relations regional (slide 76)']), flex=[3, 2])),
        S('Fluorescence quenching', cols(LS(80, 430), dul(['Chl, packaging, quenching', 'Fluorescence drops at mid-day', 'HPLC Chl does not']), flex=[3, 2])),
        S('Diel cycles', cols(LS(81, 430), dul(['c<sub>p</sub>: day growth, night loss', 'Fluorescence: no clear cycle', 'Density coordinates (slide 82)']), flex=[3, 2])),
        S('Bloom, front and nepheloid layer', cols(LS(84, 430), dul(['Bloom: b<sub>bp</sub>/b<sub>p</sub> ≈ 0.006', 'Nepheloid layer: 0.012–0.018', 'Boss et al., 2004']), flex=[3, 2])),
        S('Key points', dul(['IOP = Σ N Q S; Chl, POC, SPM set scattering', 'ξ = γ + 3', 'CDOM–DOC relations are regional', 'Fluorescence needs quenching correction'], xl=True)),
    ]
    mod = dict(id='mf', slug='06-iop-biogeochemistry', title='F · IOPs and biogeochemistry', en='From IOPs to Chl, POC, CDOM–DOC, fluorescence and diel cycles (slides 63–84)',
               qtitle='Guiding question: what biogeochemical variable does each IOP track, and how reliable is that link?',
               question='<p>Why do we care about IOPs? Because they track Chl, particulate organic carbon, dissolved organic carbon and size, and can be measured at high frequency. This module builds that link from the cross-section formula and reviews the field relations of slides 65–84, including their limits.</p>',
               sections=[
                ('From particles to IOPs', '<p>Each IOP is the sum over particle classes (slide 63):</p>' + EQ('iop_sum') +
                 f'<p><b>Example (Python).</b> 10⁷ m⁻³ spheres of 5 µm radius with Q = 2: c = {c_ex:.2e} m⁻¹; with the Mie Q ({V["mie_qext_r5um_550nm_m105"]:.2f}) {c_mie:.2e} m⁻¹. Small numerous particles can dominate the total cross-section: a population of 0.5 µm / 10¹¹ m⁻³ gives {two["small"]["c_m1"]*1e3:.1f}×10⁻³ m⁻¹, a population of 10 µm / 10⁶ m⁻³ only {two["large"]["c_m1"]*1e3:.2f}×10⁻³ m⁻¹.</p>'),
                ('Empirical relations and their spread', '<p>Each relation below is a regression with a spread; click the symbols to see the numbers.</p>' + EQ('bp_chl') + EQ('poc_spm') + EQ('mixing') + EQ('powerlaw') + '<ul><li><b>b<sub>bp</sub>/b<sub>p</sub></b> (slide 71): index first, then size.</li><li><b>CDOM</b>: weak link to Chl, regional links to DOC (slides 75–76), conservative mixing with salinity (slide 77).</li></ul>'
                 '<div class="callout warn"><b class="t">Limit</b>All these are regressions from specific data sets. They are not physical laws and must not be transferred to other water types (Big 12, K2).</div>'),
                ('Fluorescence, diel cycles and fronts', '<p>Fluorescence depends on Chl, pigment packaging and photoprotective quenching (slides 78, 80). Attenuation and b<sub>bp</sub> show daily cycles of growth and loss that fluorescence does not (slides 81–83). b<sub>bp</sub>/b<sub>p</sub> distinguishes a bloom (low) from a nepheloid layer (high) (slide 84).</p>')],
               checklist=['Write IOP = ΣNσ = ΣNQS and compute c for a population.', 'Quote b_p = 0.30 Chl^0.7 and say it is empirical (spread ×2–3).', 'Write ξ = γ + 3 and explain symbols.', 'Explain what b_bp/b_p reveals.', 'Explain quenching and the diel cycle of c_p.', 'Summarise CDOM vs Chl, DOC and salinity.'],
               summary=['IOP = Σ N·Q·S; tán xạ hạt đi theo Chl, POC, SPM với độ phân tán ×2–3.', 'ξ = γ + 3; b_bp/b_p phân biệt thực vật phù du với trầm tích.', 'Huỳnh quang bị dập tắt ban ngày; c_p có chu kỳ ngày đêm.'],
               calcs=[('sumns', 'IOP = Σ N·Q·S'), ('bpchl', 'b_p from Chl')], quiz_n=12,
               v2=dict(we_title='Tenfold more Chl', we=KL(r'b_p(550)=0.30\,[\mathrm{Chl}]^{0.7}:\quad 0.1\to%.3f,\ \ 1\to%.2f,\ \ 10\to%.2f\ \ \mathrm{m^{-1}}' % (bp["0.1"], bp["1.0"], bp["10.0"]), r'\text{tenfold more Chl: }\ 10^{0.7}=%.1f\ \text{times more scattering}' % V["bp550_tenfold_chl_factor"]),
                       qa=[('Can I use b_p = 0.30 Chl^0.7 in a river plume?', 'No: it is a Case-1 relation (slide 65); in Case 2 mineral particles do not co-vary with Chl.'), ('Why does fluorescence fall at noon?', 'Non-photochemical quenching (slide 80).')],
                       hooks=[('Regression ≠ law.', 'Hồi quy không phải định luật.'), ('Bloom: low b_bp/b_p; sediments: high.', 'Bloom: b_bp/b_p thấp; trầm tích: cao.')]))
    return mod, sl, B
