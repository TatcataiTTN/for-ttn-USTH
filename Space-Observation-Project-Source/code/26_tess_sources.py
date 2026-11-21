# -*- coding: utf-8 -*-
"""Bước 26 - Nguồn của từng con số về TESS: tìm đoạn nguyên văn trong PDF Ricker+2015 (theo từng trang) và trong các trang web công khai đã lưu
(data/raw/tess_docs/, tải ngày 2026-11-21). Ra: data/literature/tess_fact_sources.csv (mỗi dòng: điều khẳng định, giá trị, nguồn, mục/bảng, trang PDF, đoạn nguyên văn).
Một dòng chỉ được ghi verified=True khi đoạn nguyên văn tìm thấy đúng trong văn bản nguồn. Không tải gì mới; chỉ đọc."""
import csv
import glob
import html
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
RICKER = glob.glob(str(ROOT / "literature" / "pdf" / "A_Mission_data" / "Ricker_2015_*.pdf"))[0]
DOCS = ROOT / "data" / "raw" / "tess_docs"
fix = lambda t: re.sub(r"\s+", " ", t.replace("◦", "°").replace("−", "-").replace("–", "-").replace("’", "'").replace(" ", " ")).strip()


def pdf_pages(path):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout).group(1))
    return [fix(subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), path, "-"], capture_output=True, text=True).stdout) for i in range(1, n + 1)]


def web_text(name):
    t = open(DOCS / name, encoding="utf-8", errors="ignore").read()
    t = re.sub(r"(?s)<(script|style).*?</\1>", " ", t)
    return fix(html.unescape(re.sub(r"<[^>]+>", " ", t)))


RP = pdf_pages(RICKER)
R = "Ricker, G. R. et al. 2015, J. Astron. Telesc. Instrum. Syst. 1, 014003 (arXiv:1406.0151v3); PDF in literature/pdf/A_Mission_data/"
# (id, thema, điều khẳng định, giá trị, mục/bảng, đoạn nguyên văn trong PDF)
RF = [
    ("orbit_shape", "Orbit", "Elliptical orbit around the Earth", "perigee 17 R_E, apogee 59 R_E", "Sec 6", "nominal perigee and apogee of 17 R"),
    ("orbit_period", "Orbit", "Period and resonance with the Moon", "13.7 d, 2:1 with the Moon's orbit", "Sec 6", "13.7 day period in 2:1 resonance with the Moon's orbit"),
    ("orbit_incl", "Orbit", "Inclined to the ecliptic, so no long eclipses by Earth or Moon", "inclined from the ecliptic plane", "Sec 6", "inclined from the ecliptic plane, thereby eliminating lengthy eclipses"),
    ("orbit_radiation", "Orbit", "Above the radiation belts; thermal stability", "CCDs near -75 C", "Sec 6", "CCDs will operate near -75"),
    ("launch_site", "Path to orbit", "Launch and first orbit (nominal scenario)", "Cape Canaveral, parking orbit 28.5 deg", "Sec 6, Fig 5", "launched from Cape Canaveral into a parking orbit with an equatorial inclination of 28.5"),
    ("launch_apogee", "Path to orbit", "Apogee raised by two burns", "400 000 km", "Sec 6", "The apogee is raised to 400,000 km after two additional burns"),
    ("launch_moon", "Path to orbit", "Lunar flyby raises the ecliptic inclination", "to about 40 deg", "Sec 6", "lunar flyby raises the ecliptic inclination to about 40"),
    ("launch_days", "Path to orbit", "Time to reach the final orbit", "about 60 days after launch", "Sec 6", "The final orbit is achieved about 60 days after launch"),
    ("orbit_stable", "Orbit", "Stability and station-keeping", "no propulsion for station-keeping; stable for decades", "Sec 6", "requires no propulsion for station-keeping"),
    ("downlink", "Data", "Downlink rhythm", "every 13.7 d at perigee", "Sec 4.3", "downlinked every 13.7 days at perigee"),
    ("downlink_len", "Data", "Downlink duration and rate", "4 h at each perigee, 100 Mb/s", "Sec 5", "downlink the science data during 4 hr intervals at each perigee"),
    ("cameras_rect", "Cameras", "Four cameras form one rectangle", "24 x 96 deg", "Sec 5", "form a rectangle measuring 24° × 96° on the sky"),
    ("lens", "Cameras", "Lens", "f/1.4, pupil 10.5 cm", "Sec 4.1", "entrance pupil diameter of 10.5 cm"),
    ("band", "Cameras", "Wavelength range", "600-1000 nm", "Table 1", "Wavelength range 600-1000 nm"),
    ("fov", "Cameras", "Field of view", "24 x 24 deg each; 24 x 96 deg = 2300 sq. deg", "Table 1", "24° × 96° = 2300 sq. deg"),
    ("pixel", "Cameras", "Pixel size and PSF", "15 micron = 0.35 arcmin", "Sec 4.1", "one pixel or 0.35 arcmin"),
    ("ensq50", "Cameras", "Light in one pixel", "50 % in 15 x 15 micron (1 pixel)", "Table 1", "Ensquared energy 50% within 15 × 15"),
    ("ensq90", "Cameras", "Light in 4 x 4 pixels", "90 % in 4 x 4 pixels = 1.4 arcmin", "Table 1", "90% within 60 × 60"),
    ("ccd", "Cameras", "CCD format", "2048 x 2048 imaging array, 15 micron pixels", "Sec 4.2", "2048 × 2048 imaging array"),
    ("sector_len", "Pointing", "A sector lasts two orbits", "27.4 d, boresight nearly anti-solar", "Sec 7.2", "two spacecraft orbits (27.4 days)"),
    ("anti_solar", "Pointing", "Pointing direction", "nearly anti-solar", "Sec 7.2", "pointed nearly anti-solar"),
    ("sectors_n", "Pointing", "Sectors per hemisphere and extent", "13 sectors, ecliptic latitude 6 deg to the pole", "Sec 7.2", "13 partially overlapping sectors"),
    ("sector_shift", "Pointing", "Step between sectors", "about 27 deg east in ecliptic longitude", "Sec 7.2", "shifted eastward in ecliptic longitude by about 27"),
    ("coverage_27", "Pointing", "Area observed at least 27 d", "30 000 sq. deg", "Sec 7.2", "Approximately 30,000 square degrees are observed for at least 27 days"),
    ("coverage_80", "Pointing", "Area observed more than 80 d", "2800 sq. deg", "Sec 7.2", "approximately 2800 square degrees are observed for more than 80 days"),
    ("coverage_300", "Pointing", "Area observed more than 300 d", "900 sq. deg, around the ecliptic poles", "Sec 7.2", "approximately 900 square degrees are observed for more than 300 days"),
    ("coverage_time", "Pointing", "Time to cover the sky", "hemisphere 1 yr, all sky 2 yr", "Sec 7.2", "Observing an entire hemisphere takes one year"),
    ("cadence_2min", "Sampling", "2-min cadence", "60 frames of 2 s summed", "Sec 4.3", "summed into consecutive groups of 60, giving an effective exposure time of 2 min"),
    ("ffi_30", "Sampling", "Full-frame images", "every 30 min (primary mission)", "Sec 4.3", "Full frame images are also stacked every 30 min"),
    ("targets", "Sampling", "Pre-selected stars", "at least 200 000, I_C about 4-13", "Abstract", "at least 200,000 mainsequence dwarf stars with IC ≈ 4-13"),
    ("noise_floor", "Sampling", "Noise-floor assumption", "60 ppm per hour", "Sec 8.1", "an assumed 60 ppm of incorrigible noise on hourly timescales"),
    ("ops", "Orbit", "Operations rhythm", "one 4 h downlink and repoint every 2 weeks", "Table 2", "single 4-hr downlink & repoint every 2 weeks"),
]
# (id, thema, điều khẳng định, giá trị, nguồn đầy đủ, URL, tệp đã lưu, đoạn nguyên văn)
WF = [
    ("launch_date", "Launch", "Launch date and status", "18 April 2018; extended mission", "NASA Science, TESS mission page", "https://science.nasa.gov/mission/tess/", "science_nasa_gov_mission_tess_.html", "Launch April 18, 2018"),
    ("pixel_mast", "Cameras", "Pixel scale on the archive page", "21 arcseconds / pixel", "STScI MAST, TESS mission page", "https://archive.stsci.edu/missions-and-data/tess", "archive_stsci_edu_missions-and-data_tess.html", "Resolution 21 arcseconds / pixel"),
    ("fov_mast", "Cameras", "Field of view on the archive page", "24x96 degree", "STScI MAST, TESS mission page", "https://archive.stsci.edu/missions-and-data/tess", "archive_stsci_edu_missions-and-data_tess.html", "24x96 degree field-of-view"),
    ("ffi_cycles", "Sampling", "Full-frame cadence by cycle", "30 min (cycles 1-2), 10 min (3-4), 200 s (5+)", "NASA HEASARC, TESS data products", "https://heasarc.gsfc.nasa.gov/docs/tess/data-products.html", "heasarc_gsfc_nasa_gov_docs_tess_data-products_html.html", "30 minutes (Cycles 1 and 2), 10 minutes (Cycles 3 and 4), and 200 seconds (Cycles 5+)"),
    ("fast_lc", "Sampling", "20-s light curves", "added with the first extended mission", "NASA HEASARC, TESS data products", "https://heasarc.gsfc.nasa.gov/docs/tess/data-products.html", "heasarc_gsfc_nasa_gov_docs_tess_data-products_html.html", "additional option of 20 second data products was added"),
    ("sector27", "Mission phase", "First extended-mission data", "sector 27, July 2020", "STScI TESS Archive Manual, Data Product Overview", "https://outerspace.stsci.edu/display/TESS/2.0+-+Data+Product+Overview", "outerspace_stsci_edu_display_TESS_2_0_-_Data_Product_Overview.html", "Sector 27 is the first set of data associated with the TESS extended mission that began in July 2020"),
    ("years", "Mission phase", "Sectors by year", "Year 3 = S27-39, Year 4 = S40-55, Year 5 = S56-69", "MIT TESS Science Office, data products", "https://tess.mit.edu/science/data-products/", "tess_mit_edu_science_data-products_.html", "Year 3 (S27-39) Sector 27"),

    ("launch_provider", "Launch", "Launch vehicle, site and time", "SpaceX Falcon 9, Cape Canaveral AFS, 18 April 2018, 6:51 p.m. EDT", "MIT News, TESS takes off", "https://science.mit.edu/tess-takes-off", "science_mit_edu_tess-takes-off.html", "On April 18 at 6:51 p.m., TESS had a picture-perfect launch on a SpaceX Falcon 9 rocket from Cape Canaveral Air Force Station in Florida"),
    ("contract", "Launch", "NASA chose SpaceX for the launch", "Falcon 9 v1.1; contract release C14-049 of 16 Dec 2014", "NASA contract release C14-049", "https://www.nasa.gov/news-release/nasa-awards-launch-services-contract-for-transiting-exoplanet-survey-satellite-2", "www_nasa_gov_news-release_nasa-awards-launch-services-contract-for-transiting-exoplanet-su.html", "NASA has selected SpaceX to provide launch services for the Transiting Exoplanet Survey Satellite (TESS) mission"),
    ("launch_cost", "Cost", "Total cost to NASA of the launch", "about $87 million (launch service, processing, integration, tracking, data and telemetry)", "NASA contract release C14-049", "https://www.nasa.gov/news-release/nasa-awards-launch-services-contract-for-transiting-exoplanet-survey-satellite-2", "www_nasa_gov_news-release_nasa-awards-launch-services-contract-for-transiting-exoplanet-su.html", "The total cost for NASA to launch TESS is approximately $87 million"),
    ("mission_lead", "Management", "Who runs the mission", "MIT leads; Explorers Program at NASA Goddard oversees; NASA Launch Services Program (Kennedy) manages the launch", "NASA contract release C14-049", "https://www.nasa.gov/news-release/nasa-awards-launch-services-contract-for-transiting-exoplanet-survey-satellite-2", "www_nasa_gov_news-release_nasa-awards-launch-services-contract-for-transiting-exoplanet-su.html", "The TESS Mission is led by the Massachusetts Institute of Technology, with oversight by the Explorers Program"),
    ("mission_cost_pw", "Cost", "Total mission cost as reported (secondary source)", "$337 million", "Physics World, 19 April 2018", "https://physicsworld.com/a/nasa-launches-tess-exoplanet-mission/", "physicsworld_com_a_nasa-launches-tess-exoplanet-mission_.html", "the $337m Transiting Exoplanet Survey Satellite (TESS)"),
    ("early_budget_1", "Cost", "First proposal (2006)", "privately funded mission for $20 million", "MIT News, TESS takes off", "https://science.mit.edu/tess-takes-off", "science_mit_edu_tess-takes-off.html", "as a privately funded mission for $20 million"),
    ("early_budget_2", "Cost", "Second proposal", "NASA funding at $120 million; Small Explorer proposal in 2008", "MIT News, TESS takes off", "https://science.mit.edu/tess-takes-off", "science_mit_edu_tess-takes-off.html", "at a higher level of $120 million"),
    ("vn_vnredsat", "Vietnam", "VNREDSat-1 was launched abroad", "Vega rocket, Guiana Space Center, 7 May 2013", "Government of Viet Nam online newspaper", "https://en.baochinhphu.vn/vns-first-remote-sensing-satellite-launched-11116660.htm", "en_baochinhphu_vn_vns-first-remote-sensing-satellite-launched-11116660_htm.html", "was launched into orbit from the Guiana Space Center, French Guiana at 9:06 a.m (local time) on May 7"),
    ("vn_vnredsat_cost", "Vietnam", "VNREDSat-1 investment", "EUR 55.8 million: French ODA plus about VND 65 billion from Vietnam", "Government of Viet Nam online newspaper", "https://en.baochinhphu.vn/vns-first-remote-sensing-satellite-launched-11116660.htm", "en_baochinhphu_vn_vns-first-remote-sensing-satellite-launched-11116660_htm.html", "total investment of €55.8 million sourced by the French Government's Official Development Assistance"),
    ("vn_vinasat", "Vietnam", "Earlier Vietnamese satellites", "Vinasat 1 (2008), Vinasat 2 (2012), telecommunications", "Government of Viet Nam online newspaper", "https://en.baochinhphu.vn/vns-first-remote-sensing-satellite-launched-11116660.htm", "en_baochinhphu_vn_vns-first-remote-sensing-satellite-launched-11116660_htm.html", "Viet Nam launched two telecommunication satellites, Vinasat 1 and Vinasat 2 in 2008 and 2012"),
    ("vn_lotusat", "Vietnam", "LOTUSat-1 waits for a Japanese launcher", "570 kg radar satellite; scheduled February 2025 in an article of 15 July 2024; later status not checked", "VietnamNet Global, 15 July 2024", "https://vietnamnet.vn/en/vietnam-prepares-for-lotusat-1-satellite-launch-with-japanese-assistance-2301839.html", "vietnamnet_vn_en_vietnam-prepares-for-lotusat-1-satellite-launch-with-japanese-assistance-.html", "now awaiting Japan's launch vehicle to be sent into orbit"),
    ("vn_vinspace", "Vietnam", "Vietnam's 2027 launch is a SpaceX rideshare", "VinSpace (Vingroup): SpaceX Transporter rideshare, second quarter of 2027 (article of 11 Aug 2026)", "Al Jazeera, 11 August 2026", "https://aljazeera.com/economy/2026/8/11/vietnams-vinspace-announces-deal-with-spacex-to-launch-first-satellite", "aljazeera_com_economy_2026_8_11_vietnams-vinspace-announces-deal-with-spacex-to-.html", "it will use SpaceX's Transporter ride-share programme to deploy the satellites into orbit in the second quarter of 2027"),
    ("vn_smallsat", "Vietnam", "Small-satellite facility", "satellites under 180 kg; infrastructure planned for December 2025", "VietnamNet Global, 15 July 2024", "https://vietnamnet.vn/en/vietnam-prepares-for-lotusat-1-satellite-launch-with-japanese-assistance-2301839.html", "vietnamnet_vn_en_vietnam-prepares-for-lotusat-1-satellite-launch-with-japanese-assistance-.html", "small satellites under 180kg is expected to be completed by December 2025"),
]

# (id, tiền tố tệp trong literature/pdf/*/, điều khẳng định, giá trị, mục, đoạn nguyên văn)
PF = [
    ("hd209_transit", "Charbonneau_2000", "First transits of a planet across a Sun-like star", "HD 209458 b", "Title", "Detection of Planetary Transits Across a Sun-like Star"),
    ("hat_landmark", "Bakos_2004", "HD 209458 b called a landmark; motive for transit surveys", "", "Sec 1", "was a landmark in exoplanet research"),
    ("tres_first", "Alonso_2004", "First planet from a wide-field bright-star ground survey", "TrES-1", "Abstract", "the first transiting extrasolar planet to be detected by such a wide-field, bright-star survey"),
    ("wasp_cam", "Pollacco_2006", "SuperWASP cameras", "wide-field, La Palma", "Abstract", "The SuperWASP Cameras are wide-field imaging systems sited at the Observatorio del Roque de los Muchachos"),
    ("kelt", "Pepper_2007", "KELT telescope", "small-aperture wide-field robotic, Winer Observatory", "Abstract", "small-aperture, wide-field automated telescope located at Winer Observatory"),
    ("mearth", "Nutzman_2008", "MEarth aim", "network of ground-based robotic telescopes", "Abstract", "network of ground-based robotic telescopes"),
    ("corot_launch", "Auvergne_2009", "CoRoT launch", "27 December 2006", "Abstract", "the satellite was launched on December 27th 2006"),
    ("corot_first", "Barge_2008", "First CoRoT planet", "CoRoT-Exo-1b", "Abstract", "the detection of the first planet discovered by CoRoT"),
    ("kepler_launch", "Koch_2010", "Kepler launch", "6 March 2009", "Abstract", "launched on Mar 6, 2009"),
    ("kepler_ap", "Koch_2010", "Kepler aperture", "0.95 m", "Sec 2", "0.95-m aperture"),
    ("kepler_orbit", "Koch_2010", "Kepler orbit", "Earth-trailing heliocentric orbit", "Sec 2", "Earth-trailing heliocentric orbit"),
    ("k2_wheels", "Howell_2014", "Why K2 exists", "two reaction wheels lost", "Abstract", "The loss of two reaction wheels on the Kepler spacecraft has ended the primary mission data collection"),
    ("k2_ecliptic", "Howell_2014", "How K2 observes", "fields along the ecliptic", "Sec 1", "observe target fields along the ecliptic"),
    ("cheops_launch", "Benz_2021", "CHEOPS launch", "18 December 2019, Soyuz-Fregat, Kourou", "Abstract", "successfully launched on December 18, 2019, as a secondary passenger on a Soyuz-Fregat rocket from Kourou"),
    ("plato_m3", "Rauer_2014", "PLATO selection (as of 2014)", "ESA M3 launch opportunity (2022/24)", "Abstract", "selected for ESA's M3 launch opportunity (2022/24)"),
    ("hst_na", "Charbonneau_2002", "HST detects sodium in HD 209458 b", "four transits", "Abstract", "four planetary transits of HD 209458, in the region of the sodium resonance doublet"),
    ("spitzer_tres", "Charbonneau_2005", "Spitzer thermal emission of TrES-1", "", "Abstract", "Spitzer Space Telescope infrared photometric time series of the transiting extrasolar planet system TrES-1"),
    ("spitzer_hd", "Deming_2005", "Spitzer infrared radiation of HD 209458 b", "", "Sec 1", "The planet HD 209458b"),
    ("jwst_design", "Gardner_2006", "JWST design", "infrared space observatory at the second Sun-Earth Lagrange point", "Abstract", "infrared-optimized space observatory that will be launched early in the next decade into orbit around the second Earth-Sun Lagrange point"),
    ("jwst_wasp39", "Ahrer_2023", "JWST NIRCam transit of WASP-39 b", "22-23 July 2022", "Sec 2", "single transit of WASP-39b with JWST's NIRCam instrument on 22-23 July 2022"),
]
rows = []
for fid, th, st, val, loc, snip in RF:
    s = fix(snip)
    pg = [i + 1 for i, t in enumerate(RP) if s in t]
    rows.append(dict(id=fid, topic=th, statement=st, value=val, source="Ricker et al. 2015", location=loc, page=pg[0] if pg else "", url="arXiv:1406.0151", quote=snip, verified=bool(pg), full_citation=R))
for fid, th, st, val, src, url, fn, snip in WF:
    ok = fix(snip) in web_text(fn)
    rows.append(dict(id=fid, topic=th, statement=st, value=val, source=src, location="web page", page="", url=url, quote=snip, verified=ok, full_citation=f"{src}, {url}, saved {fn} on 2026-11-21 (data/raw/tess_docs/)"))
_cache = {}
for fid, pre, st, val, loc, snip in PF:
    fl = glob.glob(str(ROOT / "literature" / "pdf" / "*" / (pre + "*.pdf")))
    if not fl:
        rows.append(dict(id=fid, topic="History", statement=st, value=val, source=pre, location=loc, page="", url="", quote=snip, verified=False, full_citation="PDF missing")); continue
    pgs = _cache.setdefault(fl[0], pdf_pages(fl[0])); s_ = fix(snip); pg = [i + 1 for i, t in enumerate(pgs) if s_ in t]
    au, yr = pre.split("_")[0].replace("Gaia", "Gaia"), pre.split("_")[1]
    rows.append(dict(id=fid, topic="History", statement=st, value=val, source=f"{au} {yr}", location=loc, page=pg[0] if pg else "", url="", quote=snip, verified=bool(pg), full_citation=pathlib.Path(fl[0]).relative_to(ROOT).as_posix()))
out = ROOT / "data" / "literature" / "tess_fact_sources.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
bad = [r["id"] for r in rows if not r["verified"]]
print(len(rows), "facts;", sum(r["verified"] for r in rows), "verified verbatim; not found:", bad)
print({r["id"]: r["page"] for r in rows if r["page"]})
