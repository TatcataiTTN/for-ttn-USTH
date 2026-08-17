/* SIKD Thesis M1 — 360-question practice bank (vanilla JS, static, no backend).
   Grading = compare the learner's chosen letter to the answer parsed from the
   source .md at build time (never hand-typed). Progress in localStorage only. */
(function () {
  "use strict";

  var LS_KEY = "sikd_m1_progress_v1";
  var DATA = null;          // {meta, questions}
  var BY_PERSP = {};        // perspective num -> [questions]
  var PROGRESS = load();    // { "<id>": {chosen:"B", correct:true} }

  // Resource PDFs shipped alongside the site (see resources/).
  var RESOURCES = [
    { file: "resources/SIKD_Formula_Guide_v3_Expanded.pdf", icon: "📘",
      title: "Formula Guide v3 (Expanded)",
      desc: "Corrected v3 physics, old→new correction table, organised basic → advanced." },
    { file: "resources/SIKD_Weather_Formula_Guide.pdf", icon: "📗",
      title: "Formula Guide (original, pre-v3)",
      desc: "The earlier 50-formula guide with many drill examples. Numbers are pre-v3 — use v3 for figures." },
    { file: "resources/SIKD_Exercises_Solutions.pdf", icon: "📐",
      title: "Exercises & Solutions",
      desc: "Worked problems by topic with full step-by-step solutions." },
    { file: "resources/SIKD_Practice_Exam_80MCQ.pdf", icon: "📝",
      title: "80-MCQ Practice Exam",
      desc: "A separate multiple-choice exam with an answer grid." },
    { file: "resources/SIKD_Committee_Analysis.pdf", icon: "🎓",
      title: "Committee Analysis & Predicted Q&A",
      desc: "Examiner-by-examiner (Jacquemoud / Patanchon / Rosset) predicted questions and prepared answers." },
    { file: "resources/SIKD_Literature_Review.pdf", icon: "📚",
      title: "Literature Review",
      desc: "34 real references mapped to their role in the thesis and to each examiner." },
    { file: "resources/Defense_Slides.pdf", icon: "🖥️",
      title: "Defense Slides (9-slide, 10 min)",
      desc: "The M1 defense deck with v3 numbers." }
  ];

  function load() {
    try { return JSON.parse(localStorage.getItem(LS_KEY)) || {}; }
    catch (e) { return {}; }
  }
  function save() {
    try { localStorage.setItem(LS_KEY, JSON.stringify(PROGRESS)); } catch (e) {}
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function boot() {
    fetch("data/questions.json", { cache: "no-cache" })
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (j) {
        DATA = j;
        BY_PERSP = {};
        j.questions.forEach(function (q) {
          (BY_PERSP[q.perspective] = BY_PERSP[q.perspective] || []).push(q);
        });
        renderNav();
        window.addEventListener("hashchange", route);
        route();
      })
      .catch(function (e) {
        document.getElementById("content").innerHTML =
          '<div class="loading">Could not load the question bank (' + esc(e.message) +
          ').<br><button class="btn btn-primary" onclick="location.reload()">Retry</button></div>';
      });
  }

  function statsFor(list) {
    var done = 0, correct = 0;
    list.forEach(function (q) {
      var p = PROGRESS[q.id];
      if (p) { done++; if (p.correct) correct++; }
    });
    return { done: done, correct: correct, total: list.length };
  }

  function renderNav() {
    var nav = document.getElementById("nav");
    nav.innerHTML = "";
    DATA.meta.perspectives.forEach(function (p) {
      var list = BY_PERSP[p.num] || [];
      var st = statsFor(list);
      var btn = document.createElement("button");
      btn.className = "nav-item";
      btn.dataset.persp = p.num;
      var pct = st.total ? Math.round(100 * st.done / st.total) : 0;
      btn.innerHTML =
        '<span class="ni-top"><span class="ni-num">P' + p.num + '</span>' +
        '<span class="ni-count">' + st.done + "/" + st.total + '</span></span>' +
        '<span class="ni-title">' + esc(p.title) + "</span>" +
        '<span class="ni-mini"><i style="width:' + pct + '%"></i></span>';
      btn.onclick = function () { location.hash = "#/p/" + p.num; };
      nav.appendChild(btn);
    });
    renderOverall();
  }

  function renderOverall() {
    var st = statsFor(DATA.questions);
    var pct = Math.round(100 * st.done / st.total);
    var acc = st.done ? Math.round(100 * st.correct / st.done) : 0;
    document.getElementById("overall-progress").innerHTML =
      "<div><strong>Overall progress</strong></div>" +
      '<div class="op-bar"><div class="op-fill" style="width:' + pct + '%"></div></div>' +
      '<div class="op-stats"><span>' + st.done + " / " + st.total + " answered</span>" +
      "<span>" + acc + "% correct</span></div>";
  }

  function setActive(perspNum) {
    document.querySelectorAll(".nav-item").forEach(function (b) {
      b.classList.toggle("active", perspNum != null && b.dataset.persp == String(perspNum));
    });
  }

  function route() {
    var h = location.hash || "#/";
    var content = document.getElementById("content");
    content.scrollTop = 0;
    window.scrollTo(0, 0);
    if (h === "#/resources") { setActive(null); return renderResources(); }
    var m = h.match(/^#\/p\/(\d+)(?:\/(\d+))?$/);
    if (m) {
      var pn = parseInt(m[1], 10);
      var qi = m[2] ? parseInt(m[2], 10) : 0;
      if (BY_PERSP[pn]) { setActive(pn); return renderPerspective(pn, qi); }
    }
    setActive(null);
    renderHome();
  }

  function renderHome() {
    var st = statsFor(DATA.questions);
    var firstPersp = DATA.meta.perspectives[0].num;
    var resume = null;
    // resume = first unanswered question
    for (var i = 0; i < DATA.questions.length; i++) {
      if (!PROGRESS[DATA.questions[i].id]) { resume = DATA.questions[i]; break; }
    }
    var cta = resume
      ? '#/p/' + resume.perspective + '/' + (BY_PERSP[resume.perspective].indexOf(resume))
      : '#/p/' + firstPersp;
    var html =
      '<div class="home-hero">' +
      "<h1>360-Question Practice Bank</h1>" +
      "<p><strong>Weather-Aware Scheduling for Simultaneous Information and Key Distribution over Tropical Satellite FSO Channels</strong></p>" +
      '<p class="hh-muted">Trương Tuấn Nghĩa (2540017) · USTH Master Space · M1 defense preparation.</p>' +
      "<p>Every question carries its answer and a one-line <em>theory framework</em>, seen from 11 professional viewpoints — from basic definitions to research-level judgement, including 60 figure/diagram/video-reading questions.</p>" +
      '<a class="home-cta" href="' + cta + '">' + (st.done ? "Resume practice →" : "Start practising →") + "</a>" +
      "</div>";
    html += "<div class=\"res-grid\">";
    DATA.meta.perspectives.forEach(function (p) {
      var list = BY_PERSP[p.num]; var s = statsFor(list);
      html +=
        '<a class="res-card" href="#/p/' + p.num + '">' +
        '<div class="rc-icon">🧭</div>' +
        '<div class="rc-title">P' + p.num + " · " + esc(p.title) + "</div>" +
        '<div class="rc-desc">' + s.done + " / " + s.total + " answered" +
        (s.done ? " · " + Math.round(100 * s.correct / s.done) + "% correct" : "") + "</div></a>";
    });
    html += "</div>";
    document.getElementById("content").innerHTML = html;
  }

  function renderPerspective(pn, qi) {
    var list = BY_PERSP[pn];
    if (qi < 0) qi = 0;
    if (qi >= list.length) qi = list.length - 1;
    var q = list[qi];
    var meta = DATA.meta.perspectives.find(function (p) { return p.num === pn; });
    var st = statsFor(list);
    var pct = st.total ? Math.round(100 * st.done / st.total) : 0;
    var prog = PROGRESS[q.id];

    var html =
      '<div class="page-head"><h1>P' + pn + " · " + esc(meta.title) + "</h1>" +
      '<div class="ph-sub">Question ' + (qi + 1) + " of " + list.length +
      (q.group ? " · " + esc(q.group) : "") + "</div></div>" +
      '<div class="persp-bar"><div class="pb-prog"><div class="pb-track"><div class="pb-fill" style="width:' +
      pct + '%"></div></div></div><div class="pb-num">' + st.done + "/" + st.total +
      " answered · " + (st.done ? Math.round(100 * st.correct / st.done) + "% correct" : "—") + "</div></div>";

    html += '<div class="qcard">';
    html += '<div class="qhead"><span class="qid">Q' + q.id + "</span>" +
      (q.group ? '<span class="qgroup">' + esc(q.group) + "</span>" : "") + "</div>";
    html += '<div class="qtext">' + esc(q.question) + "</div>";
    html += '<div class="opts" id="opts">';
    q.options.forEach(function (o) {
      var cls = "opt";
      if (prog) {
        cls += " disabled";
        if (o.key === q.answer) cls += " correct";
        else if (o.key === prog.chosen) cls += " wrong";
      }
      var mark = "";
      if (prog) {
        if (o.key === q.answer) mark = "✓";
        else if (o.key === prog.chosen) mark = "✗";
      }
      html += '<div class="' + cls + '" data-key="' + o.key + '">' +
        '<span class="opt-key">' + o.key + "</span>" +
        '<span class="opt-text">' + esc(o.text) + "</span>" +
        (mark ? '<span class="opt-mark">' + mark + "</span>" : "") + "</div>";
    });
    html += "</div>";

    html += '<div class="qactions">' +
      '<button class="btn btn-primary" id="submit-btn"' + (prog ? " disabled" : "") + ">Check answer</button>" +
      '<span class="verdict" id="verdict"></span></div>';

    html += '<div class="framework' + (prog ? " show" : "") + '" id="framework">' +
      '<div class="fw-label">Theory framework</div>' + esc(q.framework) + "</div>";
    html += "</div>";

    // pager
    html += '<div class="pager">';
    html += qi > 0
      ? '<a class="btn btn-ghost" href="#/p/' + pn + "/" + (qi - 1) + '">← Prev</a>'
      : "<span></span>";
    if (qi < list.length - 1) {
      html += '<a class="btn btn-primary" id="next-btn" href="#/p/' + pn + "/" + (qi + 1) + '">Next →</a>';
    } else {
      var idx = DATA.meta.perspectives.findIndex(function (p) { return p.num === pn; });
      if (idx < DATA.meta.perspectives.length - 1) {
        var np = DATA.meta.perspectives[idx + 1].num;
        html += '<a class="btn btn-primary" href="#/p/' + np + '/0">Next section →</a>';
      } else {
        html += '<a class="btn btn-primary" href="#/">Finish → Home</a>';
      }
    }
    html += "</div>";

    var content = document.getElementById("content");
    content.innerHTML = html;

    var selected = null;
    var optsEl = document.getElementById("opts");
    var submitBtn = document.getElementById("submit-btn");
    var verdict = document.getElementById("verdict");
    var fw = document.getElementById("framework");

    if (prog) {
      verdict.textContent = prog.correct ? "Correct" : "Incorrect — correct answer: " + q.answer;
      verdict.className = "verdict " + (prog.correct ? "ok" : "bad");
    }

    if (!prog) {
      optsEl.querySelectorAll(".opt").forEach(function (el) {
        el.onclick = function () {
          selected = el.dataset.key;
          optsEl.querySelectorAll(".opt").forEach(function (x) { x.classList.remove("selected"); });
          el.classList.add("selected");
          submitBtn.disabled = false;
        };
      });
      submitBtn.disabled = true;
      submitBtn.onclick = function () {
        if (!selected) return;
        var correct = selected === q.answer;
        PROGRESS[q.id] = { chosen: selected, correct: correct };
        save();
        optsEl.querySelectorAll(".opt").forEach(function (el) {
          el.classList.add("disabled");
          el.onclick = null;
          el.classList.remove("selected");
          var k = el.dataset.key;
          if (k === q.answer) {
            el.classList.add("correct");
            el.insertAdjacentHTML("beforeend", '<span class="opt-mark">✓</span>');
          } else if (k === selected) {
            el.classList.add("wrong");
            el.insertAdjacentHTML("beforeend", '<span class="opt-mark">✗</span>');
          }
        });
        submitBtn.disabled = true;
        verdict.textContent = correct ? "Correct" : "Incorrect — correct answer: " + q.answer;
        verdict.className = "verdict " + (correct ? "ok" : "bad");
        fw.classList.add("show");
        renderNav();
        setActive(pn);
        // update this page's progress bar
        var st2 = statsFor(list);
        var pct2 = Math.round(100 * st2.done / st2.total);
        var fill = content.querySelector(".pb-fill"); if (fill) fill.style.width = pct2 + "%";
        var num = content.querySelector(".pb-num");
        if (num) num.textContent = st2.done + "/" + st2.total + " answered · " +
          Math.round(100 * st2.correct / st2.done) + "% correct";
        var nb = document.getElementById("next-btn"); if (nb) nb.focus();
      };
    }
  }

  function renderResources() {
    var html = '<a class="back-home" href="#/">← Back to practice</a>' +
      '<div class="page-head"><h1>Study resources</h1>' +
      '<div class="ph-sub">Full-length PDFs that back the question bank. Open or download; they render in the browser.</div></div>';
    html += '<div class="res-grid">';
    RESOURCES.forEach(function (r) {
      html += '<a class="res-card" href="' + r.file + '" target="_blank" rel="noopener">' +
        '<div class="rc-icon">' + r.icon + "</div>" +
        '<div class="rc-title">' + esc(r.title) + "</div>" +
        '<div class="rc-desc">' + esc(r.desc) + "</div>" +
        '<div class="rc-meta">PDF · opens in new tab</div></a>';
    });
    html += "</div>";
    document.getElementById("content").innerHTML = html;
  }

  document.getElementById("reset-btn").onclick = function () {
    if (confirm("Clear all saved progress on this browser?")) {
      PROGRESS = {}; save(); renderNav(); route();
    }
  };

  boot();
})();
