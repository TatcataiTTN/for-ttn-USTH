# -*- coding: utf-8 -*-
"""Bước 28 - Quỹ đạo của TESS vẽ theo số trong Ricker+2015 (Sec 6, Table 2) và các phép tính kiểm tra bằng định luật Kepler.
Số đầu vào từ bài báo: cận điểm 17 R_E, viễn điểm 59 R_E, chu kỳ 13.7 d, Mặt Trăng dẫn hoặc theo sau viễn điểm khoảng 90 độ, bay trên quỹ đạo địa tĩnh (6.6 R_E).
Hằng số chuẩn (không lấy từ bài báo): GM_Earth = 398600.4418 km3/s2, R_E = 6378.137 km, khoảng cách trung bình Mặt Trăng 384400 km, chu kỳ thiên văn của Mặt Trăng 27.32 d,
tốc độ quay xích đạo 0.4651 km/s. Ra: results/tess_orbit_numbers.json, figures/paper/tess_orbit.png. Hình là sơ đồ nhìn từ trên xuống, không thể hiện độ nghiêng."""
import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
GM, RE, DMOON, PMOON, VEQ = 398600.4418, 6378.137, 384400.0, 27.32, 0.4651
rp, ra = 17.0, 59.0                                   # R_E, Ricker+2015 Sec 6
a = 0.5 * (rp + ra); e = (ra - rp) / (ra + rp)
P_kepler = 2 * np.pi * np.sqrt((a * RE) ** 3 / GM) / 86400
# Δv từ quỹ đạo tròn thấp 300 km lên quỹ đạo có viễn điểm 400000 km (mô tả trong Ricker+2015 Sec 6: "apogee is raised to 400,000 km")
r0 = RE + 300; r_ap = 400000.0; a_t = 0.5 * (r0 + r_ap)
dv = np.sqrt(GM * (2 / r0 - 1 / a_t)) - np.sqrt(GM / r0)
rot = lambda lat: VEQ * np.cos(np.radians(lat))
N = dict(a_RE=a, ecc=e, period_from_kepler_d=P_kepler, period_paper_d=13.7, moon_RE=DMOON / RE, two_periods_d=2 * 13.7, moon_sidereal_d=PMOON,
         dv_leo300_to_apogee400000_kms=dv, rot_kms_cape_28p5=rot(28.5), rot_kms_vn_south_8p6=rot(8.6), rot_kms_vn_north_23p4=rot(23.4),
         rot_gain_ms_vn_south_vs_cape=1000 * (rot(8.6) - rot(28.5)), circ_leo300_kms=np.sqrt(GM / r0))
json.dump(N, open(ROOT / "results" / "tess_orbit_numbers.json", "w"), indent=1)

th = np.linspace(0, 2 * np.pi, 800); r = a * (1 - e ** 2) / (1 + e * np.cos(th))
plt.rcParams.update({"font.size": 15, "figure.dpi": 100, "savefig.dpi": 100})
fig, ax = plt.subplots(figsize=(5.4, 5.4), constrained_layout=True)
NAVY, RED, GREY = "#273896", "#ED1C24", "#6b7280"
ax.plot(N["moon_RE"] * np.cos(th), N["moon_RE"] * np.sin(th), color=GREY, lw=1.6, ls="--")
ax.plot(6.6 * np.cos(th), 6.6 * np.sin(th), color=GREY, lw=1.2, ls=":")
ax.plot(r * np.cos(th), r * np.sin(th), color=NAVY, lw=2.6)
# 4 giờ quanh cận điểm (±2 h) bằng phương trình Kepler: đoạn đậm là thời gian tải dữ liệu
M = 2 * np.pi * np.linspace(-2, 2, 40) / 24 / 13.7; E = M.copy()
for _ in range(30): E = M + e * np.sin(E)
nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2)); rr = a * (1 - e * np.cos(E))
ax.plot(rr * np.cos(nu), rr * np.sin(nu), color=RED, lw=6, solid_capstyle="round")
ax.add_patch(plt.Circle((0, 0), 1.0, color="#4a90d9")); ax.plot([N["moon_RE"] * np.cos(np.pi / 2)], [N["moon_RE"] * np.sin(np.pi / 2)], "o", color="#8a8f9c", ms=11)
ax.text(0, -11, "Earth", fontsize=14.5, ha="center")
ax.annotate("perigee 17 R$_\\oplus$", (rp, 0), xytext=(28, -22), fontsize=14.5, arrowprops=dict(arrowstyle="-", color=GREY))
ax.annotate("apogee 59 R$_\\oplus$", (-ra, 0), xytext=(-60, 10), fontsize=14.5, arrowprops=dict(arrowstyle="-", color=GREY))
ax.text(2, N["moon_RE"] + 1.5, "Moon", fontsize=14.5, ha="left"); ax.text(-62, 52, "Moon orbit\n60 R$_\\oplus$", fontsize=14.5, ha="left", va="top", color=GREY)
ax.text(30, 36, "13.7 d orbit", color=NAVY, fontsize=14.5, ha="left"); ax.text(24, -14, "4 h downlink", color=RED, fontsize=14.5, ha="left", va="top") if False else None
ax.text(5, 9, "GEO 6.6", fontsize=14.5, color=GREY, ha="left"); ax.text(18, -40, "red: 4 h around\nperigee (downlink)", color=RED, fontsize=14.5, ha="left", va="top")
ax.set_aspect("equal"); ax.set_xlim(-66, 66); ax.set_ylim(-66, 66); ax.set_xlabel("distance in Earth radii"); ax.set_yticks([-60, -30, 0, 30, 60]); ax.set_xticks([-60, -30, 0, 30, 60]); ax.grid(alpha=0.25)
fig.savefig(ROOT / "figures" / "paper" / "tess_orbit.png"); plt.close(fig)
print(json.dumps({k: round(float(v), 3) for k, v in N.items()}, indent=0))
