/* Soft gate: reminds the learner to master the "Big 12" (Start here) before modules and mock exams. Never blocks; reads the quiz score stored by quiz.js. */
(function () {
  var cs = document.currentScript; if (!cs) return;
  var root = cs.src.replace(/_shared\/gate\.js.*$/, '');
  if (/\/lessons\/start-here\//.test(location.pathname)) return;
  var want = 'lessons/start-here/index.html:p0-qz', s = null;
  try { for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i); if (k.indexOf('quiz:') === 0 && k.slice(-want.length) === want) s = JSON.parse(localStorage.getItem(k)); } } catch (e) {}
  var main = document.querySelector('main'); if (!main) return;
  var d = document.createElement('div'); d.className = 'gate';
  var link = root + 'lessons/start-here/index.html';
  if (s && s.done >= s.n && s.score >= s.n - 2) { d.className += ' ok'; d.innerHTML = '✅ <b>Big 12 mastered</b> (' + s.score + '/' + s.n + '). Go as deep as you like. <a href="' + link + '">Review the Big 12</a>'; }
  else if (s && s.done > 0) d.innerHTML = '📌 <b>Big 12 check in progress:</b> ' + s.done + '/' + s.n + ' answered, score ' + s.score + '. Reach ' + (s.n - 2) + '/' + s.n + ' before going deep. <a href="' + link + '#quiz">Continue the check</a>';
  else d.innerHTML = '📌 <b>Do this first:</b> the Big 12 ideas (3 key points, 3 formulas, 3 concepts, 3 principles) carry most of the exam. <a href="' + link + '">Start here →</a>';
  main.insertBefore(d, main.firstChild);
})();
