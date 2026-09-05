#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lớp 1 kiểm thử (theo skill bilingual-lecture-narration, Giai đoạn 5):
- Mọi file mp3 trong narration_timing.vseo6.json tồn tại thật, kích thước > 0.
- Số slide trong timing khớp đúng 121 slide của deck (index.html).
- Tỉ lệ ký tự/giây hợp lý (giống sanity-check trong synthesize_narration.py,
  chạy lại độc lập ở đây để không phụ thuộc log của lần chạy TTS).
Chạy: python3 slides/narration/build/verify_narration.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # .../slides
NARR = ROOT / "narration"
TIMING = NARR / "data" / "narration_timing.vseo6.json"
DECK = ROOT / "index.html"

errors = []
warnings = []

if not TIMING.exists():
    print(f"FATAL: {TIMING} chưa tồn tại — chạy synthesize_narration.py trước.")
    sys.exit(1)

timing = json.loads(TIMING.read_text(encoding="utf-8"))

# 1. đếm số slide thật trong deck
deck_html = DECK.read_text(encoding="utf-8")
slide_count = len(re.findall(r"^slide\(", deck_html, re.M))
print(f"Deck thật có {slide_count} slide.")
print(f"Timing có {len(timing)} entry.")
if len(timing) != slide_count:
    errors.append(f"Số slide trong timing ({len(timing)}) khác số slide thật trong deck ({slide_count})")

# 2. mọi idx 0..slide_count-1 phải có mặt và có ít nhất 1 chunk
timing_by_idx = {t["idx"]: t for t in timing}
missing_idx = [i for i in range(slide_count) if i not in timing_by_idx]
if missing_idx:
    errors.append(f"Thiếu narration cho các slide idx: {missing_idx}")

empty_chunks = [t["idx"] for t in timing if not t["chunks"]]
if empty_chunks:
    errors.append(f"Slide idx không có chunk nào: {empty_chunks}")

# 3. mọi file mp3 tồn tại, kích thước > 0, duration > 0, tỉ lệ ký tự/giây hợp lý
total_ms = 0
total_files = 0
for t in timing:
    for c in t["chunks"]:
        f = NARR / c["file"]
        total_files += 1
        if not f.exists():
            errors.append(f"File không tồn tại: {c['file']} (slide {t['idx']} chunk {c['chunkId']})")
            continue
        size = f.stat().st_size
        if size == 0:
            errors.append(f"File rỗng (0 byte): {c['file']}")
            continue
        dur = c.get("durationMs", 0)
        if not dur or dur <= 0:
            errors.append(f"durationMs không hợp lệ: {c['file']} = {dur}")
            continue
        total_ms += dur
        chars = c.get("charCount", 0)
        ratio = chars / dur * 1000 if dur else 0
        if ratio > 30 or ratio < 4:
            warnings.append(f"slide {t['idx']} chunk {c['chunkId']}: tỉ lệ {ratio:.1f} chars/s bất thường "
                             f"(chars={chars}, dur={dur}ms) — nghe thử kiểm tra tay: {c['file']}")

print(f"\nTổng {total_files} file audio, tổng thời lượng {total_ms/1000/60:.1f} phút.")

if warnings:
    print(f"\n{len(warnings)} CẢNH BÁO (không chặn, nhưng nên nghe thử kiểm tra):")
    for w in warnings:
        print(f"  - {w}")

if errors:
    print(f"\n{len(errors)} LỖI:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print("\nTất cả kiểm tra Lớp 1 đều PASS.")
