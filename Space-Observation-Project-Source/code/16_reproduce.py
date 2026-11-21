"""Bước 16 - Tìm lại CHÍNH XÁC các con số từ dataset gốc và ghi cách lấy lại.

1. Hỏi lại NASA Exoplanet Archive (TAP, trực tiếp) giá trị catalog của 11 hành tinh, so với bản CSV đã tải (data/raw/tess_catalog.csv).
2. Liệt kê đúng các file SPOC (sector, tên file, kích thước, md5, URL tải) dùng cho từng hành tinh.
3. Gom kết quả đo (result.json) thành một bảng.
Ra: results/results_table.csv, results/catalog_recheck.csv, results/data_manifest.csv  (REPRODUCE.md do 17_write_reproduce.py viết)
"""
import hashlib
import io
import json
import pathlib
import re
import sys
import urllib.parse
import urllib.request

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import transit_pipeline as tp

ROOT = tp.ROOT
slug = lambda n: re.sub(r"[^A-Za-z0-9]+", "_", n).strip("_")
names = [l.strip() for l in open(ROOT / "data" / "selected.txt") if l.strip()] + ["pi Men c"]
stress = [l.strip() for l in open(ROOT / "data" / "stress_tests.txt") if l.strip()]
allnames = names + stress

# ---- 1. catalog trực tiếp từ NASA TAP
cols = "pl_name,pl_orbper,pl_rade,pl_ratror,st_rad,tic_id,sy_tmag,pl_trandur,pl_bmasse"
q = "select " + cols + " from pscomppars where pl_name in (" + ",".join("'" + n + "'" for n in allnames) + ")"
url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?" + urllib.parse.urlencode({"query": q, "format": "csv"})
live = pd.read_csv(io.BytesIO(urllib.request.urlopen(url, timeout=90).read())).set_index("pl_name")
local = pd.read_csv(ROOT / "data" / "raw" / "tess_catalog.csv").set_index("pl_name")
rows = []
for n in allnames:
    for c in ("pl_orbper", "pl_rade", "pl_ratror", "st_rad"):
        a, b = local.loc[n, c], live.loc[n, c]
        rows.append(dict(planet=n, column=c, local_csv=a, live_tap=b, same=bool(abs(a - b) <= 1e-9 * max(1, abs(b)))))
chk = pd.DataFrame(rows)
chk.to_csv(ROOT / "results" / "catalog_recheck.csv", index=False)
print("catalog: %d/%d giá trị trùng giữa CSV đã tải và NASA TAP hôm nay" % (chk.same.sum(), len(chk)))
print(chk[~chk.same].to_string(index=False) if (~chk.same).any() else "  không có khác biệt")
print("TAP URL (mở trong trình duyệt hoặc curl):\n  " + url)

# ---- 2. file SPOC đã dùng
man = []
for n in names:
    r = json.load(open(ROOT / "results" / slug(n) / "result.json"))
    t16 = f"{int(r['tic']):016d}"
    for f in sorted(tp.CACHE.rglob(f"*-{t16}-*_lc.fits")):
        sec = int(re.search(r"-s(\d{4})-", f.name).group(1))
        if sec not in r["sectors_used"]:
            continue
        md5 = hashlib.md5(f.read_bytes()).hexdigest()
        u = f"https://archive.stsci.edu/missions/tess/tid/s{sec:04d}/{t16[0:4]}/{t16[4:8]}/{t16[8:12]}/{t16[12:16]}/{f.name}"
        man.append(dict(planet=n, tic=r["tic"], sector=sec, file=f.name, size_kb=f.stat().st_size // 1024, md5=md5, url=u))
man = pd.DataFrame(man).drop_duplicates(["planet", "file"])
man.to_csv(ROOT / "results" / "data_manifest.csv", index=False)
print("manifest:", len(man), "file SPOC cho", man.planet.nunique(), "hành tinh")

# ---- 3. bảng kết quả
out = []
for n in allnames:
    r = json.load(open(ROOT / "results" / slug(n) / "result.json")); f = r["fit"]
    out.append(dict(planet=n, tic=r["tic"], mode=r["mode"], sectors=" ".join(map(str, r["sectors_used"])), n_transits=f["n_transits"],
                    period_d=f["period"], period_err=f["period_err"], t0_btjd=f["t0"], ror=f["ror"], ror_err_total=f["ror_err"],
                    ror_err_mcmc=r["ror_err_stat"], ror_err_detrend=r["ror_err_sys"], b=f["b"], a_over_rs=f["a_rs"],
                    rstar_rsun=r["rstar_rsun"], rp_rearth=r["rp_rearth"], rp_rearth_err=r["rp_rearth_err"],
                    cat_period=r["catalog"]["period"], cat_rade=r["catalog"]["rade"], delta_period_pct=r["delta_period_pct"], delta_radius_pct=r["delta_radius_pct"]))
pd.DataFrame(out).to_csv(ROOT / "results" / "results_table.csv", index=False)
print(pd.DataFrame(out)[["planet", "mode", "sectors", "n_transits", "period_d", "rp_rearth", "rp_rearth_err", "cat_rade", "delta_radius_pct"]].round(5).to_string(index=False))
