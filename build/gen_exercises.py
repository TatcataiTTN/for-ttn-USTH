#!/usr/bin/env python3
"""Generate the 90 active-recall exercises (fill / calc / match / order) into
exercises.json. Numeric answers for `calc` items are COMPUTED here from the real
v3 formulas (never hand-typed), so a typo cannot silently produce a wrong key."""
import json
import math
import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from exercise_details import DETAILS

OUT = "/Users/tuannghiat/for-ttn-USTH/Thesis-M1/data/exercises.json"

# ---- v3 formula helpers (closed-form; mirror 05_Code_v3/modules) ----
LAMBDA = 1550e-9; THETA_C = 10e-6; A_R = 0.05; H_S = 550.0; H_ATM = 20.0
R_E = 6371.0
w0 = LAMBDA / (2 * THETA_C)

def slant_km(eps_deg):
    e = math.radians(eps_deg)
    return math.sqrt(R_E**2 * math.sin(e)**2 + 2*R_E*H_S + H_S**2) - R_E*math.sin(e)

def wL(L_km):
    L = L_km * 1e3
    return w0 * math.sqrt(1 + (L*LAMBDA/(math.pi*w0**2))**2)

def hg_db(zeta_deg):
    eps = 90 - zeta_deg
    nu = math.sqrt(math.pi/2) * A_R / wL(slant_km(eps))
    hg = math.erf(nu)**2
    return 10*math.log10(hg)

def kruse_q(V):
    if V > 50: return 1.6
    if V > 6: return 1.3
    if V > 1: return 0.16*V + 0.34
    if V > 0.5: return V - 0.5
    return 0.0

def sigma_clear(V, lam_nm=1550):
    return (3.912/V) * (lam_nm/550.0)**(-kruse_q(V))

def sigma_rain(R):
    return (0.509 * R**0.63) / 4.343 if R > 0 else 0.0

def hl_db(zeta_deg, V, R=0.0):
    L_atm = H_ATM / math.cos(math.radians(zeta_deg))
    sig = sigma_clear(V) + sigma_rain(R)
    return 10*math.log10(math.exp(-sig*L_atm))

def Rcov_km(eps_deg):
    e = math.radians(eps_deg)
    psi = math.acos(R_E/(R_E+H_S)*math.cos(e)) - e
    return R_E*psi

def off_nadir(eps_deg):
    return math.degrees(math.asin(R_E*math.cos(math.radians(eps_deg))/(R_E+H_S)))

def haversine(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2-lat1); dl = math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R_E*math.asin(math.sqrt(a))

def H2(p):
    if p <= 0 or p >= 1: return 0.0
    return -p*math.log2(p) - (1-p)*math.log2(1-p)

def skr_norm(psift, qber, fEC=1.0, chiE=0.0):
    return max(0.0, psift*(1 - (1+fEC)*H2(qber) - chiE))

ex = []
def add(**kw):
    kw["id"] = len(ex) + 1
    ex.append(kw)

def calc(section, secn, prompt, answer, unit, framework, steps, tol=0.02, tolType="rel", given=""):
    add(type="calc", section=section, sectionNum=secn, prompt=prompt, given=given,
        answer=round(answer, 6), unit=unit, tol=tol, tolType=tolType,
        framework=framework, steps=steps)

def fill(section, secn, prompt, answer, accept, unit, framework, given=""):
    add(type="fill", section=section, sectionNum=secn, prompt=prompt, given=given,
        answer=answer, accept=accept, unit=unit, framework=framework)

def match(section, secn, prompt, pairs, framework, leftLabel="Item", rightLabel="Match"):
    add(type="match", section=section, sectionNum=secn, prompt=prompt,
        left=list(pairs.keys()), right=list(pairs.values()), pairs=pairs,
        leftLabel=leftLabel, rightLabel=rightLabel, framework=framework)

def order(section, secn, prompt, items, correct, framework):
    # items already in CORRECT order; we present shuffled, store correct sequence of labels
    add(type="order", section=section, sectionNum=secn, prompt=prompt,
        items=items, correctOrder=correct, framework=framework)

# =====================================================================
# SECTION 1 — Channel-physics calculations (calc)  [1..18]
# =====================================================================
S1 = "1. Channel physics — calculate"
calc(S1,1,"Beam waist w0 = lambda/(2*thetaC), lambda=1550 nm, thetaC=10 urad. Compute w0 in metres.",
     w0,"m","w0 = lambda/(2*thetaC); tighter divergence -> larger waist -> slower spreading.",
     "w0 = 1550e-9/(2*10e-6) = 0.0775 m.", tol=0.005)
calc(S1,1,"Spherical slant range at elevation 30 deg (zeta=60), H_S=550 km, R_E=6371 km. Give L in km.",
     slant_km(30),"km","L = sqrt(R_E^2 sin^2 e + 2 R_E H_S + H_S^2) - R_E sin e; corrected from flat-Earth 1100 km.",
     "eps=30: L = 992.8 km (NOT the flat-Earth H_S/cos(zeta)=1100 km).", tol=0.01)
calc(S1,1,"Slant range at elevation 90 deg (satellite at zenith). Give L in km.",
     slant_km(90),"km","At zenith the slant range equals the satellite altitude.",
     "eps=90: L = H_S = 550 km.", tol=0.005)
calc(S1,1,"Beam radius wL at the receiver for elevation 45 deg. Give wL in metres.",
     wL(slant_km(45)),"m","wL = w0*sqrt(1+(L*lambda/(pi*w0^2))^2); far-field grows ~linearly with L.",
     "L(45)=749 km -> wL = 4.77 m.", tol=0.03)
calc(S1,1,"Corrected normalized aperture nu_R = sqrt(pi/2)*a_R/wL at elevation 90 deg (a_R=5 cm). Give nu_R.",
     math.sqrt(math.pi/2)*A_R/wL(slant_km(90)),"(dimensionless)",
     "nu_R uses sqrt(pi/2)=1.2533 (v3 fix), NOT sqrt(2); old value made hg optimistic by 1.05 dB.",
     "nu_R = 1.2533*0.05/3.502 = 0.0179.", tol=0.03)
calc(S1,1,"Geometric loss hg at elevation 45 deg, in dB (v3 corrected).",
     hg_db(45),"dB","hg=[erf(nu_R)]^2; hg ~ 1/L^2 since nu_R<<1; dominant link-budget term (>30 dB).",
     "hg(45 deg elev) = -36.6 dB.", tol=0.02, tolType="abs")
calc(S1,1,"Clear-air extinction sigma_clear at V=10 km, 1550 nm (Kruse/Kim, q=1.3). Give km^-1.",
     sigma_clear(10),"km^-1","sigma=(3.912/V)(lambda/550)^(-q(V)); longer wavelength scatters less.",
     "q(10)=1.3 -> sigma=0.1017 km^-1.", tol=0.02)
calc(S1,1,"Rain extinction sigma_rain at R=30 mm/h (tropical Kone 2024: beta=0.509 R^0.63, sigma=beta/4.343). km^-1.",
     sigma_rain(30),"km^-1","Power-law rho=0.63<1 -> sub-linear; 4.343=10/ln10 converts dB->Nepers.",
     "beta=0.509*30^0.63=4.34 dB/km; sigma=0.999 km^-1.", tol=0.02)
calc(S1,1,"Atmospheric transmission hl in dB at zeta=30 deg, V=10 km, clear (R=0). L_atm=H_atm/cos(zeta).",
     hl_db(30,10),"dB","hl=exp(-sigma_total*L_atm); L_atm=(H_atm)/cos(zeta), H_atm=20 km.",
     "L_atm=23.09 km; hl=exp(-0.1017*23.09)=0.0954 -> -10.2 dB.", tol=0.02, tolType="abs")
calc(S1,1,"hl in dB at zeta=30 deg, V=10 km, WITH heavy rain R=30 mm/h. Show how much rain adds.",
     hl_db(30,10,30),"dB","Rain adds ~100 dB vs clear -> near link cut; why cloud/heavy-rain ~ outage.",
     "sigma_total=1.101; hl=exp(-1.101*23.09) -> ~-110 dB.", tol=0.03, tolType="abs")
calc(S1,1,"Atmospheric slant path L_atm at zeta=60 deg (elevation 30), H_atm=20 km. Give km.",
     H_ATM/math.cos(math.radians(60)),"km","L_atm=(H_atm-H_U)/cos(zeta); low passes traverse more atmosphere (1/cos).",
     "L_atm=20/cos60=40 km (double the zenith value).", tol=0.01)
calc(S1,1,"Binary entropy H2(0.11). Give the value (bits).",
     H2(0.11),"bits","H2(p)=-p log2 p-(1-p)log2(1-p); H2(0.11)=0.4999 -> why SKR=0 near QBER 11%.",
     "H2(0.11)=0.4999.", tol=0.01)
calc(S1,1,"Normalized SKR = Psift*[1-2*H2(QBER)] at Psift=0.5, QBER=0.0002 (v3, fEC=1, chiE=0). Give bit/s/Hz.",
     skr_norm(0.5,0.0002),"bit/s/Hz","SKR_norm=Psift[1-(1+fEC)H2(Q)-chiE]; EC-leakage term makes it hit 0 at Q~11%.",
     "H2(2e-4)~0.0027; 1-2*0.0027=0.9946; *0.5=0.497.", tol=0.03)
calc(S1,1,"Absolute SKR (Mbps) = SKR_norm * Rb, with SKR_norm=0.497 and Rb=1 Gbps. Give Mbps.",
     0.497*1e9/1e6,"Mbps","SKR_bps=SKR_norm*Rb; v3 @45 deg ~ 61 Mbps.",
     "0.497*1000 = 497 Mbps (illustrative; table value 61.4 uses the real Psift/QBER).", tol=0.03)
calc(S1,1,"Shot-noise DC signal power P = 0.5*P_T*hg*hl (v3, NO m_K), P_T=1 W, hg=3.9e-4, hl=0.0954. Give W.",
     0.5*1*3.9e-4*0.0954,"W","v3 fix: shot noise uses total DC photocurrent, not the m_K-scaled key power (was 20x too small).",
     "0.5*1*3.9e-4*0.0954 = 1.86e-5 W.", tol=0.03)
calc(S1,1,"Cross-talk suppression factor 10^(-Iso/10) at Iso=15 dB. Give the linear factor.",
     10**(-15/10),"(linear)","sigma_CT^2 ~ 10^(-Iso/10)/8; better isolation cuts the dominant noise.",
     "10^(-1.5)=0.0316.", tol=0.02)
calc(S1,1,"Rytov scaling: sec^(11/6)(60 deg) / sec^(11/6)(30 deg). Give the ratio.",
     (1/math.cos(math.radians(60)))**(11/6)/(1/math.cos(math.radians(30)))**(11/6),
     "(ratio)","sigma_R^2 ~ sec^(11/6)(zeta); turbulence worsens at low elevation.",
     "(2/1.1547)^(11/6)=2.74.", tol=0.02)
calc(S1,1,"Convert hg=2.6e-4 (linear) to dB.",
     10*math.log10(2.6e-4),"dB","dB = 10 log10(linear); geometric loss ~ -36 dB.",
     "10*log10(2.6e-4) = -35.8 dB.", tol=0.02, tolType="abs")

# =====================================================================
# SECTION 2 — Geometry & orbital calculations (calc)  [19..30]
# =====================================================================
S2 = "2. Geometry & orbits — calculate"
calc(S2,2,"Ground-coverage radius R_cov at 30 deg mask, H_S=550 km. Give km.",
     Rcov_km(30),"km","R_cov=R_E*psi, psi=arccos(R_E/(R_E+h) cos e)-e; the 950 km 'radius' in old paper was slant range.",
     "R_cov(30 deg)=793 km.", tol=0.02)
calc(S2,2,"Ground-coverage radius at the 40 deg security mask. Give km.",
     Rcov_km(40),"km","Stricter mask -> smaller footprint (~28% loss) but safer QBER.",
     "R_cov(40 deg)=573 km.", tol=0.02)
calc(S2,2,"Max station separation for a DUAL (shared-pass) city pair at 30 deg mask = 2*R_cov. Give km.",
     2*Rcov_km(30),"km","classify_pair: DUAL if distance <= 2*R_cov; the 14/14 split threshold.",
     "2*793 = 1587 km.", tol=0.02)
calc(S2,2,"Max DUAL separation at the 40 deg mask = 2*R_cov(40). Give km.",
     2*Rcov_km(40),"km","Stricter mask shrinks the DUAL threshold too.",
     "2*573 = 1146 km.", tol=0.02)
calc(S2,2,"Off-nadir angle eta at the satellite for elevation 30 deg. sin eta=R_E cos e/(R_E+h). Give deg.",
     off_nadir(30),"deg","Zero at zenith, grows as elevation drops; the transmit-side pointing angle.",
     "sin eta=6371*cos30/6921=0.797 -> eta=52.8 deg.", tol=0.02)
calc(S2,2,"Off-nadir angle at elevation 90 deg (zenith). Give deg.",
     off_nadir(90),"deg","At the station's zenith the line of sight IS the nadir direction.",
     "eta=0 deg.", tol=0.01, tolType="abs")
calc(S2,2,"Great-circle distance Hanoi (21.03N,105.85E) to HCMC (10.82N,106.63E) by haversine. Give km.",
     haversine(21.03,105.85,10.82,106.63),"km","haversine is symmetric; DUAL/SF classification uses this distance.",
     "~1140 km.", tol=0.03)
calc(S2,2,"Is Hanoi-HCMC (dist above) DUAL at 30 deg mask? Enter the max DUAL separation it is compared against (km).",
     2*Rcov_km(30),"km","Compare distance (~1140 km) to 2*R_cov(30)=1587 km -> DUAL (1140<1587).",
     "Threshold 1587 km; 1140<1587 -> DUAL.", tol=0.02)
calc(S2,2,"Elevation angle if zenith angle zeta=55 deg. Give deg.",
     90-55,"deg","elevation = 90 - zenith; the two complementary receive-side angles.",
     "90-55 = 35 deg.", tol=0.001, tolType="abs")
calc(S2,2,"Pass frequency per day if 125 passes are seen in a 2-hour window. freq=count*(24/hours).",
     125*(24/2),"passes/day","pass_frequency_per_day extrapolates the enumerated window.",
     "125*12 = 1500 passes/day.", tol=0.01)
calc(S2,2,"Number of unique city pairs among 8 ground stations = C(8,2). Give the count.",
     math.comb(8,2),"pairs","28 pairs to serve with 8 stations -> structural starvation.",
     "8*7/2 = 28.", tol=0.001, tolType="abs")
calc(S2,2,"Footprint area reduction going 30->40 deg mask: 1-(R_cov40/R_cov30)^2, as a percentage.",
     100*(1-(Rcov_km(40)/Rcov_km(30))**2),"%","Area ~ radius^2; the security mask's coverage cost.",
     "1-(573/793)^2 = ~48% area (about 28% radius).", tol=0.05)

# =====================================================================
# SECTION 3 — Weather & availability (calc + fill)  [31..42]
# =====================================================================
S3 = "3. Weather & availability"
calc(S3,3,"Link availability A at Kuala Lumpur, November (P_cloud=0.893). A=1-P_cloud.",
     1-0.893,"(fraction)","A=p_clear+p_rain=1-P_cloud; invariant to rain fraction; worst cell in the dataset.",
     "A=1-0.893=0.107 (10.7%).", tol=0.02)
calc(S3,3,"Link availability at Bangkok, February (P_cloud=0.035). Give fraction.",
     1-0.035,"(fraction)","Best cell; A=1-P_cloud=0.965; driven by cloud, not rain.",
     "A=0.965 (96.5%).", tol=0.01)
calc(S3,3,"Hourly rain rate from R_month=313.2 mm, f_rain=0.15. R=R_month/(30*24*f_rain). mm/h.",
     313.2/(30*24*0.15),"mm/h","Tropical rain is intermittent; intensity concentrates in raining hours.",
     "313.2/108 = 2.90 mm/h.", tol=0.02)
calc(S3,3,"Same conversion with the real f_rain=0.30 instead of 0.15. mm/h.",
     313.2/(30*24*0.30),"mm/h","Larger f_rain spreads rain over more hours -> lower instantaneous intensity.",
     "313.2/216 = 1.45 mm/h.", tol=0.02)
calc(S3,3,"p_rain=min(f_rain,1-P_cloud) with f_rain=0.30, P_cloud=0.893. Give p_rain.",
     min(0.30,1-0.893),"(fraction)","When cloud is very high, p_rain is capped by (1-P_cloud).",
     "min(0.30,0.107)=0.107.", tol=0.02)
calc(S3,3,"p_clear=max(0,1-P_cloud-p_rain) with P_cloud=0.5, f_rain=0.30. Give p_clear.",
     max(0,1-0.5-min(0.30,1-0.5)),"(fraction)","Three-state split; clear gets what's left after cloud and rain.",
     "p_rain=0.30; p_clear=1-0.5-0.30=0.20.", tol=0.02)
calc(S3,3,"Effective SKR = p_clear*SKR_clear + p_rain*SKR_rain, p_clear=0.20, SKR_clear=61, p_rain=0.30, SKR_rain=5 (Mbps).",
     0.20*61+0.30*5,"Mbps","Cloud state contributes 0; weighted average over clear+rain.",
     "0.20*61+0.30*5 = 13.7 Mbps.", tol=0.02)
fill(S3,3,"What ERA5 cloud-cover percentage threshold defines a 'cloudy hour' (link outage)? Give the number with % sign.",
     "85%", ["85%","85","85 percent","85 %"], "%","CLOUD_OUTAGE_THRESHOLD=85%; a modelling choice with a sensitivity analysis.")
fill(S3,3,"How many years of ERA5/ERA5-Land reanalysis calibrate the weather model? Give the number.",
     "10", ["10","10 years","ten","2015-2024","2015–2024"], "years","2015-2024; long record captures interannual variability.")
fill(S3,3,"In which local-hour window is the combined cloud+rain 'best FSO window'? (e.g. 05-10h)",
     "05-10h", ["05-10h","5-10","05:00-10:00","mid-morning","morning","5-10h","0510"], "local",
     "Cloud lowest mid-morning, rain peaks afternoon -> best window ~05-10h, in DAYLIGHT (day/night tension).")
fill(S3,3,"Which weather variable (not rain) governs tropical optical availability?",
     "cloud", ["cloud","cloud cover","cloud outage","clouds"], "",
     "Cloud is total optical blockage; rain only attenuates. The core meteorological finding.")
fill(S3,3,"The tropical rain-attenuation law (alpha=0.509, rho=0.63) was measured in which city?",
     "Abidjan", ["abidjan","abidjan cote d'ivoire","cote d'ivoire","ivory coast"], "",
     "Kone et al. 2024; real tropical FSO measurements, defensible under a remote-sensing examiner.")

# =====================================================================
# SECTION 4 — Fill key numbers & terms (fill)  [43..57]
# =====================================================================
S4 = "4. Key numbers & terms — fill in"
fill(S4,4,"v3 secret key rate at 45 deg elevation (give value with unit, e.g. '61.4 Mbps').",
     "61.4 Mbps", ["61.4 mbps","61.4","61,4","61 mbps","61.371 mbps","61.4mbps","61371 kbps"], "",
     "Table 6.1 v3 at m_K=0.15; up from pre-v3 13.3 Mbps after the /8 cross-talk fix.")
fill(S4,4,"v3 matching gain (ALG-1 vs ALG-0) in the dry season, as a percentage (e.g. +2.47%).",
     "+2.47%", ["+2.47%","2.47%","2.47","+2.47","2.5%"], "","Modest but real coordination gain over 620 enumerated days.")
fill(S4,4,"Sign of the weather-information gain (aware vs blind): positive or negative?",
     "negative", ["negative","neg","-","minus","cost"], "",
     "-0.29%/-0.23%: weather-awareness re-assigns more -> handovers outweigh the benefit.")
fill(S4,4,"Fraction of days with at least one starved city pair (range, e.g. 91.6-96.5%).",
     "91.6-96.5%", ["91.6-96.5%","91.6-96.5","92-96%","~92%","91.6","96.5"], "",
     "Structural (8 stations / 28 pairs), unchanged across every correction round.")
fill(S4,4,"Coverage radius at the 30 deg mask (km).",
     "793 km", ["793 km","793","793km"], "","Ground-track radius (NOT the 950 km slant range of the old paper).")
fill(S4,4,"Coverage radius at the 40 deg mask (km).",
     "573 km", ["573 km","573","573km"], "","~28% smaller footprint than 30 deg, for a safer QBER margin.")
fill(S4,4,"How many DUAL city pairs (of 28) can share one satellite pass?",
     "14", ["14","fourteen"], "pairs","The other 14 are store-and-forward; a clean geographic split.")
fill(S4,4,"Number of real Starlink Shell-1 satellites used.",
     "1019", ["1019","1,019","~1000","1000"], "satellites","Filtered by inclination 53.15-53.22 deg; real, reproducible TLEs.")
fill(S4,4,"Shell-1 orbital inclination (deg).",
     "53", ["53","53 deg","~53","53.15-53.22"], "deg","Covers ~95% of world population incl. all ASEAN; launch-efficient from Cape Canaveral.")
fill(S4,4,"Satellite altitude assumed throughout (km).",
     "550", ["550","550 km"], "km","The channel model is parameterised for this single altitude.")
fill(S4,4,"QKD carrier wavelength (nm).",
     "1550", ["1550","1550 nm","1.55 um"], "nm","Telecom C-band: eye-safe, low loss, mature components, weak aerosol scattering.")
fill(S4,4,"Corrected key modulation index m_K used in the thesis.",
     "0.15", ["0.15",".15","0,15"], "","Reset from 0.05 to the source manuscript's feasible value; drops QBER below 10^-3.")
fill(S4,4,"Filter isolation Iso between the key and data subcarriers (dB).",
     "15 dB", ["15 db","15","15dB"], "","Finite isolation lets the data channel leak in as cross-talk.")
fill(S4,4,"Real acquisition/handover cost charged per handover (seconds).",
     "30 s", ["30 s","30","30s","30 seconds"], "","Every re-assignment loses 30 s of delivered key (v3).")
fill(S4,4,"BB84 QBER security threshold above which no secret key can be distilled (%).",
     "11%", ["11%","11","~11"], "","1-2*H2(Q)=0 at Q~0.11; the Shor-Preskill threshold.")

# =====================================================================
# SECTION 5 — Committee & literature (match)  [58..72]
# =====================================================================
S5 = "5. Committee & literature — match"
match(S5,5,"Match each external examiner to their home research field.",
      {"Guillaume Patanchon (APC)":"CMB detector noise & component separation",
       "Stephane Jacquemoud (IPGP)":"Radiative transfer & remote sensing (PROSPECT)",
       "Cyrille Rosset (IN2P3/APC)":"Statistical significance (Planck isotropy)"},
      "Bridge each part of the thesis to the examiner's own field; they are space-science generalists, not QKD specialists.",
      "Examiner","Field")
match(S5,5,"Match each examiner to the bridge phrase you should use with them.",
      {"Jacquemoud":"'Beer-Lambert = atmospheric correction / radiative transfer'",
       "Patanchon":"'detector noise budget & cross-talk = component separation'",
       "Rosset":"'paired significance on a full enumeration + block bootstrap'"},
      "Speak each examiner's mother tongue; do not assume QKD fluency.","Examiner","Bridge")
match(S5,5,"Match each examiner to their toughest predicted question.",
      {"Jacquemoud":"Why is Beer-Lambert enough without multiple scattering?",
       "Patanchon":"Why does cross-talk dominate when the link is strong?",
       "Rosset":"Is +2.5% significant or within day-to-day scatter?"},
      "The three trap questions; master the MECHANISM, not just the number.","Examiner","Trap question")
match(S5,5,"Match each reference to its role in the thesis.",
      {"Vu et al. 2022 (vu2022dtdd)":"Noise model & dual-threshold (BBM92 provenance)",
       "Kone et al. 2024 (kone2024tropical)":"Tropical rain-attenuation calibration",
       "Polnik et al. 2020 (polnik2020scheduling)":"Nearest scheduling precedent",
       "Liao et al. 2017 (liao2017satellite)":"Micius: first satellite QKD from LEO"},
      "Each citation anchors one layer of the work; know which paper does what.","Reference","Role")
match(S5,5,"Match each reference to its role (set 2).",
      {"Andrews & Phillips 2005":"Rytov variance & H-V turbulence profile",
       "Leverrier 2015":"Composable CV-QKD proof (future work)",
       "Gruneisen et al. 2015":"Daytime sky-access for QKD downlink",
       "Open-Meteo / ERA5 (openmeteo2023)":"10-year real weather climatology"},
      "The physics, security, daytime, and weather anchors respectively.","Reference","Role")
match(S5,5,"Match each reference to its role (set 3 — SWaP, PAT & NTN).",
      {"Schieler et al. 2023 (TBIRD)":"Small-aperture SWaP comparison (0.4 m RX)",
       "Gerard et al. 2025 (PAT)":"Pointing/Acquisition/Tracking delay -> 30 s handover",
       "Farid & Hranilovic 2007":"Pointing-error term omitted (hg = lower bound)",
       "3GPP TR 38.821":"Non-terrestrial network (NTN) standardisation"},
      "The engineering/context anchors; each justifies one modelling choice or positioning.","Reference","Role")
match(S5,5,"Match each reference to its role (set 4 — QKD landscape).",
      {"Bennett & Brassard 1984":"BB84 protocol (the SKR rate's basis)",
       "Scarani et al. 2009":"Security of practical QKD",
       "Li et al. 2025 (Jinan-1)":"Microsatellite real-time QKD (cheap sats)",
       "Toka et al. 2025":"Weather-aware LEO routing (classical data)"},
      "Foundations, security framework, and the two nearest 'cheap-sats' / 'weather-aware' precedents.","Reference","Role")
match(S5,5,"Match each examiner to what they will most likely NOT probe deeply.",
      {"Son Tong Si (USTH generalist)":"Deep QKD math (asks motivation/big picture)",
       "Jacquemoud (remote sensing)":"The Hungarian algorithm internals",
       "Rosset (statistics)":"Beam-optics derivations"},
      "Audience analysis: aim answers at each examiner's strengths, keep others high-level.","Examiner","Unlikely focus")
fill(S5,5,"Which examiner did the internal supervisor name as the likely primary reviewer? (surname)",
     "Jacquemoud", ["jacquemoud","stephane jacquemoud"], "","IPGP radiative-transfer expert; will scrutinise the atmospheric model most.")
fill(S5,5,"Which classic model is Jacquemoud the author of? (acronym)",
     "PROSPECT", ["prospect","prosail","prospect/prosail"], "","Leaf radiative-transfer model 400-2500 nm; his home ground is extinction/attenuation.")
fill(S5,5,"Which satellite mission is the canonical 'first satellite QKD from LEO' you cite in the motivation?",
     "Micius", ["micius","liao 2017","liao"], "","Liao et al. 2017, Nature 549:43; the existence proof QKD works from orbit.")
fill(S5,5,"How many real references are catalogued in the literature review?",
     "34", ["34","thirty-four","~34"], "references","Built directly from the thesis references.bib, mapped to role + examiner.")
fill(S5,5,"In one word, the strategy with this non-QKD panel: report results with ___ (integrity vs. spin).",
     "integrity", ["integrity","honesty","transparency"], "","Flag limitations proactively; the maturity signal that wins a science panel.")
fill(S5,5,"Complete Jacquemoud's answer: 'I treat cloud as a ___ outage, so multiple scattering only refines an already-lost state.'",
     "binary", ["binary","binary/ off","off"], "","Concede Beer-Lambert is first-order; justify cloud=outage -> no multiple scattering needed.")
fill(S5,5,"Complete Rosset's answer: 'It is not a random sample — I ___ every day in two 10-year proxy months.'",
     "enumerate", ["enumerate","enumerated","full enumeration","count"], "",
     "Full enumeration (620 days) -> no sampling error; paired day-by-day test isolates the ~2.5% effect.")

# =====================================================================
# SECTION 6 — Reasoning, derivations & prepared answers (order + fill)  [73..90]
# =====================================================================
S6 = "6. Reasoning, derivations & defense answers"
order(S6,6,"Put the SIKD computation pipeline in the correct order.",
      ["channel (hg, hl, sigmaX^2)","noise budget (4 terms)","dual-threshold (d0,d1)",
       "Psift & QBER (Gauss-Hermite)","SKR (Shor-Preskill)"],[0,1,2,3,4],
      "compute_sikd_performance wrapper: each stage feeds the next; SKR is the end product.")
order(S6,6,"Order the FSO channel factors as applied from transmitter to receiver.",
      ["Transmitted power P_T","Geometric spreading h_g","Atmospheric attenuation h_l",
       "Turbulence fading h_a","Received power"],[0,1,2,3,4],
      "h = h_g * h_l * h_a; three independent multiplicative loss mechanisms.")
order(S6,6,"Order the three weather states by increasing severity of link impact.",
      ["Clear (attenuation only)","Rain (added attenuation)","Cloud (link OFF)"],[0,1,2],
      "Three-state model; cloud is binary outage, not gradual attenuation.")
order(S6,6,"Order the two-level scheduling problem's steps.",
      ["Station-satellite matching (Hungarian)","Build matched pass table",
       "Pair-key allocation (greedy/ILP/maxmin)","K_q = min(sideA, sideB)"],[0,1,2,3],
      "Level 1 matching -> level 2 allocation on a shared trusted-relay satellite.")
order(S6,6,"Rank the v3 noise terms by when cross-talk dominates (weak link -> strong link).",
      ["Thermal noise (floor, weak link)","Shot noise (grows with power)","Cross-talk (~P^2, strong link)"],[0,1,2],
      "Cross-talk ~ received power squared -> dominates exactly when the link is strongest.")
fill(S6,6,"Complete the identity that makes log-normal fading energy-conserving: mu_X = ____ (in terms of sigma_X^2).",
     "-sigma_X^2", ["-sigma_x^2","-sigmax2","-sigma_x2","-sigmaX^2","minus sigma_x^2","-\\sigma_X^2","-sx2"], "",
     "E[e^{2X}]=exp(2 mu_X+2 sigma_X^2)=1 requires mu_X=-sigma_X^2 (unit-mean multiplicative fading).")
fill(S6,6,"The secret-key formula reaches zero at QBER = ___ % (fEC=1, chiE=0). Give the percentage.",
     "11%", ["11%","11","~11"], "","1-2*H2(Q)=0 at Q~0.11; the term added in the v3 SKR fix restores this.")
fill(S6,6,"Cross-talk variance scales as received power to the power ___ (give the exponent).",
     "2", ["2","squared","two","^2","P^2"], "","sigma_CT^2 ~ (h_g h_l)^2 -> P^2; the counter-intuitive SIKD result.")
fill(S6,6,"The v3 cross-talk coefficient changed from /2 to /___ (give the number).",
     "8", ["8","/8","eight"], "","Photocurrent's leading 1/2 makes amplitude (1/2)(...); variance A^2/2 -> /8.")
fill(S6,6,"Delivered pair key is a ___() over the pair path (one word/function), capping the gain.",
     "min", ["min","minimum","min()"], "","K_q=min(sideA,sideB); one weak link caps the improvement -> structural ceiling.")
fill(S6,6,"Complete the defense answer: 'Weather-awareness costs because it re-assigns more often and the extra ___ outweigh the benefit.'",
     "handovers", ["handovers","handover","re-acquisitions","acquisitions"], "",
     "Measured mechanism (I counted the handovers directly), not a bug; small, same sign both seasons.")
fill(S6,6,"Complete: 'Pair-starvation is a ___-planning finding, not an algorithm failure.'",
     "capacity", ["capacity","capacity-planning"], "","8 stations cannot serve 28 pairs; the fix is more infrastructure.")
fill(S6,6,"Which algorithm solves the station-satellite matching EXACTLY? (name)",
     "Hungarian", ["hungarian","hungarian algorithm","linear_sum_assignment"], "",
     "match_weather_aware uses scipy linear_sum_assignment on the negated weight matrix.")
fill(S6,6,"In one word, the trusted-relay assumption requires the satellite node to be ___.",
     "trusted", ["trusted","honest","not compromised","uncompromised"], "",
     "The relay learns both keys; security holds only if the relay itself is honest.")
fill(S6,6,"Complete the one-line thesis claim: 'Judge these networks at the ___ level, not by a single clear-sky link rate.'",
     "network", ["network","network-level","system"], "","The central claim; a shift in the unit of evaluation.")
fill(S6,6,"Vu et al. 2022 implements which protocol (not BB84)? Give the acronym.",
     "BBM92", ["bbm92","bbm-92"], "","The provenance caveat: the 11% BB84 bound is a borrowed, openly-stated assumption.")
order(S6,6,"Order the four v3 fixes by the stage they touch (channel -> receiver).",
      ["erf coefficient sqrt(2)->sqrt(pi/2)","spherical slant range","Rytov 0.56->2.25","cross-talk /2->/8"],[0,1,2,3],
      "Three geometric/turbulence fixes in the channel, then the receiver cross-talk fix (largest impact).")
fill(S6,6,"The daytime-background penalty is described as an 'order-of-___ estimate', not a proof. (one word)",
     "magnitude", ["magnitude","order-of-magnitude"], "","Honest confidence labelling; a plausibility bound from an FOV sweep, not a full simulation.")

# ---- emit ----
sections = []
seen = set()
for e in ex:
    if e["sectionNum"] not in seen:
        seen.add(e["sectionNum"])
        sections.append({"num": e["sectionNum"], "title": e["section"],
                         "count": sum(1 for x in ex if x["sectionNum"] == e["sectionNum"])})

assert len(ex) == 90, f"expected 90, got {len(ex)}"
# attach rich per-exercise explanations
_missing=[e["id"] for e in ex if e["id"] not in DETAILS]
if _missing: raise SystemExit(f"DETAILS missing for ids {_missing}")
for e in ex:
    e["detail"] = DETAILS[e["id"]]
payload = {"meta": {"title": "SIKD Thesis M1 — 90 Active-Recall Exercises",
                    "total": len(ex), "sections": sections}, "exercises": ex}
json.dump(payload, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK: {len(ex)} exercises -> {OUT}")
from collections import Counter
print("types:", dict(Counter(e["type"] for e in ex)))
for s in sections:
    print(f"  S{s['num']}  n={s['count']:>2}  {s['title']}")
