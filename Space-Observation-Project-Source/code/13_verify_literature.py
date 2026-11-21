"""Bước 13 - Kiểm chứng danh sách bài báo cho literature review TESS.

Mỗi dòng ứng viên: (nhóm, tác giả đầu, năm mong đợi, cụm tiêu đề). Script tra arXiv API (ti: + au:), nếu không
có thì tra Crossref (bài trước 1998 / không đăng arXiv), rồi ghi cả KẾT QUẢ TRA (tiêu đề, tác giả, năm, id/DOI)
vào data/literature/verified.csv. Bài nào không khớp tác giả đầu + năm bị đánh dấu MISMATCH, không đưa vào review.
Chỉ gửi tiêu đề/tên tác giả công khai tới arXiv/Crossref, không gửi thông tin cá nhân.
"""
import csv
import pathlib
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import json

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "literature"
OUT.mkdir(parents=True, exist_ok=True)

# (nhóm, tác giả đầu, năm, cụm tiêu đề)
C = [
 # A. Nhiệm vụ, thiết bị, dữ liệu
 ("A Mission & data", "Ricker", 2015, "Transiting Exoplanet Survey Satellite"),
 ("A Mission & data", "Sullivan", 2015, "The Transiting Exoplanet Survey Satellite: Simulations of Planet Detections and Astrophysical False Positives"),
 ("A Mission & data", "Barclay", 2018, "A Revised Exoplanet Yield from the Transiting Exoplanet Survey Satellite"),
 ("A Mission & data", "Stassun", 2018, "The TESS Input Catalog and Candidate Target List"),
 ("A Mission & data", "Stassun", 2019, "Revised Extinction and Radius Corrections for the TESS Input Catalog"),
 ("A Mission & data", "Jenkins", 2016, "The TESS science processing operations center"),
 ("A Mission & data", "Twicken", 2018, "Kepler Data Validation I: Architecture, Diagnostic Tests, and Data Products for Vetting Transiting Planet Candidates"),
 ("A Mission & data", "Li", 2019, "Kepler Data Validation II: Transit Model Fitting and Multiple-planet Search"),
 ("A Mission & data", "Smith", 2012, "Kepler Presearch Data Conditioning II - A Bayesian Approach to Systematic Error Correction"),
 ("A Mission & data", "Stumpe", 2012, "Kepler Presearch Data Conditioning I - Architecture and Algorithms for Error Correction in Kepler Light Curves"),
 ("A Mission & data", "Stumpe", 2014, "Multiscale Systematic Error Correction via Wavelet-Based Bandsplitting in Kepler Data"),
 ("A Mission & data", "Huang", 2020, "Photometry of 10 Million Stars from the First Two Years of TESS Full Frame Images: Part I"),
 ("A Mission & data", "Kunimoto", 2022, "Quick-look Pipeline Light Curves for 5.7 Million Stars in the First Two Years of TESS"),
 ("A Mission & data", "Caldwell", 2020, "TESS Science Processing Operations Center FFI Target List Products"),
 ("A Mission & data", "Guerrero", 2021, "The TESS Objects of Interest Catalog from the TESS Prime Mission"),
 ("A Mission & data", "Feinstein", 2019, "eleanor: An Open-source Tool for Extracting Light Curves from the TESS Full-frame Images"),
 ("A Mission & data", "Lightkurve Collaboration", 2018, "Lightkurve: Kepler and TESS time series analysis in Python"),
 ("A Mission & data", "Montalto", 2020, "DIAmante TESS AutoRegressive Planet Search"),
 ("A Mission & data", "Jenkins", 2010, "Overview of the Kepler Science Processing Pipeline"),
 ("A Mission & data", "Gaia Collaboration", 2018, "Gaia Data Release 2. Summary of the contents and survey properties"),
 # B. Làm phẳng / khử xu hướng
 ("B Detrending", "Vanderburg", 2014, "A technique for extracting highly precise photometry for the two-wheeled Kepler mission"),
 ("B Detrending", "Hippke", 2019, "Wotan: Comprehensive time-series de-trending in Python"),
 ("B Detrending", "Foreman-Mackey", 2017, "Fast and scalable Gaussian process modeling with applications to astronomical time series"),
 ("B Detrending", "Kovacs", 2005, "A trend filtering algorithm for wide-field variability surveys"),
 ("B Detrending", "Aigrain", 2016, "K2SC: Flexible systematics correction and detrending of K2 light curves using Gaussian Process regression"),
 ("B Detrending", "Barros", 2020, "Improving transit characterisation with Gaussian process modelling of stellar variability"),
 # C. Tìm transit (BLS, ML, tìm đa hành tinh)
 ("C Transit search", "VanderPlas", 2018, "Understanding the Lomb-Scargle Periodogram"),
 ("C Transit search", "Zechmeister", 2009, "The generalised Lomb-Scargle periodogram. A new formalism for the floating-mean and Keplerian periodograms"),
 ("C Transit search", "Kovacs", 2002, "A box-fitting algorithm in the search for periodic transits"),
 ("C Transit search", "Hippke", 2019, "Transit Least Squares: Optimized transit detection algorithm to search for periodic transits of small planets"),
 ("C Transit search", "Hartman", 2016, "VARTOOLS: A program for analyzing astronomical time-series data"),
 ("C Transit search", "Petigura", 2013, "A Plateau in the Planet Population Below Twice the Size of Earth"),
 ("C Transit search", "Jenkins", 2002, "Some Tests to Establish Confidence in Planets Discovered by Transit Photometry"),
 ("C Transit search", "Shallue", 2018, "Identifying Exoplanets with Deep Learning: A Five-planet Resonant Chain around Kepler-80"),
 ("C Transit search", "Ansdell", 2018, "Scientific Domain Knowledge Improves Exoplanet Transit Classification with Deep Learning"),
 ("C Transit search", "Yu", 2019, "Identifying Exoplanets with Deep Learning. III. Automated Triage and Vetting of TESS Candidates"),
 ("C Transit search", "Osborn", 2020, "Rapid classification of TESS planet candidates with convolutional neural networks"),
 ("C Transit search", "Dattilo", 2019, "Identifying Exoplanets with Deep Learning. II. Two New Super-Earths Uncovered by a Neural Network in K2 Data"),
 ("C Transit search", "Pearson", 2018, "Searching for Exoplanets using Artificial Intelligence"),
 ("C Transit search", "Armstrong", 2021, "Exoplanet validation with machine learning: 50 new validated Kepler planets"),
 # D. Mô hình hoá transit, MCMC
 ("D Transit modelling", "Mandel", 2002, "Analytic Light Curves for Planetary Transit Searches"),
 ("D Transit modelling", "Seager", 2003, "On the Unique Solution of Planet and Star Parameters from an Extrasolar Planet Transit Light Curve"),
 ("D Transit modelling", "Winn", 2010, "Transits and Occultations"),
 ("D Transit modelling", "Kreidberg", 2015, "batman: BAsic Transit Model cAlculatioN in Python"),
 ("D Transit modelling", "Foreman-Mackey", 2013, "emcee: The MCMC Hammer"),
 ("D Transit modelling", "Kipping", 2013, "Efficient, uninformative sampling of limb darkening coefficients for two-parameter laws"),
 ("D Transit modelling", "Kipping", 2010, "Binning is sinning: morphological light-curve distortions due to finite integration time"),
 ("D Transit modelling", "Claret", 2017, "Limb and gravity-darkening coefficients for the TESS satellite at several metallicities, surface gravities, and microturbulent velocities"),
 ("D Transit modelling", "Eastman", 2013, "EXOFAST: A Fast Exoplanetary Fitting Suite in IDL"),
 ("D Transit modelling", "Espinoza", 2019, "juliet: a versatile modelling tool for transiting and non-transiting exoplanetary systems"),
 ("D Transit modelling", "Foreman-Mackey", 2021, "exoplanet: Gradient-based probabilistic inference for exoplanet data & other astronomical time series"),
 ("D Transit modelling", "Agol", 2020, "Analytic Planetary Transit Light Curves and Derivatives for Stars with Polynomial Limb Darkening"),
 ("D Transit modelling", "Pont", 2006, "The effect of red noise on planetary transit detection"),
 ("D Transit modelling", "Carter", 2008, "Analytic Approximations for Transit Light-Curve Observables, Uncertainties, and Covariances"),
 ("D Transit modelling", "Goodman", 2010, "Ensemble samplers with affine invariance"),
 ("D Transit modelling", "Gelman", 1992, "Inference from iterative simulation using multiple sequences"),
 # E. Xác nhận, loại dương tính giả
 ("E Vetting & validation", "Collins", 2017, "AstroImageJ: Image Processing and Photometric Extraction for Ultra-precise Astronomical Light Curves"),
 ("E Vetting & validation", "Cameron", 2012, "Hot Jupiters, planet formation and the beginning of the TESS false positive problem"),
 ("E Vetting & validation", "Torres", 2011, "Modeling Kepler transit light curves as false positives: rejection of blend scenarios for Kepler-9"),
 ("E Vetting & validation", "Morton", 2012, "An efficient automated validation procedure for exoplanet transit candidates"),
 ("E Vetting & validation", "Morton", 2016, "False positive probabilities for all Kepler Objects of Interest: 1284 newly validated planets and 428 likely false positives"),
 ("E Vetting & validation", "Giacalone", 2021, "Vetting of 384 TESS Objects of Interest with TRICERATOPS and Statistical Validation of 12 Planet Candidates"),
 ("E Vetting & validation", "Santerne", 2016, "SOPHIE velocimetry of Kepler transit candidates XVII. The physical properties of giant exoplanets within 400 days of period"),
 ("E Vetting & validation", "Fressin", 2013, "The False Positive Rate of Kepler and the Occurrence of Planets"),
 ("E Vetting & validation", "Gunther", 2017, "Centroid vetting of transiting planet candidates from the Next Generation Transit Survey"),
 ("E Vetting & validation", "Bryson", 2013, "Identification of background false positives from Kepler data"),
 # F. Sao chủ, bán kính, khối lượng, thiên văn
 ("F Stellar characterisation", "Torres", 2010, "Accurate masses and radii of normal stars: modern results and applications"),
 ("F Stellar characterisation", "Berger", 2018, "Revised Radii of Kepler Stars and Planets using Gaia Data Release 2"),
 ("F Stellar characterisation", "Fulton", 2018, "The California-Kepler Survey. VII. Precise Planet Radii Leveraging Gaia DR2 Reveal the Stellar Mass Dependence of the Planet Radius Gap"),
 ("F Stellar characterisation", "Dotter", 2008, "The Dartmouth Stellar Evolution Database"),
 ("F Stellar characterisation", "Mann", 2015, "How to Constrain Your M Dwarf: Measuring Effective Temperature, Bolometric Luminosity, Mass, and Radius"),
 ("F Stellar characterisation", "Dressing", 2015, "The Occurrence of Potentially Habitable Planets Orbiting M Dwarfs Estimated from the Full Kepler Dataset"),
 ("F Stellar characterisation", "Huber", 2013, "Fundamental Properties of Stars Using Asteroseismology from Kepler and CoRoT"),
 ("F Stellar characterisation", "Winn", 2015, "Occurrence and Architecture of Exoplanetary Systems"),
 # G. Dân số, tần suất, khoảng trống bán kính, thành phần
 ("G Population & composition", "Howard", 2012, "Planet Occurrence within 0.25 AU of Solar-type Stars from Kepler"),
 ("G Population & composition", "Fulton", 2017, "The California-Kepler Survey. III. A Gap in the Radius Distribution of Small Planets"),
 ("G Population & composition", "Owen", 2013, "Kepler Planets: A Tale of Evaporation"),
 ("G Population & composition", "Owen", 2017, "Evaporation Valley in the Kepler Planets"),
 ("G Population & composition", "Weiss", 2014, "The Mass-Radius Relation for 65 Exoplanets Smaller than 4 Earth Radii"),
 ("G Population & composition", "Rogers", 2015, "Most 1.6 Earth-radius planets are not rocky"),
 ("G Population & composition", "Zeng", 2016, "Mass-Radius Relation for Rocky Planets based on PREM"),
 ("G Population & composition", "Zeng", 2019, "Growth model interpretation of planet size distribution"),
 ("G Population & composition", "Seager", 2007, "Mass-Radius Relationships for Solid Exoplanets"),
 ("G Population & composition", "Lopez", 2014, "The Role of Core Mass in Controlling Evaporation: The Kepler Radius Distribution and the Kepler-36 Density Dichotomy"),
 ("G Population & composition", "Chen", 2017, "Probabilistic Forecasting of the Masses and Radii of Other Worlds"),
 ("G Population & composition", "Hsu", 2019, "Occurrence Rates of Planets Orbiting FGK Stars: Combining Kepler DR25, Gaia DR2, and Bayesian Inference"),
 ("G Population & composition", "Bryson", 2021, "The Occurrence of Rocky Habitable Zone Planets Around Solar-Like Stars from Kepler Data"),
 ("G Population & composition", "Kunimoto", 2020, "Searching the Entirety of Kepler Data. II. Occurrence Rate Estimates for FGK Stars"),
 ("G Population & composition", "Petigura", 2018, "The California-Kepler Survey. IV. Metal-rich Stars Host a Greater Diversity of Planets"),
 ("G Population & composition", "Van Eylen", 2018, "An asteroseismic view of the radius valley: stripped cores, not born rocky"),
 ("G Population & composition", "Hardegree-Ullman", 2019, "Scaling K2. I. Revised Parameters for 222,088 K2 Stars and a K2 Planet Radius Valley at 1.9 Earth Radii"),
 ("G Population & composition", "Gupta", 2019, "Sculpting the Valley in the Radius Distribution of Small Exoplanets as a by-product of Planet Formation: The Core-Powered Mass-Loss Mechanism"),
 # H. Bài kinh điển / phát hiện nền tảng
 ("H Classic discoveries", "Mayor", 1995, "A Jupiter-mass companion to a solar-type star"),
 ("H Classic discoveries", "Charbonneau", 2000, "Detection of Planetary Transits Across a Sun-like Star"),
 ("H Classic discoveries", "Henry", 2000, "A Transiting 51 Peg-like Planet"),
 ("H Classic discoveries", "Borucki", 2010, "Kepler Planet-Detection Mission: Introduction and First Results"),
 ("H Classic discoveries", "Batalha", 2013, "Planetary Candidates Observed by Kepler. III. Analysis of the First 16 Months of Data"),
 ("H Classic discoveries", "Thompson", 2018, "Planetary Candidates Observed by Kepler. VIII. A Fully Automated Catalog With Measured Completeness and Reliability Based on Data Release 25"),
 ("H Classic discoveries", "Gillon", 2017, "Seven temperate terrestrial planets around the nearby ultracool dwarf star TRAPPIST-1"),
 ("H Classic discoveries", "Howell", 2014, "The K2 Mission: Characterization and Early Results"),
 ("H Classic discoveries", "Vanderspek", 2019, "TESS Discovery of an Ultra-short-period Planet Around the Nearby M Dwarf LHS 3844"),
 ("H Classic discoveries", "Dragomir", 2019, "TESS Delivers Its First Earth-sized Planet and a Warm Sub-Neptune"),
 ("H Classic discoveries", "Huang", 2018, "TESS Discovery of a Transiting Super-Earth in the pi Mensae System"),
 ("H Classic discoveries", "Gandolfi", 2018, "TESS's first planet: A super-Earth transiting the naked-eye star pi Mensae"),
 ("H Classic discoveries", "Charbonneau", 2002, "Detection of an Extrasolar Planet Atmosphere"),
 ("H Classic discoveries", "Knutson", 2007, "A map of the day-night contrast of the extrasolar planet HD 189733b"),
 ("H Classic discoveries", "Kreidberg", 2014, "Clouds in the atmosphere of the super-Earth exoplanet GJ1214b"),
 ("H Classic discoveries", "Sing", 2016, "A continuum from clear to cloudy hot-Jupiter exoplanets without primordial water depletion"),
 ("H Classic discoveries", "Kempton", 2018, "A Framework for Prioritizing the TESS Planetary Candidates Most Amenable to Atmospheric Characterization"),
 # I. Bài khám phá các hành tinh trong dự án
 ("I Project planets", "Hellier", 2009, "An orbital period of 0.94 days for the hot-Jupiter planet WASP-18b"),
 ("I Project planets", "Hellier", 2012, "WASP-South hot Jupiters: WASP-55b, WASP-61b and WASP-62b"),
 ("I Project planets", "Jenkins", 2020, "An ultrahot Neptune in the Neptune desert"),
 ("I Project planets", "Gunther", 2019, "A super-Earth and two sub-Neptunes transiting the nearby and bright M dwarf TOI-270"),
 ("I Project planets", "Winters", 2019, "The Second-closest Planetary System: LTT 1445"),
 ("I Project planets", "Berta-Thompson", 2015, "A rocky planet transiting a nearby low-mass star"),
 ("I Project planets", "Malavolta", 2018, "An ultra-short period rocky super-Earth with a secondary eclipse and a Neptune-like companion around K2-141"),
 ("I Project planets", "Crossfield", 2016, "197 Candidates and 104 Validated Planets in K2's First Five Fields"),
 ("I Project planets", "Plavchan", 2020, "A planet within the debris disk around the pre-main-sequence star AU Microscopii"),
 ("I Project planets", "Newton", 2019, "TESS Hunt for Young and Maturing Exoplanets (THYME). I. A Planet in the 45 Myr Tucana-Horologium Association"),
 ("I Project planets", "Pepper", 2020, "TESS Reveals HD 118203 b to be a Transiting Planet"),
 ("I Project planets", "Bouchy", 2005, "ELODIE metallicity-biased search for transiting Hot Jupiters II. A very hot Jupiter transiting the bright K star HD 189733"),
]

HEAD = {"User-Agent": "course-literature-check/1.0"}


def get(url, timeout=40):
    for k in range(3):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=HEAD), timeout=timeout).read()
        except Exception as e:
            err = e
            time.sleep(4)
    raise err


def norm(s):
    return re.sub(r"[^a-z0-9 ]+", " ", s.lower().replace("ö", "o").replace("ü", "u").replace("á", "a").replace("é", "e").replace("ć", "c").replace("č", "c")).split()


def jacc(a, b):
    A, B = set(norm(a)), set(norm(b))
    return len(A & B) / max(1, len(A | B))


def arxiv(au, title):
    last = au.split()[-1].replace("Gunther", "Gunther")
    words = " ".join(re.sub(r"[^A-Za-z0-9 ]+", " ", title).split()[:9])
    qs = urllib.parse.urlencode({"search_query": f'au:{last} AND ti:"{words}"', "max_results": 3})
    url = "http://export.arxiv.org/api/query?" + qs
    root = ET.fromstring(get(url))
    ns = {"a": "http://www.w3.org/2005/Atom"}
    out = []
    for e in root.findall("a:entry", ns):
        t = " ".join(e.find("a:title", ns).text.split())
        authors = [x.find("a:name", ns).text for x in e.findall("a:author", ns)]
        y = int(e.find("a:published", ns).text[:4])
        aid = e.find("a:id", ns).text.split("/abs/")[-1]
        out.append((t, authors, y, aid))
    return out


def crossref(au, year, title):
    url = "https://api.crossref.org/works?rows=3&select=title,author,issued,DOI,container-title&query.bibliographic=" + urllib.parse.quote(title + " " + au) + f"&filter=from-pub-date:{year-1},until-pub-date:{year+1}"
    j = json.loads(get(url))
    out = []
    for it in j["message"]["items"]:
        t = (it.get("title") or [""])[0]
        authors = [(a.get("family", "") + ", " + a.get("given", "")) for a in it.get("author", [])]
        y = it.get("issued", {}).get("date-parts", [[0]])[0][0]
        out.append((t, authors, y, it["DOI"], (it.get("container-title") or [""])[0]))
    return out


rows = []
for grp, au, yr, title in C:
    rec = dict(group=grp, first_author=au, year=yr, query=title, status="NOT FOUND", title="", authors="", ref="", venue="")
    try:
        best = None
        for t, authors, y, aid in arxiv(au, title):
            sc = jacc(t, title) + (0.5 if au.lower().split()[-1] in " ".join(authors).lower().replace("ö", "o") else 0)
            if best is None or sc > best[0]:
                best = (sc, t, authors, y, "arXiv:" + aid)
        time.sleep(3.2)
        if best is None or best[0] < 0.85:
            for t, authors, y, doi, ven in crossref(au, yr, title):
                sc = jacc(t, title) + (0.5 if au.lower().split()[-1] in " ".join(authors).lower() else 0)
                if best is None or sc > best[0]:
                    best = (sc, t, authors, y, "doi:" + doi)
                    rec["venue"] = ven
            time.sleep(1)
        if best:
            sc, t, authors, y, ref = best
            ok = jacc(t, title) >= 0.45 and au.lower().split()[-1] in " ".join(authors).lower().replace("ö", "o")
            rec.update(status="OK" if ok else "CHECK", title=t, authors="; ".join(authors[:4]) + (" et al." if len(authors) > 4 else ""), ref=ref, score=round(sc, 2), year_found=y)
    except Exception as e:
        rec["status"] = "ERROR " + str(e)[:60]
    rows.append(rec)
    print(rec["status"], "|", grp[:1], au, yr, "->", rec["title"][:70], rec["ref"], flush=True)

keys = ["group", "first_author", "year", "query", "status", "title", "authors", "ref", "venue", "score", "year_found"]
with open(OUT / "verified.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
print("xong", sum(r["status"] == "OK" for r in rows), "OK /", len(rows))
