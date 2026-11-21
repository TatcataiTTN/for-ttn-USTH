"""Bước 7 - Xuất dữ liệu cho trang demo (chạy offline trong trình duyệt).

Đọc: data/lightcurves/<slug>.npz (đã làm phẳng), results/<slug>/result.json, data/selected.txt, data/candidates_grouped.csv
Ra:  slides/demo/data/<slug>.js  (window.PLANETS[slug] = {...})  +  slides/demo/data/index.js
Dùng .js thay .json để mở trang bằng file:// không bị chặn CORS.
"""
import json
import pathlib
import re

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "slides" / "demo" / "data"
OUT.mkdir(parents=True, exist_ok=True)
BIN_MIN = 6.0   # phút

cat = pd.read_csv(ROOT / "data" / "raw" / "tess_catalog.csv")
grp = pd.read_csv(ROOT / "data" / "candidates_grouped.csv").set_index("pl_name")
names = [l.strip() for l in open(ROOT / "data" / "selected.txt") if l.strip()]


def slug(n):
    return re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_")


def binned(t, f, minutes):
    w = minutes / 1440
    k = np.floor((t - t.min()) / w).astype(int)
    u, inv = np.unique(k, return_inverse=True)
    n = np.bincount(inv)
    return np.bincount(inv, t) / n, np.bincount(inv, f) / n


index = []
for i, name in enumerate(names, 1):
    s = slug(name)
    res = json.load(open(ROOT / "results" / s / "result.json"))
    lc = np.load(ROOT / "data" / "lightcurves" / f"{s}.npz")
    tb, fb = binned(lc["t"], lc["f"], BIN_MIN)
    row = cat[cat.pl_name == name].iloc[0]
    g = grp.loc[name] if name in grp.index else None
    d = dict(
        num=i, name=name, tic=int(row.tic_num), tmag=float(row.sy_tmag), dist_pc=float(row.sy_dist),
        teff=float(row.st_teff), rstar=float(row.st_rad), rstar_err=float(row.st_raderr1) if pd.notna(row.st_raderr1) else 0.0,
        elat=float(row.elat), sectors=res["sectors_used"],
        groups={k: str(g[k]) for k in ["g_size", "g_period", "g_teq", "g_star", "g_dist", "g_sky", "g_system", "g_origin"]} if g is not None else {},
        catalog=res["catalog"], bls=res["bls"], fit=res["fit"], rp_rearth=res["rp_rearth"], rp_rearth_err=res["rp_rearth_err"],
        t=[round(float(x), 5) for x in tb], f=[int(round((x - 1) * 1e6)) for x in fb],   # ppm
    )
    (OUT / f"{s}.js").write_text(f"window.PLANETS=window.PLANETS||{{}};window.PLANETS[{json.dumps(s)}]={json.dumps(d, separators=(',', ':'))};\n")
    index.append(dict(slug=s, name=name, num=i))
    print(f"{i:2d} {name:14s} {len(tb):6d} điểm  {(OUT / (s + '.js')).stat().st_size / 1e3:.0f} kB")
(OUT / "index.js").write_text("window.INDEX=" + json.dumps(index) + ";\n")
