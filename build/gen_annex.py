#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate SIKD_Annex_Compendium.tex — the FULL appendix: master parameters, every
formula with derivation, the 30-quantity glossary, ALL 90 recall exercises and ALL
360 multiple-choice questions with their answers and explanations (the 450 items on
the interactive site), plus the thesis annexes (reproducibility, full robustness
detail, extended SIKD model, corrections history). Data sections are generated from
the same JSON the site serves; annex sections are transcribed from 10_Thesis_Shorten_v2."""
import json, os, re

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

def tq(s):
    """Escape text, rendering `code` spans as \\texttt and a few unicode math glyphs."""
    parts = str(s).split("`")
    out = []
    for i, p in enumerate(parts):
        out.append(r"\texttt{" + esc(p) + "}" if i % 2 == 1 else esc(p))
    t = "".join(out)
    for a, b in [("→", r"$\rightarrow$"), ("×", r"$\times$"), ("≈", r"$\approx$"),
                 ("≤", r"$\le$"), ("≥", r"$\ge$"), ("−", "-"), ("·", r"$\cdot$"),
                 ("μ", r"$\mu$"), ("σ", r"$\sigma$"), ("λ", r"$\lambda$"), ("θ", r"$\theta$"),
                 ("ζ", r"$\zeta$"), ("ε", r"$\varepsilon$"), ("π", r"$\pi$"), ("ν", r"$\nu$"),
                 ("χ", r"$\chi$"), ("Δ", r"$\Delta$"), ("∝", r"$\propto$"), ("≪", r"$\ll$"),
                 ("≳", r"$\gtrsim$"), ("√", r"$\surd$"), ("²", r"\textsuperscript{2}"),
                 ("ₖ", r"\textsubscript{k}"), ("₂", r"\textsubscript{2}"), ("₁", r"\textsubscript{1}"), ("₀", r"\textsubscript{0}"), ("⁻", r"\textsuperscript{-}"), ("⁵", r"\textsuperscript{5}"), ("³", r"\textsuperscript{3}"), ("≫", r"$\gg$"), ("⊕", r"$\oplus$"), ("∈", r"$\in$"), ("°", r"$^\circ$")]:
        t = t.replace(a, b)
    return t

def gl(x):
    x = esc(x)
    x = x.replace("m⁻²ᐟ³", "m$^{-2/3}$").replace("10⁻¹⁴", "$10^{-14}$").replace("10⁻¹³", "$10^{-13}$")
    x = x.replace("10⁻¹⁷", "$10^{-17}$").replace("10⁻³", "$10^{-3}$").replace("km⁻¹", "km$^{-1}$")
    x = x.replace("2H₂", "2H$_2$").replace("H₂", "H$_2$")
    x = x.replace("log₂p", "$\\log_2 p$").replace("log₂", "$\\log_2$").replace("w₀", "$w_0$")
    x = x.replace("∝", "$\\propto$").replace("≫", "$\\gg$").replace("≳", "$\\gtrsim$")
    return x

L = []
A = L.append

# ============================ PREAMBLE ============================
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
\usepackage{needspace}
\usepackage[hidelinks]{hyperref}
\geometry{margin=2cm,headheight=15pt}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\footnotesize SIKD Annex --- Formula, Explanation \& Implementation Compendium}
\fancyhead[R]{\footnotesize\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\setlength{\parindent}{0pt}\setlength{\parskip}{3pt}
\definecolor{qc}{RGB}{20,60,110}
\definecolor{ac}{RGB}{19,122,63}
\newcommand{\desc}[1]{{\small\color{blue!45!black}#1}}
\newcommand{\qid}[2]{\needspace{3\baselineskip}{\color{qc}\textbf{#1}}\ #2}
\newcommand{\ans}[1]{{\color{ac}\textbf{Answer:}} #1}
\newcommand{\fw}[1]{{\small\textit{Framework:} #1}}
\title{\textbf{\Large Annex --- Formula, Explanation \& Implementation Compendium}\\[0.3cm]
\large Weather-Aware SIKD over Tropical Satellite Free-Space Optical Channels\\[0.2cm]
\normalsize The complete reference behind the results, the defense, and the interactive study site:\\
every formula and coefficient, all 450 questions with answers and explanations, and the thesis annexes.\\[0.15cm]
\small Truong Tuan Nghia (2540017), USTH Master Space Program --- M1 internship. Supervisors: Dr.\ Vu Quang Minh (QTALab, PTIT), Dr.\ Phan Thanh Hien (USTH).}
\author{}\date{}
\begin{document}\maketitle
\begin{abstract}\noindent
This annex is the exhaustive companion to the report and the defense. Part~I gives the master
parameter set and every governing equation with its derivation and coefficients. Part~II is the
30-quantity glossary (value, typical range, rationale, cross-field comparison). Part~III reproduces,
in full, the \textbf{450 questions} of the interactive study site --- 90 active-recall exercises with
worked answers and detailed explanations, and 360 multiple-choice questions across 11 professional
perspectives with answers and one-line theory frameworks. Part~IV transcribes the thesis annexes:
reproducibility and code structure, the full numerical-robustness detail (correlation, significance,
autocorrelation, handover cost, optimality benchmark, correction history), the extended SIKD signal
model, and the equatorial-season and publication notes. Sources: \texttt{05\_Code\_v3/modules},
\texttt{10\_Thesis\_Shorten\_v2}, \texttt{Tu-hoc/SIKD\_Satellite\_QKD}, and the site's
\texttt{symbols.json}/\texttt{exercises.json}/\texttt{questions.json}
(\url{https://tatcataittn.github.io/for-ttn-USTH/Thesis-M1}).
\end{abstract}
\tableofcontents
\newpage

\part{Formulas, Coefficients and Derivations}

\section{Master parameter and coefficient reference}
\begin{center}\small\renewcommand{\arraystretch}{1.15}
\begin{longtable}{@{}lll@{}}
\toprule \textbf{Parameter} & \textbf{Symbol} & \textbf{Value} \\ \midrule \endhead
Wavelength & $\lambda$ & 1550 nm (telecom C-band) \\
Satellite altitude & $H_S$ & 550 km (Starlink Shell-1) \\
Transmit power & $P_T$ & 1 W (30 dBm) \\
QKD modulation index & $m_K$ & 0.15 (corrected v3 baseline) \\
Data modulation index & $m_D$ & 0.5 \\
RF bandpass filter isolation & $I_\text{so}$ & 15 dB \\
Bit rate & $R_b$ & 1 Gbps ($\Delta f=R_b/2$) \\
Receiver aperture radius & $a_R$ & 0.05 m \\
Beam divergence half-angle & $\theta_C$ & 10 $\mu$rad \\
Effective atmospheric height & $H_\text{atm}$ & 20 km \\
Mean Earth radius & $R_E$ & 6371 km \\
High-altitude wind (H--V) & $W$ & 21 m/s \\
Ground turbulence & $C_n^2(0)$ & $1.7\times10^{-14}$ m$^{-2/3}$ \\
Rytov variance (operational $\zeta$) & $\sigma_R^2$ & 0.057 to 0.203 \\
Responsivity (InGaAs PIN) & $R_e$ & 0.9 A/W \\
Receiver temperature & $T$ & 280 K \\
Load resistance & $R_L$ & 1 k$\Omega$ \\
Background optical power & $P_\text{bg}$ & 0 W (night-time) \\
Rain-attenuation coefficients & $\alpha,\rho$ & 0.509, 0.63 (Kon\'e 2024, Abidjan) \\
Rain-hour fraction & $f_\text{rain}(c,m)$ & 0.047 to 0.620 (mean 0.308) \\
Cloud-outage threshold & & 85\% cloud cover \\
Rain-hour threshold & & 0.1 mm/h \\
Reanalysis record & & ERA5/ERA5-Land, 2015--2024 (10 yr), 8 cities \\
Elevation mask (geometric / secure) & $\varepsilon$ & $30^\circ$ / $40^\circ$ \\
BB84 security threshold & QBER$_\text{max}$ & 11\% \\
Ground stations & $|\mathcal G|$ & 8 \\
Constellation subset & $|\mathcal S|$ & 1,019 (Shell-1) \\
DT threshold-scale coefficient & $\kappa$ & 2.0 \\
Gauss--Hermite order & $N$ & 20 \\
Handover penalty (calibrated) & $c_h$ & 1{,}841{,}142 kbps-equivalent (30 s) \\
Full-enumeration window & & 620 days (Jan + Jul, 2015--2024) \\
ISL per-hop latency & & 30 s (conservative) \\
\bottomrule
\end{longtable}\end{center}

\section{SIKD signal and FSO channel model}
\textbf{Received SCM photocurrent} (direct detection):
\[ i_r(t)=\tfrac12 R_e P_T\,h(t)\big[\,1+m_K s_K(t)+m_D s_D(t)\,\big]+n(t) \]
\desc{One 1550 nm carrier multiplexes the quantum key ($f_1,m_K$) and classical data ($f_2,m_D$) by subcarrier multiplexing; both share one photodetector, so the data term $s_D$ returns in the key receiver as cross-talk after imperfect RF filtering.}

\textbf{Composite channel:} $h=h_g\cdot h_l\cdot h_a$ (geometric $\times$ atmospheric $\times$ turbulence), independent multiplicative factors that add in decibels.

\subsection{Geometric spreading loss}
\[ w_0=\frac{\lambda}{2\theta_C},\qquad w_L=w_0\sqrt{1+\Big(\tfrac{L\lambda}{\pi w_0^2}\Big)^2},\qquad h_g=[\mathrm{erf}(\nu_R)]^2,\quad \nu_R=\sqrt{\tfrac{\pi}{2}}\,\frac{a_R}{w_L} \]
Spherical slant range (elevation $\varepsilon=90^\circ-\zeta$):
\[ L=\sqrt{R_E^2\sin^2\varepsilon+2R_E H_S+H_S^2}-R_E\sin\varepsilon \]
\desc{Derivation: a Gaussian beam of waist $w_0$ spreads to radius $w_L$ at range $L$; the fraction of power captured by a circular aperture of radius $a_R$ is $[\mathrm{erf}(\nu_R)]^2$. v3 corrections: the $\nu_R$ coefficient $\sqrt2\to\sqrt{\pi/2}$ (read directly from Vu et al.\ 2022) and the slant range flat-Earth $H_S/\cos\zeta\to$ spherical (992.8 km, not 1100 km, at $\varepsilon=30^\circ$). Because $w_L\approx4$--6 m $\gg a_R=5$ cm, $\nu_R\ll1$, so $h_g\approx\nu_R^2\propto1/L^2$ and exceeds 30 dB alone --- the dominant link-budget term. Worked value at $45^\circ$: $L=749$ km, $w_L=4.77$ m, $\nu_R=0.0131$, $h_g=-36.6$ dB.}

\subsection{Atmospheric attenuation (Beer--Lambert)}
\[ h_l=\exp\!\big[-(\sigma_\text{clear}(V)+\sigma_\text{rain}(R))\,L_\text{atm}\big],\qquad L_\text{atm}=\frac{H_\text{atm}-H_U}{\cos\zeta} \]
Clear air (Kruse/Kim): $\displaystyle\sigma_\text{clear}=\frac{3.912}{V}\Big(\frac{\lambda}{550}\Big)^{-q(V)}$, with
$q(V)=1.6\,(V{>}50)$; $1.3\,(6{<}V{\le}50)$; $0.16V{+}0.34\,(1{<}V{\le}6)$; $V{-}0.5\,(0.5{<}V{\le}1)$; $0$ else.\\
Rain (tropical): $\sigma_\text{rain}=\alpha R^\rho/4.343$, $\alpha=0.509$, $\rho=0.63$; the factor $4.343=10/\ln10$ converts dB/km to Nepers/km for the exponential.
\desc{Two independent extinction mechanisms add in the exponent. The wavelength factor $(\lambda/550)^{-q}<1$ at 1550 nm means telecom light scatters less than visible. Visibility is derived $V=15-10P_\text{cloud}$ (no ERA5 visibility variable). Worked values at $\zeta=30^\circ$, $V=10$ km: clear $h_l=-10.2$ dB; with $R=30$ mm/h it drops to $\approx-110$ dB, effectively cutting the link.}

\subsection{Turbulence-induced fading (weak, log-normal)}
Hufnagel--Valley 5/7 profile:
\[ C_n^2(h)=0.00594\Big(\tfrac{W}{27}\Big)^2(10^{-5}h)^{10}e^{-h/1000}+2.7\times10^{-16}e^{-h/1500}+C_n^2(0)e^{-h/100} \]
Rytov and log-amplitude variance:
\[ \sigma_R^2=2.25\,k^{7/6}\sec^{11/6}(\zeta)\!\int_{H_U}^{H_S}\!C_n^2(h)(h-H_U)^{5/6}dh,\qquad \sigma_X^2=\sigma_R^2/4,\quad k=2\pi/\lambda \]
Fading: $h_a=e^{2X}$, $X\sim\mathcal N(-\sigma_X^2,\sigma_X^2)$ so that $E[h_a]=1$; log-normal while $\sigma_R^2<0.3$, else Gamma--Gamma.
\desc{v3 correction: Rytov coefficient $0.56\to2.25$ (standard plane-wave slant-path value), which understated scintillation fourfold. The ground layer $C_n^2(0)e^{-h/100}$ decays within $\sim$500 m, so high-altitude wind $W$ (jet-stream term) dominates the LEO slant-path integral; changing $C_n^2(0)$ by $17\times$ moves $\sigma_R^2$ only $\sim$2.8\%. The operational range stays weak ($\sigma_R^2=0.057$--$0.203$), so log-normal holds throughout.}

\section{Receiver: noise, sifting, QBER and secret key rate}
\textbf{Noise budget} ($\Delta f=R_b/2$):
\[ \sigma_N^2=\underbrace{2qR_e\big(\tfrac12 P_T h_g h_l\big)\Delta f}_{\text{shot}}+\underbrace{\tfrac{4k_BT}{R_L}\Delta f}_{\text{thermal}}+\underbrace{2qR_e P_{bg}\Delta f}_{\text{background}}+\underbrace{\tfrac18(R_e P_T m_D h_g h_l)^2 10^{-I_\text{so}/10}}_{\text{cross-talk}} \]
\desc{v3 corrections: shot noise uses the total DC photocurrent (no $m_K$ factor); the cross-talk denominator $2\to8$ (the photocurrent's leading $\tfrac12$ makes the leaking sinusoid amplitude $\tfrac12 R_e P_T m_D h_g h_l$, whose variance is amplitude$^2/2$). Cross-talk $\propto$ received power squared, so it dominates a strong link (0.5--290$\times$ thermal across elevation) --- ``thermal-dominated'' holds only near $30^\circ$.}

\textbf{Dual-threshold decision} ($i_\text{mean}=\tfrac12 R_e G_k P_T m_K h_g h_l$, scale $\kappa=2$):
\[ d_0=-i_\text{mean}-\kappa\sigma_N,\qquad d_1=+i_\text{mean}+\kappa\sigma_N \]
Samples in the guard zone $[d_0,d_1]$ are discarded; wider $\kappa$ lowers errors but sifts out more samples.

\textbf{Sift probability and QBER} (20-point Gauss--Hermite average over log-normal fading, $h_{a,k}=e^{2\sqrt{2\sigma_X^2}x_k+2\mu_X}$):
\[ P_\text{sift}=\tfrac12(P_{00}+P_{11}+P_{10}+P_{01}),\qquad \text{QBER}=\frac{\tfrac12(P_{10}+P_{01})}{P_\text{sift}} \]

\textbf{Secret key rate} (Shor--Preskill / Devetak--Winter, ideal reconciliation $f_{EC}=1$):
\[ \text{SKR}_\text{norm}=P_\text{sift}\big[\,1-(1+f_{EC})H_2(\text{QBER})-\chi_E\,\big]=P_\text{sift}\big[1-2H_2(\text{QBER})-\chi_E\big],\qquad \text{SKR}=\text{SKR}_\text{norm}R_b \]
with $H_2(p)=-p\log_2 p-(1-p)\log_2(1-p)$, $=0$ at QBER $\approx11\%$; baseline $\chi_E=0$.
\desc{v3 correction: the earlier formula omitted the error-correction leakage $f_{EC}H_2(\text{QBER})$ and reached zero only at QBER $=50\%$; the corrected form vanishes at the 11\% BB84 threshold. Worked value at $45^\circ$: QBER $<0.02\%$, SKR $\approx61.4$ Mbps.}

\textbf{Classical data BER:} $\displaystyle\text{BER}_{CC}=\frac{1}{\sqrt\pi}\sum_k w_k\,Q\!\Big(\frac{A_0 h_{a,k}}{\sigma_{N,D}}\Big)$, $A_0=G_d R_e P_T m_D h_g h_l$, with reverse cross-talk $\propto m_K^2$ in $\sigma_{N,D}$.

\section{Three-state weather model and availability}
\[ p_\text{rain}=\min(f_\text{rain},1-P_\text{cloud}),\quad p_\text{clear}=\max(0,1-P_\text{cloud}-p_\text{rain}),\quad p_\text{cloud}=P_\text{cloud} \]
\[ \text{SKR}_\text{eff}=p_\text{clear}\text{SKR}_c+p_\text{rain}\text{SKR}_r,\qquad A=p_\text{clear}+p_\text{rain}=1-P_\text{cloud} \]
Rain rate from monthly total: $R_\text{mm/h}=R_\text{month}/(30\cdot24\cdot f_\text{rain})$.
\desc{Cloud is a binary outage; availability $A$ is invariant to $f_\text{rain}$, so it is governed by cloud alone --- spanning 10.7\% (Kuala Lumpur, Nov) to 96.5\% (Bangkok, Feb). Statistics: $P_\text{cloud}$ = fraction of hours with cloud cover $\ge85\%$; $f_\text{rain}$ = fraction with precip $\ge0.1$ mm/h; inter-city Pearson correlation of daily cloud; joint-clear probability from the joint record. Best combined FSO window: mid-morning $\sim$05:00--10:00 (in daylight, the day/night tension).}

\section{Coverage geometry and city-pair feasibility}
\[ R_\text{cov}=R_E\Big[\arccos\!\Big(\tfrac{R_E}{R_E+H_S}\cos\varepsilon\Big)-\varepsilon\Big],\qquad \text{DUAL if } d\le 2R_\text{cov}\ \text{else store-and-forward} \]
Great-circle distance (haversine): $d=2R_E\arcsin\sqrt{\sin^2\tfrac{\Delta\varphi}{2}+\cos\varphi_1\cos\varphi_2\sin^2\tfrac{\Delta\lambda}{2}}$.\\
Off-nadir angle: $\sin\eta=R_E\cos\varepsilon/(R_E+H_S)$. Slant range: $\sqrt{(R_E+H_S)^2-(R_E\cos\varepsilon)^2}-R_E\sin\varepsilon$.\\
Directed store-and-forward latency: median time from a pass over $i$ to the same satellite's next pass over $j$ (asymmetric, heading-dependent).
\desc{$R_\text{cov}=793$ km ($30^\circ$), 573 km ($40^\circ$); DUAL threshold $2R_\text{cov}=1587$/1146 km. The 28 ASEAN pairs split 14 DUAL / 14 store-and-forward --- a geographic ceiling no scheduler can lift. The paper's earlier ``950 km radius'' was actually the slant range.}

\section{Weather-aware scheduling and pair-key allocation}
\textbf{Level 1 --- station--satellite matching} (Hungarian, per step $t$):
\[ \max_x\ \sum_{g,s} w_{g,s}(t)\,x_{g,s}(t)-c_h\!\sum_g\mathbf{1}[\text{handover}],\quad \sum_s x_{g,s}\le1,\ \sum_g x_{g,s}\le1,\ x_{g,s}=0\ \text{if not visible} \]
weight $w_{g,s}=\text{SKR}_\text{eff}$ (encodes the diurnal weather cycle).\\
\textbf{Level 2 --- pair key} (trusted relay broadcasts $k_A\oplus k_B$):
\[ K_q=\min\Big(\!\sum_{p:\,\text{station}(p)=A}\! k_p y_{p,q},\ \sum_{p:\,\text{station}(p)=B}\! k_p y_{p,q}\Big),\qquad k_p=w\cdot(t_\text{set}-t_\text{rise}) \]
Strategies: ALG-0 (sticky elevation-priority baseline; ALG-0-feasible resolves double-booking by greedy tie-break); ALG-1 (weather-aware Hungarian matching, blind vs aware); ALG-2 (pass-to-pair allocation: greedy deficit rule, MILP/HiGHS, or max-min water-filling).
\desc{Fair comparison at equal resources, full enumeration of 620 real days: matching gain $+2.47/+2.48\%$; weather-info gain $-0.29/-0.23\%$; pair-starvation 91.6--96.5\%. The $\min(\cdot)$ caps the gain; a real 30 s handover is carried across segments (median segment 3.3 s).}

\section{Inter-satellite-link relay and key/data power-split}
\textbf{ISL multi-hop relay.} BFS hop distance on the static ``+Grid'' mesh (RAAN-based plane clustering); a drop-off pass over $j$ is feasible if $t_\text{rise}\ge t_\text{pick}+n_\text{hops}\cdot30$ s. \emph{time-optimal} = earliest feasible; \emph{capacity-optimal} = highest-elevation (highest-SKR) drop-off within $3\times$ the time-optimal latency. Replaces single-hop store-and-forward (worst case $\sim$711 min) with 2.9--4.1 min.\\[2pt]
\textbf{Key/data power-split.} Two-way cross-talk $\sigma_\text{CT}^2=(R_e P_T m_\text{leak} h_g h_l)^2 10^{-I_\text{so}/10}/8$ ($m_\text{leak}=m_D$ into key, $m_K$ into data). Data goodput $=R_b(1-\text{BER})$; constraint $m_K+m_D\le1$. Pareto frontier over $(m_K,m_D)$; adaptive split takes the smallest $m_K$ with $\text{SKR}\cdot10^3\cdot T_\text{pass}\ge K_\text{req}$.
\desc{Raising $m_D$ lifts data throughput but $\sigma_\text{CT}^2\propto m_D^2$ raises key QBER --- the central SIKD coupling: the two channels are not independent.}

\part{Glossary of Physical Quantities}
\section{Glossary}
For each quantity: meaning, this project's value, the typical range and why it is chosen, and how that range differs across telecom / satellite / quantum work versus other fields.
\begin{itemize}[leftmargin=1.2em,itemsep=5pt]""")
for sy in symbols:
    A(r"\item \textbf{%s} --- \textbf{%s.} %s \\ \desc{\textbf{This project:} %s\quad \textbf{Typical range:} %s} \\ \desc{\textbf{Why:} %s} \\ \desc{\textbf{Across fields:} %s}" % (
        gl(sy["sym"]), gl(sy["name"]), gl(sy["meaning"]), gl(sy["value"]),
        gl(sy["range"]), gl(sy["why"]), gl(sy["domain"])))
A(r"\end{itemize}")

# ============================ PART III: 450 QUESTIONS ============================
A(r"\part{The 450 Study Questions, with Answers and Explanations}")
A(r"This part reproduces, in full, every question implemented on the interactive study site: the 90 active-recall exercises (Section) and the 360 multiple-choice questions (Section). Numeric answers were computed from the formulas of Part~I; the explanations are the same theory frameworks shown on the site.")

# --- 90 recall exercises ---
A(r"\section{Active-recall exercises (90), by section}")
by_sec = {}
for e in ex["exercises"]:
    by_sec.setdefault(e["sectionNum"], []).append(e)
for smeta in ex["meta"]["sections"]:
    A(r"\subsection{%s}" % esc(re.sub(r'^\d+\.\s*', '', smeta["title"])))
    A(r"\small")
    for e in by_sec[smeta["num"]]:
        typ = {"calc": "calculate", "fill": "fill in", "match": "match", "order": "order"}[e["type"]]
        A(r"\qid{E%d}{[%s] %s}\par" % (e["id"], typ, tq(e["prompt"])))
        if e.get("given"):
            A(r"{\footnotesize Given: %s}\par" % tq(e["given"]))
        if e["type"] in ("calc", "fill"):
            av = e.get("answer"); unit = e.get("unit", "")
            A(r"\ans{%s %s}\par" % (tq(str(av)), tq(unit)))
        elif e["type"] == "match":
            pairs = "; ".join("%s $\\rightarrow$ %s" % (tq(k), tq(v)) for k, v in e["pairs"].items())
            A(r"\ans{%s}\par" % pairs)
        else:  # order
            seq = " $\\rightarrow$ ".join(tq(e["items"][i]) for i in e["correctOrder"])
            A(r"\ans{%s}\par" % seq)
        if e.get("steps"):
            A(r"{\footnotesize %s}\par" % tq(e["steps"]))
        if e.get("detail"):
            A(r"{\footnotesize\color{blue!45!black}In detail: %s}\par" % tq(e["detail"]))
        A(r"\vspace{3pt}")
    A(r"\normalsize")

# --- 360 MCQ ---
A(r"\section{Multiple-choice questions (360), by professional perspective}")
by_p = {}
for q in qs["questions"]:
    by_p.setdefault(q["perspective"], []).append(q)
for pmeta in qs["meta"]["perspectives"]:
    A(r"\subsection{P%d --- %s}" % (pmeta["num"], esc(pmeta["title"])))
    A(r"\small")
    for q in by_p[pmeta["num"]]:
        A(r"\qid{Q%d}{%s}\par" % (q["id"], tq(q["question"])))
        opts = " \\quad ".join("\\textbf{%s)} %s" % (o["key"], tq(o["text"])) for o in q["options"])
        A(r"{\footnotesize %s}\par" % opts)
        A(r"\ans{%s.} \fw{%s}\par" % (q["answer"], tq(q["framework"])))
        A(r"\vspace{2.5pt}")
    A(r"\normalsize")

open(OUT, "w", encoding="utf-8").write("\n".join(L))
# append the transcribed thesis annexes (Part IV) from a companion raw file
raw = os.path.join(os.path.dirname(os.path.abspath(__file__)), "annex_partIV.tex")
if os.path.exists(raw):
    with open(OUT, "a", encoding="utf-8") as f:
        f.write("\n" + open(raw, encoding="utf-8").read())
with open(OUT, "a", encoding="utf-8") as f:
    f.write("\n\\end{document}\n")

print("wrote", OUT)
print("exercises:", len(ex["exercises"]), "| MCQ:", len(qs["questions"]), "| glossary:", len(symbols))
