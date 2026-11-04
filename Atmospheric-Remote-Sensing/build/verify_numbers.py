"""Tính và kiểm chứng MỌI con số dùng trong site (nguồn sự thật duy nhất -> data/verified.json).
Mọi số trong bài giảng, quiz, bài tập tính toán đều lấy từ đây hoặc từ công thức đã in trong đề cương.
Kiểm chéo: công thức đóng (numpy) so với tính độc lập khác (scipy.integrate / định nghĩa trực tiếp)."""
import json, math, os
import numpy as np
from scipy import integrate

H = 6.62607015e-34; C = 2.99792458e8; KB = 1.380649e-23
_r = os.path.join(os.path.dirname(__file__), '..', 'site')
_r = _r if os.path.isdir(_r) else os.path.join(os.path.dirname(__file__), '..')
OUT = os.path.join(_r, 'data', 'verified.json')
V = {}

# ---- Ch1: thời gian sống ----
k, oh = 2e-13, 1e6
tau_s = 1 / (k * oh)
V['co_oh'] = dict(k=k, oh=oh, tau_s=tau_s, tau_days=tau_s / 86400)
assert abs(tau_s - 5e6) < 1 and 57.8 < tau_s / 86400 < 57.9
def par(*t): return 1 / sum(1 / x for x in t)
V['par_example'] = dict(tau=[2, 3, 6], total=par(2, 3, 6))
assert abs(par(2, 3, 6) - 1) < 1e-12
# plume: e-folding distance L = U*tau
U, L = 5.0, 50e3
V['plume'] = dict(U=U, L_km=50, tau_s=L / U, tau_h=L / U / 3600)
# kiểm tra bằng khớp hàm mũ trên dữ liệu tổng hợp tau=2.78 h
xs = np.linspace(0, 150e3, 31); c = np.exp(-xs / L)
slope = np.polyfit(xs, np.log(c), 1)[0]
assert abs(-1 / slope - L) < 1
# bảng suy giảm sau t = tau, 3 tau
V['decay'] = dict(e1=math.exp(-1), e3=math.exp(-3), half_life_over_tau=math.log(2))

# ---- Ch2: Beer–Lambert, Planck, Wien ----
tv, sza = 0.5, 60.0
ts = tv / math.cos(math.radians(sza)); T = math.exp(-ts)
V['beer'] = dict(tau_v=tv, sza=sza, tau_slant=ts, T=T)
assert abs(ts - 1.0) < 1e-12 and abs(T - 0.36787944) < 1e-8
def planck(lam_m, Tk): return 2 * H * C**2 / lam_m**5 / (math.exp(H * C / (lam_m * KB * Tk)) - 1)
def planck_inv(lam_m, B): return H * C / (lam_m * KB) / math.log(1 + 2 * H * C**2 / (lam_m**5 * B))
V['wien'] = {n: dict(T=t, lam_max_um=2898 / t) for n, t in [('sun', 5778), ('earth', 288)]}
# kiểm Wien bằng cực đại số của Planck
for n, t in [('sun', 5778), ('earth', 288)]:
    from scipy.optimize import minimize_scalar
    lm = minimize_scalar(lambda l: -planck(l, t), bounds=(0.1e-6, 60e-6), method='bounded', options=dict(xatol=1e-12)).x * 1e6
    assert abs(lm - 2898 / t) / (2898 / t) < 0.002, (n, lm)
    V['wien'][n]['lam_max_numeric_um'] = lm
V['planck_10um_288'] = planck(10e-6, 288)
assert abs(planck_inv(10e-6, planck(10e-6, 288)) - 288) < 1e-6
# Stefan–Boltzmann
V['stefan'] = dict(M_earth=5.670374419e-8 * 288**4)
# Rayleigh lambda^-4
V['rayleigh_450_650'] = (650 / 450)**4
# Dobson
V['DU'] = dict(per_DU=2.687e16, example_300DU=300 * 2.687e16)

# ---- Ch3: DOAS / AMF ----
def amf_geo(sz, vz): return 1 / math.cos(math.radians(sz)) + 1 / math.cos(math.radians(vz))
amf = amf_geo(60, 30)
scd, scd_strat = 8.0e15, 3.0e15
V['amf'] = dict(sza=60, vza=30, amf=amf, scd=scd, scd_strat=scd_strat, vcd=(scd - scd_strat) / amf)
amf0 = amf_geo(0, 0); assert abs(amf0 - 2) < 1e-12
V['amf_nadir_sun_zenith'] = amf0

# ---- Ch5: optimal estimation, AK, DOFS ----
def oe(N=12, w=3.0, se=0.1, sa=1.0, Lc=3.0):
    z = np.arange(N)
    K = np.exp(-0.5 * ((z[None, :] - z[:, None]) / w)**2)
    Sa = sa**2 * np.exp(-np.abs(z[:, None] - z[None, :]) / Lc)
    Se_inv = np.eye(N) / se**2
    dot = lambda a, b: np.einsum('ij,jk->ik', a, b)   # tránh lỗi matmul BLAS của một số bản numpy macOS
    M = dot(dot(K.T, Se_inv), K) + np.linalg.inv(Sa)
    G = dot(np.linalg.inv(M), dot(K.T, Se_inv))
    A = dot(G, K)
    assert np.isfinite(A).all()
    return A, np.trace(A)
cases = {'ideal': dict(w=0.3, se=0.01, sa=1.0, Lc=3.0), 'realistic': dict(w=3.0, se=0.1, sa=1.0, Lc=3.0),
         'noisy': dict(w=3.0, se=1.0, sa=1.0, Lc=3.0)}
V['oe'] = {}
for n, p in cases.items():
    A, d = oe(**p)
    V['oe'][n] = dict(params=p, dofs=float(d), diag=[float(x) for x in np.diag(A)], rowsum=[float(x) for x in A.sum(1)],
                      A=[[float(x) for x in r] for r in A])
# kiểm: DOFS = tr(A) = tổng các trị riêng
A, d = oe(**cases['realistic']); assert abs(np.linalg.eigvals(A).real.sum() - d) < 1e-9
assert abs(V['oe']['ideal']['dofs'] - 12) < 0.05 and 0 < V['oe']['noisy']['dofs'] < V['oe']['realistic']['dofs'] < 12
# smoothing: x_hat = xa + A (x - xa); với A=I -> x_hat = x
# ---- Ch6: Ångström ----
a1, a2, l1, l2 = 0.60, 0.15, 440, 870
alpha = math.log(a1 / a2) / math.log(l2 / l1)
V['angstrom'] = dict(tau1=a1, tau2=a2, l1=l1, l2=l2, alpha=alpha, tau550=a1 * (550 / l1)**(-alpha))
# kiểm bằng hồi quy log-log trên 5 bước sóng sinh từ alpha
ls = np.array([440, 500, 675, 870, 1020.]); ts_ = a1 * (ls / 440)**(-alpha)
assert abs(-np.polyfit(np.log(ls), np.log(ts_), 1)[0] - alpha) < 1e-9
# ---- Ch7: size parameter + Mie ----
def xpar(r_um, lam_um): return 2 * math.pi * r_um / lam_um
V['size'] = dict(lam=0.55, N2=xpar(2e-4, .55), sulfate=xpar(0.2, .55), dust=xpar(5, .55), coarse_1=xpar(1, .55), coarse_10=xpar(10, .55))
def mie_qext(m, x):
    nmax = int(x + 4 * x**(1 / 3) + 2); mx = m * x
    nmx = int(max(nmax, abs(mx)) + 16); D = np.zeros(nmx + 1, dtype=complex)
    for n in range(nmx, 0, -1): D[n - 1] = n / mx - 1 / (D[n] + n / mx)
    psi0, psi1 = math.cos(x), math.sin(x); chi0, chi1 = -math.sin(x), math.cos(x)
    xi1 = complex(psi1, -chi1); q = 0.0
    for n in range(1, nmax + 1):
        psi = (2 * n - 1) / x * psi1 - psi0; chi = (2 * n - 1) / x * chi1 - chi0; xi = complex(psi, -chi)
        a = ((D[n] / m + n / x) * psi - psi1) / ((D[n] / m + n / x) * xi - xi1)
        b = ((D[n] * m + n / x) * psi - psi1) / ((D[n] * m + n / x) * xi - xi1)
        q += (2 * n + 1) * (a.real + b.real)
        psi0, psi1, chi0, chi1, xi1 = psi1, psi, chi1, chi, xi
    return 2 / x**2 * q
V['mie_qext_m133'] = {str(x): mie_qext(1.33, x) for x in [0.1, 0.5, 1, 2, 5, 10, 20, 50, 100, 200]}
# kiểm Rayleigh: Q_ext ~ (8/3) x^4 |(m^2-1)/(m^2+2)|^2 tại x nhỏ (không hấp thụ -> Q_ext = Q_sca)
m = 1.33; xr = 0.05
qr = 8 / 3 * xr**4 * abs((m**2 - 1) / (m**2 + 2))**2
assert abs(mie_qext(m, xr) - qr) / qr < 0.02, (mie_qext(m, xr), qr)
assert abs(V['mie_qext_m133']['200'] - 2) < 0.15
# ---- Ch8: TIR height ----
def bt_layer(Ts, z_km, tau, lam_um=10.0, lapse=6.5):
    Tl = Ts - lapse * z_km; lam = lam_um * 1e-6
    I = planck(lam, Ts) * math.exp(-tau) + planck(lam, Tl) * (1 - math.exp(-tau))
    return planck_inv(lam, I), Tl
Ts, tau_a = 300.0, 0.5
b1, T1 = bt_layer(Ts, 1, tau_a); b5, T5 = bt_layer(Ts, 5, tau_a)
V['tir'] = dict(Ts=Ts, tau=tau_a, lapse=6.5, z1=dict(Tl=T1, BT=b1, dBT=Ts - b1), z5=dict(Tl=T5, BT=b5, dBT=Ts - b5))
assert (Ts - b5) > (Ts - b1) > 0
# cùng độ lệch có thể do lớp mỏng-cao hoặc dày-thấp (tính suy biến)
V['tir_degenerate'] = dict(high_thin=dict(z=5, tau=0.1, dBT=Ts - bt_layer(Ts, 5, 0.1)[0]),
                           low_thick=None)
target = Ts - bt_layer(Ts, 5, 0.1)[0]
from scipy.optimize import brentq
t_low = brentq(lambda t: (Ts - bt_layer(Ts, 1, t)[0]) - target, 0.001, 20)
V['tir_degenerate']['low_thick'] = dict(z=1, tau=t_low, dBT=Ts - bt_layer(Ts, 1, t_low)[0])
# ---- A-band: đường truyền ngắn hơn khi lớp cao (mô hình đơn giản: áp suất) ----
def p_at(z_km): return 1013.25 * math.exp(-z_km / 7.0)
V['oxygen_above'] = {str(z): p_at(z) / 1013.25 for z in (1, 3, 5, 8)}
# ---- Ch4: quỹ đạo ----
V['orbit'] = dict(occult_per_day_solar=30, geo_revisit_h=1)


# ================= v2 additions (Part A, worked examples, mock Q9-Q10) =================
KB_J = KB; AMU = 1.66053907e-27; Na_air = 2.5e19
# A.6/A.4: NO2 polluted layer
N_no2 = 20e-9 * Na_air; tau_no2 = 1.5e-19 * 1e5 * N_no2
V['a_no2'] = dict(N=N_no2, tau=tau_no2, t=math.exp(-tau_no2)); assert abs(tau_no2 - 7.5e-3) < 1e-9
# Q9(c): homogeneous layer
tau9 = 2e-20 * 5e13 * 1e5; V['q9c'] = dict(tau=tau9, t=math.exp(-tau9)); assert abs(tau9 - 0.1) < 1e-12
# Q10(c): differential optical depth
V['q10c'] = dict(D=2e-19 * 1e16)
# Q1 plume example
V['plume72'] = dict(x_km=72, U_ms=5, U_kmh=18.0, tau_h=72 / 18.0); assert V['plume72']['tau_h'] == 4.0
# Q2 ozone layer
du300 = 300 * 2.687e16; am = 1 / math.cos(math.radians(60)) + 1
oz = {}
for lam, sg in [(310, 1e-19), (330, 1e-20)]:
    ts_ = sg * du300 * am; oz[str(lam)] = dict(sigma=sg, tau=ts_, T=math.exp(-ts_))
V['ozone'] = dict(column=du300, airmass=am, **{k: v for k, v in oz.items()})
# Q3 megacity column
V['megacity'] = dict(scd=2.4e16, amf=1.2, vcd=2.4e16 / 1.2, du=2.4e16 / 1.2 / 2.687e16, vcd_amf30=2.4e16 / (1.2 * 1.3))
# Q4 limb path
Rk = 6371.0
V['limb'] = dict(R=Rk, H=1.0, L=math.sqrt(8 * Rk * 1.0), ratio=math.sqrt(8 * Rk * 1.0) / 1.0, geo_ratio=36000 / 800)
# Q5 two-layer example
Kv = np.array([[1., 1.]]); Sa2 = np.eye(2); Se2 = 0.01
A2 = Sa2 @ Kv.T @ np.linalg.inv(Kv @ Sa2 @ Kv.T + Se2) @ Kv
V['two_layer'] = dict(A=A2.tolist(), dofs=float(np.trace(A2)), denom=float((Kv @ Sa2 @ Kv.T + Se2)[0, 0])); assert abs(np.trace(A2) - 1) < 0.01
# Q6 Angstrom examples (guide convention alpha = -ln(t1/t2)/ln(l1/l2))
for nm, a1, a2_ in [('smoke', 0.8, 0.2), ('dust', 0.50, 0.45)]:
    V['ang_' + nm] = dict(t440=a1, t870=a2_, alpha=-math.log(a1 / a2_) / math.log(440 / 870))
# Q7 same particle, different regimes
V['droplet'] = dict(x_vis=2 * math.pi * 10 / 0.55, x_radar=2 * math.pi * 10 / 3000.0)
# Q8: TIR 310 K with dust at 4 km, tau=0.7; 1 km
def dep(Ts, z, tau): b, _ = bt_layer(Ts, z, tau); return Ts - b
V['tir310'] = dict(Ts=310, z4=dict(Tl=310 - 6.5 * 4, dBT=dep(310, 4, 0.7)), z1=dict(Tl=310 - 6.5, dBT=dep(310, 1, 0.7)))
V['o2_scale8'] = {str(z): math.exp(-z / 8.0) for z in (1, 6)}
# A.5 line widths
def hwhm_doppler(nu_cm, T, mass_amu): return nu_cm / C * math.sqrt(2 * math.log(2) * KB * T / (mass_amu * AMU)) * 1.0
def hwhm_lorentz(P_atm, T, g0=0.07, n=0.7): return g0 * P_atm * (296.0 / T) ** n
Tz = {0: 288., 15: 217., 40: 250.}; Pz = {z: math.exp(-z / 7.0) for z in Tz}
V['lines'] = dict(doppler_ch4_2927=hwhm_doppler(2927, 250, 16.04) * 1.0)
V['lines']['alt'] = {str(z): dict(T=Tz[z], P_atm=Pz[z], lorentz=hwhm_lorentz(Pz[z], Tz[z]), doppler=hwhm_doppler(2927, Tz[z], 16.04)) for z in Tz}
V['lines']['km_per_decade'] = 7.0 * math.log(10)
assert 0.003 < V['lines']['doppler_ch4_2927'] < 0.005
cross = [z for z in np.arange(0, 60, 0.1) if hwhm_lorentz(math.exp(-z / 7), 230) < hwhm_doppler(2927, 230, 16.04)]
V['lines']['crossover_km'] = float(cross[0])

# ---- Lecture master (J. Cuesta): hydrostatic law, sinks example, lidar exercises, DIAL ----
from scipy.integrate import solve_ivp
R_, M_, g_ = 8.314, 29e-3, 9.81
Hs = R_ * 284 / (M_ * g_)
sol = solve_ivp(lambda z, p: -p * M_ * g_ / (R_ * 284), [0, 10000], [1013.25], t_eval=[1000, 2000, 3000, 10000], rtol=1e-10, atol=1e-10)
hy = {str(int(z / 1000)): 1013.25 * math.exp(-z / Hs) for z in (1000, 2000, 3000, 10000)}
for z, pv in zip((1, 2, 3, 10), sol.y[0]): assert abs(hy[str(z)] - pv) < 1e-4 * pv
V['hydro'] = dict(H_m=Hs, H_km=Hs / 1000, p=hy, half_km=Hs * math.log(2) / 1000, table={'1': 900, '2': 794, '3': 700, '10': 265},
                  err10_pct=(hy['10'] - 265) / 265 * 100)
# sinks example (lecture slide 40): chemistry 1 d, rain once a week = 7 d, outflow 100 km / 20 km/h
tc, td, to = 1.0, 7.0, (100 / 20) / 24
kc, kd, ko = 1 / tc, 1 / td, 1 / to
ktot = kc + kd + ko
assert abs(1 / (1 / tc + 1 / td + 1 / to) - 1 / ktot) < 1e-12
V['sinks_ex'] = dict(tau_chem_d=tc, tau_dep_d=td, tau_out_h=to * 24, k_chem=kc, k_dep=kd, k_out=ko, k_tot=ktot, tau_tot_h=24 / ktot,
                     f_out=ko / ktot, f_chem=kc / ktot, f_dep=kd / ktot)
# lidar exercise 1 (lecture slide 230): P = K / z^2 * beta * T^2
Kc, bm, Pmin = 1e5, 1e-6, 1e-9
def Plid(z, bp, T): return Kc / z**2 * (bm + bp) * T**2
def Plid2(z, bp, tau_one_way): return Kc / z**2 * (bm + bp) * math.exp(-2 * tau_one_way)
cases = {'a': (1e3, 1e-6, 0.7), 'b': (3e3, 15e-6, 0.5), 'c': (12e3, 0.2e-6, 0.3)}
lid = {}
for k_, (z_, bp_, T_) in cases.items():
    a_, b_ = Plid(z_, bp_, T_), Plid2(z_, bp_, -math.log(T_)); assert abs(a_ - b_) < 1e-12 * a_
    lid[k_] = dict(z_km=z_ / 1e3, beta_p=bp_, T=T_, P_nW=a_ * 1e9, detect=bool(a_ >= Pmin))
fac = math.exp(-2 * 0.8)
lid['d'] = dict(cloud_tau=0.8, factor=fac, P3_nW=lid['b']['P_nW'] * fac, P12_nW=lid['c']['P_nW'] * fac,
                detect3=bool(lid['b']['P_nW'] * fac >= 1), detect12=bool(lid['c']['P_nW'] * fac >= 1), lecture_P3_nW=8.6)
V['lidar_ex1'] = lid
# DIAL (exercise 2): alpha = 1/(2 dr) * ln[ P_OFF(r1) P_ON(r2) / (P_ON(r1) P_OFF(r2)) ] taken positive
on1, on2, off1, off2, dr = 10.0, 7.0, 10.0, 8.0, 500.0
al = abs(math.log((off1 * on2) / (on1 * off2))) / (2 * dr)
al2 = (math.log(on1 / on2) - math.log(off1 / off2)) / (2 * dr)  # two-way: ON decays faster
assert abs(al - al2) < 1e-15
V['dial'] = dict(alpha=al, q_gkg=5e4 * al, dr=dr, lecture_alpha=1.33e-4, lecture_q=6.68)
# lidar timing and ambiguity (home-made illustration)
V['lidar_time'] = dict(t_3km_us=2 * 3000 / C * 1e6, dR_30ns=C * 30e-9 / 2, Rmax_10kHz_km=C / (2 * 10e3) / 1e3, Rmax_20Hz_km=C / (2 * 20.0) / 1e3)
# Rayleigh blue vs red, photon energies
V['rayleigh_br'] = (650 / 400) ** 4
V['photon_eV'] = dict(no2_424=H * C / 424e-9 / 1.602176634e-19, o2_240=H * C / 240e-9 / 1.602176634e-19)
V['photon_eV']['no2_kJmol'] = V['photon_eV']['no2_424'] * 96.485; V['photon_eV']['o2_kJmol'] = V['photon_eV']['o2_240'] * 96.485
# IASI / GOME-2 / multispectral (lecture slides 144-145)
V['multi'] = dict(dofs_iasi=dict(land=0.25, ocean=0.15), dofs_multi=dict(land=0.35, ocean=0.25), gain_land=0.35 / 0.25 - 1, gain_ocean=0.25 / 0.15 - 1,
                  h_iasi=dict(land=3.0, ocean=4.3), h_multi=dict(land=2.2, ocean=3.5), dh_land=3.0 - 2.2, dh_ocean=4.3 - 3.5)
# core mini-checks: slant optical depth, size parameter, aerosol Angstrom (smoke, dust vs lecture)
V['core'] = dict(slant_tau_60=0.5 / math.cos(math.radians(60)), T_slant=math.exp(-0.5 / math.cos(math.radians(60))),
                 x_dust_vis=2 * math.pi * 5 / 0.55, x_molecule=2 * math.pi * 0.0002 / 0.55)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(V, open(OUT, 'w'), indent=1, ensure_ascii=False)
print('OK verified.json — CO lifetime %.2f days; T=%.4f; x(N2,sulfate,dust)=%.4f,%.3f,%.2f; alpha=%.4f; dBT(1km,5km)=%.2f,%.2f K; DOFS ideal/realistic/noisy=%.2f/%.2f/%.2f' % (
    V['co_oh']['tau_days'], T, V['size']['N2'], V['size']['sulfate'], V['size']['dust'], alpha, Ts - b1, Ts - b5,
    V['oe']['ideal']['dofs'], V['oe']['realistic']['dofs'], V['oe']['noisy']['dofs']))
