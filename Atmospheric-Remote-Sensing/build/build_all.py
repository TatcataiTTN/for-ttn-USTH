# -*- coding: utf-8 -*-
import importlib, sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from qcore import rebalance, balance_positions
import site_pages as SP
import v2x
mods = [m[0] for m in MODULES]
stats, all_items, report = [], [], {}
for mid in mods:
    m = importlib.import_module(mid)
    mod, slides, B = m.build()
    mod, slides = v2x.apply(mid, mod, slides, B)
    rb = rebalance(B.items)
    balance_positions(B.items, seed=hash(mid) % 1000 if False else (0 if mid == 'pa' else int(mid[1:])) * 17 + 3)
    st = finish(mod, slides, B, 'Multiple-choice questions have explanations and a source; essay questions have worked solutions.')
    stats.append(dict(slides=len(slides), mcq=len(B.items), ess=len(B.essays)))
    for it in B.items: all_items.append(dict(it, mod=mid))
    report[mid] = dict(slides=len(slides), mcq=len(B.items), essays=len(B.essays), rebalanced=rb, audit=st,
                       goc=sum(1 for i in B.items if i['origin'] == 'goc'), bo_sung=sum(1 for i in B.items if i['origin'] != 'goc'))
    print(mid, 'slides', len(slides), 'mcq', len(B.items), 'essay', len(B.essays), 'goc', report[mid]['goc'], 'audit', st)
SP.gallery_page(); SP.calculators_page(); SP.exam_page(all_items); SP.reference_page(); SP.resources_page(); SP.index_page(stats)
json.dump(report, open(os.path.join(ROOT, 'data', 'build_report.json'), 'w'), ensure_ascii=False, indent=1)
print('TOTAL slides', sum(s['slides'] for s in stats), 'mcq', sum(s['mcq'] for s in stats), 'essays', sum(s['ess'] for s in stats))
