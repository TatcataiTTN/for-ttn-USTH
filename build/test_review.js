// Layer 2: test the "Review wrong answers" flow.
const puppeteer = require("puppeteer-core");
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const SITE = process.env.SITE || "http://localhost:8731/index.html";

(async () => {
  const b = await puppeteer.launch({ executablePath: CHROME, headless: "new", args: ["--no-sandbox"] });
  const p = await b.newPage();
  const errs = [];
  p.on("console", m => { if (m.type() === "error") errs.push(m.text()); });
  p.on("pageerror", e => errs.push("pageerr: " + e.message));
  await p.goto(SITE, { waitUntil: "networkidle0", timeout: 40000 });
  await p.waitForSelector(".mode-tabs", { timeout: 15000 });

  // seed progress directly: mark 2 MCQ wrong + 1 correct, 1 exercise wrong
  await p.evaluate(() => {
    localStorage.setItem("sikd_m1_progress_v1", JSON.stringify({ "1": { chosen: "Z", correct: false }, "2": { chosen: "Z", correct: false }, "3": { chosen: "A", correct: true } }));
    localStorage.setItem("sikd_m1_ex_v1", JSON.stringify({ "38": { correct: false } }));
  });
  // read the correct answers we'll need
  const info = await p.evaluate(async () => {
    const q = await (await fetch("data/questions.json")).json();
    const x = await (await fetch("data/exercises.json")).json();
    const q1 = q.questions.find(z => z.id === 1);
    const e38 = x.exercises.find(z => z.id === 38);
    return { q1ans: q1.answer, e38accept: e38.accept[0] };
  });

  // go to review home
  await p.evaluate(() => { location.hash = "#/review"; location.reload(); });
  await p.waitForSelector(".page-head", { timeout: 8000 });
  await p.waitForFunction(() => document.body.textContent.includes("Review wrong answers"), { timeout: 8000 });
  const counts = await p.evaluate(() => document.querySelector(".home-ctas").textContent);
  console.log("review home CTAs:", counts.replace(/\s+/g, " ").trim());
  if (!/2 wrong MCQ/.test(counts) || !/1 wrong recall/.test(counts)) throw new Error("wrong counts on review home");

  // enter MCQ review, fix Q1 correctly
  await p.evaluate(() => { location.hash = "#/review/mcq/0"; });
  await p.waitForSelector(".opt");
  const shownId = await p.evaluate(() => document.querySelector(".qid").textContent);
  console.log("first wrong MCQ shown:", shownId);
  await p.click('.opt[data-key="' + info.q1ans + '"]');
  await p.waitForSelector("#submit-btn:not([disabled])");
  await p.click("#submit-btn");
  await p.waitForSelector(".framework.show");
  const fixed = await p.evaluate(() => document.querySelector("#verdict").classList.contains("ok") && /Fixed/.test(document.querySelector("#verdict").textContent));
  console.log("MCQ fixed verdict:", fixed);
  if (!fixed) throw new Error("review MCQ fix failed");

  // Next wrong -> should now show the remaining wrong MCQ (Q2), count reduced to 1
  await p.click("#rev-next");
  // wait for the actual re-render (question id must change away from Q1)
  await p.waitForFunction(() => {
    var id = document.querySelector(".qid");
    return id && id.textContent !== "Q1";
  }, { timeout: 8000 });
  const remaining = await p.evaluate(() => document.querySelector(".ph-sub").textContent);
  const nowId = await p.evaluate(() => document.querySelector(".qid").textContent);
  console.log("after fixing one, review sub:", remaining.replace(/\s+/g, " ").trim(), "| showing", nowId);
  if (!/1 to fix/.test(remaining)) throw new Error("wrong-count did not shrink after fix");

  // now exercise review: fix E38
  await p.evaluate(() => { location.hash = "#/review/ex/0"; });
  await p.waitForSelector("#ex-input");
  await p.type("#ex-input", info.e38accept);
  await p.click("#submit-btn");
  await p.waitForSelector(".framework.show");
  const exFixed = await p.evaluate(() => document.querySelector("#verdict").classList.contains("ok"));
  console.log("exercise fixed:", exFixed);
  if (!exFixed) throw new Error("review exercise fix failed");

  // back to review home: recall list should now be empty
  await p.evaluate(() => { location.hash = "#/review"; });
  await p.waitForSelector(".page-head");
  const recallGone = await p.evaluate(() => !/wrong recall/.test((document.querySelector(".home-ctas") || {}).textContent || ""));
  console.log("recall wrong list cleared:", recallGone);
  if (!recallGone) throw new Error("recall wrong not cleared");

  if (errs.length) { console.log("CONSOLE ERRORS:", errs); throw new Error("console errors"); }
  console.log("\nREVIEW LAYER2 PASS ✅ — wrong lists, retry-and-fix, live shrink, MCQ+recall all work.");
  await b.close();
})().catch(e => { console.error("REVIEW FAIL ❌", e.message); process.exit(1); });
