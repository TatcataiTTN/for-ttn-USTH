"""
Sinh data/questions.json từ questions_source.py.
Xáo đáp án bằng random.Random(SEED) cố định, remap correct index sau xáo.
Chạy: python3 build/generate_questions.py
"""
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from questions_source import QUESTIONS

SEED = 42
LETTERS = ["A", "B", "C", "D"]


def build(seed):
    rng = random.Random(seed)
    out = []
    for q in QUESTIONS:
        options = [q["correct"]] + list(q["distractors"])
        indices = list(range(len(options)))
        rng.shuffle(indices)
        shuffled = [options[i] for i in indices]
        correct_letter = LETTERS[shuffled.index(q["correct"])]
        out.append(
            {
                "id": q["id"],
                "topic": q["topic"],
                "question": q["question"],
                "options": [{"letter": LETTERS[i], "text": t} for i, t in enumerate(shuffled)],
                "correct": correct_letter,
                "explain": q["explain"],
            }
        )
    return out


def audit(questions):
    from collections import Counter

    counts = Counter(q["correct"] for q in questions)
    n = len(questions)
    expected = n / len(LETTERS)
    chi2 = sum((counts.get(l, 0) - expected) ** 2 / expected for l in LETTERS)
    print(f"Position distribution: {dict(counts)} (n={n}, expected/letter={expected:.1f}, chi2={chi2:.2f})")

    correct_lens = []
    distractor_lens = []
    for q in questions:
        for opt in q["options"]:
            if opt["letter"] == q["correct"]:
                correct_lens.append(len(opt["text"]))
            else:
                distractor_lens.append(len(opt["text"]))
    avg_c = sum(correct_lens) / len(correct_lens)
    avg_d = sum(distractor_lens) / len(distractor_lens)
    ratio = avg_c / avg_d
    print(f"Avg correct len={avg_c:.1f}, avg distractor len={avg_d:.1f}, ratio={ratio:.2f}")

    ids = [q["id"] for q in questions]
    if len(ids) != len(set(ids)):
        print("!! DUPLICATE IDS FOUND")
        sys.exit(1)

    if ratio > 1.5:
        print("!! WARNING: length bias ratio > 1.5 — review distractor lengths")
    if chi2 > 7.815:  # p<0.05, df=3
        print("!! WARNING: position bias chi2 exceeds threshold — try another SEED")
    print("Audit done.")


def main():
    best_seed = SEED
    best_chi2 = None
    # thử vài seed, chọn seed có phân bố A/B/C/D đều nhất
    for candidate in range(0, 50):
        qs = build(candidate)
        from collections import Counter

        counts = Counter(q["correct"] for q in qs)
        n = len(qs)
        expected = n / len(LETTERS)
        chi2 = sum((counts.get(l, 0) - expected) ** 2 / expected for l in LETTERS)
        if best_chi2 is None or chi2 < best_chi2:
            best_chi2 = chi2
            best_seed = candidate

    print(f"Best seed found: {best_seed} (chi2={best_chi2:.2f})")
    questions = build(best_seed)
    audit(questions)

    out_path = Path(__file__).parent.parent / "data" / "questions.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {out_path}")


if __name__ == "__main__":
    main()
