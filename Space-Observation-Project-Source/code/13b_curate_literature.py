"""Bước 13b - Sửa tay có ghi lại sau khi rà verified.csv: bỏ dòng khớp sai, thay bằng bài tra lại theo arXiv id / DOI.
Dòng nào không xác minh được thì bỏ khỏi review (không trích dẫn). Ghi data/literature/verified_curated.csv."""
import csv, json, pathlib, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
ROOT = pathlib.Path(__file__).resolve().parents[1]
L = ROOT / "data" / "literature"
H = {"User-Agent": "course-literature-check/1.0"}
ns = {"a": "http://www.w3.org/2005/Atom"}
rows = list(csv.DictReader(open(L / "verified.csv")))
DROP = {("Jenkins", "2016"), ("Lightkurve Collaboration", "2018"), ("Montalto", "2020"), ("Cameron", "2012"), ("Kunimoto", "2022"),
        ("Winters", "2019"), ("Jenkins", "2020"), ("Howard", "2012"), ("Gandolfi", "2018"), ("Stassun", "2019"), ("Borucki", "2010")}
ACCEPT = {("Kovacs", "2002"), ("Gunther", "2017"), ("Gunther", "2019")}      # chỉ khác dấu trong tên tác giả
out = []
for r in rows:
    k = (r["first_author"], r["year"])
    if k in DROP:
        continue
    if k in ACCEPT:
        r["status"] = "OK"
    if k == ("Hellier", "2012"):
        r["title"] = "Seven transiting hot Jupiters from WASP-South, Euler and TRAPPIST: WASP-47b, WASP-55b, WASP-61b, WASP-62b, WASP-63b, WASP-66b and WASP-67b"
    out.append(r)
for grp, au, yr, aid in [("A Mission & data", "Stassun", 2019, "1905.10694"), ("G Population & composition", "Howard", 2012, "1103.2541"),
                         ("H Classic discoveries", "Gandolfi", 2018, "1809.07573"), ("I Project planets", "Jenkins", 2020, "2009.12832"),
                         ("I Project planets", "Winters", 2021, "2107.14737")]:
    root = ET.fromstring(urllib.request.urlopen(urllib.request.Request("http://export.arxiv.org/api/query?id_list=" + aid, headers=H), timeout=40).read())
    e = root.find("a:entry", ns)
    au_l = [x.find("a:name", ns).text for x in e.findall("a:author", ns)]
    assert au in au_l[0].replace("ä", "a"), (au, au_l[0])
    out.append(dict(group=grp, first_author=au, year=yr, query="by arXiv id", status="OK", title=" ".join(e.find("a:title", ns).text.split()),
                    authors="; ".join(au_l[:4]) + " et al.", ref="arXiv:" + aid, venue="", score="id", year_found=e.find("a:published", ns).text[:4]))
    time.sleep(3.2)
out.append(dict(group="H Classic discoveries", first_author="Borucki", year=2010, query="by DOI", status="OK",
                title="Kepler Planet-Detection Mission: Introduction and First Results", authors="Borucki, W. J. et al.", ref="doi:10.1126/science.1185402",
                venue="Science", score="doi", year_found=2010))
keys = ["group", "first_author", "year", "query", "status", "title", "authors", "ref", "venue", "score", "year_found"]
out.sort(key=lambda r: (r["group"], int(r["year"])))
with open(L / "verified_curated.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore"); w.writeheader(); w.writerows(out)
print(len(out), "bài đã kiểm chứng,", sum(r["status"] == "OK" for r in out), "OK")
