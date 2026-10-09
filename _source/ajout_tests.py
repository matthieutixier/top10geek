# -*- coding: utf-8 -*-
"""Ajoute de nouveaux tests presse à des produits existants de data.json (mise à jour hebdomadaire).

  python3 _source/ajout_tests.py _source/data/nouveaux_tests.json          # aperçu, rien n'est écrit
  python3 _source/ajout_tests.py _source/data/nouveaux_tests.json --apply  # écrit data.json

Fichier d'entrée : liste d'objets
  {"id": "<id produit de data.json>", "src": "Les Numériques", "score": 8.0 ou null, "url": "https://…", "date": "AAAA-MM-JJ"}
- score : note ramenée sur 10 (4/5 -> 8.0 ; 87 % -> 8.7) ; null pour un test sans note chiffrée.
- Un test déjà présent (même URL, ou même média et même note) est ignoré.
- La note presse (moyenne, nombre de notes, nombre de tests) est recalculée comme dans build_data.py.
- Chaque test ajouté porte "ajout": "JJ/MM/AAAA" ; build_new.py conserve ces ajouts pour les écrans et imprimantes.
Règle : jamais de test inventé — chaque entrée doit venir d'une page réellement lue, avec son URL."""
import datetime
import json
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

SRC = Path(__file__).resolve().parent
DATA = SRC / "data.json"


def recalc(pr):
    notes = pr["notes"]
    notes.sort(key=lambda n: (n["score"] is None, -(n["score"] or 0), n["src"]))
    scored = [n for n in notes if n["score"] is not None]
    pr.update(avg=(sum(n["score"] for n in scored) / len(scored)) if scored else None, n=len(scored), tests=len(notes))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    apply = "--apply" in sys.argv
    entrees = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    brut = DATA.read_text(encoding="utf-8")
    d = json.loads(brut)
    jour = datetime.datetime.now(ZoneInfo("Europe/Paris")).strftime("%d/%m/%Y")
    ajoutes, ignores = 0, 0
    for e in entrees:
        it = d["items"].get(e["id"])
        if not it:
            print(f"!! produit inconnu : {e['id']}")
            ignores += 1
            continue
        if not str(e.get("url", "")).startswith("http"):
            print(f"!! URL manquante : {e}")
            ignores += 1
            continue
        sc = e.get("score")
        if sc is not None and not (0 < float(sc) <= 10):
            print(f"!! note hors échelle (doit être sur 10) : {e}")
            ignores += 1
            continue
        pr = it.get("press") or dict(avg=None, n=0, tests=0, scope="modele", src=["", ""], notes=[])
        it["press"] = pr
        if any(n["url"] == e["url"] or (n["src"] == e["src"] and sc is not None and n["score"] == float(sc))
               for n in pr["notes"]):
            print(f"   déjà présent : {e['id']} · {e['src']}")
            ignores += 1
            continue
        avant = pr["avg"]
        pr["notes"].append(dict(src=e["src"], score=(float(sc) if sc is not None else None), url=e["url"],
                                date=e.get("date", ""), ajout=jour))
        recalc(pr)
        ajoutes += 1
        f = lambda x: "—" if x is None else f"{x:.2f}"
        print(f"+  {e['id']:28s} {e['src']:22s} {('%.1f' % float(sc)) if sc is not None else 'sans note':>9s}   "
              f"note presse {f(avant)} -> {f(pr['avg'])} ({pr['n']} notes, {pr['tests']} tests)")
    print(f"\n{ajoutes} test(s) ajouté(s), {ignores} ignoré(s).")
    if apply and ajoutes:
        DATA.write_text(json.dumps(d, ensure_ascii=False, indent=1) + ("\n" if brut.endswith("\n") else ""), encoding="utf-8")
        print("data.json mis à jour. Reste : python3 _source/gen10.py")
    elif ajoutes:
        print("Aperçu seulement : relancer avec --apply pour écrire data.json.")


if __name__ == "__main__":
    main()
