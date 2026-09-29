# -*- coding: utf-8 -*-
"""Top10Geek v4 — charte claire de l'artefact + corrections de l'audit v3 :
1) note presse = note principale et critère de classement ; 2) variantes regroupées + nouveaux modèles ;
3) noms lisibles ; 4) graphe annoté (zone « bonnes affaires ») ; 5) points faibles, filtre budget, poids/autonomie, format FR."""
import json, os, html, re, shutil, math
from urllib.parse import quote_plus
from press import PRESS
from specs import SPEC, GROUPS, CONFIG_LABEL, NEW
from guides import GUIDES

OUT = "/mnt/user-data/outputs/top10geek-v5"
DOMAIN = "https://top10geek.fr"
MAJ = "28/09/2026"
BASELINE = "Tous les tests high-tech, résumés pour vous"
E = html.escape

RAW = json.load(open("/home/claude/laptops.json", encoding="utf-8"))

CATS = [
    dict(key="bureau", slug="bureautique", label="Bureautique", h="Bureautique &amp; mobilité", tag="Autonomie avant tout", color="var(--cat-bureau)", cls="f-bureau",
         h1='Les 10 meilleurs PC portables <span class="flash">bureautique</span> en 2026',
         intro="Ici, l'autonomie réelle et le poids dans le sac priment sur des benchmarks de calcul rarement utiles au quotidien."),
    dict(key="creation", slug="creation", label="Création", h="Création &amp; photo", tag="Couleur au taquet", color="var(--cat-creation)", cls="f-creation",
         h1='Les 10 meilleurs PC portables pour la <span class="flash">création</span> en 2026',
         intro="Retouche photo, montage vidéo : la variable qui départage, c'est la fidélité des couleurs sortie d'usine — pas le nombre de cœurs du processeur."),
    dict(key="gaming", slug="gaming", label="Gaming", h="Gaming", tag="FPS ou rien", color="var(--cat-gaming)", cls="f-gaming",
         h1='Les 10 meilleurs PC portables <span class="flash">gaming</span> en 2026',
         intro="Deux chiffres suffisent à trancher la plupart des débats : les FPS en jeu réel, et le bruit du ventilo pour les obtenir."),
    dict(key="polyvalent", slug="polyvalent", label="Polyvalent", h="Polyvalent", tag="Zéro concession", color="var(--cat-poly)", cls="f-polyvalent",
         h1='Les 10 meilleurs PC portables <span class="flash">polyvalents</span> en 2026',
         intro="Pas de spécialité affichée, mais aucun vrai point faible non plus : le pari le plus sûr pour une seule machine capable de tout faire."),
    dict(key="lowcost", slug="lowcost", label="Low-cost", h="Low-cost (&lt; 500 €)", tag="Prix cassé, compromis assumés", color="var(--cat-lowcost)", cls="f-lowcost",
         h1='Les 10 meilleurs PC portables <span class="flash">à moins de 500 €</span>',
         intro="Sous les 500 €, chaque euro compte double. La presse teste rarement ces machines : quand aucune note presse n'existe, nous le disons plutôt que d'en inventer une."),
]
CAT = {c["key"]: c for c in CATS}
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


# ---------------------------------------------------------------- Construction du catalogue v4
grouped_away = {m for ms in GROUPS.values() for m in ms}
P = {}
for pid, d in RAW.items():
    if pid in grouped_away:
        continue
    short, weight, auton, weak = SPEC[pid]
    item = dict(id=pid, cat=d["cat"], short=short, ref=d["name"], badge=d["badge"], alt=d["alt"],
                idx=float(d["score"]), p=price_num(d["price"]), r=float(d["rating"].split()[0]) if "★" in d["rating"] else -1,
                verdict=d["verdict"], strengths=d["strengths"], weak=weak, weight=weight, auton=auton,
                press=mk_press(PRESS.get(pid)), configs=None, url=amazon(re.sub(r"\s*\(.*?\)", "", d["name"]).replace("— reconditionné", "").strip()))
    if pid in GROUPS:
        members = [pid] + GROUPS[pid]
        cfg = sorted([(price_num(RAW[m]["price"]), CONFIG_LABEL[m], m) for m in members])
        item["configs"] = [(CONFIG_LABEL[m], euro(p), amazon(re.sub(r"\s*\(.*?\)", "", RAW[m]["name"]).replace("— reconditionné", "").strip())) for p, _, m in cfg]
        item["p"] = cfg[0][0]
        item["from"] = True
        item["ref"] = "Existe en " + str(len(members)) + " configurations"
    P[pid] = item
for pid, n in NEW.items():
    P[pid] = dict(id=pid, cat=n["cat"], short=n["short"], ref=n["name"], badge=n["badge"], alt=n["alt"], idx=None, p=float(n["price_num"]), r=-1,
                  verdict=n["verdict"], strengths=n["strengths"], weak=n["weaknesses"], weight=n["weight"], auton=n["auton"],
                  press=mk_press(n["press"]), configs=None, url=amazon(n["short"]), new=True)

for d in P.values():
    d["weak"] = [w for w in d["weak"] if not w.startswith("Pas encore")]
    d["slug"] = CAT[d["cat"]]["slug"]
    d["price_txt"] = ("dès " if d.get("from") else "≈ ") + euro(d["p"])
    d["bucket"] = bucket(d["p"])


def rank_key(d):
    top = 0 if d["badge"] == "Le choix de la bande" else 1
    pr = d["press"]
    return (top, 0 if pr else 1, -(pr["avg"] if pr else 0), -(d["idx"] or 0), d["p"])


by_cat = {c["key"]: sorted([d for d in P.values() if d["cat"] == c["key"]], key=rank_key) for c in CATS}
for c in CATS:
    assert len(by_cat[c["key"]]) == 10, (c["key"], len(by_cat[c["key"]]))

seen, TOTAL_NOTES = set(), 0
for d in P.values():
    pr = d["press"]
    if pr and pr["src"][1] not in seen:
        seen.add(pr["src"][1]); TOTAL_NOTES += pr["n"]


def press_txt(d, long=False):
    pr = d["press"]
    if not pr:
        return None
    return fr(pr["avg"])


# ---------------------------------------------------------------- Graphe à bulles (x = note presse, y = prix, taille = nb de tests)
def bubble_svg(items, aria):
    tested = [d for d in items if d["press"]]
    untested = [d for d in items if not d["press"]]
    xs = [d["press"]["avg"] for d in tested] or [7, 9]
    xmin = min(6, math.floor(min(xs) - 0.2)); xmax = 10
    ps = [d["p"] for d in items]
    span = max(ps) - min(ps) or 100
    step = next(st for st in (50, 100, 250, 500, 1000) if span / st <= 5)
    ymin = max(0, math.floor(min(ps) * 0.9 / step) * step)
    ymax = math.ceil(max(ps) * 1.06 / step) * step
    if (ymax - ymin) / step < 3:
        ymax = ymin + 3 * step
    x0, x1, y0, y1 = 88, 330, 300, 22       # zone « notée »
    xs0 = 58                                # colonne « non testé »
    X = lambda v: x0 + (v - xmin) / (xmax - xmin) * (x1 - x0)
    Y = lambda v: y0 - (v - ymin) / (ymax - ymin) * (y0 - y1)
    g = []
    # zone bonnes affaires : note >= 8 et prix <= médiane
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
        g.append(f'<circle class="{cls}" data-id="{d["id"]}" data-cat="{d["cat"]}" data-budget="{d["bucket"]}" cx="{cx:.1f}" cy="{Y(d["p"]):.1f}" r="{rad(d):.1f}" fill="{col}"{style} tabindex="0" role="button" aria-label="{E(d["short"])}"><title>{E(tip)}</title></circle>')
    return f'<svg viewBox="0 0 340 336" role="img" aria-label="{E(aria)}" id="bubbleChart">' + "".join(g) + "</svg>"


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
        out[d["id"]] = dict(short=d["short"], ref=d["ref"], cat=d["cat"], slug=d["slug"], catLabel=CAT[d["cat"]]["label"].upper(),
                            badge=d["badge"], alt=d["alt"], idx=(fr(d["idx"]) if d["idx"] else None), idxv=d["idx"], tested=bool(pr), price=d["price_txt"],
                            rating=(fr(d["r"]) + " ★" if d["r"] > 0 else "avis en cours"), verdict=d["verdict"], strengths=d["strengths"], weak=d["weak"],
                            weight=d["weight"], auton=d["auton"], url=d["url"],
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
      <div class="metric" id="mWeight"><span class="k">Poids</span><span class="v" id="detailWeight"></span></div>
      <div class="metric" id="mAuton"><span class="k">Autonomie</span><span class="v" id="detailAuton"></span></div>
    </div>
    <p class="lead-line" id="detailVerdict"></p>
    <div class="pc-grid"><div class="strengths" id="detailStrengths"></div><div class="strengths weak" id="detailWeak"></div></div>
    <div class="featured-footer">
      <div><span class="price-tag" id="detailPrice"></span><span class="price-from">prix relevé le {MAJ}</span></div>
      <div class="cta-row"><a class="see-all" id="detailMore" href="#">Fiche complète</a><a class="cta" id="detailCta" href="#" target="_blank" rel="nofollow sponsored noopener">Voir le prix →</a></div>
    </div>
  </div>
</div></div>"""


def table(items, show_cat=True):
    rows = []
    for d in items:
        pr = d["press"]
        pcell = (f'<td class="num"><span class="press-chip">{fr(pr["avg"])}<small>·{pr["n"]}</small></span></td>' if pr else '<td class="num muted">non testé</td>')
        rows.append(f"""<tr data-id="{d['id']}" data-cat="{d['cat']}" data-budget="{d['bucket']}" data-price="{d['p']}" data-press="{pr['avg'] if pr else -1}" data-idx="{d['idx'] or -1}" data-rating="{d['r']}" tabindex="0">
<td class="name-cell"><span class="dot {d['cat']}"></span><span>{E(d['short'])}</span></td>{f"<td>{CAT[d['cat']]['label']}</td>" if show_cat else ''}
{pcell}<td class="num">{d['price_txt']}</td><td class="num">{'—' if d['weight'] == 'n.c.' else E(d['weight'])}</td><td class="num">{'—' if d['r'] < 0 else fr(d['r']) + ' ★'}</td></tr>""")
    cat_th = '<th data-sort="cat">Usage<span class="sort-arrow">↕</span></th>' if show_cat else ""
    return f"""<div class="data-table-wrap"><table class="data-table" id="dataTable">
<thead><tr><th data-sort="name">Machine<span class="sort-arrow">↕</span></th>{cat_th}
<th data-sort="press">Note presse<span class="sort-arrow">↕</span></th><th data-sort="price">Prix<span class="sort-arrow">↕</span></th>
<th>Poids</th><th data-sort="rating">Avis<span class="sort-arrow">↕</span></th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>"""


def budget_filter(items):
    present = {d["bucket"] for d in items}
    btn = []
    for k, l, _, _ in BUDGETS:
        dis = "" if k == "all" or k in present else " disabled"
        btn.append(f'<button class="pill" data-budget-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}"{dis}>{l}</button>')
    return '<div class="usage-filter" id="budgetFilter" role="group" aria-label="Filtrer par budget"><span class="filter-label">Votre budget :</span>' + "".join(btn) + "</div>"


# ---------------------------------------------------------------- Gabarit
def page(root, title, desc, path, body, active="", extra=""):
    nav = [("index.html#comparateur", "Le comparateur", "home")] + [(f"pc-portable/{c['slug']}/index.html", c["label"], c["slug"]) for c in CATS] + [("methode.html", "Méthode", "methode")]
    ACT = ' class="active"'
    nav_html = "".join(f'<a href="{root}{h}"{ACT if k == active else ""}>{t}</a>' for h, t, k in nav)
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
<meta property="og:image" content="{DOMAIN}/assets/img/og-image.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="{root}assets/img/logo-face.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800;12..96,900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <a class="brand-lockup" href="{root}index.html">
      <img class="brand-mark" src="{root}assets/img/logo-face.webp" alt="Symbole Top 10 Geek" width="40" height="40">
      <div class="brand-text"><div class="brand">TOP<span class="dot">10</span>GEEK</div><div class="baseline">{BASELINE}</div></div>
    </a>
    <nav class="topnav" id="topnav">{nav_html}</nav>
    <div class="topbar-actions"><button class="topnav-toggle" id="navToggle" aria-expanded="false" aria-controls="topnav">Menu</button></div>
  </div>
{body}
  <footer>
    <div class="disclosure" id="affiliation">Certains liens de ce site sont des liens d'affiliation : si vous achetez via ces liens, nous pouvons percevoir une commission. Cela n'entraîne aucun coût supplémentaire pour vous et n'influence pas nos verdicts, établis avant toute recherche de lien commercial.</div>
    <div class="foot-row">
      <div class="foot-sig"><img src="{root}assets/img/logo-face.webp" alt="" width="32" height="32">TOP 10 GEEK — {BASELINE}</div>
      <div class="foot-links"><a href="{root}methode.html">Méthode</a><a href="{root}mentions-legales.html">Mentions légales</a><a href="{root}politique-confidentialite.html">Confidentialité</a><span>MAJ {MAJ}</span></div>
    </div>
  </footer>
</div>
{extra}
<script src="{root}assets/main.js" defer></script>
</body>
</html>
"""


def mini(k, v, bar=False):
    if not v or v == "n.c.":
        return ""
    return f'<div class="mini{" mbar" if bar else ""}"><span class="k">{k}</span><span class="v">{v}</span></div>'


def guide_html(key):
    g = GUIDES[key]
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
    <p class="guide-go"><a class="cta" href="#comparateur">Voir notre top 10 ↓</a></p>
  </section>"""


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)


# ---------------------------------------------------------------- Accueil
home_sel = []
for c in CATS:
    items = by_cat[c["key"]]
    best = items[:2]
    cheap = sorted([d for d in items if d not in best], key=lambda d: d["p"])[:2]
    home_sel += best + cheap
table_sel = [d for c in CATS for d in by_cat[c["key"]][:3]]

pills = '<button class="pill" data-filter="all" aria-pressed="true"><span class="pdot" style="background:var(--ink)"></span>Top 20</button>' + "".join(
    f'<button class="pill {c["cls"]}" data-filter="{c["key"]}" aria-pressed="false"><span class="pdot" style="background:{c["color"]}"></span>{c["label"]}</button>' for c in CATS)


def usage_cards(root):
    out = []
    for c in CATS:
        top = by_cat[c["key"]][0]
        pr = top["press"]
        note = f'{fr(pr["avg"])}/10 presse' if pr else "pas encore testé"
        out.append(f"""<a class="usage-card" href="{root}pc-portable/{c['slug']}/index.html">
  <div class="uc-art"><img src="{root}assets/img/badge-{c['slug']}.webp" alt="" loading="lazy" width="110" height="110"></div>
  <div class="uc-body"><span class="uc-tag">{c['tag']}</span><h3><span class="dot {c['key']}"></span>{c['h']}</h3>
  <p class="uc-pick">Le choix de la bande : <b>{E(top['short'])}</b> — {note}</p>
  <span class="uc-go">Voir le top 10 →</span></div></a>""")
    return "".join(out)


FAQ = [
    ("Comment est calculée la note presse ?", "C'est la moyenne simple des notes publiées par les médias spécialisés (Notebookcheck, Clubic, Les Numériques, Tom's Hardware, TechRadar…), toutes converties sur 10 : 4/5 devient 8/10, 87 % devient 8,7/10. Le nombre de tests est toujours affiché. Quand la note porte sur une autre configuration de la même gamme, nous l'indiquons."),
    ("Comment est établi le classement ?", "En tête : « le choix de la bande », notre recommandation pour l'usage. Ensuite, les PC sont classés par note presse. Les PC que la presse n'a pas encore testés viennent en dernier, départagés par leur indice d'équipement."),
    ("Et l'indice d'équipement ?", "C'est une note secondaire sur la fiche technique, pondérée selon l'usage (autonomie et poids en bureautique, fidélité de l'écran en création, GPU et écran en gaming, stockage en low-cost). Il sert surtout à départager les PC non testés."),
    ("Faut-il 16 ou 32 Go de RAM en 2026 ?", "16 Go reste le minimum confortable pour de la bureautique ou du gaming courant. Pour la création ou pour garder la machine plusieurs années, 32 Go évite de la remplacer prématurément."),
    ("Pourquoi certains PC n'ont pas de note presse ?", "La presse teste surtout les modèles phares. Beaucoup de PC d'entrée de gamme ne sont jamais testés : plutôt que d'inventer une note, nous l'indiquons (bulle en pointillés) et nous nous appuyons sur la fiche technique et les avis acheteurs."),
]
faq_html = "".join(f'<details class="faq-item"{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(FAQ))

home = f"""
  <section class="intro">
    <div class="intro-grid">
      <div>
        <div class="eyebrow">COMPARATIF PC PORTABLES · MAJ {MAJ}</div>
        <h1>Nous avons lu tous les tests. <span class="flash">Voici le verdict, sans détour.</span></h1>
        <p>Nous n'avons pas de laboratoire : nous lisons les tests publiés par la presse spécialisée et nous en tirons une <b>note presse</b> sur 10. Nous la croisons avec la fiche technique et les avis d'acheteurs pour vous donner une recommandation claire par usage.</p>
        <div class="spec-row">
          <div><strong>{len(P)}</strong>PC sélectionnés</div>
          <div><strong>{TOTAL_NOTES}</strong>notes presse compilées</div>
          <div><strong>{len(CATS)}</strong>usages, dont le low-cost</div>
        </div>
      </div>
      <div class="hero-visual">
        <img src="assets/img/mascotte-persona-v2.webp" alt="La mascotte de Top 10 Geek, personnage geek illustré façon BD" width="800" height="800" fetchpriority="high">
        <div class="hv-cap">LA MASCOTTE — VISUEL IA</div>
      </div>
    </div>
  </section>

  <section class="comparator" id="comparateur">
    <div class="comparator-head">
      <div>
        <h2>Ce qu'en dit la presse, et ce que ça coûte</h2>
        <p class="comparator-sub">Chaque bulle est un PC. <b>Plus elle est à droite, mieux la presse l'a noté ; plus elle est basse, moins il est cher.</b> Les bonnes affaires sont donc en bas à droite. Cliquez sur une bulle pour lire le verdict.</p>
      </div>
      <img class="comparator-pose" src="assets/img/pose-investigation.webp" alt="" width="88" height="88">
    </div>
    <div class="usage-filter" id="usageFilter" role="group" aria-label="Filtrer par usage">{pills}</div>
    <div class="comparator-grid">
      <div class="chart-col">
        <div class="chart-pane">{bubble_svg(home_sel, "Graphe à bulles : note presse contre prix pour 20 PC, taille selon le nombre de tests")}</div>
        <div class="legend-strip">
          <div><div class="legend-title">Catégorie d'usage</div><div class="legend-cats">{''.join(f'<div class="legend-cat"><span class="dot {c["key"]}"></span>{c["label"]}</div>' for c in CATS)}</div></div>
          {LEGEND}
        </div>
      </div>
      {detail_card('')}
    </div>
    <p class="table-note">Le top 3 de chaque usage. Note presse : moyenne sur 10 · nombre de tests. Cliquez sur un en-tête pour trier.</p>
    {table(table_sel)}
  </section>

  <div class="divider"><span></span><span></span><span></span><span></span><span></span></div>

  <section class="section">
    <div class="section-head"><h2>Choisissez votre usage</h2><div class="tag">10 PC par usage</div></div>
    <div class="usage-grid">{usage_cards('')}</div>
  </section>

  <section class="section" id="faq" style="border-bottom:none;">
    <div class="section-head"><h2>Questions fréquentes</h2><div class="tag">FAQ</div></div>
    <div class="faq-list">{faq_html}</div>
  </section>
"""
write("index.html", page("", "Meilleur PC portable 2026 : tous les tests résumés par usage | Top 10 Geek",
                         f"{len(P)} PC portables 2026 classés par usage avec une note presse moyenne sur 10 : bureautique, création, gaming, polyvalent, low-cost.",
                         "", home, "home", js_data(home_sel + table_sel, "", by_cat["bureau"][0]["id"])))

# ---------------------------------------------------------------- Pages usage
for c in CATS:
    items = by_cat[c["key"]]
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
        rank_lbl = "NOTRE CHOIX" if i == 1 else "SUR 10"
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
    {mini("Poids", E(d['weight']))}
    {mini("Autonomie", E(d['auton']))}
    <div class="mini"><span class="k">Avis acheteurs</span><span class="v">{rating}</span></div>
    {mini("Équipement", idx, bar=True) if idx else ""}
    <a class="cta" href="{d['url']}" target="_blank" rel="nofollow sponsored noopener">Voir le prix →</a>
  </div>
</article>""")
    mascot = ('<img class="hero-badge tall" src="../../assets/img/pose-lowcost.webp" alt="La mascotte avec un PC en promo" width="170" height="260">' if c["key"] == "lowcost"
              else f'<img class="hero-badge" src="../../assets/img/badge-{c["slug"]}.webp" alt="" width="190" height="190">')
    body = f"""
  <div class="crumb"><a href="../../index.html">Accueil</a> › PC portables › {c['label']}</div>
  <section class="usage-hero">
    <div>
      <div class="eyebrow">{c['tag'].upper()} · MAJ {MAJ}</div>
      <h1>{c['h1']}</h1>
      <p>{c['intro']} <b>Classement :</b> notre choix en tête, puis par note presse.</p>
      <p class="hero-links"><a href="#comparateur">Aller directement au top 10 ↓</a> · <a href="#guide">Lire le guide d'achat</a></p>
      <div class="spec-row">
        <div><strong>10</strong>PC sélectionnés</div>
        <div><strong>{tested}/10</strong>testés par la presse</div>
        <div><strong>{n_notes}</strong>notes presse compilées</div>
      </div>
    </div>
    {mascot}
  </section>

  {guide_html(c['key'])}

  <section class="comparator" id="comparateur">
    <div class="comparator-head">
      <div><h2>Les 10 en un coup d'œil</h2>
      <p class="comparator-sub"><b>À droite : bien noté par la presse. En bas : moins cher.</b> Les bonnes affaires sont en bas à droite. Filtrez par budget, cliquez sur une bulle pour lire le verdict.</p></div>
      <img class="comparator-pose" src="../../assets/img/pose-investigation.webp" alt="" width="88" height="88">
    </div>
    {budget_filter(items)}
    <div class="comparator-grid">
      <div class="chart-col">
        <div class="chart-pane">{bubble_svg(items, "Graphe à bulles des 10 PC " + c['label'] + " : note presse contre prix, taille selon le nombre de tests")}</div>
        <div class="legend-strip">{LEGEND}</div>
      </div>
      {detail_card('../../')}
    </div>
    <p class="table-note">Note presse : moyenne sur 10 · nombre de tests. Cliquez sur un en-tête pour trier.</p>
    {table(items, show_cat=False)}
  </section>

  <section class="section" id="top10" style="border-bottom:none;">
    <div class="section-head"><h2><img class="section-badge" src="../../assets/img/badge-{c['slug']}.webp" alt="" width="50" height="50">Le top 10 {c['label'].lower()}</h2><div class="tag">Notre choix, puis note presse</div></div>
    <p class="empty-note" id="emptyNote" hidden>Aucun PC de ce top 10 dans cette tranche de prix.</p>
    <div class="top-list">{''.join(fiches)}</div>
  </section>
"""
    write(f"pc-portable/{c['slug']}/index.html",
          page("../../", f"Top 10 PC portables {c['label'].lower()} 2026 : tests résumés et verdict | Top 10 Geek",
               f"Les 10 meilleurs PC portables {c['label'].lower()} en 2026, classés par note presse, avec prix, poids, autonomie, points forts et points faibles.",
               f"pc-portable/{c['slug']}/", body, c["slug"], js_data(items, "../../", items[0]["id"])))

# ---------------------------------------------------------------- Méthode
methode = f"""
  <div class="prose">
    <div class="prose-hero">
      <div><div class="eyebrow">MÉTHODE</div><h1>Une note principale : celle de la presse</h1>
      <p>Nous ne testons pas les PC nous-mêmes : nous n'avons pas de laboratoire, et nous préférons le dire. Notre travail, c'est de lire tout ce qui a été publié, de trier le solide du marketing, et de vous le rendre lisible.</p></div>
      <img src="assets/img/pose-investigation.webp" alt="La mascotte, loupe à la main" width="200" height="200">
    </div>
    <div class="method-grid">
      <div class="method-card"><span class="mono-big">1 · Presse</span><h3>La note principale</h3><p>Moyenne simple des notes publiées par les médias spécialisés, convertie sur 10, avec le nombre de tests. « Gamme » signale une note obtenue sur une autre configuration du même modèle.</p></div>
      <div class="method-card"><span class="mono-big">2 · Acheteurs</span><h3>Le retour d'usage</h3><p>Note relevée chez les principaux revendeurs, sans arrondi ni majoration. « Avis en cours » quand les retours vérifiés sont trop peu nombreux.</p></div>
      <div class="method-card"><span class="mono-big">3 · Équipement</span><h3>La fiche technique</h3><p>Indice secondaire pondéré selon l'usage (voir ci-dessous). Il sert à départager les PC que la presse n'a pas encore testés.</p></div>
    </div>
    <h2>Le classement</h2>
    <p>En tête, <b>« le choix de la bande »</b> : notre recommandation pour l'usage, le meilleur compromis entre notes, équipement et prix. Ensuite, les PC sont classés par <b>note presse</b>. Les PC non testés viennent en dernier, départagés par l'indice d'équipement.</p>
    <h2>Les critères de l'indice d'équipement</h2>
    <ul>
      <li><b>Bureautique</b> : autonomie, poids, qualité d'écran, RAM, connectique.</li>
      <li><b>Création</b> : fidélité des couleurs (couverture colorimétrique, calibrage), définition et luminosité de l'écran, GPU, RAM.</li>
      <li><b>Gaming</b> : GPU, fréquence de l'écran, refroidissement, RAM et stockage.</li>
      <li><b>Polyvalent</b> : équilibre entre puissance, autonomie, poids et finition.</li>
      <li><b>Low-cost</b> : processeur, stockage (SSD plutôt qu'eMMC), écran Full HD, autonomie.</li>
    </ul>
    <p>La pondération détaillée sera publiée avec la prochaine mise à jour de la méthode. Les nouveaux modèles ajoutés en septembre 2026 n'ont pas encore d'indice (« non évalué »).</p>
    <h2>Comment lire le graphe à bulles</h2>
    <p>Chaque bulle est un PC. <b>Horizontalement</b> : la note presse. <b>Verticalement</b> : le prix. <b>Taille</b> : le nombre de tests (une grosse bulle = une note solide). <b>En pointillés</b>, à gauche : les PC pas encore testés. Les bonnes affaires se trouvent dans la <b>zone jaune, en bas à droite</b>.</p>
    <h2>Prix, poids et autonomie</h2>
    <p>Prix arrondis, relevés le {MAJ} ; ils évoluent vite, seul le prix affiché par le marchand fait foi. Poids et autonomie sont ceux annoncés par le constructeur, sauf mention « test ». « n.c. » : non communiqué.</p>
    <h2>Notre indépendance</h2>
    <p>Aucune marque ne paie pour figurer dans nos sélections. Certains liens sont des liens d'affiliation : ils peuvent nous rapporter une commission, sans surcoût pour vous, et n'influencent ni les notes ni les classements.</p>
    <h2>Contact</h2>
    <p>Une remarque, une erreur repérée ? Écrivez-nous : <span class="fill">[ADRESSE E-MAIL DE CONTACT]</span></p>
  </div>
"""
write("methode.html", page("", "Notre méthode : note presse, classement, indice d'équipement | Top 10 Geek",
                           "Comment Top 10 Geek calcule la note presse, établit le classement et lit les avis acheteurs.", "methode.html", methode, "methode"))

# Pages légales / 404 : reprises de la v3
for f in ["mentions-legales.html", "politique-confidentialite.html", "404.html"]:
    shutil.copy(f"/mnt/user-data/outputs/top10geek-v4/{f}", os.path.join(OUT, f))

css = open("/home/claude/artifact_base.css", encoding="utf-8").read() + open("/home/claude/extra.css", encoding="utf-8").read() + open("/home/claude/extra4.css", encoding="utf-8").read() + open("/home/claude/extra5.css", encoding="utf-8").read()
write("assets/style.css", css)
shutil.copy("/home/claude/main5.js", os.path.join(OUT, "assets/main.js"))
shutil.copytree("/mnt/user-data/outputs/top10geek-v3/assets/img", os.path.join(OUT, "assets/img"), dirs_exist_ok=True)
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
urls = [""] + [f"pc-portable/{c['slug']}/" for c in CATS] + ["methode.html", "mentions-legales.html", "politique-confidentialite.html"]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      "".join(f"  <url><loc>{DOMAIN}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
print("OK", len(P), "PC ;", TOTAL_NOTES, "notes ;", sum(1 for d in P.values() if d["press"]), "testés")
for c in CATS:
    print(c["slug"], [(d["short"][:22], fr(d["press"]["avg"]) if d["press"] else "-") for d in by_cat[c["key"]]])
