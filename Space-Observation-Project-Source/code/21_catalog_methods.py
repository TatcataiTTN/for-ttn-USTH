# -*- coding: utf-8 -*-
"""Bước 21 - Catalog (NASA pscomppars, bộ tham số mặc định) lấy từng giá trị từ bài nào? Ra:
  data/raw/catalog_methods.csv      mỗi hành tinh: phương pháp phát hiện, bài nguồn của chu kỳ, bán kính, Rp/R*, R*, sai số catalog
  data/literature/catalog_refs.csv  mỗi bài nguồn: bibcode, tác giả đầu, năm, tạp chí, tựa đề (tra Crossref, khớp tập/trang) - chỉ đọc tựa đề, không đọc toàn văn
Nguồn dữ liệu công khai (NASA Exoplanet Archive TAP, Crossref); không gửi thông tin cá nhân."""
import io
import json
import pathlib
import re
import time
import urllib.parse
import urllib.request

import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[1]
UA = {"User-Agent": "student-project-script"}
names = [l.strip() for l in open(ROOT / "data" / "selected.txt") if l.strip()] + ["pi Men c"]
cols = ("pl_name,discoverymethod,disc_facility,disc_year,disc_refname,"
        "pl_orbper,pl_orbpererr1,pl_orbpererr2,pl_orbper_reflink,"
        "pl_rade,pl_radeerr1,pl_radeerr2,pl_rade_reflink,"
        "pl_ratror,pl_ratrorerr1,pl_ratrorerr2,pl_ratror_reflink,"
        "pl_imppar,pl_imppar_reflink,pl_trandur,pl_trandur_reflink,"
        "st_rad,st_raderr1,st_raderr2,st_rad_reflink")
q = f"select {cols} from pscomppars where pl_name in ({','.join(repr(n) for n in names)})"
raw = urllib.request.urlopen(urllib.request.Request("https://exoplanetarchive.ipac.caltech.edu/TAP/sync?" + urllib.parse.urlencode({"format": "csv", "query": q}), headers=UA), timeout=90).read().decode()
df = pd.read_csv(io.StringIO(raw))


def bib(s):
    m = re.search(r"abs/([^/]+)/abstract", str(s)); return urllib.parse.unquote(m.group(1)) if m else ""


def label(s):
    m = re.search(r">([^<]+)</a>", str(s)); return re.sub(r"&([a-z])acute;", r"\1", m.group(1)).strip() if m else ""


for p in ("pl_orbper", "pl_rade", "pl_ratror", "pl_imppar", "pl_trandur", "st_rad"):
    df[p + "_ref"] = df[p + "_reflink"].map(label)
    df[p + "_bibcode"] = df[p + "_reflink"].map(bib)
df["disc_ref"] = df["disc_refname"].map(label)
df.drop(columns=[c for c in df.columns if c.endswith("_reflink") or c == "disc_refname"]).to_csv(ROOT / "data" / "raw" / "catalog_methods.csv", index=False)

# --- tra từng bài nguồn trên Crossref bằng (tác giả đầu, năm, tập, trang); chỉ nhận khi tập và trang khớp bibcode
codes = sorted({b for c in df.columns if c.endswith("_bibcode") for b in df[c].dropna() if b})
JOURNAL = {"ApJ": "Astrophysical Journal", "ApJS": "Astrophysical Journal Supplement", "AJ": "Astronomical Journal", "A&A": "Astronomy & Astrophysics",
           "MNRAS": "Monthly Notices", "NatAs": "Nature Astronomy"}
lab = {}
for c in [c for c in df.columns if c.endswith("_ref") and c != "disc_ref"]:
    for b, l in zip(df[c.replace("_ref", "_bibcode")], df[c]):
        if b: lab[b] = l
rows = []
for b in codes:       # bibcode ADS = năm(4) tạp chí(5) tập(4) ký hiệu(1) trang(4) chữ cái đầu(1)
    year, jr, vol, qual, pg = b[:4], b[4:9].strip("."), b[9:13].replace(".", ""), b[13].replace(".", ""), b[14:18].replace(".", "").lstrip("0")
    surname = lab[b].replace("&amp;", "&").split(" et al")[0].split(" &")[0].strip()
    params = {"query.author": surname, "filter": f"from-pub-date:{year},until-pub-date:{year}", "rows": 100, "select": "title,author,container-title,volume,page,article-number,DOI"}
    if jr in JOURNAL:
        params["query.container-title"] = JOURNAL[jr]
    try:
        items = json.loads(urllib.request.urlopen(urllib.request.Request("https://api.crossref.org/works?" + urllib.parse.urlencode(params), headers=UA), timeout=60).read())["message"]["items"]
    except Exception as e:
        items = []; print("crossref error", b, e)
    want = {pg, qual + pg}
    hit = next((i for i in items if i.get("author") and surname.lower()[:5] in (i["author"][0].get("family", "") or "").lower() and str(i.get("volume", "")) == vol
                and (want & set(re.split(r"[-\u2013]", str(i.get("page", "")))) or str(i.get("article-number", "")) in want)), None)
    rows.append(dict(bibcode=b, label=lab[b].replace("&amp;", "&"), year=year, journal=hit["container-title"][0] if hit and hit.get("container-title") else "", volume=vol, page=qual + pg,
                     title=re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", hit["title"][0])) if hit else "", doi=hit.get("DOI", "") if hit else "", matched=bool(hit)))
    time.sleep(1.0)
pd.DataFrame(rows).to_csv(ROOT / "data" / "literature" / "catalog_refs.csv", index=False)
pd.set_option("display.width", 300); pd.set_option("display.max_colwidth", 105)
print(pd.DataFrame(rows)[["label", "journal", "title", "matched"]].to_string(index=False))
