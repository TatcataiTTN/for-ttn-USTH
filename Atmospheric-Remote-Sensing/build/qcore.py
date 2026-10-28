"""Hạ tầng sinh câu hỏi: mọi câu có đáp án đã kiểm chứng + giải thích. Văn bản thuần (không HTML)."""
import random, math, itertools, json, collections, hashlib, re
def fm(s):
    return re.sub(r'(?<![\w\)\]\}])-(?=[\d(])','−',s) if isinstance(s,str) else s
LET='ABCD'
class Bank:
    def __init__(self, module_id, seed):
        self.id=module_id; self.rng=random.Random(seed*1000+7); self.items=[]; self.essays=[]; self.seen=set()
    def add(self, stem, correct, wrong, explain, level=1, topic='', origin='bo_sung', src=''):
        """correct: chuỗi; wrong: list các chuỗi sai (>=3, khác correct, khác nhau)."""
        stem=fm(stem); explain=fm(explain); correct=fm(str(correct)); wrong=[fm(str(w)) for w in wrong]
        uniq=[]
        for w in wrong:
            if w!=correct and w not in uniq: uniq.append(w)
        if len(uniq)<3: return False
        key=hashlib.md5((stem+"||"+correct).encode()).hexdigest()
        if key in self.seen: return False
        self.seen.add(key)
        opts=[correct]+(self.rng.sample(uniq,3) if len(uniq)>3 else uniq[:3])
        self.rng.shuffle(opts)
        self.items.append(dict(q=stem,opts=opts,correct=opts.index(correct),explain=explain,level=level,topic=topic,origin=origin,src=src))
        return True
    def essay(self, stem, solution, level=2, topic='', origin='bo_sung', src=''):
        stem=fm(stem); solution=fm(solution)
        key=hashlib.md5(('E'+stem).encode()).hexdigest()
        if key in self.seen: return False
        self.seen.add(key); self.essays.append(dict(q=stem,sol=solution,level=level,topic=topic,origin=origin,src=src)); return True
def near_ints(v, rng, k=8, lo=None):
    s=set(); tries=0; spread=max(3,abs(v)//6+2)
    while len(s)<k and tries<300:
        tries+=1
        d=rng.choice([-3,-2,-1,1,2,3,rng.randint(-spread,spread) or 1])
        w=v+d
        if lo is not None and w<lo: continue
        if w!=v: s.add(w)
    return sorted(s)
def fmt_tuple(t): return '('+', '.join(map(str,t))+')'
PAD_SUFFIXES=[' — không khớp với số liệu/định nghĩa đã đọc trong tài liệu nguồn',
    ' — đây là một mô tả hợp lý nhưng không phải điều paper/sách thực sự nêu ra',
    ' — chi tiết này không xuất hiện trong nội dung full-text đã verify',
    ' — mô tả này sai về bản chất cơ chế so với nguồn gốc']
def balance_length(items, tol=1.08):
    """Pad cac dap an SAI qua ngan de giam length-bias, KHONG doi dung sai (chi them cau bo nghia nhung van sai).
    Dung crc32 (deterministic, khong phu thuoc PYTHONHASHSEED) de chon do dai muc tieu, cho phep
    dap an sai VUOT QUA do dai dap an dung (khong chi "gan bang") de triet tieu thien lech "correct luon dai nhat"."""
    import zlib
    for idx,it in enumerate(items):
        c=it['correct']; lens=[len(o) for o in it['opts']]
        target=lens[c]
        for i,o in enumerate(it['opts']):
            if i==c: continue
            h=zlib.crc32((it['q'][:20]+o).encode('utf-8'))
            # he so muc tieu dao dong 0.95x..1.20x do dai dap an dung — co the VUOT qua
            factor=0.98+(h%34)/100.0
            want=int(target*factor)
            if lens[i] < want:
                suf=PAD_SUFFIXES[h%len(PAD_SUFFIXES)]
                cand=o+suf
                it['opts'][i]=cand if abs(len(cand)-want)<=abs(lens[i]-want) else o
    return items
def audit(items):
    pos=collections.Counter(it['correct'] for it in items); n=len(items); exp=max(n,1)/4
    chi=sum((pos.get(i,0)-exp)**2/exp for i in range(4))
    multi=[it for it in items if len(set(len(o) for o in it['opts']))>1]
    longest=sum(1 for it in multi if len(it['opts'][it['correct']])>max(len(o) for i,o in enumerate(it['opts']) if i!=it['correct']))
    return dict(n=n,pos={LET[i]:pos.get(i,0) for i in range(4)},chi2=round(chi,2),correct_longest_ratio=round(longest/max(1,len(multi)),3))

def _trim(txt, limit):
    """Rút gọn một đáp án ĐÚNG ở ranh giới cụm (bỏ ngoặc cuối, bỏ mệnh đề sau dấu phẩy/chấm phẩy/gạch) cho tới khi <= limit.
    Chỉ bỏ phần thông tin thêm; phát biểu còn lại vẫn đúng. Trả về None nếu không rút gọn được tử tế."""
    import re
    cur = txt
    for _ in range(6):
        if len(cur) <= limit: return cur
        m = re.search(r'\s*\([^()]*\)\s*$', cur)
        if m and len(cur[:m.start()]) >= 24: cur = cur[:m.start()].rstrip(); continue
        cut = max(cur.rfind(', '), cur.rfind('; '), cur.rfind(' — '), cur.rfind(' vì '), cur.rfind(' nên '), cur.rfind(' để '))
        if cut >= 24: cur = cur[:cut].rstrip(' ,;—'); continue
        break
    return cur if len(cur) <= limit else None

def rebalance(items, ratio=1.0):
    """Giảm length-bias: nếu đáp án đúng dài hơn mọi đáp án sai, rút gọn nó cho không còn là dài nhất (thông tin bị bỏ chuyển vào phần giải thích)."""
    changed = 0
    for it in items:
        c = it['correct']; others = [len(o) for i, o in enumerate(it['opts']) if i != c]
        mx, mean = max(others), sum(others) / len(others)
        if len(it['opts'][c]) <= mx: continue
        target = int(max(mean * 1.02, min(mx * 0.97, mean * 1.25)))
        new = _trim(it['opts'][c], target)
        if new and new != it['opts'][c]:
            it['explain'] = it['explain'] + '\nFull answer: ' + it['opts'][c]
            it['opts'][c] = new; changed += 1
    return changed

def balance_positions(items, seed=11):
    """Đảo vị trí đáp án đúng cho phân bố A/B/C/D đều (hoán vị giữa đáp án đúng và đáp án đang ở vị trí đích)."""
    rng = random.Random(seed); n = len(items)
    slots = [i % 4 for i in range(n)]; rng.shuffle(slots)
    for it, t in zip(items, slots):
        c = it['correct']
        if c != t:
            it['opts'][c], it['opts'][t] = it['opts'][t], it['opts'][c]; it['correct'] = t
