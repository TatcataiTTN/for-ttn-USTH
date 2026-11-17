# -*- coding: utf-8 -*-
"""Polite crawler for the Ocean Optics Web Book (CC BY 2.0). <=1 req/s, generic UA, saves raw HTML."""
import urllib.request, re, sys, time, os, json
UA = 'study-notes-bot'
RAW = os.path.join(os.path.dirname(__file__), '..', 'textbook', 'raw')
def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r: return r.read().decode('utf-8', 'replace')
def slug(url): return re.sub(r'[^A-Za-z0-9]+', '_', url.split('oceanopticsbook.info/')[-1]).strip('_') or 'home'
if __name__ == '__main__':
    urls = [l.strip() for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
    os.makedirs(RAW, exist_ok=True)
    for u in urls:
        f = os.path.join(RAW, slug(u) + '.html')
        if os.path.exists(f): continue
        try: open(f, 'w', encoding='utf-8').write(get(u)); print('ok', u)
        except Exception as e: print('ERR', u, e)
        time.sleep(1.1)
