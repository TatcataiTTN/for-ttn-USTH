# for-ttn-USTH

Static, browser-only study material (no backend). Hosted on GitHub Pages.

## Atmospheric-Remote-Sensing — study and exam-prep system (USTH)

Live: **https://tatcataittn.github.io/for-ttn-USTH/Atmospheric-Remote-Sensing/**

English-language site with eight modules matching the eight theory questions of the *Satellite Remote Sensing of Atmospheric Composition* study guide
(sinks and lifetime, light–matter interaction, trace-gas retrieval, pointing geometries, averaging kernels, passive aerosol
sensing, scattering regimes, aerosol altitude): lessons, 1280×720 slide decks (USTH-DSES theme), 138 multiple-choice questions
and 21 essay questions with explanations, 9 in-browser calculators, a 120-minute mock exam with self-grading and eight 15-question
practice exams. Every number is recomputed in Python (`Atmospheric-Remote-Sensing/notebooks/verify_numbers.ipynb`) and the
JavaScript calculators are checked against it (`tests/test_calc.js`). See `Atmospheric-Remote-Sensing/README.md`.

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
