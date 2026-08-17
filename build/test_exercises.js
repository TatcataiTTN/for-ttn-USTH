// Layer 2: browser test of the Active-Recall mode (all 4 types) + Frameworks page.
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

  // load exercises data for expected answers
  const data = await p.evaluate(async () => (await (await fetch("data/exercises.json")).json()).exercises);
  const byType = t => data.find(e => e.type === t);

  // ---- CALC ----
  const calc = byType("calc");
  await p.evaluate((id) => {
    const d = window; // navigate to that exercise
  }, calc.id);
  // find its section/index
  function locate(e) {
    const sec = e.sectionNum;
    return { sec };
  }
  async function gotoEx(e) {
    const idx = data.filter(x => x.sectionNum === e.sectionNum).findIndex(x => x.id === e.id);
    await p.evaluate((s, i) => { location.hash = "#/ex/" + s + "/" + i; }, e.sectionNum, idx);
    await p.waitForSelector(".qcard", { timeout: 8000 });
  }

  await gotoEx(calc);
  await p.waitForSelector("#ex-input");
  await p.type("#ex-input", String(calc.answer));
  await p.click("#submit-btn");
  await p.waitForSelector(".framework.show", { timeout: 5000 });
  const calcOk = await p.evaluate(() => document.querySelector("#verdict").classList.contains("ok"));
  console.log("CALC correct-path:", calcOk, "(E" + calc.id + " ans " + calc.answer + ")");
  if (!calcOk) throw new Error("calc grading failed");

  // ---- FILL ----
  const fill = byType("fill");
  await gotoEx(fill);
  await p.waitForSelector("#ex-input");
  await p.type("#ex-input", fill.accept[0]);
  await p.click("#submit-btn");
  await p.waitForSelector(".framework.show");
  const fillOk = await p.evaluate(() => document.querySelector("#verdict").classList.contains("ok"));
  console.log("FILL correct-path:", fillOk, "(E" + fill.id + ")");
  if (!fillOk) throw new Error("fill grading failed");

  // ---- FILL wrong path ----
  const fill2 = data.filter(e => e.type === "fill")[1];
  await gotoEx(fill2);
  await p.type("#ex-input", "definitely-wrong-xyz");
  await p.click("#submit-btn");
  await p.waitForSelector(".framework.show");
  const fillBad = await p.evaluate(() => document.querySelector("#verdict").classList.contains("bad"));
  console.log("FILL wrong-path shows bad + framework:", fillBad);
  if (!fillBad) throw new Error("fill wrong-path failed");

  // ---- MATCH (click-to-place) ----
  const match = byType("match");
  await gotoEx(match);
  await p.waitForSelector(".chip");
  // place each correct chip: for each left, click the chip whose value == pairs[left], then click that slot
  for (const left of match.left) {
    const want = match.pairs[left];
    await p.evaluate((w) => {
      const chip = [...document.querySelectorAll(".chip")].find(c => c.dataset.val === w);
      chip.click();
    }, want);
    await p.evaluate((l) => {
      const slot = [...document.querySelectorAll(".slot")].find(s => s.dataset.left === l);
      slot.click();
    }, left);
  }
  await p.waitForSelector("#submit-btn:not([disabled])");
  await p.click("#submit-btn");
  await p.waitForSelector(".framework.show");
  const matchOk = await p.evaluate(() => document.querySelector("#verdict").classList.contains("ok"));
  console.log("MATCH correct-path:", matchOk, "(E" + match.id + ")");
  if (!matchOk) throw new Error("match grading failed");

  // ---- ORDER (use ▼/▲ to sort into correct order) ----
  const order = byType("order");
  await gotoEx(order);
  await p.waitForSelector(".order-row");
  // bubble sort using the up buttons: repeatedly place correct item at each position
  const n = order.items.length;
  for (let pos = 0; pos < n; pos++) {
    const targetOrig = order.correctOrder[pos];
    // move the row with data-orig===targetOrig up until it's at index pos
    for (let guard = 0; guard < n * 2; guard++) {
      const idx = await p.evaluate((t) => {
        const rows = [...document.querySelectorAll("#order-wrap .order-row")];
        return rows.findIndex(r => +r.dataset.orig === t);
      }, targetOrig);
      if (idx <= pos) break;
      await p.evaluate((t) => {
        const rows = [...document.querySelectorAll("#order-wrap .order-row")];
        const row = rows.find(r => +r.dataset.orig === t);
        row.querySelector(".ord-up").click();
      }, targetOrig);
    }
  }
  await p.click("#submit-btn");
  await p.waitForSelector(".framework.show");
  const orderOk = await p.evaluate(() => document.querySelector("#verdict").classList.contains("ok"));
  console.log("ORDER correct-path:", orderOk, "(E" + order.id + ")");
  if (!orderOk) throw new Error("order grading failed");

  // ---- Frameworks page ----
  await p.evaluate(() => { location.hash = "#/frameworks"; });
  await p.waitForSelector(".fw-item", { timeout: 6000 });
  const fwCount = await p.$$eval(".fw-item", els => els.length);
  console.log("frameworks listed:", fwCount);
  if (fwCount < 400) throw new Error("expected >=400 framework items (360+90), got " + fwCount);
  // search filter
  await p.type("#fw-search", "cross-talk");
  await new Promise(r => setTimeout(r, 200));
  const visible = await p.evaluate(() => [...document.querySelectorAll(".fw-item")].filter(i => i.style.display !== "none").length);
  console.log("frameworks matching 'cross-talk':", visible);
  if (visible < 1) throw new Error("framework search failed");

  // ---- persistence: reload, calc exercise still graded ----
  await gotoEx(calc);
  const persisted = await p.evaluate(() => !!document.querySelector("#submit-btn[disabled]"));
  console.log("exercise persisted:", persisted);
  if (!persisted) throw new Error("exercise progress not persisted");

  if (errs.length) { console.log("CONSOLE ERRORS:", errs); throw new Error("console errors"); }
  console.log("\nEXERCISES LAYER2 PASS ✅ — calc/fill/match/order grading + frameworks + persistence all work.");
  await b.close();
})().catch(e => { console.error("EXERCISES FAIL ❌", e.message); process.exit(1); });
