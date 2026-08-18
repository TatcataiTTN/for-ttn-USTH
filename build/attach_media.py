#!/usr/bin/env python3
"""Attach a `media` list to each Perspective-11 (figure/video reading) question in
questions.json, by parsing the referenced filenames out of the question text and
matching them to files actually present in Thesis-M1/assets/. Verified: a referenced
file that does not exist on disk is reported, never silently linked."""
import json, os, re, sys

SITE = "/Users/tuannghiat/for-ttn-USTH/Thesis-M1"
QJSON = SITE + "/data/questions.json"
FIG = SITE + "/assets/figures"
VID = SITE + "/assets/video"

fig_files = set(os.listdir(FIG))
vid_files = set(os.listdir(VID))

# tokens like fig06_channel_performance.png, figA3_psift_qber_vs_mK.png,
# diagram_10_scheduling_pipeline.png, starlink_..._...png, prototype_*.mp4
TOKEN = re.compile(r'([A-Za-z0-9_]*(?:fig|diagram|starlink|prototype)[A-Za-z0-9_]*(?:\.\.\.)?)\.(png|mp4)')

def resolve(stem, ext):
    """Return the asset path (relative to site root) for a referenced stem+ext, or None."""
    name = stem + "." + ext
    if ext == "png":
        if name in fig_files:
            return "assets/figures/" + name
        # shortened EDA names use '...' before the extension: match by prefix
        if stem.endswith("..."):
            pref = stem[:-3]
            for f in sorted(fig_files):
                if f.startswith(pref) and f.endswith(".png"):
                    return "assets/figures/" + f
        # also try stripping a trailing '...' anywhere
        pref = stem.replace("...", "")
        for f in sorted(fig_files):
            if f.startswith(pref) and f.endswith(".png"):
                return "assets/figures/" + f
    if ext == "mp4":
        if name in vid_files:
            return "assets/video/" + name
    return None

d = json.load(open(QJSON, encoding="utf-8"))
attached = 0
missing = []
qs_with_media = 0
for q in d["questions"]:
    if q.get("perspective") != 11:
        q.pop("media", None)
        continue
    text = q["question"] + " " + " ".join(o["text"] for o in q["options"]) + " " + q.get("framework", "")
    seen = []
    for m in TOKEN.finditer(text):
        stem, ext = m.group(1), m.group(2)
        path = resolve(stem, ext)
        if path and path not in seen:
            seen.append(path)
        elif not path:
            missing.append((q["id"], stem + "." + ext))
    if seen:
        q["media"] = seen
        attached += len(seen)
        qs_with_media += 1
    else:
        q.pop("media", None)

json.dump(d, open(QJSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"attached {attached} media links to {qs_with_media} P11 questions")
if missing:
    print("UNRESOLVED references (no asset found):")
    for qid, name in sorted(set(missing)):
        print(f"  Q{qid}: {name}")
else:
    print("all referenced media resolved to an existing asset ✓")
