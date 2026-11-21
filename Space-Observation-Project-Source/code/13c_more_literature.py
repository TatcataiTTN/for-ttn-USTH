"""Bước 13c - Bổ sung bài cho các nhóm phương pháp còn thiếu; kiểm chứng CHẶT: tác giả đầu trùng họ + tiêu đề Jaccard >= 0.6.
Bài đạt thì thêm vào data/literature/verified_curated.csv (nếu chưa có); bài không đạt in ra NOT VERIFIED và không dùng."""
import csv, pathlib, time
src = open(pathlib.Path(__file__).with_name("13_verify_literature.py")).read().split("rows = []")[0]
exec(src.split("C = [")[0] + src[src.index("HEAD = "):])
MORE = [
 ("J Phase curves & timing", "Shporer", 2019, "TESS Full Orbital Phase Curve of the WASP-18b System"),
 ("J Phase curves & timing", "Parmentier", 2018, "Exoplanet Phase Curves: Observations and Theory"),
 ("J Phase curves & timing", "Eastman", 2010, "Achieving Better Than 1 Minute Accuracy in the Heliocentric and Barycentric Julian Dates"),
 ("D Transit modelling", "Kipping", 2010, "Investigations of approximate expressions for the transit duration"),
 ("D Transit modelling", "Hogg", 2010, "Data analysis recipes: Fitting a model to data"),
 ("D Transit modelling", "Hogg", 2018, "Data analysis recipes: Using Markov Chain Monte Carlo"),
 ("D Transit modelling", "Sharma", 2017, "Markov Chain Monte Carlo Methods for Bayesian Data Analysis in Astronomy"),
 ("B Detrending", "McQuillan", 2014, "Rotation periods of 34,030 Kepler main-sequence stars: the full autocorrelation sample"),
 ("A Mission & data", "Oelkers", 2018, "Precision Light Curves from TESS Full-Frame Images: A Different Imaging Approach"),
 ("C Transit search", "Eisner", 2021, "Planet Hunters TESS II: findings from the first two years of TESS"),
 ("C Transit search", "Heller", 2019, "Transit least-squares survey. I. Discovery and validation of an Earth-sized planet in the four-planet system K2-32"),
 ("E Vetting & validation", "Lissauer", 2012, "Almost All of Kepler's Multiple Planet Candidates are Planets"),
 ("G Population & composition", "Wolfgang", 2016, "Probabilistic Mass-Radius Relationship for Sub-Neptune-Sized Planets"),
 ("G Population & composition", "Burke", 2015, "Terrestrial Planet Occurrence Rates for the Kepler GK Dwarf Sample"),
 ("H Classic discoveries", "Fischer", 2016, "State of the Field: Extreme Precision Radial Velocities"),
 ("H Classic discoveries", "Kopparapu", 2013, "Habitable Zones Around Main-Sequence Stars: New Estimates"),
]
L = ROOT / "data" / "literature"
cur = list(csv.DictReader(open(L / "verified_curated.csv")))
have = {(r["first_author"], r["year"]) for r in cur}
keys = list(cur[0].keys())
for grp, au, yr, title in MORE:
    if (au, str(yr)) in have:
        continue
    try:
        best = None
        for t, authors, y, aid in arxiv(au, title):
            ok = jacc(t, title) >= 0.6 and norm(au)[-1] == norm(authors[0])[-1]
            if ok and (best is None or jacc(t, title) > best[0]):
                best = (jacc(t, title), t, authors, y, aid)
        time.sleep(7)
        if best:
            sc, t, authors, y, aid = best
            cur.append(dict(group=grp, first_author=au, year=yr, query=title, status="OK", title=t, authors="; ".join(authors[:4]) + " et al.", ref="arXiv:" + aid, venue="", score=round(sc, 2), year_found=y))
            print("OK ", au, yr, "|", t[:80], aid)
        else:
            print("NOT VERIFIED", au, yr, title[:70])
    except Exception as e:
        print("ERROR", au, yr, e)
cur.sort(key=lambda r: (r["group"], int(r["year"])))
with open(L / "verified_curated.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore"); w.writeheader(); w.writerows(cur)
print(len(cur), "bài trong verified_curated.csv")
