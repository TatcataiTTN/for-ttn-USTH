#!/usr/bin/env python3
"""Parse the VSEO6 question bank (Markdown) into questions.json.

Discipline (build-practical-website): the correct answer is NEVER hand-typed
into the output. It is extracted programmatically from each question's
`**Answer: X.**` marker in the source .md; if a question is missing its
answer/options the script aborts. Option order is then shuffled
deterministically (seeded by question id) to avoid position bias.
"""
import json
import random
import re
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source_questions.md")
OUT = os.path.join(HERE, "..", "data", "questions.json")

lines = open(SRC, encoding="utf-8").read().split("\n")

persp_re = re.compile(r"^# Perspective\s+(\d+)\s+[—-]\s+(.+?)\s+\(Q")
q_re = re.compile(r"^### Q(\d+)\.\s+(.*)$")
opt_re = re.compile(r"^([A-D])\.\s+(.*)$")
ans_re = re.compile(r"\*\*Answer:\s*([A-D])\.?\*\*\s*\*\*Framework:\*\*\s*(.*)$")

questions = []
cur_persp_num = None
cur_persp_title = None

i = 0
n = len(lines)
while i < n:
    line = lines[i]
    mp = persp_re.match(line)
    if mp:
        cur_persp_num = int(mp.group(1))
        cur_persp_title = mp.group(2).strip()
        i += 1
        continue
    mq = q_re.match(line)
    if mq:
        qnum = int(mq.group(1))
        qtext = mq.group(2).strip()
        opts = {}
        answer = None
        framework = None
        j = i + 1
        while j < n:
            l = lines[j]
            if l.startswith("### ") or l.startswith("# "):
                break
            mo = opt_re.match(l)
            if mo and mo.group(1) not in opts:
                opts[mo.group(1)] = mo.group(2).strip()
                j += 1
                continue
            ma = ans_re.search(l)
            if ma:
                answer = ma.group(1)
                framework = ma.group(2).strip()
            j += 1
        if sorted(opts.keys()) != ["A", "B", "C", "D"]:
            sys.exit(f"ERROR Q{qnum}: options != A,B,C,D -> got {sorted(opts.keys())}")
        if answer is None:
            sys.exit(f"ERROR Q{qnum}: no **Answer:** marker found")
        if not framework:
            sys.exit(f"ERROR Q{qnum}: empty framework")
        if cur_persp_num is None:
            sys.exit(f"ERROR Q{qnum}: no perspective context")
        correct_text = opts[answer]
        texts = [opts["A"], opts["B"], opts["C"], opts["D"]]
        rng = random.Random(2026000 + qnum)
        rng.shuffle(texts)
        letters = ["A", "B", "C", "D"]
        new_opts = [{"key": letters[k], "text": t} for k, t in enumerate(texts)]
        new_answer = next(o["key"] for o in new_opts if o["text"] == correct_text)
        questions.append({
            "id": qnum,
            "perspective": cur_persp_num,
            "perspectiveTitle": cur_persp_title,
            "question": qtext,
            "options": new_opts,
            "answer": new_answer,
            "framework": framework,
        })
        i = j
        continue
    i += 1

ids = [q["id"] for q in questions]
if len(ids) != len(set(ids)):
    sys.exit("ERROR: duplicate question ids")
expected = list(range(1, len(questions) + 1))
if ids != expected:
    missing = set(expected) - set(ids)
    sys.exit(f"ERROR: id sequence broken; count={len(ids)} missing/extra around {sorted(missing)[:5]}")

persp_meta = []
seen = set()
for q in questions:
    if q["perspective"] not in seen:
        seen.add(q["perspective"])
        persp_meta.append({
            "num": q["perspective"],
            "title": q["perspectiveTitle"],
            "count": sum(1 for x in questions if x["perspective"] == q["perspective"]),
        })

# audit: correct-answer letter distribution (position bias check)
dist = {"A": 0, "B": 0, "C": 0, "D": 0}
for q in questions:
    dist[q["answer"]] += 1

payload = {
    "meta": {
        "title": "VSEO6 — Satellite Altimetry for Continental Water Monitoring",
        "total": len(questions),
        "perspectives": persp_meta,
        "source": "source_questions.md",
    },
    "questions": questions,
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(payload, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK: parsed {len(questions)} questions across {len(persp_meta)} modules -> {OUT}")
for p in persp_meta:
    print(f"  P{p['num']:>2}  n={p['count']:>3}  {p['title']}")
print(f"Answer-letter distribution (position-bias check): {dist}")
