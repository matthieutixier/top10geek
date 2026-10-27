# -*- coding: utf-8 -*-
"""Exporte _source/data.json vers src/data.generated.json : les 20 usages avec leur top 10, au format utilisé par Remotion.
Reprend le classement du site (règle partagée _source/classement.py) et le prix indicatif. Ne modifie jamais data.json.

  python3 _video/export_data.py
"""
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RACINE / "_source"))
from desk import DCATS                      # noqa: E402
from familles_new import ECATS, ICATS       # noqa: E402
from classement import cle, moyenne_usage, badge_affiche, appliquer_choix  # noqa: E402

DATA = json.loads((RACINE / "_source" / "data.json").read_text(encoding="utf-8"))
COULEURS = {"bureau": "#1D5FD6", "creation": "#C2410C", "gaming": "#1F9E6E", "poly": "#9A2E7A", "lowcost": "#B78900"}

LCATS = [("bureau", "bureautique", "Bureautique", "bureau", "bureautique"), ("creation", "creation", "Création", "creation", "creation"),
         ("gaming", "gaming", "Gaming", "gaming", "gaming"), ("polyvalent", "polyvalent", "Polyvalent", "poly", "polyvalent"),
         ("lowcost", "lowcost", "Low-cost", "lowcost", "lowcost")]
FAMILLES = [
    dict(key="laptop", slug="pc-portable", label="PC portables", noun="PC portables", rub="portable", mascotte="mascotte-persona-v2",
         cats=[dict(key=k, slug=s, label=l, color=COULEURS[c], badge=b, h1=None) for k, s, l, c, b in LCATS]),
    dict(key="desktop", slug="ordinateur-de-bureau", label="Ordinateurs de bureau", noun="ordinateurs de bureau", rub="bureau", mascotte="pose-tour",
         cats=[dict(key=c["key"], slug=c["slug"], label=c["label"], color=COULEURS[re.search(r"cat-(\w+)", c["color"]).group(1).replace("poly", "poly")],
                    badge=c["badge"], h1=None) for c in DCATS]),
    dict(key="ecran", slug="ecran-pc", label="Écrans PC", noun="écrans PC", rub="ecran", mascotte="pose-ecran",
         cats=[dict(key=c["key"], slug=c["slug"], label=c["label"], color=COULEURS[re.search(r"cat-(\w+)", c["color"]).group(1)], badge=c["badge"],
                    h1=c["h1"]) for c in ECATS]),
    dict(key="imprimante", slug="imprimante", label="Imprimantes", noun="imprimantes", rub="imprimante", mascotte="pose-imprimante",
         cats=[dict(key=c["key"], slug=c["slug"], label=c["label"], color=COULEURS[re.search(r"cat-(\w+)", c["color"]).group(1)], badge=c["badge"],
                    h1=c["h1"]) for c in ICATS]),
]


H1 = {
    "bureau": "Les 10 meilleurs PC portables bureautique en 2026",
    "creation": "Les 10 meilleurs PC portables pour la création en 2026",
    "gaming": "Les 10 meilleurs PC portables gaming en 2026",
    "polyvalent": "Les 10 meilleurs PC portables polyvalents en 2026",
    "lowcost": "Les 10 meilleurs PC portables à moins de 500 €",
    "d-bureau": "Les 10 meilleurs ordinateurs de bureau pour la bureautique",
    "d-creation": "Les 10 meilleurs ordinateurs de bureau pour la création",
    "d-gaming": "Les 10 meilleurs PC gamer fixes prêts à jouer",
    "d-mini": "Les 10 meilleurs mini-PC en 2026",
    "d-aio": "Les 10 meilleurs ordinateurs tout-en-un",
}


def texte(h):
    """HTML du site -> texte brut."""
    h = re.sub(r"<[^>]+>", "", h or "")
    return h.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").strip()


def euro_ind(x):
    v = int(round(x / 10.0) * 10)
    return f"{v:,}".replace(",", " ") + " €"


def rank_key(d):
    """Même classement que le site : règle partagée de _source/classement.py."""
    pr = d["press"]
    return cle(d["badge"], pr["avg"], pr["n"], pr["tests"], d["p"], d["moy"])


def produits(catkey):
    out = []
    for pid, n in DATA["items"].items():
        if n["cat"] != catkey:
            continue
        offers = [o for o in n["offers"] if o.get("dispo", True)] or n["offers"]
        p = float(n.get("prix") or min(o["price"] for o in offers))
        out.append(dict(id=pid, badge=n["badge"], press=n["press"], p=p, n=n))
    moy = moyenne_usage([d["press"]["avg"] for d in out])
    rows = [dict(id=d["id"], badge=d["badge"], avg=d["press"]["avg"], n=d["press"]["n"], tests=d["press"]["tests"], p=d["p"]) for d in out]
    chg = appliquer_choix(rows)   # règle du 27/10/2026 : choix de préférence en zone « bonnes affaires »
    for d in out:
        d["moy"] = moy
        d["badge"] = chg.get(d["id"], d["badge"])
    out.sort(key=rank_key)
    res = []
    for i, d in enumerate(out, 1):
        n, pr = d["n"], d["press"]
        res.append(dict(rang=i, id=d["id"], nom=n["short"], ref=n["ref"], badge=badge_affiche(d["badge"], i), verdict=n["verdict"],
                        fort=(n["strengths"] or [""])[0], img=(f"assets/img/p/{n['img']}" if n.get("img") else None),
                        prix=euro_ind(d["p"]), note=(round(pr["avg"], 1) if pr["avg"] is not None else None),
                        nnotes=pr["n"], ntests=pr["tests"]))
    return res


usages = []
for f in FAMILLES:
    fam_dates = DATA.get("familles", {}).get(f["rub"], {})
    for c in f["cats"]:
        h1 = texte(c["h1"]) if c["h1"] else H1[c["key"]]
        titre = h1
        titre = re.sub(r"^Les 10 meilleur(e?)s", lambda m: "Les 3 meilleur" + m.group(1) + "s", titre)
        titre = re.sub(r" en 2026$", "", titre)
        usages.append(dict(famille=f["slug"], familleLabel=f["label"], noun=f["noun"], mascotte=f["mascotte"], cle=c["key"], slug=c["slug"],
                           label=texte(c["label"]), couleur=c["color"], badge=f"assets/img/badge-{c['badge']}.webp",
                           titre3=titre, titre10=h1, prixDate=fam_dates.get("prix_date", DATA.get("prix_date", "")),
                           maj=fam_dates.get("date", DATA.get("date", "")), top=produits(c["key"])[:10]))

sortie = RACINE / "_video" / "src" / "data.generated.json"
sortie.write_text(json.dumps(dict(familles=[dict(slug=f["slug"], label=f["label"], noun=f["noun"], mascotte=f["mascotte"]) for f in FAMILLES],
                                  usages=usages), ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(usages)} usages exportés -> {sortie.relative_to(RACINE)}")
