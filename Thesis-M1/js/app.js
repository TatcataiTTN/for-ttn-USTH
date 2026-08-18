/* SIKD Thesis M1 study app — vanilla JS, static, no backend.
   Three modes: MCQ (360), Active Recall (90: fill/calc/match/order), and a
   Theory-Frameworks reference. Grading is client-side; numeric answers for calc
   items were computed from the real formulas at build time. Progress: localStorage. */
(function () {
  "use strict";

  var LS_MCQ = "sikd_m1_progress_v1";
  var LS_EX = "sikd_m1_ex_v1";
  var Q = null;   // {meta, questions}
  var X = null;   // {meta, exercises}
  var BY_PERSP = {};
  var BY_SEC = {};
  var P_MCQ = load(LS_MCQ);   // id -> {chosen, correct}
  var P_EX = load(LS_EX);     // id -> {correct}

  var RESOURCES = [
    { file: "resources/SIKD_Formula_Guide_v3_Expanded.pdf", icon: "📘", title: "Formula Guide v3 (Expanded)", desc: "Corrected v3 physics, old→new table, basic → advanced." },
    { file: "resources/SIKD_Weather_Formula_Guide.pdf", icon: "📗", title: "Formula Guide (original, pre-v3)", desc: "Earlier 50-formula guide with many drill examples." },
    { file: "resources/SIKD_90_Active_Recall_Exercises.pdf", icon: "🧮", title: "90 Active-Recall Exercises (PDF)", desc: "The 90 fill/calc/match/order items — questions then answer key with frameworks. Printable." },
    { file: "resources/SIKD_Exercises_Solutions.pdf", icon: "📐", title: "Exercises & Solutions", desc: "Worked problems by topic, full step-by-step solutions." },
    { file: "resources/SIKD_Practice_Exam_80MCQ.pdf", icon: "📝", title: "80-MCQ Practice Exam", desc: "A separate multiple-choice exam with answer grid." },
    { file: "resources/SIKD_Committee_Analysis.pdf", icon: "🎓", title: "Committee Analysis & Predicted Q&A", desc: "Examiner-by-examiner predicted questions and prepared answers." },
    { file: "resources/SIKD_Literature_Review.pdf", icon: "📚", title: "Literature Review", desc: "34 real references mapped to role and to each examiner." },
    { file: "resources/Defense_Slides.pdf", icon: "🖥️", title: "Defense Slides (9-slide, 10 min)", desc: "The M1 defense deck with v3 numbers." }
  ];

  function load(k) { try { return JSON.parse(localStorage.getItem(k)) || {}; } catch (e) { return {}; } }
  function saveMcq() { try { localStorage.setItem(LS_MCQ, JSON.stringify(P_MCQ)); } catch (e) {} }
  function saveEx() { try { localStorage.setItem(LS_EX, JSON.stringify(P_EX)); } catch (e) {} }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function currentMode() {
    var h = location.hash || "";
    if (h.indexOf("#/ex") === 0) return "ex";
    if (h.indexOf("#/p/") === 0) return "mcq";
    return null;
  }

  function boot() {
    Promise.all([
      fetch("data/questions.json", { cache: "no-cache" }).then(chk),
      fetch("data/exercises.json", { cache: "no-cache" }).then(chk)
    ]).then(function (r) {
      Q = r[0]; X = r[1];
      Q.questions.forEach(function (q) { (BY_PERSP[q.perspective] = BY_PERSP[q.perspective] || []).push(q); });
      X.exercises.forEach(function (e) { (BY_SEC[e.sectionNum] = BY_SEC[e.sectionNum] || []).push(e); });
      window.addEventListener("hashchange", route);
      route();
    }).catch(function (e) {
      document.getElementById("content").innerHTML =
        '<div class="loading">Could not load data (' + esc(e.message) +
        ').<br><button class="btn btn-primary" onclick="location.reload()">Retry</button></div>';
    });
  }
  function chk(r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); }

  /* ---------------- sidebar ---------------- */
  function renderNav() {
    var mode = currentMode() || "mcq";
    var nav = document.getElementById("nav");
    var tabs =
      '<div class="mode-tabs">' +
      '<a class="mtab' + (mode === "mcq" ? " on" : "") + '" href="#/p/1/0">MCQ · 360</a>' +
      '<a class="mtab' + (mode === "ex" ? " on" : "") + '" href="#/ex/1/0">Recall · 90</a>' +
      "</div>";
    var list = "";
    if (mode === "ex") {
      X.meta.sections.forEach(function (s) {
        var arr = BY_SEC[s.num]; var st = exStats(arr);
        var pct = st.total ? Math.round(100 * st.done / st.total) : 0;
        list += navItem("#/ex/" + s.num + "/0", "S" + s.num, cleanSec(s.title), st, pct, "ex-" + s.num, mode);
      });
    } else {
      Q.meta.perspectives.forEach(function (p) {
        var arr = BY_PERSP[p.num]; var st = mcqStats(arr);
        var pct = st.total ? Math.round(100 * st.done / st.total) : 0;
        list += navItem("#/p/" + p.num + "/0", "P" + p.num, p.title, st, pct, "mcq-" + p.num, mode);
      });
    }
    nav.innerHTML = tabs + list;
    renderOverall();
  }
  function cleanSec(t) { return t.replace(/^\d+\.\s*/, ""); }
  function navItem(href, tag, title, st, pct, key, mode) {
    return '<a class="nav-item" data-key="' + key + '" href="' + href + '">' +
      '<span class="ni-top"><span class="ni-num">' + tag + '</span>' +
      '<span class="ni-count">' + st.done + "/" + st.total + "</span></span>" +
      '<span class="ni-title">' + esc(title) + "</span>" +
      '<span class="ni-mini"><i style="width:' + pct + '%"></i></span></a>';
  }
  function renderOverall() {
    var sm = mcqStats(Q.questions), se = exStats(X.exercises);
    var pm = Math.round(100 * sm.done / sm.total), pe = Math.round(100 * se.done / se.total);
    document.getElementById("overall-progress").innerHTML =
      "<div><strong>Overall progress</strong></div>" +
      '<div class="op-row"><span>MCQ</span><span>' + sm.done + "/" + sm.total + " · " + (sm.done ? Math.round(100 * sm.correct / sm.done) : 0) + "%</span></div>" +
      '<div class="op-bar"><div class="op-fill" style="width:' + pm + '%"></div></div>' +
      '<div class="op-row"><span>Recall</span><span>' + se.done + "/" + se.total + " · " + (se.done ? Math.round(100 * se.correct / se.done) : 0) + "%</span></div>" +
      '<div class="op-bar"><div class="op-fill alt" style="width:' + pe + '%"></div></div>';
  }
  function mcqStats(list) { var d = 0, c = 0; list.forEach(function (q) { var p = P_MCQ[q.id]; if (p) { d++; if (p.correct) c++; } }); return { done: d, correct: c, total: list.length }; }
  function exStats(list) { var d = 0, c = 0; list.forEach(function (e) { var p = P_EX[e.id]; if (p) { d++; if (p.correct) c++; } }); return { done: d, correct: c, total: list.length }; }
  function setActive(key) { document.querySelectorAll(".nav-item").forEach(function (b) { b.classList.toggle("active", b.dataset.key === key); }); }

  /* wrong-answer lists (recomputed live from progress) */
  function wrongMcq() { return Q.questions.filter(function (q) { var p = P_MCQ[q.id]; return p && !p.correct; }); }
  function wrongEx() { return X.exercises.filter(function (e) { var p = P_EX[e.id]; return p && !p.correct; }); }

  /* ---------------- router ---------------- */
  function route() {
    var h = location.hash || "#/";
    window.scrollTo(0, 0);
    renderNav();
    if (h === "#/resources") { setActive(null); return renderResources(); }
    if (h === "#/frameworks") { setActive(null); return renderFrameworks(); }
    if (h === "#/review") { setActive(null); return renderReviewHome(); }
    var rv = h.match(/^#\/review\/(mcq|ex)\/(\d+)$/);
    if (rv) { setActive(null); return renderReviewItem(rv[1], +rv[2]); }
    var mp = h.match(/^#\/p\/(\d+)(?:\/(\d+))?$/);
    if (mp && BY_PERSP[+mp[1]]) { setActive("mcq-" + mp[1]); return renderMcq(+mp[1], mp[2] ? +mp[2] : 0); }
    var me = h.match(/^#\/ex\/(\d+)(?:\/(\d+))?$/);
    if (me && BY_SEC[+me[1]]) { setActive("ex-" + me[1]); return renderEx(+me[1], me[2] ? +me[2] : 0); }
    setActive(null); renderHome();
  }

  /* ---------------- home ---------------- */
  function renderHome() {
    var sm = mcqStats(Q.questions), se = exStats(X.exercises);
    var html =
      '<div class="home-hero"><h1>SIKD Thesis M1 — Study Space</h1>' +
      "<p><strong>Weather-Aware Scheduling for Simultaneous Information and Key Distribution over Tropical Satellite FSO Channels</strong></p>" +
      '<p class="hh-muted">Trương Tuấn Nghĩa (2540017) · USTH Master Space · M1 defense preparation.</p>' +
      "<p>Two practice modes plus a theory-framework reference. Every item shows the one-line <em>framework</em> it rests on, so you memorise the reasoning, not just the answer.</p>" +
      '<div class="home-ctas">' +
      '<a class="home-cta" href="#/p/1/0">MCQ · 360 questions →</a>' +
      '<a class="home-cta alt" href="#/ex/1/0">Active recall · 90 →</a>' +
      '<a class="home-cta ghost" href="#/review">Review wrong 🔁</a>' +
      '<a class="home-cta ghost" href="#/frameworks">Theory frameworks 🧠</a>' +
      "</div></div>";
    html += '<div class="two-col">';
    html += '<div class="col-card"><h2>MCQ · 360</h2><p class="cc-sub">11 professional viewpoints, basic → advanced, incl. 60 figure/video questions.</p>' +
      '<div class="pb-track"><div class="pb-fill" style="width:' + Math.round(100 * sm.done / sm.total) + '%"></div></div>' +
      '<div class="cc-stat">' + sm.done + " / " + sm.total + " answered" + (sm.done ? " · " + Math.round(100 * sm.correct / sm.done) + "% correct" : "") + "</div></div>";
    html += '<div class="col-card"><h2>Active recall · 90</h2><p class="cc-sub">Fill-in, full calculation, and drag-drop matching/ordering — the deepest test of formula recall.</p>' +
      '<div class="pb-track"><div class="pb-fill alt" style="width:' + Math.round(100 * se.done / se.total) + '%"></div></div>' +
      '<div class="cc-stat">' + se.done + " / " + se.total + " done" + (se.done ? " · " + Math.round(100 * se.correct / se.done) + "% correct" : "") + "</div></div>";
    html += "</div>";
    document.getElementById("content").innerHTML = html;
  }

  /* ---------------- MCQ ---------------- */
  function renderMcq(pn, qi) {
    var list = BY_PERSP[pn];
    qi = Math.max(0, Math.min(qi, list.length - 1));
    var q = list[qi], meta = Q.meta.perspectives.find(function (p) { return p.num === pn; });
    var st = mcqStats(list), pct = Math.round(100 * st.done / st.total);
    var prog = P_MCQ[q.id];
    var html = pageHead("P" + pn + " · " + esc(meta.title), "Question " + (qi + 1) + " of " + list.length + (q.group ? " · " + esc(q.group) : ""), st, pct);
    html += '<div class="qcard"><div class="qhead"><span class="qid">Q' + q.id + "</span>" + (q.group ? '<span class="qgroup">' + esc(q.group) + "</span>" : "") + "</div>";
    html += '<div class="qtext">' + esc(q.question) + '</div><div class="opts" id="opts">';
    q.options.forEach(function (o) {
      var cls = "opt", mark = "";
      if (prog) { cls += " disabled"; if (o.key === q.answer) { cls += " correct"; mark = "✓"; } else if (o.key === prog.chosen) { cls += " wrong"; mark = "✗"; } }
      html += '<div class="' + cls + '" data-key="' + o.key + '"><span class="opt-key">' + o.key + "</span><span class=\"opt-text\">" + esc(o.text) + "</span>" + (mark ? '<span class="opt-mark">' + mark + "</span>" : "") + "</div>";
    });
    html += "</div>";
    html += '<div class="qactions"><button class="btn btn-primary" id="submit-btn"' + (prog ? " disabled" : "") + '>Check answer</button><span class="verdict" id="verdict"></span></div>';
    html += frameworkBox(q.framework, !!prog);
    html += "</div>" + pager("#/p/" + pn + "/", pn, qi, list.length, Q.meta.perspectives, "num", "#/ex/1/0");
    var content = document.getElementById("content"); content.innerHTML = html;

    var verdict = document.getElementById("verdict"), fw = document.getElementById("framework"), submitBtn = document.getElementById("submit-btn");
    if (prog) { verdict.textContent = prog.correct ? "Correct" : "Incorrect — correct answer: " + q.answer; verdict.className = "verdict " + (prog.correct ? "ok" : "bad"); return; }
    var selected = null, optsEl = document.getElementById("opts");
    optsEl.querySelectorAll(".opt").forEach(function (el) {
      el.onclick = function () { selected = el.dataset.key; optsEl.querySelectorAll(".opt").forEach(function (x) { x.classList.remove("selected"); }); el.classList.add("selected"); submitBtn.disabled = false; };
    });
    submitBtn.disabled = true;
    submitBtn.onclick = function () {
      if (!selected) return;
      var correct = selected === q.answer;
      P_MCQ[q.id] = { chosen: selected, correct: correct }; saveMcq();
      optsEl.querySelectorAll(".opt").forEach(function (el) {
        el.classList.add("disabled"); el.onclick = null; el.classList.remove("selected");
        var k = el.dataset.key;
        if (k === q.answer) { el.classList.add("correct"); el.insertAdjacentHTML("beforeend", '<span class="opt-mark">✓</span>'); }
        else if (k === selected) { el.classList.add("wrong"); el.insertAdjacentHTML("beforeend", '<span class="opt-mark">✗</span>'); }
      });
      submitBtn.disabled = true;
      verdict.textContent = correct ? "Correct" : "Incorrect — correct answer: " + q.answer;
      verdict.className = "verdict " + (correct ? "ok" : "bad");
      fw.classList.add("show"); renderNav(); setActive("mcq-" + pn);
    };
  }

  /* ---------------- Exercises ---------------- */
  function renderEx(sn, xi) {
    var list = BY_SEC[sn];
    xi = Math.max(0, Math.min(xi, list.length - 1));
    var e = list[xi], meta = X.meta.sections.find(function (s) { return s.num === sn; });
    var st = exStats(list), pct = Math.round(100 * st.done / st.total);
    var prog = P_EX[e.id];
    var typeLabel = { calc: "Calculation", fill: "Fill in the answer", match: "Drag to match", order: "Drag to order" }[e.type];
    var html = pageHead("S" + sn + " · " + esc(cleanSec(meta.title)), "Exercise " + (xi + 1) + " of " + list.length + " · " + typeLabel, st, pct);
    html += '<div class="qcard"><div class="qhead"><span class="qid">E' + e.id + '</span><span class="qgroup">' + typeLabel + "</span></div>";
    html += '<div class="qtext">' + esc(e.prompt) + "</div>";
    if (e.given) html += '<div class="given">Given: ' + esc(e.given) + "</div>";
    html += bodyFor(e, prog);
    html += '<div class="qactions"><button class="btn btn-primary" id="submit-btn"' + (prog ? " disabled" : "") + ">Check</button>" +
      '<button class="btn btn-ghost" id="reveal-btn"' + (prog ? " disabled" : "") + '>Reveal answer</button><span class="verdict" id="verdict"></span></div>';
    html += frameworkBox(e.framework, !!prog, e.steps);
    html += "</div>" + pager("#/ex/" + sn + "/", sn, xi, list.length, X.meta.sections, "num", "#/frameworks");
    document.getElementById("content").innerHTML = html;
    wireExercise(e, sn, !!prog);
  }

  function bodyFor(e, prog) {
    if (e.type === "calc" || e.type === "fill") {
      var val = prog ? esc(prog.given || "") : "";
      return '<div class="answer-row"><input type="text" id="ex-input" class="ex-input" autocomplete="off" ' +
        'placeholder="' + (e.type === "calc" ? "Type a number" : "Type your answer") + '" value="' + val + '"' + (prog ? " disabled" : "") + ">" +
        (e.unit ? '<span class="ex-unit">' + esc(e.unit) + "</span>" : "") + "</div>";
    }
    if (e.type === "match") {
      var right = shuffleSeeded(e.right.slice(), e.id);
      var chips = right.map(function (r) { return '<div class="chip" draggable="true" data-val="' + esc(r) + '">' + esc(r) + "</div>"; }).join("");
      var rows = e.left.map(function (l, i) {
        return '<div class="match-row"><div class="match-left">' + esc(l) + '</div>' +
          '<div class="slot" data-left="' + esc(l) + '" data-idx="' + i + '"><span class="slot-ph">drop / tap a match</span></div></div>';
      }).join("");
      return '<div class="match-wrap"><div class="chip-pool" id="chip-pool">' + chips + "</div>" +
        '<div class="match-rows" id="match-rows">' + rows + "</div>" +
        '<div class="hint">Drag a chip onto a row — or tap a chip then tap a row. Tap a filled row to clear it.</div></div>';
    }
    if (e.type === "order") {
      var items = shuffleSeeded(e.items.map(function (t, i) { return { t: t, i: i }; }), e.id);
      var rows = items.map(function (o) {
        return '<div class="order-row" draggable="true" data-orig="' + o.i + '">' +
          '<span class="order-handle">≡</span><span class="order-text">' + esc(o.t) + "</span>" +
          '<span class="order-btns"><button class="ord-up" title="up">▲</button><button class="ord-dn" title="down">▼</button></span></div>';
      }).join("");
      return '<div class="order-wrap" id="order-wrap">' + rows + '</div><div class="hint">Drag rows, or use ▲▼, to put them in the correct order (top = first).</div>';
    }
    return "";
  }

  function wireExercise(e, sn, done) {
    var submitBtn = document.getElementById("submit-btn"), revealBtn = document.getElementById("reveal-btn");
    var verdict = document.getElementById("verdict"), fw = document.getElementById("framework");
    if (done) {
      var p = P_EX[e.id];
      verdict.textContent = p.correct ? "Correct" : "Reviewed — see the correct answer & framework below";
      verdict.className = "verdict " + (p.correct ? "ok" : "bad");
      if (e.type === "match" || e.type === "order") showCorrectStatic(e);
      return;
    }
    function finish(correct) {
      P_EX[e.id] = { correct: correct }; saveEx();
      verdict.textContent = correct ? "Correct" : "Not quite — correct answer shown below";
      verdict.className = "verdict " + (correct ? "ok" : "bad");
      submitBtn.disabled = true; revealBtn.disabled = true;
      fw.classList.add("show");
      lockExercise(e);
      renderNav(); setActive("ex-" + sn);
    }

    if (e.type === "calc" || e.type === "fill") {
      var inp = document.getElementById("ex-input");
      inp.oninput = function () { submitBtn.disabled = !inp.value.trim(); };
      submitBtn.disabled = !inp.value.trim();
      submitBtn.onclick = function () {
        var ok = (e.type === "calc") ? gradeCalc(e, inp.value) : gradeFill(e, inp.value);
        inp.disabled = true; inp.classList.add(ok ? "good" : "bad");
        if (!ok) showExpectedInline(e);
        finish(ok);
      };
      revealBtn.onclick = function () { inp.value = String(e.answer) + (e.unit && e.type === "fill" ? "" : ""); showExpectedInline(e); inp.disabled = true; finish(false); };
      inp.addEventListener("keydown", function (ev) { if (ev.key === "Enter" && !submitBtn.disabled) submitBtn.click(); });
    }
    else if (e.type === "match") { wireMatch(e, submitBtn); submitBtn.onclick = function () { finish(gradeMatch(e)); }; revealBtn.onclick = function () { autoFillMatch(e); finish(false); }; }
    else if (e.type === "order") { wireOrder(); submitBtn.disabled = false; submitBtn.onclick = function () { finish(gradeOrder(e)); }; revealBtn.onclick = function () { autoFillOrder(e); finish(false); }; }
  }

  /* ---- grading ---- */
  function parseNum(s) {
    s = String(s).trim().replace(/\s+/g, "");
    if (s.indexOf(",") >= 0 && s.indexOf(".") >= 0) s = s.replace(/,/g, "");
    else s = s.replace(/,/g, ".");
    s = s.replace(/[^0-9eE.+\-]/g, "");
    var v = parseFloat(s); return isNaN(v) ? null : v;
  }
  function gradeCalc(e, input) {
    P_EX[e.id] = P_EX[e.id]; // no-op
    var v = parseNum(input); if (v === null) return false;
    e._given = input;
    var a = e.answer, tol = e.tol;
    if (e.tolType === "abs") return Math.abs(v - a) <= tol;
    var denom = Math.abs(a) < 1e-9 ? 1 : Math.abs(a);
    return Math.abs(v - a) / denom <= tol;
  }
  function normFill(s) { return String(s).toLowerCase().trim().replace(/\s+/g, " ").replace(/[.;]+$/, ""); }
  function gradeFill(e, input) {
    var u = normFill(input), uNoSp = u.replace(/\s+/g, "");
    return e.accept.some(function (a) { var n = normFill(a); return n === u || n.replace(/\s+/g, "") === uNoSp; });
  }
  function gradeMatch(e) {
    return e.left.every(function (l) {
      var slot = document.querySelector('.slot[data-left="' + cssEsc(l) + '"]');
      return slot && slot.dataset.filled === e.pairs[l];
    });
  }
  function gradeOrder(e) {
    var rows = [].slice.call(document.querySelectorAll("#order-wrap .order-row"));
    return rows.every(function (r, idx) { return +r.dataset.orig === e.correctOrder[idx]; });
  }
  function cssEsc(s) { return String(s).replace(/(["\\])/g, "\\$1"); }

  /* ---- match interactions ---- */
  var picked = null;
  function wireMatch(e, submitBtn) {
    var pool = document.getElementById("chip-pool");
    document.querySelectorAll(".chip").forEach(function (c) {
      c.addEventListener("dragstart", function (ev) { ev.dataTransfer.setData("text", c.dataset.val); picked = c; });
      c.onclick = function () { document.querySelectorAll(".chip").forEach(function (x) { x.classList.remove("pick"); }); c.classList.add("pick"); picked = c; };
    });
    document.querySelectorAll(".slot").forEach(function (s) {
      s.addEventListener("dragover", function (ev) { ev.preventDefault(); s.classList.add("over"); });
      s.addEventListener("dragleave", function () { s.classList.remove("over"); });
      s.addEventListener("drop", function (ev) { ev.preventDefault(); s.classList.remove("over"); if (picked) placeChip(s, picked); refreshMatch(e, submitBtn); });
      s.onclick = function () {
        if (s.dataset.filled) { clearSlot(s, pool); refreshMatch(e, submitBtn); return; }
        if (picked) { placeChip(s, picked); refreshMatch(e, submitBtn); }
      };
    });
    refreshMatch(e, submitBtn);
  }
  function placeChip(slot, chip) {
    if (slot.dataset.filled) clearSlot(slot, document.getElementById("chip-pool"));
    slot.dataset.filled = chip.dataset.val;
    slot.innerHTML = '<span class="slot-val">' + esc(chip.dataset.val) + "</span>";
    chip.remove(); picked = null;
  }
  function clearSlot(slot, pool) {
    var v = slot.dataset.filled; if (!v) return;
    delete slot.dataset.filled;
    slot.innerHTML = '<span class="slot-ph">drop / tap a match</span>';
    var c = document.createElement("div"); c.className = "chip"; c.draggable = true; c.dataset.val = v; c.textContent = v;
    pool.appendChild(c);
    c.addEventListener("dragstart", function (ev) { ev.dataTransfer.setData("text", v); picked = c; });
    c.onclick = function () { document.querySelectorAll(".chip").forEach(function (x) { x.classList.remove("pick"); }); c.classList.add("pick"); picked = c; };
  }
  function refreshMatch(e, submitBtn) {
    var all = e.left.every(function (l) { var s = document.querySelector('.slot[data-left="' + cssEsc(l) + '"]'); return s && s.dataset.filled; });
    submitBtn.disabled = !all;
  }
  function autoFillMatch(e) {
    e.left.forEach(function (l) {
      var s = document.querySelector('.slot[data-left="' + cssEsc(l) + '"]');
      s.dataset.filled = e.pairs[l]; s.innerHTML = '<span class="slot-val">' + esc(e.pairs[l]) + "</span>";
    });
  }
  function showCorrectStatic(e) {
    if (e.type === "match") {
      document.querySelectorAll(".slot").forEach(function (s) {
        var l = s.dataset.left, correct = e.pairs[l];
        var got = s.dataset.filled;
        s.classList.add(got === correct ? "slot-ok" : "slot-bad");
        s.innerHTML = '<span class="slot-val">' + esc(correct) + "</span>";
      });
    } else if (e.type === "order") {
      var wrap = document.getElementById("order-wrap");
      wrap.innerHTML = e.correctOrder.map(function (origIdx, pos) {
        return '<div class="order-row static"><span class="order-num">' + (pos + 1) + '.</span><span class="order-text">' + esc(e.items[origIdx]) + "</span></div>";
      }).join("");
    }
  }

  /* ---- order interactions ---- */
  function wireOrder() {
    var wrap = document.getElementById("order-wrap");
    wrap.querySelectorAll(".order-row").forEach(function (row) {
      row.querySelector(".ord-up").onclick = function () { var p = row.previousElementSibling; if (p) wrap.insertBefore(row, p); };
      row.querySelector(".ord-dn").onclick = function () { var n = row.nextElementSibling; if (n) wrap.insertBefore(n, row); };
      row.addEventListener("dragstart", function () { row.classList.add("dragging"); });
      row.addEventListener("dragend", function () { row.classList.remove("dragging"); });
    });
    wrap.addEventListener("dragover", function (ev) {
      ev.preventDefault();
      var dragging = wrap.querySelector(".dragging"); if (!dragging) return;
      var after = null, rows = [].slice.call(wrap.querySelectorAll(".order-row:not(.dragging)"));
      for (var i = 0; i < rows.length; i++) { var box = rows[i].getBoundingClientRect(); if (ev.clientY < box.top + box.height / 2) { after = rows[i]; break; } }
      if (after) wrap.insertBefore(dragging, after); else wrap.appendChild(dragging);
    });
  }
  function autoFillOrder(e) { showCorrectStatic(e); }

  function showExpectedInline(e) {
    var row = document.querySelector(".answer-row");
    if (!row || document.getElementById("expected-line")) return;
    var txt = (e.type === "calc")
      ? "Expected: " + e.answer + (e.unit ? " " + e.unit : "") + "  (±" + (e.tolType === "abs" ? e.tol + " abs" : Math.round(e.tol * 100) + "%") + ")"
      : "Accepted: " + e.answer + (e.unit ? " " + e.unit : "");
    row.insertAdjacentHTML("afterend", '<div id="expected-line" class="expected">' + esc(txt) + "</div>");
  }
  function lockExercise(e) {
    document.querySelectorAll(".chip").forEach(function (c) { c.onclick = null; c.draggable = false; });
    document.querySelectorAll(".slot").forEach(function (s) { s.onclick = null; });
    if (e.type === "match" || e.type === "order") showCorrectStatic(e);
  }

  /* ---------------- Frameworks reference ---------------- */
  function renderFrameworks() {
    var html = '<a class="back-home" href="#/">← Back</a><div class="page-head"><h1>Theory Frameworks 🧠</h1>' +
      '<div class="ph-sub">Every one-line framework behind the 360 MCQs and 90 exercises, grouped for memorisation. Use the search to drill a concept.</div></div>';
    html += '<input type="text" id="fw-search" class="fw-search" placeholder="Search frameworks (e.g. cross-talk, Rytov, Hungarian, Jacquemoud)…">';
    // MCQ frameworks grouped by perspective
    html += '<div id="fw-list">';
    Q.meta.perspectives.forEach(function (p) {
      var arr = BY_PERSP[p.num];
      html += '<div class="fw-group"><h3>MCQ · P' + p.num + " — " + esc(p.title) + "</h3>";
      arr.forEach(function (q) { html += fwItem("Q" + q.id, q.question, q.framework); });
      html += "</div>";
    });
    X.meta.sections.forEach(function (s) {
      var arr = BY_SEC[s.num];
      html += '<div class="fw-group"><h3>Recall · ' + esc(s.title) + "</h3>";
      arr.forEach(function (e) { html += fwItem("E" + e.id, e.prompt, e.framework); });
      html += "</div>";
    });
    html += "</div>";
    document.getElementById("content").innerHTML = html;
    var search = document.getElementById("fw-search");
    search.oninput = function () {
      var t = search.value.toLowerCase().trim();
      document.querySelectorAll(".fw-item").forEach(function (it) {
        it.style.display = (!t || it.textContent.toLowerCase().indexOf(t) >= 0) ? "" : "none";
      });
      document.querySelectorAll(".fw-group").forEach(function (g) {
        var any = [].some.call(g.querySelectorAll(".fw-item"), function (it) { return it.style.display !== "none"; });
        g.style.display = any ? "" : "none";
      });
    };
  }
  function fwItem(tag, prompt, fw) {
    return '<div class="fw-item"><div class="fw-q"><span class="fw-tag">' + tag + "</span> " + esc(prompt) + "</div>" +
      '<div class="fw-a">' + esc(fw) + "</div></div>";
  }

  /* ---------------- Review wrong answers ---------------- */
  function renderReviewHome() {
    var wm = wrongMcq(), we = wrongEx();
    var html = '<a class="back-home" href="#/">← Back</a><div class="page-head"><h1>Review wrong answers 🔁</h1>' +
      '<div class="ph-sub">Re-attempt only the items you got wrong. Fix one and it drops off the list.</div></div>';
    if (!wm.length && !we.length) {
      html += '<div class="qcard" style="text-align:center"><div class="qtext" style="margin:8px 0">🎉 Nothing to review — no wrong answers recorded.</div>' +
        '<p class="cc-sub">Answer some questions first, then come back to drill the ones you miss.</p>' +
        '<a class="btn btn-primary" href="#/p/1/0">Go to MCQ</a> <a class="btn btn-ghost" href="#/ex/1/0">Go to Recall</a></div>';
      document.getElementById("content").innerHTML = html; return;
    }
    html += '<div class="home-ctas">';
    if (wm.length) html += '<a class="home-cta" href="#/review/mcq/0">Review ' + wm.length + ' wrong MCQ →</a>';
    if (we.length) html += '<a class="home-cta alt" href="#/review/ex/0">Review ' + we.length + ' wrong recall →</a>';
    html += "</div>";
    function listBlock(title, items, kind) {
      if (!items.length) return "";
      var h = '<div class="fw-group"><h3>' + title + " (" + items.length + ")</h3>";
      items.forEach(function (it, i) {
        var text = kind === "mcq" ? it.question : it.prompt;
        var tag = (kind === "mcq" ? "Q" : "E") + it.id;
        h += '<a class="fw-item" style="display:block;text-decoration:none" href="#/review/' + kind + "/" + i + '">' +
          '<div class="fw-q"><span class="fw-tag">' + tag + "</span> " + esc(text) + "</div></a>";
      });
      return h + "</div>";
    }
    html += listBlock("Wrong MCQ", wm, "mcq") + listBlock("Wrong recall", we, "ex");
    document.getElementById("content").innerHTML = html;
  }

  function renderReviewItem(kind, i) {
    var list = kind === "mcq" ? wrongMcq() : wrongEx();
    if (!list.length) {
      document.getElementById("content").innerHTML =
        '<a class="back-home" href="#/review">← Review</a><div class="qcard" style="text-align:center">' +
        '<div class="qtext" style="margin:8px 0">🎉 All clear — no wrong ' + (kind === "mcq" ? "MCQ" : "recall") + ' left!</div>' +
        '<a class="btn btn-primary" href="#/review">Back to review</a></div>';
      return;
    }
    i = Math.max(0, Math.min(i, list.length - 1));
    var it = list[i];
    var head = '<a class="back-home" href="#/review">← Review</a>' +
      '<div class="page-head"><h1>Review · wrong ' + (kind === "mcq" ? "MCQ" : "recall") + "</h1>" +
      '<div class="ph-sub">' + list.length + " to fix · retrying " + (kind === "mcq" ? "Q" + it.id : "E" + it.id) + "</div></div>";

    if (kind === "mcq") return reviewMcq(it, head);
    return reviewEx(it, head);
  }

  function reviewPagerHtml() {
    return '<a class="btn btn-ghost" href="#/review">Back to list</a>' +
      '<button class="btn btn-primary" id="rev-next">Next wrong →</button>';
  }
  function wireReviewNext(kind) {
    var btn = document.getElementById("rev-next");
    if (!btn) return;
    btn.onclick = function () {
      var list = kind === "mcq" ? wrongMcq() : wrongEx();
      if (!list.length) { location.hash = "#/review"; }
      else { renderReviewItem(kind, 0); }  // re-render in place (hash may be unchanged)
    };
  }

  function reviewMcq(q, head) {
    var html = head + '<div class="qcard"><div class="qhead"><span class="qid">Q' + q.id + "</span>" +
      (q.group ? '<span class="qgroup">' + esc(q.group) + "</span>" : "") + "</div>" +
      '<div class="qtext">' + esc(q.question) + '</div><div class="opts" id="opts">';
    q.options.forEach(function (o) {
      html += '<div class="opt" data-key="' + o.key + '"><span class="opt-key">' + o.key + '</span><span class="opt-text">' + esc(o.text) + "</span></div>";
    });
    html += '</div><div class="qactions"><button class="btn btn-primary" id="submit-btn" disabled>Check answer</button>' +
      '<span class="verdict" id="verdict"></span></div>' + frameworkBox(q.framework, false) +
      '<div class="pager" id="rev-pager"></div></div>';
    document.getElementById("content").innerHTML = html;
    var selected = null, optsEl = document.getElementById("opts"), submitBtn = document.getElementById("submit-btn"),
        verdict = document.getElementById("verdict"), fw = document.getElementById("framework");
    optsEl.querySelectorAll(".opt").forEach(function (el) {
      el.onclick = function () { selected = el.dataset.key; optsEl.querySelectorAll(".opt").forEach(function (x) { x.classList.remove("selected"); }); el.classList.add("selected"); submitBtn.disabled = false; };
    });
    submitBtn.onclick = function () {
      if (!selected) return;
      var correct = selected === q.answer;
      P_MCQ[q.id] = { chosen: selected, correct: correct }; saveMcq();
      optsEl.querySelectorAll(".opt").forEach(function (el) {
        el.classList.add("disabled"); el.onclick = null; el.classList.remove("selected");
        var k = el.dataset.key;
        if (k === q.answer) { el.classList.add("correct"); el.insertAdjacentHTML("beforeend", '<span class="opt-mark">✓</span>'); }
        else if (k === selected) { el.classList.add("wrong"); el.insertAdjacentHTML("beforeend", '<span class="opt-mark">✗</span>'); }
      });
      submitBtn.disabled = true;
      verdict.textContent = correct ? "Fixed! Correct now." : "Still incorrect — answer: " + q.answer;
      verdict.className = "verdict " + (correct ? "ok" : "bad");
      fw.classList.add("show");
      document.getElementById("rev-pager").innerHTML = reviewPagerHtml();
      wireReviewNext("mcq");
      renderNav();
    };
  }

  function reviewEx(e, head) {
    var typeLabel = { calc: "Calculation", fill: "Fill in the answer", match: "Drag to match", order: "Drag to order" }[e.type];
    var html = head + '<div class="qcard"><div class="qhead"><span class="qid">E' + e.id + '</span><span class="qgroup">' + typeLabel + "</span></div>" +
      '<div class="qtext">' + esc(e.prompt) + "</div>" + (e.given ? '<div class="given">Given: ' + esc(e.given) + "</div>" : "") +
      bodyFor(e, null) +
      '<div class="qactions"><button class="btn btn-primary" id="submit-btn">Check</button>' +
      '<button class="btn btn-ghost" id="reveal-btn">Reveal answer</button><span class="verdict" id="verdict"></span></div>' +
      frameworkBox(e.framework, false, e.steps) + '<div class="pager" id="rev-pager"></div></div>';
    document.getElementById("content").innerHTML = html;
    var submitBtn = document.getElementById("submit-btn"), revealBtn = document.getElementById("reveal-btn"),
        verdict = document.getElementById("verdict"), fw = document.getElementById("framework");
    function done(correct) {
      P_EX[e.id] = { correct: correct }; saveEx();
      verdict.textContent = correct ? "Fixed! Correct now." : "Still not right — correct answer shown below";
      verdict.className = "verdict " + (correct ? "ok" : "bad");
      submitBtn.disabled = true; revealBtn.disabled = true; fw.classList.add("show"); lockExercise(e);
      document.getElementById("rev-pager").innerHTML = reviewPagerHtml();
      wireReviewNext("ex");
      renderNav();
    }
    if (e.type === "calc" || e.type === "fill") {
      var inp = document.getElementById("ex-input");
      inp.oninput = function () { submitBtn.disabled = !inp.value.trim(); };
      submitBtn.disabled = true;
      submitBtn.onclick = function () { var ok = e.type === "calc" ? gradeCalc(e, inp.value) : gradeFill(e, inp.value); inp.disabled = true; inp.classList.add(ok ? "good" : "bad"); if (!ok) showExpectedInline(e); done(ok); };
      revealBtn.onclick = function () { showExpectedInline(e); inp.disabled = true; done(false); };
      inp.addEventListener("keydown", function (ev) { if (ev.key === "Enter" && !submitBtn.disabled) submitBtn.click(); });
    } else if (e.type === "match") { wireMatch(e, submitBtn); submitBtn.onclick = function () { done(gradeMatch(e)); }; revealBtn.onclick = function () { autoFillMatch(e); done(false); }; }
    else if (e.type === "order") { wireOrder(); submitBtn.onclick = function () { done(gradeOrder(e)); }; revealBtn.onclick = function () { autoFillOrder(e); done(false); }; }
  }

  /* ---------------- shared bits ---------------- */
  function pageHead(title, sub, st, pct) {
    return '<div class="page-head"><h1>' + title + '</h1><div class="ph-sub">' + sub + "</div></div>" +
      '<div class="persp-bar"><div class="pb-prog"><div class="pb-track"><div class="pb-fill" style="width:' + pct + '%"></div></div></div>' +
      '<div class="pb-num">' + st.done + "/" + st.total + " done" + (st.done ? " · " + Math.round(100 * st.correct / st.done) + "% correct" : "") + "</div></div>";
  }
  function frameworkBox(fw, show, steps) {
    var s = steps ? '<div class="fw-steps">' + esc(steps) + "</div>" : "";
    return '<div class="framework' + (show ? " show" : "") + '" id="framework"><div class="fw-label">Theory framework</div>' + esc(fw) + s + "</div>";
  }
  function pager(base, num, i, len, arr, key, nextModeHref) {
    var html = '<div class="pager">';
    html += i > 0 ? '<a class="btn btn-ghost" href="' + base + (i - 1) + '">← Prev</a>' : "<span></span>";
    if (i < len - 1) html += '<a class="btn btn-primary" href="' + base + (i + 1) + '">Next →</a>';
    else {
      var idx = arr.findIndex(function (o) { return o[key] === num; });
      if (idx < arr.length - 1) html += '<a class="btn btn-primary" href="' + base.replace(/\/\d+\/$/, "/") + arr[idx + 1][key] + '/0">Next section →</a>';
      else html += '<a class="btn btn-primary" href="' + nextModeHref + '">Continue →</a>';
    }
    return html + "</div>";
  }

  function renderResources() {
    var html = '<a class="back-home" href="#/">← Back</a><div class="page-head"><h1>Study resources</h1><div class="ph-sub">Full-length PDFs behind the practice sets.</div></div><div class="res-grid">';
    RESOURCES.forEach(function (r) {
      html += '<a class="res-card" href="' + r.file + '" target="_blank" rel="noopener"><div class="rc-icon">' + r.icon + '</div><div class="rc-title">' + esc(r.title) + '</div><div class="rc-desc">' + esc(r.desc) + '</div><div class="rc-meta">PDF · opens in new tab</div></a>';
    });
    html += "</div>"; document.getElementById("content").innerHTML = html;
  }

  /* deterministic shuffle so option order is stable per item across reloads */
  function shuffleSeeded(arr, seed) {
    var a = arr.slice(), s = seed * 2654435761 % 2147483647 || 1;
    for (var i = a.length - 1; i > 0; i--) { s = (s * 16807) % 2147483647; var j = s % (i + 1); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }

  document.getElementById("reset-btn").onclick = function () {
    if (confirm("Clear ALL saved progress (MCQ + Recall) on this browser?")) { P_MCQ = {}; P_EX = {}; saveMcq(); saveEx(); route(); }
  };
  // wire the framework + resources links in the sidebar footer (static in HTML)
  boot();
})();
