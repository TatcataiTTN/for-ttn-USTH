# for-ttn-USTH

Static, browser-only study material (no backend). Hosted on GitHub Pages.

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
