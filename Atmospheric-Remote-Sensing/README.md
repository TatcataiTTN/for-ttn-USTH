# Atmospheric-Remote-Sensing (USTH)

Self-study and exam-preparation system for *Satellite Remote Sensing of Atmospheric Composition*, built from (1) the study pack v2
`Atmospheric_Remote_Sensing_Study_Guide_v2.zip` (Part A core knowledge, 8 theory questions with worked examples, Q&A and memory hooks, a 10-question mock exam, 24 figures, 11 lecture photos and the plotting code; v1 files are kept in `resources/`) and (2) the lecture master *Remote Sensing of the Atmosphere: a focus on air composition* (J. Cuesta, UPEC, Master Space 2026–2027, 233 pages, read by text layer + OCR). The site opens with **the Big 12** (3 key points, 3 formulas, 3 concepts, 3 principles) to master before the modules and the exams.
USTH-DSES style: USTH colours read from the official logo pixels (blue `#273896`, red `#ED1C24`), slides 1280×720 with text ≥ 20 px.
The site is in **English** (the course language); every lesson also keeps the short Vietnamese summary from the study guide.

Live site: https://tatcataittn.github.io/for-ttn-USTH/Atmospheric-Remote-Sensing/

## Layout

| Path | Content |
|---|---|
| `index.html` | Home, study path, status and limits |
| `lessons/start-here/index.html` | **The Big 12**: 12 cards, coverage table, 12-question check (soft gate on the other pages) |
| `lessons/NN-slug/index.html` | Lesson (plain words → technical → formulas → examples), exam checklist, embedded slides, quick quiz |
| `lessons/NN-slug/bank.html` | Question bank: multiple choice with explanations + essays with solutions; filters, retry, saved progress |
| `slides/<id>.html` | Module slides (1280×720 canvas, ← → keys, full screen) |
| `calculators.html` | 16 in-browser calculators (added: lidar equation, DIAL, hydrostatic pressure, sink shares) |
| `lecture-slides.html` | 137 selected pages of the lecture master (assets/images/lecture/), grouped by topic, filterable |
| `slides-gallery.html` | The 11 class photos (slides and blackboard), full resolution on click |
| `exam.html` | Five written papers (Paper 1 official, Papers 2–5 new: 44 questions, 122 parts, each part tagged A/B/C and with its Big-12 items) and twelve 15-question MCQ exams |
| `reference.html` | Formulas and acronyms (appendix of the guide) |
| `resources.html`, `resources/` | Study guide and mock exam (PDF, DOCX), 31 figures, photos and lecture pages |
| `data/verified.json` | Every number computed in Python (single source of truth) |
| `notebooks/verify_numbers.ipynb` | Independent recomputation of all numbers (executed; 80 comparisons `OK`) |

## The 13 modules

Start here (Big 12) · A core knowledge · B atmosphere and ozone chemistry · 1 sinks and lifetime · 2 light–matter interaction · 3 trace-gas retrieval · 4 pointing geometries · 5 averaging kernels and DOFS · 6 passive aerosol sensing · 7 scattering regimes · 8 aerosol altitude · C satellite case studies (cost function, IASI+GOME-2, AAI, LUT, AEROIASI, AEROS5P) · D lidar (lidar equation, DIAL, the lecture exercises)

## Verification

- `build/verify_numbers.py` computes every number by two independent routes (e.g. Wien vs the numerical maximum of Planck; DOFS vs the sum of eigenvalues; Mie Q_ext vs the Rayleigh formula).
- `tests/test_calc.js` (Node): JavaScript calculators vs Python, 478 comparisons including the 12×12 averaging-kernel matrices.
- `tests/browser_test.py` (Selenium): loads every page, broken images, console errors, quizzes, banks, calculators, exams.
- `build/check_deck.py` (Selenium): slides do not overflow, text ≥ 20 px, no empty bottom.

## Rebuild

```bash
cd build && python3 verify_numbers.py && python3 build_all.py && python3 make_notebook.py
node ../tests/test_calc.js
```

Python sources are in `build/`; module content is in `build/p0.py` (Big 12), `pa.py`, `pb.py`, `m1.py` … `m8.py`, `pc.py`, `pl.py`; `core_map.py` holds the Big 12 and the coverage levels, `papers.py` the new written papers, `lecture_pages.py` the lecture-page index, `figs3.py` the new figures.

The lecture pages are © their author and shown for private study with credit; the full lecture PDF is not republished. Coverage levels (A/B/C) are my own assessment, not a prediction of the real exam.
