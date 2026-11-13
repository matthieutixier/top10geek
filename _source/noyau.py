# -*- coding: utf-8 -*-
"""Noyau d'indexation (décision de Matthieu du 13/11/2026, plan de remontée Google).

- Règle d'indexation d'une fiche (gen10.py, indexable()) : une synthèse « Ce que disent les tests » ET au moins 3 tests recensés.
- Sitemap : sitemap-v2.xml = noyau fixe (_source/sitemap_v2.json), produit UNE FOIS par ce script :
  accueil, méthode, à propos, étude, 4 rubriques Informatique, leurs usages, et les fiches Informatique
  avec synthèse et au moins 4 tests. Les autres pages indexables (Maison, fiches à 3 tests) restent indexables
  mais hors sitemap, en attendant que le noyau soit indexé ; elles y entreront par lots, sur décision de Matthieu.

  python3 _source/noyau.py            # aperçu
  python3 _source/noyau.py --ecrire   # écrit _source/sitemap_v2.json (ne pas relancer sans décision : la liste est figée)
"""
import json, sys, datetime
from pathlib import Path

SRC = Path(__file__).resolve().parent
D = json.loads((SRC / "data.json").read_text(encoding="utf-8"))["items"]
INFO = {"portable": ("pc-portable", ""), "bureau": ("ordinateur-de-bureau", "d-"), "ecran": ("ecran-pc", "e-"), "imprimante": ("imprimante", "i-")}
MAISON = ("s-", "t-", "a-", "v-")


def famille_info(cat):
    if cat.startswith(MAISON):
        return None
    for f, (slug, pre) in INFO.items():
        if pre and cat.startswith(pre):
            return f
    return "portable"


def tests(v):
    return (v.get("press") or {}).get("tests") or 0


def complet(v, mini):
    return bool(v.get("synthese")) and tests(v) >= mini


if __name__ == "__main__":
    fiches = sorted(k for k, v in D.items() if famille_info(v["cat"]) and v["cat"] != "reconditionne" and complet(v, 4))
    print(len(fiches), "fiches Informatique avec synthèse et 4 tests ou plus")
    if "--ecrire" in sys.argv:
        (SRC / "sitemap_v2.json").write_text(json.dumps({
            "date": datetime.date.today().isoformat(),
            "regle": "fiches Informatique avec synthèse et au moins 4 tests, + accueil, méthode, à propos, étude, rubriques et usages Informatique",
            "fiches": fiches}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print("écrit : _source/sitemap_v2.json")
