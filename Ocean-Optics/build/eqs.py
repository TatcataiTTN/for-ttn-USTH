# -*- coding: utf-8 -*-
"""Interactive annotated equations (KaTeX). Tex lines use \\sym{key}{tex}: each symbol is clickable (pops up, shows meaning, unit, implication,
parameter values with sources and a plug-in-numbers example). All numbers come from verified.json or are quoted with their slide/textbook source."""
import re, html, json, os, math
_H = os.path.dirname(os.path.abspath(__file__)); _S = os.path.join(_H, '..', 'site')
V = json.load(open(os.path.join(_S if os.path.isdir(_S) else os.path.join(_H, '..'), 'data', 'verified.json')))
COL = {'R': '#e0314b', 'B': '#3b6fd8', 'G': '#1f9d5c', 'O': '#d9822b', 'P': '#8e5bd0', 'K': '#6b7280'}
W = V['pure_water_bw']; PK = V['package_Qstar']; EU = V['euphotic_1pct']; SC = V['secchi_examples']
def sci(x, d=2): m, e = f'{x:.{d}e}'.split('e'); return f'{m}\\times10^{{{int(e)}}}'

def _read_group(s, i):
    """s[i] == '{' -> return (content, index after the matching '}')"""
    assert s[i] == '{'; depth = 0; j = i
    while j < len(s):
        if s[j] == '{': depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0: return s[i + 1:j], j + 1
        j += 1
    raise ValueError('unbalanced')
def render_tex(tex, syms):
    out = ''; i = 0
    while i < len(tex):
        if tex.startswith('\\sym{', i):
            key, j = _read_group(tex, i + 4); body, j = _read_group(tex, j)
            c = COL[syms[key]['c']] if key in syms else '#000'
            out += '\\htmlClass{ks ks-' + key + '}{\\textcolor{' + c + '}{' + render_tex(body, syms) + '}}'; i = j
        else: out += tex[i]; i += 1
    return out
def S(key, c, tex, name, unit, meaning, implication, values=(), ):
    return key, dict(c=c, tex=tex, name=name, unit=unit, meaning=meaning, implication=implication, values=[list(v) for v in values])

EQS = {}
def eq(name, label, lines, syms, example=None, vi=''):
    EQS[name] = dict(label=label, lines=lines, syms=dict(syms), order=[k for k, _ in syms], example=example or [], vi=vi)

# ---------------------------------------------------------------------------------------------------------------- equations
eq('rte', 'F1 · Radiative transfer equation (lecture slide 5)',
 [r'\begin{aligned}\frac{d\sym{L}{L(\theta,\varphi)}}{\sym{r}{dr}}&=\underbrace{-\,\sym{c}{c}\,\sym{L}{L(\theta,\varphi)}}_{\footnotesize\text{loss: absorption + scattering out}}&&\qquad\sym{c}{c}=\sym{a}{a}+\sym{b}{b}\\[0.15em]&\quad+\underbrace{\int_{4\pi}\sym{beta}{\beta(\theta,\varphi;\theta^{\prime},\varphi^{\prime})}\,\sym{L}{L(\theta^{\prime},\varphi^{\prime})}\,\sym{om}{d\omega^{\prime}}}_{\footnotesize\text{gain: scattering in from all directions}}\\[0.15em]&\quad+\underbrace{\sym{S}{S}}_{\footnotesize\text{internal sources}}\end{aligned}'],
 [S('L', 'K', r'L(\theta,\varphi)', 'radiance', 'W m⁻² sr⁻¹ nm⁻¹', 'Light power per unit area, solid angle and wavelength travelling in direction (θ, φ).', 'The unknown of the equation; θ is measured from the vertical.'),
  S('r', 'K', r'dr', 'path element', 'm', 'Thin slab of water crossed by the beam.', 'Everything is a rate per metre along the path.'),
  S('c', 'R', r'c', 'attenuation coefficient', 'm⁻¹', 'Fraction of the beam lost per metre, by absorption and by scattering out of the beam: c = a + b.', 'Beer–Lambert uses c, not a: a transmissometer measures c.',
    [('example used in module A', 'a = 0.08, b = 0.12 ⇒ c = 0.20 m⁻¹', 'illustrative'), ('example used in module E', 'c = 0.5 m⁻¹ ⇒ 61 % left after 1 m', 'illustrative')]),
  S('a', 'B', r'a', 'absorption coefficient', 'm⁻¹', 'Photon energy converted to heat or chemistry.', 'Removes photons for good; sets light penetration and the colour of the sea.',
    [('pure water minimum', '≈ 0.005 m⁻¹ near 415 nm', 'slide 24, read from graph'), ('clearest gyre, total', '≈ 0.007 m⁻¹ at 410–420 nm', 'slide 26, Morel et al. 2007')]),
  S('b', 'G', r'b', 'scattering coefficient', 'm⁻¹', 'Photons change direction.', 'Redirects, never destroys: scattered photons can re-enter the beam from other directions.',
    [('pure sea water, 500 nm, S = 37', f'{W["morel_500_S37"]["b_w"]:.2e} m⁻¹', 'verified.json (slide-20 formula)'), ('Case 1 particles, 400 nm', '≈ 0.18 m⁻¹', 'slide 58, read from graph')]),
  S('beta', 'O', r'\beta', 'volume scattering function', 'm⁻¹ sr⁻¹', 'How scattered power is distributed over angles (θ,φ) ← (θ′,φ′).', 'Forward-peaked for particles, symmetric for pure water; b = 2π∫β sinθ dθ.',
    [('pure water, 90°, 546 nm, S = 0', '9.44×10⁻⁵ m⁻¹ sr⁻¹', 'slide-20 formula; textbook 0.869e-4')]),
  S('om', 'K', r'd\omega^{\prime}', 'solid-angle element', 'sr', 'Integration over every incoming direction; dω = sinθ dθ dφ.', 'The slide prints a factor 2π in front of the integral; the textbook does not.'),
  S('S', 'P', r'S', 'source term', 'W m⁻³ sr⁻¹ nm⁻¹', 'Light created inside the water (fluorescence, Raman, bioluminescence).', 'Zero for purely elastic problems; matters for Chl fluorescence.')],
 [r'\text{No sources, collimated beam: }\ \frac{dL}{dr}=-cL\ \Rightarrow\ L(1\,\mathrm{m})=L_0\,e^{-0.5\times1}=%.3f\,L_0' % math.exp(-0.5),
  r'c=a+b=0.08+0.12=0.20\ \mathrm{m^{-1}}\ \Rightarrow\ L(5\,\mathrm{m})=L_0\,e^{-0.20\times5}=%.3f\,L_0' % math.exp(-1)],
 'Ý nghĩa: ánh sáng mất đi do hấp thụ và tán xạ ra khỏi chùm (c = a + b), được bù do tán xạ từ hướng khác vào, cộng nguồn nội tại S. Slide 5 in thêm thừa số 2π trước tích phân; textbook không có.')

eq('iop_b', 'Scattering coefficients derived from β (slide 18)',
 [r'\sym{b}{b}\;=\;\int_{4\pi}\sym{beta}{\beta}\,d\omega\;=\;2\pi\int_{0}^{\pi}\sym{beta}{\beta(\theta)}\,\sym{sin}{\sin\theta}\,d\theta',
  r'\sym{b}{b}\;=\;\underbrace{\sym{bf}{b_f}}_{\footnotesize\text{forward, 0–90°}}\;+\;\underbrace{\sym{bb}{b_b}}_{\footnotesize\text{backward, 90–180°}}\qquad\sym{c}{c}=a+\sym{b}{b}',
  r'\sym{bf}{b_f}=2\pi\!\int_{0}^{\pi/2}\!\beta\sin\theta\,d\theta\qquad\sym{bb}{b_b}=2\pi\!\int_{\pi/2}^{\pi}\!\beta\sin\theta\,d\theta'],
 [S('b', 'G', 'b', 'total scattering coefficient', 'm⁻¹', 'Integral of β over all directions (revolution symmetry assumed).', 'b/c is the single-scattering albedo of the volume.', [('pure sea water 500 nm', f'{W["morel_500_S37"]["b_w"]:.2e} m⁻¹', 'verified.json')]),
  S('beta', 'O', r'\beta', 'volume scattering function', 'm⁻¹ sr⁻¹', 'Angular distribution of scattered power.', 'Pure water: U-shaped, minimum at 90° (slide 22).'),
  S('sin', 'K', r'\sin\theta', 'sinθ weight', '—', 'Comes from dω = 2π sinθ dθ for a symmetric β.', 'Directions near 0° and 180° carry little solid angle even when β is large there.'),
  S('bf', 'B', 'b_f', 'forward scattering', 'm⁻¹', 'Angles 0 → 90°.', 'Large for particles (diffraction).'),
  S('bb', 'P', 'b_b', 'backscattering', 'm⁻¹', 'Angles 90° → 180°.', 'The part that can leave the sea and be seen from space.', [('pure water: b_bw/b_w', f'{V["bbw_over_bw_500"]:.2f}', 'verified.json'), ('particles: b_bp/b_p', '≈ 0.005–0.035', 'slide 71, read from graph')]),
  S('c', 'R', 'c', 'attenuation', 'm⁻¹', 'c = a + b = a + b_f + b_b.', 'Same c as in the RTE.')],
 [r'b_w(500\,\mathrm{nm},S=0)=2\pi\,(1.38\times10^{-4})\left(2+\tfrac23\cdot0.835\right)=%s\ \mathrm{m^{-1}}' % sci(W['morel_500_S0']['b_w'], 2),
  r'b_{bw}=b_w/2=%s\ \mathrm{m^{-1}}' % sci(W['morel_500_S0']['b_w'] / 2, 2)],
 'Ý nghĩa: b là tích phân β trên mọi hướng; chia đôi theo 90° thành tán xạ tiến b_f và tán xạ ngược b_b.')

eq('iop_def', 'Definitions of a and β (slide 17)',
 [r'\sym{a}{a(\lambda)}\;=\;\lim_{\sym{dr}{\Delta r}\to 0}\frac{1}{\sym{Pi}{\Phi_i(\lambda)}}\,\frac{\sym{Pa}{\Phi_a(\lambda)}}{\sym{dr}{\Delta r}}\qquad[\mathrm{m^{-1}}]',
  r'\sym{beta}{\beta(\psi,\lambda)}\;=\;\lim_{\sym{dr}{\Delta r}\to 0}\;\lim_{\sym{dO}{\Delta\Omega}\to 0}\;\frac{\sym{Ps}{\Phi_s(\psi,\lambda)}}{\sym{Pi}{\Phi_i(\lambda)}\,\sym{dr}{\Delta r}\,\sym{dO}{\Delta\Omega}}\qquad[\mathrm{m^{-1}\,sr^{-1}}]'],
 [S('a', 'B', r'a', 'absorption coefficient', 'm⁻¹', 'Absorbed fraction of the incident flux per unit path.', 'A rate: doubling the path doubles the absorbed fraction (thin slab).'),
  S('beta', 'O', r'\beta', 'volume scattering function', 'm⁻¹ sr⁻¹', 'Scattered power per unit solid angle, per metre, per incident flux.', 'Contains all the angular information about scattering.'),
  S('Pi', 'K', r'\Phi_i', 'incident flux', 'W', 'Power entering the thin volume ΔV.', 'It cancels: IOPs do not depend on how bright the beam is.'),
  S('Pa', 'R', r'\Phi_a', 'absorbed flux', 'W', 'Power absorbed inside ΔV.', ''),
  S('Ps', 'G', r'\Phi_s', 'scattered flux', 'W', 'Power scattered at angle ψ into ΔΩ.', ''),
  S('dr', 'P', r'\Delta r', 'thickness', 'm', 'Thickness of the volume, taken to the limit 0.', 'Limits make a and β properties of the water, not of the instrument.'),
  S('dO', 'P', r'\Delta\Omega', 'solid angle', 'sr', 'Detector cone around ψ, taken to the limit 0.', '')],
 [], 'Ý nghĩa: a là tỉ lệ công suất bị hấp thụ trên mỗi mét; β là công suất tán xạ vào một góc khối ở góc ψ, trên mỗi mét; không phụ thuộc cường độ chùm tới.')

eq('additivity', 'Additivity of IOPs (slide 19)',
 [r'\sym{a}{a}\;=\;\underbrace{\sym{aw}{a_w}}_{\footnotesize\text{water}}+\underbrace{\sym{acdom}{a_{CDOM}}}_{\footnotesize\text{dissolved}}+\underbrace{\sym{aph}{a_{ph}}}_{\footnotesize\text{phytoplankton}}+\underbrace{\sym{anap}{a_{NAP}}}_{\footnotesize\text{detritus, minerals}}',
  r'\sym{b}{b}=\sym{bw}{b_w}+\sym{bp}{b_p}\qquad\qquad \sym{bbt}{b_b}=\sym{bbw}{b_{bw}}+\sym{bbp}{b_{bp}}'],
 [S('a', 'B', 'a', 'total absorption', 'm⁻¹', 'Sum of the independent contributions.', 'Additivity lets us model each constituent alone.'),
  S('aw', 'K', 'a_w', 'water', 'm⁻¹', 'Pure sea water.', 'Minimum in the blue, strong rise beyond 550 nm.', [('minimum', '≈ 0.005 m⁻¹ near 415 nm', 'slide 24, read from graph')]),
  S('acdom', 'O', 'a_{CDOM}', 'coloured dissolved organic matter', 'm⁻¹', 'Passes a 0.2 µm filter.', 'Exponential in λ, slope S′ ≈ 0.014 nm⁻¹.', [('S′', '0.014 nm⁻¹ (0.007–0.026)', 'slide 41; textbook CDOM')]),
  S('aph', 'G', 'a_{ph}', 'phytoplankton', 'm⁻¹', 'Pigment absorption, reduced by packaging.', 'Peaks at 443 and 675 nm.', [('Chl a peaks', '443 and 675 nm', 'slide 28')]),
  S('anap', 'P', 'a_{NAP}', 'non-algal particles', 'm⁻¹', 'Detritus, bacteria, minerals.', 'Exponential like CDOM; they are lumped as a_cdm.', [('S', '0.011 nm⁻¹ on average', 'slide 35')]),
  S('b', 'G', 'b', 'total scattering', 'm⁻¹', 'Water + particles.', 'Particles dominate in most waters.'),
  S('bw', 'K', 'b_w', 'water scattering', 'm⁻¹', 'Molecular scattering.', 'λ⁻⁴·³ dependence.', [('500 nm, S = 37', f'{W["morel_500_S37"]["b_w"]:.2e} m⁻¹', 'verified.json')]),
  S('bp', 'G', 'b_p', 'particle scattering', 'm⁻¹', 'All particles.', 'Weak spectral dependence (λⁿ).'),
  S('bbt', 'P', 'b_b', 'total backscattering', 'm⁻¹', 'Backward hemisphere.', 'Sum of water and particle parts.'),
  S('bbw', 'K', 'b_{bw}', 'water backscattering', 'm⁻¹', 'Half of b_w.', ''),
  S('bbp', 'P', 'b_{bp}', 'particle backscattering', 'm⁻¹', 'Measured by 117° sensors.', 'b_bp/b_p reveals particle type.')],
 [r'\text{Illustrative: }a=0.01+0.02+0.03+0.01=0.07\ \mathrm{m^{-1}}\ \ (\text{water, CDOM, phytoplankton, NAP})'],
 'Ý nghĩa: các IOP cộng được theo từng thành phần, nên mô hình hóa riêng rồi cộng lại (không đúng với AOP).')

eq('beer', 'Beer–Lambert for a collimated beam (RTE without gain)',
 [r'\sym{Lr}{L(r)}=\sym{L0}{L_0}\,e^{-\sym{c}{c}\,\sym{r}{r}}\qquad\Longrightarrow\qquad\sym{T}{T}=\frac{L}{L_0}=e^{-\sym{c}{c}\,\sym{Lp}{L}}',
  r'\sym{c}{c}=-\frac{\ln\sym{T}{T}}{\sym{Lp}{L}}'],
 [S('L0', 'K', 'L_0', 'initial radiance', 'W m⁻² sr⁻¹', 'Beam entering the water.', 'Cancels in T.'),
  S('Lr', 'K', 'L(r)', 'radiance after distance r', 'W m⁻² sr⁻¹', 'What is left of the beam.', ''),
  S('c', 'R', 'c', 'attenuation coefficient', 'm⁻¹', 'a + b.', 'e-folding path 1/c: at r = 1/c the beam is at 37 %.', [('example', '1.0 m⁻¹ (0.25 m path → T = %.3f)' % V['beer_lambert_T']['c1.0_L0.25'], 'verified.json')]),
  S('r', 'O', 'r', 'distance along the beam', 'm', 'Variable path.', ''),
  S('Lp', 'O', 'L', 'instrument path length', 'm', 'Fixed geometry of the transmissometer.', 'Illustrative 0.25 m on this site.', [('used here', '0.25 m', 'illustrative')]),
  S('T', 'B', 'T', 'transmittance', '—', 'Fraction reaching the detector.', 'Measure T, then c = −ln T / L.', [('T = 0.90', 'c = %.3f m⁻¹' % V['c_from_T_25cm']['0.9'], 'verified.json'), ('T = 0.50', 'c = %.3f m⁻¹' % V['c_from_T_25cm']['0.5'], 'verified.json')])],
 [r'c=1.0\ \mathrm{m^{-1}},\ L=0.25\ \mathrm{m}:\ \ T=e^{-1.0\times0.25}=%.3f' % V['beer_lambert_T']['c1.0_L0.25'],
  r'T=0.90,\ L=0.25\ \mathrm{m}:\ \ c=-\frac{\ln 0.90}{0.25}=%.3f\ \mathrm{m^{-1}}' % V['c_from_T_25cm']['0.9']],
 'Ý nghĩa: chùm song song suy giảm theo hàm mũ với c = a + b; đo T trên quãng đường L suy ra c.')

eq('vsf_morel', 'Pure sea-water VSF, Morel 1974 (slide 20)',
 [r'\begin{aligned}\sym{beta}{\beta_w(\theta,\lambda,S)}&=\underbrace{\sym{A}{1.38}\left(\frac{\sym{lam}{\lambda}}{500\,\mathrm{nm}}\right)^{\sym{ex}{-4.32}}}_{\footnotesize\text{blue scatters more}}\;\underbrace{\left(1+\frac{0.3\,\sym{Ssal}{S}}{37}\right)}_{\footnotesize\text{salt}}\\[0.15em]&\quad\times10^{-4}\;\underbrace{\left[1+\cos^{2}\sym{th}{\theta}\,\sym{del}{\frac{1-\delta}{1+\delta}}\right]}_{\footnotesize\text{forward = backward}}\end{aligned}',
  r'\sym{bw}{b_w}=2\pi\,\beta_w(90^\circ)\left(2+\tfrac{2}{3}\tfrac{1-\delta}{1+\delta}\right)\qquad b_{bw}=\tfrac12\,\sym{bw}{b_w}'],
 [S('beta', 'O', r'\beta_w', 'pure-water VSF', 'm⁻¹ sr⁻¹', 'Einstein–Smoluchowski scattering by density fluctuations.', 'Symmetric about 90°.', [('90°, 546 nm, S = 0 (Morel form)', f'{V["beta90_546_morel_S0"]:.3e}', 'verified.json'), ('same, Buiteveld form', f'{V["beta90_546_buiteveld_S0"]:.3e}', 'verified.json'), ('textbook value', '0.869e-4 (Morel recalled 0.83e-4)', 'Physics of Scattering')]),
  S('A', 'G', '1.38', 'amplitude at 500 nm', '10⁻⁴ m⁻¹ sr⁻¹', 'Fit to theoretical calculations.', 'Buiteveld 1994 revised it to 1.29.', [('Morel 1974', '1.38', 'slide 20'), ('Buiteveld 1994', '1.29', 'slide 23')]),
  S('lam', 'B', r'\lambda', 'wavelength', 'nm', 'Reference wavelength 500 nm.', 'Blue scatters more than green.', [('450 nm vs 550 nm', '×%.2f (−4.32)' % V['ratio_450_550_morel'], 'verified.json')]),
  S('ex', 'R', '-4.32', 'spectral exponent', '—', 'Almost Rayleigh (λ⁻⁴).', 'Revised to −4.14 (Buiteveld 1994).', [('Morel 1974', '−4.32', 'slide 20'), ('Buiteveld 1994', '−4.14', 'slide 23'), ('450/550 nm with −4.14', '×%.2f' % V['ratio_450_550_buiteveld'], 'verified.json')]),
  S('Ssal', 'P', 'S', 'salinity', 'PSU (g kg⁻¹)', 'Ions amplify density fluctuations.', '+30 % at S = 37.', [('fresh → ocean', '0 → 37: +30 %', 'slide 20'), ('b_w(500): S = 0 / 37', '%.2e / %.2e m⁻¹' % (W['morel_500_S0']['b_w'], W['morel_500_S37']['b_w']), 'verified.json')]),
  S('th', 'K', r'\theta', 'scattering angle', 'rad', 'Angle between incident and scattered directions.', 'Minimum of β at 90°.'),
  S('del', 'O', r'\frac{1-\delta}{1+\delta}', 'depolarisation', '—', 'δ = depolarisation factor.', 'The slide prints “cos2θ”; read here as cos²θ.', [('δ Morel', '0.09', 'slide 20'), ('δ Buiteveld', '0.051', 'slide 23'), ('ρ in the textbook', '0.031', 'Zhang et al. 2019')]),
  S('bw', 'G', 'b_w', 'total scattering of water', 'm⁻¹', '2π∫β sinθ dθ.', 'b_bw = b_w/2.', [('500 nm, S = 37', '%.2e m⁻¹' % W['morel_500_S37']['b_w'], 'verified.json')])],
 [r'\lambda=450\,\mathrm{nm},\ S=37:\ \ \beta_w(90^\circ)=1.38\,(450/500)^{-4.32}\,(1+0.3)\,10^{-4}=%s\ \mathrm{m^{-1}sr^{-1}}' % sci(W['morel_450_S37']['beta90'], 2),
  r'b_w(450\,\mathrm{nm})=%s\ \mathrm{m^{-1}}\qquad \frac{b_w(450)}{b_w(550)}=\left(\frac{550}{450}\right)^{4.32}=%.2f' % (sci(W['morel_450_S37']['b_w'], 2), V['ratio_450_550_morel'])],
 'Ý nghĩa: nước biển tán xạ ∝ λ^−4,32 (xanh mạnh hơn đỏ), muối +30 %, phân bố góc đối xứng nên b_bw = b_w/2.')

eq('a_water', 'Absorption from the imaginary index (textbook, Water)',
 [r'\sym{a}{a}\;=\;\frac{4\pi\,\sym{k}{k}}{\sym{lam}{\lambda}}\qquad\qquad \sym{m}{m}=\sym{n}{n}+i\,\sym{k}{k}'],
 [S('a', 'B', 'a', 'absorption coefficient', 'm⁻¹', 'Rate of absorption of a propagating wave.', 'Obtained from measurements, not first principles.', [('pure-water minimum', '≈ 0.005 m⁻¹ near 415 nm', 'slide 24, read from graph')]),
  S('k', 'R', 'k', 'imaginary index', '—', 'Imaginary part of the refractive index.', 'Sets absorption.'),
  S('lam', 'K', r'\lambda', 'wavelength', 'm', 'Vacuum wavelength.', 'a ∝ k/λ.'),
  S('m', 'K', 'm', 'complex refractive index', '—', 'm = n + ik.', ''),
  S('n', 'G', 'n', 'real index', '—', 'Sets elastic scattering.', 'Range 1.33–1.35 near the surface.', [('sea water, visible', '1.33–1.35', 'textbook Water')])],
 [], 'Ý nghĩa: hấp thụ do phần ảo k của chiết suất; phần thực n quyết định tán xạ.')

eq('package', 'Package effect (slide 33; sphere form Morel & Bricaud 1981)',
 [r'\sym{Q}{Q^{*}_a(\lambda)}\;=\;\frac{\sym{aphi}{a_\varphi(\lambda)}}{\sym{asol}{a_{sol}(\lambda)}}\qquad \sym{asol}{a_{sol}(\lambda)}=\sum_i \sym{Ci}{C_i}\,\sym{astar}{a^{*}_{sol,i}(\lambda)}',
  r'\sym{Q}{Q^{*}_a(\rho)}\;=\;\frac{3}{2\rho}\left[1+\frac{2e^{-\rho}}{\rho}+\frac{2\,(e^{-\rho}-1)}{\rho^{2}}\right]\qquad \sym{rho}{\rho}=a_{cell}\,d'],
 [S('Q', 'R', r'Q^{*}_a', 'package factor', '—', 'Absorption of pigment inside cells ÷ absorption of the same pigment in solution.', '1 = no packaging; → 0 = maximal self-shading.', [('ρ = 0.2', '%.2f' % PK['0.2'], 'verified.json'), ('ρ = 1', '%.2f' % PK['1.0'], 'verified.json'), ('ρ = 5', '%.2f' % PK['5.0'], 'verified.json'), ('field, Chl 10–30 mg m⁻³', '≈ 0.4 at 440 nm', 'slide 33, read from graph')]),
  S('aphi', 'B', r'a_\varphi', 'phytoplankton absorption', 'm⁻¹', 'Measured in vivo.', ''),
  S('asol', 'G', r'a_{sol}', 'absorption in solution', 'm⁻¹', 'Sum over pigments.', 'The no-self-shading reference.'),
  S('Ci', 'O', r'C_i', 'pigment concentration', 'mg m⁻³', 'Concentration of pigment i (from HPLC).', ''),
  S('astar', 'O', r'a^{*}_{sol,i}', 'specific absorption in solvent', 'm² mg⁻¹', 'Per-unit-mass absorption of pigment i.', '', [('Chl a peak ≈ 675 nm', '≈ 0.033 m² mg⁻¹', 'slide 29, read from graph')]),
  S('rho', 'P', r'\rho', 'optical thickness of the cell', '—', 'Intracellular absorption × diameter.', 'Large cells (high Chl) have large ρ, so a*_ph drops up to ×4.', [('a*_ph, low → high Chl', '≈ 0.1 → 0.02 m² mg⁻¹', 'slide 32, read from graph')])],
 [r'\rho=1:\ \ Q^{*}_a=\frac{3}{2}\left[1+2e^{-1}+2(e^{-1}-1)\right]=%.3f\ \ (\text{about 29 \%% less absorption})' % PK['1.0']],
 'Ý nghĩa: sắc tố trong tế bào lớn che nhau nên hấp thụ ít hơn so với khi hòa tan; Q* giảm từ 1 về 0 khi tế bào lớn lên.')

eq('expabs', 'Exponential absorption of CDOM and NAP (slides 35, 41)',
 [r'\sym{a}{a(\lambda)}\;=\;\sym{a0}{a(\lambda_0)}\,\exp\!\big[-\,\sym{S}{S}\,(\sym{lam}{\lambda}-\sym{lam0}{\lambda_0})\big]'],
 [S('a', 'B', 'a(\\lambda)', 'absorption at λ', 'm⁻¹', 'Wanted value.', ''),
  S('a0', 'G', r'a(\lambda_0)', 'reference absorption', 'm⁻¹', 'Value at the chosen reference wavelength.', 'Sets the amount; S sets the shape.', [('example', '0.30 m⁻¹ at 412 nm', 'illustrative')]),
  S('S', 'R', 'S', 'spectral slope', 'nm⁻¹', 'Exponential decay rate toward the red.', 'High S′ = fulvic (marine); low S′ = humic (terrestrial).', [('CDOM mean S′', '0.014 (range 0.007–0.026)', 'slide 41; textbook'), ('NAP mean S', '0.011', 'slide 35'), ('e-folding 1/S′', '71 nm', 'computed')]),
  S('lam', 'O', r'\lambda', 'wavelength', 'nm', 'Wavelength of interest.', ''),
  S('lam0', 'P', r'\lambda_0', 'reference wavelength', 'nm', 'Typically 412, 440 or 443 nm.', '', [('used in examples', '412 → 443 nm', 'this site')])],
 [r'a(443)=0.30\,\exp[-0.014\,(443-412)]=0.30\times%.3f=%.3f\ \mathrm{m^{-1}}' % (V['cdom_ratio_443_from_412_S014'], 0.3 * V['cdom_ratio_443_from_412_S014']),
  r'\frac{a(350)}{a(440)}=e^{0.014\times90}=%.2f\ \text{(CDOM)}\quad;\quad e^{0.011\times90}=%.2f\ \text{(NAP)}' % (V['cdom_ratio_350_over_440_S014'], V['nap_ratio_350_over_440_S011'])],
 'Ý nghĩa: hấp thụ của CDOM/NAP giảm theo hàm mũ khi bước sóng tăng, độ dốc S cho biết bản chất vật chất.')

eq('powerlaw', 'Particle scattering: power law and size distribution (slides 49, 68)',
 [r'\sym{bp}{b_p(\lambda)}\;=\;\sym{bp550}{b_p(550)}\left(\frac{\sym{lam}{\lambda}}{550}\right)^{\sym{n}{n}}\qquad n\in[-3,0],\ \text{mean}\approx-1',
  r'\sym{N}{N(D)}=N_0\left(\frac{\sym{D}{D}}{D_0}\right)^{-\sym{xi}{\xi}}\qquad \sym{cp}{c_p(\lambda)}=A\,\lambda^{-\sym{gam}{\gamma}}',
  r'\sym{xi}{\xi}=\sym{gam}{\gamma}+3'],
 [S('bp', 'G', r'b_p(\lambda)', 'particle scattering at λ', 'm⁻¹', 'Scattering by all particles.', 'Steeper (n → −3) when small particles dominate.'),
  S('bp550', 'B', r'b_p(550)', 'reference scattering', 'm⁻¹', 'Value at 550 nm.', 'Sets the amount.', [('Case 1, from Chl', 'b_p(550) = 0.30 Chl^0.7', 'slide 65'), ('Chl = 1', '%.2f m⁻¹' % V['bp550_from_chl']['1.0'], 'verified.json')]),
  S('lam', 'K', r'\lambda', 'wavelength', 'nm', '', ''),
  S('n', 'R', 'n', 'spectral exponent', '—', 'Slope of b_p in log-log.', 'Absorption inside particles can distort it.', [('n = 0', 'b_p(440)/b_p(550) = %.2f' % V['bp_440_over_550']['0'], 'verified.json'), ('n = −1 (mean)', '%.2f' % V['bp_440_over_550']['-1'], 'verified.json'), ('n = −3', '%.2f' % V['bp_440_over_550']['-3'], 'verified.json'), ('Mie, Junge ξ = 4', 'n = %.2f' % V['junge_ensemble_m105']['4.0']['n_bp'], 'verified.json')]),
  S('N', 'K', r'N(D)', 'size distribution', 'm⁻³ µm⁻¹', 'Number of particles of diameter D.', ''),
  S('D', 'K', 'D', 'particle diameter', 'µm', '', '', [('range of the fits', '0.1–100 µm', 'slide 68')]),
  S('xi', 'P', r'\xi', 'Junge slope', '—', 'Larger ξ = more small particles.', 'ξ = γ + 3.', [('PSD slope 1–17 µm', '≈ 3 (mode)', 'slide 68'), ('PSD slope 0.6–1 µm', '≈ 5–7 (mode)', 'slide 68'), ('textbook Junge law', 'n(D) ∝ D⁻⁴ ⇒ ξ = 4', 'Particle Size Distributions')]),
  S('cp', 'O', r'c_p', 'particle attenuation', 'm⁻¹', 'c_p = b_p + a_p.', ''),
  S('gam', 'O', r'\gamma', 'attenuation slope', '—', 'c_p ∝ λ⁻γ.', 'Measured with an ac meter.', [('ξ = 4', 'γ = 1', 'verified.json (Mie check)')])],
 [r'b_p(550)=1.0\ \mathrm{m^{-1}},\ n=-1:\ \ b_p(440)=1.0\,(440/550)^{-1}=%.2f\ \mathrm{m^{-1}}' % V['bp_440_over_550']['-1'],
  r'\xi=4\ \Rightarrow\ \gamma=\xi-3=1\ \Rightarrow\ n=-\gamma=-1\ \ (\text{Mie: }%.2f)' % V['junge_ensemble_m105']['4.0']['n_bp']],
 'Ý nghĩa: tán xạ hạt phụ thuộc bước sóng yếu theo lũy thừa n; n liên hệ với phân bố kích thước qua ξ = γ + 3.')

eq('bb117', 'Backscattering sensor at 117° (slide 62)',
 [r'\sym{bp}{\beta_p(117^\circ)}\;=\;\sym{b}{\beta(117^\circ)}\;-\;\sym{bw}{\beta_w(117^\circ)}',
  r'\sym{bbp}{b_{bp}}\;=\;2\pi\,\sym{chi}{\chi}\,\sym{bp}{\beta_p(117^\circ)}'],
 [S('bp', 'G', r'\beta_p(117^\circ)', 'particle VSF at 117°', 'm⁻¹ sr⁻¹', 'Measured minus pure water.', ''),
  S('b', 'B', r'\beta(117^\circ)', 'measured VSF', 'm⁻¹ sr⁻¹', 'Signal of the sensor.', ''),
  S('bw', 'K', r'\beta_w(117^\circ)', 'pure-water VSF', 'm⁻¹ sr⁻¹', 'Computed from the Morel/Buiteveld formula.', '', [('90°, 546 nm', f'{V["beta90_546_morel_S0"]:.2e}', 'verified.json')]),
  S('bbp', 'R', r'b_{bp}', 'particle backscattering', 'm⁻¹', 'Backward-hemisphere integral.', ''),
  S('chi', 'O', r'\chi', 'conversion factor', '—', 'Converts β(117°) to the whole backward hemisphere.', 'Hides an assumption on the particle phase function.', [('at 117°', '≈ 1.0–1.1', 'slide 62, read from graph')])],
 [r'\chi=1.1,\ \beta_p=1.0\times10^{-3}\ \mathrm{m^{-1}sr^{-1}}:\ \ b_{bp}=2\pi\times1.1\times10^{-3}=%s\ \mathrm{m^{-1}}' % sci(V['bbp_example_chi1p1_beta1e-3'], 2)],
 'Ý nghĩa: đo β ở một góc 117°, trừ phần nước, rồi nhân 2πχ để suy ra tán xạ ngược của hạt.')

eq('iop_sum', 'F2 · From particles to IOPs (slide 63)',
 [r'\sym{IOP}{\mathrm{IOP}(\lambda)}\;=\;\sum_i\sym{N}{\frac{N_i}{V}}\,\sym{sig}{\sigma_i(\lambda)}',
  r'=\;\sum_i\;\underbrace{\sym{N}{\frac{N_i}{V}}}_{\footnotesize\text{number per m³}}\;\underbrace{\sym{Q}{Q_i(\lambda)}}_{\footnotesize\text{efficiency}}\;\underbrace{\sym{Sa}{S_i}}_{\footnotesize\text{area (m²)}}'],
 [S('IOP', 'R', r'\mathrm{IOP}', 'a, b, b_b or c', 'm⁻¹', 'Any inherent optical property of particles.', ''),
  S('sig', 'P', r'\sigma_i', 'IOP cross-section', 'm²', 'σ = Q·S for one particle of class i.', ''),
  S('N', 'B', r'\frac{N_i}{V}', 'number concentration', 'm⁻³', 'Particles of class i per cubic metre.', 'Many small particles can outweigh a few large ones.', [('example', '10⁷ m⁻³', 'illustrative'), ('two-population example', '10¹¹ m⁻³ (0.5 µm) vs 10⁶ m⁻³ (10 µm)', 'illustrative')]),
  S('Q', 'G', r'Q_i', 'efficiency factor', '—', 'Flux absorbed or scattered ÷ flux hitting the geometric cross-section.', 'Q ≈ 2 for large non-absorbing spheres; ≪ 1 for very small ones.', [('large sphere', '≈ 2', 'textbook/van de Hulst'), ('r = 5 µm, m = 1.05, 550 nm (Mie)', '%.2f' % V['mie_qext_r5um_550nm_m105'], 'verified.json')]),
  S('Sa', 'O', r'S_i', 'geometric area', 'm²', 'πr² for a sphere of radius r.', 'Large particles ∝ area, small particles ∝ volume (slide 64).', [('r = 5 µm', '%.3e m²' % (math.pi * 25e-12), 'computed')])],
 [r'N/V=10^{7}\ \mathrm{m^{-3}},\ Q=2,\ r=5\,\mu\mathrm{m}:\ \ c=10^{7}\times2\times\pi(5\times10^{-6})^{2}=%s\ \mathrm{m^{-1}}' % sci(V['sum_N_sigma_c_example'], 2)],
 'Ý nghĩa: IOP = tổng theo lớp hạt của (số hạt) × (hiệu suất Q) × (diện tích hình học).')

eq('spectral', 'F3 · Spectral laws of the lecture',
 [r'\sym{acdom}{a_{cdom}(\lambda)}=a_{cdom}(\lambda_0)\,\exp\!\big[-\sym{Sp}{S^{\prime}}(\lambda-\lambda_0)\big]',
  r'\sym{Sp}{S^{\prime}}\approx0.014\ \mathrm{nm^{-1}}\quad(\mathrm{NAP}:\ S\approx0.011)',
  r'\sym{bp}{b_p(\lambda)}=b_p(550)\,(\lambda/550)^{\sym{n}{n}}\qquad \sym{n}{n}\approx-1',
  r'\sym{bw}{\beta_w}\propto\lambda^{-4.32}\ \ (\text{or }\lambda^{-4.14})'],
 [S('acdom', 'B', r'a_{cdom}', 'dissolved matter', 'm⁻¹', 'Exponential decay toward the red.', 'Steep = marine fulvic; shallow = terrestrial humic.', [('a(443) from 0.30 at 412', '%.3f m⁻¹' % (0.3 * V['cdom_ratio_443_from_412_S014']), 'verified.json')]),
  S('Sp', 'R', r'S^{\prime}', 'CDOM slope', 'nm⁻¹', 'Decay rate.', '', [('mean', '0.014', 'slide 41'), ('NAP', '0.011', 'slide 35')]),
  S('bp', 'G', r'b_p', 'particles', 'm⁻¹', 'Weak power law.', 'Flatter = larger particles.'),
  S('n', 'O', 'n', 'exponent', '—', '0 to −3.', '', [('mean', '−1', 'slide 49')]),
  S('bw', 'P', r'\beta_w', 'pure water', 'm⁻¹ sr⁻¹', 'Strong, almost Rayleigh dependence.', 'Why the open ocean is blue.', [('450/550 nm', '×%.2f' % V['ratio_450_550_morel'], 'verified.json')])],
 [], 'Ý nghĩa: ba "chữ ký phổ": mũ cho CDOM/NAP, lũy thừa yếu cho hạt, λ^−4,3 cho nước.')

eq('kd', 'Diffuse attenuation, euphotic and Secchi depth (textbook)',
 [r'\sym{Kd}{K_d}\equiv-\frac{d\ln \sym{Ed}{E_d}}{\sym{z}{dz}}\qquad \sym{Ed}{E_d}(z)=E_d(0)\,\exp\!\big(-\sym{Kd}{K_d}\,z\big)',
  r'\sym{a}{a}\le \sym{Kd}{K_d}\,\sym{mu}{\bar\mu_d}\le \sym{c}{c}',
  r'\sym{z1}{z_{1\%}}=\frac{\ln 100}{\sym{Kd}{K_d}}\approx\frac{4.605}{K_d}\qquad\qquad \sym{zsd}{z_{SD}}=\frac{\sym{G}{\Gamma}}{K_{dv}+c_v}'],
 [S('Kd', 'R', 'K_d', 'diffuse attenuation coefficient', 'm⁻¹', 'Exponential decay rate of downwelling irradiance with depth.', 'An AOP (depends on the Sun angle); 1/K_d is the penetration depth.', [('clear ocean', '0.04 m⁻¹', 'illustrative'), ('coastal', '0.3 m⁻¹', 'illustrative')]),
  S('Ed', 'K', 'E_d', 'downwelling irradiance', 'W m⁻² nm⁻¹', 'Plane irradiance from above.', 'Changes ×10 when a cloud passes: not a good AOP.'),
  S('z', 'K', 'dz', 'depth element', 'm', '', ''),
  S('a', 'B', 'a', 'absorption', 'm⁻¹', 'Lower bound of K_d μ̄_d.', ''),
  S('c', 'G', 'c', 'attenuation', 'm⁻¹', 'Upper bound.', 'K_d < c unless the beam is collimated and vertical.'),
  S('mu', 'O', r'\bar\mu_d', 'average cosine of the downwelling light', '—', 'Directional structure of the light field.', 'K_d ≈ a/μ̄_d.'),
  S('z1', 'P', r'z_{1\%}', 'euphotic depth', 'm', 'Depth where E_d falls to 1 % of the surface value.', '', [('K_d = 0.04', '%.1f m' % EU['0.04']['z1pct'], 'verified.json'), ('K_d = 0.1', '%.1f m' % EU['0.1']['z1pct'], 'verified.json'), ('K_d = 0.3', '%.1f m' % EU['0.3']['z1pct'], 'verified.json')]),
  S('zsd', 'P', r'z_{SD}', 'Secchi depth', 'm', 'Depth where a white disk disappears.', 'Transparency from a simple instrument.', [('K_d = 0.1, c = 0.2, Γ = 8', '%.1f m' % SC['Kd0.1_c0.2'], 'verified.json')]),
  S('G', 'O', r'\Gamma', 'contrast constant', '—', 'Depends on disk and water reflectance.', 'Iterated because K_dv and c_v are averages to z_SD.', [('range', '6–9', 'textbook'), ('HydroLight default', '8', 'textbook')])],
 [r'K_d=0.04\ \mathrm{m^{-1}}:\ \ z_{1\%%}=\frac{4.605}{0.04}=%.1f\ \mathrm{m}' % EU['0.04']['z1pct'],
  r'K_d=0.1,\ c=0.2\ \mathrm{m^{-1}},\ \Gamma=8:\ \ z_{SD}=\frac{8}{0.1+0.2}=%.1f\ \mathrm{m}' % SC['Kd0.1_c0.2']],
 'Ý nghĩa: K_d là tốc độ suy giảm của bức xạ xuống; độ sâu 1 % = 4,6/K_d; Secchi = Γ/(K_d + c).')

eq('refl', 'Reflectances (textbook)',
 [r'\sym{R}{R(z,\lambda)}=\frac{\sym{Eu}{E_u}}{\sym{Ed}{E_d}}\qquad\qquad \sym{Rrs}{R_{rs}}=\frac{\sym{Lw}{L_w}}{\sym{Ed}{E_d}}\ \ [\mathrm{sr^{-1}}]'],
 [S('R', 'B', 'R', 'irradiance reflectance', '—', 'Upwelling over downwelling irradiance.', 'Rises with b_b/(a+b_b) (classical, not on the crawled pages).'),
  S('Eu', 'O', 'E_u', 'upwelling irradiance', 'W m⁻² nm⁻¹', '', ''),
  S('Ed', 'K', 'E_d', 'downwelling irradiance', 'W m⁻² nm⁻¹', '', ''),
  S('Rrs', 'G', 'R_{rs}', 'remote-sensing reflectance', 'sr⁻¹', 'What a satellite derives after atmospheric correction.', ''),
  S('Lw', 'P', 'L_w', 'water-leaving radiance', 'W m⁻² sr⁻¹ nm⁻¹', 'Radiance leaving the sea.', 'Not the same as sea-surface reflection (slide 7).')],
 [], 'Ý nghĩa: phản xạ = bức xạ đi lên / bức xạ đi xuống; R_rs có đơn vị sr⁻¹.')


B450 = W['buiteveld_450_S37']; M450 = W['morel_450_S37']
eq('vsf_buit', 'Pure sea-water VSF, Buiteveld et al. 1994 (slide 23)',
 [r'\begin{aligned}\sym{beta}{\beta_w(\theta,\lambda,S)}&=\underbrace{\sym{A}{1.29}\left(\frac{\sym{lam}{\lambda}}{500\,\mathrm{nm}}\right)^{\sym{ex}{-4.14}}}_{\footnotesize\text{reformulated index}}\;\underbrace{\left(1+\frac{0.3\,\sym{Ssal}{S}}{37}\right)}_{\footnotesize\text{salt}}\\[0.15em]&\quad\times10^{-4}\;\underbrace{\left[1+\cos^{2}\sym{th}{\theta}\,\sym{del}{\frac{1-\delta}{1+\delta}}\right]}_{\footnotesize\text{forward = backward}}\end{aligned}'],
 [S('beta', 'O', r'\beta_w', 'pure-water VSF', 'm⁻¹ sr⁻¹', 'Same physics as Morel (1974), refitted 20 years later.', 'Accounts for the isothermal compressibility of water.', [('90°, 546 nm, S = 0', f'{V["beta90_546_buiteveld_S0"]:.3e}', 'verified.json')]),
  S('A', 'G', '1.29', 'amplitude at 500 nm', '10⁻⁴ m⁻¹ sr⁻¹', 'Replaces 1.38.', '6 % lower amplitude.', [('Buiteveld 1994', '1.29', 'slide 23')]),
  S('lam', 'B', r'\lambda', 'wavelength', 'nm', '', ''),
  S('ex', 'R', '-4.14', 'spectral exponent', '—', 'Reformulated refractive index and compressibility.', 'Slightly less blue-biased than −4.32.', [('Buiteveld 1994', '−4.14', 'slide 23'), ('450/550 nm', '×%.2f' % V['ratio_450_550_buiteveld'], 'verified.json')]),
  S('Ssal', 'P', 'S', 'salinity', 'PSU', 'Same +30 % at S = 37.', ''),
  S('th', 'K', r'\theta', 'scattering angle', 'rad', '', ''),
  S('del', 'O', r'\frac{1-\delta}{1+\delta}', 'depolarisation', '—', 'δ = 0.051 here (0.09 in Morel).', 'The slide prints “cos2θ”; read as cos²θ.', [('δ', '0.051', 'slide 23')])],
 [r'\lambda=450\,\mathrm{nm},\ S=37:\ \ \beta_w(90^\circ)=%s\ \mathrm{m^{-1}sr^{-1}}\qquad b_w=%s\ \mathrm{m^{-1}}' % (sci(B450['beta90'], 2), sci(B450['b_w'], 2)),
  r'\frac{b_w(450)}{b_w(550)}=\left(\frac{550}{450}\right)^{4.14}=%.2f\ \ (\text{Morel: }%.2f)' % (V['ratio_450_550_buiteveld'], V['ratio_450_550_morel'])],
 'Ý nghĩa: bản chỉnh năm 1994 của công thức Morel: biên độ 1,29, mũ −4,14, δ = 0,051.')

eq('bw_closed', 'Total scattering of pure water from the VSF (home-made closed form)',
 [r'\sym{bw}{b_w}=2\pi\,\sym{b90}{\beta_w(90^\circ)}\left(2+\frac{2}{3}\,\sym{k}{\frac{1-\delta}{1+\delta}}\right)',
  r'\sym{bbw}{b_{bw}}=\tfrac12\,\sym{bw}{b_w}'],
 [S('bw', 'G', 'b_w', 'total scattering of water', 'm⁻¹', '2π∫β sinθ dθ done analytically.', 'Verified against numerical integration (agree to 10⁻⁹).', [('500 nm, S = 37', '%.2e m⁻¹' % W['morel_500_S37']['b_w'], 'verified.json'), ('500 nm, S = 0', '%.2e m⁻¹' % W['morel_500_S0']['b_w'], 'verified.json')]),
  S('b90', 'O', r'\beta_w(90^\circ)', 'VSF at right angle', 'm⁻¹ sr⁻¹', 'The minimum of the U-shaped VSF.', ''),
  S('k', 'P', r'\frac{1-\delta}{1+\delta}', 'anisotropy factor', '—', 'δ = depolarisation.', '0.835 for δ = 0.09.', [('Morel', '0.835', 'computed'), ('Buiteveld', '0.903', 'computed')]),
  S('bbw', 'B', 'b_{bw}', 'backscattering of water', 'm⁻¹', 'Backward half.', 'Exactly b_w/2 because β_w is symmetric about 90°.', [('b_bw/b_w', '0.5', 'verified.json')])],
 [r'b_w(500\,\mathrm{nm},S=37)=2\pi\,(1.794\times10^{-4})\,(2+0.557)=%s\ \mathrm{m^{-1}}' % sci(W['morel_500_S37']['b_w'], 2)],
 'Ý nghĩa: tích phân hàm tán xạ thể tích của nước cho b_w; một nửa là tán xạ ngược.')

eq('es', 'Einstein–Smoluchowski scattering by pure water (textbook, Physics of Scattering)',
 [r'\sym{beta}{\beta(\psi)}=\frac{2\pi^{2}\,\sym{kB}{k}\,\sym{T}{T}}{\sym{lam}{\lambda}^{4}\,\sym{bT}{\beta_T}}\;\sym{n}{n}^{2}\left(\sym{dn}{\frac{\partial n}{\partial P}}\right)_{T}^{2}\;\sym{rho}{\frac{6+6\rho}{6-7\rho}}\left[1+\frac{1-\rho}{1+\rho}\cos^{2}\sym{psi}{\psi}\right]'],
 [S('beta', 'O', r'\beta(\psi)', 'VSF of pure water', 'm⁻¹ sr⁻¹', 'Scattering from density fluctuations of the water molecules.', 'One of the few IOPs computable from physics.', [('90°, 546 nm, 20 °C', '0.869×10⁻⁴ (textbook); our recomputation 8.54×10⁻⁵', 'Physics of Scattering; verified.json'), ('Morel 1974, recalled', '0.83×10⁻⁴', 'textbook')]),
  S('kB', 'K', 'k', 'Boltzmann constant', 'J K⁻¹', '', '', [('value', '1.3806×10⁻²³', 'textbook')]),
  S('T', 'R', 'T', 'temperature', 'K', 'Hotter water = larger fluctuations.', 'Scattering increases with T.', [('used', '293.15 K (20 °C)', 'textbook')]),
  S('lam', 'B', r'\lambda', 'wavelength', 'm', 'λ⁻⁴: the Rayleigh dependence.', 'Blue scatters much more.', [('used', '546 nm', 'textbook')]),
  S('bT', 'G', r'\beta_T', 'isothermal compressibility', 'Pa⁻¹', 'More compressible = larger fluctuations.', '', [('used', '4.5893×10⁻¹⁰', 'textbook')]),
  S('n', 'K', 'n', 'refractive index', '—', '', '', [('used', '1.33477', 'textbook')]),
  S('dn', 'P', r'\partial n/\partial P', 'pressure derivative of n', 'Pa⁻¹', 'If n did not depend on pressure there would be no scattering.', '', [('used', '1.5127×10⁻¹⁰', 'textbook')]),
  S('rho', 'O', r'\frac{6+6\rho}{6-7\rho}', 'depolarisation corr.', '—', 'ρ = depolarisation ratio.', 'Differs from the lecture δ values.', [('ρ', '0.031', 'Zhang et al. 2019 via textbook'), ('lecture δ', '0.09 / 0.051', 'slides 20, 23')]),
  S('psi', 'K', r'\psi', 'scattering angle', 'rad', '', '')],
 [r'\psi=90^\circ,\ \lambda=546\,\mathrm{nm},\ T=293.15\,\mathrm{K}:\ \ \beta=%s\ \mathrm{m^{-1}sr^{-1}}\ \ (\text{textbook states }0.869\times10^{-4})' % sci(V['es_beta90_546_textbook_constants'], 2)],
 'Ý nghĩa: tán xạ của nước tinh khiết xuất phát từ thăng giáng mật độ phân tử; tính được từ vật lý cơ bản.')

eq('bp_abs', 'Effect of particle absorption on b_p (slide 53, Doxaran et al. 2009)',
 [r'\frac{\sym{dbp}{\Delta b_p}}{\sym{ap}{a_p}}\;=\;1-\tanh\!\left(0.5\,\sym{gam}{\gamma}^{2}\right)'],
 [S('dbp', 'R', r'\Delta b_p', 'lowering of measured b_p', 'm⁻¹', 'Difference between the power-law extrapolation and the measured b_p.', 'Particle absorption lowers b_p by 5–30 % at 440 nm.', [('range', '5–30 %', 'slide 53')]),
  S('ap', 'B', r'a_p', 'particulate absorption', 'm⁻¹', 'Absorption by particles at the same wavelength.', ''),
  S('gam', 'O', r'\gamma', 'spectral exponent of b_p', '—', 'Exponent of the power law fitted in the near-infrared (715–870 nm).', 'The exponent “2” of γ is read from the slide image.', [('example', 'γ = 1', 'illustrative')])],
 [r'\gamma=1:\ \ \frac{\Delta b_p}{a_p}=1-\tanh(0.5)=%.3f' % (1 - math.tanh(0.5)), r'\gamma=2:\ \ 1-\tanh(2)=%.3f' % (1 - math.tanh(2))],
 'Ý nghĩa: hấp thụ bên trong hạt làm b_p đo được thấp hơn mô hình lũy thừa ngoại suy từ cận hồng ngoại.')

eq('bp_chl', 'Particle scattering from chlorophyll (slide 65, Loisel & Morel 1998)',
 [r'\sym{bp}{b_p(550)}\;=\;\sym{c0}{0.30}\;\sym{Chl}{[\mathrm{Chl}]}^{\,\sym{e}{0.7}}'],
 [S('bp', 'G', r'b_p(550)', 'particle scattering at 550 nm', 'm⁻¹', 'Case-1 relation.', 'Spread of about a factor 2–3 around the line.', [('Chl = 0.1', '%.3f m⁻¹' % V['bp550_from_chl']['0.1'], 'verified.json'), ('Chl = 1', '%.2f m⁻¹' % V['bp550_from_chl']['1.0'], 'verified.json'), ('Chl = 10', '%.2f m⁻¹' % V['bp550_from_chl']['10.0'], 'verified.json')]),
  S('c0', 'O', '0.30', 'coefficient', 'm⁻¹ (mg m⁻³)⁻⁰·⁷', 'Value at Chl = 1 mg m⁻³.', '', [('slide 65', '0.30 (±0.15)', 'slide 65')]),
  S('Chl', 'B', r'[\mathrm{Chl}]', 'chlorophyll concentration', 'mg m⁻³', 'Trophic state index.', '', [('range of data', '0.01–30', 'slide 65 graph')]),
  S('e', 'R', '0.7', 'exponent', '—', 'Below 1: scattering grows less than proportionally.', 'Tenfold more Chl gives ×5.0 scattering.', [('slide 65', '0.7 (±0.1)', 'slide 65'), ('10^0.7', '%.2f' % V['bp550_tenfold_chl_factor'], 'verified.json')])],
 [r'[\mathrm{Chl}]=1:\ \ b_p=0.30\times1^{0.7}=0.30\ \mathrm{m^{-1}}\qquad [\mathrm{Chl}]=10:\ \ b_p=0.30\times10^{0.7}=%.2f\ \mathrm{m^{-1}}' % V['bp550_from_chl']['10.0']],
 'Ý nghĩa: quan hệ thực nghiệm cho nước Case 1; Chl tăng 10 lần thì b_p chỉ tăng ≈ 5 lần.')

eq('poc_spm', 'POC/SPM from the red-to-green absorption ratio (slide 74, Wozniak et al. 2010)',
 [r'\sym{pm}{\frac{\mathrm{POC}}{\mathrm{SPM}}}\;=\;\sym{c0}{0.0133}\,\exp\!\big\{\sym{k}{1.27}\,\sym{R}{R}\big\}\qquad \sym{R}{R}=\frac{a_p(675)}{a_p(570)}'],
 [S('pm', 'G', r'\mathrm{POC/SPM}', 'organic fraction of suspended matter', '—', 'Particulate organic carbon over suspended particulate matter.', 'Higher = more organic (phytoplankton-rich).', [('R = 1', '%.3f' % V['poc_spm_from_ap_ratio']['1.0'], 'verified.json'), ('R = 2', '%.3f' % V['poc_spm_from_ap_ratio']['2.0'], 'verified.json'), ('r², n', '0.81, 44', 'slide 74')]),
  S('c0', 'O', '0.0133', 'coefficient', '—', 'Intercept of the log fit.', ''),
  S('k', 'P', '1.27', 'slope', '—', 'Sensitivity to R.', ''),
  S('R', 'B', 'R', 'absorption ratio', '—', 'Chl absorbs at 675 nm, minerals do not.', 'R rises with the organic share.', [('range of data', '≈ 0.7–2.8', 'slide 74 graph')])],
 [r'R=1:\ \ \frac{\mathrm{POC}}{\mathrm{SPM}}=0.0133\,e^{1.27}=%.3f\qquad R=2:\ \ 0.0133\,e^{2.54}=%.3f' % (V['poc_spm_from_ap_ratio']['1.0'], V['poc_spm_from_ap_ratio']['2.0'])],
 'Ý nghĩa: tỉ số hấp thụ đỏ/xanh của hạt cho biết hạt hữu cơ nhiều hay ít.')

eq('mixing', 'CDOM and salinity: conservative mixing (idea of slide 77)',
 [r'\sym{a}{a(S)}\;=\;\sym{af}{a_{fresh}}\left(1-\frac{\sym{S}{S}}{\sym{Ss}{S_{sea}}}\right)+\sym{ao}{a_{ocean}}\,\frac{\sym{S}{S}}{\sym{Ss}{S_{sea}}}'],
 [S('a', 'B', r'a(S)', 'CDOM absorption at salinity S', 'm⁻¹', 'Linear in S if only mixing acts.', 'A curve below the line means loss (photo-oxidation).'),
  S('af', 'R', r'a_{fresh}', 'river end member', 'm⁻¹', 'At 355 nm.', '', [('slide 77', '≥ 10 m⁻¹', 'slide 77'), ('used', '10', 'illustrative')]),
  S('ao', 'G', r'a_{ocean}', 'ocean end member', 'm⁻¹', 'At 355 nm.', '', [('slide 77', '≤ 0.1 m⁻¹', 'slide 77'), ('used', '0.1', 'illustrative')]),
  S('S', 'O', 'S', 'salinity', 'PSU', '', ''),
  S('Ss', 'P', r'S_{sea}', 'sea-water salinity', 'PSU', 'Salinity of the ocean end member.', '', [('used', '36', 'illustrative')])],
 [r'S=18:\ \ a=10\,(1-0.5)+0.1\times0.5=%.2f\ \mathrm{m^{-1}}' % V['cdom_mixing_example']['18']],
 'Ý nghĩa: nếu chỉ có trộn lẫn, a_cdom giảm tuyến tính từ nước ngọt (≥ 10 m⁻¹) tới đại dương (≤ 0,1 m⁻¹).')

eq('gordon', 'IOP–AOP link: reflectance from IOPs (classical result, Gordon et al. 1975)',
 [r'\sym{R}{R}\;\approx\;\sym{f}{f}\,\frac{\sym{bb}{b_b}}{\sym{a}{a}+\sym{bb}{b_b}}'],
 [S('R', 'B', 'R', 'irradiance reflectance', '—', 'Fraction of the downwelling light returned.', 'Rises with backscattering, falls with absorption.', [('clear (a = 0.02, b_b = 0.002), f = 1', '%.3f' % V['R_over_f_bb_a_examples']['clear_a0.02_bb0.002'], 'verified.json'), ('turbid (a = 0.5, b_b = 0.05), f = 1', '%.3f' % V['R_over_f_bb_a_examples']['turbid_a0.5_bb0.05'], 'verified.json')]),
  S('f', 'O', 'f', 'geometry factor', '—', 'Depends on the Sun angle and phase function.', 'Value not given on the pages we crawled.'),
  S('bb', 'P', r'b_b', 'backscattering coefficient', 'm⁻¹', '', ''),
  S('a', 'G', 'a', 'absorption coefficient', 'm⁻¹', '', '')],
 [r'a=0.02,\ b_b=0.002:\ \ \frac{R}{f}=\frac{0.002}{0.022}=%.3f' % V['R_over_f_bb_a_examples']['clear_a0.02_bb0.002']],
 'Ý nghĩa: phản xạ tăng khi tán xạ ngược b_b tăng và giảm khi hấp thụ a tăng. Đây là kết quả kinh điển, KHÔNG có trong các trang textbook đã crawl.')

eq('nap_fe', 'Mineral absorption versus iron content (slide 38, Babin & Stramski 2004)',
 [r'\sym{a3}{a^{*}_m(300)}=0.033\,\sym{Fe}{[\mathrm{Fe}]}+0.052\qquad r^{2}=0.88',
  r'\sym{a4}{a^{*}_m(400)}=0.031\,\sym{Fe}{[\mathrm{Fe}]}-0.043\qquad r^{2}=0.84',
  r'\sym{a5}{a^{*}_m(500)}=0.017\,\sym{Fe}{[\mathrm{Fe}]}-0.036\qquad r^{2}=0.59'],
 [S('a3', 'R', r'a^{*}_m(300)', 'mass-specific absorption, 300 nm', 'm² g⁻¹', 'UV absorption of mineral particles.', 'Best explained by iron (R² = 0.88).', [('[Fe] = 10 %', '%.3f' % (0.033 * 10 + 0.052), 'computed from slide-38 fit')]),
  S('a4', 'O', r'a^{*}_m(400)', 'at 400 nm', 'm² g⁻¹', '', '', [('[Fe] = 10 %', '%.3f' % (0.031 * 10 - 0.043), 'computed')]),
  S('a5', 'G', r'a^{*}_m(500)', 'at 500 nm', 'm² g⁻¹', 'Weaker relation (R² = 0.59).', '', [('[Fe] = 10 %', '%.3f' % (0.017 * 10 - 0.036), 'computed')]),
  S('Fe', 'B', r'[\mathrm{Fe}]', 'iron content', '%', 'Of the dry mass.', 'Range of the data: 0–30 %.', [('slide 38 range', '0–30 %', 'slide 38')])],
 [r'[\mathrm{Fe}]=10\%%:\ \ a^{*}_m(300)=%.3f,\ \ a^{*}_m(400)=%.3f,\ \ a^{*}_m(500)=%.3f\ \ \mathrm{m^2\,g^{-1}}' % (0.033 * 10 + 0.052, 0.031 * 10 - 0.043, 0.017 * 10 - 0.036)],
 'Ý nghĩa: hấp thụ của khoáng vật ở vùng UV–xanh tăng tuyến tính theo hàm lượng sắt.')

eq('cdom_twar', 'CDOM as a power law (slide 41, Twardowski et al. 2004)',
 [r'\sym{a}{a_{ds}(\lambda)}\;\propto\;\sym{lam}{\lambda}^{\,\sym{ex}{-6.92}}'],
 [S('a', 'B', r'a_{ds}(\lambda)', 'CDOM absorption', 'm⁻¹', 'Alternative to the exponential model.', 'Both fit the visible; they differ outside it.', [('a(350)/a(440), power law', '%.2f' % V['cdom_power_law_ratio_350_440_lam_minus_6p92'], 'verified.json'), ('same, exponential S′ = 0.014', '%.2f' % V['cdom_ratio_350_over_440_S014'], 'verified.json')]),
  S('lam', 'O', r'\lambda', 'wavelength', 'nm', '', ''),
  S('ex', 'R', '-6.92', 'exponent', '—', '', '', [('Twardowski 2004', '−6.92', 'slide 41')])],
 [r'\frac{a(350)}{a(440)}=\left(\frac{350}{440}\right)^{-6.92}=%.2f\quad\text{vs}\quad e^{0.014\times90}=%.2f' % (V['cdom_power_law_ratio_350_440_lam_minus_6p92'], V['cdom_ratio_350_over_440_S014'])],
 'Ý nghĩa: có thể mô tả CDOM bằng lũy thừa λ^−6,92 thay vì hàm mũ; hai mô hình gần nhau trong vùng khả kiến.')

eq('junge_tb', 'Junge size distribution: lecture and textbook conventions (slide 68; textbook)',
 [r'\sym{lec}{N(D)\propto D^{-\xi}}\qquad\text{(lecture)}',
  r'\sym{tb}{\frac{dN}{d\log D}\propto D^{-3}}\;\Longleftrightarrow\;\sym{nD}{n(D)=\frac{dN}{dD}\propto D^{-4}}\qquad\text{(textbook)}'],
 [S('lec', 'B', r'N(D)\propto D^{-\xi}', 'lecture notation', '—', 'ξ is the slope of the number distribution per unit diameter.', 'Classic Junge value: ξ = 4.', [('PSD slope, 1–17 µm', '≈ 3 (mode)', 'slide 68')]),
  S('tb', 'G', r'dN/d\log D', 'number per log-interval', '—', 'Per logarithmic size bin.', 'D⁻³ here is D⁻⁴ per unit D.'),
  S('nD', 'R', r'n(D)', 'number per unit diameter', '—', 'Same distribution as the lecture N(D).', 'So the textbook Junge law has ξ = 4 in lecture notation.', [('Mie check', 'ξ = 4 ⇒ n = %.2f' % V['junge_ensemble_m105']['4.0']['n_bp'], 'verified.json')])],
 [], 'Ý nghĩa: cùng một phân bố Junge, nhưng textbook dùng dN/dlogD ∝ D⁻³ tương đương n(D) ∝ D⁻⁴, tức ξ = 4 theo ký hiệu của bài giảng.')

eq('phase_ratio', 'Spectral ratio of the particulate phase function at 140° (slide 48)',
 [r'\sym{Rr}{R_{443/555}(140^\circ)}\;=\;-0.060\,\sym{x}{\frac{a_{NAP}}{a_{ph}}(400)}\;+\;0.99\qquad r^{2}=0.72'],
 [S('Rr', 'B', r'R_{443/555}', 'ratio of the phase function at 140°', '—', 'Blue over green backscattering shape.', 'Falls as NAP absorption grows relative to phytoplankton.', [('x = 4', '%.2f' % (-0.060 * 4 + 0.99), 'computed from the slide fit')]),
  S('x', 'O', r'a_{NAP}/a_{ph}(400)', 'detritus-to-phytoplankton absorption', '—', '', '', [('range of data', '2–7', 'slide 48 graph')])],
 [r'x=4:\ \ R=-0.060\times4+0.99=%.2f' % (-0.060 * 4 + 0.99)],
 'Ý nghĩa: hồi quy tuyến tính, không phải định luật; tỉ số giảm khi hấp thụ của detritus tăng.')

GIST = {'rte': 'Light in a thin slab of water is lost by absorption and by scattering out (c = a + b), gained by scattering in from every other direction, plus any light created inside.', 'iop_def': 'a is the fraction of light absorbed per metre; β is the light scattered into one direction, per metre and per steradian. Both belong to the water, not to the light.', 'iop_b': 'Adding β over all directions gives the scattering b; splitting at 90° gives forward and backward scattering; attenuation c = a + b.', 'additivity': 'Each constituent absorbs or scatters on its own, so the totals are sums: model every component alone, then add them.', 'beer': 'A collimated beam decays exponentially at rate c; measure the transmitted fraction T over a known path to find c.', 'vsf_morel': 'Pure sea water scatters almost like air (∝ λ⁻⁴·³): blue far more than red, 30 % more with salt, equal forward and backward.', 'vsf_buit': 'The same law refitted in 1994: slightly smaller amplitude and exponent, smaller depolarisation.', 'bw_closed': 'Integrating the VSF over all angles gives the total scattering of water; exactly half of it is backward.', 'es': 'Scattering by pure water comes from density fluctuations of the molecules: stronger when hotter, more compressible, and at short wavelengths.', 'a_water': 'Absorption comes from the imaginary part of the refractive index; scattering comes from the real part.', 'package': 'Pigments packed in a large cell shade each other, so the cell absorbs less than the same pigment in solution; the factor falls from 1 toward 0 as cells grow.', 'expabs': 'Dissolved and detrital matter absorb exponentially more toward the blue; the slope tells marine from terrestrial material.', 'cdom_twar': 'A power law λ⁻⁶·⁹² describes CDOM about as well as the exponential in the visible.', 'nap_fe': 'Mineral absorption in the UV–blue grows linearly with iron content.', 'powerlaw': 'Particle scattering varies weakly with wavelength as a power law; its exponent follows the size distribution (ξ = γ + 3).', 'junge_tb': 'The lecture and the textbook write the same Junge size law with different conventions, so ξ = 4 in lecture notation.', 'bp_abs': 'Absorption inside particles pulls the measured scattering down by 5–30 % in the blue.', 'phase_ratio': 'The blue/green ratio of the particle phase function at 140° falls as detrital absorption grows.', 'bb117': 'Measure scattering at 117°, remove pure water, then multiply by 2πχ to get the backscattering of particles.', 'iop_sum': 'Any particle IOP is a sum over particle classes of number × efficiency × geometric area.', 'bp_chl': 'More chlorophyll means more scattering particles, but less than proportionally (exponent 0.7); the spread is a factor 2–3.', 'poc_spm': 'The red-to-green absorption ratio of particles indicates how organic the suspended matter is.', 'mixing': 'If river and ocean water only mix, CDOM falls linearly with salinity from ≥ 10 m⁻¹ to ≤ 0.1 m⁻¹.', 'spectral': 'Three spectral fingerprints: exponential for CDOM and NAP, a weak power law for particles, almost Rayleigh for water.', 'kd': 'Light decays with depth at rate K_d: the 1 % depth is 4.6/K_d, and the Secchi depth is set by K_d and c.', 'refl': 'Reflectance is upwelling over downwelling light; the satellite quantity R_rs is water-leaving radiance over irradiance.', 'gordon': 'More backscattering raises the reflectance, more absorption lowers it (classical result, not on the crawled pages).'}
for _k, _v in GIST.items(): EQS[_k]['gist'] = _v


GIST_VSF = 'Pure sea water scatters almost like air (∝ λ⁻⁴·³): blue far more than red, 30 % more with salt, equal forward and backward.'
def subeq(new, base, idxs, label, gist):
    b = EQS[base]; lines = [b['lines'][i] for i in idxs]
    used = set(re.findall(r'\\sym\{(\w+)\}', ''.join(lines)))
    syms = {k: v for k, v in b['syms'].items() if k in used}
    EQS[new] = dict(label=label, lines=lines, syms=syms, order=[k for k in b['order'] if k in used], example=[x for x in b['example']], vi=b['vi'], gist=gist)
subeq('bp_power', 'powerlaw', [0], 'Particle scattering power law (slide 49)', 'Particle scattering varies weakly with wavelength as a power law: flat for large particles (n → 0), steep for small ones (n → −3).')
subeq('vsf_main', 'vsf_morel', [0], 'Pure sea-water VSF, Morel 1974 (slide 20)', GIST_VSF)
subeq('psd', 'powerlaw', [1, 2], 'Size distribution and attenuation slope (slide 68)', 'Particle numbers fall off as a power of diameter; the attenuation spectrum follows a power law whose slope is the size slope minus 3.')

# worked-example helper: static big KaTeX lines
def KL(*lines, cap=''):
    ls = ''.join(f'<div class="kx wex" data-tex="{html.escape(l, quote=True)}">{html.escape(l)}</div>' for l in lines)
    return f'<div class="wexbox">{ls}' + (f'<p class="wexcap">{cap}</p>' if cap else '') + '</div>'
def Ks(*lines, cap=''):
    """static big formulas for a slide column"""
    return '<div class="kxs">' + ''.join(f'<div class="kx fit" data-tex="{html.escape(l, quote=True)}">{html.escape(l)}</div>' for l in lines) + (f'<div class="kcap">{cap}</div>' if cap else '') + '</div>'

# ---------------------------------------------------------------------------------------------------------------- rendering
def _esc(s): return html.escape(s, quote=True)
def E(name, slide=False, fs=None):
    d = EQS[name]; syms = d['syms']
    st = lambda i: (f' data-fs="{fs}" style="font-size:{fs}px"' if (slide and fs) else '')
    lines = ''.join(f'<div class="kx{" sm" if i > 0 else ""}"{st(i)} data-tex="{_esc(render_tex(l, syms))}">{_esc(l)}</div>' for i, l in enumerate(d['lines']))
    data = {k: dict(syms[k], color=COL[syms[k]['c']]) for k in d['order']}
    data['_order'] = d['order']; data['_example'] = [render_tex(x, syms) for x in d['example']]; data['_vi'] = d['vi']
    js = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
    head = '<tr><th>Symbol</th><th>Name</th><th>Meaning</th><th class="imp">What it implies</th><th class="vals">Numbers assigned</th></tr>'
    rows = ''
    for k in d['order']:
        s = syms[k]; vals = '<br>'.join(f'{_esc(a)}: <b>{_esc(b)}</b> <small>({_esc(c)})</small>' for a, b, c in s['values'])
        tm = '\\textcolor{' + COL[s['c']] + '}{' + s['tex'] + '}'
        rows += (f'<tr class="lr" data-k="{k}"><td class="tm"><span class="kx inl" data-tex="{_esc(tm)}">{_esc(s["tex"])}</span></td>'
                 f'<td><b>{_esc(s["name"])}</b>{(" <small>[" + _esc(s["unit"]) + "]</small>") if s["unit"] else ""}</td><td>{_esc(s["meaning"])}</td><td class="imp"><i>{_esc(s["implication"])}</i></td><td class="vals">{vals}</td></tr>')
    hint = '<div class="eqhint">Click any coloured symbol (or a row of the table): it pops up in a frame, an arrow points to it from a note box, and its meaning, unit and the numbers assigned to it appear.</div>'
    bar = ('<div class="eqbar"><button type="button" class="btn alt eqprev">◀ previous</button><button type="button" class="btn eqnext">next symbol ▶</button>'
           + ('<button type="button" class="btn alt eqplugbtn">Plug in numbers</button>' if d['example'] else '') + '<button type="button" class="btn alt eqclear">Show all</button>' + ('<span class="eqtapb">Click any symbol for its meaning, unit and numbers</span>' if slide else '') + '</div>')
    def flat(t): return re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}', lambda m: ('(%s)/(%s)' % (m.group(1), m.group(2))) if re.search(r'[+\-]', m.group(1) + m.group(2)) else '%s/%s' % (m.group(1), m.group(2)), t)
    keys = ''.join(f'<span class="keyc" data-k="{k}"><span class="kx inl" data-tex="{_esc(chr(92) + "textcolor{" + COL[syms[k]["c"]] + "}{" + flat(syms[k]["tex"]) + "}")}">{_esc(syms[k]["tex"])}</span> {_esc(syms[k]["name"])}{(" <small>[" + _esc(syms[k]["unit"]) + "]</small>") if syms[k]["unit"] else ""}</span>' for k in d['order'])
    idle = (f'<div class="eqidle"><div class="eqgist">{_esc(d.get("gist", ""))}</div><div class="eqkey">{keys}</div></div>') if slide else ''
    stage = f'<div class="eqstage"><svg class="eqarrows"></svg>{lines}{idle}</div>'
    lab = f'<div class="eqlab">{_esc(d["label"])}</div>' + (f'<div class="eqgist">{_esc(d["gist"])}</div>' if d.get('gist') else '')
    vi = f'<div class="eqvi">{_esc(d["vi"])}</div>' if d['vi'] else ''
    plug = '<div class="eqplug" hidden></div><div class="eqinfo" hidden></div>'
    single = ' data-single="1"' if len(d['lines']) == 1 else ''
    if slide:
        return f'<div class="eqbig slide" data-eq="{name}"{single}>{stage}{bar}{plug}<script type="application/json" class="eqdata">{js}</script></div>'
    return f'<div class="eqbig" data-eq="{name}"{single}>{lab}{hint}{stage}{bar}{plug}<table class="eqleg">{head}{rows}</table>{vi}<script type="application/json" class="eqdata">{js}</script></div>'
SLIDE_FS = {'rte': 28, 'vsf_morel': 28, 'vsf_buit': 28, 'iop_b': 32, 'kd': 30, 'iop_sum': 32, 'bp_power': 34, 'psd': 34, 'vsf_main': 32, 'bw_closed': 34}
def Es(name, fs=None): return E(name, slide=True, fs=SLIDE_FS.get(name, fs))

def Krows(rows):
    """rows: [(chip word, tex, caption)] -> stacked bands, one big formula each (slide)"""
    out = ''
    for chip, tex, cap in rows:
        out += (f'<div class="krow"><div class="kchip">{chip}</div><div class="kbody"><div class="kx fit" data-tex="{html.escape(tex, quote=True)}">{html.escape(tex)}</div>'
                f'<div class="kcap">{cap}</div></div></div>')
    return f'<div class="krows">{out}</div>'
