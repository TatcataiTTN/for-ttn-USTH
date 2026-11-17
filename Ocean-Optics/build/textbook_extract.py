# -*- coding: utf-8 -*-
"""Extract readable text (+ linearised MathML) and image list from saved Ocean Optics Web Book pages."""
import os, re, glob, json, sys
from bs4 import BeautifulSoup, NavigableString
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'textbook')
def m2t(n):
    if isinstance(n, NavigableString): return str(n).strip()
    t = n.name
    ch = [c for c in n.children if not (isinstance(c, NavigableString) and not str(c).strip())]
    if t in ('mi', 'mn', 'mo', 'mtext'): return n.get_text().strip()
    if t == 'msub': return m2t(ch[0]) + '_' + '{' + m2t(ch[1]) + '}'
    if t == 'msup': return m2t(ch[0]) + '^' + '{' + m2t(ch[1]) + '}'
    if t == 'msubsup': return m2t(ch[0]) + '_{' + m2t(ch[1]) + '}^{' + m2t(ch[2]) + '}'
    if t == 'mfrac': return '(' + m2t(ch[0]) + ')/(' + m2t(ch[1]) + ')'
    if t == 'msqrt': return 'sqrt(' + ''.join(m2t(c) for c in ch) + ')'
    if t == 'munderover': return m2t(ch[0]) + '_{' + m2t(ch[1]) + '}^{' + m2t(ch[2]) + '}'
    if t in ('munder',): return m2t(ch[0]) + '_{' + m2t(ch[1]) + '}'
    if t in ('mover',): return m2t(ch[0]) + '^{' + m2t(ch[1]) + '}'
    return ' '.join(x for x in (m2t(c) for c in ch) if x)
def extract(path):
    s = BeautifulSoup(open(path, encoding='utf-8').read(), 'html.parser')
    title = s.find('h1'); title = title.get_text(strip=True) if title else os.path.basename(path)
    body = s.find(class_='iws-l2h-latex-html') or s
    imgs = []
    for img in body.find_all('img'):
        imgs.append(img.get('src'))
        img.replace_with(f' [IMG {img.get("src")}] ')
    for m in body.find_all('math'):
        m.replace_with(NavigableString(' ⟦' + m2t(m).replace('  ', ' ') + '⟧ '))
    txt = body.get_text(' ')
    txt = re.sub(r'[ \t]+', ' ', txt); txt = re.sub(r'\s*\n\s*', '\n', txt); txt = re.sub(r'\n{3,}', '\n\n', txt)
    return title, txt.strip(), imgs
if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, 'text'), exist_ok=True)
    idx = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'raw', '*.html'))):
        t, x, im = extract(f); sl = os.path.basename(f)[:-5]
        open(os.path.join(ROOT, 'text', sl + '.txt'), 'w', encoding='utf-8').write('# ' + t + '\n\n' + x)
        idx[sl] = dict(title=t, chars=len(x), images=im)
    json.dump(idx, open(os.path.join(ROOT, 'page_index.json'), 'w'), indent=1)
    for k, v in idx.items(): print(f'{v["chars"]:6d} {len(v["images"]):3d} {k}  | {v["title"]}')
