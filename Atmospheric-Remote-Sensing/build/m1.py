# -*- coding: utf-8 -*-
"""M1 — Sinks and lifetime of air pollutants (study guide Ch.1)."""
from lib import *
from lib import _PIL
from qcore import Bank
V = VERIFIED
CO = V['co_oh']

def build():
    B = Bank('m1', seed=1)
    # ---------------- QUIZ ----------------
    B.add('How is the atmospheric lifetime τ of a pollutant defined?',
          'τ = atmospheric burden M divided by the total loss rate L (τ = M / L)',
          ['τ = emission rate divided by the background concentration of the species',
           'τ = time for half of the species to disappear, i.e. τ = ln 2 / k',
           'τ = distance the molecule is carried by the wind divided by the wind speed'],
          'Study guide Ch.1: τ = M / L (steady state τ = M / P). For a first-order sink τ = 1/k′. The half-life t½ = τ·ln 2 ≈ 0.69 τ is a different quantity.',
          1, 'Lifetime', origin='goc', src='Mock exam Q1(a)')
    B.add('When several first-order sinks act in parallel, how is the combined lifetime obtained?',
          'Add the inverses: 1/τ = 1/τ₁ + 1/τ₂ + …',
          ['Add the lifetimes directly: τ = τ₁ + τ₂ + …',
           'Take the longest lifetime, because the slowest sink controls the loss',
           'Take the arithmetic mean of the individual lifetimes'],
          'First-order loss rates add, so 1/τ = Σ 1/τᵢ. Consequence: the total τ is always SHORTER than the fastest single sink.',
          1, 'Lifetime', origin='goc', src='Mock exam Q1(a); guide 1.1')
    B.add('Which list contains the main sinks of atmospheric pollutants?',
          'OH oxidation, photolysis, dry deposition, wet deposition, heterogeneous chemistry, transport out of the domain',
          ['Industrial emissions, wildfires, volcanoes, grasslands and oceans',
           'Rayleigh scattering, Mie scattering, absorption, thermal emission and surface reflection',
           'Nadir, limb and occultation geometries, geostationary and polar orbits'],
          'Guide 1.1 lists gas-phase oxidation (mainly OH), photolysis, dry deposition, wet deposition, heterogeneous/multiphase chemistry and transport out of the domain. Emissions are SOURCES, not sinks.',
          1, 'Sinks', origin='goc', src='Study guide Ch.1 (checklist: ≥ 4 sinks)')
    B.add('Why is the OH radical called the "detergent of the atmosphere"?',
          'It oxidises and removes most reactive gases such as CO, CH₄ and NO₂',
          ['It absorbs ultraviolet light and protects the troposphere from solar radiation',
           'It makes rain by turning aerosol particles into cloud condensation nuclei',
           'It neutralises dust particles with electric charge so that they fall to the ground'],
          'OH is the main gas-phase oxidant: CO + OH → CO₂ + H; CH₄ + OH → CH₃ + H₂O; NO₂ + OH + M → HNO₃. It therefore sets the lifetime of many gases.',
          1, 'Sinks', src='Study guide 1.1')
    B.add('Which type of sink is the reaction NO₂ + hν (λ < 420 nm) → NO + O?',
          'Photolysis', ['Dry deposition', 'Wet deposition', 'Heterogeneous chemistry on aerosol particles'],
          'A photon of UV/visible light breaks the molecule, so this is photolysis. HCHO + hν and CFC photolysis in the stratosphere are of the same type.',
          1, 'Sinks', src='Study guide 1.1')
    B.add('Which sink is the MAIN loss process for most aerosols and for soluble gases such as HNO₃ and NH₃?',
          'Wet deposition by cloud and rain (rainout and washout)', ['Photolysis by strong UV radiation', 'Gas-phase reaction with OH', 'Transport to the stratosphere followed by photolysis'],
          'Guide 1.1: wet deposition includes rainout (in-cloud, particles act as CCN) and washout (below cloud); it is the main sink of soluble gases and of most aerosols.',
          1, 'Sinks', src='Study guide 1.1')
    B.add('How is dry deposition described, and what is the flux formula?',
          'By a deposition velocity v_d, with flux F = −v_d · C',
          ['By a rate constant k, with flux F = −k · [OH]', 'By an optical depth τ, with flux F = I₀ · e^(−τ)', 'By an Ångström exponent α, with flux F = τ₀ · λ^(−α)'],
          'Guide 1.1: direct uptake at the surface (stomata, soil, water, buildings) without precipitation, described by v_d; F = −v_d·C.',
          2, 'Sinks', src='Study guide 1.1')
    B.add('Why is N₂O₅ + H₂O (on particles) → HNO₃ called heterogeneous chemistry?',
          'The reaction occurs on the surface or inside particles or droplets, not purely in the gas phase',
          ['The reaction needs light, so it only happens in daytime', 'The reaction produces two products in different states of matter', 'The reaction only occurs in the stratosphere'],
          'Heterogeneous (multiphase) means a solid or liquid phase takes part. Gas-to-particle conversion (nucleation, condensation) is a sink for the gas but a SOURCE of aerosol.',
          2, 'Sinks', src='Study guide 1.1')
    # ---- calculations (answers come from verified.json) ----
    d = CO['tau_days']
    B.add('With k(CO+OH) ≈ 2×10⁻¹³ cm³ molecule⁻¹ s⁻¹ and [OH] ≈ 1×10⁶ molecule cm⁻³, what is the lifetime of CO with respect to OH?',
          f'≈ {d:.0f} days (≈ 5×10⁶ s, about 2 months)',
          ['≈ 5.8 days (wrong conversion from seconds to days)', '≈ 1 390 days (divided by 3 600 and called it days)', '≈ 5×10⁶ days (forgot to convert seconds to days)'],
          f'τ = 1/(k[OH]) = 1/(2×10⁻¹³ × 1×10⁶) = 5×10⁶ s; dividing by 86 400 s/day gives {d:.2f} days. Recomputed in Python (data/verified.json).',
          1, 'Calculation', origin='goc', src='Mock exam Q1(b)')
    p = V['par_example']
    B.add('A gas is lost by chemistry (τ = 2 days), dry deposition (τ = 3 days) and wet deposition (τ = 6 days). What is the combined lifetime?',
          f'{p["total"]:.0f} day', ['11 days (sum of the lifetimes)', '3.67 days (arithmetic mean)', '2 days (the fastest sink only)'],
          '1/τ = 1/2 + 1/3 + 1/6 = 1 day⁻¹, so τ = 1 day — shorter than even the fastest sink (2 days).',
          2, 'Calculation', src='Study guide 1.1 (formula 1/τ = Σ 1/τᵢ)')
    pl = V['plume']
    B.add('Downwind of a point source the NO₂ column decays exponentially with an e-folding length of 50 km. The mean wind is 5 m/s. What is the NO₂ lifetime?',
          f'≈ {pl["tau_h"]:.1f} hours', ['≈ 10 hours', '≈ 0.28 hours (km confused with m)', '≈ 27.8 hours'],
          'C(x) ∝ exp(−x/(U·τ)) so τ = L/U = 50 000 m / 5 m s⁻¹ = 10 000 s ≈ 2.8 h, inside the 2–6 h range given for NO₂.',
          2, 'Calculation', src='Study guide 1.2 (plume-decay method)')
    B.add('A first-order sink has τ = 10 days. After 10 days, what fraction of the initial amount remains?',
          f'≈ {V["decay"]["e1"]*100:.0f}% (e⁻¹)', ['50% (one half)', '10% (one tenth)', '0% (everything is gone)'],
          'C/C₀ = e^(−t/τ). At t = τ, e⁻¹ ≈ 36.8% remains. Half is lost only after t½ = τ ln 2 ≈ 6.9 days.',
          2, 'Calculation', src='Study guide Figure 3 (decay curve e^(−t/τ))')
    B.add('Which formula estimates the typical distance a molecule is carried by the wind during its lifetime τ?',
          'L ≈ U · τ (U is the horizontal wind speed)', ['L ≈ τ / U', 'L ≈ U / τ²', 'L ≈ τ · [OH]'],
          'Guide 1.2: L ≈ U·τ with U ≈ 5–10 m/s. Compare L with source size and mixing distance to tell whether a satellite map looks like a source map or is already mixed.',
          1, 'Reading maps', src='Study guide 1.2')
    B.add('A satellite NO₂ map has small hotspots over cities while the CH₄ map is almost uniform. What is the correct explanation?',
          'NO₂ lives for hours so it is destroyed before it can spread; CH₄ lives ~10 years, longer than the global mixing time (~1 year), so it is well mixed',
          ['NO₂ is measured with a higher-resolution sensor than CH₄, so more detail is visible',
           'CH₄ has almost no surface emission sources, so it is spread evenly',
           'NO₂ lives longer than CH₄, so it accumulates over urban areas for years'],
          'Guide 1.2 and answer key Q1(c): short τ → map looks like the sources; τ ≫ mixing time → uniform distribution (variations of only ~1%).',
          2, 'Reading maps', origin='goc', src='Mock exam Q1(c)')
    B.add('Which species has a satellite map that looks most like a map of its sources (sharp hotspots decaying within tens to hundreds of km)?',
          'NO₂ in the boundary layer (lifetime of hours)', ['CO₂ (lifetime of a century or more)', 'CH₄ (lifetime 9–12 years)', 'N₂O (lifetime 50–120 years)'],
          'The shorter the lifetime, the more the map looks like the sources. NO₂, SO₂ and HCHO are short-lived; CO₂, CH₄ and N₂O are well mixed with only ~1% variation.',
          1, 'Reading maps', src='Study guide 1.2')
    B.add('According to the Junge relationship quoted in the guide, how does the relative spatial variability σ/C relate to the lifetime τ?',
          'Inversely: σ/C ≈ 0.14/τ (τ in years)', ['Proportionally: σ/C ≈ 0.14 · τ', 'It does not depend on τ', 'Inversely with the square of τ'],
          'The longer a species lives, the more uniform it is. For CH₄ (τ ≈ 10 years) σ/C ≈ 1.4%, consistent with an almost uniform map. This is a rough rule.',
          2, 'Reading maps', src='Study guide 1.2 (Junge relationship)')
    B.add('Which species has a typical lifetime of the order of HOURS?',
          'NO₂ and HCHO in the boundary layer', ['CO', 'CH₄', 'N₂O'],
          'Guide table Ch.1: NO₂ 2–12 h; HCHO/glyoxal hours; CO ≈ 1–2 months; CH₄ ≈ 9–12 years; N₂O ≈ 50–120 years.',
          1, 'Orders of magnitude', src='Study guide 1.3')
    B.add('Which ordering by INCREASING lifetime is correct?',
          'NO₂ < SO₂ < tropospheric aerosol < CO < CH₄ < N₂O',
          ['SO₂ < NO₂ < CO < aerosol < N₂O < CH₄', 'CO < NO₂ < SO₂ < CH₄ < aerosol < N₂O', 'CH₄ < CO < aerosol < SO₂ < NO₂ < N₂O'],
          'Hours (NO₂) → 1–2 days (SO₂) → ~1 week (aerosol) → 1–2 months (CO) → ~10 years (CH₄) → 50–120 years (N₂O).',
          2, 'Orders of magnitude', origin='goc', src='Study guide Ch.1 (checklist: orders of magnitude)')
    B.add('How do the lifetimes of SO₂ in the troposphere and in the stratosphere differ?',
          'About 1–2 days in the troposphere, but of the order of weeks in the stratosphere',
          ['Longer in the troposphere because there is more water to dissolve in', 'Equal, because the loss mechanisms are identical', 'About 1–2 years in both layers'],
          'In the troposphere SO₂ is removed quickly by OH, aqueous oxidation and dry deposition; in the stratosphere there is no rain and little humidity, so it lives for weeks.',
          3, 'Orders of magnitude', src='Study guide 1.3')
    B.add('In what way is CO₂ different from other gases when we talk about lifetime?',
          'It has no single lifetime because the ocean and the biosphere take it up at different rates',
          ['Its lifetime is only a few days because OH oxidises it quickly', 'Its lifetime is exactly 1 year, the inter-hemispheric mixing time', 'Its lifetime is infinite because it has no sink'],
          'The guide table lists CO₂ as "~100+ years (no single lifetime)", with ocean and biosphere uptake as the sinks; the map is almost uniform (±2%).',
          3, 'Orders of magnitude', src='Study guide 1.3')
    B.add('Which mixing times should the lifetime be compared with?',
          'A few weeks to mix around a latitude band, about 1 year to mix between hemispheres',
          ['A few hours around a latitude band, a few days between hemispheres', 'A few years around a latitude band, a few decades between hemispheres', 'A few minutes around a latitude band, 1 month between hemispheres'],
          'Guide 1.2. A species with τ ≪ a few weeks is not yet mixed around a latitude band; one with τ ≫ 1 year is mixed globally.',
          2, 'Reading maps', src='Study guide 1.2')
    B.add('Which statement describes an NO₂ plume downwind of a point source?',
          'The column is highest at the source and then decays exponentially with an e-folding length U·τ',
          ['The column is lowest at the source and increases with distance downwind', 'The column stays constant along the plume because NO₂ is not lost', 'The column oscillates periodically with wavelength'],
          'Guide Figure 2: the shorter τ, the faster the downwind decay; an exponential fit gives τ_NO₂ ≈ 2–6 h.',
          2, 'Reading maps', src='Study guide 1.2, Figure 2')
    B.essay('(a) Define the atmospheric lifetime τ of a pollutant and explain how parallel sinks are combined.\n(b) Compute the lifetime of CO with respect to OH (k = 2×10⁻¹³ cm³ molecule⁻¹ s⁻¹, [OH] = 1×10⁶ cm⁻³) in days.\n(c) Explain why an NO₂ map has hotspots while a CH₄ map is nearly uniform.',
            '(a) τ = M / L (burden divided by loss rate). For a first-order sink τ = 1/k′. In parallel: 1/τ = Σ 1/τᵢ (chemistry, photolysis, dry and wet deposition).\n'
            f'(b) τ = 1/(k[OH]) = 1/(2×10⁻¹³ × 1×10⁶) = 5×10⁶ s ≈ {d:.0f} days ≈ 2 months.\n'
            '(c) NO₂ lives for hours and is destroyed before the wind can spread it, so its map looks like the sources. CH₄ lives ~10 years ≫ the global mixing time (~1 year), so it is well mixed, with only ~1% variation.',
            3, 'Mock exam', origin='goc', src='Mock exam Q1 (2.5 points) + suggested answer')
    B.essay('List at least four sinks of atmospheric pollutants; for each give an example species and the mechanism.',
            'OH oxidation (CO + OH → CO₂ + H). Photolysis (NO₂ + hν → NO + O). Dry deposition (O₃, SO₂ at the surface, F = −v_d C). Wet deposition (HNO₃, NH₃, aerosols by rainout/washout). '
            'Also: heterogeneous chemistry (N₂O₅ → HNO₃ on particles) and transport to the stratosphere (N₂O, CFCs).',
            2, 'Sinks', origin='goc', src='Study guide Ch.1 (question + checklist)')
    B.essay('Downwind of a point source the NO₂ column ratio C/C₀ is 1, 0.61 and 0.37 at x = 0, 50 and 100 km. The wind is 5 m/s. Compute τ.',
            'ln(C/C₀) = −x/(Uτ). At x = 100 km: ln 0.37 ≈ −0.99 ≈ −1, so Uτ ≈ 100 km. Hence τ = 100 000 m / 5 m s⁻¹ = 2×10⁴ s ≈ 5.6 hours. '
            'Check at x = 50 km: exp(−0.5) = 0.61 ✓. The result lies in the 2–6 h range of NO₂.',
            3, 'Calculation', src='Study guide 1.2 (extra exercise; numbers checked in Python)')
    # ---------------- SLIDES ----------------
    tp = V['co_oh']
    sl = [
        cover('Sinks and lifetime of air pollutants',
              'Study guide chapter 1 — reading lifetime from satellite maps',
              '<b>Atmospheric Remote Sensing</b> · USTH<br>Satellite Remote Sensing of Atmospheric Composition<br>Sinks · lifetime · orders of magnitude'),
        S('Six sinks of air pollutants', cards(
            card('OH oxidation', 'The main sink of reactive gases.<br>CO + OH → CO₂ + H'),
            card('Photolysis', 'UV/visible photons break molecules.<br>NO₂ + hν → NO + O'),
            card('Dry deposition', 'Uptake at the surface, no rain needed.<br>F = −v<sub>d</sub>·C'),
            card('Wet deposition', 'Rainout (in-cloud) and washout (below cloud).<br>Soluble gases and aerosols'),
            card('Heterogeneous chemistry', 'Reactions on particles or cloud droplets.<br>N₂O₅ → HNO₃'),
            card('Transport out of the domain', 'Up to the stratosphere, then photolysis.<br>N₂O, CFCs'), cols=3)),
        S('Lifetime and parallel sinks',
          fm('<span class="l">Definition</span>τ = M / L &nbsp;&nbsp; (steady state: τ = M / P)') +
          fm('<span class="l">Several sinks in parallel</span>1/τ = 1/τ<sub>chem</sub> + 1/τ<sub>phot</sub> + 1/τ<sub>dry</sub> + 1/τ<sub>wet</sub>') +
          fm('<span class="l">First-order chemistry</span>τ<sub>chem</sub> = 1 / (k·[OH])') +
          '<p class="note"><b>M</b>: burden (mass or number of molecules). <b>L</b>: total loss rate. Loss <i>rates</i> add, so the total τ is always <b>shorter</b> than the fastest sink.</p>' +
          callout('info', 'Picture it', 'A bath with several drains: the <b>rates</b> add; the <b>times</b> do not.')),
        S('Example: lifetime of CO against OH',
          cols(fm(f'k ≈ 2×10<sup>−13</sup> cm³ s<sup>−1</sup><br>[OH] ≈ 1×10<sup>6</sup> cm<sup>−3</sup>', 34) +
               fm(f'τ = 1/(k[OH]) = 5×10<sup>6</sup> s<br>≈ <b>{tp["tau_days"]:.0f} days</b> ≈ 2 months', 36),
               ul_(['Convert seconds to days: divide by 86 400', 'More OH (tropics) means a shorter CO lifetime', 'About 2 months is long enough for fire CO to cross an ocean'], 34), flex=[1.1, 1]) +
          callout('info', 'Parallel example', 'Chemistry 2 days, dry deposition 3 days, wet deposition 6 days: 1/τ = 1/2 + 1/3 + 1/6 = 1 → <b>τ = 1 day</b>.') + '<p class="note">Python check: τ(CO) = 57.87 days; parallel total = 1.000 day.</p>'),
        S('Lifetime versus transport time', cards2(430, 
            card('Short-lived (hours – days)', 'The map ≈ <b>a map of the sources</b>: hotspots at cities, plants, ships, fires.<br>NO₂, SO₂, HCHO'),
            card('Medium-lived (weeks – months)', '<b>Continental-scale plumes</b> appear: fire CO, dust crossing the Atlantic.'),
            card('Long-lived (years – centuries)', 'Well mixed: almost uniform, ~1% variation; high precision needed.<br>CO₂, CH₄, N₂O'), cols=3) +
          '<p class="note">Distance <b>L ≈ U·τ</b> (U ≈ 5–10 m/s). Mixing around a latitude band takes weeks; between hemispheres ~1 year.</p>'),
        S('Lifetime vs scale of variability', figfit('f1_lifetime', 'Figure 1 (study guide): lifetime versus spatial scale of variability — orders of magnitude.', 520)),
        S('Reading τ from a plume', figfit('f12_plume', 'Figure 2: NO₂ decays exponentially downwind; the shorter the plume, the smaller τ.', 340) +
          fm('τ = L / U = 50 000 m / 5 m s<sup>−1</sup> = 10<sup>4</sup> s ≈ <b>2.8 h</b>', 34) + '<p class="note">Measure the e-folding length L of the NO₂ plume; fit C(x) ∝ exp(−x/(U·τ)).</p>'),
        S('First-order decay curves', figfit('f18_decay', 'Figure 3: C/C₀ = e<sup>−t/τ</sup> for NO₂, SO₂, aerosol, CO and CH₄ (logarithmic time axis).', 470) +
          '<p class="note">At t = τ, e<sup>−1</sup> ≈ 36.8% remains; half is lost after t<sub>½</sub> = τ ln 2 ≈ 0.69 τ.</p>'),
        S('Typical lifetimes (orders of magnitude)', dtable(tbl(['Species', 'Lifetime', 'Main sink', 'On the map'], [
            ['NO₂ (boundary layer)', '2–12 hours', 'OH → HNO₃; N₂O₅', 'Hotspots'], ['SO₂', '1–2 days', 'OH, aqueous, dry', 'Point sources, volcanoes'],
            ['Aerosol (troposphere)', '~1 week', 'Dry and wet deposition', 'Regional plumes'], ['CO', '1–2 months', 'OH', 'Intercontinental plumes'],
            ['CH₄', '9–12 years', 'OH, soil, stratosphere', 'Nearly uniform'], ['N₂O, CFCs', '50–120 years', 'Stratospheric photolysis', 'Well mixed']]), 'mid')),
        S('Exam checklist — Chapter 1', chk([
            'List ≥ 4 sinks: OH, photolysis, dry deposition, wet deposition (+ heterogeneous chemistry, transport)',
            'Define τ = M/L; combine with 1/τ = Σ 1/τᵢ',
            'Compare τ with transport time: short τ → source map; long τ → uniform',
            'Orders of magnitude: hours (NO₂), days (SO₂), week (aerosol), months (CO), decade (CH₄), century (N₂O, CO₂)'])),
        S('Key points', dul([
            'Six sinks: OH, photolysis, dry/wet deposition, heterogeneous chemistry, transport',
            'τ = M/L and 1/τ = Σ 1/τᵢ',
            'Short τ → source map; long τ → uniform map',
            'NO₂ hours · SO₂ days · CO months · CH₄ decade']))]
    mod = dict(id='m1', slug='01-sinks-lifetime', title='M1 · Sinks & lifetime', en='Sinks and lifetime of air pollutants',
               question='<ul><li>What are possible sinks of air pollutants in the atmosphere?</li><li>How do we understand the typical lifetime of an air pollutant by inspecting its spatial distribution from space?</li><li>Provide examples of typical lifetime (orders of magnitude) of air pollutants.</li></ul>',
               calcs=[('lifetime', 'Lifetime calculator'), ('plume', 'Lifetime from a plume')],
               checklist=['List ≥ 4 sinks: OH oxidation, photolysis, dry deposition, wet deposition (+ heterogeneous chemistry, transport).',
                          'Define τ = burden / loss rate; combine sinks with 1/τ = Σ 1/τᵢ.',
                          'Lifetime vs transport time: short τ → map of sources; long τ → well mixed.',
                          'Give orders of magnitude: hours (NO₂), days (SO₂), week (aerosols), months (CO), decade (CH₄), century (N₂O, CO₂).'],
               summary=['Bể chứa: oxy hóa bởi OH, quang phân, lắng đọng khô, lắng đọng ướt, phản ứng dị thể, vận chuyển ra khỏi vùng.',
                        'Thời gian sống τ = lượng tồn trữ / tốc độ mất; nhiều quá trình song song: 1/τ = Σ 1/τᵢ.',
                        'So τ với thời gian vận chuyển: τ ngắn → bản đồ trùng nguồn (NO₂ đô thị); τ dài → đồng đều (CO₂, CH₄).',
                        'Bậc độ lớn: giờ (NO₂), ngày (SO₂), tuần (aerosol, O₃), tháng (CO), chục năm (CH₄), thế kỷ (N₂O, CO₂).'],
               sections=[
        ('What is a sink?', '<p><b>Picture it:</b> the atmosphere is a bath. Emissions are the tap; <b>sinks</b> are the drains. How long a pollutant stays depends on how fast the drains are.</p>'
         '<p>Technically, a sink is any process that removes a species from the air mass under consideration. The guide distinguishes six types:</p>' +
         hx_table(['Sink', 'Mechanism', 'Example', 'Important for'], [
             ['Gas-phase oxidation', 'OH radical (also O₃, NO₃ at night, halogens)', 'CO + OH → CO₂ + H; CH₄ + OH → CH₃ + H₂O; NO₂ + OH + M → HNO₃', 'Most reactive gases'],
             ['Photolysis', 'UV/visible photons break the molecule', 'NO₂ + hν (λ &lt; 420 nm) → NO + O; HCHO + hν; CFCs in the stratosphere', 'NO₂, HCHO, CFCs'],
             ['Dry deposition', 'Uptake at the surface (stomata, soil, water), v<sub>d</sub>; F = −v<sub>d</sub>·C', 'O₃, SO₂, NH₃, HNO₃, coarse particles', 'Soluble gases, coarse particles'],
             ['Wet deposition', 'Rainout (in cloud, particles act as CCN) and washout (below cloud)', 'HNO₃, SO₂, NH₃, aerosols', 'Soluble gases, most aerosols'],
             ['Heterogeneous chemistry', 'Reactions on or inside particles and cloud droplets; gas → particle', 'N₂O₅ → HNO₃; SO₂ → sulfate in water', 'Gas-to-particle conversion'],
             ['Transport out of the domain', 'Export to the free troposphere or stratosphere', 'N₂O and CFCs go up to the stratosphere and are photolysed', 'Long-lived gases']], 'left') +
         callout('info', 'Do not confuse', '<b>Sources</b> (emissions, biology, fires) are not <b>sinks</b>. Gas-to-particle conversion is a sink of the gas and at the same time a source of aerosol.')),
        ('Lifetime τ and combining sinks',
         '<p>The lifetime tells you "how long, on average, a molecule stays". The formulas of the guide:</p>' + eq('Definition', 'τ = M / L = M / (F<sub>out</sub> + L<sub>chem</sub> + D<sub>dry</sub> + D<sub>wet</sub>) &nbsp;; steady state: τ = M / P') +
         eq('Parallel sinks', '1/τ = 1/τ<sub>chem</sub> + 1/τ<sub>photolysis</sub> + 1/τ<sub>dry</sub> + 1/τ<sub>wet</sub> &nbsp;; &nbsp; τ<sub>chem</sub> = 1/(k·[OH])') +
         '<p><b>Memory aid:</b> <i>rates</i> add, <i>times</i> do not. Two drains open together empty the bath faster than either alone.</p>'
         f'<div class="ex"><div class="exh">Example 1 · CO against OH</div><p>k ≈ 2×10⁻¹³ cm³ s⁻¹, [OH] ≈ 1×10⁶ cm⁻³ ⇒ τ = 1/(k[OH]) = 5×10⁶ s ≈ <b>{tp["tau_days"]:.1f} days</b> ≈ 2 months. (Python: 57.87 days.)</p></div>'
         '<div class="ex"><div class="exh">Example 2 · Three parallel sinks</div><p>τ = 2, 3, 6 days ⇒ 1/τ = 0.5 + 0.333 + 0.167 = 1.0 ⇒ <b>τ = 1 day</b>.</p></div>'
         '<div class="ex"><div class="exh">Example 3 · Half-life is not the lifetime</div><p>For a first-order sink the concentration falls as C/C₀ = e<sup>−t/τ</sup>. At t = τ, e⁻¹ ≈ 36.8% remains; half is lost after t<sub>½</sub> = τ ln 2 ≈ 0.69 τ.</p></div>' +
         callout('warn', 'Common mistakes', 'Confusing τ with the half-life; adding lifetimes instead of their inverses; forgetting to convert seconds to days (divide by 86 400).')),
        ('Reading lifetime from satellite maps',
         '<p>The core idea is a <b>race between the lifetime τ and the transport time</b>. During τ a molecule travels L ≈ U·τ (U ≈ 5–10 m/s). Mixing around a latitude band takes a few weeks and mixing between the hemispheres about a year.</p>' +
         hx_table(['Class', 'What the satellite map looks like', 'Examples'], [
             ['Short-lived (hours – days)', 'Map ≈ map of the sources: hotspots at cities, power plants, ships, fires; decay within tens to hundreds of km', 'NO₂ (TROPOMI), SO₂, HCHO following isoprene'],
             ['Medium-lived (weeks – months)', 'Plumes and continental-scale transport are visible; main gradient is between hemispheres', 'CO from African/Amazon fires crossing oceans; dust over the Atlantic'],
             ['Long-lived (years – centuries)', 'Nearly uniform (~1% variability), small north–south gradient and seasonal cycle; very high precision needed to see sources', 'CO₂ (OCO-2), CH₄, N₂O']], 'left') +
         lfig('f1_lifetime', 'Figure 1 (study guide): lifetime versus spatial scale of variability.') +
         '<p><b>Quantitative rule (Junge relationship):</b> σ/C ≈ 0.14/τ with τ in years — the longer a species lives, the more uniform it is. For CH₄ (τ ≈ 10 years): σ/C ≈ 1.4%.</p>'
         '<p><b>Deriving τ directly from a plume:</b> downwind of a point source the NO₂ column decays as C(x) ∝ exp(−x/(U·τ)). An exponential fit gives the e-folding length L = U·τ, hence τ = L/U. Example: L = 50 km, U = 5 m/s ⇒ τ = 10⁴ s ≈ <b>2.8 hours</b> (guide: τ<sub>NO₂</sub> ≈ 2–6 h).</p>' +
         lfig('f12_plume', 'Figure 2 (study guide): NO₂ decay downwind gives τ.') + lfig('f18_decay', 'Figure 3 (study guide): decay curves e<sup>−t/τ</sup> for NO₂, SO₂, aerosol, CO, CH₄.')),
        ('Typical lifetimes (orders of magnitude)', hx_table(['Species', 'Typical lifetime', 'Main sink', 'Appearance from space'], [
            ['OH, NO₃', '~1 s to minutes', 'Very fast chemistry', 'Not mapped directly'],
            ['NO₂/NOₓ (boundary layer)', 'hours (2–12 h; longer in winter)', 'OH → HNO₃, N₂O₅ hydrolysis', 'Hotspots on sources'],
            ['HCHO, glyoxal', 'hours', 'Photolysis, OH', 'Follows VOC sources/fires'],
            ['SO₂', '~1–2 days (weeks in the stratosphere)', 'OH, aqueous oxidation, dry deposition', 'Point sources, volcano plumes'],
            ['NH₃', 'hours – 1 day', 'Conversion to NH₄⁺, deposition', 'Agricultural hotspots'],
            ['Aerosols (troposphere)', '~1 week (days – 2 weeks)', 'Wet and dry deposition', 'Regional plumes (dust, smoke)'],
            ['O₃ (troposphere)', '~3 weeks (days in the boundary layer – months in the free troposphere)', 'Photolysis + H₂O, NO, HO₂, deposition', 'Hemispheric background'],
            ['CO', '~1–2 months', 'OH', 'Intercontinental plumes'],
            ['CH₄', '~9–12 years', 'OH, soil, stratosphere', 'Nearly uniform, ~1% gradients'],
            ['N₂O, CFCs', '~50–120 years', 'Stratospheric photolysis', 'Well mixed'],
            ['CO₂', '~100+ years (no single lifetime)', 'Ocean and biosphere uptake', 'Well mixed (±2%)']], 'left'))])
    return mod, sl, B

def ul_(items, size=28):
    return '<ul class="tight-ul">' + ''.join(f'<li style="font-size:{size}px">{i}</li>' for i in items) + '</ul>'
