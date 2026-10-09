# -*- coding: utf-8 -*-
"""Ajoute (ou met à jour) dans data.json les écrans et imprimantes de catalog_ecrans.py et catalog_imprimantes.py.
Les 100 ordinateurs déjà présents ne sont pas touchés. Commande : python3 _source/build_new.py
- offres : Amazon (prix constaté lors du relevé, identifiant Partenaires ajouté au lien) ; un produit déjà présent
  garde le prix et la disponibilité de son dernier relevé (releve.py) ;
- note presse : moyenne des notes chiffrées (les tests sans note sont listés mais n'entrent pas dans la moyenne) ;
- photo : assets/img/p/<id>.webp si elle existe (photos constructeurs, voir photos_constructeurs.json)."""
import json, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, SRC)
from catalog_ecrans import ECR
from catalog_imprimantes import IMP

AMAZON_TAG = "geekconcept-21"
IMG_DIR = os.path.join(os.path.dirname(SRC.rstrip("/")), "assets/img/p")


def press(it):
    notes = [dict(src=s, score=(float(v) if v is not None else None), url=u, date="") for s, v, u in it["notes"]]
    notes.sort(key=lambda n: (n["score"] is None, -(n["score"] or 0), n["src"]))
    scored = [n for n in notes if n["score"] is not None]
    return dict(avg=(sum(n["score"] for n in scored) / len(scored)) if scored else None, n=len(scored), tests=len(notes),
                scope=it["scope"], src=["", ""], notes=notes)


def item(pid, it):
    tiers = it["seller"] != "Amazon"
    offer = dict(m="Amazon", price=float(it["price"]), url=f"https://www.amazon.fr/dp/{it['asin']}?tag={AMAZON_TAG}",
                 name=it["amz"], cfg=("vendu par un vendeur tiers" if tiers else ""), asin=it["asin"])
    img = pid + ".webp"
    d = {k: v for k, v in it.items() if k not in ("notes", "scope", "asin", "amz", "price", "seller", "pour", "eviter")}
    d.update(id=pid, m=list(it["m"]), offers=[offer], press=press(it), prix=float(it["price"]),
             img=img if os.path.exists(os.path.join(IMG_DIR, img)) else None, rating=None, nrev=0)
    return d


if __name__ == "__main__":
    path = SRC + "data.json"
    data = json.load(open(path, encoding="utf-8"))
    for cat in (ECR, IMP):
        for pid, it in cat.items():
            new, old = item(pid, it), data["items"].get(pid)
            # un relevé de prix (releve.py) a pu mettre à jour l'offre depuis : on garde ses prix et sa disponibilité
            if old and old["offers"] and old["offers"][0].get("asin") == it["asin"]:
                for f in ("price", "dispo"):
                    if f in old["offers"][0]:
                        new["offers"][0][f] = old["offers"][0][f]
                new["prix"] = old.get("prix", new["prix"])
            data["items"][pid] = new
    json.dump(data, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(data["items"]), "produits ;", Counter(d["cat"] for d in data["items"].values() if d["cat"][:2] in ("e-", "i-")))
    print("sans photo :", sum(1 for d in data["items"].values() if d["cat"][:2] in ("e-", "i-") and not d["img"]))
