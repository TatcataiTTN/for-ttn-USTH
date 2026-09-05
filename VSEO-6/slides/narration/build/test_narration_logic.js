/*
 * Kiểm thử logic thật của js/narration.js bằng Node, giả lập DOM/Audio/fetch tối thiểu.
 * Không thay thế kiểm thử trình duyệt thật (Lớp 2 lý tưởng là puppeteer/Chrome thật),
 * nhưng chạy được TRỰC TIẾP code sản phẩm (không viết lại logic), bắt được lỗi thật
 * trong control-flow: thứ tự chunk, bôi sáng công thức, chuỗi tự động chuyển slide,
 * và đúng race-condition fix (lastIdx pre-sync trước khi gọi go(1)).
 *
 * Chạy: node slides/narration/build/test_narration_logic.js
 */
const fs = require("fs");
const path = require("path");
const assert = require("assert");

const SLIDES_DIR = path.resolve(__dirname, "..", "..");
const TIMING = JSON.parse(fs.readFileSync(path.join(SLIDES_DIR, "narration", "data", "narration_timing.vseo6.json"), "utf8"));
const NUM_SLIDES = TIMING.length;

const log = [];

// ---------- fake element ----------
function makeEl(tag) {
  const el = {
    tagName: tag || "DIV",
    _classes: new Set(),
    children: [],
    _listeners: {},
    style: {},
    classList: {
      add(c) { el._classes.add(c); },
      remove(c) { el._classes.delete(c); },
      toggle(c, force) {
        const has = el._classes.has(c);
        const want = force === undefined ? !has : force;
        if (want) el._classes.add(c); else el._classes.delete(c);
      },
      contains(c) { return el._classes.has(c); },
    },
    appendChild(child) { el.children.push(child); child.parent = el; return child; },
    addEventListener(type, fn) { (el._listeners[type] = el._listeners[type] || []).push(fn); },
    dispatch(type, evt) { (el._listeners[type] || []).forEach((fn) => fn(evt || {})); },
    querySelector(sel) { return queryFirst(el, sel); },
    querySelectorAll(sel) { return queryAll(el, sel); },
    setAttribute() {},
    get textContent() { return el._text || ""; },
    set textContent(v) { el._text = v; },
  };
  Object.defineProperty(el, "className", {
    get() { return Array.from(el._classes).join(" "); },
    set(v) { el._classes = new Set(String(v).split(/\s+/).filter(Boolean)); },
  });
  return el;
}

function matches(el, sel) {
  // hỗ trợ selector class đơn hoặc ghép, vd ".eqn-box.narrating"
  if (sel.startsWith(".")) {
    const classes = sel.slice(1).split(".").filter(Boolean);
    return classes.every((c) => el._classes.has(c));
  }
  return false;
}
function queryFirst(root, sel) {
  const stack = [...root.children];
  while (stack.length) {
    const cur = stack.shift();
    if (matches(cur, sel)) return cur;
    stack.push(...cur.children);
  }
  return null;
}
function queryAll(root, sel) {
  const out = [];
  const stack = [...root.children];
  while (stack.length) {
    const cur = stack.shift();
    if (matches(cur, sel)) out.push(cur);
    stack.push(...cur.children);
  }
  return out;
}

// ---------- fake deck: N slide, slide idx=3 và idx=5 có nhiều chunk (khớp timing thật) ----------
const deckEl = makeEl("DIV");
for (let i = 0; i < NUM_SLIDES; i++) {
  const slideEl = makeEl("DIV");
  slideEl._classes.add("slide");
  // slide có eqn-box khớp số chunk "rate chậm" của nó trong timing thật
  const chunks = TIMING[i].chunks;
  const formulaCount = chunks.filter((c) => (c.rate || "").indexOf("-") === 0).length;
  for (let f = 0; f < formulaCount; f++) {
    const box = makeEl("DIV");
    box._classes.add("eqn-box");
    slideEl.appendChild(box);
  }
  deckEl.appendChild(slideEl);
}
deckEl.style = { transform: "translateX(-0vw)" };

// ---------- fake global fetch / document / window / Audio / MutationObserver / localStorage ----------
let idx = 0;
global.window = {
  go(delta) {
    idx = Math.max(0, Math.min(NUM_SLIDES - 1, idx + delta));
    deckEl.style.transform = `translateX(-${idx * 100}vw)`;
  },
};
global.document = {
  getElementById(id) { return id === "deck" ? deckEl : null; },
  body: makeEl("BODY"),
  createElement(tag) { return makeEl(tag); },
};
global.localStorage = {
  _s: {},
  getItem(k) { return Object.prototype.hasOwnProperty.call(this._s, k) ? this._s[k] : null; },
  setItem(k, v) { this._s[k] = v; },
};
global.console = console;

let audioInstances = [];
const AUDIO_SPEEDUP = 200; // giả lập: 1ms thật = AUDIO_SPEEDUP ms audio thật, để test chạy nhanh
class FakeAudio {
  constructor(src) {
    this.src = src;
    this.paused = true;
    audioInstances.push(this);
    // tìm durationMs thật từ timing để giả lập đúng thời gian tương đối (rút gọn theo AUDIO_SPEEDUP)
    let durationMs = 1000;
    for (const s of TIMING) {
      const c = s.chunks.find((c) => c.file === src);
      if (c) { durationMs = c.durationMs; break; }
    }
    this._durationMs = durationMs;
  }
  play() {
    this.paused = false;
    const self = this;
    this._timer = setTimeout(() => {
      if (self.onended) self.onended();
    }, Math.max(5, this._durationMs / AUDIO_SPEEDUP));
    return Promise.resolve();
  }
  pause() {
    this.paused = true;
    clearTimeout(this._timer);
  }
}
global.Audio = FakeAudio;

global.MutationObserver = class {
  constructor(cb) { this.cb = cb; }
  observe() {}
};

global.fetch = function (url) {
  return Promise.resolve({
    ok: true,
    json: async () => TIMING,
  });
};

// ---------- load code thật của narration.js ----------
const code = fs.readFileSync(path.join(SLIDES_DIR, "js", "narration.js"), "utf8");
const vm = require("vm");
const script = new vm.Script(code, { filename: "narration.js" });
const context = vm.createContext({
  window: global.window, document: global.document, localStorage: global.localStorage,
  console: global.console, Audio: global.Audio, MutationObserver: global.MutationObserver,
  fetch: global.fetch, setTimeout, clearTimeout,
});
script.runInContext(context);

// ---------- chạy test tuần tự ----------
async function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }
async function waitUntil(cond, timeoutMs, intervalMs) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    if (cond()) return true;
    await sleep(intervalMs);
  }
  return cond();
}

async function main() {
  await sleep(50); // chờ fetch (Promise) resolve + injectButtons chạy xong

  // TEST 1: mọi slide có đúng 1 nút narr-btn
  const allButtons = queryAll(deckEl, ".narr-btn");
  assert.strictEqual(allButtons.length, NUM_SLIDES, `phải có ${NUM_SLIDES} nút, có ${allButtons.length}`);
  console.log(`[PASS] Đã inject đủ ${allButtons.length} nút narr-btn (1 cho mỗi slide).`);

  // TEST 2: click nút slide 3 (biết trước có 3 chunk, chunk giữa là công thức "chậm")
  // Di chuyển deck thật tới slide 3 trước (giả lập user đã bấm Next tới đó), khớp giả định
  // getCurrentIdx() của narration.js đọc từ deck.style.transform.
  global.window.go(3);
  await sleep(10);
  const slide3 = deckEl.children[3];
  const btn3 = slide3.querySelector(".narr-btn");
  const chunks3 = TIMING[3].chunks;
  assert.ok(chunks3.length >= 2, "slide 3 cần có ít nhất 2 chunk để test tuần tự");
  btn3.dispatch("click", { stopPropagation() {} });
  await sleep(10);
  assert.strictEqual(btn3.classList.contains("is-playing"), true, "nút phải chuyển trạng thái playing ngay sau click");
  console.log("[PASS] Nút chuyển sang trạng thái 'is-playing' ngay sau khi click.");

  // chờ hết chunk 0 (không phải công thức) rồi kiểm tra chunk 1 (công thức) có bôi sáng eqn-box không.
  // Poll liên tục thay vì đợi 1 mốc cố định, vì độ trễ setTimeout thật có jitter.
  const formulaChunkIdx = chunks3.findIndex((c) => (c.rate || "").indexOf("-") === 0);
  if (formulaChunkIdx === 1) {
    const sawHighlight = await waitUntil(() => slide3.querySelector(".eqn-box.narrating") !== null, 3000, 3);
    assert.ok(sawHighlight, "phải có .eqn-box.narrating tại một thời điểm nào đó khi đọc chunk công thức");
    console.log("[PASS] eqn-box được bôi sáng đúng lúc đọc chunk công thức (rate chậm).");
  } else {
    console.log(`[SKIP] chunk công thức của slide 3 không ở vị trí 1 (ở vị trí ${formulaChunkIdx}), bỏ qua bước kiểm tra bôi sáng theo thứ tự cụ thể này.`);
  }
  // đợi hẳn cho xong toàn bộ chunk 0+1 trước khi tiếp tục test (dựa trên tổng thời lượng thật)
  await sleep((chunks3[0].durationMs + chunks3[1].durationMs) / AUDIO_SPEEDUP + 15);

  // chờ hết toàn bộ các chunk còn lại của slide 3
  // chunks3[0] và chunks3[1] đã được chờ hết ở bước trên — giờ chỉ cần chờ nốt chunk cuối (idx 2)
  const remainingMs = chunks3.slice(2).reduce((a, c) => a + c.durationMs, 0) / AUDIO_SPEEDUP;
  await sleep(remainingMs + 50);
  assert.strictEqual(btn3.classList.contains("is-playing"), false, "nút phải trở về trạng thái idle sau khi hết mọi chunk");
  const highlightGone = slide3.querySelector(".eqn-box.narrating");
  assert.strictEqual(highlightGone, null, "phải gỡ bôi sáng sau khi slide đọc xong");
  console.log("[PASS] Sau khi hết mọi chunk: nút trở về idle, gỡ bôi sáng công thức.");

  // TEST 3: auto-advance — vì autoAdvanceEnabled mặc định true, slide 3 đọc xong phải tự chuyển sang slide 4
  // và slide 4 phải tự phát (không do ta gọi thủ công)
  await sleep(30);
  assert.strictEqual(idx, 4, `sau khi slide 3 đọc xong, idx phải tự chuyển thành 4 (đang là ${idx})`);
  const slide4 = deckEl.children[4];
  const btn4 = slide4.querySelector(".narr-btn");
  assert.strictEqual(btn4.classList.contains("is-playing"), true, "slide 4 phải TỰ ĐỘNG bắt đầu phát sau khi auto-advance");
  console.log("[PASS] Auto-advance: sau khi slide 3 đọc xong, tự chuyển sang slide 4 VÀ tự phát audio slide 4.");

  // dừng lại (test kết thúc ở đây, không cần đợi hết toàn bộ deck)
  btn4.dispatch("click", { stopPropagation() {} });
  await sleep(10);
  assert.strictEqual(btn4.classList.contains("is-playing"), false, "click lại nút đang phát phải dừng audio");
  console.log("[PASS] Click lại nút đang phát → dừng audio đúng như kỳ vọng.");

  console.log("\n=== TẤT CẢ TEST LOGIC NARRATION.JS ĐỀU PASS ===");
  process.exit(0);
}

main().catch((err) => {
  console.error("\n[FAIL]", err.message);
  process.exit(1);
});
