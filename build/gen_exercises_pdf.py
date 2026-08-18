#!/usr/bin/env python3
"""Render exercises.json -> a printable LaTeX PDF (questions then answer key).
Single source of truth = the same JSON the website uses, so the PDF can never
drift from the site's computed answers."""
import json, re, os

SRC = "/Users/tuannghiat/for-ttn-USTH/Thesis-M1/data/exercises.json"
OUT_TEX = "/Users/tuannghiat/Downloads/Bài Quantum Communication PTIT /Tự học /SIKD_Satellite_QKD/Exam_Practice/SIKD_90_Active_Recall_Exercises.tex"

d = json.load(open(SRC, encoding="utf-8"))
ex = d["exercises"]
secs = d["meta"]["sections"]

def esc(s):
    s = str(s)
    reps = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
            "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    for a, b in reps.items():
        s = s.replace(a, b)
    # arrows / units that appear in prompts
    s = s.replace("->", r"$\rightarrow$").replace("<=", r"$\le$").replace(">=", r"$\ge$")
    s = s.replace("sqrt", r"$\sqrt{\ }$").replace("^2", r"\textsuperscript{2}")
    return s

def type_label(t):
    return {"calc": "Calculate", "fill": "Fill in", "match": "Match", "order": "Order"}[t]

lines = []
A = lines.append
A(r"""\documentclass[11pt,a4paper]{article}
\usepackage{fontspec}
\setmainfont{Times New Roman}
\usepackage{amsmath,amssymb}
\usepackage{geometry}
\usepackage{booktabs}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{tcolorbox}
\usepackage{fancyhdr}
\usepackage{hyperref}
\geometry{margin=2cm,headheight=14pt}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{90 Active-Recall Exercises --- SIKD Thesis M1}
\fancyhead[R]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\tcbuselibrary{skins,breakable}
\newtcolorbox{ansbox}[1][]{colback=green!5,colframe=green!50!black,fonttitle=\bfseries,breakable,#1}
\newtcolorbox{fwbox}[1][]{colback=blue!5,colframe=blue!50!black,fonttitle=\bfseries,breakable,#1}
\title{\Huge\textbf{90 Active-Recall Exercises}\\[0.35cm]
\Large Fill-in / Calculation / Match / Order --- SIKD over Tropical Satellite FSO\\[0.2cm]
\normalsize Companion to the 360-question bank; same computed answers as the web app.\\[0.1cm]
\small Truong Tuan Nghia (2540017), USTH Master Space --- M1 defense preparation}
\author{}\date{}
\begin{document}\maketitle
\begin{fwbox}[title={How to use}]
Work each section with pen and paper (calculations) or from memory (fill/match/order), then
check Part~B. Every item lists its \textbf{theory framework} so you memorise the reasoning, not
just the answer. Numeric answers were computed from the v3 formulas, identical to the website
\href{https://tatcataittn.github.io/for-ttn-USTH/Thesis-M1/}{tatcataittn.github.io/for-ttn-USTH/Thesis-M1}.
\end{fwbox}
\tableofcontents
\newpage
\part*{Part A --- Questions}
\addcontentsline{toc}{section}{Part A --- Questions}
""")

# PART A: questions only
for s in secs:
    A(r"\section*{S%d. %s}" % (s["num"], esc(re.sub(r'^\d+\.\s*', '', s["title"]))))
    A(r"\addcontentsline{toc}{section}{S%d. %s}" % (s["num"], esc(re.sub(r'^\d+\.\s*', '', s["title"]))))
    A(r"\begin{enumerate}[leftmargin=1.3em,label=\textbf{E\arabic*.},start=%d]" % [e for e in ex if e["sectionNum"]==s["num"]][0]["id"])
    for e in [x for x in ex if x["sectionNum"] == s["num"]]:
        A(r"\item \textbf{[%s]} %s" % (type_label(e["type"]), esc(e["prompt"])))
        if e.get("given"):
            A(r"\\ \textit{Given: %s}" % esc(e["given"]))
        if e["type"] == "match":
            A(r"\\[2pt]\textit{Left:} %s \\ \textit{Right (shuffled):} %s" %
              ("; ".join(esc(l) for l in e["left"]), "; ".join(esc(r) for r in sorted(e["right"]))))
        if e["type"] == "order":
            A(r"\\[2pt]\textit{Items (shuffled):} %s" % ("; ".join(esc(i) for i in sorted(e["items"]))))
        if e["type"] in ("calc", "fill"):
            A(r"\\[2pt]Answer: \underline{\hspace{5cm}} %s" % (esc(e.get("unit","")) if e.get("unit") else ""))
        A(r"\vspace{3pt}")
    A(r"\end{enumerate}")
    A(r"\vspace{4pt}")

# PART B: answer key + frameworks
A(r"\newpage\part*{Part B --- Answer key \& theory frameworks}")
A(r"\addcontentsline{toc}{section}{Part B --- Answer key \& frameworks}")
for s in secs:
    A(r"\subsection*{S%d. %s}" % (s["num"], esc(re.sub(r'^\d+\.\s*', '', s["title"]))))
    for e in [x for x in ex if x["sectionNum"] == s["num"]]:
        if e["type"] == "calc":
            ans = r"\textbf{%s}%s \; (tol %s)" % (
                esc(("%g" % e["answer"])), (" " + esc(e["unit"]) if e.get("unit") else ""),
                (esc(str(e["tol"]))+" abs" if e["tolType"]=="abs" else esc(str(round(e["tol"]*100)))+"\\%"))
        elif e["type"] == "fill":
            ans = r"\textbf{%s}%s" % (esc(e["answer"]), (" " + esc(e["unit"]) if e.get("unit") else ""))
        elif e["type"] == "match":
            ans = "; ".join(r"%s $\rightarrow$ %s" % (esc(l), esc(e["pairs"][l])) for l in e["left"])
        else:  # order
            ans = " $\\rightarrow$ ".join(esc(e["items"][i]) for i in e["correctOrder"])
        A(r"\noindent\textbf{E%d.} %s" % (e["id"], ans))
        if e.get("steps"):
            A(r"\\ \textit{%s}" % esc(e["steps"]))
        A(r"\\ {\small\color{blue!50!black}Framework: %s}" % esc(e["framework"]))
        if e.get("detail"):
            A(r"\\ {\small In detail: %s}" % esc(e["detail"]))
        A(r"\par\vspace{5pt}")
    A(r"\vspace{2pt}")

A(r"\end{document}")

os.makedirs(os.path.dirname(OUT_TEX), exist_ok=True)
open(OUT_TEX, "w", encoding="utf-8").write("\n".join(lines))
print("wrote", OUT_TEX, "(%d exercises)" % len(ex))
