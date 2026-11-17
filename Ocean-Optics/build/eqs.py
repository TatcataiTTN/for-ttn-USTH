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
 [r'\begin{aligned}\frac{d\sym{L}{L(\theta,\varphi)}}{\sym{r}{dr}}&=\underbrace{-\,\sym{c}{c}\,\sym{L}{L(\theta,\varphi)}}_{\footnotesize\text{loss: absorption + scattering out}}\\[0.15em]&\quad+\underbrace{\int_{4\pi}\sym{beta}{\beta(\theta,\varphi;\theta^{\prime},\varphi^{\prime})}\,\sym{L}{L(\theta^{\prime},\varphi^{\prime})}\,\sym{om}{d\omega^{\prime}}}_{\footnotesize\text{gain: scattering in from all directions}}\\[0.15em]&\quad+\underbrace{\sym{S}{S}}_{\footnotesize\text{internal sources}}\end{aligned}',
  r'\sym{c}{c}\;=\;\sym{a}{a}\;+\;\sym{b}{b}'],
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
  S('del', 'O', r'\frac{1-\delta}{1+\delta}', 'depolarisation term', '—', 'δ = depolarisation factor.', 'The slide prints “cos2θ”; read here as cos²θ.', [('δ Morel', '0.09', 'slide 20'), ('δ Buiteveld', '0.051', 'slide 23'), ('ρ in the textbook', '0.031', 'Zhang et al. 2019')]),
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
 [r'\sym{acdom}{a_{cdom}(\lambda)}=a_{cdom}(\lambda_0)\,e^{-\sym{Sp}{S^{\prime}}(\lambda-\lambda_0)}\qquad \sym{Sp}{S^{\prime}}\approx0.014\ \mathrm{nm^{-1}}\ \ (\mathrm{NAP}:\ S\approx0.011)',
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

# ---------------------------------------------------------------------------------------------------------------- rendering
def _esc(s): return html.escape(s, quote=True)
def E(name, slide=False, fs=None):
    d = EQS[name]; syms = d['syms']
    st = lambda i: (f' data-fs="{fs if i == 0 else fs - 1}" style="font-size:{fs if i == 0 else fs - 1}px"' if (slide and fs) else '')
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
           + ('<button type="button" class="btn alt eqplugbtn">Plug in numbers</button>' if d['example'] else '') + '<button type="button" class="btn alt eqclear">Show all</button></div>')
    idle = '<div class="eqidle">Click any coloured symbol: it pops up and its meaning, unit and numbers appear here, with an arrow.</div>' if slide else ''
    stage = f'<div class="eqstage"><svg class="eqarrows"></svg>{lines}{idle}</div>'
    lab = f'<div class="eqlab">{_esc(d["label"])}</div>'
    vi = f'<div class="eqvi">{_esc(d["vi"])}</div>' if d['vi'] else ''
    plug = '<div class="eqplug" hidden></div><div class="eqinfo" hidden></div>'
    single = ' data-single="1"' if len(d['lines']) == 1 else ''
    if slide:
        return f'<div class="eqbig slide" data-eq="{name}"{single}>{stage}{bar}{plug}<script type="application/json" class="eqdata">{js}</script></div>'
    return f'<div class="eqbig" data-eq="{name}"{single}>{lab}{hint}{stage}{bar}{plug}<table class="eqleg">{head}{rows}</table>{vi}<script type="application/json" class="eqdata">{js}</script></div>'
def Es(name, fs=None): return E(name, slide=True, fs=fs)
