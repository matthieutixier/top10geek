# -*- coding: utf-8 -*-
"""Offres Electro Dépôt à partir du flux produits Effinity (programme affilié validé le 12/10/2026).

  python3 _source/effinity.py            # aperçu : ce qui changerait, rien n'est écrit
  python3 _source/effinity.py --apply    # met à jour data.json

L'adresse du flux contient une clé API personnelle : elle ne doit JAMAIS être versionnée (dépôt public).
Elle est lue dans la variable d'environnement EFFINITY_URL, sinon dans _source/effinity.local.json
({"url": "https://products.effinity.fr/product-output/output/…?apikey=…"}), fichier exclu de Git.

Ce que fait le script :
- télécharge le flux (CSV séparé par « ; », une ligne par produit en stock, EAN dans « gtin ») ;
- offres Electro Dépôt déjà présentes dans data.json (repérées par leur EAN) : met à jour prix, lien suivi,
  libellé, disponibilité (produit absent du flux = « dispo »: false) et date de relevé (« releve ») ;
- effinity_map.json : produits du catalogue vendus chez Electro Dépôt sans offre encore créée (équivalences
  vérifiées à la main, ex. TS4150i = TS4151i) ; l'offre est créée si l'EAN est dans le flux ;
- recalcule le prix indicatif de chaque produit touché (« prix » = le plus bas des offres en vente) ;
- ne charge aucune page marchande (les liens sont des liens de suivi : les ouvrir compterait de faux clics).
Le prix Electro Dépôt est affiché tel quel sur le site (avec sa date de relevé) : relancer ce script
à chaque mise à jour (tâche du vendredi), pour toutes les rubriques."""
import csv
import datetime
import io
import json
import os
import sys
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

SRC = Path(__file__).resolve().parent
DATA = SRC / "data.json"
MAP = SRC / "effinity_map.json"
LOCAL = SRC / "effinity.local.json"
M = "Electro Dépôt"


def flux_url():
    url = os.environ.get("EFFINITY_URL")
    if not url and LOCAL.exists():
        url = json.loads(LOCAL.read_text(encoding="utf-8")).get("url")
    if not url:
        sys.exit("Adresse du flux introuvable : variable EFFINITY_URL ou fichier _source/effinity.local.json")
    return url


def lire_flux(url):
    req = urllib.request.Request(url, headers={"User-Agent": "top10geek-effinity/1.0"})
    brut = urllib.request.urlopen(req, timeout=120).read().decode("utf-8")
    csv.field_size_limit(10 ** 9)
    lignes = list(csv.DictReader(io.StringIO(brut), delimiter=";"))
    if len(lignes) < 500 or "gtin" not in lignes[0]:
        sys.exit(f"Flux anormal ({len(lignes)} lignes) : rien n'est modifié")
    return {x["gtin"].strip(): x for x in lignes if x.get("gtin")}


def prix_indicatif(it):
    en_vente = [o["price"] for o in it["offers"] if o.get("dispo", True)]
    return min(en_vente) if en_vente else it.get("prix")


def main():
    apply = "--apply" in sys.argv
    flux = lire_flux(flux_url())
    jour = datetime.datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d")
    d = json.loads(DATA.read_text(encoding="utf-8"))
    carte = json.loads(MAP.read_text(encoding="utf-8")) if MAP.exists() else {}
    lignes, touches = [], set()

    # 1. offres à créer (produits du catalogue reconnus dans le flux, voir effinity_map.json)
    for pid, m in carte.items():
        it = d["items"].get(pid)
        if not it or any(o["m"] == M for o in it["offers"]):
            continue
        x = flux.get(m["ean"])
        if not x:
            lignes.append(f"  {pid} : EAN {m['ean']} absent du flux, offre non créée")
            continue
        it["offers"].append(dict(m=M, price=float(x["price"]), url=x["link"], name=x["title"].strip(),
                                 cfg=m.get("cfg", ""), ean=m["ean"], edid=x["id"]))
        touches.add(pid)
        lignes.append(f"+ {pid} : offre créée, {x['price']} €")

    # 2. mise à jour de toutes les offres Electro Dépôt
    for pid, it in d["items"].items():
        for o in it["offers"]:
            if o["m"] != M:
                continue
            x = flux.get(o.get("ean", ""))
            avant = (o["price"], o.get("dispo", True))
            if x:
                o.update(price=float(x["price"]), url=x["link"], name=x["title"].strip(), edid=x["id"], releve=jour)
                o.pop("dispo", None)
            else:
                o["dispo"] = False
                o["releve"] = jour
            apres = (o["price"], o.get("dispo", True))
            if apres != avant:
                touches.add(pid)
                lignes.append(f"~ {pid} : {avant[0]} € → {apres[0]} €" + ("" if apres[1] else " (plus en vente)"))
            touches.add(pid)   # date de relevé mise à jour : prix indicatif recalculé

    for pid in touches:
        it = d["items"][pid]
        it["prix"] = prix_indicatif(it)

    nb = sum(1 for it in d["items"].values() for o in it["offers"] if o["m"] == M)
    nv = sum(1 for it in d["items"].values() for o in it["offers"] if o["m"] == M and o.get("dispo", True))
    print(f"Flux : {len(flux)} produits. Offres Electro Dépôt : {nb} ({nv} en vente).")
    print("\n".join(lignes) if lignes else "Aucun changement de prix ni de disponibilité.")
    if apply:
        DATA.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print("data.json mis à jour. Reste : python3 _source/gen10.py")
    else:
        print("(aperçu : relancer avec --apply pour écrire data.json)")


if __name__ == "__main__":
    main()
