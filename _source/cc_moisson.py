# -*- coding: utf-8 -*-
"""Moisson CommentChoisir : liste, pour une catégorie, les produits avec nb de tests, nb de notes, moyenne /5.
Usage : python3 cc_moisson.py <categorie-id> <sortie.json> marque1 marque2 ...   (ex. 71-aspirateurs-robot)
Lecture seule, pause entre les requêtes."""
import urllib.request, re, json, sys, time, html
UA = {'User-Agent': 'Mozilla/5.0'}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read().decode('latin-1')
cat, out, marques = sys.argv[1], sys.argv[2], sys.argv[3:]
liens = {}
for m in marques:
    try:
        h = get(f"https://www.commentchoisir.fr/marque-{m}.htm?categorie={cat}")
    except Exception as e:
        print(m, 'ERR', e); continue
    for l in re.findall(r"href=['\"](/test-[^'\"#]+\.htm)['\"]", h):
        liens[l] = m
    time.sleep(0.4)
import os
res = json.load(open(out)) if os.path.exists(out) else []
fait = {r["url"] for r in res}
t0 = time.time()
for l, m in liens.items():
    if "https://www.commentchoisir.fr" + l in fait: continue
    if time.time() - t0 > 140: print("budget atteint, relancer"); break
    try:
        h = get("https://www.commentchoisir.fr" + l)
    except Exception as e:
        continue
    t = re.search(r"<title>(.*?)</title>", h, re.S)
    t = html.unescape(t.group(1)).strip() if t else ''
    r = re.match(r"(.+?): (\d+) tests? et avis(?:, avec (\d+) notes?)?(?: — ([\d.]+)/5)?", t)
    if r:
        res.append(dict(url="https://www.commentchoisir.fr" + l, marque=m, nom=r.group(1), tests=int(r.group(2)),
                        notes=int(r.group(3) or 0), moy=float(r.group(4)) if r.group(4) else None))
    time.sleep(0.3)
res.sort(key=lambda x: (-x['notes'], -x['tests']))
json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1)
print(len(res), 'produits')
