# -*- coding: utf-8 -*-
"""Outil à usage unique (11/11/2026) : reconstitue les corrections de notes audio à partir d'un relevé compact,
les applique avec presse_crawl.py / ajout_tests.py, retire les tests hors sujet, puis découpe en 3 lots de data.json."""
import copy, json, re, subprocess, sys, hashlib
from pathlib import Path
R = Path(".")
S = R / "_source"
AT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_publication/tmp_lots")
d0 = json.loads((S / "data.json").read_text(encoding="utf-8"))
ETAT = {"o": "ok", "E": "ÉCART", "N": "NOTE TROUVÉE"}
lignes = []
for tok in (AT / "c.txt").read_text().strip().split(";"):
    pid, rest = tok.split(":", 1)
    for idx, k, sc, dt in re.findall(r"(\d+)([oEN])([\d.]*)/(\d*)", rest):
        n = d0["items"][pid]["press"]["notes"][int(idx)]
        sc = float(sc) if sc else None
        lignes.append({"id": pid, "media": n["src"], "url": n["url"], "etat": ETAT[k], "note_page": sc,
                       "methode": "JSON-LD reviewRating" if sc is not None else None,
                       "date_page": ("20%s-%s-%s" % (dt[:2], dt[2:4], dt[4:6])) if dt else None})
for e in json.loads((AT / "extras.json").read_text(encoding="utf-8")):
    lignes.append({"id": e[0], "media": e[1], "url": e[2], "etat": "NOTE TROUVÉE", "note_page": 10.0,
                   "methode": "JSON-LD reviewRating 5/5", "date_page": e[3]})
(S / "data").mkdir(exist_ok=True)
(S / "data" / "verif_filtre.json").write_text(json.dumps({"date": "2026-11-11", "famille": "audio", "lignes": lignes}, ensure_ascii=False), encoding="utf-8")
(S / "data" / "confirmations.json").write_text((AT / "confirmations.json").read_text(encoding="utf-8"), encoding="utf-8")
def run(*a):
    r = subprocess.run(a, capture_output=True, text=True)
    print(r.stdout[-400:], r.stderr[-400:])
    if r.returncode: sys.exit("échec : " + " ".join(a))
run("python3", "_source/presse_crawl.py", "confirmer", "_source/data/confirmations.json", "--apply")
run("python3", "_source/presse_crawl.py", "appliquer", "_source/data/verif_filtre.json", "--apply")
(S / "data" / "nouveaux_tests.json").write_text(json.dumps([{"id": "razer-kraken-kitty-v3-pro", "src": "Gameblog", "score": 8.0,
    "url": "https://www.gameblog.fr/tech/hardware/tests/test-kraken-kitty-v3-pro-avis-709632", "date": "2026-01-17"}]), encoding="utf-8")
run("python3", "_source/ajout_tests.py", "_source/data/nouveaux_tests.json", "--apply")
# retrait des tests hors sujet (liste validée par Matthieu le 11/11/2026)
raw = (S / "data.json").read_text(encoding="utf-8")
d = json.loads(raw)
retirer = json.loads((AT / "retirer.json").read_text(encoding="utf-8"))
def recalc(pr):
    sc = [n for n in pr["notes"] if n["score"] is not None]
    pr.update(avg=(sum(n["score"] for n in sc) / len(sc)) if sc else None, n=len(sc), tests=len(pr["notes"]))
for pid, u in retirer:
    pr = d["items"][pid]["press"]
    k = len(pr["notes"]); pr["notes"] = [n for n in pr["notes"] if n["url"] != u]
    assert len(pr["notes"]) == k - 1, (pid, u)
    recalc(pr)
final = json.dumps(d, ensure_ascii=False, indent=1) + ("\n" if raw.endswith("\n") else "")
subprocess.run(["git", "checkout", "--", "_source/cc_fiches_audio.json"], check=True)   # cc_fiches (1 seule ligne de 230 Ko) : non republié
Path("/tmp/final.json").write_text(final, encoding="utf-8")
(S / "data.json").write_text(raw, encoding="utf-8")
subprocess.run(["git", "checkout", "--", "_source/data.json"], check=True)
subprocess.run(["git", "clean", "-fdq", "_source/data"], check=False)
print("final sha256", hashlib.sha256(final.encode()).hexdigest())
# découpage en 3 lots
B = json.loads((S / "data.json").read_text(encoding="utf-8")); F = json.loads(final)
cur = copy.deepcopy(B); nl = raw.endswith("\n")
for k, g in enumerate([["a-bt", "a-anc"], ["a-cas", "a-open"], ["a-gam"]], 1):
    for pid, it in F["items"].items():
        if it["cat"] in g: cur["items"][pid] = copy.deepcopy(it)
    (S / "data.json").write_text(json.dumps(cur, ensure_ascii=False, indent=1) + ("\n" if nl else ""), encoding="utf-8")
    p = subprocess.check_output(["git", "diff", "-U1", "--", "_source/data.json"]).decode()
    Path("/tmp/lot%d.patch" % k).write_text(p, encoding="utf-8")
    subprocess.check_call(["git", "-c", "user.name=x", "-c", "user.email=x@x", "commit", "-qam", "lot%d" % k])
    print("lot", k, len(p.encode()), hashlib.md5(p.encode()).hexdigest())
