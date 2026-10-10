# -*- coding: utf-8 -*-
"""Lecture des tests presse avec Crawl4AI (mise à jour hebdomadaire). Ne modifie JAMAIS data.json.

Installation (une fois) :  pip install crawl4ai  &&  crawl4ai-setup

  python3 _source/presse_crawl.py verifier --famille ecran [--top 2] [--ids a,b]
      Relit les tests presse déjà cités pour les N produits les mieux classés de chaque usage de la rubrique et signale :
      liens morts, pages bloquées, notes différentes de celles du site (écart), notes retrouvées pour un test cité « sans note ».
      Rapport : _source/data/presse_rapport.json (+ résumé à l'écran).

  python3 _source/presse_crawl.py appliquer _source/data/presse_rapport.json [--apply]
      Reporte les notes déclarées en JSON-LD (écarts et notes retrouvées) dans data.json et dans catalog_ecrans.py /
      catalog_imprimantes.py ; chaque note corrigée garde « avant » et « corrige » (date). Sans --apply : aperçu.

  python3 _source/presse_crawl.py lire URL [URL…] --id <produit>
      Lit de nouvelles pages de test (URL trouvées par recherche web) et prépare un brouillon pour ajout_tests.py :
      _source/data/nouveaux_tests_brouillon.json  (média, date, note sur 10 si elle est lisible dans les données structurées de la page).
      Puis : python3 _source/ajout_tests.py _source/data/nouveaux_tests_brouillon.json   (aperçu), puis --apply.

Règles : jamais de note inventée (une note n'est reprise automatiquement que si la page la déclare en JSON-LD ; une note lue dans le
texte est seulement suggérée, à vérifier) ; robots.txt respecté ; un captcha ou un blocage n'est ni résolu ni contourné : la page est
signalée « bloquée » et le site concerné est laissé de côté pour la suite de la passe ; 6 sites en parallèle au plus, pages d'un même site l'une après l'autre avec une pause.
Variable facultative C4_CDP_URL : se connecter à un Chrome déjà lancé (http://localhost:9222) au lieu du Chromium de Playwright."""
import argparse
import asyncio
import datetime
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlparse

SRC = Path(__file__).resolve().parent
DATA = SRC / "data.json"
SORTIE = SRC / "data"
FAMILLE_DE_CAT = lambda cat: "ecran" if cat.startswith("e-") else "imprimante" if cat.startswith("i-") else "bureau" if cat.startswith("d-") else "portable"
BLOQUE = re.compile(r"captcha|are you a robot|access denied|just a moment|verify you are human|cf-chl|attention required|unusual traffic", re.I)
SANS_NOTE = {"RTINGS", "Test-Achats", "Que Choisir", "Which?", "Tænk", "Choice"}   # notes réservées aux abonnés (cf. CLAUDE.md)


# ------------------------------------------------------------------ données du site
def charger():
    return json.loads(DATA.read_text(encoding="utf-8"))


def rank_key(it):
    pr = it["press"]
    top = 0 if it["badge"] == "Le choix de la bande" else 1
    return (top, 0 if pr["avg"] is not None else 1, -(pr["avg"] or 0), -(pr["n"] if pr["avg"] is not None else pr["tests"]),
            float(it.get("prix") or 0))


def meilleurs(d, famille, par_usage, ids=None):
    """Les `par_usage` produits les mieux classés de chaque usage de la rubrique (même classement que le site)."""
    if ids:
        return [i for i in ids if i in d["items"]]
    cats = defaultdict(list)
    for pid, it in d["items"].items():
        if FAMILLE_DE_CAT(it["cat"]) == famille:
            cats[it["cat"]].append((rank_key(it), pid))
    return [pid for lst in cats.values() for _, pid in sorted(lst)[:par_usage]]


def medias_par_hote(d):
    """hôte -> nom du média, appris des tests déjà présents dans data.json."""
    c = defaultdict(Counter)
    for it in d["items"].values():
        for n in it["press"]["notes"]:
            h = urlparse(n.get("url") or "").netloc.lower().removeprefix("www.")
            if h:
                c[h][n["src"]] += 1
    return {h: cnt.most_common(1)[0][0] for h, cnt in c.items()}


# ------------------------------------------------------------------ extraction de la note
def _noeuds(x):
    if isinstance(x, list):
        for y in x:
            yield from _noeuds(y)
    elif isinstance(x, dict):
        yield x
        for v in x.values():
            if isinstance(v, (dict, list)):
                yield from _noeuds(v)


def _num(v):
    try:
        return float(str(v).replace(",", ".").strip())
    except ValueError:
        return None


def note_jsonld(html):
    """Note de la rédaction déclarée par la page (reviewRating d'un Review/Product), ramenée sur 10. Jamais aggregateRating (avis lecteurs).
    Une page qui déclare plusieurs notes différentes (comparatif, « meilleurs … ») est ambiguë : aucune note n'est reprise."""
    trouvees = []
    for bloc in re.findall(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', html or "", re.S | re.I):
        try:
            j = json.loads(bloc.strip())
        except ValueError:
            continue
        for nd in _noeuds(j):
            rr = nd.get("reviewRating")
            if isinstance(rr, list):
                rr = rr[0] if rr else None
            if not isinstance(rr, dict):
                continue
            v, best = _num(rr.get("ratingValue")), _num(rr.get("bestRating"))
            if v is None or best is None or best <= 0:
                continue                      # sans échelle explicite : ambigu, on ne devine pas
            if 0 <= v <= best:
                trouvees.append((round(v / best * 10, 2), f"JSON-LD reviewRating {rr.get('ratingValue')}/{rr.get('bestRating')}"))
    if not trouvees:
        return None, None
    if len({t[0] for t in trouvees}) > 1:
        return None, "ambigu"
    return trouvees[0]


def note_texte(md):
    """Note repérée dans le texte (« 8/10 », « 4/5 », « 87 % ») près d'un mot-clé : SEULEMENT suggérée, à vérifier."""
    md = re.sub(r"\]\(https?://[^)]*\)|https?://\S+", "", md or "")          # sans les adresses (ex. .../2/5 d'une URL)
    m = re.search(r"(?i)\b(?:note|score|verdict|rating|notre avis)\b[^\n]{0,40}?(\d{1,3}(?:[.,]\d)?)\s*(?:/|sur|out of)\s*(10|5|100)\b", md)
    if m:
        v, b = _num(m.group(1)), _num(m.group(2))
        if v is not None and 0 <= v <= b:
            return round(v / b * 10, 2), f"texte « {m.group(0).strip()[:70]} »"
    return None, None


def date_page(html):
    m = re.search(r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})', html or "") or re.search(
        r'property=["\']article:published_time["\'][^>]*content=["\'](\d{4}-\d{2}-\d{2})', html or "")
    return m.group(1) if m else ""


def titre_page(r):
    md = getattr(r, "metadata", None) or {}
    return (md.get("title") or "").strip()


# ------------------------------------------------------------------ crawl
async def lire_pages(urls):
    """-> {url: dict(statut, http, score, methode, score_texte, date, titre)} ; aucune exception ne remonte."""
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
    cdp = os.environ.get("C4_CDP_URL")
    bc = BrowserConfig(cdp_url=cdp, verbose=False) if cdp else BrowserConfig(headless=True, verbose=False)
    cfg = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, page_timeout=45000, wait_until="domcontentloaded", check_robots_txt=True, verbose=False)
    sortie, blocs = {}, Counter()
    par_hote = defaultdict(list)
    for u in urls:
        par_hote[urlparse(u).netloc].append(u)
    async with AsyncWebCrawler(config=bc) as crawler:
        async def hote(h, lst, sem):
            async with sem:
                for u in lst:
                    if blocs[h] >= 2:
                        sortie[u] = dict(statut="ignoré (site bloquant)", http=None)
                        continue
                    try:
                        r = await crawler.arun(u, config=cfg)
                    except Exception as e:                  # noqa: BLE001
                        sortie[u] = dict(statut=f"erreur : {str(e)[:80]}", http=None)
                        continue
                    sortie[u] = analyser(r)
                    if sortie[u]["statut"].startswith("erreur"):          # seconde tentative, une seule
                        await asyncio.sleep(3)
                        try:
                            sortie[u] = analyser(await crawler.arun(u, config=cfg))
                        except Exception:                                 # noqa: BLE001
                            pass
                    if sortie[u]["statut"] == "bloqué":
                        blocs[h] += 1
                    await asyncio.sleep(1.2)                # politesse
        sem = asyncio.Semaphore(6)           # 6 sites en parallèle, pages d'un même site l'une après l'autre
        await asyncio.gather(*(hote(h, lst, sem) for h, lst in par_hote.items()))
    return sortie


def analyser(r):
    code = getattr(r, "status_code", None)
    html = getattr(r, "html", "") or ""
    md = str(getattr(r, "markdown", "") or "")
    if code in (404, 410):
        return dict(statut="lien mort", http=code)
    if code in (401, 403, 429) or (BLOQUE.search(md[:3000]) and len(md) < 4000):
        return dict(statut="bloqué", http=code)
    if not getattr(r, "success", False) or not html:
        return dict(statut=f"erreur : {(getattr(r, 'error_message', '') or '')[:80]}", http=code)
    s, meth = note_jsonld(html)
    st, mt = (None, None) if s is not None else note_texte(md)
    return dict(statut="ok", http=code, score=s, methode=meth, score_texte=st, methode_texte=mt, date=date_page(html), titre=titre_page(r))


# ------------------------------------------------------------------ commandes
def cmd_verifier(a):
    d = charger()
    pids = meilleurs(d, a.famille, a.top, a.ids.split(",") if a.ids else None)
    seules = set(Path(a.urls).read_text(encoding="utf-8").split()) if a.urls else None
    if seules:
        pids = [pid for pid, it in d["items"].items() if any(n.get("url") in seules for n in it["press"]["notes"])]
    taches = {}                                             # url -> [(pid, note)]
    for pid in pids:
        for n in d["items"][pid]["press"]["notes"]:
            u = n.get("url") or ""
            if u.startswith("http") and (seules is None or u in seules):
                taches.setdefault(u, []).append((pid, n))
    print(f"{len(pids)} produit(s), {len(taches)} page(s) de test à relire…")
    res = asyncio.run(lire_pages(list(taches)))
    rapport, compte = [], Counter()
    for u, lst in taches.items():
        r = res.get(u, dict(statut="non lu"))
        for pid, n in lst:
            stocke = n.get("score")
            etat = r["statut"]
            detail = ""
            if etat == "ok":
                if n["src"] in SANS_NOTE:
                    etat = "ok (sans note par règle)"
                elif r.get("score") is not None and stocke is not None:
                    if abs(r["score"] - stocke) > 0.15:
                        etat, detail = "ÉCART", f"site {stocke:.1f} · page {r['score']:.1f} ({r['methode']})"
                    else:
                        etat = "ok"
                elif r.get("score") is not None and stocke is None:
                    etat, detail = "NOTE TROUVÉE", f"page {r['score']:.1f} ({r['methode']})"
                elif r.get("score_texte") is not None and stocke is not None and abs(r["score_texte"] - stocke) > 0.15:
                    etat, detail = "à vérifier", f"site {stocke:.1f} · texte {r['score_texte']:.1f} ({r['methode_texte']})"
                else:
                    etat = "ok (note non lisible automatiquement)" if stocke is not None else "ok"
            compte[etat.split(" (")[0]] += 1
            rapport.append(dict(id=pid, media=n["src"], url=u, note_site=stocke, etat=etat, detail=detail, http=r.get("http"),
                                note_page=r.get("score"), methode=r.get("methode")))
    SORTIE.mkdir(exist_ok=True)
    out = SORTIE / (a.sortie or "presse_rapport.json")
    out.write_text(json.dumps(dict(date=datetime.datetime.now().isoformat(timespec="seconds"), famille=a.famille, lignes=rapport),
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nBilan :", ", ".join(f"{k} {v}" for k, v in compte.most_common()))
    for x in rapport:
        if x["etat"] not in ("ok", "ok (sans note par règle)", "ok (note non lisible automatiquement)"):
            print(f"  {x['etat']:14s} {x['id']:30s} {x['media']:18s} {x['detail']}  {x['url'] if x['etat'] in ('lien mort', 'bloqué') else ''}")
    print(f"\nRapport complet : {out.relative_to(SRC.parent)} (aucune donnée du site modifiée)")


def cmd_lire(a):
    d = charger()
    hotes = medias_par_hote(d)
    res = asyncio.run(lire_pages(a.urls))
    brouillon = []
    for u in a.urls:
        r = res.get(u, dict(statut="non lu"))
        h = urlparse(u).netloc.lower().removeprefix("www.")
        e = dict(id=a.id, src=hotes.get(h, h), score=r.get("score"), url=u, date=r.get("date", ""))
        if r["statut"] != "ok":
            print(f"!! {u} : {r['statut']} — non repris")
            continue
        if r.get("score") is None and r.get("score_texte") is not None:
            e["score_a_verifier"] = f"{r['score_texte']:.1f} — {r['methode_texte']}"
        e["_verif"] = dict(titre=r.get("titre", ""), methode=r.get("methode") or "aucune note déclarée par la page")
        brouillon.append(e)
        print(f"{e['src']:20s} note={e['score'] if e['score'] is not None else '—'}  {e['date']}  {r.get('titre', '')[:70]}")
        if "score_a_verifier" in e:
            print(f"{'':20s} (à vérifier à la main : {e['score_a_verifier']})")
    SORTIE.mkdir(exist_ok=True)
    out = SORTIE / "nouveaux_tests_brouillon.json"
    out.write_text(json.dumps(brouillon, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(brouillon)} entrée(s) -> {out.relative_to(SRC.parent)}. "
          f"Contrôler les notes puis : python3 _source/ajout_tests.py {out.relative_to(SRC.parent)}")


def recalc(pr):
    notes = pr["notes"]
    notes.sort(key=lambda n: (n["score"] is None, -(n["score"] or 0), n["src"]))
    scored = [n for n in notes if n["score"] is not None]
    pr.update(avg=(sum(n["score"] for n in scored) / len(scored)) if scored else None, n=len(scored), tests=len(notes))


CATALOGUES = {"ecran": SRC / "catalog_ecrans.py", "imprimante": SRC / "catalog_imprimantes.py"}


def cmd_appliquer(a):
    """Reporte dans data.json (et dans catalog_ecrans.py / catalog_imprimantes.py, pour que build_new.py ne les écrase pas)
    les notes que les pages déclarent elles-mêmes en JSON-LD : écarts avec le site et notes retrouvées pour des tests cités sans note."""
    d = charger()
    jour = datetime.datetime.now().strftime("%d/%m/%Y")
    lignes = [l for f in a.rapports for l in json.loads(Path(f).read_text(encoding="utf-8"))["lignes"]]
    sources = {k: v.read_text(encoding="utf-8") for k, v in CATALOGUES.items()}
    faits, touches, catal = 0, set(), Counter()
    for l in lignes:
        if l["etat"] not in ("ÉCART", "NOTE TROUVÉE") or l.get("note_page") is None or not str(l.get("methode", "")).startswith("JSON-LD"):
            continue
        it = d["items"].get(l["id"])
        n = next((x for x in (it or {}).get("press", {}).get("notes", []) if x.get("url") == l["url"]), None)
        if not n or n["src"] in SANS_NOTE:
            continue
        neuf = round(float(l["note_page"]), 1)
        if n["score"] is not None and abs(n["score"] - neuf) < 0.05:
            continue
        print(f"{'écart' if n['score'] is not None else 'note '} {l['id'][:30]:30s} {n['src'][:20]:20s} "
              f"{'—' if n['score'] is None else n['score']:>4} -> {neuf:<4} ({l['methode']})")
        n.update(avant=n["score"], score=neuf, corrige=jour)
        touches.add(l["id"]); faits += 1
        fam = FAMILLE_DE_CAT(it["cat"])
        if fam in sources:                                  # même correction dans le catalogue source
            motif = re.compile(r'(,\s*)(None|\d+(?:\.\d+)?)(\s*,\s*["\']' + re.escape(l["url"]) + r'["\'])')
            sources[fam], k = motif.subn(lambda m: f"{m.group(1)}{neuf}{m.group(3)}", sources[fam])
            catal[fam] += k
    avant = {pid: d["items"][pid]["press"]["avg"] for pid in touches}
    for pid in touches:
        recalc(d["items"][pid]["press"])
    print(f"\n{faits} note(s) corrigée(s) sur {len(touches)} produit(s) ; catalogues : {dict(catal)}")
    for pid in sorted(touches, key=lambda p: (d["items"][p]["press"]["avg"] or 0) - (avant[p] or 0)):
        av, ap = avant[pid], d["items"][pid]["press"]["avg"]
        print(f"   {d['items'][pid]['short'][:34]:34s} {'—' if av is None else f'{av:.2f}':>5} -> {ap:.2f}")
    if a.apply and faits:
        DATA.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        for fam, txt in sources.items():
            CATALOGUES[fam].write_text(txt, encoding="utf-8")
        print("data.json et catalogues mis à jour. Reste : python3 _source/gen10.py")
    elif faits:
        print("Aperçu seulement : relancer avec --apply.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    v = sp.add_parser("verifier")
    v.add_argument("--famille", choices=["portable", "bureau", "ecran", "imprimante"], required=True)
    v.add_argument("--top", type=int, default=2, help="produits les mieux classés par usage (défaut 2, soit 10 par rubrique)")
    v.add_argument("--ids", help="liste d'identifiants séparés par des virgules (remplace le classement)")
    v.add_argument("--urls", help="fichier texte : ne relire que ces adresses (une par ligne)")
    v.add_argument("--sortie", help="nom du rapport dans _source/data/ (défaut presse_rapport.json)")
    ap_ = sp.add_parser("appliquer")
    ap_.add_argument("rapports", nargs="+", help="rapports produits par verifier")
    ap_.add_argument("--apply", action="store_true")
    l = sp.add_parser("lire")
    l.add_argument("urls", nargs="+")
    l.add_argument("--id", required=True, help="identifiant du produit dans data.json")
    a = ap.parse_args()
    if a.cmd == "verifier":
        cmd_verifier(a)
    elif a.cmd == "appliquer":
        cmd_appliquer(a)
    else:
        if a.id not in charger()["items"]:
            sys.exit(f"Produit inconnu : {a.id}")
        cmd_lire(a)


if __name__ == "__main__":
    main()
