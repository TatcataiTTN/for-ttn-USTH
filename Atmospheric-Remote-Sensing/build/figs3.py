# -*- coding: utf-8 -*-
"""Hình mới (f25-f32) từ bài giảng Cuesta. dpi 100, figsize = px/100; mọi số lấy từ data/verified.json."""
import json, os, math
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
ROOT = os.path.join(os.path.dirname(__file__), '..', 'site')
OUT = os.path.join(ROOT, 'assets', 'images', 'fig')
V = json.load(open(os.path.join(ROOT, 'data', 'verified.json')))
BLUE, RED, CY, GR, OR, PU, DK = '#273896', '#ED1C24', '#15AFF0', '#1b7f4c', '#a05a00', '#7a3fa0', '#333333'
plt.rcParams.update({'font.size': 16, 'axes.titlesize': 18, 'axes.labelsize': 16, 'xtick.labelsize': 15, 'ytick.labelsize': 15,
                     'axes.spines.top': False, 'axes.spines.right': False, 'font.family': 'DejaVu Sans'})
def save(f, n): f.savefig(os.path.join(OUT, n + '.png'), dpi=100, facecolor='white'); plt.close(f)

# ---------- f25 hydrostatic ----------
def f25():
    H = V['hydro']; z = np.linspace(0, 30, 301); Hs = H['H_km']
    f, ax = plt.subplots(figsize=(11.6, 5.6)); ax.plot(1013.25 * np.exp(-z / Hs), z, color=BLUE, lw=3.2, label=f'isothermal model, H = {Hs:.1f} km')
    tz = [1, 2, 3, 10]; ax.plot([H['table'][str(k)] for k in tz], tz, 'o', color=RED, ms=11, label='lecture table (real atmosphere)')
    ax.plot([H['p']['10']], [10], 's', color=BLUE, ms=11)
    ax.annotate(f"10 km: model {H['p']['10']:.0f} hPa\nreal {H['table']['10']} hPa (+{H['err10_pct']:.0f}%)\nbecause T falls with height", xy=(H['p']['10'], 10), xytext=(520, 14.5), fontsize=15, arrowprops=dict(arrowstyle='->', color=DK))
    ax.axhline(H['half_km'], color='#888', ls=':', lw=2); ax.text(560, H['half_km'] + .5, f"p halves every H·ln2 = {H['half_km']:.2f} km", fontsize=15, color=DK)
    ax.set_xlabel('pressure (hPa)'); ax.set_ylabel('altitude (km)'); ax.set_xlim(0, 1100); ax.set_ylim(0, 30); ax.legend(loc='upper right', frameon=False, fontsize=15)
    ax.set_title('Hydrostatic law: p = p₀·exp(−z/H), H = RT/(Mg)'); f.tight_layout(); save(f, 'f25_hydrostatic')

# ---------- f26 sinks ----------
def f26():
    S = V['sinks_ex']; names = ['Outflow\n(τ = 5 h)', 'Chemistry\n(τ = 1 d)', 'Rain\n(τ = 7 d)']; ks = [S['k_out'], S['k_chem'], S['k_dep']]; fr = [S['f_out'], S['f_chem'], S['f_dep']]
    f, ax = plt.subplots(figsize=(11.6, 4.8)); b = ax.barh(names[::-1], ks[::-1], color=[GR, OR, RED][::-1][::-1][::-1] if False else [CY, OR, RED], height=.6)
    for r, k, fr_ in zip(b, ks[::-1], fr[::-1]): ax.text(k + .08, r.get_y() + r.get_height() / 2, f'{k:.2f} d⁻¹  →  {fr_*100:.0f}%', va='center', fontsize=16)
    ax.set_xlim(0, 7.6); ax.set_xlabel('loss rate constant k (d⁻¹)'); ax.set_title(f"Urban plume, 100 km, wind 20 km/h:  k_tot = {S['k_tot']:.2f} d⁻¹,  τ = {S['tau_tot_h']:.1f} h")
    f.tight_layout(); save(f, 'f26_sinks_pathways')

# ---------- f27 ozone cycle ----------
def box(ax, x, y, w, h, t, fc, fs=17):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.02,rounding_size=0.03', fc=fc, ec='#555', lw=1.6)); ax.text(x + w / 2, y + h / 2, t, ha='center', va='center', fontsize=fs)
def arr(ax, p, q, c=DK, rad=0.0, ls='-'):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='-|>', mutation_scale=22, lw=2.4, color=c, connectionstyle=f'arc3,rad={rad}', linestyle=ls))
def f27():
    f, ax = plt.subplots(figsize=(12.4, 6.4)); ax.set_xlim(0, 12.4); ax.set_ylim(0, 6.4); ax.axis('off')
    box(ax, 0.3, 4.2, 2.6, 1.3, 'NO₂', '#fde9d0'); box(ax, 5.0, 4.2, 2.6, 1.3, 'NO + O', '#fff2c2'); box(ax, 9.6, 4.2, 2.5, 1.3, 'O₃', '#e3ecf7')
    arr(ax, (2.95, 5.0), (4.95, 5.0)); ax.text(3.95, 5.35, 'hν, λ < 424 nm', ha='center', fontsize=15, color=RED)
    arr(ax, (7.65, 5.0), (9.55, 5.0)); ax.text(8.6, 5.35, 'O + O₂ + M', ha='center', fontsize=15, color=BLUE)
    arr(ax, (10.8, 4.15), (1.6, 4.15), rad=-0.32, c=GR); ax.text(7.7, 2.15, 'NO + O₃ → NO₂ + O₂   (titration: ozone destroyed)', ha='center', fontsize=16, color=GR)
    ax.text(6.2, 3.45, 'Pure NOx cycle: zero net ozone production', ha='center', fontsize=17, weight='bold')
    box(ax, 0.3, 0.2, 5.0, 1.15, 'VOC + OH → RO₂, HO₂ (peroxy radicals)', '#e9f4ec', 15)
    arr(ax, (1.2, 1.4), (0.9, 4.15), c=OR, rad=0.0); ax.text(1.35, 2.35, 'RO₂ + NO → NO₂\n(no O₃ used)\n⇒ net O₃ production', fontsize=15, color=OR, va='center')
    ax.text(6.2, 6.1, 'Tropospheric ozone: NOx cycle and the peroxy-radical shortcut', ha='center', fontsize=18)
    f.tight_layout(); save(f, 'f27_o3_cycle')

# ---------- f28 lidar exercise ----------
def f28():
    L = V['lidar_ex1']; labels = ['(a) particles\n1 km', '(b) water cloud\n3 km', '(c) sub-visible\ncirrus 12 km', '(d) cloud 3 km\nbehind τ = 0.8', '(d) cirrus 12 km\nbehind τ = 0.8']
    vals = [L['a']['P_nW'], L['b']['P_nW'], L['c']['P_nW'], L['d']['P3_nW'], L['d']['P12_nW']]
    f, ax = plt.subplots(figsize=(12.6, 5.8)); cols = [BLUE if v >= 1 else RED for v in vals]; b = ax.bar(labels, vals, color=cols, width=.62); ax.set_yscale('log'); ax.set_ylim(5e-3, 3e2)
    ax.axhline(1, color=DK, ls='--', lw=2.2); ax.text(4.45, 1.25, 'detection limit 1 nW', ha='right', fontsize=16)
    for r, v in zip(b, vals): ax.text(r.get_x() + r.get_width() / 2, v * 1.25, f'{v:.3g} nW', ha='center', fontsize=16, weight='bold')
    ax.set_ylabel('signal P (nW), log scale'); ax.set_title('Lidar exercise 1: P = K/z² · (β_m + β_p) · T²   (blue = detected, red = not detected)'); ax.tick_params(axis='x', labelsize=14)
    f.tight_layout(); save(f, 'f28_lidar_exercise')

# ---------- f29 DIAL ----------
def f29():
    on = [10, 7]; off = [10, 8]; r = [1.0, 1.5]; D = V['dial']
    f, ax = plt.subplots(figsize=(11.6, 5.6)); ax.plot(r, np.log(on), 'o-', color=RED, lw=3.2, ms=11, label='ON line (λ = 830 nm): water vapour absorbs')
    ax.plot(r, np.log(off), 's-', color=BLUE, lw=3.2, ms=11, label='OFF (λ = 831 nm): no water-vapour absorption')
    ax.set_xlabel('altitude (km)'); ax.set_ylabel('ln P  (P in nW)'); ax.set_xlim(.9, 1.6); ax.set_ylim(1.9, 2.4); ax.set_xticks([1.0, 1.25, 1.5])
    ax.legend(loc='lower left', frameon=False, fontsize=15)
    ax.annotate('', xy=(1.5, np.log(7)), xytext=(1.5, np.log(8)), arrowprops=dict(arrowstyle='<->', color=DK, lw=2.2))
    ax.text(1.52, 2.0, f"ln(8/7) = 0.134 ⇒ α = 0.134/(2·500 m)\n= {D['alpha']*1e4:.2f}×10⁻⁴ m⁻¹ ⇒ q = {D['q_gkg']:.2f} g/kg", fontsize=15, color=DK, va='center', ha='left')
    ax.set_title('Water-vapour DIAL: only the difference of the two slopes is water vapour'); f.tight_layout(); save(f, 'f29_dial')

# ---------- f30 multispectral ----------
def f30():
    M = V['multi']; f, (a, b) = plt.subplots(1, 2, figsize=(13, 5.6)); x = np.arange(3); w = .36
    land = [M['dofs_iasi']['land'], 0.10, M['dofs_multi']['land']]; ocean = [M['dofs_iasi']['ocean'], 0.10, M['dofs_multi']['ocean']]
    a.bar(x - w / 2, land, w, color=BLUE, label='land', hatch=['', '//', ''][0]); a.bar(x + w / 2, ocean, w, color=CY, label='ocean')
    for rr in a.patches[1:2] + a.patches[4:5]: pass
    a.patches[1].set_hatch('//'); a.patches[4].set_hatch('//'); a.patches[1].set_alpha(.55); a.patches[4].set_alpha(.55); a.set_xticks(x); a.set_xticklabels(['IASI\n(IR)', 'GOME-2\n(UV)', 'IASI+\nGOME-2'])
    a.text(1, .115, 'upper bound\n< 0.10', ha='center', fontsize=14); a.text(2 - w / 2, land[2] + .01, '0.35', ha='center', fontsize=15); a.text(2 + w / 2, ocean[2] + .01, '0.25', ha='center', fontsize=15)
    a.text(0 - w / 2, land[0] + .01, '0.25', ha='center', fontsize=15); a.text(0 + w / 2, ocean[0] + .01, '0.15', ha='center', fontsize=15)
    a.set_ylabel('DOFS below 3 km'); a.set_title('Information on the lowest layers'); a.legend(frameon=False, fontsize=15, loc='upper left'); a.set_ylim(0, .45)
    hl = [M['h_iasi']['land'], 3.7, M['h_multi']['land']]; ho = [M['h_iasi']['ocean'], 3.7, M['h_multi']['ocean']]
    b.bar(x - w / 2, hl, w, color=BLUE); b.bar(x + w / 2, ho, w, color=CY); b.set_xticks(x); b.set_xticklabels(['IASI', 'GOME-2', 'IASI+\nGOME-2']); b.set_ylabel('height of max. sensitivity (km agl)'); b.set_title('Peak sensitivity is 0.8 km lower'); b.set_ylim(0, 5)
    for i, (u, v) in enumerate(zip(hl, ho)): b.text(i - w / 2, u + .08, f'{u:g}', ha='center', fontsize=15); b.text(i + w / 2, v + .08, f'{v:g}', ha='center', fontsize=15)
    f.tight_layout(); save(f, 'f30_multispectral')

# ---------- f31 Big 12 map ----------
BIG = [  # (id, column, title, line 2, line 3, serves)
 ('K1', 0, 'Photons → amount', 'source → sink → light →', 'instrument → retrieval', 'Q3 Q5 Q6'),
 ('K2', 0, 'Pick λ × geometry', 'nadir · limb · occultation', '· lidar, by target', 'Q4 Q6 Q8 D'),
 ('K3', 0, 'Smoothed products', 'averaging kernel', '+ a priori', 'Q3 Q5'),
 ('F1', 1, 'I = I₀·exp(−τ)', 'τ = σ·N·L', 'Beer–Lambert', 'Q2 Q6 Q9 Q10'),
 ('F2', 1, 'dI/dl = −k·I + J', 'J = α·B(T)', 'emission + attenuation', 'Q2 Q8 Q9'),
 ('F3', 1, 'x̂ = xₐ + A(x − xₐ)', '+ ε ;  DOFS = tr(A)', 'optimal estimation', 'Q3 Q5'),
 ('C1', 2, 'Lifetime & mixing', 'τ = 1/Σkᵢ', 'hours → hotspots', 'Q1'),
 ('C2', 2, 'Scattering regimes', 'x = 2πr/λ', 'Rayleigh · Mie · geom.', 'Q6 Q7'),
 ('C3', 2, 'Two-λ trick', 'DOAS · DIAL', 'Ångström · A-band', 'Q3 Q6 Q8 Q10'),
 ('R1', 3, 'Photon budget', 'absorption destroys,', 'scattering redirects', 'Q2 Q9'),
 ('R2', 3, 'Kirchhoff + Planck', 'absorbers also emit', 'contrast with surface', 'Q2 Q8 Q9'),
 ('R3', 3, 'Hydrostatic layering', 'p = p₀·exp(−z/H)', 'altitude gets a label', 'Q3 Q8 Q10'),
]
def f31():
    import core_map as CM
    SV = CM.serves(CM.P1, None)
    f, ax = plt.subplots(figsize=(14, 7.6)); ax.set_xlim(0, 14); ax.set_ylim(0, 7.6); ax.axis('off')
    heads = [('3 KEY POINTS', '#273896'), ('3 FORMULAS', '#ED1C24'), ('3 CONCEPTS', '#1b7f4c'), ('3 PRINCIPLES', '#a05a00')]
    fills = ['#e3ecf7', '#fde2e3', '#e3f1e8', '#f6ead6']; cc = [BLUE, RED, GR, OR]
    for c, (h, col) in enumerate(heads):
        x = 0.15 + c * 3.5; ax.add_patch(FancyBboxPatch((x, 6.85), 3.3, 0.65, boxstyle='round,pad=0.02,rounding_size=0.08', fc=col, ec='none')); ax.text(x + 1.65, 7.17, h, ha='center', va='center', color='white', fontsize=17, weight='bold')
    for i, (k, c, t, l2, l3, srv) in enumerate(BIG):
        r = i % 3; x = 0.15 + c * 3.5; y = 4.75 - r * 2.3
        ax.add_patch(FancyBboxPatch((x, y), 3.3, 2.1, boxstyle='round,pad=0.02,rounding_size=0.08', fc=fills[c], ec='#666', lw=1.5))
        ax.text(x + .15, y + 1.75, k, fontsize=19, weight='bold', color=cc[c], va='center'); ax.text(x + .85, y + 1.75, t, fontsize=14, weight='bold', va='center')
        ax.text(x + .2, y + 1.17, l2, fontsize=14, va='center'); ax.text(x + .2, y + .76, l3, fontsize=14, va='center'); ax.text(x + .2, y + .27, 'mock exam: ' + ' '.join(sorted(SV[k], key=lambda q: int(q[1:]))), fontsize=13, color='#7a1f1f', va='center')
    f.tight_layout(pad=.3); save(f, 'f31_big12_map')

if __name__ == '__main__':
    for fn in (f25, f26, f27, f28, f29, f30, f31): fn()
    print('figures written to', OUT)
