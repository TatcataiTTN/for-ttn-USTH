# Atmospheric-Remote-Sensing (USTH)

Self-study and exam-preparation system for *Satellite Remote Sensing of Atmospheric Composition*, built from the study pack v2
`Atmospheric_Remote_Sensing_Study_Guide_v2.zip` (Part A core knowledge, 8 theory questions with worked examples, Q&A and memory hooks, a 10-question mock exam, 24 figures, 11 lecture photos and the plotting code). v1 files are kept in `resources/`.
USTH-DSES style: USTH colours read from the official logo pixels (blue `#273896`, red `#ED1C24`), slides 1280×720 with text ≥ 20 px.
The site is in **English** (the course language); every lesson also keeps the short Vietnamese summary from the study guide.

Live site: https://tatcataittn.github.io/for-ttn-USTH/Atmospheric-Remote-Sensing/

## Layout

| Path | Content |
|---|---|
| `index.html` | Home, study path, status and limits |
| `lessons/NN-slug/index.html` | Lesson (plain words → technical → formulas → examples), exam checklist, embedded slides, quick quiz |
| `lessons/NN-slug/bank.html` | Question bank: multiple choice with explanations + essays with solutions; filters, retry, saved progress |
| `slides/mN.html` | Module slides (1280×720 canvas, ← → keys, full screen) |
| `calculators.html` | 12 in-browser calculators |
| `slides-gallery.html` | The 11 lecture photos (slides and blackboard), full resolution on click |
| `exam.html` | Original 120-minute mock exam v2: 10 questions, 25 points (self-graded) and eight 15-question practice exams |
| `reference.html` | Formulas and acronyms (appendix of the guide) |
| `resources.html`, `resources/` | Study guide and mock exam (PDF, DOCX), 24 figures, 11 lecture photos |
| `data/verified.json` | Every number computed in Python (single source of truth) |
| `notebooks/verify_numbers.ipynb` | Independent recomputation of all numbers (executed; 58 comparisons `OK`) |

## The 9 modules

0. Part A core knowledge · 1. Sinks and lifetime · 2. Light–matter interaction · 3. Trace-gas retrieval: column and profile · 4. Pointing geometries ·
5. Averaging kernels and DOFS · 6. Passive aerosol sensing · 7. Scattering regimes · 8. Aerosol altitude

## Verification

- `build/verify_numbers.py` computes every number by two independent routes (e.g. Wien vs the numerical maximum of Planck; DOFS vs the sum of eigenvalues; Mie Q_ext vs the Rayleigh formula).
- `tests/test_calc.js` (Node): JavaScript calculators vs Python, 458 comparisons including the 12×12 averaging-kernel matrices.
- `tests/browser_test.py` (Selenium): loads every page, broken images, console errors, quizzes, banks, calculators, exams.
- `build/check_deck.py` (Selenium): slides do not overflow, text ≥ 20 px, no empty bottom.

## Rebuild

```bash
cd build && python3 verify_numbers.py && python3 build_all.py && python3 make_notebook.py
node ../tests/test_calc.js
```

Python sources are in `build/`; the content of each module is in `build/m1.py` … `m8.py`.
