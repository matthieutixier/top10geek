# -*- coding: utf-8 -*-
"""Ajoute (ou met à jour) dans data.json les écrans et imprimantes de catalog_ecrans.py et catalog_imprimantes.py.
Les 100 ordinateurs déjà présents ne sont pas touchés. Commande : python3 _source/build_new.py
- offres : Amazon (prix constaté lors du relevé, identifiant Partenaires ajouté au lien) et/ou Electro Dépôt (champ ed :
  lien suivi Effinity et prix du flux produits) ; un produit déjà présent
  garde le prix et la disponibilité de son dernier relevé (releve.py) ;
- note presse : moyenne des notes chiffrées (les tests sans note sont listés mais n'entrent pas dans la moyenne) ;
  une note nouvelle ou modifiée qui n'a pas été lue sur la page du média est mise en attente (garde_notes.py) ;
- photo : assets/img/p/<id>.webp si elle existe (photos constructeurs, voir photos_constructeurs.json) ;
- un écran ou une imprimante retiré de catalog_ecrans.py / catalog_imprimantes.py est retiré de data.json."""
import copy, datetime, json, os, sys
SRC = os.path.dirname(os.path.abspath(__file__)) + "/"
sys.path.insert(0, SRC)
from catalog_ecrans import ECR
from catalog_imprimantes import IMP
from catalog_sols import SOLS
from garde_notes import controler_import, recalc

AMAZON_TAG = "geekconcept-21"
IMG_DIR = os.path.join(os.path.dirname(SRC.rstrip("/")), "assets/img/p")


def press(it):
    notes = [dict(src=s, score=(float(v) if v is not None else None), url=u, date="") for s, v, u in it["notes"]]
    notes.sort(key=lambda n: (n["score"] is None, -(n["score"] or 0), n["src"]))
    scored = [n for n in notes if n["score"] is not None]
    return dict(avg=(sum(n["score"] for n in scored) / len(scored)) if scored else None, n=len(scored), tests=len(notes),
                scope=it["scope"], src=["", ""], notes=notes)


def item(pid, it):
    offers = []
    if it["asin"]:
        tiers = it["seller"] != "Amazon"
        offers.append(dict(m="Amazon", price=float(it["price"]), url=f"https://www.amazon.fr/dp/{it['asin']}?tag={AMAZON_TAG}",
                           name=it["amz"], cfg=("vendu par un vendeur tiers" if tiers else ""), asin=it["asin"]))
    if it.get("ed"):
        e = it["ed"]   # Electro Dépôt : lien suivi Effinity tel que fourni par le flux produits
        offers.append(dict(m="Electro Dépôt", price=float(e["price"]), url=e["url"], name=e["name"], cfg="",
                           ean=e["ean"], edid=e["edid"]))
    assert offers, pid
    img = pid + ".webp"
    d = {k: v for k, v in it.items() if k not in ("notes", "scope", "asin", "amz", "price", "seller", "pour", "eviter", "ed")}
    d.update(id=pid, m=list(it["m"]), offers=offers, press=press(it), prix=min(o["price"] for o in offers),
             img=img if os.path.exists(os.path.join(IMG_DIR, img)) else None, rating=None, nrev=0)
    return d


if __name__ == "__main__":
    path = SRC + "data.json"
    data = json.load(open(path, encoding="utf-8"))
    jour = datetime.date.today().strftime("%d/%m/%Y")
    en_attente = []
    tests_ignores = []
    for cat in (ECR, IMP, SOLS):
        for pid, it in cat.items():
            new, old = item(pid, it), data["items"].get(pid)
            # un relevé de prix (releve.py) a pu mettre à jour l'offre depuis : on garde ses prix et sa disponibilité
            if old and old["offers"] and it["asin"] and old["offers"][0].get("asin") == it["asin"]:
                for f in ("price", "dispo"):
                    if f in old["offers"][0]:
                        new["offers"][0][f] = old["offers"][0][f]
                new["prix"] = old.get("prix", new["prix"])
            # offres d'un produit existant (20/11/2026) : celles de data.json font foi (prix et dates des relevés, offres
            # Electro Dépôt ajoutées par effinity.py, mention vendeur tiers corrigée) ; seul un changement d'ASIN Amazon
            # dans le catalogue remplace l'offre Amazon.
            if old and old.get("offers"):
                amz_new = next((o for o in new["offers"] if o["m"] == "Amazon"), None)
                amz_old = next((o for o in old["offers"] if o["m"] == "Amazon"), None)
                offres = copy.deepcopy(old["offers"])
                if amz_new and amz_old and amz_new.get("asin") != amz_old.get("asin"):
                    offres = [amz_new if o["m"] == "Amazon" else o for o in offres]
                elif amz_new and not amz_old:
                    offres.insert(0, amz_new)
                new["offers"] = offres
                new["prix"] = old.get("prix", new["prix"])
            # tests ajoutés par ajout_tests.py (mise à jour hebdomadaire) : conservés
            if old and old.get("press"):
                urls = {n["url"] for n in new["press"]["notes"]}
                extra = [n for n in old["press"]["notes"] if n.get("ajout") and n["url"] not in urls]
                # note retrouvée par ajout_tests.py pour un test déjà au catalogue sans note
                notes_ajout = {n["url"]: n for n in old["press"]["notes"] if n.get("ajout") and n["url"] in urls}
                for n in new["press"]["notes"]:
                    a = notes_ajout.get(n["url"])
                    if a and n["score"] is None and a["score"] is not None:
                        n.update(score=a["score"], ajout=a["ajout"])
                if notes_ajout:
                    keep = {n["url"]: n.get("ajout") for n in new["press"]["notes"]}
                    new["press"] = press(dict(notes=[(n["src"], n["score"], n["url"]) for n in new["press"]["notes"]],
                                              scope=new["press"]["scope"]))
                    for n in new["press"]["notes"]:
                        if keep.get(n["url"]):
                            n["ajout"] = keep[n["url"]]
                if extra:
                    new["press"]["notes"] += extra
                    new["press"] = press(dict(notes=[(n["src"], n["score"], n["url"]) for n in new["press"]["notes"]],
                                              scope=new["press"]["scope"]))
                    for n in new["press"]["notes"]:
                        e = next((x for x in extra if x["url"] == n["url"]), None)
                        if e:
                            n.update(date=e.get("date", ""), ajout=e["ajout"])
            # traces des vérifications presse (presse_crawl.py : « avant », « corrige », « verifie ») et dates connues : conservées
            if old and old.get("press"):
                anciens = {n["url"]: n for n in old["press"]["notes"]}
                for n in new["press"]["notes"]:
                    o = anciens.get(n["url"])
                    if o and o.get("score") == n["score"]:
                        for f in ("avant", "corrige", "verifie"):
                            if f in o and f not in n:
                                n[f] = o[f]
                        if o.get("date") and not n.get("date"):
                            n["date"] = o["date"]
            # data.json fait foi pour les notes d'un produit existant (20/11/2026) : les catalogues et cc_fiches ne servent
            # qu'à créer un produit ; ensuite, les notes ne changent que par presse_crawl.py et ajout_tests.py.
            if old and old.get("press"):
                ignores = {n["url"] for n in new["press"]["notes"]} - {n["url"] for n in old["press"]["notes"]}
                if ignores:
                    tests_ignores.append((pid, len(ignores)))
                new["press"] = copy.deepcopy(old["press"])
            # garde-fou (20/11/2026) : une note non lue sur la page du média n'entre pas dans la moyenne (garde_notes.py)
            att = controler_import(new["press"], old["press"] if old else None, jour)
            if att:
                recalc(new["press"])
                en_attente.append((pid, att))
            # synthèse rédigée (syntheses.py) : conservée
            if old and old.get("synthese"):
                new["synthese"] = old["synthese"]
            data["items"][pid] = new
    # écrans et imprimantes retirés des catalogues : retirés aussi de data.json (les ordinateurs ne sont pas concernés)
    retires = [k for k, v in data["items"].items() if v["cat"][:2] in ("e-", "i-", "s-", "t-", "a-", "v-") and k not in ECR and k not in IMP and k not in SOLS]
    for k in retires:
        del data["items"][k]
    if retires:
        print("retirés :", ", ".join(retires))
    open(path, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=1) + "\n")
    from collections import Counter
    print(len(data["items"]), "produits ;", Counter(d["cat"] for d in data["items"].values() if d["cat"][:2] in ("e-", "i-", "s-", "t-", "a-", "v-")))
    if tests_ignores:
        print(f"\nTests des catalogues absents de data.json, ignorés ({sum(n for _, n in tests_ignores)}) : un test s'ajoute par ajout_tests.py "
              "(retirés volontairement ou jamais vérifiés) — " + ", ".join(f"{p} ({n})" for p, n in tests_ignores[:12]))
    if en_attente:
        print(f"\nNotes EN ATTENTE de lecture à la source ({sum(len(a) for _, a in en_attente)}) : citées sans note jusqu'à confirmation.")
        for pid, att in en_attente:
            print(f"  {pid:30s} " + ", ".join(f"{s} {v}" for s, v in att))
        ids = ",".join(pid for pid, _ in en_attente)
        print(f"Ensuite : python3 _source/presse_crawl.py verifier --famille <rubrique> --ids {ids}"
              " puis appliquer --apply ; le reste : confirmer (lecture à la main).")
    print("sans photo :", sum(1 for d in data["items"].values() if d["cat"][:2] in ("e-", "i-") and not d["img"]))
