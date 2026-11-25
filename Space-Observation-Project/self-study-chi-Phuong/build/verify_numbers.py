# -*- coding: utf-8 -*-
"""Kiểm số liệu cho site tự học (L1 - L3 của cô Phương). Mỗi đại lượng tính HAI cách độc lập; lệch > 1e-3 thì dừng.
Ra: self-study/data/verified.json (đọc bởi build_site.py và tests/test_calc.js). Chạy: python3 self-study/build/verify_numbers.py
Hằng số: CODATA 2018 qua scipy.constants (G, k, m_H dùng m_u). G trên slide L2 p8 = 6.673e-8 cgs: ghi cả hai."""
import json
import math
import pathlib
import sys

import numpy as np
from scipy import constants as C
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

ROOT = pathlib.Path(__file__).resolve().parents[1]
G = C.G * 1e3                      # cgs: cm3 g-1 s-2   (6.674e-8)
G_SLIDE = 6.673e-8
K_B = C.k * 1e7                    # erg/K
M_H = C.m_u * 1e3                  # g (1 u, used as m_H; the 0.8 % difference is below the other uncertainties)
PC, AU, LY, MSUN, YR, MYR = C.parsec * 100, C.au * 100, C.light_year * 100, 1.98847e33, C.Julian_year, C.Julian_year * 1e6
out, bad = {}, []


def chk(name, a, b, tol=1e-3):
    rel = abs(a - b) / max(abs(a), abs(b))
    if rel > tol: bad.append((name, a, b, rel))
    return a


# ---------------------------------------------------------------- L1: c = lambda nu, E = h nu, Wien
bands = [("radio", 1e3), ("microwave", 1e-2), ("infrared", 1e-5), ("visible", 0.5e-6), ("ultraviolet", 1e-8), ("X-ray", 1e-10), ("gamma", 1e-12)]
slide_nu = {"radio": 1e4, "microwave": 1e8, "infrared": 1e12, "visible": 1e15, "ultraviolet": 1e16, "X-ray": 1e18, "gamma": 1e20}   # tick marks read from L1 p2 (positions are rough)
em = []
for nm, lam in bands:
    nu_a = C.c / lam                                # way 1: c = lambda nu
    nu_b = 1.0 / (lam / C.c)                        # way 2: via period T = lambda / c
    chk("nu " + nm, nu_a, nu_b)
    E_a = C.h * nu_a / C.e                          # eV, E = h nu
    E_b = C.h * C.c / lam / C.e                     # E = h c / lambda
    chk("E " + nm, E_a, E_b)
    T_w = 2.897771955e-3 / lam                      # Wien: temperature whose emission peaks at this wavelength
    em.append(dict(band=nm, lam_m=lam, nu_Hz=nu_a, E_eV=E_a, T_wien_K=T_w, slide_axis_Hz=slide_nu[nm]))
out["em"] = em
# 1 nm = 1e-9 m etc: units on L1 p3
out["l1p3"] = dict(xray_nm=1, uv_nm=10, vis_nm=500, ir_um=10, mm=1, radio_cm=10, nu_vis_Hz=C.c / 500e-9)

# ---------------------------------------------------------------- L2: free fall, sound speed, Jeans
MU = (2.0, 2.33)                                    # mean mass per particle in units of m_H (pure H2; H2 + 10 % He by number)
NS = (1e3, 1e4)                                     # cm-3
TS = (30.0, 50.0)                                   # K, exercise L2 p13
TS_SLIDE = (50.0, 100.0)                            # K, L2 p4


def rho_of(n, mu): return n * mu * M_H


def tff_slide(rho): return 1.0 / math.sqrt(G * rho)                          # L2 p8: t_ff = sqrt(1/(G rho))
def tff_full_a(rho): return math.sqrt(3 * math.pi / (32 * G * rho))          # closed form


def tff_full_b(rho):                                                         # numerical: shell of radius r0 in uniform sphere, M = 4/3 pi r0^3 rho
    r0 = 1.0; M = 4.0 / 3.0 * math.pi * r0 ** 3 * rho
    def f(t, y): return [y[1], -G * M / y[0] ** 2]
    ev = lambda t, y: y[0] - 1e-4 * r0
    ev.terminal = True; ev.direction = -1
    s = solve_ivp(f, [0, 1e15], [r0, 0.0], events=ev, rtol=1e-11, atol=1e-14 * r0, max_step=1e12)
    return s.t_events[0][0] * 1.0                                            # up to r = 1e-4 r0 (the last 1e-4 contributes ~1e-6 relative)


def cs_a(T, mu): return math.sqrt(K_B * T / (mu * M_H))                      # isothermal sound speed


def cs_b(T, mu):                                                             # c_s^2 = dP/drho at fixed T, P = rho k T / (mu m_H), by finite difference
    h = 1e-6; rho = 1e-20
    P = lambda r: r * K_B * T / (mu * M_H)
    return math.sqrt((P(rho * (1 + h)) - P(rho * (1 - h))) / (2 * rho * h))


def LJ_rigorous_a(cs, rho): return cs * math.sqrt(math.pi / (G * rho))       # Jeans wavelength
def LJ_rigorous_b(cs, rho):                                                  # root of the dispersion relation w^2 = cs^2 k^2 - 4 pi G rho
    kJ = brentq(lambda k: cs * cs * k * k - 4 * math.pi * G * rho, 1e-30, 1e-10, xtol=1e-40, rtol=1e-13)
    return 2 * math.pi / kJ
def LJ_slide(cs, rho): return cs / math.sqrt(G * rho)                        # L2 p10: t_s = L / c_s set equal to t_ff = 1 / sqrt(G rho)


def mass_sphere(R, rho): return 4.0 / 3.0 * math.pi * R ** 3 * rho


tab = []
for mu in MU:
    for n in NS:
        rho = rho_of(n, mu)
        ta, tb = tff_full_a(rho), tff_full_b(rho)
        chk("tff full", ta, tb, 2e-3)
        row = dict(mu=mu, n=n, rho=rho, tff_slide_s=tff_slide(rho), tff_slide_Myr=tff_slide(rho) / MYR, tff_full_s=ta, tff_full_Myr=ta / MYR, tff_full_numeric_Myr=tb / MYR)
        for T in TS + TS_SLIDE:
            ca, cb = cs_a(T, mu), cs_b(T, mu); chk("cs", ca, cb)
            la, lb = LJ_rigorous_a(ca, rho), LJ_rigorous_b(ca, rho); chk("LJ", la, lb)
            ls = LJ_slide(ca, rho)
            row[f"T{int(T)}"] = dict(cs_kms=ca / 1e5, LJ_rig_cm=la, LJ_rig_pc=la / PC, LJ_slide_pc=ls / PC, LJ_rig_AU=la / AU,
                                     MJ_rig_halfsphere_Msun=mass_sphere(la / 2, rho) / MSUN, MJ_rig_sphereR_Msun=mass_sphere(la, rho) / MSUN,
                                     MJ_slide_sphereR_Msun=mass_sphere(ls, rho) / MSUN, MJ_slide_halfsphere_Msun=mass_sphere(ls / 2, rho) / MSUN)
        tab.append(row)
out["jeans_table"] = tab
# Two extra checks of the closed forms: M_J ~ T^{3/2} rho^{-1/2}; L_J ~ T^{1/2} rho^{-1/2}
r1, r2 = tab[0]["T30"], tab[0]["T50"]
chk("MJ scaling T", r2["MJ_rig_sphereR_Msun"] / r1["MJ_rig_sphereR_Msun"], (50 / 30) ** 1.5)
chk("LJ scaling rho", tab[1]["T30"]["LJ_rig_pc"] / tab[0]["T30"]["LJ_rig_pc"], 10 ** -0.5)
# ranges for the two original exercises (used in the text)
out["ex_tff_range_Myr"] = dict(slide=[min(r["tff_slide_Myr"] for r in tab), max(r["tff_slide_Myr"] for r in tab)], full=[min(r["tff_full_Myr"] for r in tab), max(r["tff_full_Myr"] for r in tab)])
flat = [(r["mu"], r["n"], T, r[f"T{T}"]) for r in tab for T in (30, 50)]
out["ex_jeans_range"] = dict(
    cs_kms=[min(x[3]["cs_kms"] for x in flat), max(x[3]["cs_kms"] for x in flat)],
    LJ_rig_pc=[min(x[3]["LJ_rig_pc"] for x in flat), max(x[3]["LJ_rig_pc"] for x in flat)],
    MJ_rig_halfsphere=[min(x[3]["MJ_rig_halfsphere_Msun"] for x in flat), max(x[3]["MJ_rig_halfsphere_Msun"] for x in flat)],
    MJ_rig_sphereR=[min(x[3]["MJ_rig_sphereR_Msun"] for x in flat), max(x[3]["MJ_rig_sphereR_Msun"] for x in flat)],
    LJ_slide_pc=[min(x[3]["LJ_slide_pc"] for x in flat), max(x[3]["LJ_slide_pc"] for x in flat)],
    MJ_slide_sphereR=[min(x[3]["MJ_slide_sphereR_Msun"] for x in flat), max(x[3]["MJ_slide_sphereR_Msun"] for x in flat)])
# G in the slide (6.673e-8) vs CODATA: effect on t_ff
out["G"] = dict(codata_cgs=G, slide_cgs=G_SLIDE, tff_ratio=math.sqrt(G / G_SLIDE))
# slide numbers: cloud ~150 ly, mass 1e5 - 1e6 Msun -> mean density; dark cloud 200,000 AU, collapse 10,000 AU
R_cloud = 75 * LY
for Mc in (1e5, 1e6):
    rho_c = Mc * MSUN / (4.0 / 3.0 * math.pi * R_cloud ** 3)
    out[f"cloud_M{int(Mc):d}"] = dict(rho_gcm3=rho_c, n_H2=rho_c / (2.33 * M_H), tff_Myr=tff_full_a(rho_c) / MYR)
out["sizes"] = dict(AU_cm=AU, pc_cm=PC, ly_cm=LY, pc_AU=PC / AU, pc_ly=PC / LY, dark_cloud_pc=200000 * AU / PC, core_pc=10000 * AU / PC, cloud_150ly_pc=150 * LY / PC)
# spin-up: r^2 omega = const
out["spinup"] = dict(example_radius_ratio=10, omega_ratio=10 ** 2, note="Illustration: L = I omega, I ~ M r^2, so omega2 = omega1 (r1/r2)^2")

# ---------------------------------------------------------------- L3: radioactive decay, timescales
T_HALF_SLIDE = 1.25                                  # Gyr, read from the ticks 1.25 / 2.5 / 3.75 on the decay graph of L3 p37
def N_frac(t, th): return 2.0 ** (-t / th)
def N_frac_ode(t, th):
    lam = math.log(2) / th
    s = solve_ivp(lambda tt, y: [-lam * y[0]], [0, t], [1.0], rtol=1e-12, atol=1e-14); return s.y[0][-1]
dec = []
for k in range(0, 6):
    t = k * T_HALF_SLIDE; dec.append(dict(n_half_lives=k, t_Gyr=t, parent=chk("decay", N_frac(t, T_HALF_SLIDE), N_frac_ode(t, T_HALF_SLIDE)), daughter=1 - N_frac(t, T_HALF_SLIDE)))
out["decay"] = dec
def age_a(DP, th): return th * math.log2(1.0 + DP)
def age_b(DP, th): return brentq(lambda t: (1 - 2.0 ** (-t / th)) / 2.0 ** (-t / th) - DP, 0, 100 * th)     # solve D/P = 2^{t/T} - 1 numerically
ages = []
for DP in (0.25, 0.5, 1.0, 2.0, 3.0, 7.0):
    ages.append(dict(DP=DP, t_Gyr=chk("age", age_a(DP, T_HALF_SLIDE), age_b(DP, T_HALF_SLIDE)), parent_frac=1 / (1 + DP)))
out["ages"] = ages
out["meteorite_age"] = dict(Gyr=4.6, half_lives_of_K40=4.6 / T_HALF_SLIDE, parent_left=N_frac(4.6, T_HALF_SLIDE), DP=2 ** (4.6 / T_HALF_SLIDE) - 1)
out["time_ratios"] = dict(solar_age_over_universe=(4.6 / 13.0, 4.6 / 14.0), disk_life_Myr=10, core_accretion_Myr=(3, 10), gas_collapse_Myr=0.1, jupiter_orbits=None)
out["frost"] = dict(note="temperatures on L3 p17: 2000 K, 300 K, 50 K (labels do not align with substances; reading kept qualitative)")
# Planck: wavelength of peak emission (Wien) for the temperatures on the slide, a link between L1 and L3
out["wien"] = [dict(T_K=T, lam_um=2.897771955e-3 / T * 1e6) for T in (2000, 300, 100, 50, 30)]


# ---------------------------------------------------------------- extras for the formula pages
from scipy.optimize import minimize_scalar
SIGMA = C.sigma; HC_EVNM = C.h * C.c / C.e * 1e9          # eV nm
def planck(lam, T): return 1.0 / (lam ** 5 * (math.exp(C.h * C.c / (lam * C.k * T)) - 1.0))
def wien_num(T):                                          # way 2: maximise the Planck function numerically
    r = minimize_scalar(lambda x: -planck(x * 1e-6, T), bounds=(1e-3 / T * 1e3, 2e4 / T), method="bounded", options=dict(xatol=1e-12)); return r.x * 1e-6
wien = []
for lab, T in (("Sun", 5772.0), ("Earth surface", 288.0), ("dense cloud", 10.0), ("CMB", 2.7255), ("hot gas in a cluster", 1e7), ("X-ray gas", 1e6)):
    a = C.value("Wien wavelength displacement law constant") / T; b = wien_num(T); chk("wien " + lab, a, b, 2e-3)
    wien.append(dict(label=lab, T_K=T, lam_m=a, lam_num_m=b))
out["wien_examples"] = wien; out["wien_b_umK"] = C.value("Wien wavelength displacement law constant") * 1e6
out["hc_eVnm"] = HC_EVNM; out["h_eVs"] = C.h / C.e; out["me_c2_keV"] = C.m_e * C.c ** 2 / C.e / 1e3
def teq_formula(d_au, L=1.0): return 278.3 * L ** 0.25 / math.sqrt(d_au)            # way 1: textbook coefficient
def teq_num(d_au, L=1.0):                                                           # way 2: balance L_sun pi R^2 / (4 pi d^2) = 4 pi R^2 sigma T^4 ... solved by root finding
    Lsun = 3.828e26; d = d_au * C.au
    f = lambda T: 4 * math.pi * d ** 2 * 0 + (L * Lsun / (16 * math.pi * SIGMA * d ** 2)) ** 0.25 - T
    return brentq(f, 1.0, 1e4)
teq = []
for d in (1.0, 3.0, 5.2, 30.0):
    a, b = teq_formula(d), teq_num(d); chk("Teq %g" % d, a, b, 2e-3); teq.append(dict(d_au=d, T_K=a))
out["Teq"] = teq; out["Teq_coeff_K"] = teq_num(1.0)
# decay constants
th = 1.25; lam_d = math.log(2) / th
out["decay_const"] = dict(T_half=th, lam_per_Gyr=lam_d, tau_Gyr=1 / lam_d, tau_over_T=1 / math.log(2))
# practice items (answers by the same two-method functions)
def tff_both(n, mu): r = rho_of(n, mu); return tff_slide(r) / MYR, tff_full_a(r) / MYR, tff_full_b(r) / MYR
def jeans_all(n, mu, T):
    r = rho_of(n, mu); c = cs_a(T, mu); chk("cs pr", c, cs_b(T, mu)); L = LJ_rig_a_ = LJ_rigorous_a(c, r); chk("LJ pr", L, LJ_rigorous_b(c, r))
    return dict(rho=r, cs_kms=c / 1e5, LJ_pc=L / PC, LJ_AU=L / AU, LJslide_pc=LJ_slide(c, r) / PC, MJ_half=mass_sphere(L / 2, r) / MSUN, MJ_full=mass_sphere(L, r) / MSUN)
pr = {}
pr["tff_1e5"] = dict(n=1e5, mu=2.33, vals=tff_both(1e5, 2.33))
pr["jeans_core"] = dict(n=1e5, mu=2.33, T=10.0, vals=jeans_all(1e5, 2.33, 10.0))
pr["jeans_diffuse"] = dict(n=1e2, mu=2.33, T=100.0, vals=jeans_all(1e2, 2.33, 100.0))
pr["spin_core"] = dict(r1_AU=1e4, r2_AU=100.0, factor=(1e4 / 100.0) ** 2, factor_to_1AU=(1e4 / 1.0) ** 2)
rho_1Myr = 3 * math.pi / (32 * G * (1 * MYR) ** 2)       # density that gives t_ff(full) = 1 Myr
chk("tff inverse", tff_full_a(rho_1Myr) / MYR, 1.0)
pr["tff_inverse"] = dict(t_Myr=1.0, rho=rho_1Myr, n_mu233=rho_1Myr / (2.33 * M_H))
pr["age_DP05"] = dict(DP=0.5, t_Gyr=age_a(0.5, T_HALF_SLIDE)); chk("age 0.5", age_a(0.5, 1.25), age_b(0.5, 1.25))
pr["age_DP15"] = dict(DP=15.0, t_Gyr=age_a(15.0, T_HALF_SLIDE)); chk("age 15", age_a(15.0, 1.25), age_b(15.0, 1.25))
pr["teq_dist150"] = dict(T_K=150.0, d_au=(278.3 / 150.0) ** 2)
chk("teq inverse", teq_formula((278.3 / 150.0) ** 2), 150.0)
out["practice"] = pr

json.dump(out, open(ROOT / "data" / "verified.json", "w"), indent=1, default=float)
if bad:
    print("FAILS:"); [print(" ", b) for b in bad]; sys.exit(1)
print("FAILS: none")
t = out["ex_tff_range_Myr"]; j = out["ex_jeans_range"]
print(f"t_ff slide form {t['slide'][0]:.2f}-{t['slide'][1]:.2f} Myr; full {t['full'][0]:.2f}-{t['full'][1]:.2f} Myr")
print(f"c_s {j['cs_kms'][0]:.2f}-{j['cs_kms'][1]:.2f} km/s; L_J rigorous {j['LJ_rig_pc'][0]:.2f}-{j['LJ_rig_pc'][1]:.2f} pc; slide-form {j['LJ_slide_pc'][0]:.2f}-{j['LJ_slide_pc'][1]:.2f} pc")
print(f"M_J (sphere R=L_J/2) {j['MJ_rig_halfsphere'][0]:.0f}-{j['MJ_rig_halfsphere'][1]:.0f}; (sphere R=L_J) {j['MJ_rig_sphereR'][0]:.0f}-{j['MJ_rig_sphereR'][1]:.0f}; slide-form R=L_J {j['MJ_slide_sphereR'][0]:.0f}-{j['MJ_slide_sphereR'][1]:.0f} Msun")
