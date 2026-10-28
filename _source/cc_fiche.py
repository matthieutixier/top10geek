# -*- coding: utf-8 -*-
"""Lit une fiche CommentChoisir : tests (média, note /10, date, url d'origine), points forts et réserves cités.
Usage : python3 cc_fiche.py sortie.json url1 url2 ...   Lecture seule."""
import urllib.request, re, json, sys, html, time
from collections import Counter
UA = {'User-Agent': 'Mozilla/5.0'}
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read().decode('latin-1')
def clean(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
def fiche(u):
    """Les notes de CommentChoisir sont affichées AVANT le test qu'elles concernent : le bloc de note porte le nom du média,
    suivi du bloc « testé le … [lire le test complet sur MÉDIA] ». On apparie donc chaque note au test suivant du même média
    (correctif du 28/10/2026 : l'ancienne version attribuait la note au test précédent)."""
    h = get(u)
    tests = []
    pending = None
    ev = re.compile(r'class="score">(\d+(?:[.,]\d+)?)</strong>(?:(?!divtest mt-0).)*?<small[^>]*>(\d+)</small>(?:(?!divtest mt-0).)*?<strong class="text-black">([^<]*)</strong>'
                    r'|<div class="divtest mt-0">(.*?)</div>', re.S)
    norm = lambda x: re.sub(r'[^a-z0-9]', '', html.unescape(x).lower())
    for m in ev.finditer(h):
        if m.group(1):
            pending = (float(m.group(1).replace(',', '.')), float(m.group(2)), html.unescape(m.group(3)).strip())
            continue
        for part in m.group(4).split('<br>'):
            lien = re.search(r'<a href="(https?://[^"]+)"[^>]*>\[lire le test complet sur ([^\]]+)\]', part)
            if not lien: continue
            media = html.unescape(lien.group(2)).strip()
            note = re.search(r'\[(\d+(?:[.,]\d+)?)\s*/\s*(\d+)\]', part)
            n10 = None; origine = ''
            if pending and norm(pending[2]) == norm(media):
                n10 = round(10 * pending[0] / pending[1], 1)   # la note du bloc média prime
                pending = None; origine = 'bloc'
            elif note:
                n10 = round(10 * float(note.group(1).replace(',', '.')) / float(note.group(2)), 1); origine = 'inline'
            date = re.search(r'test.? le (\d\d/\d\d/\d{4})', part)
            tests.append(dict(media=media, note10=n10, origine=origine, date=date.group(1) if date else '', url=lien.group(1)))
    seen = set(); uniq = []
    for t in tests:
        if t['url'] in seen: continue
        seen.add(t['url']); uniq.append(t)
    tests = uniq
    pros = Counter(); cons = Counter()
    for a in re.findall(r"alert-success[^>]*>(.*?)</div>", h, re.S):
        for l in re.split(r'<br\s*/?>', a):
            l = clean(l)
            if 3 < len(l) < 140: pros[l] += 1
    for a in re.findall(r"alert-danger[^>]*>(.*?)</div>", h, re.S):
        for l in re.split(r'<br\s*/?>', a):
            l = clean(l)
            if 3 < len(l) < 140: cons[l] += 1
    return dict(source=u, tests=tests, pros=[p for p, _ in pros.most_common(12)], cons=[c for c, _ in cons.most_common(12)])
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
