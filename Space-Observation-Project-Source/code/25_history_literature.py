# -*- coding: utf-8 -*-
"""Bước 25 - Nhóm K "Search history": các bài gốc của hành trình tìm exoplanet (RV, transit từ mặt đất, sứ mệnh vũ trụ, đặc trưng khí quyển).
Kiểm chứng CHẶT như 13c: tác giả đầu trùng họ + tiêu đề Jaccard >= 0.6 + năm lệch tối đa 1; arXiv trước, Crossref sau (bài không đăng arXiv).
Bài đạt thì thêm vào data/literature/verified_curated.csv (nếu (tác giả, năm) chưa có); bài không đạt in NOT VERIFIED và không dùng.
Chỉ gửi tiêu đề và họ tác giả công khai tới arXiv/Crossref. Sau đó chạy code/14_download_literature.py để tải PDF open-access (không vượt paywall)."""
import csv
import pathlib
import time

src = open(pathlib.Path(__file__).with_name("13_verify_literature.py")).read().split("rows = []")[0]
exec(src.split("C = [")[0] + src[src.index("HEAD = "):])       # nạp import và hàm get/norm/jacc/arxiv/crossref

K = "K Search history"
MORE = [
    (K, "Wolszczan", 1992, "A planetary system around the millisecond pulsar PSR1257 + 12"),
    (K, "Borucki", 1984, "The photometric method of detecting other planetary systems"),
    (K, "Konacki", 2003, "An extrasolar planet that transits the disk of its parent star"),
    (K, "Alonso", 2004, "TrES-1: The Transiting Planet of a Bright K0 V Star"),
    (K, "Bakos", 2004, "Wide-Field Millimagnitude Photometry with the HAT: A Tool for Extrasolar Planet Detection"),
    (K, "Pollacco", 2006, "The WASP Project and the SuperWASP Cameras"),
    (K, "Pepper", 2007, "The Kilodegree Extremely Little Telescope (KELT): A Small Robotic Telescope for Large-Area Synoptic Surveys"),
    (K, "Nutzman", 2008, "Design Considerations for a Ground-based Transit Search for Habitable Planets Orbiting M dwarfs"),
    (K, "Barge", 2008, "Transiting exoplanets from the CoRoT space mission. I. CoRoT-Exo-1b: a low-density short-period planet around a G0V star"),
    (K, "Auvergne", 2009, "The CoRoT satellite in flight: description and performance"),
    (K, "Koch", 2010, "Kepler Mission Design, Realized Photometric Performance, and Early Science"),
    (K, "Borucki", 2010, "Kepler Planet-Detection Mission: Introduction and First Results"),
    (K, "Borucki", 2011, "Characteristics of Kepler Planetary Candidates Based on the First Data Set"),
    (K, "Batalha", 2013, "Planetary Candidates Observed by Kepler. III. Analysis of the First 16 Months of Data"),
    (K, "Howell", 2014, "The K2 Mission: Characterization and Early Results"),
    (K, "Rauer", 2014, "The PLATO 2.0 mission"),
    (K, "Vanderburg", 2015, "Planetary Candidates from the First Year of the K2 Mission"),
    (K, "Thompson", 2018, "Planetary Candidates Observed by Kepler. VIII. A Fully Automated Catalog With Measured Completeness and Reliability Based on Data Release 25"),
    (K, "Benz", 2021, "The CHEOPS mission"),
    (K, "Pepe", 2021, "ESPRESSO at VLT. On-sky performance and first results"),
    (K, "Charbonneau", 2002, "Detection of an Extrasolar Planet Atmosphere"),
    (K, "Charbonneau", 2005, "Detection of Thermal Emission from an Extrasolar Planet"),
    (K, "Deming", 2005, "Infrared radiation from an extrasolar planet"),
    (K, "Gardner", 2006, "The James Webb Space Telescope"),
    (K, "Ahrer", 2023, "Early Release Science of the exoplanet WASP-39b with JWST NIRCam"),
    (K, "Bond", 2004, "OGLE 2003-BLG-235/MOA 2003-BLG-53: A Planetary Microlensing Event"),
    (K, "Marois", 2008, "Direct Imaging of Multiple Planets Orbiting the Star HR 8799"),
]
L = ROOT / "data" / "literature"
cur = list(csv.DictReader(open(L / "verified_curated.csv")))
have = {(r["first_author"], r["year"]) for r in cur}
keys = list(cur[0].keys())
last = lambda name: norm(name.split(",")[0] if "," in name else name)[-1]
for grp, au, yr, title in MORE:
    if (au, str(yr)) in have:
        print("already in list:", au, yr)
        continue
    best = None
    try:
        for t, authors, y, aid in arxiv(au, title):
            sc = jacc(t, title)
            if sc >= 0.6 and last(au) == last(authors[0]) and abs(y - yr) <= 1 and (best is None or sc > best[0]):
                best = (sc, t, authors, y, "arXiv:" + aid, "")
        time.sleep(7)
        if best is None:                                                   # không có trên arXiv: tra Crossref (chỉ để xác nhận bài tồn tại, không tải)
            for t, authors, y, doi, ven in crossref(au, yr, title):
                sc = jacc(t, title)
                if sc >= 0.6 and last(au) == last(authors[0]) and abs(y - yr) <= 1 and (best is None or sc > best[0]):
                    best = (sc, t, authors, y, "doi:" + doi, ven)
            time.sleep(2)
    except Exception as e:
        print("ERROR", au, yr, str(e)[:80]); time.sleep(10); continue
    if best:
        sc, t, authors, y, ref, ven = best
        cur.append(dict(group=grp, first_author=au, year=yr, query=title, status="OK", title=t, authors="; ".join(authors[:4]) + " et al.", ref=ref, venue=ven, score=round(sc, 2), year_found=y))
        print("OK ", au, yr, "|", t[:78], ref, flush=True)
    else:
        print("NOT VERIFIED", au, yr, title[:70], flush=True)
cur.sort(key=lambda r: (r["group"], int(r["year"])))
with open(L / "verified_curated.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore"); w.writeheader(); w.writerows(cur)
print(len(cur), "bài trong verified_curated.csv;", sum(r["group"] == K for r in cur), "trong nhóm K")
