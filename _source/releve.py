#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Relevé de prix local de top10geek.fr (Playwright, sans service tiers).

À lancer sur un ordinateur en France (IP française => prix Amazon TTC en .fr).

  python3 _source/releve.py                 # relève tout, écrit _source/data/releve.json
  python3 _source/releve.py --apply         # idem + met à jour data.json (prix + date)
  python3 _source/releve.py --only Amazon --limit 5 --headed --debug   # essai
  python3 _source/releve.py --only Amazon,Geekom --apply   # relevé complet de certains marchands
  python3 _source/releve.py --famille ecran --only Amazon --apply   # une seule rubrique
  python3 _source/releve.py --manuel _source/data/manuel.json --apply
        # prix lus à la main dans un navigateur : [{"id": ..., "j": ..., "price": ...}, ...]

Chaque marchand a sa propre date de relevé (`dates` dans data.json) : elle n'avance
que si au moins la moitié de ses offres ont été relues.

Avec --apply : met à jour le `price` et la disponibilité (`dispo`) des offres lues, le prix
indicatif de chaque produit (`prix`, le plus bas des offres en vente), `prix_date` et `date`.
Le site (gen10.py) n'affiche que ce prix indicatif et les liens des offres en vente.
Règles : jamais de prix inventé ; en cas de doute l'ancien prix est conservé.
"""
import argparse
import datetime
import json
import random
import re
import sys
import unicodedata
from pathlib import Path
from zoneinfo import ZoneInfo

SRC = Path(__file__).resolve().parent
DATA = SRC / "data.json"
OUT_DIR = SRC / "data"            # dossier ignoré par git
PROFILE = Path.home() / ".cache" / "top10geek-releve"   # profil navigateur (cookies)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
SEUIL_ECART = 0.30
SEUIL_PUBLICATION = 0.5

# rubriques du site, d'après le préfixe de la catégorie du produit
FAMILLES = {
    "portable": lambda c: "-" not in c,
    "bureau": lambda c: c.startswith("d-"),
    "ecran": lambda c: c.startswith("e-"),
    "imprimante": lambda c: c.startswith("i-"),
}

# statuts : ok | indispo | marketplace | autre_produit | captcha | echec


# ---------------------------------------------------------------- utilitaires
def parse_prix(txt):
    """'1 299,99 €' / '1.299,99' / '1299.99' / 449 -> float, sinon None."""
    if txt is None:
        return None
    if isinstance(txt, (int, float)):
        return float(txt) if txt > 0 else None
    s = unicodedata.normalize("NFKC", str(txt))
    m = re.search(r"\d[\d\s.,]*", s)
    if not m:
        return None
    s = re.sub(r"\s", "", m.group(0)).rstrip(".,")
    if "," in s and "." in s:                      # 1.299,99 ou 1,299.99
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".")
    elif s.count(".") > 1 or re.fullmatch(r"\d{1,3}\.\d{3}", s):
        s = s.replace(".", "")                     # 1.299 = séparateur de milliers
    try:
        v = float(s)
    except ValueError:
        return None
    return round(v, 2) if v > 0 else None


def jetons(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return {t for t in re.findall(r"[a-z0-9]+", s) if len(t) >= 3}


def meme_produit(nom, titre):
    """Recouvrement grossier entre le nom stocké et le titre de la page."""
    a, b = jetons(nom), jetons(titre)
    if not a or not b:
        return None                                # indéterminé
    return len(a & b) / len(a) >= 0.3


def txt(page, sel):
    try:
        loc = page.locator(sel)
        if loc.count():
            return (loc.first.text_content(timeout=2000) or "").strip()
    except Exception:
        pass
    return ""


def produits_ldjson(page):
    out = []
    try:
        blocs = page.locator('script[type="application/ld+json"]').all_text_contents()
    except Exception:
        return out
    for b in blocs:
        try:
            j = json.loads(b)
        except Exception:
            continue
        pile = j if isinstance(j, list) else [j]
        while pile:
            x = pile.pop()
            if isinstance(x, list):
                pile.extend(x)
            elif isinstance(x, dict):
                if "@graph" in x:
                    pile.append(x["@graph"])
                t = x.get("@type")
                if t in ("Product", "ProductGroup") or (isinstance(t, list) and "Product" in t):
                    out.append(x)
                    if x.get("hasVariant"):
                        pile.append(x["hasVariant"])
    return out


def offres_ld(prod):
    o = prod.get("offers")
    if not o:
        return []
    o = o if isinstance(o, list) else [o]
    res = []
    for x in o:
        if not isinstance(x, dict):
            continue
        if x.get("@type") == "AggregateOffer":
            res.append({"price": parse_prix(x.get("lowPrice") or x.get("price")),
                        "dispo": str(x.get("availability", "")), "etat": "", "vendeur": ""})
            for y in (x.get("offers") or []):
                if isinstance(y, dict):
                    o.append(y)
            continue
        vend = x.get("seller")
        vend = vend.get("name", "") if isinstance(vend, dict) else (vend or "")
        res.append({"price": parse_prix(x.get("price")),
                    "dispo": str(x.get("availability", "")),
                    "etat": str(x.get("itemCondition", "")),
                    "vendeur": str(vend)})
    return [r for r in res if r["price"]]


def var_page(html, cle):
    """Valeur d'une variable de data layer : cle":"valeur" / cle: 'valeur'."""
    m = re.search(r'["\']?' + re.escape(cle) + r'["\']?\s*[:=]\s*["\']([^"\']*)["\']', html)
    return m.group(1) if m else ""


# ------------------------------------------------------------------ marchands
def lire_amazon(page, html):
    if re.search(r"captchacharacters|validateCaptcha|/errors/validateCaptcha", html) \
            or "Saisissez les caractères" in html:
        return {"status": "captcha", "note": "captcha Amazon"}
    titre = txt(page, "#productTitle")
    if not titre:
        return {"status": "echec", "note": "titre introuvable (page inattendue)"}
    dispo = txt(page, "#availability")
    bloc = " ".join(txt(page, s) for s in (
        "#offer-display-features", "#merchantInfoFeature_feature_div", "#merchant-info",
        "#tabular-buybox", "#shipsFromSoldByInsideBuyBox_feature_div",
        "#fulfillerInfoFeature_feature_div", "#sellerProfileTriggerId"))
    # prix de l'offre neuve principale uniquement (pas l'encart occasion)
    prix = None
    for sel in ("#newAccordionRow_0 .a-price .a-offscreen", "#newAccordionRow .a-price .a-offscreen",
                "#corePriceDisplay_desktop_feature_div .priceToPay .a-offscreen",
                "#corePriceDisplay_desktop_feature_div .a-price .a-offscreen",
                "#corePrice_feature_div .a-price .a-offscreen",
                "#apex_desktop .a-price .a-offscreen",
                "#price_inside_buybox", "#priceblock_ourprice"):
        prix = parse_prix(txt(page, sel))
        if prix:
            break
    if not prix:
        e, f = txt(page, "#corePriceDisplay_desktop_feature_div .a-price-whole"), \
            txt(page, "#corePriceDisplay_desktop_feature_div .a-price-fraction")
        if e:
            prix = parse_prix(re.sub(r"\D", "", e) + "," + (re.sub(r"\D", "", f) or "00"))
    achetable = page.locator("#add-to-cart-button, #buy-now-button").count() > 0
    r = {"titre": titre, "vendeur": re.sub(r"\s+", " ", bloc)[:120], "dispo": dispo[:80]}
    if re.search(r"indisponible|en rupture", dispo, re.I) or not achetable or not prix:
        return dict(r, status="indispo", note="pas d'offre neuve achetable", prix_vu=prix)
    # « Expéditeur / Vendeur Amazon », « Expédié par Amazon », « Vendu par Amazon »
    # (le mot Amazon seul ne suffit pas : il figure aussi dans les mentions de paiement et de retours)
    if not re.search(r"(Exp[ée]diteur(\s*/\s*Vendeur)?|Vendeur|Exp[ée]di[ée] par|Vendu par)\s+Amazon", bloc, re.I):
        return dict(r, status="marketplace", note="ni vendu ni expédié par Amazon", prix_vu=prix)
    if re.search(r"hors TVA|excl\. VAT|HT\b", txt(page, "#corePriceDisplay_desktop_feature_div")):
        return dict(r, status="echec", note="prix affiché HT", prix_vu=prix)
    return dict(r, status="ok", price=prix)


def lire_darty(page, html):
    if "Maintenance" in (page.title() or "") or len(html) < 20000:
        return {"status": "echec", "note": "page de blocage/maintenance Darty"}
    titre = txt(page, "h1")
    type_vendeur = var_page(html, "product_seller_type").lower()
    etat = var_page(html, "product_state").lower()
    vendeur = var_page(html, "product_seller")
    prix = parse_prix(var_page(html, "product_unitprice_ttc"))
    dispo = var_page(html, "product_availability_code")
    offres = [o for p in produits_ldjson(page) for o in offres_ld(p)]
    if not prix and offres:
        prix = offres[0]["price"]
        etat = etat or offres[0]["etat"].lower()
        vendeur = vendeur or offres[0]["vendeur"]
        dispo = dispo or offres[0]["dispo"]
    if not prix:
        prix = parse_prix(txt(page, ".product-price__price, .darty_prix, [data-automation-id='product_price']"))
    r = {"titre": titre, "vendeur": vendeur or type_vendeur, "dispo": dispo, "etat": etat}
    if not prix:
        return dict(r, status="indispo" if titre else "echec", note="aucun prix lisible")
    if type_vendeur == "marketplace" or re.search(r"recondition|occasion|used", etat) \
            or (vendeur and "darty" not in vendeur.lower()):
        return dict(r, status="marketplace", note="offre marketplace ou reconditionnée", prix_vu=prix)
    if re.search(r"outofstock|indisponible|epuise|unavailable", dispo, re.I):
        return dict(r, status="indispo", note="indisponible", prix_vu=prix)
    if not type_vendeur and not vendeur:
        return dict(r, status="echec", note="vendeur non identifié (sélecteurs à revoir)", prix_vu=prix)
    return dict(r, status="ok", price=prix)


def lire_generique(page, html, plus_bas=False):
    """Geekom (prix le plus bas des configurations) et Acer Store (prix TTC affiché)."""
    prods = produits_ldjson(page)
    titre = txt(page, "h1") or (prods[0].get("name", "") if prods else "")
    offres = [o for p in prods for o in offres_ld(p)]
    if not offres:
        meta = page.locator('meta[property="product:price:amount"], meta[itemprop="price"]')
        if meta.count():
            p = parse_prix(meta.first.get_attribute("content"))
            if p:
                offres = [{"price": p, "dispo": "", "etat": "", "vendeur": ""}]
    if not offres:
        return {"status": "echec", "titre": titre, "note": "aucun prix structuré dans la page"}
    dispos = [o for o in offres if not re.search(r"OutOfStock|Discontinued|SoldOut", o["dispo"])]
    if not dispos:
        return {"status": "indispo", "titre": titre, "note": "en rupture",
                "prix_vu": min(o["price"] for o in offres)}
    prix = min(o["price"] for o in dispos) if plus_bas else dispos[0]["price"]
    return {"status": "ok", "titre": titre, "price": prix, "dispo": dispos[0]["dispo"][-20:]}


def lire(page, offre, debug_dir=None, idx=0):
    url = offre["url"]
    if offre["m"] == "Amazon":
        url = re.sub(r"[?&]tag=[^&]*", "", url)      # lecture sans le tag (URL stockée intacte)
    try:
        rep = page.goto(url, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(random.randint(1800, 3200))
        html = page.content()
    except Exception as e:
        return {"status": "echec", "note": "chargement: " + str(e).splitlines()[0][:100]}
    if debug_dir:
        (debug_dir / f"{idx:03d}_{offre['m'].replace(' ', '')}.html").write_text(html, encoding="utf-8")
    code = rep.status if rep else 0
    if code >= 400 and offre["m"] != "Amazon":
        return {"status": "echec", "note": f"HTTP {code}"}
    if code == 404:
        return {"status": "indispo", "note": "HTTP 404"}
    try:
        if offre["m"] == "Amazon":
            r = lire_amazon(page, html)
        elif offre["m"] == "Darty":
            r = lire_darty(page, html)
        else:
            r = lire_generique(page, html, plus_bas=(offre["m"] == "Geekom"))
    except Exception as e:
        return {"status": "echec", "note": "analyse: " + str(e).splitlines()[0][:100]}
    if r["status"] == "ok" and meme_produit(offre["name"], r.get("titre", "")) is False:
        r = dict(r, status="autre_produit", note="le titre de la page ne correspond pas", prix_vu=r.pop("price"))
    return r


# ------------------------------------------------------------------ programme
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="met à jour data.json si ≥ 50 %% des offres sont relues")
    ap.add_argument("--only", help="marchand(s) séparés par des virgules (Amazon, Darty, Geekom, 'Acer Store')")
    ap.add_argument("--famille", choices=sorted(FAMILLES), help="limite le relevé à une rubrique "
                    "(portable, bureau, ecran, imprimante)")
    ap.add_argument("--duree", type=int, help="s'arrête proprement après N secondes ; relancer la même commande "
                    "pour reprendre (les lectures du jour sont gardées dans _source/data/reprise.json)")
    ap.add_argument("--manuel", help="fichier JSON de prix lus à la main (aucune page n'est chargée)")
    ap.add_argument("--limit", type=int, help="nombre maximum d'offres (essais)")
    ap.add_argument("--headed", action="store_true", help="navigateur visible (utile pour résoudre un captcha)")
    ap.add_argument("--debug", action="store_true", help="enregistre le HTML de chaque page dans _source/data/debug/")
    ap.add_argument("--channel", default=None, help="navigateur installé à utiliser, ex. chrome ou msedge")
    a = ap.parse_args()

    if a.manuel:
        import contextlib
        sync_playwright = lambda: contextlib.nullcontext()
    else:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            sys.exit("Playwright manquant : pip install playwright && playwright install chromium")

    brut = DATA.read_text(encoding="utf-8")
    d = json.loads(brut)
    offres = [(k, j, o) for k, it in d["items"].items() for j, o in enumerate(it["offers"])]
    total = len(offres)
    only = [m.strip().lower() for m in a.only.split(",")] if a.only else None
    cible = [x for x in offres if not only or x[2]["m"].lower() in only]
    if a.famille:
        cible = [x for x in cible if FAMILLES[a.famille](d["items"][x[0]]["cat"])]
    manuel = None
    if a.manuel:
        manuel = {(x["id"], x["j"]): x for x in json.loads(Path(a.manuel).read_text(encoding="utf-8"))}
        cible = [x for x in offres if (x[0], x[1]) in manuel]
    if a.limit:
        cible = cible[:a.limit]
    partiel = bool(a.limit)                        # un essai --limit n'est jamais appliqué
    OUT_DIR.mkdir(exist_ok=True)
    debug_dir = None
    if a.debug:
        debug_dir = OUT_DIR / "debug"
        debug_dir.mkdir(exist_ok=True)

    import time
    debut = time.monotonic()
    jour = datetime.datetime.now(ZoneInfo("Europe/Paris")).strftime("%d/%m/%Y")
    f_reprise = OUT_DIR / "reprise.json"
    deja = {}
    if a.duree and f_reprise.exists():
        c = json.loads(f_reprise.read_text(encoding="utf-8"))
        if c.get("date") == jour:
            deja = {k: r for k, r in c["res"].items() if r["status"] not in ("echec", "captcha")}
    restant = 0
    res = []
    for k, j, o in (cible if manuel else []):
        x = manuel[(k, j)]
        prix = parse_prix(x.get("price"))
        r = {"status": "ok", "price": prix, "note": "lecture manuelle"} if prix and x.get("status", "ok") == "ok" \
            else {"status": x.get("status") if x.get("status") not in (None, "ok") else "echec",
                  "note": x.get("note", "lecture manuelle")}
        if r["status"] == "ok" and abs(prix / o["price"] - 1) > SEUIL_ECART and not x.get("confirme"):
            r = {"status": "echec", "note": "écart > 30 % non confirmé (ajouter \"confirme\": true)", "prix_vu": prix}
        r.update(id=k, j=j, m=o["m"], ancien=o["price"], name=o["name"])
        res.append(r)
        print(f"[manuel] {o['m']:10s} {k:24s} {r['status']:13s} {o['price']} -> {r.get('price', '—')}  {r.get('note', '')}")
    with sync_playwright() as p:
        ctx = None if manuel else p.chromium.launch_persistent_context(
            str(PROFILE), headless=not a.headed, channel=a.channel,
            locale="fr-FR", timezone_id="Europe/Paris", user_agent=UA,
            viewport={"width": 1366, "height": 900},
            extra_http_headers={"Accept-Language": "fr-FR,fr;q=0.9"})
        page = None if manuel else (ctx.pages[0] if ctx.pages else ctx.new_page())
        for n, (k, j, o) in enumerate([] if manuel else cible, 1):
            if f"{k}|{j}" in deja:
                res.append(deja[f"{k}|{j}"])
                continue
            if a.duree and time.monotonic() - debut > a.duree:
                restant += 1
                continue
            r = lire(page, o, debug_dir, n)
            if r["status"] in ("echec", "captcha"):                 # seconde tentative
                if r["status"] == "captcha" and a.headed:
                    input("  Captcha : résolvez-le dans la fenêtre puis appuyez sur Entrée… ")
                page.wait_for_timeout(random.randint(4000, 7000))
                r = lire(page, o, debug_dir, n)
            if r["status"] == "ok" and abs(r["price"] / o["price"] - 1) > SEUIL_ECART:
                page.wait_for_timeout(random.randint(3000, 5000))   # écart > 30 % : relecture
                r2 = lire(page, o, debug_dir, n)
                if r2["status"] == "ok" and r2["price"] == r["price"]:
                    r["note"] = "écart > 30 % confirmé par deux lectures"
                else:
                    r = dict(r, status="echec", note="écart > 30 % non confirmé", prix_vu=r.pop("price"))
            r.update(id=k, j=j, m=o["m"], ancien=o["price"], name=o["name"])
            res.append(r)
            print(f"[{n:3d}/{len(cible)}] {o['m']:10s} {k:24s} {r['status']:13s} "
                  f"{o['price']} -> {r.get('price', '—')}  {r.get('note', '')}", flush=True)
            if a.duree:
                deja[f"{k}|{j}"] = r
                f_reprise.write_text(json.dumps({"date": jour, "res": deja}, ensure_ascii=False), encoding="utf-8")
            page.wait_for_timeout(random.randint(1500, 4000))       # rythme modéré
        if ctx:
            ctx.close()

    if restant:
        partiel = True
        print(f"\nINCOMPLET : {restant} offres restantes — relancer la même commande pour reprendre.")
    ok = [r for r in res if r["status"] == "ok"]
    modifs = [r for r in ok if r["price"] != r["ancien"]]
    bilan = {"date": jour, "total_offres": total, "ciblees": len(cible), "relues_ok": len(ok),
             "modifiees": len(modifs), "partiel": partiel, "applique": False, "resultats": res}

    print(f"\nRelevé du {jour} : {len(ok)}/{len(cible)} offres relues, {len(modifs)} prix modifiés.")
    par = {}
    for r in res:
        if r["status"] != "ok":
            par.setdefault(r["status"], []).append(f"{r['id']} ({r['m']})")
    for s, l in par.items():
        print(f"  {s} : {len(l)} — " + ", ".join(l[:8]) + (" …" if len(l) > 8 else ""))

    # un marchand est « relevé » si au moins la moitié de SES offres ont été relues
    tot_m, ok_m = {}, {}
    for _, _, o in (cible if a.famille else offres):   # avec --famille : seuil calculé sur la rubrique
        tot_m[o["m"]] = tot_m.get(o["m"], 0) + 1
    for r in ok:
        ok_m[r["m"]] = ok_m.get(r["m"], 0) + 1
    releves = [m for m in tot_m if ok_m.get(m, 0) >= SEUIL_PUBLICATION * tot_m[m]]
    bilan["marchands_releves"] = releves
    for m in sorted({r["m"] for r in res}):
        print(f"  {m} : {ok_m.get(m, 0)}/{tot_m[m]} offres relues" + ("" if m in releves else " — date NON avancée"))

    if a.apply:
        if partiel:
            print("--apply ignoré : essai partiel (--limit).")
        elif not ok:
            print("--apply refusé : aucune offre relue. data.json inchangé.")
        else:
            # Chaque prix réellement lu est appliqué ; la date d'un marchand n'avance qu'à 50 % de ses offres.
            for r in modifs:
                d["items"][r["id"]]["offers"][r["j"]]["price"] = r["price"]
            for r in res:                                   # disponibilité : pilote les liens affichés
                o = d["items"][r["id"]]["offers"][r["j"]]
                if r["status"] == "ok":
                    o.pop("dispo", None)
                elif r["status"] == "indispo":
                    o["dispo"] = False
            # prix indicatif de chaque produit : le plus bas des offres en vente
            for it in d["items"].values():
                enl = [o for o in it["offers"] if o.get("dispo", True)] or it["offers"]
                it["prix"] = min(o["price"] for o in enl)
            mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
                    "septembre", "octobre", "novembre", "décembre"]
            mois_txt = f"{mois[int(jour[3:5]) - 1]} {jour[6:]}"
            if a.manuel:
                pass                              # lecture manuelle : complète un relevé, ne date pas la rubrique
            elif a.famille:
                # date de la rubrique : n'avance que si au moins la moitié de ses offres ont été relues
                if len(ok) >= SEUIL_PUBLICATION * len(cible):
                    d.setdefault("familles", {})[a.famille] = {"date": jour, "prix_date": mois_txt,
                                                                "iso": jour[6:] + "-" + jour[3:5] + "-" + jour[:2]}
                else:
                    print(f"Date de la rubrique « {a.famille} » NON avancée ({len(ok)}/{len(cible)} offres relues).")
                fams = d.get("familles", {})
                if len(fams) == len(FAMILLES):    # mois affiché sur les pages multi-rubriques : le plus ancien
                    d["prix_date"] = min(fams.values(), key=lambda x: x["iso"])["prix_date"]
            else:
                d["prix_date"] = mois_txt
                for f in d.get("familles", {}):
                    d["familles"][f].update(date=jour, prix_date=mois_txt,
                                            iso=jour[6:] + "-" + jour[3:5] + "-" + jour[:2])
            dates = d.get("dates") or {m: d["date"] for m in tot_m}
            for m in releves:
                dates[m] = jour
            d["dates"] = {m: dates[m] for m in sorted(dates)}
            d["date"] = jour
            fin = "\n" if brut.endswith("\n") else ""
            DATA.write_text(json.dumps(d, ensure_ascii=False, indent=1) + fin, encoding="utf-8")
            bilan["applique"] = True
            print(f"data.json mis à jour ({len(modifs)} prix, date {jour}). "
                  "Reste : python3 _source/gen10.py puis commit.")
    (OUT_DIR / "releve.json").write_text(json.dumps(bilan, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Détail : {OUT_DIR / 'releve.json'}")
    return 0 if (partiel or ok) else 2


if __name__ == "__main__":
    sys.exit(main())
