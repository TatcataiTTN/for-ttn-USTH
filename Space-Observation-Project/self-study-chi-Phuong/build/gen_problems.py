# -*- coding: utf-8 -*-
"""Kho bài tập tương tự bài của cô (tham số cố định, không ngẫu nhiên khi chạy): 9 dạng x 14 bài = 126 bài. Mỗi đáp án tính HAI cách độc lập (công thức đóng và phương pháp số / suy ngược), lệch > 3e-3 thì dừng.
Ra: data/problems.json, site/data/problems.js. tests/test_calc.js tính lại từng bài bằng JavaScript (calc.js: solve) và so với file này.
Chạy: python3 build/gen_problems.py"""
import json
import math
import pathlib
import sys

from scipy import constants as C
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

ROOT = pathlib.Path(__file__).resolve().parents[1]
G = C.G * 1e3; KB = C.k * 1e7; MH = C.m_u * 1e3; PC = C.parsec * 100; AU = C.au * 100; MSUN = 1.98847e33; MYR = C.Julian_year * 1e6
bad = []


def chk(name, a, b, tol=3e-3):
    if abs(a - b) / max(abs(a), abs(b)) > tol: bad.append((name, a, b))
    return a


def p10(x):                                   # 10000 -> 10⁴ ; 3000 -> 3×10³
    if x == 0: return "0"
    e = int(math.floor(math.log10(abs(x)) + 1e-12)); m = x / 10 ** e
    sup = lambda k: str(k).translate(str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"))
    if e in (0, 1, 2) and abs(m - round(m)) < 1e-9: return f"{x:g}"
    return (f"10{sup(e)}" if abs(m - 1) < 1e-9 else f"{m:g}×10{sup(e)}")


def num(x, sig=3):
    if x == 0: return "0"
    if 1e-3 <= abs(x) < 1e4:
        s = f"{x:.{sig}g}"
        if "e" not in s: return s
    m, e = f"{x:.{sig - 1}e}".split("e"); sup = str(int(e)).translate(str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")); return f"{float(m):g}×10{sup}"


VNC = lambda s: s.replace(".", ",")           # decimal comma in Vietnamese text (applied only to strings made of numbers)
def both(en, **kw): return (en, VNC_text(en))
def VNC_text(en):
    import re
    return re.sub(r"(?<=\d)\.(?=\d)", ",", en)


# ---------------------------------------------------------------- two-method solvers
def rho_(n, mu): return n * mu * MH


def tff_slide(rho): return 1 / math.sqrt(G * rho)
def tff_full_a(rho): return math.sqrt(3 * math.pi / (32 * G * rho))
def tff_full_b(rho):
    r0 = 1.0; M = 4 / 3 * math.pi * r0 ** 3 * rho
    ev = lambda t, y: y[0] - 1e-4 * r0; ev.terminal = True; ev.direction = -1
    s = solve_ivp(lambda t, y: [y[1], -G * M / y[0] ** 2], [0, 1e15], [r0, 0.0], events=ev, rtol=1e-11, atol=1e-14, max_step=1e12); return s.t_events[0][0]
def cs_a(T, mu): return math.sqrt(KB * T / (mu * MH))
def cs_b(T, mu):
    h = 1e-6; rho = 1e-20; P = lambda r: r * KB * T / (mu * MH); return math.sqrt((P(rho * (1 + h)) - P(rho * (1 - h))) / (2 * rho * h))
def lj_a(cs, rho): return cs * math.sqrt(math.pi / (G * rho))
def lj_b(cs, rho):
    k = brentq(lambda k: cs * cs * k * k - 4 * math.pi * G * rho, 1e-30, 1e-10, xtol=1e-40, rtol=1e-13); return 2 * math.pi / k
def msph(R, rho): return 4 / 3 * math.pi * R ** 3 * rho


def teq_a(d): return (3.828e26 / (16 * math.pi * C.sigma * (d * C.au) ** 2)) ** 0.25
def teq_b(d):          # balance of absorbed and emitted power solved by root finding
    Lsun = 3.828e26; R = 1.0; return brentq(lambda T: Lsun * math.pi * R ** 2 / (4 * math.pi * (d * C.au) ** 2) - 4 * math.pi * R ** 2 * C.sigma * T ** 4, 1.0, 1e5)


P = []


def add(type_, lec, eq, q, params, fields, steps, level=1):
    P.append(dict(id=f"{type_}{sum(1 for p in P if p['type'] == type_) + 1}", type=type_, lec=lec, eq=eq, q=q, params=params, fields=fields, steps=steps, level=level))


def F(k, label, unit, acc): return dict(k=k, label=label, unit=unit, accept=acc)


# ---- 1 free-fall time (L2 p9)
N1 = [(1e2, 2.33), (3e2, 2.0), (1e3, 2.33), (3e3, 2.0), (1e4, 2.0), (3e4, 2.33), (1e5, 2.33), (3e5, 2.0), (1e6, 2.33), (1e7, 2.0), (5e2, 2.33), (2e4, 2.0), (5e4, 2.33), (2e5, 2.33)]
for n, mu in N1:
    rho = rho_(n, mu); a = tff_slide(rho) / MYR; b = chk("tff", tff_full_a(rho), tff_full_b(rho)) / MYR
    en = f"A molecular cloud has a mean density of {p10(n)} molecules per cm³ (μ = {mu:g}). Find its free-fall time, in Myr (give the slide form 1/√(Gρ) or the exact form)."
    vi = f"Một đám mây phân tử có mật độ trung bình {p10(n)} phân tử trên cm³ (μ = {str(mu).replace('.', ',')}). Tìm thời gian rơi tự do, theo triệu năm (cho dạng slide 1/√(Gρ) hoặc dạng chính xác)."
    st = [(f"ρ = n μ m_H = {p10(n)} × {mu:g} × 1.661×10⁻²⁴ = {num(rho)} g/cm³.", f"ρ = n μ m_H = {p10(n)} × {str(mu).replace('.', ',')} × 1,661×10⁻²⁴ = {VNC(num(rho))} g/cm³."),
          (f"Slide form: t_ff = 1/√(Gρ) = {num(tff_slide(rho))} s = {num(a)} Myr.", VNC(f"Dạng slide: t_ff = 1/√(Gρ) = {num(tff_slide(rho))} s = {num(a)} triệu năm.")),
          (f"Exact form: × 0.543 = {num(b)} Myr.", VNC(f"Dạng chính xác: × 0,543 = {num(b)} triệu năm."))]
    add("tff", "L2", "tff", (en, vi), dict(n=n, mu=mu), [F("t", ("free-fall time", "thời gian rơi tự do"), "Myr", [a, b])], [(x[0], VNC(x[1]) if "0,543" not in x[1] else x[1]) for x in st])

# ---- 2 Jeans length and mass (L2 p13)
J = [(1e3, 30, 2.33), (1e4, 30, 2.33), (1e3, 50, 2.33), (1e4, 50, 2.33), (1e2, 100, 2.33), (1e3, 100, 2.0), (1e5, 10, 2.33), (1e4, 20, 2.33), (1e6, 10, 2.0), (1e5, 20, 2.33), (5e3, 40, 2.33), (2e4, 15, 2.0), (1e2, 50, 2.33), (1e3, 10, 2.33)]
for n, T, mu in J:
    rho = rho_(n, mu); c = chk("cs", cs_a(T, mu), cs_b(T, mu)); L = chk("LJ", lj_a(c, rho), lj_b(c, rho)); Ls = c / math.sqrt(G * rho)
    mh, mf, ms = msph(L / 2, rho) / MSUN, msph(L, rho) / MSUN, msph(Ls, rho) / MSUN
    en = f"Calculate the sound speed, the Jeans length and the Jeans mass of a cloud with n = {p10(n)} cm⁻³, T = {T:g} K, μ = {mu:g}. (Say which sphere radius you use for the mass.)"
    vi = f"Tính tốc độ âm, độ dài Jeans và khối lượng Jeans của một đám mây có n = {p10(n)} cm⁻³, T = {T:g} K, μ = {str(mu).replace('.', ',')}. (Nêu bán kính cầu dùng cho khối lượng.)"
    st = [(f"ρ = {num(rho)} g/cm³; c_s = √(kT/(μ m_H)) = {num(c / 1e5)} km/s.", VNC(f"ρ = {num(rho)} g/cm³; c_s = √(kT/(μ m_H)) = {num(c / 1e5)} km/s.")),
          (f"λ_J = c_s √(π/(Gρ)) = {num(L)} cm = {num(L / PC)} pc = {num(L / AU)} AU (slide-style c_s/√(Gρ): {num(Ls / PC)} pc).", VNC(f"λ_J = c_s √(π/(Gρ)) = {num(L)} cm = {num(L / PC)} pc = {num(L / AU)} AU (kiểu slide c_s/√(Gρ): {num(Ls / PC)} pc).")),
          (f"M_J = (4π/3) ρ r³: r = λ_J/2 → {num(mh)} M☉; r = λ_J → {num(mf)} M☉.", VNC(f"M_J = (4π/3) ρ r³: r = λ_J/2 → {num(mh)} M☉; r = λ_J → {num(mf)} M☉."))]
    add("jeans", "L2", "jl", (en, vi), dict(n=n, T=T, mu=mu), [F("cs", ("sound speed", "tốc độ âm"), "km/s", [c / 1e5]), F("lj", ("Jeans length", "độ dài Jeans"), "pc", [L / PC, Ls / PC]), F("mj", ("Jeans mass", "khối lượng Jeans"), "M☉", [mh, mf, ms])], st, 2)

# ---- 3 inverse free-fall: density for a given time
for t in (0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 8.0, 10.0):
    ts = t * MYR; rho_a = 3 * math.pi / (32 * G * ts ** 2)
    rho_b = brentq(lambda r: tff_full_a(r) - ts, 1e-28, 1e-12, xtol=1e-40, rtol=1e-13); chk("inv", rho_a, rho_b)
    n_ex = rho_a / (2.33 * MH); n_sl = 1 / (G * ts ** 2) / (2.33 * MH)
    en = f"A cloud must collapse in {t:g} Myr. What number density n (cm⁻³, μ = 2.33) does it need? (Exact form, or the slide form 1/√(Gρ).)"
    vi = f"Một đám mây phải sụp đổ trong {str(t).replace('.', ',')} triệu năm. Nó cần mật độ số hạt n (cm⁻³, μ = 2,33) bằng bao nhiêu? (Dạng chính xác, hoặc dạng slide 1/√(Gρ).)"
    st = [("Invert the formula: ρ = 3π/(32 G t²) (exact) or ρ = 1/(G t²) (slide).", "Đảo công thức: ρ = 3π/(32 G t²) (chính xác) hoặc ρ = 1/(G t²) (slide)."), (f"t = {t:g} Myr = {num(ts)} s → ρ = {num(rho_a)} g/cm³ (exact).", VNC(f"t = {t:g} triệu năm = {num(ts)} s → ρ = {num(rho_a)} g/cm³ (chính xác).")),
          (f"n = ρ/(μ m_H) = {num(n_ex)} cm⁻³ (exact); {num(n_sl)} cm⁻³ (slide form).", VNC(f"n = ρ/(μ m_H) = {num(n_ex)} cm⁻³ (chính xác); {num(n_sl)} cm⁻³ (dạng slide)."))]
    add("tffinv", "L2", "tff", (en, vi), dict(t=t), [F("n", ("number density", "mật độ số hạt"), "cm⁻³", [n_ex, n_sl])], st, 2)

# ---- 4 spin-up (L2 p14)
for R1, R2 in [(1e4, 1e3), (1e4, 100), (5e3, 500), (1e4, 10), (2e4, 200), (1e4, 1), (3e3, 300), (1e4, 2e3), (1e5, 1e4), (1e4, 50), (8e3, 80), (1e4, 5e3), (2e3, 20), (1e5, 1e3)]:
    f_a = (R1 / R2) ** 2
    M = 1.0; w1 = 1.0; I1 = 0.4 * M * R1 ** 2; Lm = I1 * w1; w2 = Lm / (0.4 * M * R2 ** 2); f_b = chk("spin", f_a, w2 / w1)
    en = f"A rotating core shrinks from {p10(R1)} AU to {p10(R2)} AU. By what factor does its spin rate increase if angular momentum is conserved?"
    vi = f"Một lõi quay co lại từ {p10(R1)} AU còn {p10(R2)} AU. Tốc độ quay tăng bao nhiêu lần nếu mômen động lượng được bảo toàn?"
    st = [("I ω = const, I ∝ R², so ω₂/ω₁ = (R₁/R₂)².", "I ω = hằng số, I ∝ R², nên ω₂/ω₁ = (R₁/R₂)²."), (f"({p10(R1)}/{p10(R2)})² = {num(f_a)}.", VNC(f"({p10(R1)}/{p10(R2)})² = {num(f_a)}.")), ("Real cores shed angular momentum (disk, jets), so the real factor is smaller.", "Lõi thật mất mômen động lượng (đĩa, jet), nên hệ số thật nhỏ hơn.")]
    add("spin", "L2", "spin", (en, vi), dict(R1=R1, R2=R2), [F("f", ("factor", "hệ số"), "×", [f_a])], st)

# ---- 5 age from D/P (L3 p37)
for Th, dp in [(1.25, 0.25), (1.25, 0.5), (1.25, 1), (1.25, 2), (1.25, 3), (1.25, 5), (1.25, 7), (1.25, 11.8), (0.7, 1.0), (0.7, 3), (4.47, 0.5), (4.47, 1.0), (14.0, 0.2), (10.0, 7)]:
    t_a = Th * math.log2(1 + dp); t_b = brentq(lambda t: (1 - 2 ** (-t / Th)) / 2 ** (-t / Th) - dp, 0, 200 * Th); chk("age", t_a, t_b)
    en = f"A rock has {dp:g} daughter atoms for every parent atom. The isotope has a half-life of {Th:g} Gyr. How old is the rock (Gyr)? (No daughter at the start.)"
    vi = f"Một đá có {str(dp).replace('.', ',')} nguyên tử con cho mỗi nguyên tử mẹ. Đồng vị có chu kỳ bán rã {str(Th).replace('.', ',')} tỉ năm. Đá bao nhiêu tuổi (tỉ năm)? (Ban đầu không có nguyên tử con.)"
    st = [("D/P = 2^{t/T½} − 1, so t = T½ log₂(1 + D/P).", "D/P = 2^{t/T½} − 1, nên t = T½ log₂(1 + D/P)."), (f"t = {Th:g} × log₂({1 + dp:g}) = {Th:g} × {num(math.log2(1 + dp))} = {num(t_a)} Gyr ({num(t_a / Th)} half-lives).", VNC(f"t = {Th:g} × log₂({1 + dp:g}) = {Th:g} × {num(math.log2(1 + dp))} = {num(t_a)} tỉ năm ({num(t_a / Th)} chu kỳ bán rã)."))]
    add("age", "L3", "age", (en, vi), dict(Th=Th, DP=dp), [F("t", ("age", "tuổi"), "Gyr", [t_a])], st)

# ---- 6 parent fraction left
for Th, t in [(1.25, 0.5), (1.25, 1), (1.25, 2), (1.25, 3.75), (1.25, 4.6), (1.25, 6), (1.25, 10), (0.7, 2), (0.7, 3.5), (4.47, 4.6), (4.47, 9), (14.0, 4.6), (5.0, 12.5), (1.25, 0.1)]:
    f_a = 100 * 2 ** (-t / Th); s = solve_ivp(lambda tt, y: [-math.log(2) / Th * y[0]], [0, t], [1.0], rtol=1e-12, atol=1e-14); f_b = 100 * s.y[0][-1]; chk("frac", f_a, f_b, 1e-6)
    en = f"An isotope has a half-life of {Th:g} Gyr. What percentage of the parent atoms is left after {t:g} Gyr?"
    vi = f"Một đồng vị có chu kỳ bán rã {str(Th).replace('.', ',')} tỉ năm. Còn lại bao nhiêu phần trăm nguyên tử mẹ sau {str(t).replace('.', ',')} tỉ năm?"
    st = [("N/N₀ = 2^{−t/T½}.", "N/N₀ = 2^{−t/T½}."), (f"t/T½ = {t:g}/{Th:g} = {num(t / Th)}; 2^(−{num(t / Th)}) = {num(f_a / 100)} → {num(f_a)} %.", VNC(f"t/T½ = {t:g}/{Th:g} = {num(t / Th)}; 2^(−{num(t / Th)}) = {num(f_a / 100)} → {num(f_a)} %."))]
    add("frac", "L3", "dec", (en, vi), dict(Th=Th, t=t), [F("f", ("fraction left", "phần còn lại"), "%", [f_a])], st)

# ---- 7 light: wavelength / energy / frequency (L1 p2-3, p22-23)
LIGHT = [("lam", 0.21, "21 cm"), ("lam", 656e-9, "656 nm (Hα, L1 p22)"), ("lam", 500e-9, "500 nm"), ("lam", 10e-6, "10 µm"), ("lam", 8e-6, "8 µm (L1 p9)"), ("lam", 250e-6, "250 µm (Herschel, L1 p9)"), ("lam", 1.25e-3, "1.25 mm (IRAM, L2 p3)"),
         ("lam", 1.3e-3, "1.3 mm (EHT, L1 p23)"), ("lam", 1e-9, "1 nm (X-ray, L1 p3)"), ("lam", 1e-10, "0.1 nm"), ("lam", 1e-12, "10⁻¹² m (gamma, L1 p2)"), ("lam", 1e3, "10³ m (radio, L1 p2)"), ("E", 511e3, "511 keV (L1 p22)"), ("E", 1.809e6, "1.809 MeV (L1 p22)")]
for kind, v, lab in LIGHT:
    if kind == "lam":
        nu_a = C.c / v; nu_b = 1 / (v / C.c); E_a = C.h * nu_a / C.e; E_b = 1239.841984 / (v * 1e9); chk("light E", E_a, E_b, 1e-4)
        en = f"A source is observed at {lab}. Find the frequency (Hz) and the photon energy (eV)."
        vi = f"Một nguồn được quan sát ở {lab}. Tìm tần số (Hz) và năng lượng photon (eV)."
        st = [(f"ν = c/λ = 2.998×10⁸ / {num(v)} = {num(nu_a)} Hz.", VNC(f"ν = c/λ = 2,998×10⁸ / {num(v)} = {num(nu_a)} Hz.")), (f"E = h ν = hc/λ = 1239.8 eV nm / {num(v * 1e9)} nm = {num(E_a)} eV.", VNC(f"E = h ν = hc/λ = 1239,8 eV nm / {num(v * 1e9)} nm = {num(E_a)} eV."))]
        fields = [F("nu", ("frequency", "tần số"), "Hz", [nu_a]), F("E", ("photon energy", "năng lượng photon"), "eV", [E_a])]
    else:
        lam_a = C.h * C.c / (v * C.e); lam_b = 1239.841984 / v * 1e-9; chk("light lam", lam_a, lam_b, 1e-4); nu_a = C.c / lam_a
        en = f"A gamma-ray photon has an energy of {lab}. Find its wavelength (m) and frequency (Hz)."
        vi = f"Một photon gamma có năng lượng {lab}. Tìm bước sóng (m) và tần số (Hz)."
        st = [(f"λ = hc/E = 1239.8 eV nm / {num(v)} eV = {num(lam_a * 1e9)} nm = {num(lam_a)} m.", VNC(f"λ = hc/E = 1239,8 eV nm / {num(v)} eV = {num(lam_a * 1e9)} nm = {num(lam_a)} m.")), (f"ν = c/λ = {num(nu_a)} Hz.", VNC(f"ν = c/λ = {num(nu_a)} Hz."))]
        fields = [F("lam", ("wavelength", "bước sóng"), "m", [lam_a]), F("nu", ("frequency", "tần số"), "Hz", [nu_a])]
    add("light", "L1", "c" if kind == "lam" else "E", (en, vi), dict(kind=kind, v=v), fields, st)

# ---- 8 equilibrium temperature (L3 p15-19)
for d, lab in [(0.39, "Mercury, 0.39 AU"), (0.72, "Venus, 0.72 AU"), (1.0, "1 AU"), (1.52, "Mars, 1.52 AU"), (2.7, "2.7 AU (asteroid belt)"), (3.4, "3.4 AU"), (5.2, "Jupiter, 5.2 AU"), (9.6, "Saturn, 9.6 AU"), (19.2, "Uranus, 19.2 AU"), (30.0, "Neptune, 30 AU"), (40.0, "40 AU (Kuiper belt)"), (10.0, "10 AU"), (2.0, "2 AU"), (50.0, "50 AU")]:
    T_a = teq_a(d); T_b = chk("teq", teq_b(d), T_a, 1e-6)
    vl = {"Mercury, 0.39 AU": "Thủy tinh, 0,39 AU", "Venus, 0.72 AU": "Kim tinh, 0,72 AU", "Mars, 1.52 AU": "Hỏa tinh, 1,52 AU", "2.7 AU (asteroid belt)": "2,7 AU (vành đai tiểu hành tinh)", "Jupiter, 5.2 AU": "Mộc tinh, 5,2 AU", "Saturn, 9.6 AU": "Thổ tinh, 9,6 AU", "Uranus, 19.2 AU": "Thiên Vương tinh, 19,2 AU", "Neptune, 30 AU": "Hải Vương tinh, 30 AU", "40 AU (Kuiper belt)": "40 AU (vành đai Kuiper)"}.get(lab, lab.replace(".", ","))
    en = f"Using the blackbody equilibrium temperature of a dark body heated by the Sun (no albedo, no greenhouse), find T at {lab} (K)."
    vi = f"Dùng nhiệt độ cân bằng vật đen của một vật tối được Mặt Trời nung (không albedo, không hiệu ứng nhà kính), tìm T tại {vl} (K)."
    st = [("T = (L☉/(16 π σ d²))^¼ = 278.3 K (d/AU)^(−1/2).", "T = (L☉/(16 π σ d²))^¼ = 278,3 K (d/AU)^(−1/2)."), (f"T = 278.3 / √{d:g} = {num(T_a)} K.", VNC(f"T = 278,3 / √{d:g} = {num(T_a)} K.")), ("A trend, not the temperature of the young disk.", "Chỉ là xu hướng, không phải nhiệt độ của đĩa trẻ.")]
    add("teq", "L3", "teq", (en, vi), dict(d=d), [F("T", ("temperature", "nhiệt độ"), "K", [T_a])], st)

# ---- 9 scaling of the Jeans mass
for (n1, T1, n2, T2) in [(1e3, 30, 1e4, 30), (1e4, 30, 1e4, 50), (1e3, 30, 1e3, 50), (1e4, 10, 1e4, 40), (1e3, 100, 1e5, 10), (1e4, 20, 1e6, 20), (1e2, 100, 1e4, 10), (1e3, 30, 1e2, 30), (1e4, 50, 1e4, 12.5), (1e5, 10, 1e3, 10), (1e3, 10, 1e3, 90), (1e4, 30, 1e2, 300), (1e6, 10, 1e4, 10), (1e3, 50, 1e3, 30)]:
    ra = (T2 / T1) ** 1.5 * (n2 / n1) ** -0.5
    mu = 2.33; rb = msph(lj_a(cs_a(T2, mu), rho_(n2, mu)) / 2, rho_(n2, mu)) / msph(lj_a(cs_a(T1, mu), rho_(n1, mu)) / 2, rho_(n1, mu)); chk("scale", ra, rb, 1e-9)
    en = f"The Jeans mass of a cloud with n = {p10(n1)} cm⁻³ and T = {T1:g} K is M₁. What is the ratio M₂/M₁ for n = {p10(n2)} cm⁻³ and T = {T2:g} K? (Same μ.)"
    vi = f"Khối lượng Jeans của một đám mây có n = {p10(n1)} cm⁻³ và T = {T1:g} K là M₁. Tỉ số M₂/M₁ với n = {p10(n2)} cm⁻³ và T = {T2:g} K là bao nhiêu? (Cùng μ.)"
    st = [("M_J ∝ T^{3/2} ρ^{−1/2}, and ρ ∝ n.", "M_J ∝ T^{3/2} ρ^{−1/2}, và ρ ∝ n."), (f"M₂/M₁ = ({T2:g}/{T1:g})^1.5 × ({p10(n2)}/{p10(n1)})^−0.5 = {num((T2 / T1) ** 1.5)} × {num((n2 / n1) ** -0.5)} = {num(ra)}.", VNC(f"M₂/M₁ = ({T2:g}/{T1:g})^1,5 × ({p10(n2)}/{p10(n1)})^−0,5 = {num((T2 / T1) ** 1.5)} × {num((n2 / n1) ** -0.5)} = {num(ra)}."))]
    add("scale", "L2", "scal", (en, vi), dict(n1=n1, T1=T1, n2=n2, T2=T2), [F("r", ("mass ratio", "tỉ số khối lượng"), "×", [ra])], st, 2)

TYPES = [("tff", "Free-fall time", "Thời gian rơi tự do", "L2"), ("jeans", "Jeans length and mass", "Độ dài và khối lượng Jeans", "L2"), ("tffinv", "Density from a collapse time", "Mật độ từ thời gian sụp đổ", "L2"), ("scale", "Scaling of the Jeans mass", "Quy luật tỉ lệ của khối lượng Jeans", "L2"),
         ("spin", "Spin-up", "Quay nhanh dần", "L2"), ("age", "Age from daughter/parent", "Tuổi từ tỉ lệ con/mẹ", "L3"), ("frac", "Fraction left", "Phần còn lại", "L3"), ("teq", "Temperature and distance", "Nhiệt độ và khoảng cách", "L3"), ("light", "Wavelength, frequency, energy", "Bước sóng, tần số, năng lượng", "L1")]
out = dict(types=[dict(id=a, en=b, vi=c, lec=d) for a, b, c, d in TYPES], problems=P)
json.dump(out, open(ROOT / "data" / "problems.json", "w"), indent=0, ensure_ascii=False, default=float)
js = [dict(id=p["id"], t=p["type"], l=p["lec"], e=p["eq"], q=dict(en=p["q"][0], vi=p["q"][1]), f=[dict(k=f["k"], l=dict(en=f["label"][0], vi=f["label"][1]), u=f["unit"], a=f["accept"]) for f in p["fields"]], s=[dict(en=s[0], vi=s[1]) for s in p["steps"]], lv=p["level"]) for p in P]
(ROOT / "site" / "data").mkdir(parents=True, exist_ok=True)
(ROOT / "site" / "data" / "problems.js").write_text("window.PTYPES=" + json.dumps(out["types"], ensure_ascii=False) + ";window.PROBLEMS=" + json.dumps(js, ensure_ascii=False, default=float) + ";", encoding="utf-8")
if bad: print("FAILS:", bad); sys.exit(1)
from collections import Counter
print("FAILS: none |", len(P), "problems", dict(Counter(p["type"] for p in P)))
