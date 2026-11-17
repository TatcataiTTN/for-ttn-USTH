# for-ttn-USTH

Static, browser-only study material (no backend). Hosted on GitHub Pages.

## Atmospheric-Remote-Sensing — study and exam-prep system (USTH)

Live: **https://tatcataittn.github.io/for-ttn-USTH/Atmospheric-Remote-Sensing/**

English-language site built from study guide v2 and the lecture master (J. Cuesta, UPEC). It opens with **the Big 12** (3 key points, 3 formulas, 3 concepts, 3 principles) to master before the modules and the exams, then 12 modules:
Part A core knowledge, Part B atmosphere and ozone chemistry, the eight theory chapters (sinks and lifetime, light–matter interaction, trace-gas retrieval, pointing geometries, averaging kernels, passive aerosol
sensing, scattering regimes, aerosol altitude), Part C satellite case studies and Part D lidar: lessons, 1280×720 slide decks (USTH-DSES theme), 260 multiple-choice questions and 36 essay questions with explanations,
16 in-browser calculators, 137 lecture pages and 11 class photos, five written mock papers (44 questions, self-graded, each part tagged with the Big-12 items it needs) and twelve 15-question practice exams.
Every number is recomputed in Python (`Atmospheric-Remote-Sensing/notebooks/verify_numbers.ipynb`) and the
JavaScript calculators are checked against it (`tests/test_calc.js`). See `Atmospheric-Remote-Sensing/README.md`.

## Ocean-Optics — self-study and exam-practice system (USTH)

Live: **https://tatcataittn.github.io/for-ttn-USTH/Ocean-Optics/**

English-language site built from the lecture *Marine Optics* (H. Loisel, LOG; 120 slides) and the Ocean Optics Web Book (CC BY 2.0). It opens with **the Big 12**, then eight modules (light in water and IOPs, pure water, absorption, particle scattering, measuring IOPs, IOPs and biogeochemistry, light field (textbook only), new platforms): lessons, 1280×720 slide decks, 138 multiple-choice and 20 essay questions with sources, 10 in-browser calculators, 82 selected lecture pages, five written mock papers and twelve multiple-choice mock exams.
Every number is recomputed in Python by two independent methods (`Ocean-Optics/data/verified.json`, `Ocean-Optics/notebooks/verify_numbers.ipynb`) and the calculators are tested against it (`tests/test_calc.js`). No sample exam from the lecturer was available; see `Ocean-Optics/README.md` and the "Sources and limits" page.

## Thesis-M1 — 360-question practice bank

Live: **https://tatcataittn.github.io/for-ttn-USTH/Thesis-M1/**

An interactive, self-grading multiple-choice quiz (360 questions across 11 professional
perspectives, from basic definitions to figure/video reading) for the M1 internship thesis
*"Weather-Aware Scheduling for Simultaneous Information and Key Distribution over Tropical
Satellite Free-Space Optical Channels"* (Trương Tuấn Nghĩa, 2540017, USTH Master Space).

- Pick an answer, get instant correct/incorrect grading plus the one-line **theory framework**.
- Progress is saved in the browser (`localStorage`) — no server, no account.
- A **Study resources** page links the full PDFs (formula guides, exercises, committee
  analysis, literature review, defense slides).

### Regenerating the question bank (never hand-type answers)

The correct answers are parsed programmatically from the source Markdown, then the option
order is shuffled deterministically (so the answer isn't always the same letter):

```bash
python3 build/parse_questions.py        # -> Thesis-M1/data/questions.json
```

### Testing

```bash
cd Thesis-M1 && python3 -m http.server 8731   # serve locally
node build/test_browser.js                     # Layer-2 browser test (needs Chrome + puppeteer-core)
```
