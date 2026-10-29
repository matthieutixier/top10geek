#!/usr/bin/env python3
"""Historique des prix pour la page Black Friday (« baisses constatées »).

Principe : à chaque passage, on photographie les prix de data.json (offres en vente, par marchand) dans
_source/historique_prix.json, au format { "AAAA-MM-JJ": { "<id produit>": { "<marchand>": prix } } }.
Un seul instantané par jour (le dernier du jour remplace le précédent). On ne mélange jamais deux marchands :
la baisse d'un produit est mesurée marchand par marchand (voir bf_baisses dans gen10.py).

Usage :
    python3 _source/bf_historique.py                 # instantané du jour (à lancer après les relevés de prix)
    python3 _source/bf_historique.py --seed-git 35   # reconstitue les jours passés depuis l'historique Git de data.json
    python3 _source/bf_historique.py --etat          # nombre de jours et de produits suivis

Ne modifie jamais data.json.
"""
import datetime
import json
import os
import subprocess
import sys
from zoneinfo import ZoneInfo

SRC = os.path.dirname(os.path.abspath(__file__)) + "/"
HIST = SRC + "historique_prix.json"
GARDER_JOURS = 120   # au-delà, les jours les plus anciens sont supprimés


def charger():
    return json.load(open(HIST, encoding="utf-8")) if os.path.exists(HIST) else {}


def enregistrer(h):
    for j in sorted(h)[:-GARDER_JOURS]:
        del h[j]
    with open(HIST, "w", encoding="utf-8") as f:
        json.dump(h, f, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def prix_par_marchand(items):
    """{id: {marchand: prix}} pour les offres en vente (dispo ≠ False) avec un prix > 0, hors vendeurs tiers."""
    res = {}
    for pid, n in items.items():
        m = {}
        for o in n.get("offers", []):
            # vendeur tiers (Amazon) exclu : son prix n'est pas celui du marchand et change de vendeur sans prévenir
            if o.get("dispo", True) and o.get("price") and "tiers" not in (o.get("cfg") or ""):
                m[o["m"]] = min(float(o["price"]), m.get(o["m"], 1e9))
        if m:
            res[pid] = m
    return res


def aujourdhui():
    return datetime.datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d")


def instantane():
    items = json.load(open(SRC + "data.json", encoding="utf-8"))["items"]
    h = charger()
    h[aujourdhui()] = prix_par_marchand(items)
    enregistrer(h)
    print(f"OK instantané du {aujourdhui()} : {len(h[aujourdhui()])} produits, {len(h)} jour(s) en historique")


def seed_git(jours):
    """Reconstitue des instantanés passés depuis les commits qui ont touché data.json (le dernier commit de chaque jour)."""
    racine = os.path.dirname(SRC.rstrip("/"))
    depuis = (datetime.date.today() - datetime.timedelta(days=jours)).isoformat()
    out = subprocess.run(["git", "-C", racine, "log", f"--since={depuis}", "--format=%H %ad", "--date=short", "--", "_source/data.json"],
                         capture_output=True, text=True, check=True).stdout.split("\n")
    par_jour = {}
    for ligne in out:           # du plus récent au plus ancien : on garde le premier vu de chaque jour
        if ligne.strip():
            sha, jour = ligne.split()
            par_jour.setdefault(jour, sha)
    h = charger()
    for jour, sha in sorted(par_jour.items()):
        if jour in h:
            continue
        brut = subprocess.run(["git", "-C", racine, "show", f"{sha}:_source/data.json"], capture_output=True, text=True, check=True).stdout
        h[jour] = prix_par_marchand(json.loads(brut)["items"])
        print("  ", jour, sha[:8], len(h[jour]), "produits")
    enregistrer(h)


if __name__ == "__main__":
    if "--seed-git" in sys.argv:
        seed_git(int(sys.argv[sys.argv.index("--seed-git") + 1]))
    elif "--etat" in sys.argv:
        h = charger()
        print(len(h), "jour(s) :", ", ".join(sorted(h)[:1] + sorted(h)[-1:]) if h else "aucun")
    else:
        instantane()
