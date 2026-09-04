(function () {
  "use strict";

  const TABS = ["overview", "program", "theory", "lecturers", "quiz"];
  const LS_KEY = "vseo6_quiz_progress_v1";

  function renderProgram() {
    const root = document.getElementById("program-days");
    root.innerHTML = PROGRAM_DAYS.map((d) => {
      const rows = d.rows
        .map(
          (r) =>
            `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td></tr>`
        )
        .join("");
      return `<div class="day-card"><h3>${d.day}</h3><table class="day-table">${rows}</table></div>`;
    }).join("");
  }

  function renderTheory() {
    const root = document.getElementById("theory-list");
    root.innerHTML = THEORY_TOPICS.map(
      (t, i) => `
      <div class="accordion-item" data-idx="${i}">
        <button class="accordion-head" type="button">
          <span><span class="tag">${t.tag}</span>${t.title}</span>
          <span class="chevron">▸</span>
        </button>
        <div class="accordion-body">${t.body}</div>
      </div>`
    ).join("");
    root.querySelectorAll(".accordion-head").forEach((btn) => {
      btn.addEventListener("click", () => {
        btn.closest(".accordion-item").classList.toggle("open");
      });
    });
  }

  function renderLecturers() {
    const root = document.getElementById("lecturer-list");
    root.innerHTML = LECTURERS.map((l) => {
      const pubs = l.pubs
        .map((p) => `<li>${p.u ? `<a href="${p.u}" target="_blank" rel="noopener">${p.t}</a>` : p.t}</li>`)
        .join("");
      const more = l.pubLink
        ? `<p><a href="${l.pubLink}" target="_blank" rel="noopener">Hồ sơ đầy đủ →</a></p>`
        : "";
      return `
      <div class="lect-card">
        <h3>${l.name}</h3>
        <div class="lect-org">${l.org}</div>
        <p>${l.bio}</p>
        <ul class="lect-pubs">${pubs}</ul>
        ${more}
      </div>`;
    }).join("");
  }

  // ---------- Quiz ----------
  let quizState = null; // { questions, current, answers: {id: letter}, submitted: {id: bool} }

  function loadProgress() {
    try {
      const raw = localStorage.getItem(LS_KEY);
      return raw ? JSON.parse(raw) : {};
    } catch (e) {
      return {};
    }
  }

  function saveProgress(state) {
    try {
      localStorage.setItem(
        LS_KEY,
        JSON.stringify({ answers: state.answers, submitted: state.submitted })
      );
    } catch (e) {
      /* ignore quota errors */
    }
  }

  async function initQuiz() {
    const root = document.getElementById("quiz-root");
    root.innerHTML = `<p class="lead">Đang tải câu hỏi…</p>`;
    let questions;
    try {
      const res = await fetch("data/questions.json", { cache: "no-store" });
      if (!res.ok) throw new Error("HTTP " + res.status);
      questions = await res.json();
    } catch (e) {
      root.innerHTML = `<p class="lead">Không tải được câu hỏi (${e.message}). <button class="btn secondary" id="retry-quiz">Thử lại</button></p>`;
      document.getElementById("retry-quiz").addEventListener("click", initQuiz);
      return;
    }
    const saved = loadProgress();
    quizState = {
      questions,
      answers: saved.answers || {},
      submitted: saved.submitted || {},
    };
    renderQuiz();
  }

  function score() {
    let correct = 0;
    let answered = 0;
    quizState.questions.forEach((q) => {
      if (quizState.submitted[q.id]) {
        answered++;
        if (quizState.answers[q.id] === q.correct) correct++;
      }
    });
    return { correct, answered, total: quizState.questions.length };
  }

  function renderQuiz() {
    const root = document.getElementById("quiz-root");
    const s = score();
    const pct = quizState.questions.length
      ? Math.round((s.answered / quizState.questions.length) * 100)
      : 0;

    const header = `
      <div class="quiz-progress">
        <span>Đã trả lời: ${s.answered}/${s.total}</span>
        <span>Đúng: ${s.correct}/${s.answered || 0}</span>
      </div>
      <div class="quiz-bar"><div class="quiz-bar-fill" style="width:${pct}%"></div></div>
      <div class="quiz-actions">
        <button class="btn secondary" id="reset-quiz">Làm lại từ đầu</button>
      </div>
    `;

    const cards = quizState.questions
      .map((q) => {
        const submitted = !!quizState.submitted[q.id];
        const chosen = quizState.answers[q.id];
        const opts = q.options
          .map((o) => {
            let cls = "q-opt";
            if (submitted) {
              if (o.letter === q.correct) cls += " correct";
              else if (o.letter === chosen) cls += " wrong";
            }
            const checked = chosen === o.letter ? "checked" : "";
            return `<label class="${cls}">
              <input type="radio" name="q-${q.id}" value="${o.letter}" ${checked} ${submitted ? "disabled" : ""}>
              <span><strong>${o.letter}.</strong> ${o.text}</span>
            </label>`;
          })
          .join("");
        const verdictHtml = submitted
          ? `<div class="q-verdict ${chosen === q.correct ? "correct" : "wrong"}">${
              chosen === q.correct ? "✓ Chính xác" : `✗ Chưa đúng — đáp án đúng: ${q.correct}`
            }</div>
             <div class="q-explain show">${q.explain}</div>`
          : `<div class="quiz-actions">
               <button class="btn submit-btn" data-qid="${q.id}" ${chosen ? "" : "disabled"}>Kiểm tra</button>
             </div>`;
        return `
        <div class="q-card" data-qid="${q.id}">
          <div class="q-topic">${q.topic}</div>
          <div class="q-text">${q.question}</div>
          <div class="q-options">${opts}</div>
          ${verdictHtml}
        </div>`;
      })
      .join("");

    const summary =
      s.answered === s.total
        ? `<div class="result-summary">
             <div class="score">${s.correct}/${s.total}</div>
             <div>Bạn đã hoàn thành toàn bộ quiz (${Math.round((s.correct / s.total) * 100)}%).</div>
           </div>`
        : "";

    root.innerHTML = header + cards + summary;

    root.querySelectorAll('input[type="radio"]').forEach((inp) => {
      inp.addEventListener("change", (e) => {
        const qid = e.target.closest(".q-card").dataset.qid;
        quizState.answers[qid] = e.target.value;
        saveProgress(quizState);
        const btn = root.querySelector(`.submit-btn[data-qid="${qid}"]`);
        if (btn) btn.disabled = false;
      });
    });
    root.querySelectorAll(".submit-btn").forEach((btn) => {
      btn.addEventListener("click", () => {
        const qid = btn.dataset.qid;
        if (!quizState.answers[qid]) return;
        quizState.submitted[qid] = true;
        saveProgress(quizState);
        renderQuiz();
      });
    });
    const resetBtn = document.getElementById("reset-quiz");
    if (resetBtn) {
      resetBtn.addEventListener("click", () => {
        quizState.answers = {};
        quizState.submitted = {};
        saveProgress(quizState);
        renderQuiz();
      });
    }
  }

  // ---------- Routing ----------
  function showTab(tab) {
    if (!TABS.includes(tab)) tab = "overview";
    TABS.forEach((t) => {
      document.getElementById(`view-${t}`).classList.toggle("hidden", t !== tab);
    });
    document.querySelectorAll("#tabs a").forEach((a) => {
      a.classList.toggle("active", a.dataset.tab === tab);
    });
    if (tab === "quiz" && !quizState) initQuiz();
  }

  function route() {
    const hash = (location.hash || "#overview").replace("#", "");
    showTab(hash);
  }

  window.addEventListener("hashchange", route);

  document.addEventListener("DOMContentLoaded", () => {
    renderProgram();
    renderTheory();
    renderLecturers();
    route();
  });
})();
