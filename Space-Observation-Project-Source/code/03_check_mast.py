"""Bước 3 - Shortlist theo từng ngách rồi hỏi MAST: sao có bao nhiêu sector SPOC 2-phút?

Ra: data/shortlist_mast.csv
"""
import pathlib
import warnings

import pandas as pd
import lightkurve as lk

warnings.filterwarnings("ignore")
ROOT = pathlib.Path(__file__).resolve().parents[1]
c = pd.read_csv(ROOT / "data" / "candidates_grouped.csv")

# Lấy top theo S/N trong mỗi giá trị của mỗi trục nhóm (ít nhất 5 mỗi ngách)
axes = ["g_size", "g_period", "g_teq", "g_star", "g_dist", "g_sky", "g_system", "g_origin"]
keep = set()
for ax in axes:
    for _, sub in c.groupby(ax):
        keep.update(sub.sort_values("snr_est", ascending=False).head(6).index)
# thêm các hành tinh hiếm theo trục kích thước nhỏ / nhiệt độ thấp / USP
for key in ["Earth-size", "Super-Earth"]:
    keep.update(c[c.g_size == key].sort_values("snr_est", ascending=False).head(10).index)
short = c.loc[sorted(keep)].copy()
print("Shortlist:", len(short))

rows = []
for i, r in enumerate(short.itertuples(), 1):
    try:
        res = lk.search_lightcurve(f"TIC {int(r.tic_num)}", mission="TESS", author="SPOC", exptime=120)
        secs = sorted({int(str(m).split()[-1]) for m in res.table["mission"]}) if len(res) else []
    except Exception as e:
        secs = []
        print("  lỗi", r.pl_name, e)
    rows.append({"pl_name": r.pl_name, "n_sectors": len(secs), "sectors": " ".join(map(str, secs))})
    print(f"[{i}/{len(short)}] {r.pl_name:16s} sectors={len(secs)}", flush=True)

m = pd.DataFrame(rows)
out = short.merge(m, on="pl_name")
out.to_csv(ROOT / "data" / "shortlist_mast.csv", index=False)
print("\nCó dữ liệu SPOC 2-min:", (out.n_sectors > 0).sum(), "/", len(out))
