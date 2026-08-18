/* mathify(raw) -> safe pretty-math HTML for the ASCII notation used in this app.
   No external library: Unicode Greek + <sub>/<sup> only. Input is trusted authored
   text (not user input). Works in the browser (window.mathify) and in Node (module.exports). */
(function (root) {
  "use strict";

  var GREEK = {
    lambda: "λ", theta: "θ", sigma: "σ", mu: "μ", nu: "ν", zeta: "ζ",
    epsilon: "ε", rho: "ρ", alpha: "α", beta: "β", chi: "χ", psi: "ψ",
    eta: "η", pi: "π", gamma: "γ", omega: "ω", Delta: "Δ", delta: "δ",
    Omega: "Ω", phi: "φ", tau: "τ", kappa: "κ"
  };
  // longest names first so alternation prefers e.g. "theta" over "eta"
  var GREEK_KEYS = Object.keys(GREEK).sort(function (a, b) { return b.length - a.length; });
  var GREEK_RE = new RegExp("(?<![A-Za-z])(" + GREEK_KEYS.join("|") + ")(?![A-Za-z])", "g");

  function mathify(raw) {
    if (raw == null) return "";
    var s = String(raw);

    // 1) ampersand, then comparison/arrow operators, then remaining angle brackets
    s = s.replace(/&/g, "&amp;");
    s = s.replace(/<->/g, "↔").replace(/->/g, "→").replace(/<=/g, "≤").replace(/>=/g, "≥")
         .replace(/!=/g, "≠").replace(/~=/g, "≈").replace(/\+-/g, "±");
    s = s.replace(/</g, "&lt;").replace(/>/g, "&gt;");

    // 2) sqrt
    s = s.replace(/\bsqrt\s*\(/g, "√(").replace(/\bsqrt\b/g, "√");

    // 3) named compounds that are NOT simple x_y (do before greek + generic subscript)
    var COMP = [
      [/\bthetaC\b/g, "θ<sub>C</sub>"],
      [/\bCn2\b/g, "C<sub>n</sub><sup>2</sup>"], [/\bCn\^2\b/g, "C<sub>n</sub><sup>2</sup>"],
      [/\bchiE\b/g, "χ<sub>E</sub>"],
      [/\bH2\b/g, "H<sub>2</sub>"], [/\blog2\b/g, "log<sub>2</sub>"],
      [/\bw0\b/g, "w<sub>0</sub>"], [/\bwL\b/g, "w<sub>L</sub>"],
      [/\bd0\b/g, "d<sub>0</sub>"], [/\bd1\b/g, "d<sub>1</sub>"],
      [/\bf1\b/g, "f<sub>1</sub>"], [/\bf2\b/g, "f<sub>2</sub>"]
    ];
    COMP.forEach(function (r) { s = s.replace(r[0], r[1]); });

    // 4) superscripts: ^(...) then ^number(.dec)(/frac) then ^letter
    s = s.replace(/\^\(([^)]*)\)/g, function (_, g) { return "<sup>" + g + "</sup>"; });
    s = s.replace(/\^(-?\d+(?:\.\d+)?(?:\/\d+)?)/g, "<sup>$1</sup>");
    s = s.replace(/\^([A-Za-z])/g, "<sup>$1</sup>");

    // 5) Greek whole-words (underscore / digits count as boundaries via lookaround)
    s = s.replace(GREEK_RE, function (_, name) { return GREEK[name]; });

    // 6) generic subscripts x_y  (x may be latin or a greek glyph we just inserted)
    var SUBRE = /([A-Za-zλθσμνζεραβχψηπγωΔδΩφτκ])_\{?([A-Za-z0-9]+)\}?/g;
    // run twice to catch chained cases
    s = s.replace(SUBRE, "$1<sub>$2</sub>").replace(SUBRE, "$1<sub>$2</sub>");

    // 7) units and multiplication
    s = s.replace(/\burad\b/g, "μrad").replace(/\bum\b/g, "μm");
    s = s.replace(/\*/g, "·");
    s = s.replace(/(\s)~(\s)/g, "$1≈$2");

    return s;
  }

  mathify.strip = function (raw) { // plain-text version (no tags) for detection/search
    return mathify(raw).replace(/<\/?(sub|sup)>/g, "").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
  };

  if (typeof module !== "undefined" && module.exports) module.exports = mathify;
  else root.mathify = mathify;
})(typeof window !== "undefined" ? window : this);
