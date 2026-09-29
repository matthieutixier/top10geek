# -*- coding: utf-8 -*-
"""Top10Geek v6 — site multi-familles (PC portables + ordinateurs de bureau), menus déroulants,
nouvelle page d'accueil. Charte claire de l'artefact, graphe à bulles et mascottes."""
import json, os, html, re, shutil, math
from urllib.parse import quote_plus
from press import PRESS
from specs import SPEC, GROUPS, CONFIG_LABEL, NEW
from guides import GUIDES
from desk import DESK, DCATS
from guides_desk import GUIDES_DESK
import hashlib
VER = hashlib.md5(b''.join(open(f'/home/claude/{f}','rb').read() for f in ['artifact_base.css','extra.css','extra4.css','extra5.css','extra6.css','main6.js'])).hexdigest()[:8]

OUT = "/mnt/user-data/outputs/top10geek-v6"
DOMAIN = "https://top10geek.fr"
MAJ = "29/09/2026"
BASELINE = "Tous les tests high-tech, résumés pour vous"
AMAZON_MENTION = "En tant que Partenaire Amazon, je réalise un bénéfice sur les achats remplissant les conditions requises."
E = html.escape
GUIDES_ALL = dict(GUIDES, **GUIDES_DESK)

RAW = json.load(open("/home/claude/laptops.json", encoding="utf-8"))

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
         intro="Sous les 500 €, chaque euro compte double. La presse teste rarement ces machines : quand aucune note presse n'existe, nous le disons plutôt que d'en inventer une."),
]

FAMILIES = [
    dict(key="laptop", slug="pc-portable", label="PC portable", plural="PC portables", cats=LCATS, provisional=False,
         m_labels=("Poids", "Autonomie"), col="Poids", mascot="mascotte-persona-v2",
         h1='Comparatif PC portables 2026 : <span class="flash">le verdict par usage</span>',
         intro="50 PC portables passés au crible, une note presse sur 10 tirée de centaines de tests, et un top 10 pour chaque usage."),
    dict(key="desktop", slug="ordinateur-de-bureau", label="Ordinateur de bureau", plural="Ordinateurs de bureau", cats=DCATS, provisional=True,
         m_labels=("Format", "Processeur"), col="Format", mascot="pose-investigation",
         h1='Comparatif ordinateurs de bureau : <span class="flash">tours, mini-PC et tout-en-un</span>',
         intro="Bureautique, création, gaming, mini-PC et tout-en-un : notre sélection d'ordinateurs de bureau, classée par usage."),
]
CAT = {}
for f in FAMILIES:
    for c in f["cats"]:
        c["family"] = f["key"]; c["fslug"] = f["slug"]
        CAT[c["key"]] = c
FAM = {f["key"]: f for f in FAMILIES}
BUDGETS = [("all", "Tous les prix", 0, 1e9), ("b1", "< 500 €", 0, 500), ("b2", "500 – 1 000 €", 500, 1000),
           ("b3", "1 000 – 1 500 €", 1000, 1500), ("b4", "1 500 – 2 000 €", 1500, 2000), ("b5", "> 2 000 €", 2000, 1e9)]


def fr(x, d=1):
    return f"{x:.{d}f}".replace(".", ",")


def euro(x):
    v = int(round(x / 10.0) * 10) if x >= 1000 else int(x)
    return f"{v:,}".replace(",", " ") + " €"


def bucket(p):
    for k, _, lo, hi in BUDGETS[1:]:
        if lo <= p < hi:
            return k
    return "b5"


def price_num(s):
    return float(s.replace("€", "").replace(" ", "").replace(" ", "").replace(",", ".").strip())


def mk_press(pr):
    if not pr:
        return None
    if "agg" in pr:
        avg, n = pr["agg"]
    else:
        vals = [v for _, v in pr["notes"]]
        avg, n = sum(vals) / len(vals), len(vals)
    return dict(avg=avg, n=n, scope=pr["scope"], src=pr["src"], notes=pr.get("notes"))


def amazon(q):
    return "https://www.amazon.fr/s?k=" + quote_plus(q)


# ---------------------------------------------------------------- Catalogue PC portables
grouped_away = {m for ms in GROUPS.values() for m in ms}
ITEMS = {}
for pid, d in RAW.items():
    if pid in grouped_away:
        continue
    short, weight, auton, weak = SPEC[pid]
    item = dict(id=pid, cat=d["cat"], short=short, ref=d["name"], badge=d["badge"],
                idx=float(d["score"]), p=price_num(d["price"]), r=float(d["rating"].split()[0]) if "★" in d["rating"] else -1,
                verdict=d["verdict"], strengths=d["strengths"], weak=weak, m=(weight, auton),
                press=mk_press(PRESS.get(pid)), configs=None, url=amazon(re.sub(r"\s*\(.*?\)", "", d["name"]).replace("— reconditionné", "").strip()))
    if pid in GROUPS:
        members = [pid] + GROUPS[pid]
        cfg = sorted([(price_num(RAW[m]["price"]), CONFIG_LABEL[m], m) for m in members])
        item["configs"] = [(CONFIG_LABEL[m], euro(p), amazon(re.sub(r"\s*\(.*?\)", "", RAW[m]["name"]).replace("— reconditionné", "").strip())) for p, _, m in cfg]
        item["p"] = cfg[0][0]; item["from"] = True
        item["ref"] = "Existe en " + str(len(members)) + " configurations"
    ITEMS[pid] = item
for pid, n in NEW.items():
    ITEMS[pid] = dict(id=pid, cat=n["cat"], short=n["short"], ref=n["name"], badge=n["badge"], idx=None, p=float(n["price_num"]), r=-1,
                      verdict=n["verdict"], strengths=n["strengths"], weak=n["weaknesses"], m=(n["weight"], n["auton"]),
                      press=mk_press(n["press"]), configs=None, url=amazon(n["short"]))
# ---------------------------------------------------------------- Catalogue ordinateurs de bureau (provisoire)
for pid, n in DESK.items():
    ITEMS[pid] = dict(id=pid, cat=n["cat"], short=n["short"], ref=n["ref"], badge=n["badge"], idx=None, p=float(n["price"]), r=-1,
                      verdict=n["verdict"], strengths=n["strengths"], weak=n["weak"], m=(n["fmt"], n["cpu"]),
                      press=mk_press(n["press"]), configs=None, url=amazon(n["short"]), provisional=True)

for d in ITEMS.values():
    c = CAT[d["cat"]]
    d["weak"] = [w for w in d["weak"] if not w.startswith("Pas encore")]
    d["slug"] = c["slug"]; d["family"] = c["family"]; d["fslug"] = c["fslug"]
    d["price_txt"] = ("dès " if d.get("from") else "≈ ") + euro(d["p"])
    d["bucket"] = bucket(d["p"])
    d["href"] = f'{c["fslug"]}/{c["slug"]}/index.html#{d["id"]}'


def rank_key(d):
    top = 0 if d["badge"] == "Le choix de la bande" else 1
    pr = d["press"]
    return (top, 0 if pr else 1, -(pr["avg"] if pr else 0), -(d["idx"] or 0), d["p"])


by_cat = {k: sorted([d for d in ITEMS.values() if d["cat"] == k], key=rank_key) for k in CAT}
for c in LCATS:
    assert len(by_cat[c["key"]]) == 10, c["key"]


def notes_total(items):
    seen, tot = set(), 0
    for d in items:
        pr = d["press"]
        if pr and pr["src"][1] not in seen:
            seen.add(pr["src"][1]); tot += pr["n"]
    return tot


TOTAL_NOTES = notes_total(ITEMS.values())


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
    g.append(f'<text class="axis-label" x="{xs0:.0f}" y="312" text-anchor="middle">non</text><text class="axis-label" x="{xs0:.0f}" y="321" text-anchor="middle">testé</text>')
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
        tip = f'{d["short"]} — ' + (f'note presse {fr(pr["avg"])}/10 ({pr["n"]} test{"s" if pr["n"] > 1 else ""})' if pr else "pas encore testé par la presse") + f', {d["price_txt"]}'
        cls = "bubble" + ("" if pr else " nopress")
        style = f' style="stroke:{col}"' if not pr else ""
        circ = f'<circle class="{cls}" data-id="{d["id"]}" data-cat="{d["cat"]}" data-budget="{d["bucket"]}" cx="{cx:.1f}" cy="{Y(d["p"]):.1f}" r="{rad(d):.1f}" fill="{col}"{style} tabindex="0" role="button" aria-label="{E(d["short"])}"><title>{E(tip)}</title></circle>'
        if link_root is not None:
            circ = f'<a href="{link_root}{d["href"]}">' + circ.replace(' tabindex="0" role="button"', '') + "</a>"
        g.append(circ)
    return f'<svg viewBox="0 0 340 336" role="img" aria-label="{E(aria)}" id="{sid}">' + "".join(g) + "</svg>"


LEGEND = """<div>
  <div class="legend-title">Comment lire le graphe</div>
  <p class="legend-note"><b>→ À droite</b> : la presse l'a bien noté. <b>↑ En haut</b> : il est cher. <b>Grosse bulle</b> : note appuyée sur beaucoup de tests. <b>Pointillés</b> : pas encore testé. Les meilleures affaires sont <b>en bas à droite</b>, dans la zone jaune.</p>
</div>
<div>
  <div class="legend-title">Taille = nombre de tests presse</div>
  <div class="legend-size">
    <div class="ex"><svg width="20" height="20"><circle cx="10" cy="10" r="7" fill="none" stroke="var(--ink-muted)" stroke-width="1.6"/></svg>1 test</div>
    <div class="ex"><svg width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--ink-muted)" stroke-width="1.6"/></svg>15+ tests</div>
    <div class="ex"><svg width="20" height="20"><circle cx="10" cy="10" r="7" fill="var(--ink-muted)" fill-opacity=".1" stroke="var(--ink-muted)" stroke-width="1.6" stroke-dasharray="3 2"/></svg>non testé</div>
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
                            rating=(fr(d["r"]) + " ★" if d["r"] > 0 else "avis en cours"), verdict=d["verdict"], strengths=d["strengths"], weak=d["weak"],
                            m=[[fam["m_labels"][0], d["m"][0]], [fam["m_labels"][1], d["m"][1]]], url=d["url"],
                            press=(dict(avg=fr(pr["avg"]), n=pr["n"], gamme=pr["scope"] == "gamme") if pr else None))
    return "<script>window.T10G=" + json.dumps(dict(laptops=out, root=root, first=first), ensure_ascii=False) + ";</script>"


def detail_card(root):
    return f"""<div class="detail-col"><div class="featured" id="detailCard">
  <div class="art" id="detailArt"><img class="art-badge" id="detailArtImg" src="{root}assets/img/badge-bureautique.webp" alt=""></div>
  <div class="featured-body">
    <div class="cat-label-inline" id="detailCatLabel"></div>
    <span class="fbadge" id="detailBadge"></span>
    <div class="featured-title"><div><h3 id="detailName"></h3><div class="ref" id="detailRef"></div></div>
      <div class="score big-press" id="detailPress"></div></div>
    <div class="metrics m4">
      <div class="metric"><span class="k">Avis acheteurs</span><span class="v" id="detailRating"></span></div>
      <div class="metric" id="mIdx"><span class="k">Équipement</span><span class="bar"><i id="detailIdxBar"></i></span></div>
      <div class="metric" id="mA"><span class="k" id="mAk"></span><span class="v" id="mAv"></span></div>
      <div class="metric" id="mB"><span class="k" id="mBk"></span><span class="v" id="mBv"></span></div>
    </div>
    <p class="lead-line" id="detailVerdict"></p>
    <div class="pc-grid"><div class="strengths" id="detailStrengths"></div><div class="strengths weak" id="detailWeak"></div></div>
    <div class="featured-footer">
      <div><span class="price-tag" id="detailPrice"></span><span class="price-from">prix relevé le {MAJ}</span></div>
      <div class="cta-row"><a class="see-all" id="detailMore" href="#">Fiche complète</a><a class="cta" id="detailCta" href="#" target="_blank" rel="nofollow sponsored noopener">Voir le prix →</a></div>
    </div>
  </div>
</div></div>"""


def table(items, fam, show_cat=True):
    rows = []
    for d in items:
        pr = d["press"]
        pcell = (f'<td class="num"><span class="press-chip">{fr(pr["avg"])}<small>·{pr["n"]}</small></span></td>' if pr else '<td class="num muted">non testé</td>')
        m0 = d["m"][0]
        rows.append(f"""<tr data-id="{d['id']}" data-cat="{d['cat']}" data-budget="{d['bucket']}" data-price="{d['p']}" data-press="{pr['avg'] if pr else -1}" data-idx="{d['idx'] or -1}" data-rating="{d['r']}" tabindex="0">
<td class="name-cell"><span class="dot {CAT[d['cat']]['cls'].replace('f-', '')}"></span><span>{E(d['short'])}</span></td>{f"<td>{CAT[d['cat']]['label']}</td>" if show_cat else ''}
{pcell}<td class="num">{d['price_txt']}</td><td class="{'num' if fam['key'] == 'laptop' else ''}">{'—' if m0 == 'n.c.' else E(m0)}</td>{('<td class="num">' + ('—' if d['r'] < 0 else fr(d['r']) + ' ★') + '</td>') if fam['key'] == 'laptop' else ''}</tr>""")
    cat_th = '<th data-sort="cat">Usage<span class="sort-arrow">↕</span></th>' if show_cat else ""
    return f"""<div class="data-table-wrap"><table class="data-table" id="dataTable">
<thead><tr><th data-sort="name">Machine<span class="sort-arrow">↕</span></th>{cat_th}
<th data-sort="press">Note presse<span class="sort-arrow">↕</span></th><th data-sort="price">Prix<span class="sort-arrow">↕</span></th>
<th>{fam['col']}</th>{'<th data-sort="rating">Avis<span class="sort-arrow">↕</span></th>' if fam['key'] == 'laptop' else ''}</tr></thead>
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
    <p class="guide-go"><a class="cta" href="#comparateur">Voir notre sélection ↓</a></p>
  </section>"""


PROVISIONAL_NOTE = '<div class="provisional"><b>Sélection provisoire.</b> Le comparatif complet des ordinateurs de bureau (notes presse, prix vérifiés, top 10) arrive très bientôt. Prix indicatifs.</div>'


# ---------------------------------------------------------------- Gabarit
def nav_html(root, active):
    parts = []
    for f in FAMILIES:
        subs = f'<a class="dd-all" href="{root}{f["slug"]}/index.html"><span>Tout le comparatif</span><span class="arr">→</span></a><div class="dd-sep">Par usage</div>' + "".join(
            f'<a href="{root}{f["slug"]}/{c["slug"]}/index.html"><span class="dot {c["cls"].replace("f-", "")}"></span>{c["label"]}</a>' for c in f["cats"])
        act = " active" if active == f["slug"] else ""
        parts.append(f"""<div class="dd{act}"><a class="dd-top" href="{root}{f['slug']}/index.html" aria-haspopup="true">{f['label']}<span class="caret">▾</span></a>
  <div class="dd-menu">{subs}</div></div>""")
    parts.append(f'<a class="nav-link{" active" if active == "methode" else ""}" href="{root}methode.html">Méthode</a>')
    return "".join(parts)


def page(root, title, desc, path, body, active="", extra="", body_cls=""):
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{DOMAIN}/{path}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Top 10 Geek">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{DOMAIN}/assets/img/og-image.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg">
<link rel="icon" type="image/png" href="{root}assets/img/logo-face.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800;12..96,900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/style.css?v={VER}">
</head>
<body class="{body_cls}">
<div class="wrap">
  <div class="topbar">
    <a class="brand-lockup" href="{root}index.html">
      <img class="brand-mark" src="{root}assets/img/logo-face.webp" alt="Symbole Top 10 Geek" width="40" height="40">
      <div class="brand-text"><div class="brand">TOP<span class="dot">10</span>GEEK</div><div class="baseline">{BASELINE}</div></div>
    </a>
    <nav class="topnav" id="topnav">{nav_html(root, active)}</nav>
    <div class="topbar-actions"><button class="topnav-toggle" id="navToggle" aria-expanded="false" aria-controls="topnav">Menu</button></div>
  </div>
{body}
  <footer>
    <div class="disclosure" id="affiliation">Certains liens de ce site sont des liens d'affiliation : si vous achetez via ces liens, nous pouvons percevoir une commission. Cela n'entraîne aucun coût supplémentaire pour vous et n'influence pas nos verdicts, établis avant toute recherche de lien commercial. {AMAZON_MENTION}</div>
    <div class="foot-row">
      <div class="foot-sig"><img src="{root}assets/img/logo-face.webp" alt="" width="32" height="32">TOP 10 GEEK — {BASELINE}</div>
      <div class="foot-links"><a href="{root}pc-portable/index.html">PC portables</a><a href="{root}ordinateur-de-bureau/index.html">Ordinateurs de bureau</a><a href="{root}methode.html">Méthode</a><a href="{root}mentions-legales.html">Mentions légales</a><a href="{root}politique-confidentialite.html">Confidentialité</a><span>MAJ {MAJ}</span></div>
    </div>
  </footer>
</div>
{extra}
<script src="{root}assets/main.js?v={VER}" defer></script>
</body>
</html>
"""


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)


def usage_cards(fam, root):
    out = []
    for c in fam["cats"]:
        top = by_cat[c["key"]][0]
        pr = top["press"]
        note = f'{fr(pr["avg"])}/10 presse' if pr else "pas encore testé"
        out.append(f"""<a class="usage-card" href="{root}{fam['slug']}/{c['slug']}/index.html">
  <div class="uc-art"><img src="{root}assets/img/badge-{c['badge']}.webp" alt="" loading="lazy" width="110" height="110"></div>
  <div class="uc-body"><span class="uc-tag">{c['tag']}</span><h3><span class="dot {c['cls'].replace('f-', '')}"></span>{c['h']}</h3>
  <p class="uc-pick">Le choix de la bande : <b>{E(top['short'])}</b> — {note}</p>
  <span class="uc-go">{'Voir le top 10' if not fam['provisional'] else 'Voir la sélection'} →</span></div></a>""")
    return "".join(out)


FAQ_L = [
    ("Comment est calculée la note presse ?", "C'est la moyenne simple des notes publiées par les médias spécialisés (Notebookcheck, Clubic, Les Numériques, Tom's Hardware, TechRadar…), toutes converties sur 10 : 4/5 devient 8/10, 87 % devient 8,7/10. Le nombre de tests est toujours affiché. Quand la note porte sur une autre configuration de la même gamme, nous l'indiquons."),
    ("Comment est établi le classement ?", "En tête : « le choix de la bande », notre recommandation pour l'usage. Ensuite, les PC sont classés par note presse. Les PC que la presse n'a pas encore testés viennent en dernier."),
    ("Faut-il 16 ou 32 Go de RAM en 2026 ?", "16 Go reste le minimum confortable pour de la bureautique ou du gaming courant. Pour la création ou pour garder la machine plusieurs années, 32 Go évite de la remplacer prématurément."),
    ("Pourquoi certains PC n'ont pas de note presse ?", "La presse teste surtout les modèles phares. Plutôt que d'inventer une note, nous l'indiquons (bulle en pointillés) et nous nous appuyons sur la fiche technique et les avis acheteurs."),
]


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
    faq = "".join(f'<details class="faq-item"{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(FAQ_L))
    tested = sum(1 for d in all_items if d["press"])
    body = f"""
  <div class="crumb"><a href="../index.html">Accueil</a> › {fam['plural']}</div>
  <section class="usage-hero">
    <div>
      <div class="eyebrow">COMPARATIF {fam['plural'].upper()} · MAJ {MAJ}</div>
      <h1>{fam['h1']}</h1>
      <p>{fam['intro']}</p>
      <div class="spec-row">
        <div><strong>{len(all_items)}</strong>{fam['plural']} sélectionnés</div>
        <div><strong>{tested}</strong>testés par la presse</div>
        <div><strong>{len(cats)}</strong>usages</div>
      </div>
    </div>
    <img class="hero-badge tall" src="../assets/img/{fam['mascot']}.webp" alt="La mascotte Top 10 Geek" width="220" height="260">
  </section>
  {PROVISIONAL_NOTE if fam['provisional'] else ''}
  <section class="comparator" id="comparateur">
    <div class="comparator-head">
      <div><h2>Ce qu'en dit la presse, et ce que ça coûte</h2>
      <p class="comparator-sub">Chaque bulle est un {'PC portable' if fam['key'] == 'laptop' else 'ordinateur de bureau'}. <b>Plus elle est à droite, mieux la presse l'a noté ; plus elle est basse, moins il est cher.</b> Cliquez sur une bulle pour lire le verdict.</p></div>
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
      {detail_card(root)}
    </div>
    <p class="table-note">Le top 3 de chaque usage. Note presse : moyenne sur 10 · nombre de tests. Cliquez sur un en-tête pour trier.</p>
    {table(tsel, fam)}
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
             else "Meilleur ordinateur de bureau 2026 : tours, mini-PC, tout-en-un | Top 10 Geek")
    desc = (f"{len(all_items)} PC portables 2026 classés par usage avec une note presse moyenne sur 10 : bureautique, création, gaming, polyvalent, low-cost."
            if fam["key"] == "laptop" else "Ordinateurs de bureau classés par usage : bureautique, création, gaming, mini-PC et tout-en-un.")
    write(f"{fam['slug']}/index.html", page(root, title, desc, f"{fam['slug']}/", body, fam["slug"], js_data(sel + tsel, root, by_cat[cats[0]["key"]][0]["id"])))


# ---------------------------------------------------------------- Pages usage
def usage_page(fam, c):
    root = "../../"
    items = by_cat[c["key"]]
    n = len(items)
    _s = {}
    for d in items:
        if d["press"]:
            _s[d["press"]["src"][1]] = d["press"]["n"]
    n_notes, tested = sum(_s.values()), sum(1 for d in items if d["press"])
    fiches = []
    for i, d in enumerate(items, 1):
        pr = d["press"]
        if pr:
            big = f'<span class="pn">{fr(pr["avg"])}</span><span class="pd">/10</span><span class="pc">note presse · {pr["n"]} test{"s" if pr["n"] > 1 else ""}{" · gamme" if pr["scope"] == "gamme" else ""}</span>'
            if pr["notes"] and pr["n"] > 1:
                lis = "".join(f"<li><span>{E(s)}</span><b>{fr(v)}</b></li>" for s, v in pr["notes"])
                det = f'<details><summary>Détail des {pr["n"]} notes presse</summary><ul class="notes-list">{lis}</ul><p class="src">Source : <a href="{pr["src"][1]}" target="_blank" rel="noopener">{E(pr["src"][0])}</a></p></details>'
            elif pr["notes"]:
                det = f'<p class="src small">Source : <a href="{pr["src"][1]}" target="_blank" rel="noopener">{E(pr["src"][0])}</a> ({E(pr["notes"][0][0])})</p>'
            else:
                det = f'<p class="src small">Moyenne de {pr["n"]} notes relevée par <a href="{pr["src"][1]}" target="_blank" rel="noopener">{E(pr["src"][0])}</a></p>'
        else:
            big = '<span class="pn none">—</span><span class="pc">pas encore testé par la presse</span>'
            det = ""
        st = "".join(f'<span class="s">{E(s)}</span>' for s in d["strengths"])
        wk = "".join(f'<span class="s">{E(s)}</span>' for s in d["weak"]) or ('<span class="s muted">Défauts non documentés : pas encore de test presse</span>' if not pr else '<span class="s muted">Aucun défaut majeur relevé par la presse</span>')
        cfg = ""
        if d["configs"]:
            cfg = '<div class="configs"><span class="k">Configurations</span>' + "".join(
                f'<a href="{u}" target="_blank" rel="nofollow sponsored noopener"><span>{E(l)}</span><b>{p}</b></a>' for l, p, u in d["configs"]) + "</div>"
        idx = f'<span class="bar" title="Indice d\'équipement : {fr(d["idx"])}/10"><i style="width:{d["idx"] * 10:.0f}%"></i></span>' if d["idx"] else ""
        rating = f'{fr(d["r"])} ★' if d["r"] > 0 else '<span class="none">avis en cours</span>'
        rank_lbl = "NOTRE CHOIX" if i == 1 else f"SUR {n}"
        fiches.append(f"""<article class="fiche{' top' if i == 1 else ''}" id="{d['id']}" data-budget="{d['bucket']}">
  <div class="rank">#{i}<small>{rank_lbl}</small></div>
  <div class="f-main">
    <span class="fbadge{' alt' if i != 1 else ''}">{E(d['badge'])}</span>
    <h3>{E(d['short'])}</h3>
    <div class="ref">{E(d['ref'])}</div>
    <p class="lead-line"><b>En bref.</b> {E(d['verdict'])}</p>
    <div class="pc-grid">
      <div class="strengths"><span class="pc-t pro">Points forts</span>{st}</div>
      <div class="strengths weak"><span class="pc-t con">Points faibles</span>{wk}</div>
    </div>
    {cfg}
    {det}
  </div>
  <div class="f-side">
    <div class="press-big">{big}</div>
    <div class="mini"><span class="k">Prix</span><span class="v">{d['price_txt']}</span></div>
    {mini(fam['m_labels'][0], E(d['m'][0]))}
    {mini(fam['m_labels'][1], E(d['m'][1]))}
    {'<div class="mini"><span class="k">Avis acheteurs</span><span class="v">' + rating + '</span></div>' if fam['key'] == 'laptop' else ''}
    {mini("Équipement", idx, bar=True) if idx else ""}
    <a class="cta" href="{d['url']}" target="_blank" rel="nofollow sponsored noopener">Voir le prix →</a>
  </div>
</article>""")
    mascot = ('<img class="hero-badge tall" src="../../assets/img/pose-lowcost.webp" alt="La mascotte avec un PC en promo" width="170" height="260">' if c["key"] == "lowcost"
              else f'<img class="hero-badge" src="../../assets/img/badge-{c["badge"]}.webp" alt="" width="190" height="190">')
    top_word = f"Le top 10 {c['label'].lower()}" if n == 10 else f"Notre sélection {c['label'].lower()}"
    body = f"""
  <div class="crumb"><a href="../../index.html">Accueil</a> › <a href="../index.html">{fam['plural']}</a> › {c['label']}</div>
  <section class="usage-hero">
    <div>
      <div class="eyebrow">{c['tag'].upper()} · MAJ {MAJ}</div>
      <h1>{c['h1']}</h1>
      <p>{c['intro']} <b>Classement :</b> notre choix en tête, puis par note presse.</p>
      <p class="hero-links"><a href="#comparateur">Aller directement à la sélection ↓</a> · <a href="#guide">Lire le guide d'achat</a></p>
      <div class="spec-row">
        <div><strong>{n}</strong>{fam['plural'].lower()} sélectionnés</div>
        {f'<div><strong>{tested}/{n}</strong>testés par la presse</div><div><strong>{n_notes}</strong>notes presse compilées</div>' if tested else '<div><strong>Bientôt</strong>notes presse en cours de compilation</div>'}
      </div>
    </div>
    {mascot}
  </section>
  {PROVISIONAL_NOTE if fam['provisional'] else ''}
  {guide_html(c['key'])}

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
      {detail_card(root)}
    </div>
    <p class="table-note">Note presse : moyenne sur 10 · nombre de tests. Cliquez sur un en-tête pour trier.</p>
    {table(items, fam, show_cat=False)}
  </section>

  <section class="section" id="top10" style="border-bottom:none;">
    <div class="section-head"><h2><img class="section-badge" src="../../assets/img/badge-{c['badge']}.webp" alt="" width="50" height="50">{top_word}</h2><div class="tag">Notre choix, puis note presse</div></div>
    <p class="empty-note" id="emptyNote" hidden>Aucun modèle de cette sélection dans cette tranche de prix.</p>
    <div class="top-list">{''.join(fiches)}</div>
  </section>
"""
    if fam["key"] == "laptop":
        title = f"Top 10 PC portables {c['label'].lower()} 2026 : tests résumés et verdict | Top 10 Geek"
        desc = f"Les 10 meilleurs PC portables {c['label'].lower()} en 2026, classés par note presse, avec prix, poids, autonomie, points forts et points faibles."
    else:
        title = f"Meilleurs ordinateurs de bureau {c['label'].lower()} 2026 | Top 10 Geek"
        desc = f"Notre sélection d'ordinateurs de bureau {c['label'].lower()} : guide d'achat, prix, points forts et points faibles."
    write(f"{fam['slug']}/{c['slug']}/index.html", page(root, title, desc, f"{fam['slug']}/{c['slug']}/", body, fam["slug"], js_data(items, root, items[0]["id"])))


for fam in FAMILIES:
    family_page(fam)
    for c in fam["cats"]:
        usage_page(fam, c)

# ---------------------------------------------------------------- Page d'accueil
champions = [next((d for d in by_cat[c["key"]] if d["press"]), by_cat[c["key"]][0]) for f in FAMILIES for c in f["cats"]]
laptop_count = sum(1 for d in ITEMS.values() if d["family"] == "laptop")
desk_count = sum(1 for d in ITEMS.values() if d["family"] == "desktop")


def champ_card(d):
    c = CAT[d["cat"]]
    pr = d["press"]
    score = (f'<span class="ch-score"><b>{fr(pr["avg"])}</b><small>/10</small><em>{pr["n"]} test{"s" if pr["n"] > 1 else ""} presse</em></span>' if pr
             else '<span class="ch-score none"><b>À confirmer</b><em>tests presse à venir</em></span>')
    return f"""<a class="champ" href="{d['href']}" style="--c:{c['color']}">
  <span class="ch-top"><span class="ch-usage"><span class="dot {c['cls'].replace('f-', '')}"></span>{c['label']}</span><img src="assets/img/badge-{c['badge']}.webp" alt="" width="64" height="64" loading="lazy"></span>
  <span class="ch-name">{E(d['short'])}</span>
  <span class="ch-verdict">{E(d['verdict'])}</span>
  <span class="ch-bottom">{score}<span class="ch-price">{d['price_txt']}</span></span>
  <span class="ch-go">Voir le classement →</span>
</a>"""


def ticker():
    tops = sorted([d for d in ITEMS.values() if d["press"] and d["press"]["n"] >= 5], key=lambda d: -d["press"]["avg"])[:12]
    items = "".join(f'<span class="tk-item"><b>{E(d["short"])}</b> {fr(d["press"]["avg"])}/10 <small>· {d["press"]["n"]} tests</small></span>' for d in tops)
    return f'<div class="ticker" aria-hidden="true"><div class="tk-track">{items}{items}</div></div>'


radar_items = [by_cat[c["key"]][i] for c in LCATS for i in (0, 1, 2)]
SOON = [("Écrans PC", "Bureautique, gaming, retouche : la bonne dalle pour chaque usage."), ("Smartphones", "Les meilleurs téléphones par budget, notes presse à l'appui."),
        ("Casques &amp; écouteurs", "Réduction de bruit, sport, gaming : le son sans se tromper."), ("Tablettes", "iPad, Android, Windows : laquelle pour lire, dessiner ou travailler ?")]

home = f"""
  <section class="home-hero">
    <div class="hh-text">
      <div class="eyebrow">LE COMPARATEUR QUI A LU TOUS LES TESTS · MAJ {MAJ}</div>
      <h1>Tous les tests high&#8209;tech, <span class="flash">résumés pour vous.</span></h1>
      <p>Nous lisons les tests de la presse spécialisée, nous en tirons une <b>note presse sur 10</b> et nous vous disons, usage par usage, quoi acheter — et pourquoi. Sans jargon, sans pub déguisée.</p>
      <div class="hh-ctas">
        <a class="cta big" href="pc-portable/index.html">Trouver mon PC portable →</a>
        <a class="cta big ghost" href="ordinateur-de-bureau/index.html">Trouver mon ordinateur de bureau →</a>
      </div>
      <div class="spec-row">
        <div><strong>{TOTAL_NOTES}</strong>notes presse compilées</div>
        <div><strong>{laptop_count + desk_count}</strong>ordinateurs sélectionnés</div>
        <div><strong>10</strong>usages couverts</div>
      </div>
    </div>
    <div class="hh-visual">
      <div class="hh-blob"></div>
      <img class="hh-mascot" src="assets/img/mascotte-persona-v2.webp" alt="La mascotte de Top 10 Geek" width="800" height="800" fetchpriority="high">
      <img class="hh-sticker s1" src="assets/img/badge-gaming.webp" alt="" width="120" height="120">
      <img class="hh-sticker s2" src="assets/img/badge-creation.webp" alt="" width="120" height="120">
      <img class="hh-sticker s3" src="assets/img/badge-bureautique.webp" alt="" width="120" height="120">
      <div class="hh-bubble">« J'ai lu {TOTAL_NOTES} notes pour vous. De rien. »</div>
    </div>
  </section>

  {ticker()}

  <section class="section">
    <div class="section-head"><h2>Les champions du moment</h2><div class="tag">Les mieux notés par la presse, par usage</div></div>
    <div class="family-row">
      <div class="fr-head"><h3>PC portables</h3><a class="see-all" href="pc-portable/index.html">Tout le comparatif →</a></div>
      <p class="champ-hint">← Faites glisser pour voir les 5 usages →</p><div class="champ-grid">{''.join(champ_card(d) for d in champions if d['family'] == 'laptop')}</div>
    </div>
    <div class="family-row">
      <div class="fr-head"><h3>Ordinateurs de bureau <span class="soon-chip">sélection provisoire</span></h3><a class="see-all" href="ordinateur-de-bureau/index.html">Toute la sélection →</a></div>
      <p class="champ-hint">← Faites glisser pour voir les 5 usages →</p><div class="champ-grid">{''.join(champ_card(d) for d in champions if d['family'] == 'desktop')}</div>
    </div>
  </section>

  <section class="section radar">
    <div class="radar-grid">
      <div class="radar-text">
        <div class="eyebrow">LE RADAR DES BONNES AFFAIRES · PC PORTABLES</div>
        <h2>Bien noté <span class="flash">et</span> pas trop cher&nbsp;? C'est en bas à droite.</h2>
        <p>Chaque bulle est l'un des 3 meilleurs PC portables de chaque usage. Plus elle est à droite, plus la presse l'a aimé ; plus elle est basse, plus il est abordable ; plus elle est grosse, plus la note repose sur de nombreux tests. Cliquez sur une bulle pour ouvrir sa fiche.</p>
        <div class="legend-cats">{''.join(f'<div class="legend-cat"><span class="dot {c["cls"].replace("f-", "")}"></span>{c["label"]}</div>' for c in LCATS)}</div>
        <img class="radar-pose" src="assets/img/pose-investigation.webp" alt="" width="140" height="140">
      </div>
      <div class="chart-col"><div class="chart-pane">{bubble_svg(radar_items, "Radar des bonnes affaires : note presse contre prix des champions", link_root="", sid="homeRadar")}</div></div>
    </div>
  </section>

  <section class="section">
    <div class="section-head"><h2>Par où commencer ?</h2><div class="tag">Deux familles, dix usages</div></div>
    <div class="fam-grid">
      <a class="fam-card" href="pc-portable/index.html">
        <div class="fam-art"><img src="assets/img/badge-bureautique.webp" alt="" width="96" height="96"><img src="assets/img/badge-gaming.webp" alt="" width="96" height="96"><img src="assets/img/badge-creation.webp" alt="" width="96" height="96"></div>
        <h3>PC portables</h3><p>{laptop_count} machines, un top 10 par usage, {notes_total([d for d in ITEMS.values() if d['family'] == 'laptop'])} notes presse.</p>
        <div class="fam-chips">{''.join(f'<span>{c["label"]}</span>' for c in LCATS)}</div><span class="uc-go">Explorer →</span></a>
      <a class="fam-card" href="ordinateur-de-bureau/index.html">
        <div class="fam-art"><img src="assets/img/badge-polyvalent.webp" alt="" width="96" height="96"><img src="assets/img/badge-gaming.webp" alt="" width="96" height="96"><img src="assets/img/badge-lowcost.webp" alt="" width="96" height="96"></div>
        <h3>Ordinateurs de bureau</h3><p>Tours, mini-PC et tout-en-un : {desk_count} machines en sélection provisoire.</p>
        <div class="fam-chips">{''.join(f'<span>{c["label"]}</span>' for c in DCATS)}</div><span class="uc-go">Explorer →</span></a>
    </div>
    <div class="soon-grid">{''.join(f'<div class="soon-card"><span class="soon-chip">Bientôt</span><h3>{t}</h3><p>{x}</p></div>' for t, x in SOON)}</div>
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
        <p style="margin-top:16px"><a class="see-all" href="methode.html">Lire notre méthode complète →</a></p>
      </div>
    </div>
  </section>
"""
write("index.html", page("", "Top 10 Geek : tous les tests high-tech résumés pour vous — PC portables, ordinateurs de bureau",
                         "Nous lisons tous les tests de la presse high-tech et vous donnons une note presse sur 10 et un verdict clair par usage : PC portables, ordinateurs de bureau.",
                         "", home, "home", body_cls="home"))

# ---------------------------------------------------------------- Méthode + légal (repris v5, avec les modifications faites en ligne)
def reframe(src_path, active="", path=""):
    s = open(src_path, encoding="utf-8").read()
    body = s[s.index('  </div>\n', s.index('<div class="topbar">')) + len('  </div>\n'):s.index('  <footer>')]
    title = re.search(r"<title>(.*?)</title>", s).group(1)
    desc = re.search(r'<meta name="description" content="(.*?)">', s).group(1)
    return page("", html.unescape(title), html.unescape(desc), path, body, active)


write("methode.html", reframe("/mnt/user-data/outputs/top10geek-v5/methode.html", "methode", "methode.html"))
ml = reframe("/mnt/user-data/outputs/top10geek-v5/mentions-legales.html", "", "mentions-legales.html")
ml = ml.replace("<p><span class=\"fill\">[À confirmer selon l'hébergeur retenu]</span><br>Netlify, Inc. — 512 2nd Street, Suite 200, San Francisco, CA 94107, États-Unis — www.netlify.com</p>",
                "<p>Cloudflare, Inc. — 101 Townsend St, San Francisco, CA 94107, États-Unis — www.cloudflare.com</p>")
assert "Cloudflare" in ml
write("mentions-legales.html", ml)
write("politique-confidentialite.html", reframe("/mnt/user-data/outputs/top10geek-v5/politique-confidentialite.html", "", "politique-confidentialite.html"))
nf = reframe("/mnt/user-data/outputs/top10geek-v5/404.html", "", "404.html").replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/').replace('href="index.html"', 'href="/index.html"').replace('href="pc-portable/', 'href="/pc-portable/').replace('href="ordinateur-de-bureau/', 'href="/ordinateur-de-bureau/').replace('href="methode.html"', 'href="/methode.html"').replace('href="mentions-legales.html"', 'href="/mentions-legales.html"').replace('href="politique-confidentialite.html"', 'href="/politique-confidentialite.html"').replace('src="assets', 'src="/assets')
write("404.html", nf)

css = "".join(open(f"/home/claude/{f}", encoding="utf-8").read() for f in ["artifact_base.css", "extra.css", "extra4.css", "extra5.css", "extra6.css"])
write("assets/style.css", css)
shutil.copy("/home/claude/main6.js", os.path.join(OUT, "assets/main.js"))
shutil.copytree("/mnt/user-data/outputs/top10geek-v5/assets/img", os.path.join(OUT, "assets/img"), dirs_exist_ok=True)
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
urls = [""] + [f"{f['slug']}/" for f in FAMILIES] + [f"{f['slug']}/{c['slug']}/" for f in FAMILIES for c in f["cats"]] + ["methode.html", "mentions-legales.html", "politique-confidentialite.html"]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      "".join(f"  <url><loc>{DOMAIN}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
print("OK", len(ITEMS), "ordinateurs ;", TOTAL_NOTES, "notes")
