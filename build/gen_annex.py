#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate SIKD_Annex_Compendium.tex — the long appendix that gathers EVERY
formula, coefficient and description behind the results and the interactive site.
Formula sections A-H are curated (grounded in 05_Code_v3 and the Tu-hoc guides);
the symbol glossary (I) and the website-implementation index (J) are generated
from the exact same JSON the site serves, so nothing on the site is missed."""
import json, os

DATA = "/Users/tuannghiat/for-ttn-USTH/Thesis-M1/data"
OUT = "/Users/tuannghiat/Downloads/Bài Quantum Communication PTIT /11_Slides_Thesis/SIKD_Annex_Compendium.tex"

symbols = json.load(open(f"{DATA}/symbols.json", encoding="utf-8"))["symbols"]
ex = json.load(open(f"{DATA}/exercises.json", encoding="utf-8"))
qs = json.load(open(f"{DATA}/questions.json", encoding="utf-8"))

def esc(s):
    s = str(s)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("#", r"\#"),
                 ("_", r"\_"), ("{", r"\{"), ("}", r"\}"), ("~", r"\textasciitilde{}"),
                 ("^", r"\textasciicircum{}"), ("$", r"\$")]:
        s = s.replace(a, b)
    return s


_UNI = [("m⁻²ᐟ³","$^{-2/3}$"),("10⁻¹⁴","$^{-14}$"),("10⁻¹³","$^{-13}$"),("10⁻¹⁷","$^{-17}$"),
        ("10⁻³","$^{-3}$"),("km⁻¹","$^{-1}$"),("2H₂","2H$_2$"),("H₂","H$_2$"),
        ("log₂p","$\\log_2 p$"),("log₂","$\\log_2$"),("w₀","$w_0$"),
        ("∝","$\\propto$"),("≫","$\\gg$"),("≳","$\\gtrsim$")]
def gl(x):
    x = esc(x)
    # fix the number-prefixed superscripts: put the base outside math
    x = x.replace("m⁻²ᐟ³","m$^{-2/3}$").replace("10⁻¹⁴","$10^{-14}$").replace("10⁻¹³","$10^{-13}$")
    x = x.replace("10⁻¹⁷","$10^{-17}$").replace("10⁻³","$10^{-3}$").replace("km⁻¹","km$^{-1}$")
    x = x.replace("2H₂","2H$_2$").replace("H₂","H$_2$")
    x = x.replace("log₂p","$\\log_2 p$").replace("log₂","$\\log_2$").replace("w₀","$w_0$")
    x = x.replace("∝","$\\propto$").replace("≫","$\\gg$").replace("≳","$\\gtrsim$")
    return x

L = []
A = L.append

A(r"""\documentclass[11pt,a4paper]{article}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage{amsmath,amssymb}
\usepackage{geometry}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage{hyperref}
\geometry{margin=2cm,headheight=14pt}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{SIKD Annex --- Formula \& Implementation Compendium}
\fancyhead[R]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{4pt}
\newcommand{\desc}[1]{{\small\color{blue!45!black}#1}}
\title{\textbf{Annex --- Formula \& Implementation Compendium}\\[0.3cm]
\large Weather-Aware SIKD over Tropical Satellite Free-Space Optical Channels\\[0.2cm]
\normalsize Every formula, coefficient, and quantity behind the results and the interactive study site.\\[0.1cm]
\small Truong Tuan Nghia (2540017), USTH Master Space --- M1 internship. Companion to the defense slides.}
\author{}\date{}
\begin{document}\maketitle
\begin{abstract}\noindent
This annex consolidates the complete mathematical machinery of the thesis: the SIKD signal and
channel model, the dual-threshold receiver, the three-state weather model, the coverage geometry,
the two-level scheduling formulation, the inter-satellite-link relay, and the key/data power-split,
together with every coefficient and a glossary of all physical quantities (value, typical range,
rationale). Sections A--H are the curated derivations (source: \texttt{05\_Code\_v3/modules} and the
self-study guides in \texttt{Tu-hoc/SIKD\_Satellite\_QKD}); Sections I--J are generated directly from
the data served by the interactive site (\url{https://tatcataittn.github.io/for-ttn-USTH/Thesis-M1}),
so every online implementation is indexed here.
\end{abstract}
\tableofcontents
\newpage

\section{Master parameter and coefficient table}
All defaults are the corrected v3 values ($m_K=0.15$).
\begin{center}\small\renewcommand{\arraystretch}{1.2}
\begin{longtable}{@{}lll@{}}
\toprule \textbf{Symbol} & \textbf{Value} & \textbf{Meaning} \\ \midrule
$\lambda$ & 1550 nm & carrier wavelength (telecom C-band) \\
$\theta_C$ & 10 $\mu$rad & beam divergence half-angle \\
$a_R$ & 0.05 m & receiver aperture radius \\
$H_S$ & 550 km & satellite altitude (Starlink Shell-1) \\
$H_\text{atm}$ & 20 km & effective atmospheric height \\
$R_E$ & 6371 km & mean Earth radius \\
$W$ & 21 m/s & high-altitude wind (Hufnagel--Valley) \\
$C_n^2(0)$ & $1.7\times10^{-14}$ m$^{-2/3}$ & ground turbulence strength \\
$R_e$ & 0.9 A/W & InGaAs PIN responsivity \\
$T$ & 280 K & receiver temperature \\
$R_L$ & 1 k$\Omega$ & load resistance \\
$R_b$ & 1 Gbps & raw bit rate ($\Delta f=R_b/2$) \\
$P_{bg}$ & 0 & background power (night operation) \\
$\mathrm{Iso}$ & 15 dB & subcarrier filter isolation \\
$P_T$ & 1 W (30 dBm) & transmit optical power \\
$m_K$ & 0.15 & key-channel modulation index \\
$m_D$ & 0.5 & data-channel modulation index \\
$\zeta_\text{scale}$ & 2.0 & dual-threshold scale factor \\
$N_\text{GH}$ & 20 & Gauss--Hermite quadrature order \\
$\alpha,\rho$ & 0.509, 0.63 & tropical rain law (Kon\'e 2024, Abidjan) \\
Cloud threshold & 85\% & cloud-cover outage threshold \\
Rain-hour threshold & 0.1 mm/h & measurable-precipitation threshold \\
Record & 2015--2024 (10 yr) & ERA5/ERA5-Land, 8 cities \\
Handover cost & 30 s & real acquisition time per re-assignment \\
ISL hop latency & 30 s & conservative on-board relay overhead \\
QBER$_\text{max}$ & 11\% & BB84 Shor--Preskill security threshold \\
\bottomrule
\end{longtable}\end{center}

\section{SIKD signal and FSO channel model}
\textbf{Received SCM photocurrent} (direct detection):
\[ i_r(t)=\tfrac12 R_e P_T\,h(t)\big[\,1+m_K s_K(t)+m_D s_D(t)\,\big]+n(t) \]
\desc{One 1550 nm carrier multiplexes the quantum key ($f_1,m_K$) and classical data ($f_2,m_D$); both share one photodetector, so $s_D$ returns as cross-talk.}

\textbf{Composite channel:} $h=h_g\cdot h_l\cdot h_a$ (geometric $\times$ atmospheric $\times$ turbulence).

\subsection{Geometric spreading}
\[ w_0=\frac{\lambda}{2\theta_C},\qquad w_L=w_0\sqrt{1+\Big(\frac{L\lambda}{\pi w_0^2}\Big)^2},\qquad h_g=[\mathrm{erf}(\nu_R)]^2,\quad \nu_R=\sqrt{\tfrac{\pi}{2}}\,\frac{a_R}{w_L} \]
Spherical slant range (elevation $\varepsilon=90^\circ-\zeta$):
\[ L=\sqrt{R_E^2\sin^2\varepsilon+2R_E H_S+H_S^2}-R_E\sin\varepsilon \]
\desc{v3 fixes: $\nu_R$ coefficient $\sqrt2\to\sqrt{\pi/2}$; slant range flat-Earth $\to$ spherical (992.8 km, not 1100 km, at $\varepsilon=30^\circ$). $h_g$ exceeds 30 dB alone.}

\subsection{Atmospheric attenuation (Beer--Lambert)}
\[ h_l=\exp\!\big[-(\sigma_\text{clear}+\sigma_\text{rain})L_\text{atm}\big],\qquad L_\text{atm}=\frac{H_\text{atm}-H_U}{\cos\zeta} \]
Clear air (Kruse/Kim): $\displaystyle\sigma_\text{clear}=\frac{3.912}{V}\Big(\frac{\lambda}{550}\Big)^{-q(V)}$, with $q(V)=1.6\,(V{>}50)$; $1.3\,(6{<}V{\le}50)$; $0.16V{+}0.34\,(1{<}V{\le}6)$; $V{-}0.5\,(0.5{<}V{\le}1)$; $0$ else.\\
Rain (tropical): $\sigma_\text{rain}=\alpha R^\rho/4.343$, $\alpha=0.509$, $\rho=0.63$; $4.343=10/\ln10$ (dB$\to$Neper).
\desc{Independent extinction mechanisms add in the exponent; $V=15-10P_\text{cloud}$ is derived (no ERA5 visibility variable).}

\subsection{Turbulence (weak, log-normal)}
Hufnagel--Valley 5/7 profile:
\[ C_n^2(h)=0.00594\Big(\tfrac{W}{27}\Big)^2(10^{-5}h)^{10}e^{-h/1000}+2.7\times10^{-16}e^{-h/1500}+C_n^2(0)e^{-h/100} \]
Rytov variance and log-amplitude variance:
\[ \sigma_R^2=2.25\,k^{7/6}\sec^{11/6}(\zeta)\!\int_{H_U}^{H_S}\!C_n^2(h)(h-H_U)^{5/6}dh,\qquad \sigma_X^2=\sigma_R^2/4 \]
Fading: $h_a=\exp(2X)$, $X\sim\mathcal N(-\sigma_X^2,\sigma_X^2)$ (so $E[h_a]=1$); log-normal while $\sigma_R^2<0.3$, else Gamma--Gamma.
\desc{v3 fix: Rytov coefficient $0.56\to2.25$ (plane-wave slant path). The slant path stays weak, so log-normal holds throughout.}

\section{Receiver: noise, sifting, QBER and secret key rate}
\textbf{Noise budget} ($\Delta f=R_b/2$):
\[ \sigma_N^2=\underbrace{2qR_e\big(\tfrac12 P_T h_g h_l\big)\Delta f}_{\text{shot}}+\underbrace{\tfrac{4k_BT}{R_L}\Delta f}_{\text{thermal}}+\underbrace{2qR_e P_{bg}\Delta f}_{\text{background}}+\underbrace{\tfrac18(R_e P_T m_D h_g h_l)^2 10^{-\mathrm{Iso}/10}}_{\text{cross-talk}} \]
\desc{v3 fixes: shot noise uses the total DC photocurrent (no $m_K$); cross-talk denominator $/2\to/8$. Cross-talk $\propto$ power$^2$, so it dominates a strong link (0.5--290$\times$ thermal across elevation).}

\textbf{Dual-threshold decision} ($i_\text{mean}=\tfrac12 R_e G_k P_T m_K h_g h_l$):
\[ d_0=-i_\text{mean}-\zeta_\text{scale}\sigma_N,\qquad d_1=+i_\text{mean}+\zeta_\text{scale}\sigma_N \]
\textbf{Sift probability and QBER} (20-point Gauss--Hermite over fading):
\[ P_\text{sift}=\tfrac12(P_{00}+P_{11}+P_{10}+P_{01}),\qquad \text{QBER}=\frac{\tfrac12(P_{10}+P_{01})}{P_\text{sift}} \]
\textbf{Secret key rate} (Shor--Preskill / Devetak--Winter, $f_{EC}=1$):
\[ \text{SKR}_\text{norm}=P_\text{sift}\big[\,1-(1+f_{EC})H_2(\text{QBER})-\chi_E\,\big]=P_\text{sift}\big[1-2H_2(\text{QBER})-\chi_E\big],\quad \text{SKR}=\text{SKR}_\text{norm}R_b \]
with $H_2(p)=-p\log_2 p-(1-p)\log_2(1-p)$, $=0$ at QBER $\approx11\%$.
\desc{v3 fix: the error-correction leakage term $f_{EC}H_2(\text{QBER})$ was missing; it makes SKR vanish at the BB84 threshold. Baseline $\chi_E=0$.}

\textbf{Classical data BER:} $\displaystyle\text{BER}_{CC}=\frac{1}{\sqrt\pi}\sum_{k}w_k\,Q\!\Big(\frac{A_0 h_{a,k}}{\sigma_{N,D}}\Big)$, $A_0=G_d R_e P_T m_D h_g h_l$.

\section{Three-state weather model and availability}
\[ p_\text{rain}=\min(f_\text{rain},1-P_\text{cloud}),\quad p_\text{clear}=\max(0,1-P_\text{cloud}-p_\text{rain}),\quad p_\text{cloud}=P_\text{cloud} \]
\[ \text{SKR}_\text{eff}=p_\text{clear}\text{SKR}_c+p_\text{rain}\text{SKR}_r,\qquad A=p_\text{clear}+p_\text{rain}=1-P_\text{cloud} \]
Rain rate: $R_\text{mm/h}=R_\text{month}/(30\cdot24\cdot f_\text{rain})$.\\
Statistics: $P_\text{cloud}$ = fraction of hours with cloud cover $\ge85\%$; $f_\text{rain}$ = fraction with precip $\ge0.1$ mm/h; inter-city Pearson correlation of daily cloud; joint-clear probability from the joint record.
\desc{Cloud is a binary outage; $A$ is invariant to $f_\text{rain}$. Availability spans 10.7\% (Kuala Lumpur, Nov) to 96.5\% (Bangkok, Feb). Best combined FSO window: mid-morning ($\sim$05:00--10:00).}

\section{Coverage geometry and city-pair feasibility}
\[ R_\text{cov}=R_E\Big[\arccos\!\Big(\tfrac{R_E}{R_E+H_S}\cos\varepsilon\Big)-\varepsilon\Big],\qquad \text{DUAL if } d\le 2R_\text{cov}\ \text{else store-and-forward} \]
Great-circle distance (haversine): $d=2R_E\arcsin\sqrt{\sin^2\tfrac{\Delta\varphi}{2}+\cos\varphi_1\cos\varphi_2\sin^2\tfrac{\Delta\lambda}{2}}$.\\
Off-nadir angle: $\sin\eta=R_E\cos\varepsilon/(R_E+H_S)$. Slant range: $\sqrt{(R_E+H_S)^2-(R_E\cos\varepsilon)^2}-R_E\sin\varepsilon$.\\
Directed store-and-forward latency: median time from a pass over $i$ to the same satellite's next pass over $j$ (asymmetric).
\desc{$R_\text{cov}=793$ km ($30^\circ$), 573 km ($40^\circ$). The 28 ASEAN pairs split 14 DUAL / 14 store-and-forward --- a geographic ceiling.}

\section{Weather-aware scheduling and pair-key allocation}
\textbf{Level 1 --- matching} (Hungarian, per step $t$):
\[ \max_x\ \sum_{g,s} w_{g,s}(t)\,x_{g,s}(t)-c_h\!\sum_g\mathbf{1}[\text{handover}],\quad \sum_s x_{g,s}\le1,\ \sum_g x_{g,s}\le1,\ x=0\ \text{if not visible} \]
weight $w_{g,s}=\text{SKR}_\text{eff}$.\\
\textbf{Level 2 --- pair key} (trusted relay, satellite broadcasts $k_A\oplus k_B$):
\[ K_q=\min\Big(\sum_{p:\,\text{station}(p)=A} k_p y_{p,q},\ \sum_{p:\,\text{station}(p)=B} k_p y_{p,q}\Big),\qquad k_p=w\cdot(t_\text{set}-t_\text{rise}) \]
Strategies: ALG-0 (sticky elevation-priority baseline; ALG-0-feasible resolves double-booking); ALG-1 (weather-aware Hungarian matching, blind vs aware); ALG-2 (pass-to-pair allocation: greedy deficit rule, MILP/HiGHS, or max-min water-filling).
\desc{Fair comparison at equal resources over 620 real days: matching gain $+2.47/+2.48\%$; weather-info gain $-0.29/-0.23\%$; pair-starvation 91.6--96.5\%. Handover cost carried across segments (median 3.3 s).}

\section{Inter-satellite-link relay and key/data power-split}
\textbf{ISL multi-hop relay.} BFS hop distance on the static ``+Grid'' mesh; a drop-off pass is feasible if $t_\text{rise}\ge t_\text{pick}+n_\text{hops}\cdot30\,\text{s}$. \emph{time-optimal} = earliest feasible; \emph{capacity-optimal} = highest-elevation (highest-SKR) within $3\times$ the time-optimal latency. Replaces single-hop store-and-forward (worst case $\sim$711 min) with 2.9--4.1 min.\\[3pt]
\textbf{Power-split.} Two-way cross-talk $\sigma_\text{CT}^2=(R_e P_T m_\text{leak} h_g h_l)^2 10^{-\mathrm{Iso}/10}/8$ ($m_\text{leak}=m_D$ into key, $m_K$ into data). Data goodput $=R_b(1-\text{BER})$; constraint $m_K+m_D\le1$. Pareto frontier over $(m_K,m_D)$; adaptive split picks the smallest $m_K$ with $\text{SKR}\cdot10^3\cdot T_\text{pass}\ge K_\text{req}$.
\desc{Raising $m_D$ improves data throughput but $\sigma_\text{CT}^2\propto m_D^2$ raises key QBER --- the central SIKD coupling.}
""")

# ---------- Section I: symbol glossary (from symbols.json) ----------
A(r"\section{Glossary of physical quantities}")
A(r"For each quantity: meaning, this project's value, the typical range and why it is chosen, and how that range differs across fields (as served by the interactive site).")
A(r"\begin{itemize}[leftmargin=1.2em,itemsep=4pt]")
for sy in symbols:
    A(r"\item \textbf{%s} --- \textbf{%s.} %s \\ \desc{\textbf{This project:} %s\quad \textbf{Typical range:} %s} \\ \desc{\textbf{Why:} %s} \\ \desc{\textbf{Across fields:} %s}" % (
        gl(sy["sym"]), gl(sy["name"]), gl(sy["meaning"]),
        gl(sy["value"]), gl(sy["range"]), gl(sy["why"]), gl(sy["domain"])))
A(r"\end{itemize}")

# ---------- Section J: website implementation index ----------
A(r"\section{Index of website implementations (nothing omitted)}")
A(r"The interactive site implements every item below; each is backed by the formulas above.")

# 90 active-recall by section
A(r"\subsection{Active-recall exercises (90) --- 6 sections}")
secs = ex["meta"]["sections"]
A(r"\begin{center}\small\begin{longtable}{@{}clc@{}}\toprule \textbf{\#} & \textbf{Section} & \textbf{Items} \\ \midrule")
import re as _re
for s in secs:
    A(r"S%d & %s & %d \\" % (s["num"], esc(_re.sub(r'^\d+\.\s*', '', s["title"])), s["count"]))
A(r"\bottomrule\end{longtable}\end{center}")
A(r"Every calc item's numeric answer is computed from the formulas in Sections B--H (never hand-typed); fill/match/order items encode the coefficients, references and reasoning above.")

# 360 MCQ by perspective
A(r"\subsection{Multiple-choice questions (360) --- 11 professional perspectives}")
A(r"\begin{center}\small\begin{longtable}{@{}clc@{}}\toprule \textbf{P} & \textbf{Perspective} & \textbf{Items} \\ \midrule")
for pmeta in qs["meta"]["perspectives"]:
    A(r"P%d & %s & %d \\" % (pmeta["num"], esc(pmeta["title"]), pmeta["count"]))
A(r"\bottomrule\end{longtable}\end{center}")
A(r"Perspective 11 (Figure/Video reading) is backed by the result figures; all others by Sections A--H. Full text, answers and one-line theory frameworks are available on the site and in the self-study guides.")

A(r"""\section*{Sources}
\addcontentsline{toc}{section}{Sources}
Curated derivations: \texttt{05\_Code\_v3/modules/} and \texttt{Tu-hoc/SIKD\_Satellite\_QKD/Study\_Materials/}
(\texttt{SIKD\_Formula\_Guide\_v3\_Expanded}). Data-driven sections generated from the site's
\texttt{symbols.json}, \texttt{exercises.json}, \texttt{questions.json}. Live site:
\url{https://tatcataittn.github.io/for-ttn-USTH/Thesis-M1}.
\end{document}""")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write("\n".join(L))
print("wrote", OUT)
print("glossary entries:", len(symbols), "| exercise sections:", len(secs), "| MCQ perspectives:", len(qs["meta"]["perspectives"]))
