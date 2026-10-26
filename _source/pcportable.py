# -*- coding: utf-8 -*-
"""Offres PC-Portable.net (reconditionnés) à partir du flux produits Effinity (programme validé en octobre 2026).

  python3 _source/pcportable.py            # aperçu : ce qui changerait, rien n'est écrit
  python3 _source/pcportable.py --apply    # met à jour data.json
  python3 _source/pcportable.py --fichier flux.csv   # lit un flux déjà téléchargé

L'adresse du flux contient une clé API personnelle : elle ne doit JAMAIS être versionnée (dépôt public).
Elle est lue dans la variable d'environnement PCPORTABLE_URL, sinon dans _source/effinity.local.json
(clé « url_pc_portable »), fichier exclu de Git.

Contrairement à Electro Dépôt, le flux n'a pas d'EAN (« gtin » = référence interne du vendeur, non fiable) :
- chaque produit de catalog_reconditionnes.py garde l'identifiant d'annonce retenu (« ppid ») ;
- si l'annonce a disparu du flux, une annonce équivalente est cherchée (expression « re » du catalogue, moins « non »),
  Windows 11 d'abord puis la moins chère en stock, 8 Go de RAM minimum, clavier AZERTY (annonces « Qwertz » exclues) ;
- l'offre porte la configuration exacte de l'annonce (« cfg ») : le prix affiché est celui de CETTE configuration ;
- prix indicatif du produit = prix de l'annonce retenue ; aucune page marchande n'est chargée
  (les liens sont des liens de suivi : les ouvrir compterait de faux clics)."""
import csv, datetime, io, json, os, re, sys, urllib.parse, urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

SRC = Path(__file__).resolve().parent
DATA = SRC / "data.json"
LOCAL = SRC / "effinity.local.json"
M = "PC-Portable.net"


def flux_url():
    url = os.environ.get("PCPORTABLE_URL")
    if not url and LOCAL.exists():
        url = json.loads(LOCAL.read_text(encoding="utf-8")).get("url_pc_portable")
    if not url:
        sys.exit("Adresse du flux introuvable : variable PCPORTABLE_URL ou clé url_pc_portable de _source/effinity.local.json")
    return url


def lire_flux(url=None, fichier=None):
    if fichier:
        brut = Path(fichier).read_text(encoding="utf-8-sig")
    else:
        req = urllib.request.Request(url or flux_url(), headers={"User-Agent": "top10geek-effinity/1.0"})
        brut = urllib.request.urlopen(req, timeout=120).read().decode("utf-8-sig")
    csv.field_size_limit(10 ** 9)
    lignes = list(csv.DictReader(io.StringIO(brut), delimiter=";"))
    if len(lignes) < 200 or "link" not in lignes[0]:
        sys.exit(f"Flux anormal ({len(lignes)} lignes) : rien n'est modifié")
    return {x["id"]: x for x in lignes if x.get("id")}


def _nb(t):
    try:
        return float(str(t).replace(",", ".").split()[0])
    except (ValueError, IndexError):
        return None


def ram(titre):
    m = re.search(r"RAM\s*(\d+)\s*G[Oo]|(\d+)\s*G[Oo]\s*RAM", titre, re.I)
    return int(m.group(1) or m.group(2)) if m else None


def cfg(titre, lien=""):
    """Configuration lisible tirée du titre de l'annonce : « Core i5 · 16 Go · SSD 250 Go · Windows 11 · grade B ».
    Certains titres du flux sont tronqués : l'adresse de la fiche (qui répète la configuration) complète le texte."""
    t = re.sub(r"\s+", " ", titre)
    if lien:
        slug = urllib.parse.unquote(lien.split("url=")[-1]).rsplit("/", 1)[-1].replace(".html", "").replace("-", " ")
        t = t + " " + slug
    out = []
    m = re.search(r"\b(I[3579])\b|CORE[- ]?(I[3579])|RYZEN [357]", t, re.I)
    if m:
        out.append(("Core " + (m.group(1) or m.group(2)).lower()) if (m.group(1) or m.group(2)) else m.group(0).title())
    r = ram(t)
    if r:
        out.append(f"{r} Go")
    s = re.search(r"SSD\s*(\d+)\s*(G[Oo]|T[Oo])", t, re.I) or re.search(r"(\d+)\s*(G[Oo]|T[Oo])\s*SSD", t, re.I)
    if s:
        n, u = s.group(1), s.group(2)
        out.append(f"SSD {n} {'To' if u.upper() == 'TO' else 'Go'}")
    w = re.search(r"WIN(?:DOWS)?\s*(10|11)", t, re.I)
    if w:
        out.append(f"Windows {w.group(1)}")
    if re.search(r"GRADE B", t, re.I):
        out.append("grade B")
    out.append("reconditionné")
    return " · ".join(out)


def nom(titre):
    return re.sub(r"\s+", " ", titre).strip(" -–")


def candidates(flux, fl):
    pat, non = re.compile(fl["re"], re.I), re.compile(fl.get("non", "$^"), re.I)
    res = []
    for x in flux.values():
        t = x["title"]
        if pat.search(t) and not non.search(t) and int(x.get("stock") or 0) > 0 and (ram(t) or 0) >= 8 and _nb(x["price"]):
            res.append(x)
    # Windows 11 d'abord (Windows 10 n'est plus pris en charge depuis octobre 2025), puis le prix le plus bas
    return sorted(res, key=lambda x: ("11" not in (cfg(x["title"], x["link"]).split("Windows ")[-1][:2] if "Windows " in cfg(x["title"], x["link"]) else ""), _nb(x["price"]), -int(x.get("stock") or 0)))


def offre(x, today):
    return dict(m=M, price=_nb(x["price"]), url=x["link"], name=nom(x["title"]), cfg=cfg(x["title"], x["link"]), ppid=x["id"], releve=today)


def rafraichir(data, flux, catalogue, today=None, log=print):
    """Met à jour (ou crée) l'offre PC-Portable.net de chaque produit du catalogue. Retourne le nombre de changements."""
    today = today or datetime.datetime.now(ZoneInfo("Europe/Paris")).date().isoformat()
    n = 0
    for pid, it in catalogue.items():
        d = data["items"].get(pid)
        if not d:
            continue
        fl = it["flux"]
        ancienne = next((o for o in d["offers"] if o["m"] == M), None)
        ppid = (ancienne or {}).get("ppid") or fl["ppid"]
        x = flux.get(ppid)
        if not (x and int(x.get("stock") or 0) > 0 and _nb(x["price"])):
            c = candidates(flux, fl)
            x = c[0] if c else None
            if x:
                log(f"  {pid}: annonce {ppid} absente, remplacée par {x['id']} ({x['title'][:60]}) à {x['price']} €")
        if x:
            nouvelle = offre(x, today)
            if ancienne != nouvelle:
                n += 1
                if ancienne:
                    log(f"  {pid}: {ancienne['price']} -> {nouvelle['price']} € ({nouvelle['cfg']})")
                else:
                    log(f"  {pid}: offre créée à {nouvelle['price']} € ({nouvelle['cfg']})")
            if ancienne:
                ancienne.clear(); ancienne.update(nouvelle)
            else:
                d["offers"].append(nouvelle)
        elif ancienne and ancienne.get("dispo", True):
            ancienne["dispo"] = False; ancienne["releve"] = today; n += 1
            log(f"  {pid}: plus aucune annonce en stock -> offre masquée (à remplacer ou retirer, décision de Matthieu)")
        en_vente = [o["price"] for o in d["offers"] if o.get("dispo", True)]
        if en_vente:
            d["prix"] = min(en_vente)
    return n


if __name__ == "__main__":
    sys.path.insert(0, str(SRC))
    from catalog_reconditionnes import RECO
    args = sys.argv[1:]
    fichier = args[args.index("--fichier") + 1] if "--fichier" in args else None
    flux = lire_flux(fichier=fichier)
    data = json.loads(DATA.read_text(encoding="utf-8"))
    n = rafraichir(data, flux, RECO)
    print(n, "changement(s)")
    if "--apply" in args:
        data["familles"].setdefault("portable", {})
        DATA.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
        print("data.json mis à jour")
