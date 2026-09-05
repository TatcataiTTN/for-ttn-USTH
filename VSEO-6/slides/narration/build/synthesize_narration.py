#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tổng hợp giọng đọc (edge-tts) cho toàn bộ narration_source.vseo6.json,
đo thời lượng thật bằng ffprobe, ghi ra narration_timing.vseo6.json.

Dừng ngay (exit 1) nếu bất kỳ chunk nào lỗi TTS hoặc ffprobe trả duration rỗng/0
— không được để sót chunk hỏng (theo đúng yêu cầu skill bilingual-lecture-narration).

Chạy: python3 slides/narration/build/synthesize_narration.py
"""
import asyncio
import json
import subprocess
import sys
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parents[1]  # .../slides/narration
SRC = ROOT / "data" / "narration_source.vseo6.json"
AUDIO_DIR = ROOT / "audio" / "vseo6"
TIMING_OUT = ROOT / "data" / "narration_timing.vseo6.json"

VOICE = "vi-VN-HoaiMyNeural"
MAX_RETRIES = 6


async def synth_one(text, rate, out_path):
    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            communicate = edge_tts.Communicate(text, VOICE, rate=rate)
            await communicate.save(str(out_path))
            return
        except Exception as e:
            last_err = e
            wait = min(2 * (attempt + 1), 10)
            print(f"  retry {attempt+1}/{MAX_RETRIES} for {out_path.name}: {e} (chờ {wait}s)", file=sys.stderr)
            await asyncio.sleep(wait)
    raise RuntimeError(f"TTS failed after {MAX_RETRIES} attempts for {out_path.name}: {last_err}")


def ffprobe_duration_ms(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    out = result.stdout.strip()
    if not out:
        return None
    try:
        return round(float(out) * 1000)
    except ValueError:
        return None


async def main():
    data = json.loads(SRC.read_text(encoding="utf-8"))
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    timing = []
    total = sum(len(s["chunks"]) for s in data)
    done = 0
    failed = []

    for slide in data:
        idx = slide["idx"]
        chunk_entries = []
        for ci, chunk in enumerate(slide["chunks"]):
            text = chunk["text"]
            rate = chunk.get("rate", "+0%")
            fname = f"slide_{idx:03d}_{ci}_vi.mp3"
            out_path = AUDIO_DIR / fname

            # resume: bỏ qua nếu file đã tồn tại và ffprobe đọc được duration hợp lệ
            if out_path.exists():
                existing_dur = ffprobe_duration_ms(out_path)
                if existing_dur and existing_dur > 0:
                    chunk_entries.append({
                        "chunkId": ci,
                        "file": f"audio/vseo6/{fname}",
                        "durationMs": existing_dur,
                        "rate": rate,
                        "charCount": len(text),
                    })
                    done += 1
                    print(f"[{done}/{total}] SKIP (already ok) slide {idx} chunk {ci}: {existing_dur}ms")
                    continue

            try:
                await synth_one(text, rate, out_path)
            except Exception as e:
                failed.append((idx, ci, str(e)))
                done += 1
                print(f"[{done}/{total}] FAILED slide {idx} chunk {ci}: {e}")
                continue

            dur = ffprobe_duration_ms(out_path)
            if not dur or dur <= 0:
                failed.append((idx, ci, "ffprobe returned empty/zero duration"))
                done += 1
                print(f"[{done}/{total}] FAILED (bad duration) slide {idx} chunk {ci}")
                continue

            # sanity: chars/ms ratio — phát hiện chunk bị cắt cụt hoặc đọc sai giọng
            char_count = len(text)
            ratio = char_count / dur * 1000  # chars per second
            if ratio > 30 or ratio < 4:
                print(f"  [WARN] slide {idx} chunk {ci}: unusual ratio {ratio:.1f} chars/s "
                      f"(chars={char_count}, dur={dur}ms) — check manually")

            chunk_entries.append({
                "chunkId": ci,
                "file": f"audio/vseo6/{fname}",
                "durationMs": dur,
                "rate": rate,
                "charCount": char_count,
            })
            done += 1
            print(f"[{done}/{total}] OK slide {idx} chunk {ci}: {dur}ms ({char_count} chars)")

        timing.append({"idx": idx, "chunks": chunk_entries})

    if failed:
        print(f"\n{len(failed)} chunk(s) FAILED:")
        for idx, ci, err in failed:
            print(f"  slide {idx} chunk {ci}: {err}")
        sys.exit(1)

    TIMING_OUT.write_text(json.dumps(timing, ensure_ascii=False, indent=2), encoding="utf-8")
    total_ms = sum(c["durationMs"] for s in timing for c in s["chunks"])
    print(f"\nAll {total} chunks synthesized OK. Total duration: {total_ms/1000/60:.1f} minutes.")
    print(f"Timing written to {TIMING_OUT}")


if __name__ == "__main__":
    asyncio.run(main())
