# -*- coding: utf-8 -*-
"""Own figures (dpi 100, size in px / 100, text >= 14.4 pt = 20 px). All curves are computed here, never traced from the lecture."""
import os, json, math
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__)); _S = os.path.join(HERE, '..', 'site'); SITE = _S if os.path.isdir(_S) else os.path.join(HERE, '..')
OUT = os.path.join(SITE, 'assets', 'images', 'fig')
V = json.load(open(os.path.join(SITE, 'data', 'verified.json')))
plt.rcParams.update({'font.size': 15, 'axes.labelsize': 15, 'xtick.labelsize': 14.5, 'ytick.labelsize': 14.5, 'legend.fontsize': 14.5, 'axes.grid': True, 'grid.alpha': .3,
                     'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 100, 'savefig.dpi': 100})
BLUE, RED, GREY, GREEN, ORG = '#273896', '#ED1C24', '#666666', '#2a9d4b', '#e08a00'
def save(fig, name): fig.savefig(os.path.join(OUT, name + '.png'), facecolor='white'); plt.close(fig)
def bw(lam, theta, S=37, A=1.38, e=-4.32, d=0.09):
    return A * (lam / 500) ** e * (1 + 0.3 * S / 37) * 1e-4 * (1 + np.cos(theta) ** 2 * (1 - d) / (1 + d))

# 1. VSF of pure sea water at 350/450/550 (Morel form, S = 37)
th = np.linspace(0, math.pi, 361); fig, ax = plt.subplots(figsize=(7.2, 5.2), constrained_layout=True)
for lam, c in ((350, BLUE), (450, GREEN), (550, ORG)): ax.semilogy(np.degrees(th), bw(lam, th), color=c, lw=2.6, label=f'{lam} nm')
ax.set_xlabel('scattering angle ψ (°)'); ax.set_ylabel('β_w (m⁻¹ sr⁻¹)'); ax.set_xticks([0, 45, 90, 135, 180]); ax.set_ylim(5e-5, 6e-3); ax.legend(loc='upper center', ncol=3)
save(fig, 'vsf_water')

# 2. b_w(lambda): Morel (4.32) vs Buiteveld (4.14), S = 37 and S = 0
lam = np.arange(400, 701, 5.0)
def bwc(l, S, A, e, d): k = (1 - d) / (1 + d); return 2 * math.pi * A * (l / 500) ** e * (1 + 0.3 * S / 37) * 1e-4 * (2 + 2 * k / 3)
fig, ax = plt.subplots(figsize=(11.6, 4.8), constrained_layout=True)
ax.semilogy(lam, bwc(lam, 37, 1.38, -4.32, .09), color=BLUE, lw=2.8, label='Morel 1974 form (λ^−4.32), S = 37')
ax.semilogy(lam, bwc(lam, 37, 1.29, -4.14, .051), color=RED, lw=2.8, ls='--', label='Buiteveld 1994 form (λ^−4.14), S = 37')
ax.semilogy(lam, bwc(lam, 0, 1.38, -4.32, .09), color=GREY, lw=2.2, ls=':', label='Morel form, S = 0')
ax.set_xlabel('wavelength (nm)'); ax.set_ylabel('b_w (m⁻¹)'); ax.legend(loc='upper right'); save(fig, 'bw_spectrum')

# 3. exponential absorption models normalised at 440 nm
lam = np.arange(350, 701, 2.0); fig, ax = plt.subplots(figsize=(11.6, 4.8), constrained_layout=True)
ax.semilogy(lam, np.exp(-0.014 * (lam - 440)), color=BLUE, lw=2.8, label='CDOM: exp(−0.014 (λ−440))')
ax.semilogy(lam, np.exp(-0.011 * (lam - 440)), color=ORG, lw=2.8, label='NAP: exp(−0.011 (λ−440))')
ax.semilogy(lam, (lam / 440) ** -6.92, color=RED, lw=2.4, ls='--', label='CDOM power law: λ^−6.92')
ax.set_ylim(1e-3, 30); ax.set_xlabel('wavelength (nm)'); ax.set_ylabel('a(λ) / a(440)'); ax.legend(loc='upper right'); save(fig, 'exp_absorption')

# 4. b_p(lambda)/b_p(550) for n = 0, -1, -3
lam = np.arange(400, 701, 2.0); fig, ax = plt.subplots(figsize=(7.2, 5.2), constrained_layout=True)
for n, c in ((0, GREY), (-1, BLUE), (-3, RED)): ax.plot(lam, (lam / 550) ** n, color=c, lw=2.8, label=f'n = {n}')
ax.set_xlabel('wavelength (nm)'); ax.set_ylabel('b_p(λ) / b_p(550)'); ax.legend(); save(fig, 'bp_power')

# 5. package effect Q*_a vs rho
rho = np.logspace(-2, 1.3, 100)
def qa(r): return 1.5 * (1 + 2 * np.exp(-r) / r + 2 * (np.exp(-r) - 1) / r ** 2) / r
fig, ax = plt.subplots(figsize=(7.2, 5.2), constrained_layout=True); ax.semilogx(rho, qa(rho), color=BLUE, lw=2.8)
ax.set_xlabel('ρ = a_cell · d (absorption inside the cell × diameter)'); ax.set_ylabel('Q*_a (package factor)'); ax.set_ylim(0, 1.05)
for r in (0.2, 1, 5): ax.plot([r], [qa(r)], 'o', color=RED, ms=9); ax.annotate(f'{qa(r):.2f}', (r, qa(r)), textcoords='offset points', xytext=(8, 8))
save(fig, 'package_effect')

# 6. Mie ensembles: exponent n of b_p and b_bp vs Junge slope xi; b_bp/b_p vs refractive index
E = V['junge_ensemble_m105']; xi = np.array([float(k) for k in E]); nbp = [E[k]['n_bp'] for k in E]; nbb = [E[k]['n_bbp'] for k in E]
fig, ax = plt.subplots(figsize=(7.2, 5.2), constrained_layout=True)
ax.plot(xi, nbp, 'o-', color=BLUE, lw=2.6, ms=9, label='b_p exponent (Mie, m = 1.05)'); ax.plot(xi, nbb, 's-', color=RED, lw=2.6, ms=9, label='b_bp exponent')
ax.plot(xi, -(xi - 3), '--', color=GREY, lw=2.2, label='−(ξ − 3)'); ax.set_xlabel('Junge slope ξ of N(D) ∝ D^−ξ'); ax.set_ylabel('exponent n in λ^n'); ax.legend(loc='upper right', fontsize=13); save(fig, 'junge_exponent')
R = V['bbp_over_bp_vs_index_and_slope']; fig, ax = plt.subplots(figsize=(7.2, 5.2), constrained_layout=True)
ms = [float(k) for k in R]
for x_, c in zip(('3.0', '3.5', '4.0', '4.5'), (BLUE, GREEN, ORG, RED)): ax.plot(ms, [R[k][x_] for k in R], 'o-', color=c, lw=2.4, ms=8, label=f'ξ = {x_}')
ax.set_xlabel('relative refractive index m'); ax.set_ylabel('b_bp / b_p at 550 nm'); ax.legend(fontsize=13); save(fig, 'bbp_index')

# 7. euphotic depth and Secchi depth vs Kd
Kd = np.logspace(-2, 0, 100); fig, ax = plt.subplots(figsize=(7.2, 5.2), constrained_layout=True)
ax.loglog(Kd, math.log(100) / Kd, color=BLUE, lw=2.8, label='1 % light depth = 4.6 / K_d')
ax.loglog(Kd, 8 / (Kd + 2 * Kd), color=RED, lw=2.8, ls='--', label='Secchi = 8/(K_d + c), c = 2 K_d (illustrative)')
ax.set_xlabel('K_d (m⁻¹)'); ax.set_ylabel('depth (m)'); ax.legend(fontsize=13); save(fig, 'euphotic_secchi')

# 8. Beer-Lambert: transmission along 0.25 m path
c = np.logspace(-2, 0.6, 100); fig, ax = plt.subplots(figsize=(7.2, 5.2), constrained_layout=True)
for L, col in ((0.1, GREEN), (0.25, BLUE), (1.0, RED)): ax.semilogx(c, np.exp(-c * L), color=col, lw=2.6, label=f'L = {L} m')
ax.set_xlabel('c (m⁻¹)'); ax.set_ylabel('T = exp(−c L)'); ax.legend(); save(fig, 'beer_lambert')

# 9. Coverage: BGC-Argo sensors (counts from slide 115)
B = V['bgc_argo_may2025']; names = ['oxygen', 'suspended_particles', 'chlorophyll_a', 'ph', 'nitrate', 'downwelling_irradiance', 'full_bgc']
lab = ['Oxygen', 'Susp. particles (b_bp)', 'Chlorophyll a', 'pH', 'Nitrate', 'Downwelling irradiance', 'Full BGC (all)']
fig, ax = plt.subplots(figsize=(11.6, 4.6), constrained_layout=True); ax.barh(lab[::-1], [B[n] for n in names][::-1], color=[RED if n == 'full_bgc' else BLUE for n in names][::-1])
for i, v in enumerate([B[n] for n in names][::-1]): ax.text(v + 8, i, str(v), va='center', fontsize=15)
ax.set_xlabel('operational BGC-Argo floats carrying the sensor (May 2025, slide 115)'); ax.set_xlim(0, 900); ax.grid(axis='y', alpha=0); save(fig, 'bgc_sensors')
print('figs ok')
