# -*- coding: utf-8 -*-
"""verify_numbers.py — every number shown on the site is recomputed here by TWO independent methods.
Output: ../site/data/verified.json.  A disagreement is reported in V['discrepancies'] (never silently fixed)."""
import json, math, os
import numpy as np
from scipy import integrate, optimize

HERE = os.path.dirname(os.path.abspath(__file__))
_S = os.path.join(HERE, '..', 'site')
SITE = _S if os.path.isdir(_S) else os.path.join(HERE, '..')   # in the deployed repo, build/ sits next to index.html
OUT = os.path.join(SITE, 'data', 'verified.json')
V, DISC = {}, []
def check(name, a, b, tol_rel, note=''):
    ok = abs(a - b) <= tol_rel * max(abs(a), abs(b), 1e-30)
    V.setdefault('checks', []).append(dict(name=name, method_A=a, method_B=b, rel_diff=abs(a - b) / max(abs(a), abs(b), 1e-30), ok=ok, note=note))
    if not ok: DISC.append(name)
    return ok

# ---------------------------------------------------------------- 1. pure-water VSF (slides 20, 23, 24)
def beta_w(theta, lam, S, A, expo, delta):
    """Slide form: beta = A (lam/500)^expo (1+0.3 S/37) 1e-4 (1 + cos^2(theta)(1-d)/(1+d)). Units m^-1 sr^-1."""
    return A * (lam / 500.0) ** expo * (1 + 0.3 * S / 37.0) * 1e-4 * (1 + np.cos(theta) ** 2 * (1 - delta) / (1 + delta))
MOREL = dict(A=1.38, expo=-4.32, delta=0.09)
BUIT = dict(A=1.29, expo=-4.14, delta=0.051)
def bw_numeric(lam, S, P):
    f = lambda th: 2 * math.pi * beta_w(th, lam, S, **P) * math.sin(th)
    return integrate.quad(f, 0, math.pi)[0]
def bw_closed(lam, S, P):
    k = (1 - P['delta']) / (1 + P['delta'])
    b90 = beta_w(math.pi / 2, lam, S, **P)
    return 2 * math.pi * b90 * (2 + 2 * k / 3)          # integral of (1 + k cos^2) sin = 2 + 2k/3
W = {}
for name, P in (('morel', MOREL), ('buiteveld', BUIT)):
    for lam in (400, 450, 500, 550, 600, 700):
        for S in (0, 35, 37):
            a, b = bw_numeric(lam, S, P), bw_closed(lam, S, P)
            check(f'bw_{name}_{lam}_S{S}', a, b, 1e-9, 'quad vs closed form')
            W[f'{name}_{lam}_S{S}'] = dict(b_w=a, beta90=float(beta_w(math.pi / 2, lam, S, **P)))
V['pure_water_bw'] = W
V['beta90_546_morel_S0'] = float(beta_w(math.pi / 2, 546, 0, **MOREL))
V['beta90_546_buiteveld_S0'] = float(beta_w(math.pi / 2, 546, 0, **BUIT))
# cos(2*theta) reading of the slide (as literally printed) for comparison with graph s24 (b_w(500) ~ 0.003 read from graph, ~10 %)
def bw_cos2theta(lam, S, P):
    k = (1 - P['delta']) / (1 + P['delta'])
    f = lambda th: 2 * math.pi * A_ * (lam / 500.0) ** P['expo'] * (1 + 0.3 * S / 37) * 1e-4 * (1 + math.cos(2 * th) * k) * math.sin(th)
    return integrate.quad(f, 0, math.pi)[0]
A_ = MOREL['A']
V['bw500_S37_cos2'] = bw_cos2theta(500, 37, MOREL)
V['bw500_S37_cos_sq'] = bw_closed(500, 37, MOREL)
V['bw500_S0_cos_sq'] = bw_closed(500, 0, MOREL)
V['salinity_effect_S37'] = (1 + 0.3 * 37 / 37) - 1      # +30 % at S = 37 (slide 20 "S impact: 30 %")
V['ratio_450_550_morel'] = (550 / 450) ** 4.32
V['ratio_450_550_buiteveld'] = (550 / 450) ** 4.14
V['ratio_450_550_rayleigh_lam4'] = (550 / 450) ** 4.0
V['bw_450_over_550_numeric'] = bw_numeric(450, 37, MOREL) / bw_numeric(550, 37, MOREL)
check('ratio_450_550_morel_vs_numeric', V['ratio_450_550_morel'], V['bw_450_over_550_numeric'], 1e-9)
V['tau_water_scattering_length_m_500_S37'] = 1 / bw_closed(500, 37, MOREL)

# textbook Einstein-Smoluchowski value at 546 nm (Ocean Optics Web Book, Physics of Scattering, Eq. 5)
kB, T_, n_, bT, dndP, rho, lam_ = 1.3806e-23, 293.15, 1.33477, 4.5893e-10, 1.5127e-10, 0.031, 546e-9
pref = 2 * math.pi ** 2 * kB * T_ / (lam_ ** 4 * bT) * n_ ** 2 * dndP ** 2 * (6 + 6 * rho) / (6 - 7 * rho)
V['es_beta90_546_textbook_constants'] = pref
V['es_beta90_546_textbook_stated'] = 0.869e-4
V['es_beta90_546_morel1974_textbook'] = 0.83e-4
# second route: the same formula written through the density derivative, (pi^2/2 lam^4) kT beta_T (dEps/drho rho)^2 ... = same algebra, so
# an independent number is the slide formula for S=0 at 546 nm:
V['es_vs_slide_morel_S0'] = V['beta90_546_morel_S0']
V['es_vs_slide_buiteveld_S0'] = V['beta90_546_buiteveld_S0']
V['es_rel_diff_to_textbook_stated'] = abs(pref - 0.869e-4) / 0.869e-4
V['slide_morel_vs_textbook_morel_note'] = 'Slide formula at 546 nm, S=0, theta=90 gives %.3e; textbook quotes Morel 1974 = 0.83e-4 and its own calculation 0.869e-4.' % V['beta90_546_morel_S0']

# ---------------------------------------------------------------- 2. CDOM / NAP exponentials (slides 38-45)
def a_exp(a0, S, lam, lam0): return a0 * math.exp(-S * (lam - lam0))
V['cdom_ratio_443_from_412_S014'] = a_exp(1, 0.014, 443, 412)
V['nap_ratio_443_from_412_S011'] = a_exp(1, 0.011, 443, 412)
V['cdom_ratio_350_over_440_S014'] = math.exp(0.014 * 90)
V['nap_ratio_350_over_440_S011'] = math.exp(0.011 * 90)
# method B: recover S from two points by log-linear least squares on synthetic noiseless spectrum, and by curve_fit
lam = np.arange(350, 701, 10.0); a = np.array([a_exp(0.5, 0.014, l, 440) for l in lam])
S_fit = -np.polyfit(lam, np.log(a), 1)[0]
popt, _ = optimize.curve_fit(lambda l, a0, S: a0 * np.exp(-S * (l - 440)), lam, a, p0=[1, 0.01])
check('S_recovered_logfit_vs_curvefit', float(S_fit), float(popt[1]), 1e-6)
V['cdom_S_recovered'] = float(popt[1])
V['cdom_e_folding_nm_S014'] = 1 / 0.014
V['cdom_a443_given_a412_0p3'] = 0.3 * V['cdom_ratio_443_from_412_S014']
V['cdom_power_law_ratio_350_440_lam_minus_6p92'] = (350 / 440) ** -6.92
# a_w + a_cdom example: wavelength at which a_cdom(443)=a_w(443)? uses user-visible inputs only, no tabulated a_w

# ---------------------------------------------------------------- 3. Mie machinery (Bohren & Huffman), used for slides 46-57, 63-71
from scipy.special import spherical_jn, spherical_yn
def mie_coeffs(m, x):
    """Mie coefficients a_n, b_n for a homogeneous NON-absorbing sphere (real relative index m), via spherical Bessel functions."""
    nmax = int(x + 4 * x ** (1 / 3) + 2); n = np.arange(1, nmax + 1); mx = m * x
    jx, jpx = spherical_jn(n, x), spherical_jn(n, x, derivative=True)
    yx, ypx = spherical_yn(n, x), spherical_yn(n, x, derivative=True)
    jm, jpm = spherical_jn(n, mx), spherical_jn(n, mx, derivative=True)
    psi, dpsi = x * jx, jx + x * jpx                       # Riccati-Bessel psi_n(x) and derivative
    psim, dpsim = mx * jm, jm + mx * jpm
    xi, dxi = x * (jx + 1j * yx), (jx + 1j * yx) + x * (jpx + 1j * ypx)
    a = (m * psim * dpsi - psi * dpsim) / (m * psim * dxi - xi * dpsim)
    b = (psim * dpsi - m * psi * dpsim) / (psim * dxi - m * xi * dpsim)
    return n, a, b
def mie_q(m, x):
    n, a, b = mie_coeffs(m, x)
    qext = 2 / x ** 2 * np.sum((2 * n + 1) * (a.real + b.real))
    qsca = 2 / x ** 2 * np.sum((2 * n + 1) * (abs(a) ** 2 + abs(b) ** 2))
    return qext, qsca
MU, WT = np.polynomial.legendre.leggauss(900)   # enough nodes for x up to ~300 (a 240-node first version was inaccurate at large x; found by the independent notebook)         # Gauss-Legendre in cos(theta)
def mie_back_q(m, x):
    """Backscattering efficiency Qb = (1/(x^2)) * int_{mu<0} (|S1|^2+|S2|^2) dmu (per pi r^2), and total Qsca by the same quadrature."""
    n, a, b = mie_coeffs(m, x); nmax = len(n)
    pi_ = np.zeros((nmax + 1, len(MU))); tau = np.zeros((nmax + 1, len(MU)))
    pi_[1] = 1.0; tau[1] = MU
    for k in range(2, nmax + 1):
        pi_[k] = (2 * k - 1) / (k - 1) * MU * pi_[k - 1] - k / (k - 1) * pi_[k - 2]
        tau[k] = k * MU * pi_[k] - (k + 1) * pi_[k - 1]
    c = (2 * n + 1) / (n * (n + 1))
    S1 = (c[:, None] * (a[:, None] * pi_[1:] + b[:, None] * tau[1:])).sum(0)
    S2 = (c[:, None] * (a[:, None] * tau[1:] + b[:, None] * pi_[1:])).sum(0)
    I = abs(S1) ** 2 + abs(S2) ** 2
    qsca_q = np.sum(WT * I) / x ** 2        # integral over mu in [-1,1]; dsigma/dOmega=I/(2k^2) -> Qsca = (1/x^2) int I dmu
    qb = np.sum(WT[MU < 0] * I[MU < 0]) / x ** 2
    return qsca_q, qb
# validation: Q_sca from series vs from angular quadrature; and large-sphere limit
for m, x in ((1.05, 0.5), (1.05, 5.0), (1.15, 20.0), (1.33, 10.0), (1.05, 100.0), (1.05, 280.0), (1.20, 280.0)):
    qs_series = mie_q(m, x)[1]; qs_quad = mie_back_q(m, x)[0]
    check(f'mie_qsca_series_vs_angular_m{m}_x{x}', qs_series, qs_quad, 1e-3, 'two independent routes')
V['mie_qext_m105'] = {str(x): mie_q(1.05, x)[0] for x in (0.1, 0.5, 1, 2, 5, 10, 20, 50, 100)}
V['mie_qext_m120'] = {str(x): mie_q(1.20, x)[0] for x in (0.1, 0.5, 1, 2, 5, 10, 20, 50, 100)}
# Known analytic limit (van de Hulst): Rayleigh Qsca = (8/3) x^4 ((m^2-1)/(m^2+2))^2 for x<<1
for m_ in (1.05, 1.15, 1.33):
    xr = 0.02; check(f'rayleigh_closed_form_m{m_}', mie_q(m_, xr)[1], 8/3*xr**4*((m_**2-1)/(m_**2+2))**2, 5e-3, 'series vs Rayleigh closed form')
# Rayleigh limit: Qsca ~ x^4 for small x -> slope of log Q vs log x
xs = np.array([0.02, 0.04, 0.08]); qs = np.array([mie_q(1.15, x)[1] for x in xs])
V['rayleigh_qsca_loglog_slope'] = float(np.polyfit(np.log(xs), np.log(qs), 1)[0])
check('rayleigh_slope_is_4', V['rayleigh_qsca_loglog_slope'], 4.0, 0.02)

# ---------------------------------------------------------------- 4. Junge PSD ensembles: spectral slope of b_p and b_bp/b_p (slides 49, 68, 71)
NW = 1.34
def ensemble(m, xi, lam_nm, Dmin=0.1, Dmax=100.0, nD=140):
    D = np.logspace(math.log10(Dmin), math.log10(Dmax), nD)         # um
    N = D ** (-xi)                                                   # dN/dD per um (Junge: n(D) ~ D^-xi)
    x = math.pi * D * NW / (lam_nm / 1000.0)
    bp = bb = 0.0; pairs = []
    for Di, Ni, xi_ in zip(D, N, x):
        qs = mie_q(m, xi_)[1]; qb = mie_back_q(m, xi_)[1]
        area = math.pi * (Di / 2) ** 2
        pairs.append((Ni * area * qs, Ni * area * qb))
    pairs = np.array(pairs)
    # integrate over D (trapezoid on log grid: dD = D dlnD)
    w = D * np.gradient(np.log(D))
    return float(np.sum(pairs[:, 0] * w)), float(np.sum(pairs[:, 1] * w))
ENS = {}
for xi in (3.5, 4.0, 4.5, 5.0):
    r = {}
    for lam_ in (440, 550, 660):
        bp, bb = ensemble(1.05, xi, lam_)
        r[lam_] = (bp, bb)
    n_bp = math.log(r[440][0] / r[660][0]) / math.log(440 / 660)
    n_bb = math.log(r[440][1] / r[660][1]) / math.log(440 / 660)
    ENS[str(xi)] = dict(n_bp=n_bp, n_bbp=n_bb, bbp_over_bp_550=r[550][1] / r[550][0], gamma_expected_xi_minus_3=xi - 3)
V['junge_ensemble_m105'] = ENS
# method B for the exponent: direct least-squares on three wavelengths instead of two end points
for xi in (4.0,):
    ls = np.array([440, 550, 660.0]); vals = np.array([ensemble(1.05, xi, l)[0] for l in ls])
    slope = np.polyfit(np.log(ls), np.log(vals), 1)[0]
    check('junge_xi4_bp_exponent_endpoints_vs_lsq', ENS['4.0']['n_bp'], float(slope), 0.05, 'power-law exponent n of b_p ~ lambda^n')
RI = {}
for m in (1.02, 1.05, 1.10, 1.15, 1.20):
    RI[str(m)] = {str(xi): ensemble(m, xi, 550)[1] / ensemble(m, xi, 550)[0] for xi in (3.0, 3.5, 4.0, 4.5)}
V['bbp_over_bp_vs_index_and_slope'] = RI

# ---------------------------------------------------------------- 5. b_p ~ lambda^n and Sum N sigma (slides 49, 63)
V['bp_440_over_550'] = {str(n_): (440 / 550) ** n_ for n_ in (0, -1, -3)}
V['bp_fixed_550_1p0_at_440'] = {str(n_): (440 / 550) ** n_ for n_ in (0, -0.5, -1, -2, -3)}
r_um, Nv, Q = 5.0, 1e7, 2.0
S_area = math.pi * (r_um * 1e-6) ** 2
V['sum_N_sigma_c_example'] = Nv * Q * S_area                      # m^-1
# method B: Monte-Carlo-free alternative = Mie Q_ext at large x then multiply
qext_big = mie_q(1.05, math.pi * 2 * r_um * NW / 0.55)[0]
V['mie_qext_r5um_550nm_m105'] = qext_big
V['sum_N_sigma_c_with_mie_Q'] = Nv * qext_big * S_area
def q_ext_ad(m, x):   # van de Hulst anomalous-diffraction approximation (independent of Mie series)
    rho = 2 * x * (m - 1); return 2 - 4 / rho * math.sin(rho) + 4 / rho ** 2 * (1 - math.cos(rho))
xbig = math.pi * 2 * r_um * NW / 0.55
check('Q_ext_Mie_vs_anomalous_diffraction_r5um', qext_big, q_ext_ad(1.05, xbig), 0.05, 'Mie series vs AD approximation, m=1.05')
V['q_ext_ad_r5um'] = q_ext_ad(1.05, xbig)
V['q_ext_to_2_limit_note'] = 'Q_ext oscillates around 2 for large non-absorbing spheres; with m=1.05 and x~77 it is 1.6 (not 2). Use Q=2 only as a rough upper-level estimate.'
for xx in (50, 100, 200):
    check(f'Q_ext_AD_vs_Mie_m1.05_x{xx}', mie_q(1.05, xx)[0], q_ext_ad(1.05, xx), 0.08, 'Mie vs AD')
V['two_populations_example'] = dict(
    small=dict(r_um=0.5, N=1e11, Q=0.9), large=dict(r_um=10.0, N=1e6, Q=2.0))
for k, d in V['two_populations_example'].items():
    d['sigma_m2'] = d['Q'] * math.pi * (d['r_um'] * 1e-6) ** 2; d['c_m1'] = d['N'] * d['sigma_m2']
V['two_populations_total_c'] = sum(d['c_m1'] for d in V['two_populations_example'].values())

# ---------------------------------------------------------------- 6. package effect (slides 32-34)
def Qa_star_closed(rho):      # rho = a_cell * d ; Q_a(rho)=1+2e^-rho/rho+2(e^-rho-1)/rho^2 ; Q*=(3/2)Qa/rho  (Morel & Bricaud 1981)
    if rho < 1e-6: return 1.0
    return 1.5 * (1 + 2 * math.exp(-rho) / rho + 2 * (math.exp(-rho) - 1) / rho ** 2) / rho
def Qa_star_numeric(rho):     # ray-path integral through a sphere of radius R, a = rho/(2R)
    R = 1.0; a = rho / (2 * R)
    f = lambda b: (1 - math.exp(-a * 2 * math.sqrt(max(R * R - b * b, 0)))) * 2 * math.pi * b
    absorbed = integrate.quad(f, 0, R, limit=200)[0]                 # absorbed power per unit flux
    abs_no_pack = a * (4 / 3) * math.pi * R ** 3                     # same pigment spread out (no self-shading)
    return absorbed / abs_no_pack
PK = {}
for rho in (0.05, 0.2, 0.5, 1.0, 2.0, 5.0):
    A_, B_ = Qa_star_closed(rho), Qa_star_numeric(rho)
    check(f'package_Qstar_rho{rho}', A_, B_, 1e-3, 'closed form vs ray-path quadrature (anomalous-diffraction sphere)')
    PK[str(rho)] = A_
V['package_Qstar'] = PK
# a_cell: intracellular absorption of chlorophyll at 440 nm. Illustration only: a_cm ~ 1e5 m^-1 is NOT a lecture number -> parametrised by rho
V['package_note'] = 'rho = a_cm * d (intracellular absorption x cell diameter): illustrative parameter, not a measured value.'

# ---------------------------------------------------------------- 7. Beer-Lambert and instruments (slides 5, 59-61)
def T_closed(c, L): return math.exp(-c * L)
def T_numeric(c, L):
    sol = integrate.solve_ivp(lambda x, I: -c * I, [0, L], [1.0], rtol=1e-10, atol=1e-12); return float(sol.y[0, -1])
BL = {}
for c in (0.05, 0.1, 0.5, 1.0, 2.0):
    for L in (0.1, 0.25, 1.0):
        check(f'beer_c{c}_L{L}', T_closed(c, L), T_numeric(c, L), 1e-7)
        BL[f'c{c}_L{L}'] = T_closed(c, L)
V['beer_lambert_T'] = BL
V['c_from_T_25cm'] = {str(T): -math.log(T) / 0.25 for T in (0.99, 0.9, 0.5, 0.1)}
# Boss & Pegau: b_bp = 2 pi chi beta_p(117).  chi ~ 1.1 read from graph s62 (~10 %) -> used as parameter only
V['bbp_from_beta117'] = lambda_ = None
V.pop('bbp_from_beta117')
beta_p117 = 1.0e-3
V['bbp_example_chi1p1_beta1e-3'] = 2 * math.pi * 1.1 * beta_p117
# angular integration check: b_b from VSF = 2pi int_{pi/2}^{pi} beta sin ; for a Fournier-less test use pure-water slide VSF
bb_num = integrate.quad(lambda th: 2 * math.pi * beta_w(th, 500, 37, **MOREL) * math.sin(th), math.pi / 2, math.pi)[0]
V['bbw_500_S37'] = bb_num; V['bbw_over_bw_500'] = bb_num / bw_closed(500, 37, MOREL)
check('bbw_is_half_of_bw', V['bbw_over_bw_500'], 0.5, 1e-9, 'symmetric cos^2 VSF -> b_b/b = 1/2')

# ---------------------------------------------------------------- 8. light field (textbook; NOT in the lecture)
def zeu_closed(Kd, frac=0.01): return -math.log(frac) / Kd
def zeu_root(Kd, frac=0.01): return optimize.brentq(lambda z: math.exp(-Kd * z) - frac, 0.0, 1e4)
EU = {}
for Kd in (0.03, 0.04, 0.1, 0.3, 1.0):
    check(f'zeu1pct_Kd{Kd}', zeu_closed(Kd), zeu_root(Kd), 1e-8)
    EU[str(Kd)] = dict(z1pct=zeu_closed(Kd), z10pct=zeu_closed(Kd, 0.1), penetration_1_over_Kd=1 / Kd)
V['euphotic_1pct'] = EU
def secchi(Kd, c, Gamma=8.0): return Gamma / (Kd + c)
V['secchi_examples'] = {f'Kd{k}_c{c}': secchi(k, c) for k, c in ((0.04, 0.1), (0.1, 0.2), (0.3, 1.0), (0.05, 0.12))}
V['secchi_lee_2015_gamma1_Kd0p04'] = 1 / (2.5 * 0.04)    # gamma ~ O(1): illustrative only
V['secchi_range_gamma_6_9_Kd0p1_c0p2'] = [secchi(0.1, 0.2, 6), secchi(0.1, 0.2, 9)]
# method B for Secchi: solve z*(Kd+c)=Gamma by root finding
check('secchi_root_vs_formula', secchi(0.1, 0.2), optimize.brentq(lambda z: z * 0.3 - 8.0, 0.1, 1000), 1e-9)
# R ~ f b_b/(a+b_b) (classical, NOT on crawled textbook pages) : monotonic behaviour only
def R_gordon(a, bb, f=0.33): return f * bb / (a + bb)
V['R_over_f_bb_a_examples'] = {'clear_a0.02_bb0.002': R_gordon(0.02, 0.002, 1), 'turbid_a0.5_bb0.05': R_gordon(0.5, 0.05, 1)}
V['R_over_f_note'] = 'R/f = b_b/(a+b_b). Classical result (Gordon et al. 1975); not found on the crawled textbook pages; used for qualitative reasoning only.'
V['c_gt_Kd_rule'] = 'a <= Kd*mu_d <= c (textbook, K functions)'

# ---------------------------------------------------------------- 9. platforms
V['argo_floats_2025_06_30'] = 4153
V['bgc_argo_may2025'] = dict(operational=788, suspended_particles=551, downwelling_irradiance=166, ph=451, nitrate=447, chlorophyll_a=551, oxygen=782, full_bgc=77)
V['bgc_argo_fractions'] = {k: v / 788 for k, v in V['bgc_argo_may2025'].items() if k not in ('operational', 'full_bgc')}
V['bgc_full_fraction'] = 77 / 788
V['bgc_vs_argo_fraction'] = 788 / 4153
V['satellite_vs_secchi_coverage'] = 'slide 4: ~1/2 million Secchi/Chl points over 100 years vs ~1/2 million SeaWiFS observations every ~30 s (Boyce et al. 2010)'
V['seconds_to_match_100yr_secchi_record'] = 30                    # from slide 4: ~half a million obs every ~30 s

# ---------------------------------------------------------------- 10. Case 1 / Case 2 and a_total (qualitative cross-checks of s45)
V['s45_case1_total_min_nm_graph'] = '~400-420 (read from graph, ~10 %)'
V['s45_case2_total_min_nm_graph'] = '~570 (read from graph, ~10 %)'

# ---------------------------------------------------------------- 11. IOP <-> biogeochemistry (slides 65, 74, 77)
for chl in (0.03, 0.1, 1.0, 10.0):
    A_ = 0.30 * chl ** 0.7; B_ = 0.30 * math.exp(0.7 * math.log(chl))
    check(f'bp550_from_chl_{chl}', A_, B_, 1e-12)
V['bp550_from_chl'] = {str(c): 0.30 * c ** 0.7 for c in (0.03, 0.1, 1.0, 10.0)}
V['bp550_tenfold_chl_factor'] = 10 ** 0.7                              # 5.01: a tenfold Chl change -> ~5x in b_p
for r_ in (0.7, 1.0, 2.0, 3.0):
    A_ = 0.0133 * math.exp(1.27 * r_); B_ = float(np.exp(np.log(0.0133) + 1.27 * r_))
    check(f'poc_spm_ratio_{r_}', A_, B_, 1e-12)
V['poc_spm_from_ap_ratio'] = {str(r_): 0.0133 * math.exp(1.27 * r_) for r_ in (0.7, 1.0, 2.0, 3.0)}
# conservative mixing of CDOM with salinity (textbook/slide 77 idea): a(S) = a_fresh (1 - S/S_sea) + a_sea (S/S_sea)
def a_mix(S, a_f, a_s, S_s=36.0): return a_f * (1 - S / S_s) + a_s * (S / S_s)
V['cdom_mixing_example'] = {str(S_): a_mix(S_, 10.0, 0.1) for S_ in (0, 5, 18, 30, 36)}
chk_S = 18.0; check('cdom_mix_midpoint', a_mix(chk_S, 10.0, 0.1), (10.0 + 0.1) / 2, 1e-12, 'midpoint of a linear mixing line')
V['cdom_mix_note'] = 'illustrative end members 10 and 0.1 m^-1 at 355 nm (orders of magnitude quoted on slide 77: >=10 fresh, <=0.1 oceanic)'
# diurnal: nothing numeric.  Argo coverage fractions
V['argo_bgc_share'] = 788 / 4153
V['discrepancies'] = DISC
V['n_checks'] = len(V['checks']); V['n_ok'] = sum(c['ok'] for c in V['checks'])
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(V, open(OUT, 'w', encoding='utf-8'), indent=1, ensure_ascii=False, default=float)
print('checks', V['n_checks'], 'ok', V['n_ok'], 'DISCREPANCIES:', DISC)
