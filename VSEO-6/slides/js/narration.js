/*
 * Narration player cho VSEO6 slide deck.
 * Không sửa logic hiện có của deck (biến deck/idx/go/render trong index.html) —
 * chỉ đọc DOM đã có sẵn (#deck > .slide, theo đúng thứ tự SLIDES) và quan sát
 * thay đổi style.transform của #deck để phát hiện chuyển slide thủ công.
 *
 * Kiến trúc: 1 slide = 1..N chunk mp3 (đã tổng hợp sẵn bằng edge-tts, xem
 * slides/narration/build/synthesize_narration.py). Đồng bộ bằng audio.onended
 * (ổn định 100%, không phụ thuộc WordBoundary vốn đã verify không hoạt động).
 */
(function () {
  "use strict";

  var DECK_ID = "vseo6";
  var TIMING_URL = "narration/data/narration_timing." + DECK_ID + ".json";
  var LANG_KEY = "narration_autoadvance_" + DECK_ID;

  var timingByIdx = {};   // idx -> [{chunkId, file, durationMs, rate}, ...]
  var deck = document.getElementById("deck");
  if (!deck) return; // deck chưa sẵn sàng (không nên xảy ra, script load sau engine)

  var currentAudio = null;
  var playingIdx = -1;      // slide đang phát narration (-1 = không phát gì)
  var autoAdvanceEnabled = true;
  try {
    var saved = localStorage.getItem(LANG_KEY);
    if (saved !== null) autoAdvanceEnabled = saved === "1";
  } catch (e) { /* localStorage có thể bị chặn — im lặng dùng mặc định */ }

  // ---------- lấy idx hiện tại từ deck.style.transform (không đụng biến idx nội bộ của engine) ----------
  function getCurrentIdx() {
    var t = deck.style.transform || "";
    var m = t.match(/-([\d.]+)vw/);
    return m ? Math.round(parseFloat(m[1]) / 100) : 0;
  }

  // ---------- highlight công thức đang đọc (chunk có rate chậm = đang đọc công thức) ----------
  function clearFormulaHighlight() {
    var cur = deck.children[playingIdx >= 0 ? playingIdx : getCurrentIdx()];
    if (cur) {
      var els = cur.querySelectorAll(".eqn-box.narrating");
      for (var i = 0; i < els.length; i++) els[i].classList.remove("narrating");
    }
  }
  function highlightFormula(slideEl, formulaOrdinal) {
    clearFormulaHighlight();
    var boxes = slideEl.querySelectorAll(".eqn-box");
    if (boxes[formulaOrdinal]) boxes[formulaOrdinal].classList.add("narrating");
  }

  // ---------- nút trên từng slide ----------
  function setButtonState(idx, state) {
    // state: "idle" | "playing"
    var slideEl = deck.children[idx];
    if (!slideEl) return;
    var btn = slideEl.querySelector(".narr-btn");
    if (!btn) return;
    btn.classList.toggle("is-playing", state === "playing");
    btn.textContent = state === "playing" ? "⏸" : "🔊";
    btn.setAttribute("aria-label", state === "playing" ? "Tạm dừng giọng đọc" : "Nghe giọng đọc slide này");
  }

  function stopCurrent() {
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.onended = null;
      currentAudio.onerror = null;
      currentAudio = null;
    }
    if (playingIdx >= 0) {
      setButtonState(playingIdx, "idle");
      clearFormulaHighlight();
    }
    playingIdx = -1;
  }

  function playSlide(idx) {
    var chunks = timingByIdx[idx];
    if (!chunks || !chunks.length) return; // slide chưa có narration (không nên xảy ra khi đã tổng hợp đủ)
    stopCurrent();
    playingIdx = idx;
    setButtonState(idx, "playing");
    var slideEl = deck.children[idx];
    var formulaCount = 0;
    var ci = 0;

    function playNext() {
      if (ci >= chunks.length) {
        setButtonState(idx, "idle");
        clearFormulaHighlight();
        playingIdx = -1;
        if (autoAdvanceEnabled && idx < deck.children.length - 1) {
          // đồng bộ lastIdx TRƯỚC khi gọi go(1): MutationObserver chạy bất đồng bộ (microtask),
          // nên phải tự cập nhật lastIdx ngay để nó không hiểu nhầm đây là điều hướng thủ công
          // rồi lỡ tay dừng audio slide mới vừa bắt đầu phát.
          lastIdx = idx + 1;
          window.go(1);
          playSlide(idx + 1);
        }
        return;
      }
      var chunk = chunks[ci];
      ci += 1;
      if (chunk.rate && chunk.rate.indexOf("-") === 0) {
        highlightFormula(slideEl, formulaCount);
        formulaCount += 1;
      } else {
        clearFormulaHighlight();
      }
      var audio = new Audio(chunk.file);
      currentAudio = audio;
      audio.onended = function () {
        if (currentAudio === audio) playNext();
      };
      audio.onerror = function () {
        console.error("[narration] lỗi tải audio:", chunk.file);
        if (currentAudio === audio) playNext(); // bỏ qua chunk lỗi, không kẹt cả bài
      };
      audio.play().catch(function (err) {
        console.warn("[narration] trình duyệt chặn play (cần tương tác người dùng):", err);
        setButtonState(idx, "idle");
        playingIdx = -1;
      });
    }
    playNext();
  }

  function toggleSlide(idx) {
    if (playingIdx === idx) {
      stopCurrent();
    } else {
      playSlide(idx);
    }
  }

  // ---------- quan sát chuyển slide thủ công (phím mũi tên / click nav / Home / End) ----------
  var lastIdx = getCurrentIdx();
  var observer = new MutationObserver(function () {
    var newIdx = getCurrentIdx();
    if (newIdx !== lastIdx) {
      // lastIdx đã được narration.js tự cập nhật trước khi gọi go(1) trong chuỗi auto-advance
      // (xem playNext) — nên nếu tới đây newIdx vẫn khác lastIdx, chắc chắn là điều hướng
      // thủ công (phím mũi tên / click / Home / End), luôn dừng audio đang phát.
      lastIdx = newIdx;
      stopCurrent();
    }
  });
  observer.observe(deck, { attributes: true, attributeFilter: ["style"] });

  // ---------- inject nút vào từng slide + thanh điều khiển tự động chuyển slide ----------
  function injectButtons() {
    var slides = deck.children;
    for (var i = 0; i < slides.length; i++) {
      var slideEl = slides[i];
      if (slideEl.querySelector(".narr-btn")) continue;
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "narr-btn";
      btn.textContent = "🔊";
      btn.setAttribute("aria-label", "Nghe giọng đọc slide này");
      (function (idx) {
        btn.addEventListener("click", function (e) {
          e.stopPropagation();
          toggleSlide(idx);
        });
      })(i);
      slideEl.appendChild(btn);
    }
  }

  function buildAutoAdvanceControl() {
    var bar = document.createElement("div");
    bar.className = "narrbar";
    var toggle = document.createElement("button");
    toggle.type = "button";
    toggle.className = "narrbar-toggle";
    function render() {
      toggle.textContent = "🔁 Tự động chuyển slide: " + (autoAdvanceEnabled ? "BẬT" : "TẮT");
      toggle.classList.toggle("on", autoAdvanceEnabled);
    }
    toggle.addEventListener("click", function (e) {
      e.stopPropagation();
      autoAdvanceEnabled = !autoAdvanceEnabled;
      try { localStorage.setItem(LANG_KEY, autoAdvanceEnabled ? "1" : "0"); } catch (e2) { /* im lặng */ }
      render();
    });
    render();
    bar.appendChild(toggle);
    document.body.appendChild(bar);
  }

  // ---------- boot ----------
  fetch(TIMING_URL)
    .then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then(function (data) {
      data.forEach(function (slide) {
        timingByIdx[slide.idx] = slide.chunks;
      });
      injectButtons();
      buildAutoAdvanceControl();
    })
    .catch(function (err) {
      console.error("[narration] không tải được narration_timing:", err);
    });
})();
