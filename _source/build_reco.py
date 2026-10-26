# -*- coding: utf-8 -*-
"""Ajoute (ou met à jour) dans data.json les 10 reconditionnés de catalog_reconditionnes.py (usage « reconditionne »).
Les autres produits ne sont pas touchés. Commande : python3 _source/build_reco.py [--fichier flux.csv]
Notes presse : moyenne des notes chiffrées ; les tests sans note (LaptopMedia, LaptopMag) sont listés mais n'entrent pas
dans la moyenne. Les offres PC-Portable.net viennent du flux (pcportable.py). Un produit retiré du catalogue est retiré
de data.json. Les tests ajoutés par ajout_tests.py, les synthèses (syntheses.py) et les traces de vérification
(presse_crawl.py) d'un produit déjà présent sont conservés."""
import json, os, sys
IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/img/p")
SRC = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, SRC)
from catalog_reconditionnes import RECO
import pcportable


def press(notes, scope):
    ns = [dict(src=s, score=(float(v) if v is not None else None), url=u, date=dt, **({"verifie": vf} if vf else {}))
          for s, v, u, dt, vf in notes]
    ns.sort(key=lambda n: (n["score"] is None, -(n["score"] or 0), n["src"]))
    sc = [n for n in ns if n["score"] is not None]
    return dict(avg=(sum(n["score"] for n in sc) / len(sc)) if sc else None, n=len(sc), tests=len(ns), scope=scope, src=["", ""], notes=ns)


if __name__ == "__main__":
    path = SRC + "data.json"
    data = json.load(open(path, encoding="utf-8"))
    fichier = sys.argv[sys.argv.index("--fichier") + 1] if "--fichier" in sys.argv else None
    flux = pcportable.lire_flux(fichier=fichier)
    for pid, it in RECO.items():
        old = data["items"].get(pid)
        d = dict(cat="reconditionne", short=it["short"], ref=it["ref"], badge=it["badge"], verdict=it["verdict"],
                 strengths=it["strengths"], weak=it["weak"], m=list(it["m"]), id=pid,
                 press=press(it["notes"], "modele"), offers=[], img=(pid + ".webp") if os.path.exists(os.path.join(IMG_DIR, pid + ".webp")) else None, rating=None, nrev=0)
        if old:
            d["offers"] = [o for o in old["offers"] if o["m"] == pcportable.M]
            if old.get("synthese"):
                d["synthese"] = old["synthese"]
            urls = {n["url"] for n in d["press"]["notes"]}
            extra = [n for n in old["press"]["notes"] if n.get("ajout") and n["url"] not in urls]
            if extra:
                d["press"]["notes"] += extra
                d["press"] = press([(n["src"], n["score"], n["url"], n.get("date", ""), n.get("verifie")) for n in d["press"]["notes"]], "modele")
                for n in d["press"]["notes"]:
                    e = next((x for x in extra if x["url"] == n["url"]), None)
                    if e:
                        n["ajout"] = e["ajout"]
        data["items"][pid] = d
    n = pcportable.rafraichir(data, flux, RECO)
    retires = [k for k, v in data["items"].items() if v["cat"] == "reconditionne" and k not in RECO]
    for k in retires:
        del data["items"][k]
    if retires:
        print("retirés :", ", ".join(retires))
    for pid in RECO:
        assert data["items"][pid]["offers"], f"{pid}: aucune offre trouvée dans le flux"
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(RECO), "reconditionnés ;", n, "offre(s) créée(s) ou modifiée(s)")
    for pid in RECO:
        o = data["items"][pid]["offers"][0]
        print(f"  {pid}: {o['price']} € · {o['cfg']}")
