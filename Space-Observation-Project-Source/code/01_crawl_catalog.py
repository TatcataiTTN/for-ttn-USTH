"""Bước 1 - Crawl catalog hành tinh transit từ NASA Exoplanet Archive (TAP, bảng pscomppars).

Chạy:  python code/01_crawl_catalog.py
Ra:    data/raw/pscomppars_transit_all.csv   (mọi hành tinh có transit)
       data/raw/tess_catalog.csv             (tập con có TIC ID + Tmag, ứng viên cho TESS)
"""
import io
import pathlib
import sys

import pandas as pd
import requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)

URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
COLS = [
    "pl_name", "hostname", "tic_id", "disc_facility", "disc_year", "discoverymethod",
    "pl_orbper", "pl_orbpererr1", "pl_rade", "pl_radeerr1", "pl_radj", "pl_bmasse",
    "pl_orbsmax", "pl_ratror", "pl_trandep", "pl_trandur", "pl_imppar", "pl_orbincl",
    "pl_eqt", "pl_insol", "pl_orbeccen", "pl_tranmid",
    "st_rad", "st_raderr1", "st_mass", "st_teff", "st_logg", "st_spectype",
    "sy_dist", "sy_vmag", "sy_tmag", "sy_pnum", "ra", "dec", "elon", "elat", "glon", "glat",
]


def tap(query: str) -> pd.DataFrame:
    r = requests.get(URL, params={"query": query, "format": "csv"}, timeout=120)
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text))


def main() -> None:
    q = f"select {','.join(COLS)} from pscomppars where tran_flag=1"
    try:
        df = tap(q)
    except Exception as exc:  # cột nào đó không tồn tại -> thử lại từng cột
        print("Truy vấn đầy đủ lỗi:", exc, file=sys.stderr)
        ok = []
        for c in COLS:
            try:
                tap(f"select top 1 {c} from pscomppars")
                ok.append(c)
            except Exception:
                print("  bỏ cột", c)
        df = tap(f"select {','.join(ok)} from pscomppars where tran_flag=1")
    df.to_csv(OUT / "pscomppars_transit_all.csv", index=False)
    print("Tổng hành tinh transit:", len(df))

    tess = df[df["tic_id"].notna() & df["sy_tmag"].notna()].copy()
    tess["tic_num"] = tess["tic_id"].str.replace("TIC ", "", regex=False).astype("int64")
    tess.to_csv(OUT / "tess_catalog.csv", index=False)
    print("Có TIC ID + Tmag:", len(tess))
    print("Phát hiện bởi TESS:", tess["disc_facility"].str.contains("TESS", na=False).sum())
    print(tess[["pl_orbper", "pl_rade", "sy_dist", "sy_tmag"]].describe().round(2))


if __name__ == "__main__":
    main()
