# -*- coding: utf-8 -*-
"""Générateur d'épingles Pinterest (décision du 29/10/2026 : Pinterest x3 à x5).

Lit le site DÉJÀ GÉNÉRÉ (pages usage et fiches produit à la racine du dépôt), donc les classements, notes et prix des épingles
sont exactement ceux affichés sur le site au moment de la génération. Ne modifie ni data.json ni le générateur du site.

Sorties :
  assets/img/pins/<type>-<slug>.jpg   visuels 1000 x 1500 (publiés avec le site : Pinterest va les chercher en ligne)
  _com/pins-planning.csv              lignes à ajouter au Google Sheet « Top10Geek – Planning épingles Pinterest »
                                      colonnes : statut,titre,description,lien,image_url,tableau,board_id,type

Types : top3 (top 3 d'un usage), produit (fiche d'un produit), bf (top 3 Black Friday d'un usage), bf-conseils.
Usage : python3 _source/pins.py [--types top3,produit,bf,bf-conseils] [--max-produits 60] [--seulement-nouveaux]
Dépendances : Pillow, fonttools + brotli (conversion des polices woff2 en ttf, cache dans _source/.cache_pins/).
Règles : aucune donnée inventée (tout vient des pages du site), pas de logo ni de photo tierce, mention « prix indicatif ».
"""
import argparse
import csv
import html
import json
import pathlib
import re
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://top10geek.fr"
OUT_IMG = ROOT / "assets" / "img" / "pins"
OUT_CSV = ROOT / "_com" / "pins-planning.csv"
CACHE = pathlib.Path(__file__).resolve().parent / ".cache_pins"
BOARDS_JSON = pathlib.Path(__file__).resolve().parent / "pins_boards.json"   # {"nom du tableau": "id Pinterest"}
FALLBACK_BOARD = "Comparatifs high-tech"
W, H = 1000, 1500

BG = (81, 79, 56)
GREEN = (0, 255, 171)
MAGENTA = (255, 0, 200)
WHITE = (255, 255, 255)
CARD = (250, 250, 245)
INK = (30, 30, 25)
GREY = (110, 110, 100)
PILL = (6, 0, 0)

FAMILLES = {   # dossier -> (libellé, tableau Pinterest)
    "pc-portable": ("PC portables", "PC portables"),
    "ordinateur-de-bureau": ("PC de bureau", "PC de bureau et mini-PC"),
    "ecran-pc": ("Écrans PC", "Écrans PC"),
    "imprimante": ("Imprimantes", "Imprimantes"),
    "aspirateur-robot": ("Aspirateurs robots", "Aspirateurs robots"),
    "tv": ("Téléviseurs", "TV et barres de son"),
    "audio": ("Audio", "Enceintes, casques et écouteurs"),
    "photo-video": ("Photo et vidéo", "Photo, vidéo et drones"),
}
BOARD_BF = "Black Friday 2026"


# ---------------------------------------------------------------- polices
def _ttf(nom):
    CACHE.mkdir(exist_ok=True)
    dst = CACHE / (nom + ".ttf")
    if not dst.exists():
        from fontTools.ttLib import TTFont
        t = TTFont(str(ROOT / "assets" / "fonts" / (nom + ".woff2")))
        t.flavor = None
        t.save(str(dst))
    return str(dst)


_FC = {}


def font(nom, taille, poids):
    k = (nom, taille, poids)
    if k not in _FC:
        f = ImageFont.truetype(_ttf(nom), taille)
        axes = f.get_variation_axes()
        vals = []
        for a in axes:
            n = a["name"]
            n = n.decode() if isinstance(n, bytes) else n
            vals.append(max(a["minimum"], min(a["maximum"], poids)) if n == "Weight" else a["maximum"] if n == "Optical size" else a["default"])
        f.set_variation_by_axes(vals)
        _FC[k] = f
    return _FC[k]


def titre(t, p=800):
    return font("bricolage-grotesque", t, p)


def corps(t, p=700):
    return font("plus-jakarta-sans", t, p)


# ---------------------------------------------------------------- lecture du site
def _txt(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def _jsonld(h):
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            j = json.loads(m.group(1))
        except ValueError:
            continue
        for n in j.get("@graph", [j]):
            yield n


def fr(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def euro(p):
    return f"{int(round(p)):,}".replace(",", " ") + " €"


_PRODUITS = {}


def produit(url):
    """Fiche produit lue sur la page générée (title : « Nom : avis et tests, 8,2/10 (27 notes), env. 990 € »)."""
    path = url.replace(SITE, "").strip("/")
    if path in _PRODUITS:
        return _PRODUITS[path]
    f = ROOT / path / "index.html"
    res = None
    if f.exists():
        h = f.read_text(encoding="utf8")
        t = html.unescape(re.search(r"<title>(.*?)</title>", h, re.S).group(1))
        img = re.search(r'og:image" content="([^"]+)"', h)
        desc = re.search(r'<meta name="description" content="([^"]*)"', h)
        crumbs = [n for n in _jsonld(h) if n.get("@type") == "BreadcrumbList"]
        big = re.search(r'class="ps-big"><b>([\d,]+)</b>', h)
        nn = re.search(r"Moyenne de <b>(\d+) notes?</b>", h)
        tests = re.search(r"(\d+) tests? recens", h)
        prix = re.search(r"env\. ([\d \u202f\u00a0]+) €", t)
        usage_label = usage_url = None
        if crumbs and len(crumbs[0]["itemListElement"]) >= 4:
            e = crumbs[0]["itemListElement"][2]
            usage_label, usage_url = e["name"], e["item"]
            nom = html.unescape(crumbs[0]["itemListElement"][3]["name"])
            if big and nn and img and "/assets/img/p/" in img.group(1):
                res = {
                    "nom": nom, "avg": float(big.group(1).replace(",", ".")), "n": int(nn.group(1)),
                    "prix": float(re.sub(r"\D", "", prix.group(1))) if prix else None,
                    "img": ROOT / img.group(1).replace(SITE + "/", ""), "url": SITE + "/" + path + "/",
                    "desc": html.unescape(desc.group(1)) if desc else "", "usage_label": usage_label, "usage_url": usage_url,
                    "tests": int(tests.group(1)) if tests else None,
                }
    _PRODUITS[path] = res
    return res


_DATA = None


def data_items():
    global _DATA
    if _DATA is None:
        d = json.load(open(ROOT / "_source" / "data.json", encoding="utf8"))["items"]
        _DATA = {v.get("short"): v for v in d.values()}
    return _DATA


def usages():
    """Pages usage : (famille, libellé usage, url, classement [(nom, url)])."""
    out = []
    for fam, (flabel, board) in FAMILLES.items():
        for d in sorted((ROOT / fam).iterdir()):
            f = d / "index.html"
            if not f.is_file():
                continue
            h = f.read_text(encoding="utf8")
            il = [n for n in _jsonld(h) if n.get("@type") == "ItemList"]
            cr = [n for n in _jsonld(h) if n.get("@type") == "BreadcrumbList"]
            if not il or not cr or len(cr[0]["itemListElement"]) < 3:
                continue
            if len(cr[0]["itemListElement"]) != 3:
                continue
            lab = cr[0]["itemListElement"][2]["name"]
            items = [(e["name"], e["url"]) for e in sorted(il[0]["itemListElement"], key=lambda e: e["position"])]
            out.append({"fam": fam, "flabel": flabel, "board": board, "label": lab, "url": f"{SITE}/{fam}/{d.name}/", "items": items})
    return out


def intitule(u):
    """Nom d'usage lisible dans un titre d'épingle (« PC portables gaming », « Casques Bluetooth »)."""
    lab, fam, low = u["label"], u["fam"], u["label"].lower()
    if fam == "pc-portable":
        return "PC portables " + low
    if fam == "ordinateur-de-bureau":
        return {"Mini-PC": "Mini-PC", "Tout-en-un": "PC tout-en-un"}.get(lab, "PC de bureau " + low)
    if fam == "ecran-pc":
        return "Écrans PC " + low
    if fam == "imprimante":
        return "Imprimantes " + (lab if lab == "Laser N&B" else low)
    if fam == "aspirateur-robot":
        return {"Petit prix": "Robots aspirateurs petit prix", "Robot aspirateur laveur": "Robots aspirateurs laveurs"}.get(lab, lab)
    if fam == "tv":
        return lab if lab == "Barres de son" else "TV " + (low if lab[0].isalpha() else lab)
    return lab


# ---------------------------------------------------------------- dessin
def lignes(d, texte, f, largeur):
    mots, cur, res = texte.split(), "", []
    for m in mots:
        t = (cur + " " + m).strip()
        if d.textlength(t, font=f) <= largeur:
            cur = t
        else:
            if cur:
                res.append(cur)
            cur = m
    if cur:
        res.append(cur)
    return res


def ajuste(d, texte, fabrique, largeur, max_lignes, tmax, tmin):
    for t in range(tmax, tmin - 1, -2):
        f = fabrique(t)
        ls = lignes(d, texte, f, largeur)
        if len(ls) <= max_lignes:
            return f, ls
    f = fabrique(tmin)
    ls = lignes(d, texte, f, largeur)[:max_lignes]
    if ls:
        ls[-1] = ls[-1].rstrip(" ,.;:") + "…"
    return f, ls


def centre(d, y, texte, f, fill, ombre=True, x=W // 2):
    w = d.textlength(texte, font=f)
    if ombre:
        d.text((x - w / 2 + 3, y + 4), texte, font=f, fill=(0, 0, 0))
    d.text((x - w / 2, y), texte, font=f, fill=fill)


def base():
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 18], fill=GREEN)
    return im, d


def pied(d):
    f = titre(52, 800)
    w = d.textlength("top10geek.fr", font=f)
    d.rounded_rectangle([W / 2 - w / 2 - 36, 1388, W / 2 + w / 2 + 36, 1470], radius=22, fill=PILL)
    d.text((W / 2 - w / 2, 1398), "top10geek.fr", font=f, fill=MAGENTA)


def pastille(d, x, y, texte, fond, couleur):
    f = corps(30, 800)
    w = d.textlength(texte, font=f)
    d.rounded_rectangle([x, y, x + w + 44, y + 58], radius=29, fill=fond)
    d.text((x + 22, y + 10), texte, font=f, fill=couleur)
    return w + 44


def photo(im, p, box):
    x0, y0, x1, y1 = box
    ph = Image.open(p["img"]).convert("RGB")
    k = min((x1 - x0) / ph.width, (y1 - y0) / ph.height)
    ph = ph.resize((int(ph.width * k), int(ph.height * k)), Image.LANCZOS)
    im.paste(ph, (x0 + (x1 - x0 - ph.width) // 2, y0 + (y1 - y0 - ph.height) // 2))


def entete(d, kicker, ligne1, sous, bf=False):
    fk = corps(30, 800)
    k = kicker.upper()
    w = d.textlength(k, font=fk)
    d.rounded_rectangle([W / 2 - w / 2 - 26, 56, W / 2 + w / 2 + 26, 112], radius=28, fill=MAGENTA if bf else GREEN)
    d.text((W / 2 - w / 2, 64), k, font=fk, fill=WHITE if bf else PILL)
    f, ls = ajuste(d, ligne1.upper(), lambda t: titre(t, 800), 880, 3, 92, 52)
    y = 140
    for l in ls:
        centre(d, y, l, f, WHITE)
        y += int(f.size * 1.08)
    if sous:
        fs, lss = ajuste(d, sous, lambda t: titre(t, 700), 880, 2, 44, 30)
        for l in lss:
            centre(d, y + 6, l, fs, GREEN)
            y += int(fs.size * 1.15)
    return y


def carte_top(im, d, y, rang, p):
    d.rounded_rectangle([60, y, 940, y + 300], radius=36, fill=CARD)
    photo(im, p, (84, y + 36, 384, y + 264))
    cx, cy = 78, y + 30
    d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=MAGENTA)
    n = str(rang)
    f = titre(52, 800)
    d.text((cx - d.textlength(n, font=f) / 2, cy - 33), n, font=f, fill=WHITE)
    fn, ls = ajuste(d, p["nom"], lambda t: corps(t, 800), 520, 2, 40, 28)
    ty = y + 34
    for l in ls:
        d.text((414, ty), l, font=fn, fill=INK)
        ty += int(fn.size * 1.2)
    fnote = titre(104, 800)
    note = fr(p["avg"])
    d.text((414, y + 128), note, font=fnote, fill=(0, 150, 100))
    wn = d.textlength(note, font=fnote)
    d.text((414 + wn + 6, y + 190), "/10", font=corps(34, 700), fill=GREY)
    inf = f"{p['n']} note{'s' if p['n'] > 1 else ''} presse"
    if p["prix"]:
        inf += f" · env. {euro(p['prix'])}"
    d.text((414, y + 252), inf, font=corps(26, 700), fill=GREY)


def pin_top3(u, bf=False):
    ps = []
    for nom, url in u["items"]:
        p = produit(url)
        if p:
            ps.append(p)
        if len(ps) == 3:
            break
    if len(ps) < 3:
        return None
    im, d = base()
    lab = u["label"]
    if bf:
        y = entete(d, "Black Friday 2026", f"Top 3 {intitule(u)}", "les mieux notés par la presse", bf=True)
    else:
        y = entete(d, "Selon la presse", f"Top 3 {intitule(u)}", "notes de la presse high-tech, résumées")
    y = max(y + 30, 400)
    for i, p in enumerate(ps, 1):
        carte_top(im, d, y, i, p)
        y += 330
    pied(d)
    return im, ps


def pin_produit(p):
    im, d = base()
    y = entete(d, "Le test en résumé", p["nom"], None)
    top = max(y + 30, 330)
    d.rounded_rectangle([80, top, 920, top + 560], radius=40, fill=CARD)
    photo(im, p, (110, top + 30, 890, top + 530))
    y = top + 590
    fnote = titre(150, 800)
    note = fr(p["avg"])
    d.text((90, y - 12), note, font=fnote, fill=GREEN)
    wn = d.textlength(note, font=fnote)
    d.text((90 + wn + 6, y + 82), "/10", font=corps(48, 700), fill=WHITE)
    x2 = 90 + wn + 130
    d.text((x2, y + 18), f"{p['n']} note{'s' if p['n'] > 1 else ''} de presse", font=corps(34, 800), fill=WHITE)
    if p["prix"]:
        d.text((x2, y + 66), f"env. {euro(p['prix'])}", font=corps(34, 800), fill=GREEN)
        d.text((x2, y + 112), "prix indicatif", font=corps(24, 600), fill=(200, 200, 185))
    y += 190
    it = data_items().get(p["nom"], {})
    lst = [("+", s) for s in (it.get("strengths") or [])[:2]] + [("−", s) for s in (it.get("weak") or [])[:1]]
    for sig, s in lst:
        if y > 1330:
            break
        col = GREEN if sig == "+" else MAGENTA
        d.ellipse([90, y + 4, 128, y + 42], fill=col)
        fs = corps(32, 800)
        d.text((109 - d.textlength(sig, font=fs) / 2, y + 2), sig, font=fs, fill=PILL)
        f, ls = ajuste(d, s, lambda t: corps(t, 700), 760, 2, 32, 24)
        yy = y
        for l in ls:
            d.text((148, yy), l, font=f, fill=WHITE)
            yy += int(f.size * 1.25)
        y = max(yy, y + 50) + 14
    pied(d)
    return im


def pin_bf_conseils(titres):
    im, d = base()
    y = entete(d, "Black Friday 2026", "Comment repérer une vraie promo", "4 réflexes avant d'acheter", bf=True)
    y = max(y + 40, 420)
    for i, t in enumerate(titres, 1):
        d.rounded_rectangle([60, y, 940, y + 190], radius=34, fill=CARD)
        d.ellipse([90, y + 45, 190, y + 145], fill=MAGENTA)
        f = titre(60, 800)
        n = str(i)
        d.text((140 - d.textlength(n, font=f) / 2, y + 60), n, font=f, fill=WHITE)
        fn, ls = ajuste(d, t, lambda s: corps(s, 800), 680, 3, 38, 26)
        ty = y + 95 - int(len(ls) * fn.size * 1.2 / 2) + 10
        for l in ls:
            d.text((225, ty), l, font=fn, fill=INK)
            ty += int(fn.size * 1.2)
        y += 215
    pied(d)
    return im


# ---------------------------------------------------------------- sorties
def board_id(nom, boards):
    return boards.get(nom) or boards.get(FALLBACK_BOARD, "1091700834613967505")


def enregistrer(im, nom):
    OUT_IMG.mkdir(parents=True, exist_ok=True)
    im.save(OUT_IMG / (nom + ".jpg"), quality=78, optimize=True, progressive=True)
    return f"{SITE}/assets/img/pins/{nom}.jpg"


def slug(url):
    return url.rstrip("/").split("/")[-1]


def coupe(t, n):
    return t if len(t) <= n else t[: n - 1].rsplit(" ", 1)[0].rstrip(" ,.;:") + "…"


CALENDRIER = pathlib.Path(__file__).resolve().parent / "pins_calendrier.json"   # mémoire : épingles déjà planifiées
FEED = ROOT / "assets" / "pins" / "feed"


def planifier(lignes, a):
    """Répartit les épingles pas encore planifiées sur les prochains jours : un fichier JSON par date et créneau.

    Make lit chaque jour https://top10geek.fr/assets/pins/feed/AAAA-MM-JJ-m.json (matin) et -s.json (soir) et publie son contenu.
    Un visuel n'est jamais planifié deux fois (mémoire dans pins_calendrier.json)."""
    import datetime
    cal = json.load(open(CALENDRIER, encoding="utf8")) if CALENDRIER.exists() else {"planifies": [], "derniere_date": ""}
    deja = set(cal["planifies"])
    nouvelles = [l for l in lignes if l[4] not in deja]
    if a.debut:
        jour = datetime.date.fromisoformat(a.debut)
    elif cal["derniere_date"]:
        jour = datetime.date.fromisoformat(cal["derniere_date"]) + datetime.timedelta(days=1)
    else:
        jour = datetime.date.today() + datetime.timedelta(days=1)
    jour = max(jour, datetime.date.today() + datetime.timedelta(days=1))
    FEED.mkdir(parents=True, exist_ok=True)
    pas = a.par_creneau
    fin = jour + datetime.timedelta(days=a.jours)
    i, derniere = 0, cal["derniere_date"]
    while jour < fin and i < len(nouvelles):
        for cr in ("m", "s"):
            lot = nouvelles[i:i + pas]
            if not lot:
                break
            pins = [{"title": l[1], "description": l[2], "link": l[3], "image": l[4], "board_id": str(l[6]), "board": l[5]} for l in lot]
            json.dump({"date": jour.isoformat(), "creneau": cr, "pins": pins}, open(FEED / f"{jour.isoformat()}-{cr}.json", "w", encoding="utf8"),
                      ensure_ascii=False, indent=1)
            cal["planifies"] += [l[4] for l in lot]
            i += len(lot)
            derniere = jour.isoformat()
        jour += datetime.timedelta(days=1)
    cal["derniere_date"] = derniere
    json.dump(cal, open(CALENDRIER, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print(f"planifié : {i} épingles jusqu'au {derniere} ({len(nouvelles) - i} en attente)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--types", default="top3,produit,bf,bf-conseils")
    ap.add_argument("--max-produits", type=int, default=60)
    ap.add_argument("--famille", default="")
    ap.add_argument("--seulement-nouveaux", action="store_true", help="ne pas régénérer un visuel déjà présent")
    ap.add_argument("--planifier", action="store_true", help="écrit les fichiers de publication quotidiens lus par Make (assets/pins/feed/)")
    ap.add_argument("--jours", type=int, default=28, help="horizon de planification, en jours, à partir de la dernière date planifiée")
    ap.add_argument("--par-creneau", type=int, default=2, help="épingles par créneau (2 créneaux par jour : m = matin, s = soir)")
    ap.add_argument("--debut", default="", help="première date (AAAA-MM-JJ) ; par défaut le lendemain de la dernière date planifiée, ou demain")
    a = ap.parse_args()
    a.seulement_nouveaux = False   # les visuels sont reproductibles ; la mémoire des épingles déjà planifiées est pins_calendrier.json
    types = set(a.types.split(","))
    boards = json.load(open(BOARDS_JSON, encoding="utf8")) if BOARDS_JSON.exists() else {}
    rows = []   # (famille, type, ligne)

    def ajouter(fam, typ, titre_, desc, lien, img_url, tableau):
        rows.append((fam, typ, ["a publier", coupe(titre_, 100), coupe(desc, 480), lien, img_url, tableau, board_id(tableau, boards), typ]))

    us = [u for u in usages() if not a.famille or u["fam"] == a.famille]
    prod_faits = set()
    for u in us:
        lab, fl = u["label"], u["flabel"]
        nom_usage = intitule(u)
        if "top3" in types:
            f = OUT_IMG / f"top3-{u['fam']}-{slug(u['url'])}.jpg"
            if not (a.seulement_nouveaux and f.exists()):
                r = pin_top3(u)
            else:
                r = None
            if r:
                im, ps = r
                url_img = enregistrer(im, f"top3-{u['fam']}-{slug(u['url'])}")
                det = ", ".join(f"{p['nom']} ({fr(p['avg'])}/10)" for p in ps)
                ajouter(u["fam"], "top3", f"Top 3 {nom_usage} 2026 : le choix de la presse",
                        f"Les 3 mieux classés : {det}. Notes sur 10 calculées à partir des tests de la presse high-tech, sources à l'appui. "
                        f"Le top 10 complet, avec prix indicatifs et points forts, sur Top10Geek.", u["url"], url_img, u["board"])
        if "bf" in types:
            f = OUT_IMG / f"bf-{u['fam']}-{slug(u['url'])}.jpg"
            if not (a.seulement_nouveaux and f.exists()):
                r = pin_top3(u, bf=True)
            else:
                r = None
            if r:
                im, ps = r
                url_img = enregistrer(im, f"bf-{u['fam']}-{slug(u['url'])}")
                ajouter(u["fam"], "bf", f"Black Friday 2026 : top 3 {nom_usage} selon la presse",
                        f"Black Friday le 27 novembre 2026 : avant de craquer, voici les 3 {nom_usage} les mieux notés par la presse high-tech "
                        f"({', '.join(p['nom'] for p in ps)}). Les vraies baisses sont relevées sur la page Black Friday de Top10Geek.",
                        f"{SITE}/black-friday/", url_img, BOARD_BF)
        if "produit" in types:
            for nom, url in u["items"][:3]:
                if url in prod_faits:
                    continue
                prod_faits.add(url)
                p = produit(url)
                if not p or len([r for r in rows if r[1] == "produit"]) >= a.max_produits:
                    continue
                f = OUT_IMG / f"produit-{u['fam']}-{slug(url)}.jpg"
                if a.seulement_nouveaux and f.exists():
                    continue
                url_img = enregistrer(pin_produit(p), f"produit-{u['fam']}-{slug(url)}")
                ajouter(u["fam"], "produit", f"{p['nom']} : avis, test et note de la presse ({fr(p['avg'])}/10)",
                        (p["desc"] or f"{p['nom']} : {fr(p['avg'])}/10 sur {p['n']} notes presse.")
                        + " Points forts, réserves et prix indicatif sur Top10Geek.", url, url_img, u["board"])
    if "bf-conseils" in types:
        h = (ROOT / "black-friday" / "index.html").read_text(encoding="utf8")
        zone = h.split("Reconnaître une vraie promo", 1)[-1]
        tt = [_txt(x) for x in re.findall(r"<h3[^>]*>(.*?)</h3>", zone, re.S)][:4]
        if len(tt) == 4:
            url_img = enregistrer(pin_bf_conseils(tt), "bf-conseils")
            ajouter("", "bf-conseils", "Black Friday 2026 : comment repérer une vraie promo (4 réflexes)",
                    "Partir du prix le plus bas, vérifier la référence exacte, regarder la note de la presse, se méfier des pièges par catégorie : "
                    "les 4 réflexes pour ne pas se faire piéger le 27 novembre.", f"{SITE}/black-friday/#reconnaitre", url_img, BOARD_BF)
    # ordre de publication : on alterne familles et types pour ne pas enchaîner deux épingles voisines
    par_fam = {}
    for fam, typ, ligne in rows:
        par_fam.setdefault(fam, []).append(ligne)
    ordre, cles = [], list(par_fam)
    while any(par_fam.values()):
        for k in cles:
            if par_fam[k]:
                ordre.append(par_fam[k].pop(0))
    if a.planifier:
        planifier(ordre, a)
    OUT_CSV.parent.mkdir(exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf8") as fh:
        w = csv.writer(fh)
        w.writerow(["statut", "titre", "description", "lien", "image_url", "tableau", "board_id", "type"])
        w.writerows(ordre)
    print(f"OK {len(ordre)} épingles -> {OUT_CSV.relative_to(ROOT)}")


if __name__ == "__main__":
    sys.exit(main())
