"""Bước 3b - Tải trực tiếp file SPOC (lc, tp, báo cáo DV) từ kho tệp tĩnh https://archive.stsci.edu/missions/tess/ khi API MAST (astroquery/lightkurve) không phản hồi.
Chạy: python 03b_fetch_static.py <TIC> <sector> [<sector> ...]   ->  data/mast_cache/static/<TIC>/
Đường dẫn: tid/sSSSS/<tic16[0:4]>/<tic16[4:8]>/<tic16[8:12]>/<tic16[12:16]>/ ; tên file lấy từ danh sách thư mục."""
import pathlib, re, sys, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[1]
H = {"User-Agent": "course-fetch/1.0"}
def get(u, t=120):
    return urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=t).read()
tic = int(sys.argv[1]); secs = [int(x) for x in sys.argv[2:]]
t16 = f"{tic:016d}"
for s in secs:
    base = f"https://archive.stsci.edu/missions/tess/tid/s{s:04d}/{t16[0:4]}/{t16[4:8]}/{t16[8:12]}/{t16[12:16]}/"
    names = re.findall(r'href="([^"/][^"]*)"', get(base).decode())
    want = [n for n in names if n.endswith(("_lc.fits", "_tp.fits")) or n.endswith("_dvr.pdf")]
    d = ROOT / "data" / "mast_cache" / "static" / str(tic); d.mkdir(parents=True, exist_ok=True)
    for n in want:
        p = d / n
        if not p.exists():
            p.write_bytes(get(base + n)); print("tải", n, p.stat().st_size // 1024, "KB", flush=True)
