"""Bước 2 - Lọc ứng viên khả thi + gán nhóm theo nhiều trục.

Ra: data/candidates_grouped.csv  (pool ứng viên, mỗi dòng có nhãn nhóm theo 6 trục)
"""
import pathlib

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
cat = pd.read_csv(ROOT / "data" / "raw" / "tess_catalog.csv")

# ---- 1. Lọc: phải đo được bằng ánh sáng TESS 2-phút trong 1 sector -----------------
need = ["pl_orbper", "pl_rade", "st_rad", "pl_trandep", "pl_trandur", "sy_dist", "st_teff", "sy_tmag"]
c = cat.dropna(subset=need).copy()
c = c[(c.sy_tmag < 11.0)            # đủ sáng để có SPOC 2-min và nhiễu nhỏ
      & (c.pl_orbper < 15)          # >= 2 lần transit trong ~27 ngày của 1 sector
      & (c.pl_trandep > 0.05)]      # pl_trandep tính bằng %, lọc >= 500 ppm
c["depth_ppm_cat"] = c.pl_trandep * 1e4

# S/N gần đúng: nhiễu 1 giờ (CDPP) ~ 60 ppm * 10^(0.2*(Tmag-8)) -> thô nhưng đủ xếp hạng
cdpp1h = 60 * 10 ** (0.2 * (c.sy_tmag - 8))
n_tr = 27.4 / c.pl_orbper
c["snr_est"] = c.depth_ppm_cat / (cdpp1h / np.sqrt(c.pl_trandur)) * np.sqrt(n_tr)
c = c[c.snr_est > 12]               # đủ chắc để tự đo lại

# ---- 2. Nhóm theo 6 trục ---------------------------------------------------------
def size_group(r):
    if r < 1.25: return "Earth-size"
    if r < 2.0:  return "Super-Earth"
    if r < 4.0:  return "Sub-Neptune"
    if r < 8.0:  return "Neptune/Saturn"
    return "Jupiter-size"

def period_group(p):
    if p < 1.0:  return "USP (<1 d)"
    if p < 3.0:  return "Hot (1-3 d)"
    if p < 7.0:  return "Warm (3-7 d)"
    return "Cool (7-15 d)"

def teq_group(t):
    if pd.isna(t): return "n/a"
    if t > 2000: return "Ultra-hot (>2000 K)"
    if t > 1200: return "Hot (1200-2000 K)"
    if t > 500:  return "Warm (500-1200 K)"
    return "Temperate (<500 K)"

def star_group(t):
    if t < 3900: return "M dwarf"
    if t < 5200: return "K dwarf"
    if t < 6000: return "G (Sun-like)"
    return "F/hotter"

def dist_group(d):
    if d < 50:  return "Near (<50 pc)"
    if d < 150: return "Mid (50-150 pc)"
    return "Far (>150 pc)"

def sky_group(elat):
    a = abs(elat)
    if a > 78: return "CVZ (|β|>78°, ~1 yr coverage)"
    if a > 54: return "High (54-78°, many sectors)"
    return "Low (<54°, 1-2 sectors)"

c["g_size"] = c.pl_rade.map(size_group)
c["g_period"] = c.pl_orbper.map(period_group)
c["g_teq"] = c.pl_eqt.map(teq_group)
c["g_star"] = c.st_teff.map(star_group)
c["g_dist"] = c.sy_dist.map(dist_group)
c["g_sky"] = c.elat.map(sky_group)
c["g_hemi"] = np.where(c.dec >= 0, "Northern sky", "Southern sky")
c["g_system"] = np.where(c.sy_pnum > 1, "Multi-planet", "Single-planet")
c["g_origin"] = np.where(c.disc_facility.str.contains("TESS", na=False), "Found by TESS", "Known before TESS")

out = ROOT / "data" / "candidates_grouped.csv"
c.sort_values("snr_est", ascending=False).to_csv(out, index=False)
print("Pool ứng viên:", len(c))
for g in ["g_size", "g_period", "g_teq", "g_star", "g_dist", "g_sky", "g_hemi", "g_system", "g_origin"]:
    print(f"\n[{g}]"); print(c[g].value_counts().to_string())
