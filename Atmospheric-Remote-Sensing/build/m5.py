# -*- coding: utf-8 -*-
"""M5 — Sensitivity of passive retrievals: averaging kernels, DOFS (study guide Ch.5)."""
from lib import *
from qcore import Bank
V = VERIFIED
OE = V['oe']

def build():
    B = Bank('m5', seed=5)
    di, dr, dn = OE['ideal']['dofs'], OE['realistic']['dofs'], OE['noisy']['dofs']
    B.add('Which quantity is used to quantify the sensitivity of passive retrievals?',
          'The averaging kernel matrix A = ∂x̂/∂x (sensitivity of the retrieved state to the true state)', ['The Ångström exponent α, describing the spectral dependence of aerosol optical depth', 'The air mass factor AMF = SCD/VCD, describing the length of the light path', 'The measurement-error covariance matrix S_ε, describing the noise of the sensor'],
          'Guide 5.1: A = ∂x̂/∂x = G·K, where G = (KᵀS_ε⁻¹K + S_a⁻¹)⁻¹KᵀS_ε⁻¹ is the gain matrix.', 1, 'Averaging kernel', origin='goc', src='Study guide Ch.5 (checklist)')
    B.add('What relation links the retrieved profile, the true profile and the a priori through the averaging kernel?',
          'x̂ = x_a + A (x_true − x_a) + G ε', ['x̂ = x_true + A x_a + G', 'x̂ = A⁻¹ x_true', 'x̂ = x_a · A / ε'],
          'The retrieved profile is a smoothed version of the true profile, mixed with the a priori, plus noise amplified by G.', 1, 'Averaging kernel', origin='goc', src='Mock exam Q5(a)')
    B.add('How is DOFS (Degrees Of Freedom for Signal) calculated and what does it mean?',
          'DOFS = tr(A), the trace of A: the number of independent pieces of information on the vertical profile', ['DOFS = det(A), the determinant of A: the remaining uncertainty volume of the profile', 'DOFS = ΣS_ε, the sum of noise variances over all channels', 'DOFS = A⁻¹, the inverse of the sensitivity'],
          'Guide 5.1: DOFS = tr(A). DOFS equals the number of levels when A is the identity, and 0 if the retrieval just returns the a priori.', 1, 'DOFS', origin='goc', src='Study guide Ch.5 (checklist)')
    B.add('What does one row of the averaging kernel tell us?',
          'The retrieved value at a level is a weighted average of the true profile at all levels; the FWHM is the vertical resolution', ['The altitude at which the gas has its maximum concentration, and the thickness of that layer', 'The random error of the measurement at that level, plus the systematic error of the forward model', 'The absorption coefficient of the gas at that level times its number density'],
          'Guide 5.1: the peak shows where the information really comes from; the width (FWHM) is the vertical resolution.', 2, 'Averaging kernel', src='Study guide 5.1')
    B.add('A row of the averaging kernel has an area close to 1. What does it mean?',
          'The retrieved value at that level comes mainly from the measurement', ['The retrieved value is mostly the a priori value and barely depends on the measurement', 'The measurement error at that level is zero, so regularisation is no longer needed', 'The vertical resolution at that level has reached the maximum the instrument can have'],
          'Guide 5.1: area ≈ 1 → the measurement dominates; area ≈ 0 → the retrieved value just equals the a priori.', 2, 'Averaging kernel', src='Study guide 5.1')
    B.add('What does the averaging kernel look like in the ideal case of perfect sensitivity?',
          'A = identity matrix: each row is a delta function equal to 1 at its own level and 0 elsewhere', ['A = zero matrix: the measurement carries no information about the true profile at any level', 'A is a diagonal matrix whose elements are all 0.5: each level gets only half of the information', 'All elements of A are equal, so every level gives the same mean value of the profile'],
          'Guide 5.2(a): the retrieval reproduces the true profile exactly, independent of the a priori, with infinitely fine vertical resolution and DOFS equal to the number of levels.', 1, 'Ideal vs real', origin='goc', src='Study guide Ch.5 (checklist)')
    B.add('Which features describe the averaging kernels of a realistic nadir ozone retrieval (UV 270–330 nm or IASI 9.6 µm)?',
          'Broad kernels (FWHM ~7–15 km) that overlap, peaks shifted from the nominal level, amplitudes < 1 (~0.3–0.6)', ['Narrow delta-like kernels of 1–2 km at each level', 'Amplitudes larger than 1 near the ground', 'Identical kernels at every level'],
          'Guide 5.2(b): sensitivity is low near the surface (Rayleigh scattering, strong O₃ absorption above, clouds), so near-surface values come mostly from the a priori.', 2, 'Ideal vs real', src='Study guide 5.2')
    B.add('What are typical DOFS for nadir O₃ retrievals in the UV and with IASI?',
          'About 4–6 in the UV (≈ 1 for the troposphere), about 3–4 with IASI', ['About 20–30 for both', 'About 1 for the UV and 10 for IASI', 'Zero, because nadir has no vertical information'],
          'Guide 5.2(b): the stratosphere is known in ~3–4 thick layers plus roughly 1 piece of tropospheric information. Limb: kernels ~2–3 km, DOFS ≈ 20–30.', 2, 'Ideal vs real', src='Study guide 5.2')
    B.add('A CO retrieval from a thermal-infrared sounder has DOFS = 1.2. What does this mean?',
          'About one independent piece of information: essentially a column, most sensitive in the mid-troposphere (~3–8 km), little near the ground', ['CO is known at 1.2 independent levels right at the ground, where the thermal contrast is largest', 'The retrieval error is 1.2 times the uncertainty of the initial a priori profile', 'There are 12 independent levels but each one is noisy at about 10% of the signal'],
          'Answer key Q5(b): thermal contrast with the surface is largest in the mid-troposphere; near the ground the thermal contrast is low so sensitivity is poor.', 2, 'DOFS', origin='goc', src='Mock exam Q5(b)')
    B.add('When comparing satellite retrievals with a chemistry-transport model, what must be done with the averaging kernel?',
          'Smooth the model profile: x_m,smooth = x_a + A (x_model − x_a), then compare with x̂', ['Add the measurement noise to the model profile and average it with the a priori', 'Compare only at levels where A is zero to avoid the effect of the measurement', 'Divide the model profile by the DOFS and multiply by the mean air mass factor'],
          'Answer key Q5(c): this removes the effect of smoothing and a priori, so the comparison is like-for-like.', 2, 'Using AKs', origin='goc', src='Mock exam Q5(c)')
    B.add('What is the ideal column averaging kernel a(z) = ∂VCD̂/∂n(z)?',
          'Equal to 1 at all altitudes', ['Equal to 0 at all altitudes', 'Equal to 1 only at the ground', 'Equal to the AMF at all altitudes'],
          'Guide 5.1: in DOAS, a(z) = AMF_layer / AMF_total. Ideal = 1 at every height (uniform sensitivity of the column).', 3, 'Averaging kernel', src='Study guide 5.1')
    B.add('Which two components make up the retrieval error?',
          'The smoothing error (I − A) S_a (I − A)ᵀ and the noise error G S_ε Gᵀ', ['The AMF error due to the assumed light path and the DOAS fitting error due to cross-sections', 'The Ångström error due to particle size and the ω₀ error due to particle absorption', 'The orbit error due to satellite position and the calibration error due to the instrument'],
          'Guide 5.1: Ŝ = (I − A) S_a (I − A)ᵀ + G S_ε Gᵀ.', 3, 'Error', src='Study guide 5.1')
    B.add(f'In a 12-level simulation with very narrow kernels and very small noise, what is the DOFS?',
          f'≈ {di:.1f} (A close to the identity matrix)', [f'≈ {dr:.1f} (as in the realistic case with 3-level-wide kernels)', '≈ 1.0 (a single column, no vertical information)', '≈ 0 (no information, only the a priori remains)'],
          f'Run in Python: w = 0.3 level, σ_ε = 0.01 → DOFS = {di:.3f}. Narrow kernels and accurate measurements give A → I and DOFS → number of levels.', 2, 'DOFS', src='Home-made Python simulation (data/verified.json)')
    B.add('In the same 12-level model, what happens to DOFS when the noise increases from 0.1 to 1.0 (kernel width 3 levels)?',
          f'It falls from ≈ {dr:.1f} to ≈ {dn:.1f}', [f'It rises from ≈ {dn:.1f} to ≈ {dr:.1f}', 'It does not change because DOFS depends only on the kernel', 'It rises to 12 because noise adds information'],
          f'More noise → the result relies more on the a priori → A shrinks → DOFS falls: {dr:.3f} → {dn:.3f} (Python).', 3, 'DOFS', src='Home-made Python simulation (data/verified.json)')
    B.add('Why are limb ozone retrievals closer to the ideal case than nadir retrievals?',
          'Because limb geometry gives narrow kernels (~2–3 km) and DOFS ≈ 20–30', ['Because limb looks straight down so there is no scattering from above', 'Because limb uses more a priori information than nadir, so the result is less uncertain', 'Because limb measures the concentration directly with a laser pulse from the satellite'],
          'Guide 5.2: limb ozone is close to the ideal case in the stratosphere.', 2, 'Ideal vs real', src='Study guide 5.2')
    B.essay('(a) Write the relation between the retrieved profile, the true profile and the a priori using the averaging kernel.\n(b) A CO retrieval from a thermal-infrared sounder has DOFS = 1.2. What does it mean? Where is the sensitivity highest and why?\n(c) How should averaging kernels be used when comparing satellites with a chemistry-transport model?',
            '(a) x̂ = x_a + A(x_true − x_a) + Gε; A = ∂x̂/∂x = GK; DOFS = tr(A).\n(b) ≈ one independent piece of information → essentially a column, most sensitive in the mid-troposphere (~3–8 km) where the thermal contrast with the surface is largest; near the ground it is almost the a priori.\n'
            '(c) Smooth the model profile: x_m,smooth = x_a + A(x_model − x_a), then compare with x̂ to remove the effect of smoothing and the a priori.', 3, 'Mock exam', origin='goc', src='Mock exam Q5 (2.5 points) + suggested answer')
    B.essay('Draw and compare the ideal averaging kernels with the realistic ones of a nadir ozone retrieval.',
            'Ideal: A = I, delta functions at each level, DOFS = number of levels, independent of the a priori. Realistic (nadir O₃): kernels 7–15 km wide, overlapping, shifted peaks, amplitudes 0.3–0.6, DOFS ≈ 4–6 (≈ 1 in the troposphere), poor sensitivity near the ground (Rayleigh, absorption above, clouds) and above 50 km; hence vertical resolution ~6–10 km in the stratosphere and worse in the troposphere.', 2, 'Ideal vs real', origin='goc', src='Study guide 5.2 / Figure 16')
    sl = [
        cover('Sensitivity of retrievals: averaging kernels', 'Study guide chapter 5',
              '<b>Atmospheric Remote Sensing</b> · USTH<br>A = ∂x̂/∂x · DOFS = tr(A) · ideal and realistic cases'),
        S('The averaging kernel matrix', fm('<span class="l">Definition</span>A = ∂x̂/∂x = G K &nbsp;,&nbsp; G = (K<sup>T</sup>S<sub>ε</sub><sup>−1</sup>K + S<sub>a</sub><sup>−1</sup>)<sup>−1</sup>K<sup>T</sup>S<sub>ε</sub><sup>−1</sup>', 26) +
          fm('<span class="l">Retrieval = smoothing + a priori + noise</span>x̂ = x<sub>a</sub> + A (x<sub>true</sub> − x<sub>a</sub>) + G ε', 30) +
          '<p class="note">Each row of A: the value at one level is a weighted average of the true profile; the <b>FWHM</b> is the vertical resolution and the <b>peak</b> shows where the information comes from.</p>'),
        S('Row area and DOFS', cards2(330, card('Row area ≈ 1', 'The retrieved value comes mostly from the <b>measurement</b>.'), card('Row area ≈ 0', 'The retrieved value is close to the <b>a priori</b>.'),
          card('DOFS = tr(A)', 'Number of independent pieces of information on the profile. DOFS = number of levels when A = I.'), cols=3) + fm('Ŝ = (I − A) S<sub>a</sub> (I − A)<sup>T</sup> + G S<sub>ε</sub> G<sup>T</sup>', 28)),
        S('Column averaging kernels', figfit('f14_colavk', 'Figure 15 (study guide): column kernels — ideal (= 1) versus typical UV-vis, cloudy and thermal-IR cases.', 480) +
          '<p class="note">a(z) = ∂VCD̂/∂n(z) = AMF<sub>layer</sub> / AMF<sub>total</sub>; ideal is 1 at every altitude.</p>'),
        S('Ideal versus realistic (nadir O₃)', figfit('f4_avk', 'Figure 16 (study guide): (a) A = I; (b) a typical nadir ozone profile retrieval.', 500)),
        S('Features of nadir ozone retrievals', cols(
            ulb(['Kernels ~7–15 km wide, overlapping', 'Peaks shifted from the nominal level', 'Amplitudes < 1 (~0.3–0.6)', 'DOFS ≈ 4–6 (UV), ≈ 3–4 (IASI)'], 33, 44),
            ulb(['Near the ground: low sensitivity (Rayleigh, absorption above, clouds) → <b>a priori</b>', 'Above 50 km: little ozone, so sensitivity is lost', 'Limb: kernels ~2–3 km, DOFS ≈ 20–30'], 33, 44))),
        S('12-level simulation (Python)', dtable(tbl(['Case', 'Kernel width', 'Noise σ<sub>ε</sub>', 'DOFS'], [
            ['Ideal', '0.3 levels', '0.01', f'{di:.2f}'], ['Realistic', '3 levels', '0.1', f'{dr:.2f}'], ['Noisy', '3 levels', '1.0', f'{dn:.2f}']]), 'xl') +
          '<p class="note" style="margin-top:20px">A priori correlated with height (length 3 levels). DOFS = tr(A) = sum of the eigenvalues of A; narrow kernels and accurate data give A → I.</p>'),
        S('Using averaging kernels with a model', fm('x<sub>m,smooth</sub> = x<sub>a</sub> + A (x<sub>model</sub> − x<sub>a</sub>)', 34) +
          ulb(['Smooth the model profile with the satellite’s own A', 'Then compare with x̂ to remove smoothing and a priori effects', 'Without this step a difference may come from sensitivity, not from the model'], 33, 30)),
        S('Exam checklist — Chapter 5', chk(['Name: averaging kernel matrix A = ∂x̂/∂x; DOFS = trace(A)', 'x̂ = x<sub>a</sub> + A (x − x<sub>a</sub>) + G ε', 'Row width = vertical resolution; area = contribution of the measurement', 'Draw delta functions (ideal) and broad, overlapping, peak-shifted kernels (nadir O₃, DOFS ≈ 4–6)'])),
        S('Key points', dul(['Sensitivity is measured by A = ∂x̂/∂x; DOFS = tr(A)', 'Ideal: A = I, independent of the a priori', 'Realistic nadir O₃: broad kernels, DOFS ≈ 4–6', 'Compare with models by smoothing with A']))]
    mod = dict(id='m5', slug='05-averaging-kernels', title='M5 · Averaging kernels', en='Sensitivity of passive retrievals: averaging kernels',
               question='<ul><li>Which magnitude is used to quantify the sensitivity of passive remote sensing methods for retrieving the concentration of trace gases?</li><li>Explain the general concept and illustrate with drawings a case of ideally perfect sensitivity and a realistic case (such as the retrieval of the ozone profiles using satellite spectral measurements in nadir pointing geometry).</li></ul>',
               calcs=[('ak', 'Averaging kernel and DOFS (12-level simulation)')],
               checklist=['Name: averaging kernel matrix A = ∂x̂/∂x; DOFS = trace(A).', 'x̂ = x_a + A(x − x_a) + Gε — retrieval = smoothed truth + a priori contribution.', 'Row width = vertical resolution; area = measurement contribution.', 'Draw delta functions (ideal) vs broad, overlapping, peak-shifted kernels (nadir O₃, DOFS ≈ 4–6).'],
               summary=['Đại lượng đo độ nhạy: ma trận hạt nhân trung bình (averaging kernel) A = ∂x̂/∂x; vết của A = số bậc tự do tín hiệu (DOFS).', 'Trường hợp lý tưởng: A = ma trận đơn vị → hàm delta tại mỗi độ cao, không phụ thuộc tiên nghiệm.', 'Thực tế (O₃ nadir): hạt nhân rộng 7–15 km, chồng lên nhau, biên độ < 1, DOFS ≈ 4–6; gần mặt đất độ nhạy thấp → kết quả phụ thuộc nhiều vào profil tiên nghiệm.'],
               sections=[
        ('Averaging kernel, in plain words', '<p>Retrieving a profile is like redrawing a picture from a blurred photo: you get a <b>smoothed</b> version of the true picture, and where the photo is too blurry you fill in with <b>prior guesses (the a priori)</b>. The <b>averaging kernel A</b> tells you how blurry it is at each altitude.</p>' +
         eq('Definition', 'A = ∂x̂ / ∂x = G K &nbsp;;&nbsp; G = (K<sup>T</sup> S<sub>ε</sub><sup>−1</sup> K + S<sub>a</sub><sup>−1</sup>)<sup>−1</sup> K<sup>T</sup> S<sub>ε</sub><sup>−1</sup> (gain)') +
         eq('Consequence', 'x̂ = x<sub>a</sub> + A (x<sub>true</sub> − x<sub>a</sub>) + G ε') +
         '<ul><li><b>Each row</b> of A: the retrieved value at a level is a weighted average of the true profile at all levels. The <b>width (FWHM)</b> is the vertical resolution; the <b>peak</b> shows where the information really comes from.</li>'
         '<li><b>Row area</b>: ≈ 1 → the measurement dominates; ≈ 0 → the value is just the a priori.</li><li><b>DOFS = tr(A)</b> = the number of independent pieces of information on the profile.</li>'
         '<li><b>Column</b>: a(z) = ∂VCD̂/∂n(z) (in DOAS: AMF<sub>layer</sub>/AMF<sub>total</sub>); ideal is 1 at all altitudes.</li></ul>' +
         eq('Retrieval error', 'Ŝ = (I − A) S<sub>a</sub> (I − A)<sup>T</sup> [smoothing] + G S<sub>ε</sub> G<sup>T</sup> [noise]') + lfig('f14_colavk', 'Figure 15 (study guide): column kernels — ideal vs UV-vis, cloudy and thermal-IR cases.')),
        ('Ideal and realistic cases', '<p><b>(a) Ideal: A = I.</b> Each kernel is a delta function equal to 1 at its own level and 0 elsewhere: the retrieval reproduces the true profile, independent of the a priori, with infinite resolution and DOFS = number of levels.</p>'
         '<p><b>(b) Realistic: nadir ozone</b> (GOME-2/OMI in UV 270–330 nm, or IASI at 9.6 µm):</p><ul><li>Broad kernels (FWHM ~7–15 km) that overlap → vertical resolution ~6–10 km in the stratosphere, worse in the troposphere.</li><li>Peaks shifted from the nominal level; amplitudes &lt; 1 (≈ 0.3–0.6).</li>'
         '<li>DOFS ≈ 4–6 in the UV (≈ 1 for the troposphere), ≈ 3–4 for IASI: the stratosphere is known in ~3–4 thick layers plus roughly 1 piece of tropospheric information.</li><li>Poor sensitivity near the surface (Rayleigh scattering, strong O₃ absorption above, clouds) and above 50 km (little ozone) → those values come mostly from the a priori.</li></ul>'
         '<p>By contrast, <b>limb</b> ozone retrievals have narrow kernels (~2–3 km), DOFS ≈ 20–30, close to the ideal case in the stratosphere.</p>' + lfig('f4_avk', 'Figure 16 (study guide): (a) perfect sensitivity A = I; (b) a typical nadir ozone profile retrieval.')),
        ('12-level simulation (checked in Python)', '<p>Home-made model: N = 12 levels; weighting functions K are Gaussians of width w levels; noise S<sub>ε</sub> = σ<sub>ε</sub>²I; a priori S<sub>a</sub> correlated with height (length 3 levels, σ<sub>a</sub> = 1). Results:</p>' +
         hx_table(['Case', 'Kernel width w', 'σ<sub>ε</sub>', 'DOFS = tr(A)'], [['Ideal', '0.3 levels', '0.01', f'<b>{di:.2f}</b>'], ['Realistic', '3 levels', '0.1', f'<b>{dr:.2f}</b>'], ['Noisy', '3 levels', '1.0', f'<b>{dn:.2f}</b>']]) +
         '<p>Observation: narrow kernels and accurate data → A → I and DOFS → number of levels. More noise or wider kernels → DOFS falls and the result relies more on the a priori. Try it in the <a href="../../calculators.html#ak">averaging-kernel calculator</a>. (DOFS = tr(A) also equals the sum of the eigenvalues of A; checked with numpy.)</p>'
         '<p><b>Using AKs with a model:</b> x<sub>m,smooth</sub> = x<sub>a</sub> + A (x<sub>model</sub> − x<sub>a</sub>), then compare with x̂; without this step a difference can come from sensitivity rather than from the model.</p>')])
    return mod, sl, B
