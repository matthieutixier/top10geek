# -*- coding: utf-8 -*-
"""Top10Geek v10 (09/10/2026) — deux nouvelles rubriques : Écrans PC et Imprimantes (familles_new.py,
catalog_ecrans.py, catalog_imprimantes.py, guides_new.py ; données ajoutées par build_new.py). Textes génériques par famille.
v9 — comparateur de prix mis en veille : un prix indicatif par produit
(champ `prix` de data.json, constaté `prix_date`) et de simples liens vers les marchands
où le produit est en vente. Les prix par marchand restent dans data.json (champ `price`
des offres) mais ne sont plus affichés ; à réactiver avec les flux affiliés.
v8 — bloc « Notre choix », tri des fiches (sans tableau), une page par produit.
v7 — catalogue réel (50 PC portables + 50 ordinateurs de bureau), photos produits,
prix relevés par marchand (Amazon, Darty, Acer Store, Geekom), notes presse avec liens vers les tests.
Données : data.json (produit par build_data.py à partir de catalog.py)."""
import json, os, html, re, shutil, math, hashlib, unicodedata
from guides import GUIDES
from guides_desk import GUIDES_DESK
from desk import DCATS
from profiles import PROFILES
from familles_new import ECATS, ICATS, FAMILIES_NEW, FAQ_E, FAQ_I
from guides_new import GUIDES_NEW
from catalog_ecrans import ECR
from catalog_imprimantes import IMP
PROFILES = dict(PROFILES, **{k: (v["pour"], v["eviter"]) for k, v in list(ECR.items()) + list(IMP.items())})
SRC = os.path.dirname(os.path.abspath(__file__)) + "/"
CSS_FILES = ['artifact_base.css', 'extra.css', 'extra4.css', 'extra5.css', 'extra6.css', 'extra7.css', 'extra8.css', 'extra9.css', 'extra10.css', 'extra11.css', 'extra12.css', 'extra13.css']
VER = hashlib.md5(b''.join(open(SRC + f, 'rb').read() for f in CSS_FILES + ['main10.js'])).hexdigest()[:8]

OUT = os.path.dirname(SRC.rstrip("/"))
DOMAIN = "https://top10geek.fr"
DATA = json.load(open(SRC + "data.json", encoding="utf-8"))
MAJ = DATA["date"]
PRIX_DATE = DATA.get("prix_date", "")          # ex. « octobre 2026 »
IND = f"prix indicatif · {PRIX_DATE}"
# Mise à jour par rubrique (releve.py --famille) : chaque rubrique a sa date et son mois de prix.
# Sans entrée pour une rubrique, on retombe sur les dates globales.
ASSOC = {"Test-Achats", "Que Choisir", "Which?", "Tænk", "Choice", "Stiftung Warentest", "Consumer Reports", "OCU", "Altroconsumo"}
FAM_REL = {"laptop": "portable", "desktop": "bureau", "ecran": "ecran", "imprimante": "imprimante"}
FAM_DATES = DATA.get("familles", {})


def maj(fam):
    return FAM_DATES.get(FAM_REL.get(fam["key"]), {}).get("date", MAJ)


def pdate(fam):
    return FAM_DATES.get(FAM_REL.get(fam["key"]), {}).get("prix_date", PRIX_DATE)


def ind_txt(fam):
    return f"prix indicatif · {pdate(fam)}"
BASELINE = "Tous les tests high-tech, résumés pour vous"
AMAZON_MENTION = "En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises."
E = html.escape
GUIDES_ALL = dict(GUIDES, **GUIDES_DESK, **GUIDES_NEW)

LCATS = [
    dict(key="bureau", slug="bureautique", label="Bureautique", h="Bureautique &amp; mobilité", tag="Autonomie avant tout", color="var(--cat-bureau)", cls="f-bureau", badge="bureautique",
         h1='Les 10 meilleurs PC portables <span class="flash">bureautique</span> en 2026',
         intro="Ici, l'autonomie réelle et le poids dans le sac priment sur des benchmarks de calcul rarement utiles au quotidien."),
    dict(key="creation", slug="creation", label="Création", h="Création &amp; photo", tag="Couleur au taquet", color="var(--cat-creation)", cls="f-creation", badge="creation",
         h1='Les 10 meilleurs PC portables pour la <span class="flash">création</span> en 2026',
         intro="Retouche photo, montage vidéo : la variable qui départage, c'est la fidélité des couleurs sortie d'usine — pas le nombre de cœurs du processeur."),
    dict(key="gaming", slug="gaming", label="Gaming", h="Gaming", tag="FPS ou rien", color="var(--cat-gaming)", cls="f-gaming", badge="gaming",
         h1='Les 10 meilleurs PC portables <span class="flash">gaming</span> en 2026',
         intro="Deux chiffres suffisent à trancher la plupart des débats : les FPS en jeu réel, et le bruit du ventilo pour les obtenir."),
    dict(key="polyvalent", slug="polyvalent", label="Polyvalent", h="Polyvalent", tag="Zéro concession", color="var(--cat-poly)", cls="f-polyvalent", badge="polyvalent",
         h1='Les 10 meilleurs PC portables <span class="flash">polyvalents</span> en 2026',
         intro="Pas de spécialité affichée, mais aucun vrai point faible non plus : le pari le plus sûr pour une seule machine capable de tout faire."),
    dict(key="lowcost", slug="lowcost", label="Low-cost", h="Low-cost (&lt; 500 €)", tag="Prix cassé, compromis assumés", color="var(--cat-lowcost)", cls="f-lowcost", badge="lowcost",
         h1='Les 10 meilleurs PC portables <span class="flash">à moins de 500 €</span>',
         intro="Sous les 500 €, chaque euro compte double. La presse teste peu ces machines : nous affichons le nombre de tests derrière chaque note pour que vous sachiez à quoi vous fier."),
]
DH1 = {"d-bureau": 'Les 10 meilleurs ordinateurs de bureau pour la <span class="flash">bureautique</span>',
       "d-creation": 'Les 10 meilleurs ordinateurs de bureau pour la <span class="flash">création</span>',
       "d-gaming": 'Les 10 meilleurs <span class="flash">PC gamer fixes</span> prêts à jouer',
       "d-mini": 'Les 10 meilleurs <span class="flash">mini-PC</span> en 2026',
       "d-aio": 'Les 10 meilleurs ordinateurs <span class="flash">tout-en-un</span>'}
for c in DCATS:
    c["h1"] = DH1[c["key"]]

FAMILIES = [
    dict(key="laptop", slug="pc-portable", label="PC portable", plural="PC portables", cats=LCATS, provisional=False,
         m_labels=("Poids", "Autonomie"), col="Poids", mascot="mascotte-persona-v2", noun="PC portable", noun_det="le PC portable",
         h1='Comparatif PC portables 2026 : <span class="flash">le verdict par usage</span>',
         intro="50 PC portables passés au crible, une note presse sur 10 tirée de centaines de tests, un prix indicatif, les liens vers les marchands et un top 10 pour chaque usage."),
    dict(key="desktop", slug="ordinateur-de-bureau", label="Ordinateur de bureau", plural="Ordinateurs de bureau", cats=DCATS, provisional=False,
         m_labels=("Format", "Processeur"), col="Format", mascot="pose-tour", noun="ordinateur de bureau", noun_det="l'ordinateur",
         h1='Comparatif ordinateurs de bureau 2026 : <span class="flash">tours, mini-PC et tout-en-un</span>',
         intro="50 ordinateurs de bureau classés par usage : bureautique, création, gaming, mini-PC et tout-en-un, avec les notes de la presse, un prix indicatif et les liens vers les marchands."),
] + FAMILIES_NEW
CAT = {}
for f in FAMILIES:
    for c in f["cats"]:
        c["family"] = f["key"]; c["fslug"] = f["slug"]
        CAT[c["key"]] = c
FAM = {f["key"]: f for f in FAMILIES}
BUDGETS = [("all", "Tous les prix", 0, 1e9), ("b1", "< 500 €", 0, 500), ("b2", "500 – 1 000 €", 500, 1000),
           ("b3", "1 000 – 1 500 €", 1000, 1500), ("b4", "1 500 – 2 000 €", 1500, 2000), ("b5", "> 2 000 €", 2000, 1e9)]
MERCHANT_CLS = {"Amazon": "amazon", "Darty": "darty", "Fnac": "fnac", "Acer Store": "acer", "Geekom": "geekom"}
# Marchands dont le programme d'affiliation est validé (lien rémunéré). Les autres sont de simples liens directs.
# À compléter à chaque validation (ex. Awin : "Darty", "Fnac", "Acer Store", "Geekom") : attributs rel et mentions suivent.
AFFILIATED = ["Amazon"]
AFF_TXT = " et ".join(AFFILIATED)


def rel_m(m):
    """rel d'un lien marchand : « sponsored » réservé aux liens réellement rémunérés."""
    return "nofollow sponsored noopener" if m in AFFILIATED else "nofollow noopener"


def fr(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def euro(x):
    v = int(round(x / 10.0) * 10) if x >= 1000 else int(x)
    return f"{v:,}".replace(",", " ") + " €"


def euro2(x):
    """Prix exact relevé (avec centimes s'il y en a)."""
    s = f"{x:,.2f}".replace(",", " ").replace(".", ",")
    if s.endswith(",00"):
        s = s[:-3]
    return s + " €"


def euro_ind(x):
    """Prix indicatif arrondi à la dizaine, sans changer de tranche de budget (499 € reste « < 500 € »)."""
    v = int(round(x / 10.0) * 10)
    if bucket(v) != bucket(x):
        v = int(x // 10 * 10)
    return f"{v:,}".replace(",", " ") + " €"


def bucket(p):
    for k, _, lo, hi in BUDGETS[1:]:
        if lo <= p < hi:
            return k
    return "b5"


def pslug(name):
    """Adresse d'une fiche produit : « Asus Zenbook A14 » -> asus-zenbook-a14."""
    t = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower().replace('"', "")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


# ---------------------------------------------------------------- Catalogue (data.json)
ITEMS = {}
for pid, n in DATA["items"].items():
    c = CAT[n["cat"]]
    tests = n["press"]
    rated = tests if tests["avg"] is not None else None
    # Liens marchands : uniquement là où le produit est en vente (sauf s'il ne reste aucune offre),
    # le marchand affilié en premier, puis l'ordre du dernier prix connu.
    offers = [o for o in n["offers"] if o.get("dispo", True)] or n["offers"]
    offers = sorted(offers, key=lambda o: (o["m"] not in AFFILIATED, o["price"]))
    d = dict(id=pid, cat=n["cat"], short=n["short"], ref=n["ref"], badge=n["badge"], idx=None,
             p=float(n.get("prix") or min(o["price"] for o in offers)),
             r=(n["rating"] if n.get("rating") and n.get("nrev", 0) >= 3 else -1), nrev=n.get("nrev", 0),
             verdict=n["verdict"], strengths=n["strengths"], weak=n["weak"], m=tuple(n["m"]),
             press=rated, tests=tests, offers=offers, img=n.get("img"), configs=None, url=offers[0]["url"])
    d["slug"] = c["slug"]; d["family"] = c["family"]; d["fslug"] = c["fslug"]
    d["from"] = len(offers) > 1
    d["price_txt"] = "env. " + euro_ind(d["p"])
    d["bucket"] = bucket(d["p"])
    d["href"] = f'{c["fslug"]}/{c["slug"]}/#{pid}'
    d["pslug"] = pslug(n["short"])
    d["purl"] = f'{c["fslug"]}/{d["pslug"]}/'
    d["pour"], d["eviter"] = PROFILES[pid]
    ITEMS[pid] = d
assert len({d["purl"] for d in ITEMS.values()}) == len(ITEMS)
assert not {d["pslug"] for d in ITEMS.values()} & {c["slug"] for c in CAT.values()}


def rank_key(d):
    top = 0 if d["badge"] == "Le choix de la bande" else 1
    pr = d["press"]
    return (top, 0 if pr else 1, -(pr["avg"] if pr else 0), -(pr["n"] if pr else d["tests"]["tests"]), d["p"])


by_cat = {k: sorted([d for d in ITEMS.values() if d["cat"] == k], key=rank_key) for k in CAT}
for k in CAT:
    assert len(by_cat[k]) == 10, k


def notes_total(items):
    seen, tot = set(), 0
    for d in items:
        pr = d["press"]
        if pr and pr["src"][1] not in seen:
            seen.add(pr["src"][1]); tot += pr["n"]
    return tot


TOTAL_NOTES = sum(d["tests"]["n"] for d in ITEMS.values())
TOTAL_TESTS = sum(d["tests"]["tests"] for d in ITEMS.values())


# ---------------------------------------------------------------- Graphe à bulles
def bubble_svg(items, aria, link_root=None, sid="bubbleChart"):
    tested = [d for d in items if d["press"]]
    xs = [d["press"]["avg"] for d in tested] or [7, 9]
    xmin = min(6, math.floor(min(xs) - 0.2)); xmax = 10
    ps = [d["p"] for d in items]
    span = max(ps) - min(ps) or 100
    step = next(st for st in (50, 100, 250, 500, 1000) if span / st <= 5)
    ymin = max(0, math.floor(min(ps) * 0.9 / step) * step)
    ymax = math.ceil(max(ps) * 1.06 / step) * step
    if (ymax - ymin) / step < 3:
        ymax = ymin + 3 * step
    x0, x1, y0, y1 = 88, 330, 300, 22
    xs0 = 58
    X = lambda v: x0 + (v - xmin) / (xmax - xmin) * (x1 - x0)
    Y = lambda v: y0 - (v - ymin) / (ymax - ymin) * (y0 - y1)
    g = []
    med = sorted(ps)[len(ps) // 2]
    zx, zy = X(8), Y(med)
    g.append(f'<rect class="deal-zone" x="{zx:.1f}" y="{zy:.1f}" width="{x1 - zx:.1f}" height="{y0 - zy:.1f}" rx="6"></rect>')
    g.append(f'<text class="deal-label" x="{x1 - 4:.1f}" y="{y0 - 6:.1f}" text-anchor="end">BONNES AFFAIRES ↘</text>')
    nt = int(round((ymax - ymin) / step))
    for i in range(1, nt):
        y = Y(ymin + i * step); g.append(f'<line class="grid-line" x1="{xs0 - 16}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}"></line>')
    for v in range(xmin + 1, xmax):
        x = X(v); g.append(f'<line class="grid-line" x1="{x:.1f}" y1="{y1}" x2="{x:.1f}" y2="{y0}"></line>')
    g.append(f'<line class="axis-line" x1="{xs0 - 16}" y1="{y0}" x2="{x1}" y2="{y0}"></line><line class="axis-line" x1="{x0 - 12}" y1="{y1}" x2="{x0 - 12}" y2="{y0}" style="stroke-dasharray:2 3;stroke-width:1"></line>')
    for v in range(xmin, xmax + 1):
        g.append(f'<text class="axis-label" x="{X(v):.1f}" y="312" text-anchor="middle">{v}</text>')
    g.append(f'<text class="axis-label" x="{xs0:.0f}" y="312" text-anchor="middle">sans</text><text class="axis-label" x="{xs0:.0f}" y="321" text-anchor="middle">note</text>')
    g.append(f'<text class="axis-label" x="{x1}" y="330" text-anchor="end">Note presse (/10) →</text>')
    for i in range(0, nt + 1):
        v = ymin + i * step
        g.append(f'<text class="axis-label" x="{xs0 - 20}" y="{Y(v) + 3:.1f}" text-anchor="end">{int(v):,} €</text>'.replace(",", " "))
    g.append('<text class="axis-label" x="4" y="12" text-anchor="start">↑ Prix</text>')

    def rad(d):
        return 7 if not d["press"] else max(5, min(15, 4.5 + 2.6 * math.sqrt(d["press"]["n"])))
    for d in sorted(items, key=lambda d: -rad(d)):
        pr = d["press"]
        col = CAT[d["cat"]]["color"]
        cx = X(pr["avg"]) if pr else xs0
        tip = f'{d["short"]} — ' + (f'note presse {fr(pr["avg"])}/10 ({pr["n"]} note{"s" if pr["n"] > 1 else ""})' if pr else "testé par la presse, sans note chiffrée") + f', {d["price_txt"]}'
        cls = "bubble" + ("" if pr else " nopress")
        style = f' style="stroke:{col}"' if not pr else ""
        circ = f'<circle class="{cls}" data-id="{d["id"]}" data-cat="{d["cat"]}" data-budget="{d["bucket"]}" cx="{cx:.1f}" cy="{Y(d["p"]):.1f}" r="{rad(d):.1f}" fill="{col}"{style} tabindex="0" role="button" aria-label="{E(d["short"])}"><title>{E(tip)}</title></circle>'
        if link_root is not None:
            circ = f'<a href="{link_root}{d["href"]}">' + circ.replace(' tabindex="0" role="button"', '') + "</a>"
        g.append(circ)
    return f'<svg viewBox="0 0 340 336" role="img" aria-label="{E(aria)}" id="{sid}">' + "".join(g) + "</svg>"


LEGEND = """<div>
  <div class="legend-title">Comment lire le graphe</div>
  <p class="legend-note"><b>→ À droite</b> : la presse l'a bien noté. <b>↑ En haut</b> : il est cher. <b>Grosse bulle</b> : note appuyée sur beaucoup de tests. <b>Pointillés</b> : testé par la presse, mais sans note chiffrée. Les meilleures affaires sont <b>en bas à droite</b>, dans la zone jaune.</p>
</div>
<div>
  <div class="legend-title">Taille = nombre de notes presse</div>
  <div class="legend-size">
    <div class="ex"><svg width="20" height="20"><circle cx="10" cy="10" r="7" fill="none" stroke="var(--ink-muted)" stroke-width="1.6"/></svg>1 note</div>
    <div class="ex"><svg width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--ink-muted)" stroke-width="1.6"/></svg>15+ notes</div>
    <div class="ex"><svg width="20" height="20"><circle cx="10" cy="10" r="7" fill="var(--ink-muted)" fill-opacity=".1" stroke="var(--ink-muted)" stroke-width="1.6" stroke-dasharray="3 2"/></svg>sans note</div>
  </div>
</div>"""


def js_data(items, root, first):
    out = {}
    for d in items:
        pr = d["press"]
        fam = FAM[d["family"]]
        out[d["id"]] = dict(short=d["short"], ref=d["ref"], cat=d["cat"], slug=d["slug"], fslug=d["fslug"], badgeImg=CAT[d["cat"]]["badge"],
                            catLabel=(CAT[d["cat"]]["label"] + (" · " + fam["label"] if True else "")).upper(),
                            badge=d["badge"], idx=(fr(d["idx"]) if d["idx"] else None), idxv=d["idx"], tested=bool(pr), price=d["price_txt"],
                            rating=(fr(d["r"]) + " ★" if d["r"] > 0 else ""), img=d["img"], ntests=d["tests"]["tests"],
                            offers=[[o["m"], "", o["url"], o.get("cfg", ""), o["m"] in AFFILIATED] for o in d["offers"]], verdict=d["verdict"], strengths=d["strengths"], weak=d["weak"],
                            m=[[fam["m_labels"][0], d["m"][0]], [fam["m_labels"][1], d["m"][1]]], url=d["url"], purl=d["purl"],
                            press=(dict(avg=fr(pr["avg"]), n=pr["n"], gamme=pr["scope"] == "gamme") if pr else None))
    return "<script>window.T10G=" + json.dumps(dict(laptops=out, root=root, first=first), ensure_ascii=False) + ";</script>"


def detail_card(root, fam=None):
    return f"""<div class="detail-col"><div class="featured" id="detailCard">
  <div class="art art-photo" id="detailArt"><img class="art-product" id="detailArtImg" src="{root}assets/img/badge-bureautique.webp" alt="" width="560" height="420"><img class="art-cat" id="detailCatImg" src="{root}assets/img/badge-bureautique.webp" alt="" width="54" height="54"></div>
  <div class="featured-body">
    <div class="cat-label-inline" id="detailCatLabel"></div>
    <span class="fbadge" id="detailBadge"></span>
    <div class="featured-title"><div><h3 id="detailName"></h3><div class="ref" id="detailRef"></div></div>
      <div class="score big-press" id="detailPress"></div></div>
    <div class="metrics m4">
      <div class="metric" id="mR"><span class="k">Avis clients Darty</span><span class="v" id="detailRating"></span></div>
      <div class="metric" id="mA"><span class="k" id="mAk"></span><span class="v" id="mAv"></span></div>
      <div class="metric" id="mB"><span class="k" id="mBk"></span><span class="v" id="mBv"></span></div>
    </div>
    <p class="lead-line" id="detailVerdict"></p>
    <div class="pc-grid"><div class="strengths" id="detailStrengths"></div><div class="strengths weak" id="detailWeak"></div></div>
    <div class="offers" id="detailOffers"></div>
    <div class="featured-footer">
      <div><span class="price-tag" id="detailPrice"></span><span class="price-from">{ind_txt(fam) if fam else IND}</span></div>
      <div class="cta-row"><a class="see-all" id="detailMore" href="#">Avis et tests détaillés</a><a class="cta" id="detailCta" href="#" target="_blank" rel="nofollow noopener">Voir chez le marchand →</a></div>
    </div>
  </div>
</div></div>"""


def table(items, fam, show_cat=True, root='../'):
    rows = []
    for d in items:
        pr = d["press"]
        pcell = (f'<td class="num"><span class="press-chip">{fr(pr["avg"])}<small>·{pr["n"]}</small></span></td>' if pr else '<td class="num muted">sans note</td>')
        m0 = d["m"][0]
        rows.append(f"""<tr data-id="{d['id']}" data-cat="{d['cat']}" data-budget="{d['bucket']}" data-price="{d['p']}" data-press="{pr['avg'] if pr else -1}" data-idx="{d['idx'] or -1}" data-rating="{d['r']}" tabindex="0">
<td class="name-cell">{f'<img class="thumb" src="{root}assets/img/p/{d["img"]}" alt="" width="48" height="36" loading="lazy">' if d['img'] else ''}<span class="dot {CAT[d['cat']]['cls'].replace('f-', '')}"></span><span>{E(d['short'])}</span></td>{f"<td>{CAT[d['cat']]['label']}</td>" if show_cat else ''}
{pcell}<td class="num">{d['price_txt']}</td><td class="{'num' if fam['key'] == 'laptop' else ''}">{'—' if m0 == 'n.c.' else E(m0)}</td>{('<td class="num">' + ('—' if d['r'] < 0 else fr(d['r']) + ' ★') + '</td>') if fam['key'] == 'laptop' else ''}</tr>""")
    cat_th = '<th data-sort="cat">Usage<span class="sort-arrow">↕</span></th>' if show_cat else ""
    return f"""<div class="data-table-wrap"><table class="data-table" id="dataTable">
<thead><tr><th data-sort="name">Machine<span class="sort-arrow">↕</span></th>{cat_th}
<th data-sort="press">Note presse<span class="sort-arrow">↕</span></th><th data-sort="price">Prix<span class="sort-arrow">↕</span></th>
<th>{fam['col']}</th>{'<th data-sort="rating">Avis Darty<span class="sort-arrow">↕</span></th>' if fam['key'] == 'laptop' else ''}</tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>"""


def budget_filter(items):
    present = {d["bucket"] for d in items}
    if len(present) < 2:
        return ""
    btn = []
    for k, l, _, _ in BUDGETS:
        if k != "all" and k not in present:
            continue
        dis = ""
        btn.append(f'<button class="pill" data-budget-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}"{dis}>{l}</button>')
    return '<div class="usage-filter" id="budgetFilter" role="group" aria-label="Filtrer par budget"><span class="filter-label">Votre budget :</span>' + "".join(btn) + "</div>"


def mini(k, v, bar=False):
    if not v or v == "n.c.":
        return ""
    return f'<div class="mini{" mbar" if bar else ""}"><span class="k">{k}</span><span class="v">{v}</span></div>'


def guide_html(key):
    g = GUIDES_ALL[key]
    crit = "".join(f'<div class="g-card"><span class="g-num">0{i}</span><h3>{t}</h3><p>{x}</p></div>' for i, (t, x) in enumerate(g["criteres"], 1))
    pieges = "".join(f"<li>{p}</li>" for p in g["pieges"])
    bud = "".join(f'<div class="g-tier"><strong>{a}</strong><span>{b}</span></div>' for a, b in g["budget"])
    return f"""<section class="guide" id="guide">
    <div class="section-head"><h2>{g['titre']}</h2><div class="tag">Guide d'achat</div></div>
    <p class="guide-intro">{g['intro']}</p>
    <div class="g-grid">{crit}</div>
    <div class="g-bottom">
      <div class="g-box"><div class="legend-title">Les pièges à éviter</div><ul class="g-pieges">{pieges}</ul></div>
      <div class="g-box"><div class="legend-title">Quel budget prévoir ?</div><div class="g-tiers">{bud}</div></div>
    </div>
    <p class="guide-go"><a class="cta" href="#top10">Voir le classement ↓</a></p>
  </section>"""


PROVISIONAL_NOTE = '<div class="provisional"><b>Sélection provisoire.</b> Le comparatif complet des ordinateurs de bureau (notes presse, prix vérifiés, top 10) arrive très bientôt. Prix indicatifs.</div>'


# ---------------------------------------------------------------- Gabarit
def nav_html(root, active):
    parts = []
    for f in FAMILIES:
        subs = f'<a class="dd-all" href="{root}{f["slug"]}/"><span>Tout le comparatif</span><span class="arr">→</span></a><div class="dd-sep">Par usage</div>' + "".join(
            f'<a href="{root}{f["slug"]}/{c["slug"]}/"><span class="dot {c["cls"].replace("f-", "")}"></span>{c["label"]}</a>' for c in f["cats"])
        act = " active" if active == f["slug"] else ""
        parts.append(f"""<div class="dd{act}"><a class="dd-top" href="{root}{f['slug']}/" aria-haspopup="true">{f['label']}<span class="caret">▾</span></a>
  <div class="dd-menu">{subs}</div></div>""")
    parts.append(f'<a class="nav-link{" active" if active == "methode" else ""}" href="{root}methode">Méthode</a>')
    return "".join(parts)


ORG = {"@type": "Organization", "@id": DOMAIN + "/#organisation", "name": "Top 10 Geek", "url": DOMAIN + "/",
       "logo": DOMAIN + "/assets/img/logo-face.png", "email": "contact@top10geek.fr"}


def plain(t):
    """Texte brut pour les données structurées : sans balises ni entités HTML."""
    return html.unescape(re.sub(r"<[^>]+>", "", t)).strip()


def ld_crumbs(*steps):
    """steps : (nom, chemin relatif au domaine). Le dernier élément est la page courante."""
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": plain(n), "item": f"{DOMAIN}/{p}"} for i, (n, p) in enumerate(steps, 1)]}


def ld_faq(pairs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in pairs]}


def ld_script(nodes):
    if not nodes:
        return ""
    data = {"@context": "https://schema.org", "@graph": nodes}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>\n"


def page(root, title, desc, path, body, active="", extra="", body_cls="", og_img="assets/img/og-image.jpg", ld=None):
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8"><script>document.documentElement.classList.add('js')</script>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{DOMAIN}/{path}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Top 10 Geek">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{DOMAIN}/{og_img}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{DOMAIN}/{og_img}">
<link rel="icon" type="image/png" href="{root}assets/img/logo-face.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800;12..96,900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/style.css?v={VER}">
{ld_script(ld)}</head>
<body class="{body_cls}">
<div class="wrap">
  <div class="topbar">
    <a class="brand-lockup" href="{root or "./"}">
      <img class="brand-mark" src="{root}assets/img/logo-face.webp" alt="Symbole Top 10 Geek" width="40" height="40">
      <div class="brand-text"><div class="brand">TOP<span class="dot">10</span>GEEK</div><div class="baseline">{BASELINE}</div></div>
    </a>
    <nav class="topnav" id="topnav">{nav_html(root, active)}</nav>
    <div class="topbar-actions"><button class="topnav-toggle" id="navToggle" aria-expanded="false" aria-controls="topnav">Menu</button></div>
  </div>
{body}
  <footer>
    <div class="disclosure" id="affiliation">Certains liens de ce site sont des liens d'affiliation (à ce jour : {AFF_TXT}) : si vous achetez via ces liens, nous pouvons percevoir une commission. Cela n'entraîne aucun coût supplémentaire pour vous et n'influence pas nos verdicts, établis avant toute recherche de lien commercial. {AMAZON_MENTION}</div>
    <div class="foot-row">
      <div class="foot-sig"><img src="{root}assets/img/logo-face.webp" alt="" width="32" height="32">TOP 10 GEEK — {BASELINE}</div>
      <div class="foot-links"><a href="{root}pc-portable/">PC portables</a><a href="{root}ordinateur-de-bureau/">Ordinateurs de bureau</a><a href="{root}ecran-pc/">Écrans PC</a><a href="{root}imprimante/">Imprimantes</a><a href="{root}black-friday/">Black Friday 2026</a><a href="{root}methode">Méthode</a><a href="{root}mentions-legales">Mentions légales</a><a href="{root}politique-confidentialite">Confidentialité</a><span>MAJ {MAJ}</span></div>
    </div>
  </footer>
  <a class="to-top" href="#" aria-label="Revenir en haut de la page">↑</a>
</div>
{extra}
<script src="{root}assets/main.js?v={VER}" defer></script>
</body>
</html>
"""


MAIL = '<a href="mailto:contact@top10geek.fr">contact@top10geek.fr</a>'
LEGAL_FILL = [
    ('Nom : <span class="fill">[PRÉNOM NOM]</span>', 'Nom : Matthieu Tixier — nom commercial : Geek Concept'),
    ('<span class="fill">[ex. entrepreneur individuel (micro-entreprise)]</span>', 'Entrepreneur individuel (EI)'),
    ('SIRET : <span class="fill">[N° SIRET]</span>', 'SIRET : 130 805 831 00018 — R.C.S. La Rochelle 130 805 831'),
    ('<span class="fill">[ADRESSE POSTALE]</span>', '4 rue Anatole France, 17000 La Rochelle, France'),
    ('<span class="fill">[ADRESSE E-MAIL DE CONTACT]</span>', MAIL),
    ('<span class="fill">[PRÉNOM NOM]</span>', 'Matthieu Tixier'),
]


def write(path, content):
    if path.endswith(".html"):
        for x, y in LEGAL_FILL:
            content = content.replace(x, y)
        assert 'class="fill"' not in content, path
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)


def usage_cards(fam, root):
    out = []
    for c in fam["cats"]:
        top = by_cat[c["key"]][0]
        pr = top["press"]
        note = f'{fr(pr["avg"])}/10 presse' if pr else "testé, sans note"
        out.append(f"""<a class="usage-card" href="{root}{fam['slug']}/{c['slug']}/">
  <div class="uc-art"><img src="{root}assets/img/badge-{c['badge']}.webp" alt="" loading="lazy" width="110" height="110"></div>
  <div class="uc-body"><span class="uc-tag">{c['tag']}</span><h3><span class="dot {c['cls'].replace('f-', '')}"></span>{c['h']}</h3>
  <p class="uc-pick">Le choix de la bande : <b>{E(top['short'])}</b> — {note}</p>
  <span class="uc-go">{'Voir le top 10' if not fam['provisional'] else 'Voir la sélection'} →</span></div></a>""")
    return "".join(out)


FAQ_L = [
    ("Comment est calculée la note presse ?", "C'est la moyenne simple des notes publiées par les médias spécialisés (Notebookcheck, Clubic, Les Numériques, Tom's Hardware, TechRadar…), toutes converties sur 10 : 4/5 devient 8/10, 87 % devient 8,7/10. Le nombre de tests est toujours affiché. Quand la note porte sur une autre configuration de la même gamme, nous l'indiquons."),
    ("Comment est établi le classement ?", "En tête : « le choix de la bande », notre recommandation pour l'usage. Ensuite, les ordinateurs sont classés par note presse. Ceux dont les tests ne donnent pas de note chiffrée viennent en dernier."),
    ("Faut-il 16 ou 32 Go de RAM en 2026 ?", "16 Go reste le minimum confortable pour de la bureautique ou du gaming courant. Pour la création ou pour garder la machine plusieurs années, 32 Go évite de la remplacer prématurément."),
    ("Pourquoi certains ordinateurs n'ont pas de note presse ?", "Tous les ordinateurs de la sélection ont été testés par au moins un média. Mais certains tests ne donnent pas de note chiffrée : dans ce cas nous l'indiquons (bulle en pointillés) et nous donnons le lien vers le test plutôt que d'inventer une note."),
    ("D'où viennent les prix ?", f"Nous affichons un prix indicatif par ordinateur : le plus bas que nous avons constaté chez les marchands (Amazon, Darty, Acer Store, Geekom) en {PRIX_DATE}, arrondi à la dizaine d'euros. Il sert à situer la machine, pas à comparer les marchands : le prix a pu changer depuis et la configuration exacte peut différer d'un marchand à l'autre. Seul le prix affiché par le marchand fait foi."),
]


def fam_faq(fam):
    return {"ecran": FAQ_E, "imprimante": FAQ_I}.get(fam["key"], FAQ_L)


# ---------------------------------------------------------------- Pages comparatif par famille
def family_page(fam):
    root = "../"
    cats = fam["cats"]
    sel, tsel = [], []
    for c in cats:
        items = by_cat[c["key"]]
        best = items[:2]
        cheap = sorted([d for d in items if d not in best], key=lambda d: d["p"])[:2]
        sel += best + cheap
        tsel += items[:3]
    all_items = [d for c in cats for d in by_cat[c["key"]]]
    pills = '<button class="pill" data-filter="all" aria-pressed="true"><span class="pdot" style="background:var(--ink)"></span>Tous</button>' + "".join(
        f'<button class="pill {c["cls"]}" data-filter="{c["key"]}" aria-pressed="false"><span class="pdot" style="background:{c["color"]}"></span>{c["label"]}</button>' for c in cats)
    faq = "".join(f'<details class="faq-item"{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(fam_faq(fam)))
    tested = sum(1 for d in all_items if d["press"])
    body = f"""
  <div class="crumb"><a href="../">Accueil</a> › {fam['plural']}</div>
  <section class="usage-hero">
    <div>
      <div class="eyebrow">COMPARATIF {fam['plural'].upper()} · MAJ {maj(fam)}</div>
      <h1>{fam['h1']}</h1>
      <p>{fam['intro']}</p>
      <div class="spec-row">
        <div><strong>{len(all_items)}</strong>{fam['plural']} sélectionné{'e' if fam['key'] == 'imprimante' else ''}s</div>
        <div><strong>{sum(d["tests"]["tests"] for d in all_items)}</strong>tests presse recensés</div>
        <div><strong>{len(cats)}</strong>usages</div>
      </div>
    </div>
    <img class="hero-badge tall" src="../assets/img/{fam['mascot']}.webp" alt="La mascotte Top 10 Geek" width="220" height="260">
  </section>
  {PROVISIONAL_NOTE if fam['provisional'] else ''}
  <section class="comparator" id="comparateur">
    <div class="comparator-head">
      <div><h2>Ce qu'en dit la presse, et ce que ça coûte</h2>
      <p class="comparator-sub">Chaque bulle est {'une' if fam['key'] == 'imprimante' else 'un'} {fam['noun']}. <b>Plus elle est à droite, mieux la presse l'a noté ; plus elle est basse, moins il est cher.</b> Cliquez sur une bulle pour lire le verdict.</p></div>
      <img class="comparator-pose" src="../assets/img/pose-investigation.webp" alt="" width="88" height="88">
    </div>
    <div class="usage-filter" id="usageFilter" role="group" aria-label="Filtrer par usage">{pills}</div>
    <div class="comparator-grid">
      <div class="chart-col">
        <div class="chart-pane">{bubble_svg(sel, "Graphe à bulles : note presse contre prix, taille selon le nombre de tests")}</div>
        <div class="legend-strip">
          <div><div class="legend-title">Catégorie d'usage</div><div class="legend-cats">{''.join(f'<div class="legend-cat"><span class="dot {c["cls"].replace("f-", "")}"></span>{c["label"]}</div>' for c in cats)}</div></div>
          {LEGEND}
        </div>
      </div>
      {detail_card(root, fam)}
    </div>
  </section>
  <div class="divider"><span></span><span></span><span></span><span></span><span></span></div>
  <section class="section">
    <div class="section-head"><h2>Choisissez votre usage</h2><div class="tag">{fam['plural']}</div></div>
    <div class="usage-grid">{usage_cards(fam, root)}</div>
  </section>
  <section class="section" id="faq" style="border-bottom:none;">
    <div class="section-head"><h2>Questions fréquentes</h2><div class="tag">FAQ</div></div>
    <div class="faq-list">{faq}</div>
  </section>
"""
    title = ("Meilleur PC portable 2026 : tous les tests résumés par usage | Top 10 Geek" if fam["key"] == "laptop"
             else "Meilleur ordinateur de bureau 2026 : tours, mini-PC, tout-en-un | Top 10 Geek" if fam["key"] == "desktop" else fam["title"])
    desc = (f"{len(all_items)} PC portables 2026 classés par usage avec une note presse moyenne sur 10 : bureautique, création, gaming, polyvalent, low-cost."
            if fam["key"] == "laptop" else f"{len(all_items)} ordinateurs de bureau 2026 classés par usage avec une note presse sur 10 et un prix indicatif : bureautique, création, gaming, mini-PC, tout-en-un."
            if fam["key"] == "desktop" else fam["desc"])
    write(f"{fam['slug']}/index.html", page(root, title, desc, f"{fam['slug']}/", body, fam["slug"], js_data(sel, root, by_cat[cats[0]["key"]][0]["id"]),
          ld=[ld_crumbs(("Accueil", ""), (fam["plural"], f"{fam['slug']}/")), ld_faq(fam_faq(fam)),
              {"@type": "ItemList", "name": plain(fam["h1"]), "itemListElement": [
                  {"@type": "ListItem", "position": i, "name": plain(c["h"]), "url": f"{DOMAIN}/{fam['slug']}/{c['slug']}/"} for i, c in enumerate(cats, 1)]}]))


# ---------------------------------------------------------------- Bloc « Notre choix » + alternatives par priorité
def few(d, cls="few"):
    """Pastille d'alerte quand la note presse repose sur moins de 3 notes."""
    pr = d["press"]
    if not pr or pr["n"] >= 3:
        return ""
    txt = "1 seul test noté" if pr["n"] == 1 else "2 tests notés seulement"
    return f'<span class="{cls}" title="Note presse calculée sur {pr["n"]} note{"s" if pr["n"] > 1 else ""} seulement : à prendre avec prudence.">{txt}</span>'


def press_big(d, short=False):
    pr, ts = d["press"], d["tests"]
    gam = " · gamme" if ts["scope"] == "gamme" else ""
    if pr:
        return f'<span class="pn">{fr(pr["avg"])}</span><span class="pd">/10</span><span class="pc">note presse · {pr["n"]} note{"s" if pr["n"] > 1 else ""}{gam}</span>{few(d)}'
    return f'<span class="pn none">—</span><span class="pc">{ts["tests"]} test{"s" if ts["tests"] > 1 else ""} presse, sans note chiffrée{gam}</span>'


def weight_kg(d):
    m = re.search(r"(\d+(?:,\d+)?)\s*kg", d["m"][0])
    return float(m.group(1).replace(",", ".")) if m else None


def alternatives(fam, items):
    """Trois alternatives au choix n° 1, chacune pour une priorité différente — calculées sur les données, pas rédigées."""
    rest, out, used = items[1:], [], set()

    def take(label, cands, why):
        for d in cands:
            if d["id"] not in used:
                used.add(d["id"]); out.append((label, d, why(d))); return
    def sup(d, key, best, among):
        """Superlatif seulement s'il est vrai sur toute la sélection (choix n° 1 compris)."""
        return best if key(d) == min(key(x) for x in items) else among
    take("Le prix", sorted(rest, key=lambda d: d["p"]), lambda d: f"{sup(d, lambda x: x['p'], 'Le moins cher', 'Parmi les moins chers')} : {d['price_txt']}")
    solid = [d for d in rest if d["press"] and d["press"]["n"] >= 3] or [d for d in rest if d["press"]]
    take("La note presse", sorted(solid, key=lambda d: (-d["press"]["avg"], -d["press"]["n"])),
         lambda d: f"{sup(d, lambda x: -(x['press']['avg'] if x['press'] else 0), 'La meilleure note : ', '')}{fr(d['press']['avg'])}/10 sur {d['press']['n']} note{'s' if d['press']['n'] > 1 else ''}")
    if fam["key"] == "laptop":
        take("Le poids", sorted([d for d in rest if weight_kg(d)], key=weight_kg), lambda d: f"{sup(d, lambda x: weight_kg(x) or 99, 'Le plus léger', 'Parmi les plus légers')} : {d['m'][0]}")
    else:
        take("Le recul", sorted(rest, key=lambda d: -d["tests"]["tests"]), lambda d: f"{sup(d, lambda x: -x['tests']['tests'], 'Le plus testé', 'Parmi les plus testés')} : {d['tests']['tests']} tests presse")
    return out


def pick_block(fam, c, items, root):
    d = items[0]
    best = d["offers"][0]
    why = "".join(f"<li>{E(x)}</li>" for x in d["strengths"][:3])
    warn = f'<li class="warn">{E(d["weak"][0])}</li>' if d["weak"] else ""
    photo = (f'<a class="pick-photo" href="{root}{d["purl"]}"><img src="{root}assets/img/p/{d["img"]}" alt="{E(d["short"])}" width="560" height="420"></a>' if d["img"] else "")
    alts = []
    for label, a, reason in alternatives(fam, items):
        apr = a["press"]
        meta = (f'{fr(apr["avg"])}/10 presse · ' if apr else "") + a["price_txt"]
        alts.append(f'''<a class="alt-card" href="#{a['id']}">
      <span class="alt-k">{label}</span>
      {f'<img src="{root}assets/img/p/{a["img"]}" alt="" width="96" height="72" loading="lazy">' if a['img'] else ''}
      <b>{E(a['short'])}</b><span class="alt-why">{E(reason)}</span><span class="alt-meta">{meta}</span></a>''')
    return f"""<section class="pick" id="notre-choix">
    <div class="pick-card">
      {photo}
      <div class="pick-body">
        <span class="fbadge">Notre choix · {c['label']}</span>
        <h2><a href="{root}{d['purl']}">{E(d['short'])}</a></h2>
        <p class="pick-verdict">{E(d['verdict'])}</p>
        <ul class="pick-why">{why}{warn}</ul>
      </div>
      <div class="pick-buy">
        <div class="press-big">{press_big(d)}</div>
        <div class="pick-price"><b>{d['price_txt']}</b><span>{ind_txt(fam)}</span></div>
        <a class="cta big buy" href="{E(best['url'])}" target="_blank" rel="{rel_m(best['m'])}">Voir chez {E(best['m'])} →</a>
        <a class="see-all" href="{root}{d['purl']}">Avis et tests détaillés →</a>
      </div>
    </div>
    <div class="pick-alt">
      <div class="legend-title">Vous privilégiez autre chose ?</div>
      <div class="alt-grid">{''.join(alts)}</div>
    </div>
  </section>"""


def sort_bar(fam):
    return """<div class="sort-bar"><label class="filter-label" for="sortBy">Trier par</label>
      <select id="sortBy" class="sort-select">
        <option value="rank">Notre classement</option>
        <option value="press">Note presse</option>
        <option value="price-asc">Prix croissant</option>
        <option value="price-desc">Prix décroissant</option>
        <option value="tests">Nombre de tests presse</option>
      </select></div>"""


# ---------------------------------------------------------------- Pages usage
def usage_page(fam, c):
    root = "../../"
    items = by_cat[c["key"]]
    n = len(items)
    _s = {}
    for d in items:
        _s[d["id"]] = d["tests"]["n"]
    n_notes, tested = sum(_s.values()), sum(d["tests"]["tests"] for d in items)
    fiches = []
    for i, d in enumerate(items, 1):
        pr, ts = d["press"], d["tests"]
        gam = " · gamme" if ts["scope"] == "gamme" else ""
        if pr:
            big = f'<span class="pn">{fr(pr["avg"])}</span><span class="pd">/10</span><span class="pc">note presse · {pr["n"]} note{"s" if pr["n"] > 1 else ""}{gam}</span>{few(d)}'
        else:
            big = f'<span class="pn none">—</span><span class="pc">{ts["tests"]} test{"s" if ts["tests"] > 1 else ""} presse, sans note chiffrée{gam}</span>'

        def note_li(nt):
            name = E(nt["src"])
            if nt.get("url"):
                name = f'<a href="{E(nt["url"])}" target="_blank" rel="noopener nofollow">{name}</a>'
            val = f'<b>{fr(nt["score"])}</b>' if nt["score"] is not None else '<b class="nn">test</b>'
            return f"<li><span>{name}</span>{val}</li>"
        lis = "".join(note_li(nt) for nt in ts["notes"])
        src = f'<p class="src">Source : <a href="{E(ts["src"][1])}" target="_blank" rel="noopener nofollow">{E(ts["src"][0])}</a>{" — notes portant sur la gamme (configurations ou générations proches)." if gam else ""}</p>' if ts["src"][1] else ""
        lab = (f'Détail des {ts["tests"]} tests presse' if ts["tests"] > 1 else "Le test presse") + (f' ({pr["n"]} note{"s" if pr["n"] > 1 else ""})' if pr and pr["n"] != ts["tests"] else "")
        det = f'<details{" open" if ts["tests"] <= 2 else ""}><summary>{lab}</summary><ul class="notes-list">{lis}</ul>{src}</details>'
        st = "".join(f'<span class="s">{E(x)}</span>' for x in d["strengths"])
        wk = "".join(f'<span class="s">{E(x)}</span>' for x in d["weak"]) or '<span class="s muted">Aucun défaut majeur relevé par la presse</span>'
        offs = "".join(
            f'<a class="offer m-{MERCHANT_CLS.get(o["m"], "x")}" href="{E(o["url"])}" target="_blank" rel="{rel_m(o["m"])}" title="{E(o["name"])}">'
            f'<span class="o-m">{E(o["m"])}</span><span class="o-c">{E(o.get("cfg") or "")}</span><span class="o-go">Voir →</span></a>' for o in d["offers"])
        offers_html = f'<div class="offers"><span class="k">Où l\'acheter</span>{offs}<p class="o-note">La configuration peut différer d\'un marchand à l\'autre : vérifiez la fiche avant d\'acheter.</p></div>'
        rating = f'{fr(d["r"])} ★ <small>({d["nrev"]})</small>' if d["r"] > 0 else ""
        rank_lbl = "NOTRE CHOIX" if i == 1 else f"SUR {n}"
        photo = (f'<a class="f-photo" href="{E(d["url"])}" target="_blank" rel="{rel_m(d["offers"][0]["m"])}"><img src="../../assets/img/p/{d["img"]}" alt="{E(d["short"])}" width="560" height="420" loading="lazy"></a>' if d["img"] else "")
        best = d["offers"][0]
        fiches.append(f"""<article class="fiche v7{' top' if i == 1 else ''}" id="{d['id']}" data-budget="{d['bucket']}" data-rank="{i}" data-price="{d['p']}" data-press="{pr['avg'] if pr else -1}" data-tests="{ts['tests']}">
  {'<img class="stamp" src="../../assets/img/stamp-choix.webp" alt="Le choix de la bande" width="92" height="92" loading="lazy">' if i == 1 and d['badge'] == 'Le choix de la bande' else ''}
  <div class="rank">#{i}<small>{rank_lbl}</small></div>
  <div class="f-main">
    <span class="fbadge{' alt' if i != 1 else ''}">{E(d['badge'])}</span>
    <h3><a href="{root}{d['purl']}">{E(d['short'])}</a></h3>
    <div class="ref">{E(d['ref'])}</div>
    <p class="lead-line"><b>En bref.</b> {E(d['verdict'])}</p>
    <button type="button" class="f-toggle" aria-expanded="false" aria-controls="x-{d['id']}">Points forts, points faibles et tests</button>
    <div class="f-x" id="x-{d['id']}">
    <div class="pc-grid">
      <div class="strengths"><span class="pc-t pro">Points forts</span>{st}</div>
      <div class="strengths weak"><span class="pc-t con">Points faibles</span>{wk}</div>
    </div>
    {offers_html}
    {det}
    <a class="see-all f-more" href="{root}{d['purl']}">{E(d['short'])} : avis et tests détaillés →</a>
    </div>
  </div>
  <div class="f-side">
    {photo}
    <div class="press-big">{big}</div>
    <div class="mini"><span class="k">Prix indicatif</span><span class="v">{d['price_txt']}</span></div>
    <div class="f-x f-xs">
    {mini(fam['m_labels'][0], E(d['m'][0]))}
    {mini(fam['m_labels'][1], E(d['m'][1]))}
    {('<div class="mini"><span class="k">Avis clients Darty</span><span class="v">' + rating + '</span></div>') if rating else ''}
    </div>
    <a class="cta" href="{E(best['url'])}" target="_blank" rel="{rel_m(best['m'])}">Voir chez {E(best['m'])} →</a>
  </div>
</article>""")
    mascot = ('<img class="hero-badge tall" src="../../assets/img/pose-lowcost.webp" alt="La mascotte avec un PC en promo" width="170" height="260">' if c["key"] == "lowcost"
              else f'<img class="hero-badge" src="../../assets/img/badge-{c["badge"]}.webp" alt="" width="190" height="190">')
    # peu de notes publiques (imprimantes : notes des associations réservées aux abonnés) :
    # on met en avant les tests de laboratoire plutôt qu'un « 0 notes compilées » trompeur
    labs = sum(1 for d in items for x in (d["tests"] or {}).get("notes", []) if x["src"] in ASSOC)
    if n_notes < 3 and labs:
        third_stat = f'<div><strong>{labs}</strong>tests en laboratoire (associations)</div>'
    else:
        third_stat = f'<div><strong>{n_notes}</strong>note{"s" if n_notes > 1 else ""} compilée{"s" if n_notes > 1 else ""}</div>'
    top_word = f"Le top 10 {c['label'].lower()}" if n == 10 else f"Notre sélection {c['label'].lower()}"
    body = f"""
  <div class="crumb"><a href="../../">Accueil</a> › <a href="../">{fam['plural']}</a> › {c['label']}</div>
  <section class="usage-hero">
    <div>
      <div class="eyebrow">{c['tag'].upper()} · MAJ {maj(fam)}</div>
      <h1>{c['h1']}</h1>
      <p>{c['intro']} <b>Classement :</b> notre choix en tête, puis par note presse.</p>
      <p class="hero-links"><a href="#top10">Voir le classement complet ↓</a> · <a href="#guide">Lire le guide d'achat</a></p>
      <div class="spec-row">
        <div><strong>{n}</strong>{fam.get('plural_low', fam['plural'].lower())} sélectionné{'e' if fam['key'] == 'imprimante' else ''}s</div>
        <div><strong>{tested}</strong>tests presse recensés</div>{third_stat}
      </div>
    </div>
    {mascot}
  </section>
  {PROVISIONAL_NOTE if fam['provisional'] else ''}
  {pick_block(fam, c, items, root)}

  <section class="comparator" id="comparateur">
    <div class="comparator-head">
      <div><h2>{'Les 10' if n == 10 else 'La sélection'} en un coup d'œil</h2>
      <p class="comparator-sub"><b>À droite : bien noté par la presse. En bas : moins cher.</b> Les bonnes affaires sont en bas à droite. Filtrez par budget, cliquez sur une bulle pour lire le verdict.</p></div>
      <img class="comparator-pose" src="../../assets/img/pose-investigation.webp" alt="" width="88" height="88">
    </div>
    {budget_filter(items)}
    <div class="comparator-grid">
      <div class="chart-col">
        <div class="chart-pane">{bubble_svg(items, "Graphe à bulles : note presse contre prix, taille selon le nombre de tests")}</div>
        <div class="legend-strip">{LEGEND}</div>
      </div>
      {detail_card(root, fam)}
    </div>
  </section>
  {guide_html(c['key'])}

  <section class="section" id="top10" style="border-bottom:none;">
    <div class="section-head"><h2><img class="section-badge" src="../../assets/img/badge-{c['badge']}.webp" alt="" width="50" height="50">{top_word}</h2><div class="tag">Notre choix, puis note presse</div></div>
    {sort_bar(fam)}
    <div class="top-list" id="topList">{''.join(fiches)}</div>
  </section>
"""
    if fam["key"] == "laptop":
        title = f"Top 10 PC portables {c['label'].lower()} 2026 : tests résumés et verdict | Top 10 Geek"
        desc = f"Les 10 meilleurs PC portables {c['label'].lower()} en 2026, classés par note presse, avec photos, prix indicatif, poids, points forts et points faibles."
    elif fam["key"] == "desktop":
        title = f"Top 10 {'mini-PC' if c['key'] == 'd-mini' else 'tout-en-un' if c['key'] == 'd-aio' else 'ordinateurs de bureau ' + c['label'].lower()} 2026 : tests résumés et prix | Top 10 Geek"
        desc = f"Les 10 meilleurs ordinateurs de bureau {c['label'].lower()} en 2026, classés par note presse, avec photos, prix indicatif, points forts et points faibles."
    else:
        lab = (plain(c["h"]).lower().replace("écrans portables", "portables").replace("imprimantes photo", "photo")
               .replace("réservoirs d'encre", "à réservoirs d'encre").replace(" & télétravail", ""))
        title = fam["usage_title"].format(label=lab)
        desc = fam["usage_desc"].format(label=lab)
    write(f"{fam['slug']}/{c['slug']}/index.html", page(root, title, desc, f"{fam['slug']}/{c['slug']}/", body, fam["slug"], js_data(items, root, items[0]["id"]),
          ld=[ld_crumbs(("Accueil", ""), (fam["plural"], f"{fam['slug']}/"), (c["label"], f"{fam['slug']}/{c['slug']}/")),
              {"@type": "ItemList", "name": plain(c["h1"]), "numberOfItems": n, "itemListOrder": "https://schema.org/ItemListOrderAscending",
               "itemListElement": [{"@type": "ListItem", "position": i, "name": d["short"], "url": f"{DOMAIN}/{d['purl']}"} for i, d in enumerate(items, 1)]}]))


for fam in FAMILIES:
    family_page(fam)
    for c in fam["cats"]:
        usage_page(fam, c)

# ---------------------------------------------------------------- Fiches produits (une adresse par ordinateur)
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def brand_of(short):
    return "Alienware" if short.startswith("Alienware") else short.split()[0]


def low_first(t):
    return t[0].lower() + t[1:] if t else t


def product_page(fam, c, rank, d, items):
    root = "../../"
    pr, ts = d["press"], d["tests"]
    name = E(d["short"])
    best = d["offers"][0]
    n_items = len(items)
    scored = [nt for nt in ts["notes"] if nt["score"] is not None]
    medias = len({nt["src"] for nt in ts["notes"]})
    gam = ts["scope"] == "gamme"

    # --- consensus chiffré
    if pr:
        hi, lo = max(scored, key=lambda x: x["score"]), min(scored, key=lambda x: x["score"])
        good = sum(1 for x in scored if x["score"] >= 8)
        if len(scored) == 1:
            cons = f'Une seule note chiffrée à ce jour : <b>{fr(hi["score"])}/10</b>, attribuée par {E(hi["src"])}. À lire comme un avis isolé, pas comme un consensus.'
        elif hi["score"] == lo["score"]:
            cons = f'Les {len(scored)} notes relevées sont identiques : <b>{fr(hi["score"])}/10</b>.'
        else:
            cons = (f'Sur {len(scored)} notes, <b>{good}</b> {"atteint" if good == 1 else "atteignent"} ou {"dépasse" if good == 1 else "dépassent"} 8/10. '
                    f'La plus haute : <b>{fr(hi["score"])}/10</b> ({E(hi["src"])}) ; la plus basse : <b>{fr(lo["score"])}/10</b> ({E(lo["src"])}).')
        stats = (f'<div><strong>{fr(pr["avg"])}/10</strong>note presse moyenne</div><div><strong>{pr["n"]}</strong>note{"s" if pr["n"] > 1 else ""} chiffrée{"s" if pr["n"] > 1 else ""}</div>'
                 f'<div><strong>{ts["tests"]}</strong>test{"s" if ts["tests"] > 1 else ""} recensé{"s" if ts["tests"] > 1 else ""}</div><div><strong>{medias}</strong>média{"s" if medias > 1 else ""}</div>')
    else:
        cons = f'{"Les tests recensés ne donnent" if ts["tests"] > 1 else "Le test recensé ne donne"} pas de note chiffrée : nous renvoyons vers {"les articles" if ts["tests"] > 1 else "l&#39;article"} plutôt que d&#39;inventer une note.'
        stats = f'<div><strong>{ts["tests"]}</strong>test{"s" if ts["tests"] > 1 else ""} recensé{"s" if ts["tests"] > 1 else ""}</div><div><strong>{medias}</strong>média{"s" if medias > 1 else ""}</div><div><strong>—</strong>sans note chiffrée</div>'
    if gam:
        cons += " Ces notes portent sur la gamme : configurations ou générations proches de celle vendue aujourd&#39;hui."
    dates = sorted(nt["date"] for nt in ts["notes"] if nt.get("date"))
    last = f'Dernier test relevé : {MOIS[int(dates[-1][5:7]) - 1]} {dates[-1][:4]}.' if dates else ""

    def note_li(nt):
        nm = E(nt["src"])
        if nt.get("url"):
            nm = f'<a href="{E(nt["url"])}" target="_blank" rel="noopener nofollow">{nm}</a>'
        val = f'<b>{fr(nt["score"])}</b>' if nt["score"] is not None else '<b class="nn">test</b>'
        return f"<li><span>{nm}</span>{val}</li>"
    notes = "".join(note_li(nt) for nt in ts["notes"])
    src = f'<p class="src">Source du relevé : <a href="{E(ts["src"][1])}" target="_blank" rel="noopener nofollow">{E(ts["src"][0])}</a>.</p>' if ts["src"][1] else ""

    st = "".join(f'<span class="s">{E(x)}</span>' for x in d["strengths"])
    wk = "".join(f'<span class="s">{E(x)}</span>' for x in d["weak"]) or '<span class="s muted">Aucun défaut majeur relevé par la presse</span>'
    offs = "".join(
        f'<a class="offer m-{MERCHANT_CLS.get(o["m"], "x")}" href="{E(o["url"])}" target="_blank" rel="{rel_m(o["m"])}" title="{E(o["name"])}">'
        f'<span class="o-m">{E(o["m"])}</span><span class="o-c">{E(o.get("cfg") or "")}</span><span class="o-go">Voir chez {E(o["m"])} →</span></a>' for o in d["offers"])
    specs = "".join(f"<div class=\"mini{' wide' if k.startswith(('Config', 'Caract')) else ''}\"><span class=\"k\">{k}</span><span class=\"v\">{v}</span></div>" for k, v in [
        ("Configuration de référence" if fam["key"] in ("laptop", "desktop") else "Caractéristiques principales", E(d["ref"])), (fam["m_labels"][0], E(d["m"][0])), (fam["m_labels"][1], E(d["m"][1])),
        ("Avis clients Darty", f'{fr(d["r"])} ★ ({d["nrev"]} avis)' if d["r"] > 0 else "")] if v and v != "n.c.")

    # --- alternatives : les voisins du classement
    others = [x for x in items if x["id"] != d["id"]]
    near = sorted(others, key=lambda x: (abs(items.index(x) - (rank - 1)), items.index(x)))[:3]
    near.sort(key=lambda x: items.index(x))
    alt = "".join(f"""<a class="alt-card" href="{root}{a['purl']}">
      <span class="alt-k">N° {items.index(a) + 1} · {E(a['badge'])}</span>
      {f'<img src="{root}assets/img/p/{a["img"]}" alt="" width="96" height="72" loading="lazy">' if a['img'] else ''}
      <b>{E(a['short'])}</b><span class="alt-why">{E(a['verdict'])}</span>
      <span class="alt-meta">{(fr(a['press']['avg']) + '/10 presse · ') if a['press'] else ''}{a['price_txt']}</span></a>""" for a in near)

    usage_txt = f"{fam['plural']} {c['label'].lower()}" if c["key"] not in ("d-mini", "d-aio") else ("mini-PC" if c["key"] == "d-mini" else "ordinateurs tout-en-un")
    usage_url = f"{root}{fam['slug']}/{c['slug']}/"
    rank_txt = (f'<b>Notre choix</b> dans le <a href="{usage_url}">top {n_items} {usage_txt}</a>' if rank == 1
                else f'<b>N° {rank} sur {n_items}</b> dans le <a href="{usage_url}">top {n_items} {usage_txt}</a>')

    # --- FAQ (réponses tirées des données affichées plus haut)
    marchands = [o["m"] for o in d["offers"]]
    ou = (" et ".join([", ".join(marchands[:-1]), marchands[-1]]) if len(marchands) > 1 else marchands[0])
    if pr:
        a1 = (f'La note presse moyenne est de {fr(pr["avg"])}/10, calculée sur {pr["n"]} note{"s" if pr["n"] > 1 else ""}'
              + (f' (de {fr(lo["score"])} à {fr(hi["score"])}/10)' if len(scored) > 1 and hi["score"] != lo["score"] else "") + f'. {E(d["verdict"])}')
    else:
        a1 = f'{ts["tests"]} test{"s" if ts["tests"] > 1 else ""} presse recensé{"s" if ts["tests"] > 1 else ""}, sans note chiffrée. {E(d["verdict"])}'
    faq = [
        (f"Que pense la presse de {fam['noun_det']} {name} ?" if fam["key"] not in ("laptop", "desktop") else f"Que pense la presse de l'ordinateur {name} ?", a1),
        (f"Quels sont les points faibles relevés par les tests ?", (" ; ".join(E(x) for x in d["weak"]) + ".") if d["weak"] else "La presse ne relève aucun défaut majeur."),
        (f"À qui s'adresse le modèle {name} ?", f'{E(d["pour"])} À éviter si : {low_first(E(d["eviter"]))}'),
        (f"Où l'acheter, et à quel prix ?", f'Comptez environ {euro_ind(d["p"])} (prix indicatif constaté en {pdate(fam)}). Nous l&#39;avons trouvé en vente chez {E(ou)}. Les prix changent vite et la configuration peut différer d&#39;un marchand à l&#39;autre : seul le prix affiché par le marchand fait foi.'),
    ]
    faq_html = "".join(f'<details class="faq-item"{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(faq))

    body = f"""
  <div class="crumb"><a href="{root or "./"}">Accueil</a> › <a href="{root}{fam['slug']}/">{fam['plural']}</a> › <a href="{usage_url}">{c['label']}</a> › {name}</div>
  <section class="p-hero">
    <div class="p-text">
      <div class="eyebrow">{E(d['badge']).upper()} · MAJ {maj(fam)}</div>
      <h1>{name} : <span class="flash">avis, tests et prix</span></h1>
      <div class="ref">{E(d['ref'])}</div>
      <p class="p-verdict"><b>Le verdict en une phrase.</b> {E(d['verdict'])}</p>
      <p class="p-rank">{rank_txt}.</p>
    </div>
    <div class="p-side">
      {f'<div class="f-photo"><img src="{root}assets/img/p/{d["img"]}" alt="{name}" width="560" height="420" fetchpriority="high"></div>' if d['img'] else ''}
      <div class="press-big">{press_big(d)}</div>
      <div class="pick-price"><b>{d['price_txt']}</b><span>{ind_txt(fam)}</span></div>
      <a class="cta big buy" href="{E(best['url'])}" target="_blank" rel="{rel_m(best['m'])}">Voir chez {E(best['m'])} →</a>
    </div>
  </section>

  <section class="section p-sec" id="pour-qui">
    <div class="section-head"><h2>Pour qui ?</h2><div class="tag">En deux lignes</div></div>
    <div class="who-grid">
      <div class="who yes"><span class="pc-t pro">Fait pour vous si</span><p>{E(d['pour'])}</p></div>
      <div class="who no"><span class="pc-t con">À éviter si</span><p>{E(d['eviter'])}</p></div>
    </div>
  </section>

  <section class="section p-sec" id="consensus">
    <div class="section-head"><h2>Le consensus de la presse</h2><div class="tag">{ts['tests']} test{'s' if ts['tests'] > 1 else ''} lu{'s' if ts['tests'] > 1 else ''}</div></div>
    <div class="spec-row">{stats}</div>
    <p class="p-cons">{cons} {last}</p>
    <div class="pc-grid p-pc">
      <div class="strengths"><span class="pc-t pro">Ce que la presse apprécie</span>{st}</div>
      <div class="strengths weak"><span class="pc-t con">Les réserves qui reviennent</span>{wk}</div>
    </div>
  </section>

  <section class="section p-sec" id="prix">
    <div class="section-head"><h2>Où l'acheter</h2><div class="tag">Environ {euro_ind(d['p'])} · {ind_txt(fam)}</div></div>
    <div class="offers p-offers">{offs}<p class="o-note">La configuration peut différer d'un marchand à l'autre : vérifiez la fiche avant d'acheter. Seuls les liens {AFF_TXT} sont affiliés à ce jour ; les autres sont de simples liens directs. Aucun n'influence les notes ni le classement.</p></div>
    <div class="p-specs">{specs}</div>
  </section>

  <section class="section p-sec" id="tests">
    <div class="section-head"><h2>Tous les tests recensés</h2><div class="tag">Sources</div></div>
    <p class="p-cons">Chaque ligne renvoie vers le test d'origine. Les notes sont converties sur 10 ; « test » signale un article sans note chiffrée. <a href="{root}methode">Notre méthode</a>.</p>
    <ul class="notes-list p-notes">{notes}</ul>
    {src}
  </section>

  <section class="section p-sec" id="alternatives">
    <div class="section-head"><h2>Les alternatives pour le même usage</h2><a class="see-all" href="{usage_url}">Tout le top {n_items} →</a></div>
    <div class="alt-grid">{alt}</div>
  </section>

  <section class="section p-sec" id="faq" style="border-bottom:none;">
    <div class="section-head"><h2>Questions fréquentes</h2><div class="tag">FAQ</div></div>
    <div class="faq-list">{faq_html}</div>
    <p class="p-final"><a class="cta big buy" href="{E(best['url'])}" target="_blank" rel="{rel_m(best['m'])}">Voir chez {E(best['m'])} →</a> <a class="see-all" href="{usage_url}">Revenir au classement</a></p>
  </section>
"""
    note_t = f' ({fr(pr["avg"])}/10 presse)' if pr else ""
    title = f'{d["short"]} : avis, tests et prix{note_t} | Top 10 Geek'
    lead = (f'{pr["n"]} note{"s" if pr["n"] > 1 else ""} presse, moyenne {fr(pr["avg"])}/10. ' if pr else f'{ts["tests"]} test{"s" if ts["tests"] > 1 else ""} presse résumé{"s" if ts["tests"] > 1 else ""}. ')
    desc = lead + d["verdict"]
    if len(desc) > 158:
        desc = desc[:155].rsplit(" ", 1)[0] + "…"
    ind = int(euro_ind(d["p"]).replace(" ", "").replace("€", ""))
    product = {"@type": "Product", "@id": f"{DOMAIN}/{d['purl']}#produit", "name": d["short"], "description": d["verdict"],
               "brand": {"@type": "Brand", "name": brand_of(d["short"])}, "category": f"{fam['label']} · {c['label']}",
               "url": f"{DOMAIN}/{d['purl']}",
               # Pas d'AggregateRating : Google réserve ce balisage aux notes collectées sur le site lui-même, pas aux notes de la presse.
               # Prix indicatif affiché sur la page (arrondi), sans offre ni prix par marchand.
               "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": f"{ind:.2f}", "offerCount": len(d["offers"])}}
    if d["img"]:
        product["image"] = f"{DOMAIN}/assets/img/p/{d['img']}"
    write(d["purl"] + "index.html", page(root, title, desc, d["purl"], body, fam["slug"],
                                         og_img=(f'assets/img/p/{d["img"]}' if d["img"] else "assets/img/og-image.jpg"),
                                         ld=[ld_crumbs(("Accueil", ""), (fam["plural"], f"{fam['slug']}/"), (c["label"], f"{fam['slug']}/{c['slug']}/"), (d["short"], d["purl"])),
                                             product, ld_faq(faq)]))


for fam in FAMILIES:
    for c in fam["cats"]:
        for i, d in enumerate(by_cat[c["key"]], 1):
            product_page(fam, c, i, d, by_cat[c["key"]])

# ---------------------------------------------------------------- Page d'accueil
def champion(items):
    """Champion d'accueil : le mieux classé dont la note repose sur au moins 3 notes presse ;
    à défaut, celui dont la note s'appuie sur le plus de notes."""
    solid = [d for d in items if d["press"] and d["press"]["n"] >= 3]
    if solid:
        return solid[0]
    rated = [d for d in items if d["press"]]
    return max(rated, key=lambda d: (d["press"]["n"], d["press"]["avg"])) if rated else items[0]


champions = [champion(by_cat[c["key"]]) for f in FAMILIES for c in f["cats"]]
laptop_count = sum(1 for d in ITEMS.values() if d["family"] == "laptop")
desk_count = sum(1 for d in ITEMS.values() if d["family"] == "desktop")


def champ_card(d):
    c = CAT[d["cat"]]
    pr = d["press"]
    score = (f'<span class="ch-score"><b>{fr(pr["avg"])}</b><small>/10</small><em>{pr["n"]} note{"s" if pr["n"] > 1 else ""} presse</em></span>' if pr
             else '<span class="ch-score none"><b>Testé</b><em>sans note chiffrée</em></span>')
    return f"""<a class="champ" href="{d['href']}" style="--c:{c['color']}">
  <span class="ch-top"><span class="ch-usage"><span class="dot {c['cls'].replace('f-', '')}"></span>{c['label']}</span><img src="assets/img/badge-{c['badge']}.webp" alt="" width="64" height="64" loading="lazy"></span>
  {f'<img class="ch-photo" src="assets/img/p/{d["img"]}" alt="{E(d["short"])}" width="560" height="420" loading="lazy">' if d['img'] else ''}
  <span class="ch-name">{E(d['short'])}</span>
  <span class="ch-verdict">{E(d['verdict'])}</span>
  <span class="ch-bottom">{score}<span class="ch-price">{d['price_txt']}</span></span>
  {few(d, "few ch-few")}<span class="ch-go">Voir le classement →</span>
</a>"""


def ticker():
    tops = sorted([d for d in ITEMS.values() if d["press"] and d["press"]["n"] >= 5], key=lambda d: -d["press"]["avg"])[:12]
    items = "".join(f'<span class="tk-item"><b>{E(d["short"])}</b> {fr(d["press"]["avg"])}/10 <small>· {d["press"]["n"]} notes</small></span>' for d in tops)
    return f'<div class="ticker" aria-hidden="true"><div class="tk-track">{items}{items}</div></div>'


radar_items = [by_cat[c["key"]][i] for c in LCATS for i in (0, 1, 2)]
SOON_IMG = ["soon-smartphone", "soon-casque", "soon-tablette"]
SOON = [("Smartphones", "Les meilleurs téléphones par budget, notes presse à l'appui."),
        ("Casques &amp; écouteurs", "Réduction de bruit, sport, gaming : le son sans se tromper."), ("Tablettes", "iPad, Android, Windows : laquelle pour lire, dessiner ou travailler ?")]

ICON = {
    "laptop": '<path d="M5 6h14v9H5z"/><path d="M2.5 18.5h19"/>',
    "desktop": '<rect x="3" y="4" width="13" height="10" rx="1"/><path d="M9.5 14v3M6.5 17h6"/><rect x="18" y="6" width="3.5" height="11" rx="0.8"/>',
    "ecran": '<rect x="2.5" y="4" width="19" height="12" rx="1"/><path d="M12 16v3.5M8 19.5h8"/>',
    "imprimante": '<path d="M7 9V3.5h10V9"/><rect x="3" y="9" width="18" height="7.5" rx="1.2"/><path d="M7 14h10v6.5H7z"/>',
}
def fam_btn(fam):
    n = sum(len(by_cat[c["key"]]) for c in fam["cats"])
    return (f'<a class="fam-btn" href="{fam["slug"]}/"><span class="fb-ic"><svg viewBox="0 0 24 24" aria-hidden="true">{ICON[fam["key"]]}</svg></span>'
            f'<span class="fb-txt"><b>{fam["plural"]}</b><small>{len(fam["cats"])} usages · {n} modèles</small></span><span class="fb-go" aria-hidden="true">→</span></a>')
FAM_BTNS = "\n        ".join(fam_btn(f) for f in FAMILIES)

home = f"""
  <section class="home-hero">
    <div class="hh-text">
      <div class="eyebrow">LE COMPARATEUR QUI A LU TOUS LES TESTS · MAJ {MAJ}</div>
      <h1>Tous les tests high&#8209;tech, <span class="flash">résumés pour vous.</span></h1>
      <p>Nous lisons les tests de la presse spécialisée, nous en tirons une <b>note presse sur 10</b> et nous vous disons, usage par usage, quoi acheter — et pourquoi. Sans jargon, sans pub déguisée.</p>
      <nav class="fam-btns" aria-label="Nos comparatifs">
        {FAM_BTNS}
      </nav>
      <div class="spec-row">
        <div><strong>{TOTAL_TESTS}</strong>tests presse recensés</div>
        <div><strong>{len(ITEMS)}</strong>produits sélectionnés</div>
        <div><strong>{len(CAT)}</strong>usages couverts</div>
      </div>
    </div>
    <div class="hh-visual">
      <div class="hh-blob"></div>
      <img class="hh-mascot" src="assets/img/mascotte-persona-v2.webp" alt="La mascotte de Top 10 Geek" width="800" height="800" fetchpriority="high">
      <img class="hh-sticker s1" src="assets/img/badge-gaming.webp" alt="" width="120" height="120">
      <img class="hh-sticker s2" src="assets/img/badge-creation.webp" alt="" width="120" height="120">
      <img class="hh-sticker s3" src="assets/img/badge-bureautique.webp" alt="" width="120" height="120">
      <div class="hh-bubble">« J'ai lu {TOTAL_TESTS} tests pour vous. De rien. »</div>
    </div>
  </section>

  {ticker()}

  <section class="section">
    <div class="section-head"><h2>Les champions du moment</h2><div class="tag">Les mieux notés par la presse, par usage</div></div>
    <div class="family-row">
      <div class="fr-head"><h3>PC portables</h3><a class="see-all" href="pc-portable/">Tout le comparatif →</a></div>
      <p class="champ-hint">← Faites glisser pour voir les 5 usages →</p><div class="champ-grid">{''.join(champ_card(d) for d in champions if d['family'] == 'laptop')}</div>
    </div>
    <div class="family-row">
      <div class="fr-head"><h3>Ordinateurs de bureau</h3><a class="see-all" href="ordinateur-de-bureau/">Tout le comparatif →</a></div>
      <p class="champ-hint">← Faites glisser pour voir les 5 usages →</p><div class="champ-grid">{''.join(champ_card(d) for d in champions if d['family'] == 'desktop')}</div>
    </div>
    <div class="family-row">
      <div class="fr-head"><h3>Écrans PC</h3><a class="see-all" href="ecran-pc/">Tout le comparatif →</a></div>
      <p class="champ-hint">← Faites glisser pour voir les 5 usages →</p><div class="champ-grid">{''.join(champ_card(d) for d in champions if d['family'] == 'ecran')}</div>
    </div>
    <div class="family-row">
      <div class="fr-head"><h3>Imprimantes</h3><a class="see-all" href="imprimante/">Tout le comparatif →</a></div>
      <p class="champ-hint">← Faites glisser pour voir les 5 usages →</p><div class="champ-grid">{''.join(champ_card(d) for d in champions if d['family'] == 'imprimante')}</div>
    </div>
  </section>

  <section class="section radar">
    <div class="radar-grid">
      <div class="radar-text">
        <div class="eyebrow">LE RADAR DES BONNES AFFAIRES · PC PORTABLES</div>
        <h2>Bien noté <span class="flash">et</span> pas trop cher&nbsp;? C'est en bas à droite.</h2>
        <p>Chaque bulle est l'un des 3 meilleurs PC portables de chaque usage. Plus elle est à droite, plus la presse l'a aimé ; plus elle est basse, plus il est abordable ; plus elle est grosse, plus la note repose sur de nombreux tests. Cliquez sur une bulle pour ouvrir sa fiche.</p>
        <div class="legend-cats">{''.join(f'<div class="legend-cat"><span class="dot {c["cls"].replace("f-", "")}"></span>{c["label"]}</div>' for c in LCATS)}</div>
        <img class="radar-pose" src="assets/img/pose-radar.webp" alt="" width="200" height="254">
      </div>
      <div class="chart-col"><div class="chart-pane">{bubble_svg(radar_items, "Radar des bonnes affaires : note presse contre prix des champions", link_root="", sid="homeRadar")}</div></div>
    </div>
  </section>

  <section class="section">
    <div class="section-head"><h2>Par où commencer ?</h2><div class="tag">Quatre familles, {len(CAT)} usages</div></div>
    <p class="bf-home"><a class="see-all" href="black-friday/">Black Friday 2026 : les PC qui valent vraiment le coup, et leur prix repère →</a></p>
    <div class="fam-grid">
      <a class="fam-card" href="pc-portable/">
        <div class="fam-art"><img src="assets/img/badge-bureautique.webp" alt="" width="96" height="96"><img src="assets/img/badge-gaming.webp" alt="" width="96" height="96"><img src="assets/img/badge-creation.webp" alt="" width="96" height="96"></div>
        <h3>PC portables</h3><p>{laptop_count} machines, un top 10 par usage, {sum(d['tests']['n'] for d in ITEMS.values() if d['family'] == 'laptop')} notes presse.</p>
        <div class="fam-chips">{''.join(f'<span>{c["label"]}</span>' for c in LCATS)}</div><span class="uc-go">Explorer →</span></a>
      <a class="fam-card" href="ordinateur-de-bureau/">
        <div class="fam-art"><img src="assets/img/badge-tout-en-un.webp" alt="" width="96" height="96"><img src="assets/img/badge-gaming.webp" alt="" width="96" height="96"><img src="assets/img/badge-mini-pc.webp" alt="" width="96" height="96"></div>
        <h3>Ordinateurs de bureau</h3><p>{desk_count} machines, un top 10 par usage : tours, mini-PC et tout-en-un.</p>
        <div class="fam-chips">{''.join(f'<span>{c["label"]}</span>' for c in DCATS)}</div><span class="uc-go">Explorer →</span></a>
      <a class="fam-card" href="ecran-pc/">
        <div class="fam-art"><img src="assets/img/badge-gaming.webp" alt="" width="96" height="96"><img src="assets/img/badge-ecran-portable.webp" alt="" width="96" height="96"><img src="assets/img/badge-ecran-lowcost.webp" alt="" width="96" height="96"></div>
        <h3>Écrans PC</h3><p>{sum(1 for d in ITEMS.values() if d['family'] == 'ecran')} écrans, un top 10 par usage : bureautique, gaming, création, portables et petits prix.</p>
        <div class="fam-chips">{''.join(f'<span>{c["label"]}</span>' for c in ECATS)}</div><span class="uc-go">Explorer →</span></a>
      <a class="fam-card" href="imprimante/">
        <div class="fam-art"><img src="assets/img/badge-reservoir.webp" alt="" width="96" height="96"><img src="assets/img/badge-laser-couleur.webp" alt="" width="96" height="96"><img src="assets/img/badge-photo.webp" alt="" width="96" height="96"></div>
        <h3>Imprimantes</h3><p>{sum(1 for d in ITEMS.values() if d['family'] == 'imprimante')} imprimantes, un top 10 par usage : réservoirs, laser, photo et petits prix.</p>
        <div class="fam-chips">{''.join(f'<span>{c["label"]}</span>' for c in ICATS)}</div><span class="uc-go">Explorer →</span></a>
    </div>
    <div class="soon-grid">{''.join(f'<div class="soon-card"><img class="soon-img" src="assets/img/{SOON_IMG[i]}.webp" alt="" width="84" height="84" loading="lazy"><span class="soon-chip">Bientôt</span><h3>{t}</h3><p>{x}</p></div>' for i, (t, x) in enumerate(SOON))}</div>
  </section>

  <section class="section method-strip" style="border-bottom:none;">
    <div class="ms-grid">
      <img src="assets/img/pose-lowcost.webp" alt="La mascotte" width="170" height="260">
      <div>
        <div class="section-head"><h2>Notre méthode en 3 étapes</h2><div class="tag">Transparence</div></div>
        <div class="method-grid">
          <div class="method-card"><span class="mono-big">01</span><h3>On lit tous les tests</h3><p>Presse française et internationale : Clubic, Les Numériques, Notebookcheck, Tom's Hardware, The Verge…</p></div>
          <div class="method-card"><span class="mono-big">02</span><h3>On calcule une note presse</h3><p>La moyenne de toutes les notes, convertie sur 10, avec le nombre de tests toujours affiché.</p></div>
          <div class="method-card"><span class="mono-big">03</span><h3>On résume le verdict</h3><p>Points forts, points faibles, pour qui c'est fait — et notre choix pour chaque usage.</p></div>
        </div>
        <p style="margin-top:16px"><a class="see-all" href="methode">Lire notre méthode complète →</a></p>
      </div>
    </div>
  </section>
"""
write("index.html", page("", "Top 10 Geek : tous les tests high-tech résumés pour vous — PC, écrans, imprimantes",
                         "Nous lisons tous les tests de la presse high-tech et vous donnons une note presse sur 10 et un verdict clair par usage : PC portables, ordinateurs de bureau, écrans PC, imprimantes.",
                         "", home, "home", body_cls="home",
                         ld=[ORG, {"@type": "WebSite", "@id": DOMAIN + "/#site", "url": DOMAIN + "/", "name": "Top 10 Geek", "description": BASELINE,
                                   "inLanguage": "fr-FR", "publisher": {"@id": ORG["@id"]}}]))

# ---------------------------------------------------------------- Méthode
methode = f"""
  <div class="prose">
    <div class="prose-hero">
      <div><div class="eyebrow">MÉTHODE · MAJ {MAJ}</div><h1>Une note principale : celle de la presse</h1>
      <p>Nous ne testons pas les produits nous-mêmes : nous n'avons pas de laboratoire, et nous préférons le dire. Notre travail, c'est de lire tout ce qui a été publié, de trier le solide du marketing, et de vous le rendre lisible.</p></div>
      <img src="assets/img/pose-investigation.webp" alt="La mascotte, loupe à la main" width="200" height="200">
    </div>
    <div class="method-grid">
      <div class="method-card"><span class="mono-big">1 · Sélection</span><h3>Deux conditions pour entrer</h3><p>Un produit n'entre dans un top 10 que s'il est <b>réellement en vente</b> chez au moins un des marchands que nous suivons et s'il a fait l'objet d'<b>au moins un test</b> dans la presse.</p></div>
      <div class="method-card"><span class="mono-big">2 · Presse</span><h3>La note principale</h3><p>Moyenne simple des notes publiées par les médias spécialisés, convertie sur 10, avec le nombre de notes. Chaque note renvoie vers le test d'origine. « Gamme » signale des notes obtenues sur une configuration ou une génération proche.</p></div>
      <div class="method-card"><span class="mono-big">3 · Prix</span><h3>Un prix indicatif</h3><p>Pour chaque produit, nous affichons un prix indicatif, avec le mois où nous l'avons constaté, et les liens vers les marchands où nous l'avons trouvée en vente.</p></div>
    </div>
    <h2>Le classement</h2>
    <p>En tête, <b>« le choix de la bande »</b> : notre recommandation pour l'usage, le meilleur compromis entre notes presse et prix. Ensuite, les produits sont classés par <b>note presse</b>. Ceux dont les tests ne donnent pas de note chiffrée viennent en dernier : nous donnons alors le lien vers le test plutôt que d'inventer une note.</p>
    <h2>Comment est calculée la note presse</h2>
    <p>Toutes les notes sont ramenées sur 10 : 4/5 devient 8/10, 87 % devient 8,7/10. Nous faisons une moyenne simple, sans pondérer les médias. Le nombre de notes est toujours affiché : une moyenne appuyée sur quinze tests est plus solide qu'une note unique. Les tests sans note chiffrée sont listés mais n'entrent pas dans la moyenne. Au {MAJ}, le site recense <b>{TOTAL_TESTS} tests</b> et <b>{TOTAL_NOTES} notes</b> pour {len(ITEMS)} produits.</p>
    <h2>Les imprimantes et les associations de consommateurs</h2>
    <p>Les imprimantes sont peu testées par la presse high-tech, mais très bien par les <b>associations de consommateurs</b> (Test-Achats, Que Choisir, Which?, Tænk), qui les mesurent en laboratoire. Ces associations réservent leurs notes à leurs abonnés : nous citons et lions leurs tests, sans note chiffrée, et la note presse n'est calculée que sur les notes publiées librement. C'est pourquoi beaucoup d'imprimantes affichent « testé, sans note ».</p>
    <h2>Comment lire le graphe à bulles</h2>
    <p>Chaque bulle est un produit. <b>Horizontalement</b> : la note presse. <b>Verticalement</b> : le prix indicatif. <b>Taille</b> : le nombre de notes (une grosse bulle = une note solide). <b>En pointillés</b>, à gauche : les produits testés mais sans note chiffrée. Les bonnes affaires se trouvent dans la <b>zone jaune, en bas à droite</b>.</p>
    <h2>Prix, photos et configurations</h2>
    <p>Le prix indicatif est le plus bas que nous avons constaté chez Amazon, Darty, sur l'Acer Store ou chez Geekom (pour les écrans et les imprimantes : sur Amazon, en précisant quand le produit n'est proposé que par un vendeur tiers), arrondi à la dizaine d'euros ; le mois du constat est indiqué à côté. Nous le revoyons environ une fois par mois. Il situe la machine mais ne remplace pas une comparaison : <b>seul le prix affiché par le marchand fait foi</b>. Nous ne comparons pas, pour l'instant, les prix marchand par marchand : nous indiquons seulement où la machine est en vente. Un même modèle existe souvent en plusieurs configurations (mémoire, stockage, carte graphique) : celle de chaque offre est indiquée à côté du lien, et peut différer d'un marchand à l'autre. Les photos sont celles fournies par les marchands et les constructeurs.</p>
    <h2>Avis clients, poids et autonomie</h2>
    <p>La note « avis clients Darty » est celle affichée par Darty lors de notre dernier relevé ; nous ne l'affichons qu'à partir de trois avis. Poids et autonomie sont ceux annoncés par le constructeur, sauf mention « test ». « n.c. » : non communiqué.</p>
    <h2>Notre indépendance</h2>
    <p>Aucune marque ne paie pour figurer dans nos sélections. Certains liens sont des liens d'affiliation (à ce jour : {AFF_TXT}) : ils peuvent nous rapporter une commission, sans surcoût pour vous, et n'influencent ni les notes ni les classements.</p>
    <h2>Contact</h2>
    <p>Une remarque, une erreur repérée ? Écrivez-nous : <a href="mailto:contact@top10geek.fr">contact@top10geek.fr</a></p>
  </div>
"""
write("methode.html", page("", "Notre méthode : sélection, note presse, prix indicatif | Top 10 Geek",
                           "Comment Top 10 Geek sélectionne les produits, calcule la note presse, établit le classement et indique les prix.",
                           "methode", methode, "methode", ld=[ld_crumbs(("Accueil", ""), ("Méthode", "methode")), ORG]))

# ---------------------------------------------------------------- Page Black Friday
BF_DATE = "vendredi 27 novembre 2026"
BF_TIPS = [
    ("Partez du prix repère", "Une promo n'est une affaire que si elle passe nettement sous le prix habituel. Nous affichons pour chaque machine le prix le plus bas que nous avons constaté avant le Black Friday : c'est votre point de comparaison."),
    ("Vérifiez la configuration", "Un même nom de modèle cache souvent plusieurs versions. Avant de comparer deux prix, comparez la mémoire, le stockage et le processeur : 8 Go et 256 Go ne valent pas 16 Go et 512 Go."),
    ("Regardez la note presse", "Un gros rabais sur une machine mal notée reste un mauvais achat. Mieux vaut une petite remise sur un ordinateur que la presse recommande."),
    ("Méfiez-vous du prix barré", "Le prix barré est parfois un ancien prix conseillé que plus personne ne pratiquait. Seul l'écart avec le prix réellement constaté les semaines précédentes compte."),
]


def bf_card(d, root, label):
    pr = d["press"]
    note = (f'{fr(pr["avg"])}/10 presse · {pr["n"]} note{"s" if pr["n"] > 1 else ""}{" (prudence)" if pr["n"] < 3 else ""}' if pr
            else f'{d["tests"]["tests"]} test{"s" if d["tests"]["tests"] > 1 else ""} presse, sans note chiffrée')
    img = f'<img src="{root}assets/img/p/{d["img"]}" alt="" width="96" height="72" loading="lazy">' if d["img"] else ""
    return f"""<a class="alt-card" href="{root}{d['purl']}">
      <span class="alt-k">{label}</span>
      {img}
      <b>{E(d['short'])}</b><span class="alt-why">{note}</span><span class="alt-meta">Prix repère : {d['price_txt']}</span></a>"""


BF_PIEGES = [
    ("PC portables", "Le même nom cache plusieurs configurations : comparez processeur, mémoire et stockage avant le prix. Méfiez-vous des modèles de l'an dernier présentés comme des nouveautés."),
    ("Ordinateurs de bureau", "Une grosse carte graphique attire l'œil, mais une alimentation ou un stockage au rabais font souvent la différence de prix. Vérifiez aussi ce qui est fourni : écran, clavier, souris."),
    ("Écrans PC", "Regardez la dalle (IPS, VA, OLED), la définition et la fréquence, pas seulement la taille. Une révision plus ancienne d'un même modèle peut être vendue sous un nom proche."),
    ("Imprimantes", "Le prix d'achat compte moins que celui de l'encre. Une imprimante bradée avec des cartouches chères coûte vite plus cher qu'une imprimante à réservoirs."),
]


def bf_family(fam, root, n_top, title, tag):
    blocks = []
    for c in fam["cats"]:
        top = by_cat[c["key"]][:n_top]
        cards = "".join(bf_card(d, root, "Notre choix" if i == 0 else f"N° {i + 1}") for i, d in enumerate(top))
        blocks.append(f"""<div class="bf-block">
      <h3><span class="dot {c['cls'].replace('f-', '')}"></span>{c['label']}</h3>
      <div class="alt-grid{' bf-two' if n_top == 2 else ''}">{cards}</div>
      <p class="bf-more"><a class="see-all" href="{root}{fam['slug']}/{c['slug']}/">Voir le top 10 {c['label'].lower()} →</a></p>
    </div>""")
    return f"""
  <section class="section" id="bf-{fam['slug']}">
    <div class="section-head"><h2>{title}</h2><div class="tag">{tag}</div></div>
    <p class="bf-note">Prix repères ({ind_txt(fam)}), pas des promotions.</p>
    {''.join(blocks)}
  </section>"""


def black_friday_page():
    root = "../"
    lap, desk, ecr, imp = FAM["laptop"], FAM["desktop"], FAM["ecran"], FAM["imprimante"]
    tips = "".join(f'<div class="g-card"><span class="g-num">0{i}</span><h3>{t}</h3><p>{x}</p></div>' for i, (t, x) in enumerate(BF_TIPS, 1))
    pieges = "".join(f'<div class="g-card"><span class="g-num">{t[:2].upper()}</span><h3>{t}</h3><p>{x}</p></div>' for t, x in BF_PIEGES)
    nav = "".join(f'<a class="bf-chip" href="#bf-{f["slug"]}">{f["plural"]}</a>' for f in (lap, desk, ecr, imp))
    faq = [
        ("Quand a lieu le Black Friday 2026 ?", f"Le Black Friday tombe le {BF_DATE}. Il est suivi du Cyber Monday, le lundi 30 novembre 2026. Beaucoup de marchands lancent leurs offres plusieurs jours avant et les prolongent après."),
        ("Les prix affichés sur cette page sont-ils des promotions ?", f"Non. Ce sont des prix repères : le prix le plus bas que nous avons constaté pour chaque produit avant le Black Friday, arrondi à la dizaine d'euros (mois du relevé indiqué dans chaque rubrique). Ils servent à juger si une offre est réellement intéressante. Seul le prix affiché par le marchand fait foi."),
        ("Comment savoir si une promo Black Friday est une vraie affaire ?", "Comparez le prix de l'offre au prix repère du produit, vérifiez que la référence et la configuration sont bien les mêmes, puis regardez la note presse. Une remise sur un produit mal noté n'est pas une bonne affaire."),
        ("Quels PC portables surveiller pendant le Black Friday ?", "Ceux que la presse recommande déjà au prix normal. Nous listons pour chaque usage les trois premiers de notre classement : bureautique, création, gaming, polyvalent et petits prix."),
        ("Faut-il acheter un écran PC pendant le Black Friday ?", "C'est souvent le bon moment pour les écrans gaming et les écrans 4K, très présents dans les promotions. Partez de l'usage (bureautique, jeu, création) et vérifiez la dalle et la définition : un gros écran mal adapté reste un mauvais achat."),
        ("Une imprimante en promo est-elle une bonne affaire ?", "Seulement si l'encre suit. Regardez le prix des cartouches ou des bouteilles et le nombre de pages qu'elles impriment. Pour imprimer régulièrement, une imprimante à réservoirs, même moins remisée, revient presque toujours moins cher."),
        ("Top 10 Geek teste-t-il les produits ?", "Non. Nous lisons les tests publiés par la presse spécialisée et les associations de consommateurs, et nous en tirons une note presse sur 10, avec le nombre de tests et les liens vers les sources."),
    ]
    faq_html = "".join(f'<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    body = f"""
  <div class="crumb"><a href="../">Accueil</a> › Black Friday 2026</div>
  <section class="usage-hero">
    <div>
      <div class="eyebrow">BLACK FRIDAY · {BF_DATE.upper()}</div>
      <h1>Black Friday 2026 : la high-tech qui <span class="flash">vaut vraiment le coup</span></h1>
      <p>Pendant le Black Friday, tout est « en promo ». Pour trier, nous partons de ce que dit la presse : voici les PC, écrans et imprimantes les mieux notés de nos comparatifs, avec leur <b>prix repère</b> relevé avant les promotions. Si une offre passe nettement en dessous, c'est une vraie affaire.</p>
      <p class="bf-chips">{nav}</p>
      <p class="hero-links"><a href="#reconnaitre">Reconnaître une vraie promo</a> · <a href="#pieges">Les pièges par catégorie</a></p>
    </div>
    <img class="hero-badge tall" src="../assets/img/pose-lowcost.webp" alt="La mascotte avec un PC en promo" width="170" height="260">
  </section>

  <section class="guide" id="reconnaitre">
    <div class="section-head"><h2>Reconnaître une vraie promo</h2><div class="tag">4 réflexes</div></div>
    <div class="g-grid">{tips}</div>
  </section>
{bf_family(lap, root, 3, "Les PC portables à surveiller", "Les 3 premiers par usage")}
{bf_family(desk, root, 2, "Les ordinateurs de bureau à surveiller", "Les 2 premiers par usage")}
{bf_family(ecr, root, 2, "Les écrans PC à surveiller", "Les 2 premiers par usage")}
{bf_family(imp, root, 2, "Les imprimantes à surveiller", "Les 2 premières par usage")}

  <section class="guide" id="pieges">
    <div class="section-head"><h2>Les pièges, catégorie par catégorie</h2><div class="tag">À vérifier avant de payer</div></div>
    <div class="g-grid">{pieges}</div>
  </section>

  <section class="section" style="border-bottom:none;">
    <div class="section-head"><h2>Questions fréquentes</h2><div class="tag">Black Friday</div></div>
    <div class="faq-list">{faq_html}</div>
  </section>
"""
    write("black-friday/index.html", page(root, "Black Friday 2026 : PC, écrans et imprimantes qui valent le coup selon la presse | Top 10 Geek",
          "Black Friday 2026 : PC portables, ordinateurs de bureau, écrans PC et imprimantes les mieux notés par la presse, avec leur prix repère pour reconnaître une vraie promo.",
          "black-friday/", body, "black-friday",
          ld=[ld_crumbs(("Accueil", ""), ("Black Friday 2026", "black-friday/")), ld_faq(faq)]))


black_friday_page()


# ---------------------------------------------------------------- Fichiers statiques
css = "".join(open(SRC + f, encoding="utf-8").read() for f in CSS_FILES)
write("assets/style.css", css)
shutil.copy(SRC + "main10.js", os.path.join(OUT, "assets/main.js"))
os.makedirs(os.path.join(OUT, "assets/img/p"), exist_ok=True)
for d in ITEMS.values():  # photos : copiées par build_data.py (img_p/) si présentes, sinon déjà dans assets/img/p
    if d["img"] and os.path.exists(SRC + "img_p/" + d["img"]):
        shutil.copy(SRC + "img_p/" + d["img"], os.path.join(OUT, "assets/img/p", d["img"]))
urls = [""] + [f"{f['slug']}/" for f in FAMILIES] + [f"{f['slug']}/{c['slug']}/" for f in FAMILIES for c in f["cats"]] + [d["purl"] for k in CAT for d in by_cat[k]] + ["black-friday/", "methode", "mentions-legales", "politique-confidentialite"]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      "".join(f"  <url><loc>{DOMAIN}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
print("OK", len(ITEMS), "produits ;", TOTAL_NOTES, "notes ;", TOTAL_TESTS, "tests")
