# -*- coding: utf-8 -*-
"""Bước 25b - Ba bài của nhóm K mà truy vấn theo tiêu đề không khớp (tiêu đề arXiv có phụ đề hoặc dấu chấm khác). Tra theo mã arXiv đã biết,
chấp nhận chỉ khi tác giả đầu trùng họ, năm lệch tối đa 1 và MỌI từ trong tiêu đề dự kiến đều có trong tiêu đề arXiv. Thêm vào verified_curated.csv."""
import csv, pathlib, time
src = open(pathlib.Path(__file__).with_name("13_verify_literature.py")).read().split("rows = []")[0]
exec(src.split("C = [")[0] + src[src.index("HEAD = "):])
K = "K Search history"
BY_ID = [("Borucki", 2011, "Characteristics of Kepler Planetary Candidates Based on the First Data Set", "1006.2799"),
         ("Rauer", 2014, "The PLATO 2.0 mission", "1310.0696"),
         ("Pepe", 2021, "ESPRESSO VLT On-sky performance and first results", "2010.00316")]
L = ROOT / "data" / "literature"; cur = list(csv.DictReader(open(L / "verified_curated.csv"))); keys = list(cur[0].keys())
have = {(r["first_author"], r["year"]) for r in cur}
ns = {"a": "http://www.w3.org/2005/Atom"}
for au, yr, title, aid in BY_ID:
    if (au, str(yr)) in have: print("already", au, yr); continue
    root = ET.fromstring(get("http://export.arxiv.org/api/query?id_list=" + aid)); time.sleep(7)
    e = root.find("a:entry", ns)
    t = " ".join(e.find("a:title", ns).text.split()); authors = [x.find("a:name", ns).text for x in e.findall("a:author", ns)]; y = int(e.find("a:published", ns).text[:4])
    ok = norm(au)[-1] == norm(authors[0])[-1] and abs(y - yr) <= 1 and set(norm(title)) <= set(norm(t))
    print(("OK " if ok else "NOT VERIFIED"), au, yr, "|", t[:90], aid)
    if ok:
        cur.append(dict(group=K, first_author=au, year=yr, query=title, status="OK", title=t, authors="; ".join(authors[:4]) + " et al.", ref="arXiv:" + aid, venue="", score=1.0, year_found=y))
cur.sort(key=lambda r: (r["group"], int(r["year"])))
with open(L / "verified_curated.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore"); w.writeheader(); w.writerows(cur)
print(len(cur), "bài;", sum(r["group"] == K for r in cur), "trong nhóm K")
