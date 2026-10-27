# -*- coding: utf-8 -*-
"""Lit une fiche CommentChoisir : tests (média, note /10, date, url d'origine), points forts et réserves cités.
Usage : python3 cc_fiche.py sortie.json url1 url2 ...   Lecture seule."""
import urllib.request, re, json, sys, html, time
from collections import Counter
UA = {'User-Agent': 'Mozilla/5.0'}
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read().decode('latin-1')
def clean(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
def fiche(u):
    h = get(u)
    tests = []
    blocs = re.split(r'(?=<div class="divtest mt-0">)', h)[1:]
    for b in blocs:
        dv = re.match(r'<div class="divtest mt-0">(.*?)</div>', b, re.S)
        if not dv: continue
        sc = re.search(r'class="score">(\d+(?:[.,]\d+)?)</strong>.*?<small[^>]*>(\d+)</small>', b[dv.end():dv.end() + 900], re.S)
        first = True
        for part in dv.group(1).split('<br>'):
            lien = re.search(r'<a href="(https?://[^"]+)"[^>]*>\[lire le test complet sur ([^\]]+)\]', part)
            if not lien: continue
            note = re.search(r'\[(\d+(?:[.,]\d+)?)\s*/\s*(\d+)\]', part)
            if not note and sc and first: note = sc
            first = False
            date = re.search(r'test.? le (\d\d/\d\d/\d{4})', part)
            n10 = round(10 * float(note.group(1).replace(',', '.')) / float(note.group(2)), 1) if note else None
            tests.append(dict(media=html.unescape(lien.group(2)).strip(), note10=n10, date=date.group(1) if date else '', url=lien.group(1)))
    pros = Counter(); cons = Counter()
    for a in re.findall(r"alert-success[^>]*>(.*?)</div>", h, re.S):
        for l in re.split(r'<br\s*/?>', a):
            l = clean(l)
            if 3 < len(l) < 140: pros[l] += 1
    for a in re.findall(r"alert-danger[^>]*>(.*?)</div>", h, re.S):
        for l in re.split(r'<br\s*/?>', a):
            l = clean(l)
            if 3 < len(l) < 140: cons[l] += 1
    seen = set(); uniq = []
    for t in tests:
        if t['url'] in seen: continue
        seen.add(t['url']); uniq.append(t)
    return dict(source=u, tests=uniq, pros=[p for p, _ in pros.most_common(12)], cons=[c for c, _ in cons.most_common(12)])
if __name__ == '__main__':
    out = {}
    for u in sys.argv[2:]:
        try: out[u] = fiche(u)
        except Exception as e: out[u] = dict(erreur=str(e))
        time.sleep(0.4)
    json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
    for u, f in out.items():
        t = f.get('tests', [])
        print(u.split('test-')[-1], len(t), 'tests,', sum(1 for x in t if x['note10'] is not None), 'notés')
