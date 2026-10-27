# -*- coding: utf-8 -*-
"""Synthèses rédigées des fiches produit (audit SEO du 10/10/2026 : « fiches minces et gabaritées »).

Une synthèse résume ce que disent réellement les tests cités sur la fiche : points d'accord, désaccords entre médias,
limites relevées, pour qui. Elle s'affiche sur la fiche, sous « Le consensus de la presse », avec sa date et ses sources.

  python3 _source/syntheses.py a-faire [--famille ecran] [--top 10]
      Fiches à 3 notes presse ou plus sans synthèse, puis synthèses périmées (notes ou tests ajoutés depuis la rédaction).
  python3 _source/syntheses.py appliquer _source/data/syntheses.json [--apply]
      Contrôle puis écrit les synthèses dans data.json. Sans --apply : aperçu.

Fichier d'entrée : [{"id": "<produit>", "texte": "…", "sources": ["Les Numériques", "Notebookcheck", …]}]
  - texte : 500 à 1 500 caractères, paragraphes séparés par une ligne vide, texte brut (ni HTML ni lien) ;
  - sources : médias réellement lus pour la rédiger, tous cités sur la fiche ; au moins 2 sont nommés dans le texte.

Règles (vérifiées autant que possible par le script) : seulement des fiches à 3 notes presse ou plus ; rien d'inventé —
chaque affirmation vient d'un test cité et lu ; pas de superlatif publicitaire ; pas de phrase type reprise d'une fiche à
l'autre (une synthèse trop proche d'une autre est refusée) ; la note et le classement ne sont jamais modifiés ici."""
import datetime
import json
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

SRC = Path(__file__).resolve().parent
DATA = SRC / "data.json"
SEUIL = 3
PUB = re.compile(r"\b(incroyable|révolutionnaire|exceptionnel(le)?|parfait(e)?|imbattable|le meilleur du marché|à couper le souffle|must-have|bluffant)\b", re.I)
FAM = lambda cat: "robot" if cat.startswith("s-") else "ecran" if cat.startswith("e-") else "imprimante" if cat.startswith("i-") else "bureau" if cat.startswith("d-") else "portable"


def ngrams(t, k=5):
    w = re.findall(r"\w+", t.lower())
    return {" ".join(w[i:i + k]) for i in range(len(w) - k + 1)}


def perimee(it):
    s, pr = it.get("synthese"), it["press"]
    return bool(s) and (s.get("n") != pr["n"] or s.get("tests") != pr["tests"])


def a_faire(a):
    d = json.loads(DATA.read_text(encoding="utf-8"))
    rows = []
    for pid, it in d["items"].items():
        if a.get("famille") and FAM(it["cat"]) != a["famille"]:
            continue
        pr = it["press"]
        if pr["avg"] is None or pr["n"] < SEUIL:
            continue
        if not it.get("synthese"):
            rows.append((0, -pr["n"], pid, f"sans synthèse · {pr['n']} notes"))
        elif perimee(it):
            rows.append((1, -pr["n"], pid, f"périmée ({it['synthese']['date']}) · {it['synthese']['n']} -> {pr['n']} notes"))
    rows.sort()
    print(f"{len(rows)} fiche(s) à rédiger ou à revoir")
    for _, _, pid, txt in rows[:a.get("top", 10)]:
        print(f"  {pid:32s} {txt}")


def appliquer(fichier, apply):
    d = json.loads(DATA.read_text(encoding="utf-8"))
    jour = datetime.datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d")
    entrees = json.loads(Path(fichier).read_text(encoding="utf-8"))
    autres = {pid: ngrams(it["synthese"]["texte"]) for pid, it in d["items"].items() if it.get("synthese")}
    ok = 0
    for e in entrees:
        pid, t = e.get("id"), (e.get("texte") or "").strip()
        it = d["items"].get(pid)
        err = []
        if not it:
            err.append("produit inconnu")
        else:
            pr = it["press"]
            medias = {n["src"] for n in pr["notes"]}
            if pr["avg"] is None or pr["n"] < SEUIL:
                err.append(f"moins de {SEUIL} notes presse")
            if not 500 <= len(t) <= 1500:
                err.append(f"longueur {len(t)} (500 à 1 500)")
            if re.search(r"<|https?://|www\.", t):
                err.append("HTML ou lien dans le texte")
            if PUB.search(t):
                err.append(f"superlatif publicitaire : « {PUB.search(t).group(0)} »")
            src = e.get("sources") or []
            hors = [s for s in src if s not in medias]
            if not src or hors:
                err.append(f"sources absentes de la fiche : {hors or 'aucune source'}")
            elif sum(1 for s in src if s.lower() in t.lower()) < min(2, len(src)):
                err.append("moins de 2 médias nommés dans le texte")
            g = ngrams(t)
            for o, go in autres.items():
                if o != pid and g and len(g & go) / len(g) > 0.15:
                    err.append(f"trop proche de la synthèse de {o}")
                    break
        if err:
            print(f"REFUSÉE {pid} : " + " ; ".join(err))
            continue
        it["synthese"] = dict(texte=t, date=jour, n=it["press"]["n"], tests=it["press"]["tests"], sources=src)
        autres[pid] = ngrams(t)
        ok += 1
        print(f"ok      {pid} ({len(t)} caractères, {len(src)} sources)")
    if apply and ok:
        DATA.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"{ok} synthèse(s) écrite(s) dans data.json. Reste : python3 _source/gen10.py")
    elif ok:
        print("Aperçu seulement : relancer avec --apply.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["a-faire"]:
        opts = {"top": 10}
        if "--famille" in args:
            opts["famille"] = args[args.index("--famille") + 1]
        if "--top" in args:
            opts["top"] = int(args[args.index("--top") + 1])
        a_faire(opts)
    elif args[:1] == ["appliquer"] and len(args) >= 2:
        appliquer(args[1], "--apply" in args)
    else:
        sys.exit(__doc__)
