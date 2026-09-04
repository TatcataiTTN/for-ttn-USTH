/* VSEO6 study app — vanilla JS, static, no backend.
   MCQ practice (52 questions / 7 modules) + schedule + speakers pages.
   Grading is client-side; correct answers were parsed programmatically from
   the source Markdown at build time (build/parse_questions.py), never hand-typed.
   Progress: localStorage only. */
(function () {
  "use strict";

  var LS_MCQ = "vseo6_progress_v1";
  var Q = null;      // {meta, questions}
  var SCHED = null;  // schedule.json
  var SPK = null;    // speakers.json
  var BY_PERSP = {};
  var P_MCQ = load(LS_MCQ); // id -> {chosen, correct}
  var LOAD_TIMEOUT_MS = 30000;

  function load(k) { try { return JSON.parse(localStorage.getItem(k)) || {}; } catch (e) { return {}; } }
  function saveMcq() { try { localStorage.setItem(LS_MCQ, JSON.stringify(P_MCQ)); } catch (e) {} }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function boot() {
    var timedOut = false;
    var timer = setTimeout(function () {
      timedOut = true;
      showLoadError(new Error("Quá thời gian chờ tải dữ liệu (30s)"));
    }, LOAD_TIMEOUT_MS);

    Promise.all([
      fetch("data/questions.json", { cache: "no-cache" }).then(chk),
      fetch("data/schedule.json", { cache: "no-cache" }).then(chk),
      fetch("data/speakers.json", { cache: "no-cache" }).then(chk)
    ]).then(function (r) {
      if (timedOut) return;
      clearTimeout(timer);
      Q = r[0]; SCHED = r[1]; SPK = r[2];
      Q.questions.forEach(function (q) { (BY_PERSP[q.perspective] = BY_PERSP[q.perspective] || []).push(q); });
      window.addEventListener("hashchange", route);
      route();
    }).catch(function (e) {
      if (timedOut) return;
      clearTimeout(timer);
      showLoadError(e);
    });
  }
  function chk(r) { if (!r.ok) throw new Error("HTTP " + r.status + " — " + r.url); return r.json(); }
  function showLoadError(e) {
    document.getElementById("content").innerHTML =
      '<div class="loading">Không tải được dữ liệu (' + esc(e.message) +
      ').<br><button class="btn btn-primary" onclick="location.reload()">Thử lại</button></div>';
  }

  /* ---------------- sidebar ---------------- */
  function renderNav() {
    var nav = document.getElementById("nav");
    var list = "";
    Q.meta.perspectives.forEach(function (p) {
      var arr = BY_PERSP[p.num]; var st = mcqStats(arr);
      var pct = st.total ? Math.round(100 * st.done / st.total) : 0;
      list += navItem("#/p/" + p.num + "/0", "M" + p.num, p.title, st, pct, "mcq-" + p.num);
    });
    nav.innerHTML = list;
    renderOverall();
  }
  function navItem(href, tag, title, st, pct, key) {
    return '<a class="nav-item" data-key="' + key + '" href="' + href + '">' +
      '<span class="ni-top"><span class="ni-num">' + tag + '</span>' +
      '<span class="ni-count">' + st.done + "/" + st.total + "</span></span>" +
      '<span class="ni-title">' + esc(title) + "</span>" +
      '<span class="ni-mini"><i style="width:' + pct + '%"></i></span></a>';
  }
  function renderOverall() {
    var sm = mcqStats(Q.questions);
    var pm = sm.total ? Math.round(100 * sm.done / sm.total) : 0;
    document.getElementById("overall-progress").innerHTML =
      "<div><strong>Tiến độ chung</strong></div>" +
      '<div class="op-row"><span>MCQ</span><span>' + sm.done + "/" + sm.total + " · " + (sm.done ? Math.round(100 * sm.correct / sm.done) : 0) + "%</span></div>" +
      '<div class="op-bar"><div class="op-fill" style="width:' + pm + '%"></div></div>';
  }
  function mcqStats(list) { var d = 0, c = 0; list.forEach(function (q) { var p = P_MCQ[q.id]; if (p) { d++; if (p.correct) c++; } }); return { done: d, correct: c, total: list.length }; }
  function setActive(key) { document.querySelectorAll(".nav-item").forEach(function (b) { b.classList.toggle("active", b.dataset.key === key); }); }
  function wrongMcq() { return Q.questions.filter(function (q) { var p = P_MCQ[q.id]; return p && !p.correct; }); }

  /* ---------------- router ---------------- */
  function route() {
    var h = location.hash || "#/";
    window.scrollTo(0, 0);
    renderNav();
    if (h === "#/schedule") { setActive(null); return renderSchedule(); }
    if (h === "#/speakers") { setActive(null); return renderSpeakers(); }
    if (h === "#/review") { setActive(null); return renderReviewHome(); }
    var rv = h.match(/^#\/review\/(\d+)$/);
    if (rv) { setActive(null); return renderReviewItem(+rv[1]); }
    var mp = h.match(/^#\/p\/(\d+)(?:\/(\d+))?$/);
    if (mp && BY_PERSP[+mp[1]]) { setActive("mcq-" + mp[1]); return renderMcq(+mp[1], mp[2] ? +mp[2] : 0); }
    setActive(null); renderHome();
  }

  /* ---------------- home ---------------- */
  function renderHome() {
    var sm = mcqStats(Q.questions);
    var html =
      '<div class="home-hero"><h1>VSEO6 — Study Space</h1>' +
      "<p><strong>Satellite Altimetry: A Tool for Continental Water Monitoring</strong></p>" +
      '<p class="hh-muted">The 6th Vietnam School of Earth Observation · ICISE, Quy Nhơn · 7–12/9/2026 · Tổ chức bởi Rencontres du Vietnam (đối tác UNESCO).</p>' +
      "<p>52 câu hỏi trắc nghiệm tự chấm điểm, chia theo 7 module lý thuyết bám sát chương trình giảng dạy thật của khóa học — từ Nadir altimetry cổ điển tới SWOT, Copernicus, hydroweb.next, data assimilation và giám sát lũ lụt xuyên biên giới Mekong.</p>" +
      '<div class="home-ctas">' +
      '<a class="home-cta" href="#/p/1/0">Bắt đầu Module 1 →</a>' +
      '<a class="home-cta alt" href="#/schedule">Xem lịch trình 🗓️</a>' +
      '<a class="home-cta ghost" href="#/speakers">Giảng viên & công bố 🎓</a>' +
      '<a class="home-cta ghost" href="#/review">Ôn lại câu sai 🔁</a>' +
      "</div></div>";
    html += '<div class="two-col">';
    Q.meta.perspectives.forEach(function (p) {
      var arr = BY_PERSP[p.num]; var st = mcqStats(arr);
      var pct = st.total ? Math.round(100 * st.done / st.total) : 0;
      html += '<div class="col-card"><h2>M' + p.num + ' · ' + esc(p.title) + '</h2>' +
        '<div class="pb-track"><div class="pb-fill" style="width:' + pct + '%"></div></div>' +
        '<div class="cc-stat">' + st.done + " / " + st.total + " đã làm" + (st.done ? " · " + Math.round(100 * st.correct / st.done) + "% đúng" : "") +
        '</div><a class="btn btn-ghost" style="margin-top:8px;display:inline-block" href="#/p/' + p.num + '/0">Vào module →</a></div>';
    });
    html += "</div>";
    document.getElementById("content").innerHTML = html;
  }

  /* ---------------- MCQ ---------------- */
  function renderMcq(pn, qi) {
    var list = BY_PERSP[pn];
    qi = Math.max(0, Math.min(qi, list.length - 1));
    var q = list[qi], meta = Q.meta.perspectives.find(function (p) { return p.num === pn; });
    var st = mcqStats(list), pct = st.total ? Math.round(100 * st.done / st.total) : 0;
    var prog = P_MCQ[q.id];
    var html = pageHead("M" + pn + " · " + esc(meta.title), "Câu " + (qi + 1) + " / " + list.length, st, pct);
    html += '<div class="qcard"><div class="qhead"><span class="qid">Q' + q.id + "</span></div>";
    html += '<div class="qtext">' + esc(q.question) + '</div><div class="opts" id="opts">';
    q.options.forEach(function (o) {
      var cls = "opt", mark = "";
      if (prog) { cls += " disabled"; if (o.key === q.answer) { cls += " correct"; mark = "✓"; } else if (o.key === prog.chosen) { cls += " wrong"; mark = "✗"; } }
      html += '<div class="' + cls + '" data-key="' + o.key + '"><span class="opt-key">' + o.key + "</span><span class=\"opt-text\">" + esc(o.text) + "</span>" + (mark ? '<span class="opt-mark">' + mark + "</span>" : "") + "</div>";
    });
    html += "</div>";
    html += '<div class="qactions"><button class="btn btn-primary" id="submit-btn"' + (prog ? " disabled" : "") + '>Kiểm tra</button><span class="verdict" id="verdict"></span></div>';
    html += frameworkBox(q.framework, !!prog);
    html += "</div>" + pager("#/p/" + pn + "/", pn, qi, list.length, Q.meta.perspectives);
    document.getElementById("content").innerHTML = html;

    var verdict = document.getElementById("verdict"), fw = document.getElementById("framework"), submitBtn = document.getElementById("submit-btn");
    if (prog) { verdict.textContent = prog.correct ? "Chính xác" : "Chưa đúng — đáp án đúng: " + q.answer; verdict.className = "verdict " + (prog.correct ? "ok" : "bad"); return; }
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
      verdict.textContent = correct ? "Chính xác" : "Chưa đúng — đáp án đúng: " + q.answer;
      verdict.className = "verdict " + (correct ? "ok" : "bad");
      fw.classList.add("show"); renderNav(); setActive("mcq-" + pn);
    };
  }

  /* ---------------- Review wrong ---------------- */
  function renderReviewHome() {
    var wm = wrongMcq();
    var html = '<a class="back-home" href="#/">← Trang chủ</a><div class="page-head"><h1>Ôn lại câu sai 🔁</h1>' +
      '<div class="ph-sub">Làm lại đúng những câu bạn từng chọn sai. Sửa xong, câu đó sẽ tự động rời khỏi danh sách này.</div></div>';
    if (!wm.length) {
      html += '<div class="qcard" style="text-align:center"><div class="qtext" style="margin:8px 0">🎉 Không còn câu nào sai — tuyệt vời!</div>' +
        '<a class="btn btn-primary" href="#/p/1/0">Về Module 1</a></div>';
      document.getElementById("content").innerHTML = html; return;
    }
    html += '<div class="home-ctas"><a class="home-cta" href="#/review/0">Ôn ' + wm.length + ' câu sai →</a></div>';
    html += '<div class="fw-group"><h3>Danh sách câu sai (' + wm.length + ')</h3>';
    wm.forEach(function (it, i) {
      html += '<a class="fw-item" style="display:block;text-decoration:none" href="#/review/' + i + '">' +
        '<div class="fw-q"><span class="fw-tag">Q' + it.id + "</span> " + esc(it.question) + "</div></a>";
    });
    html += "</div>";
    document.getElementById("content").innerHTML = html;
  }
  function renderReviewItem(i) {
    var list = wrongMcq();
    if (!list.length) {
      document.getElementById("content").innerHTML =
        '<a class="back-home" href="#/review">← Ôn tập</a><div class="qcard" style="text-align:center">' +
        '<div class="qtext" style="margin:8px 0">🎉 Đã hết câu sai!</div><a class="btn btn-primary" href="#/review">Về trang ôn tập</a></div>';
      return;
    }
    i = Math.max(0, Math.min(i, list.length - 1));
    var q = list[i];
    var head = '<a class="back-home" href="#/review">← Ôn tập</a><div class="page-head"><h1>Ôn lại câu sai</h1>' +
      '<div class="ph-sub">' + list.length + " câu cần sửa · đang làm Q" + q.id + "</div></div>";
    var html = head + '<div class="qcard"><div class="qhead"><span class="qid">Q' + q.id + "</span></div>" +
      '<div class="qtext">' + esc(q.question) + '</div><div class="opts" id="opts">';
    q.options.forEach(function (o) {
      html += '<div class="opt" data-key="' + o.key + '"><span class="opt-key">' + o.key + '</span><span class="opt-text">' + esc(o.text) + "</span></div>";
    });
    html += '</div><div class="qactions"><button class="btn btn-primary" id="submit-btn" disabled>Kiểm tra</button>' +
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
      verdict.textContent = correct ? "Đã sửa đúng!" : "Vẫn sai — đáp án đúng: " + q.answer;
      verdict.className = "verdict " + (correct ? "ok" : "bad");
      fw.classList.add("show");
      var remain = wrongMcq();
      document.getElementById("rev-pager").innerHTML = '<a class="btn btn-ghost" href="#/review">Về danh sách</a>' +
        (remain.length ? '<button class="btn btn-primary" id="rev-next">Câu sai tiếp theo →</button>' : "");
      var nb = document.getElementById("rev-next");
      if (nb) nb.onclick = function () { renderReviewItem(0); };
      renderNav();
    };
  }

  /* ---------------- Schedule ---------------- */
  function renderSchedule() {
    var m = SCHED.meta;
    var html = '<a class="back-home" href="#/">← Trang chủ</a><div class="page-head"><h1>Lịch trình VSEO6</h1>' +
      '<div class="ph-sub">' + esc(m.dates) + " · " + esc(m.venue) + " · Tổ chức: " + esc(m.organizer) + "</div></div>";
    html += '<div class="qcard"><div class="qtext" style="margin-bottom:4px">Liên hệ: ' + esc(m.contact) + '</div>' +
      '<div class="cc-sub">Nguồn: <a href="' + esc(m.source) + '" target="_blank" rel="noopener">' + esc(m.source) + '</a></div></div>';
    SCHED.days.forEach(function (d) {
      html += '<div class="fw-group"><h3>' + esc(d.date) + " — " + esc(d.theme) + '</h3><div class="sched-table">';
      d.sessions.forEach(function (s) {
        html += '<div class="sched-row"><div class="sched-time">' + esc(s.time) + '</div>' +
          '<div class="sched-body"><div class="sched-title">' + esc(s.title) + '</div>' +
          (s.speakers ? '<div class="sched-speakers">' + esc(s.speakers) + '</div>' : '') + '</div></div>';
      });
      html += "</div></div>";
    });
    document.getElementById("content").innerHTML = html;
  }

  /* ---------------- Speakers ---------------- */
  function renderSpeakers() {
    var html = '<a class="back-home" href="#/">← Trang chủ</a><div class="page-head"><h1>Giảng viên & công bố khoa học</h1>' +
      '<div class="ph-sub">Đơn vị công tác và công bố tiêu biểu, tra cứu qua ResearchGate/Google Scholar/HESS/AGU/hydro-matters.fr. Nơi không tìm thấy nguồn đáng tin cậy được ghi rõ thay vì suy đoán.</div></div>';
    SPK.speakers.forEach(function (s) {
      html += '<div class="qcard speaker-card"><h2 style="margin:0 0 4px">' + esc(s.name) + '</h2>' +
        '<div class="cc-sub" style="margin-bottom:8px">' + esc(s.affiliation) + '</div>' +
        '<div class="qtext" style="font-size:14px;margin-bottom:8px">' + esc(s.bio) + '</div>';
      if (s.publications && s.publications.length) {
        html += '<div class="fw-label">Công bố tiêu biểu</div><ul class="pub-list">';
        s.publications.forEach(function (p) { html += "<li>" + esc(p) + "</li>"; });
        html += "</ul>";
      }
      if (s.source) html += '<div class="cc-sub">Nguồn: <a href="' + esc(s.source) + '" target="_blank" rel="noopener">' + esc(s.source) + '</a></div>';
      html += "</div>";
    });
    document.getElementById("content").innerHTML = html;
  }

  /* ---------------- shared bits ---------------- */
  function pageHead(title, sub, st, pct) {
    return '<div class="page-head"><h1>' + title + '</h1><div class="ph-sub">' + sub + "</div></div>" +
      '<div class="persp-bar"><div class="pb-prog"><div class="pb-track"><div class="pb-fill" style="width:' + pct + '%"></div></div></div>' +
      '<div class="pb-num">' + st.done + "/" + st.total + " đã làm" + (st.done ? " · " + Math.round(100 * st.correct / st.done) + "% đúng" : "") + "</div></div>";
  }
  function frameworkBox(fw, show) {
    return '<div class="framework' + (show ? " show" : "") + '" id="framework"><div class="fw-label">Giải thích</div>' + esc(fw) + "</div>";
  }
  function pager(base, num, i, len, arr) {
    var html = '<div class="pager">';
    html += i > 0 ? '<a class="btn btn-ghost" href="' + base + (i - 1) + '">← Câu trước</a>' : "<span></span>";
    if (i < len - 1) html += '<a class="btn btn-primary" href="' + base + (i + 1) + '">Câu tiếp →</a>';
    else {
      var idx = arr.findIndex(function (o) { return o.num === num; });
      if (idx < arr.length - 1) html += '<a class="btn btn-primary" href="#/p/' + arr[idx + 1].num + '/0">Module tiếp theo →</a>';
      else html += '<a class="btn btn-primary" href="#/">Hoàn thành — về trang chủ 🎉</a>';
    }
    return html + "</div>";
  }

  document.getElementById("reset-btn").onclick = function () {
    if (confirm("Xóa TOÀN BỘ tiến độ đã lưu trên trình duyệt này?")) { P_MCQ = {}; saveMcq(); route(); }
  };
  boot();
})();
