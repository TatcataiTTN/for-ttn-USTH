// Layer 2: real-browser interaction test using installed Chrome via puppeteer-core.
const puppeteer = require("puppeteer-core");
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const URL = "http://localhost:8731/index.html";

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME, headless: "new",
    args: ["--no-sandbox", "--disable-dev-shm-usage"],
  });
  const page = await browser.newPage();
  const errors = [];
  page.on("console", m => { if (m.type() === "error") errors.push(m.text()); });
  page.on("pageerror", e => errors.push("pageerror: " + e.message));

  await page.goto(URL, { waitUntil: "networkidle0", timeout: 30000 });

  // nav rendered with 11 perspectives?
  await page.waitForSelector(".nav-item", { timeout: 10000 });
  const navCount = await page.$$eval(".nav-item", els => els.length);
  console.log("nav items:", navCount);
  if (navCount !== 11) throw new Error("expected 11 nav items, got " + navCount);

  // go to perspective 1, first question
  await page.evaluate(() => { location.hash = "#/p/1/0"; });
  await page.waitForSelector(".qcard .opt", { timeout: 10000 });

  // read the correct answer from the loaded data for THIS question
  const info = await page.evaluate(async () => {
    const d = await (await fetch("data/questions.json")).json();
    const q = d.questions.find(x => x.perspective === 1);
    return { id: q.id, answer: q.answer };
  });
  console.log("Q" + info.id + " correct =", info.answer);

  // pick a WRONG option deliberately to test red-marking
  const wrongKey = ["A", "B", "C", "D"].find(k => k !== info.answer);
  await page.click('.opt[data-key="' + wrongKey + '"]');
  await page.waitForSelector("#submit-btn:not([disabled])");
  await page.click("#submit-btn");
  await page.waitForSelector(".framework.show", { timeout: 5000 });

  const state = await page.evaluate((ans, wrong) => {
    const correctEl = document.querySelector('.opt[data-key="' + ans + '"]');
    const wrongEl = document.querySelector('.opt[data-key="' + wrong + '"]');
    const fw = document.querySelector(".framework.show");
    const verdict = document.querySelector("#verdict");
    return {
      correctMarked: correctEl && correctEl.classList.contains("correct"),
      wrongMarked: wrongEl && wrongEl.classList.contains("wrong"),
      fwVisible: !!fw && fw.offsetHeight > 0,
      verdict: verdict ? verdict.textContent : null,
    };
  }, info.answer, wrongKey);
  console.log("grading state:", JSON.stringify(state));
  if (!state.correctMarked || !state.wrongMarked || !state.fwVisible)
    throw new Error("grading UI did not mark correctly");
  if (!/Incorrect/.test(state.verdict)) throw new Error("verdict wrong: " + state.verdict);

  // persistence: reload, the answer should still be shown graded
  await page.reload({ waitUntil: "networkidle0" });
  await page.evaluate(() => { location.hash = "#/p/1/0"; });
  await page.waitForSelector(".qcard .opt", { timeout: 8000 });
  const persisted = await page.evaluate(() =>
    !!document.querySelector(".opt.correct") && !!document.querySelector("#submit-btn[disabled]"));
  console.log("persisted after reload:", persisted);
  if (!persisted) throw new Error("progress did not persist");

  // now answer CORRECTLY on a fresh question (P2 Q1) and check green + overall counter moves
  await page.evaluate(() => { location.hash = "#/p/2/0"; });
  await page.waitForSelector(".qcard .opt:not(.disabled)", { timeout: 8000 });
  const info2 = await page.evaluate(async () => {
    const d = await (await fetch("data/questions.json")).json();
    const q = d.questions.find(x => x.perspective === 2);
    return { answer: q.answer };
  });
  await page.click('.opt[data-key="' + info2.answer + '"]');
  await page.waitForSelector("#submit-btn:not([disabled])");
  await page.click("#submit-btn");
  await page.waitForSelector(".framework.show");
  const ok = await page.evaluate(ans =>
    document.querySelector('.opt[data-key="' + ans + '"]').classList.contains("correct") &&
    /Correct/.test(document.querySelector("#verdict").textContent), info2.answer);
  console.log("correct-answer path ok:", ok);
  if (!ok) throw new Error("correct-answer grading failed");

  // resources route renders cards
  await page.evaluate(() => { location.hash = "#/resources"; });
  await page.waitForSelector(".res-card", { timeout: 5000 });
  const resCount = await page.$$eval(".res-card", els => els.length);
  console.log("resource cards:", resCount);
  if (resCount < 7) throw new Error("expected >=7 resource cards");

  if (errors.length) { console.log("CONSOLE ERRORS:", errors); throw new Error("console errors present"); }

  console.log("\nLAYER2 PASS ✅ — nav, grading (wrong+correct), framework reveal, persistence, resources all work.");
  await browser.close();
})().catch(e => { console.error("LAYER2 FAIL ❌", e.message); process.exit(1); });
