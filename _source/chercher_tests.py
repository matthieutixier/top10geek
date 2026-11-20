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
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

SRC = Path(__file__).resolve().parent
PREFIXES = {"s-": "robot", "t-": "tv", "a-": "audio", "v-": "video", "e-": "ecran", "i-": "imprimante", "d-": "bureau"}
FAMILLE = lambda cat: next((f for p, f in PREFIXES.items() if cat.startswith(p)), "portable")
MAISON = ("robot", "tv", "audio", "video")
INFORMATIQUE = ("portable", "bureau", "ecran", "imprimante")
EXCLUS = ("amazon.", "commentchoisir.", "idealo.", "ledenicheur.", "darty.", "fnac.com", "boulanger.", "cdiscount.",
          "electrodepot.", "ldlc.", "youtube.", "youtu.be", "reddit.", "facebook.", "x.com", "twitter.", "google.")

CONSIGNE = """Tu cherches des tests (reviews) publiés par des médias ou des laboratoires pour UN modèle précis.
Modèle : {nom} — référence : {ref}
Tests déjà connus (à ne pas renvoyer) : {connus}

Règles :
- Utilise UNIQUEMENT l'outil de recherche web (search_web), 3 recherches au maximum. N'exécute aucune commande, n'ouvre
  aucune page, ne vérifie rien toi-même : la vérification sera faite après toi. Réponds dès la 3e recherche au plus tard.
- Utilise la recherche Google. Cherche en français, anglais, allemand, espagnol, italien.
- Seulement des pages de TEST complet de CE modèle exact (pas une autre taille, pas une autre génération, pas une actualité,
  pas un comparatif de plusieurs produits, pas une boutique, pas un forum, pas une vidéo).
- N'invente aucune adresse : renvoie seulement des adresses que la recherche a réellement trouvées.
- Réponds UNIQUEMENT par un tableau JSON des adresses des sources que l'outil t'a renvoyées et qui semblent être un test
  de ce modèle, recopiées telles quelles (y compris les liens vertexaisearch.cloud.google.com/grounding-api-redirect/…),
  10 au maximum, sans aucun autre texte. Le tri final sera fait après toi.
- Si l'outil ne t'a renvoyé aucune source utile, réponds [].
"""


def agy_exe():
    exe = shutil.which("agy") or shutil.which("agy.exe")
    if not exe:
        sys.exit("agy introuvable : installer Antigravity CLI puis rouvrir le terminal (voir la procédure).")
    return exe


def demander(exe, prompt, timeout, options):
    """Une question à agy (sortie stream-json : on voit les outils réellement utilisés) ; nouvel essai après 60 s
    si les serveurs gratuits sont saturés (503). Renvoie (code, réponse, erreur, outils utilisés)."""
    for essai in (1, 2):
        r = subprocess.run([exe, "-p", prompt, "--output-format", "stream-json", "--print-timeout", f"{timeout}s"] + options,
                           capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout + 60)
        tout = r.stdout + r.stderr
        if essai == 1 and ("503" in tout or "No capacity" in tout) and '"status":"SUCCESS"' not in tout:
            print("   serveurs saturés, nouvel essai dans 60 s…")
            time.sleep(60)
            continue
        break
    texte, outils, erreur = "", [], ""
    for ligne in r.stdout.splitlines():
        try:
            ev = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        su = ev.get("step_update") or {}
        if su.get("step_type") == "tool" and su.get("state") in ("DONE", "ERROR"):
            q = (su.get("tool_info") or {}).get("parameters", {})
            outils.append(f"{su.get('tool_name')}:{su.get('state')}:{q.get('query', '')[:80]}")
        if ev.get("event") == "result":
            texte = ev["result"].get("response") or ""
            erreur = ev["result"].get("error") or ""
    return r.returncode, texte, (erreur or r.stderr[-400:]), outils


def resoudre(u):
    """Lien de redirection de la recherche Google (grounding-api-redirect) -> adresse de la page source (en-tête Location,
    la page elle-même n'est pas chargée). Toute autre adresse est rendue telle quelle."""
    if "grounding-api-redirect" not in u:
        return u
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=15)
        return r.geturl()
    except urllib.error.HTTPError as e:
        return e.headers.get("Location") or ""
    except Exception:
        return ""


class _SansSuivre(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


urllib.request.install_opener(urllib.request.build_opener(_SansSuivre))


def adresses(texte, connues):
    vues, out = set(connues), []
    for u in re.findall(r"https?://[^\s\"'\]\)<>,]+", texte or ""):
        u = resoudre(u.rstrip(".;"))
        h = urlparse(u).netloc.lower()
        if not h or any(x in h for x in EXCLUS) or u in vues:
            continue
        vues.add(u)
        out.append(u)
    return out[:10]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rubrique", required=True,
                    choices=sorted(set(PREFIXES.values()) | {"portable", "auto-maison", "auto-informatique"}),
                    help="auto-maison / auto-informatique : la rubrique que traitera la prochaine mise à jour "
                         "hebdomadaire (même rotation que les tâches : date « tente » la plus ancienne)")
    ap.add_argument("--max", type=int, default=0, help="nombre maximal de fiches (essai)")
    ap.add_argument("--ids", help="fiches précises, séparées par des virgules")
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--effort", default="medium", choices=["low", "medium", "high"])
    ap.add_argument("--bac-a-sable", action="store_true", help="lance agy avec --sandbox (peut bloquer la recherche)")
    ap.add_argument("--refaire", action="store_true", help="refait les fiches déjà traitées")
    a = ap.parse_args()
    d0 = json.loads((SRC / "data.json").read_text(encoding="utf-8"))
    if a.rubrique.startswith("auto-"):
        groupe = MAISON if a.rubrique == "auto-maison" else INFORMATIQUE
        fams = d0.get("familles", {})
        a.rubrique = min(groupe, key=lambda f: (fams.get(f, {}).get("tente") or fams.get(f, {}).get("iso") or ""))
        print(f"Rubrique de la prochaine mise à jour : {a.rubrique}")
    exe = agy_exe()
    options = ["--effort", a.effort] + (["--sandbox"] if a.bac_a_sable else [])
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
        if k in res and res[k].get("statut") == "ok" and not a.refaire:
            print(f"[{n}/{len(cible)}] {k} : déjà fait"); continue
        connues = [x["url"] for x in p["press"]["notes"] if x.get("url")]
        prompt = CONSIGNE.format(nom=p.get("short", k), ref=p.get("ref", ""), connus=", ".join(connues) or "aucun")
        try:
            code, texte, err, outils = demander(exe, prompt, a.timeout, options)
        except subprocess.TimeoutExpired:
            code, texte, err, outils = -1, "", "délai dépassé", []
        urls = adresses(texte, connues)
        statut = "ok" if code == 0 and texte else "echec"
        res[k] = dict(nom=p.get("short", k), ref=p.get("ref", ""), tests_avant=p["press"]["tests"], urls=urls,
                      statut=statut, erreur=(err if statut != "ok" else ""), code=code,
                      reponse_brute=(texte or "")[:2000], outils=outils,          # pour comprendre une réponse vide ou filtrée
                      adresses_ecartees=[u for u in re.findall(r"https?://[^\s\"'\]\)<>,]+", texte or "") if u.rstrip(".;") not in urls],
                      date=datetime.datetime.now().isoformat(timespec="seconds"))
        sortie.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"   outils : {', '.join(outils) or 'aucun'}")
        print(f"[{n}/{len(cible)}] {k:28s} {statut:5s} {len(urls)} adresse(s)" + (f"  ({err.strip()[:120]})" if statut != "ok" else ""))
    ok = [v for v in res.values() if v["statut"] == "ok"]
    print(f"\nBilan : {len(ok)}/{len(res)} fiches traitées, {sum(len(v['urls']) for v in ok)} adresses candidates.")
    print("Envoie le fichier à Claude (ou dis-lui « lis les candidats ») : chaque note sera lue sur la page du média.")


if __name__ == "__main__":
    main()
