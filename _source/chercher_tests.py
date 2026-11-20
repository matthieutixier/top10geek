# -*- coding: utf-8 -*-
"""Pilote (20/11/2026) : recherche de NOUVEAUX tests presse avec Antigravity CLI (agy, successeur de Gemini CLI)
et sa recherche Google. À lancer sur l'ordinateur de Matthieu, après une première connexion interactive à agy.

  python _source/chercher_tests.py --rubrique portable --max 5        # essai sur 5 fiches
  python _source/chercher_tests.py --rubrique portable                # toutes les fiches à moins de 3 tests

Pour chaque fiche à moins de 3 tests, agy reçoit le modèle exact et la liste des tests déjà cités, et doit renvoyer
SEULEMENT des adresses de pages de test (aucun texte, aucune note). Les adresses sont écrites dans
_source/data/candidats_tests_<rubrique>.json. Rien d'autre n'est modifié.

Ensuite (session Claude) : python3 _source/presse_crawl.py lire <adresses> --id <produit>  -> la note n'est reprise
que si la page du média la déclare elle-même (JSON-LD), puis ajout_tests.py. Aucun texte produit par agy n'est conservé.
"""
import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

SRC = Path(__file__).resolve().parent
PREFIXES = {"s-": "robot", "t-": "tv", "a-": "audio", "v-": "video", "e-": "ecran", "i-": "imprimante", "d-": "bureau"}
FAMILLE = lambda cat: next((f for p, f in PREFIXES.items() if cat.startswith(p)), "portable")
EXCLUS = ("amazon.", "commentchoisir.", "idealo.", "ledenicheur.", "darty.", "fnac.com", "boulanger.", "cdiscount.",
          "electrodepot.", "ldlc.", "youtube.", "reddit.", "facebook.", "x.com", "twitter.", "google.")

CONSIGNE = """Tu cherches des tests (reviews) publiés par des médias ou des laboratoires pour UN modèle précis.
Modèle : {nom} — référence : {ref}
Tests déjà connus (à ne pas renvoyer) : {connus}

Règles :
- Utilise la recherche Google. Cherche en français, anglais, allemand, espagnol, italien.
- Seulement des pages de TEST complet de CE modèle exact (pas une autre taille, pas une autre génération, pas une actualité,
  pas un comparatif de plusieurs produits, pas une boutique, pas un forum, pas une vidéo).
- N'invente aucune adresse : renvoie seulement des adresses que la recherche a réellement trouvées.
- Réponds UNIQUEMENT par un tableau JSON d'adresses, sans aucun autre texte, par exemple :
["https://www.exemple.fr/test-modele", "https://www.example.com/model-review"]
- Si tu ne trouves rien de sûr, réponds [].
"""


def agy_exe():
    exe = shutil.which("agy") or shutil.which("agy.exe")
    if not exe:
        sys.exit("agy introuvable : installer Antigravity CLI puis rouvrir le terminal (voir la procédure).")
    return exe


def demander(exe, prompt, timeout):
    r = subprocess.run([exe, "-p", prompt, "--output-format", "json"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    sortie = r.stdout.strip()
    try:                                    # enveloppe JSON documentée : {"response": "...", ...}
        env = json.loads(sortie)
        texte = env.get("response") or env.get("result") or ""
    except (json.JSONDecodeError, AttributeError):
        texte = sortie
    return r.returncode, texte, r.stderr[-400:]


def adresses(texte, connues):
    vues, out = set(connues), []
    for u in re.findall(r"https?://[^\s\"'\]\)<>,]+", texte or ""):
        u = u.rstrip(".;")
        h = urlparse(u).netloc.lower()
        if not h or any(x in h for x in EXCLUS) or u in vues:
            continue
        vues.add(u)
        out.append(u)
    return out[:8]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rubrique", required=True, choices=sorted(set(PREFIXES.values()) | {"portable"}))
    ap.add_argument("--max", type=int, default=0, help="nombre maximal de fiches (essai)")
    ap.add_argument("--ids", help="fiches précises, séparées par des virgules")
    ap.add_argument("--timeout", type=int, default=240)
    a = ap.parse_args()
    exe = agy_exe()
    d = json.loads((SRC / "data.json").read_text(encoding="utf-8"))
    cible = [(k, p) for k, p in d["items"].items()
             if FAMILLE(p.get("cat", "")) == a.rubrique and (p.get("press") or {}).get("tests", 0) < 3]
    if a.ids:
        voulu = set(a.ids.split(","))
        cible = [(k, p) for k, p in d["items"].items() if k in voulu]
    if a.max:
        cible = cible[:a.max]
    sortie = SRC / "data" / f"candidats_tests_{a.rubrique}.json"
    sortie.parent.mkdir(exist_ok=True)
    res = json.loads(sortie.read_text(encoding="utf-8")) if sortie.exists() else {}
    print(f"{len(cible)} fiche(s) à chercher ; résultats : {sortie}")
    for n, (k, p) in enumerate(cible, 1):
        if k in res and res[k].get("statut") == "ok":
            print(f"[{n}/{len(cible)}] {k} : déjà fait"); continue
        connues = [x["url"] for x in p["press"]["notes"] if x.get("url")]
        prompt = CONSIGNE.format(nom=p.get("short", k), ref=p.get("ref", ""), connus=", ".join(connues) or "aucun")
        try:
            code, texte, err = demander(exe, prompt, a.timeout)
        except subprocess.TimeoutExpired:
            code, texte, err = -1, "", "délai dépassé"
        urls = adresses(texte, connues)
        statut = "ok" if code == 0 and texte else "echec"
        res[k] = dict(nom=p.get("short", k), ref=p.get("ref", ""), tests_avant=p["press"]["tests"], urls=urls,
                      statut=statut, erreur=(err if statut != "ok" else ""),
                      date=datetime.datetime.now().isoformat(timespec="seconds"))
        sortie.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[{n}/{len(cible)}] {k:28s} {statut:5s} {len(urls)} adresse(s)" + (f"  ({err.strip()[:120]})" if statut != "ok" else ""))
    ok = [v for v in res.values() if v["statut"] == "ok"]
    print(f"\nBilan : {len(ok)}/{len(res)} fiches traitées, {sum(len(v['urls']) for v in ok)} adresses candidates.")
    print("Envoie le fichier à Claude (ou dis-lui « lis les candidats ») : chaque note sera lue sur la page du média.")


if __name__ == "__main__":
    main()
