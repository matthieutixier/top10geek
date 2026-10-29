# -*- coding: utf-8 -*-
"""Top10Geek v10 (09/10/2026) — deux nouvelles rubriques : Écrans PC et Imprimantes (familles_new.py,
catalog_ecrans.py, catalog_imprimantes.py, guides_new.py ; données ajoutées par build_new.py). Textes génériques par famille.
v9 — comparateur de prix mis en veille : un prix indicatif par produit
(champ `prix` de data.json, constaté `prix_date`) et de simples liens vers les marchands
où le produit est en vente. Les prix par marchand restent dans data.json (champ `price`
des offres) mais ne sont plus affichés ; à réactiver avec les flux affiliés.
v8 — bloc « Notre choix », tri des fiches (sans tableau), une page par produit.
v7 — catalogue réel (50 PC portables + 50 ordinateurs de bureau), photos produits,
prix relevés par marchand (Amazon, Darty, Acer Store, Geekom, Electro Dépôt), notes presse avec liens vers les tests.
Données : data.json (source de vérité ; build_data.py est hors service depuis le 10/10/2026)."""
import json, os, html, re, shutil, math, hashlib, unicodedata
from guides import GUIDES
from guides_desk import GUIDES_DESK
from desk import DCATS
from profiles import PROFILES
from familles_new import ECATS, ICATS, SCATS, TCATS, ACATS, VCATS, FAMILIES_NEW, FAQ_E, FAQ_I, FAQ_S, FAQ_T, FAQ_A, FAQ_V
from guides_new import GUIDES_NEW
from catalog_ecrans import ECR
from catalog_imprimantes import IMP
from catalog_sols import SOLS
from catalog_reconditionnes import RECO, GUIDE_RECO
PROFILES = dict(PROFILES, **{k: (v["pour"], v["eviter"]) for k, v in list(ECR.items()) + list(IMP.items()) + list(SOLS.items()) + list(RECO.items())})
SRC = os.path.dirname(os.path.abspath(__file__)) + "/"
CSS_FILES = ['artifact_base.css', 'extra.css', 'extra4.css', 'extra5.css', 'extra6.css', 'extra7.css', 'extra8.css', 'extra9.css', 'extra10.css', 'extra11.css', 'extra12.css', 'extra13.css', 'extra14.css', 'extra15.css', 'extra16.css', 'extra17.css', 'extra18.css', 'extra19.css', 'extra20.css', 'extra21.css', 'extra22.css', 'extra23.css']
VER = hashlib.md5(b''.join(open(SRC + f, 'rb').read() for f in CSS_FILES + ['main15.js'])).hexdigest()[:8]

OUT = os.path.dirname(SRC.rstrip("/"))
DOMAIN = "https://top10geek.fr"
DATA = json.load(open(SRC + "data.json", encoding="utf-8"))
MAJ = DATA["date"]
PRIX_DATE = DATA.get("prix_date", "")          # ex. « octobre 2026 »
IND = f"prix indicatif · {PRIX_DATE}"
# Mise à jour par rubrique (releve.py --famille) : chaque rubrique a sa date et son mois de prix.
# Sans entrée pour une rubrique, on retombe sur les dates globales.
ASSOC = {"Test-Achats", "Que Choisir", "Which?", "Tænk", "Choice", "Stiftung Warentest", "Consumer Reports", "OCU", "Altroconsumo"}
FAM_SLUGS_OK = None  # défini après le filtrage des familles
MAISON_SLUGS = ("aspirateur-robot", "tv", "audio", "photo-video")   # univers « Maison » : accent et ambiance propres (extra21.css)
FAM_REL = {"laptop": "portable", "desktop": "bureau", "ecran": "ecran", "imprimante": "imprimante", "robot": "robot", "tv": "tv", "audio": "audio", "video": "video"}
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
GUIDES_ALL = dict(GUIDES, **GUIDES_DESK, **GUIDES_NEW, reconditionne=GUIDE_RECO)

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
    # Rubrique ajoutée le 26/10/2026 (PC-Portable.net, Effinity) : 10 PC professionnels reconditionnés, notes du modèle neuf à sa sortie.
    dict(key="reconditionne", slug="reconditionnes", label="Reconditionnés", h="Reconditionnés", tag="Le PC pro d'hier au prix d'aujourd'hui", color="var(--cat-reco)", cls="f-reco", badge="reconditionne",
         h1='Les 10 meilleurs <span class="flash">PC portables reconditionnés</span>',
         intro="Des PC professionnels (Dell Latitude, Lenovo ThinkPad, HP EliteBook) revendus reconditionnés par PC-Portable.net, contrôlés et garantis 2 ans, souvent sous 400 €. Attention : les notes de la presse portent sur le modèle neuf à sa sortie, pas sur l'exemplaire reconditionné que vous recevrez. L'état esthétique et la batterie varient d'un exemplaire à l'autre."),
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
         intro="60 PC portables, neufs et reconditionnés, passés au crible : une note presse sur 10 tirée de centaines de tests, un prix indicatif, les liens vers les marchands et un top 10 pour chaque usage."),
    dict(key="desktop", slug="ordinateur-de-bureau", label="Ordinateur de bureau", plural="Ordinateurs de bureau", cats=DCATS, provisional=False,
         m_labels=("Format", "Processeur"), col="Format", mascot="pose-tour", noun="ordinateur de bureau", noun_det="l'ordinateur",
         h1='Comparatif ordinateurs de bureau 2026 : <span class="flash">tours, mini-PC et tout-en-un</span>',
         intro="50 ordinateurs de bureau classés par usage : bureautique, création, gaming, mini-PC et tout-en-un, avec les notes de la presse, un prix indicatif et les liens vers les marchands."),
] + FAMILIES_NEW
# Une famille V2 sans aucun produit dans data.json n'est pas générée (rubrique en construction).
import json as _j, os as _o
_present = {_i["cat"] for _i in _j.load(open(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), "data.json"), encoding="utf-8"))["items"].values()}
FAMILIES = [_f for _f in FAMILIES if any(_c["key"] in _present for _c in _f["cats"])]
FAM_SLUGS_OK = {_f["slug"] for _f in FAMILIES}
CAT = {}
for f in FAMILIES:
    for c in f["cats"]:
        c["family"] = f["key"]; c["fslug"] = f["slug"]
        CAT[c["key"]] = c
FAM = {f["key"]: f for f in FAMILIES}

def foot_tail(root):
    """Fin du pied de page : liens des rubriques (1re ligne) puis liens du site sur une ligne à part."""
    return f'''<div class="foot-links"><a href="{root}pc-portable/">PC portables</a><a href="{root}ordinateur-de-bureau/">Ordinateurs de bureau</a><a href="{root}ecran-pc/">Écrans PC</a><a href="{root}imprimante/">Imprimantes</a><a href="{root}aspirateur-robot/">Robots aspirateurs</a><a href="{root}tv/">TV</a><a href="{root}audio/">Audio</a>{FOOT_VIDEO(root)}<a href="{root}black-friday/">Black Friday 2026</a><span>MAJ {MAJ}</span></div>
    </div>
    <nav class="foot-legal" aria-label="Informations sur le site"><a href="{root}methode">Méthode</a><a href="{root}a-propos">À propos</a><a href="{root}mentions-legales">Mentions légales</a><a href="{root}politique-confidentialite">Confidentialité</a></nav>'''


def FOOT_VIDEO(root):
    return f'<a href="{root}photo-video/">Photo et vidéo</a>' if "photo-video" in FAM_SLUGS_OK else ""


def carte_video():
    """Carte d'accueil Photo et vidéo, seulement quand la rubrique a des produits (en construction sinon)."""
    if "photo-video" not in FAM_SLUGS_OK:
        return ""
    n = sum(1 for d in ITEMS.values() if d['family'] == 'video')
    return (f'''<a class="fam-card maison" href="photo-video/">
        <div class="fam-art"><img src="assets/img/sticker-camera.webp" alt="" width="96" height="96" loading="lazy" decoding="async"><img src="assets/img/sticker-drone.webp" alt="" width="96" height="96" loading="lazy" decoding="async"><img src="assets/img/sticker-projector.webp" alt="" width="96" height="96" loading="lazy" decoding="async"></div>
        <h3>Photo et vidéo</h3><p>{n} caméras, vidéoprojecteurs, appareils photo et drones classés par usage, de la surveillance au drone.</p>
        <div class="fam-chips">{''.join(f'<span>{c["label"]}</span>' for c in VCATS)}</div><span class="uc-go">Explorer →</span></a>''')

BUDGETS = [("all", "Tous les prix", 0, 1e9), ("b1", "< 500 €", 0, 500), ("b2", "500 – 1 000 €", 500, 1000),
           ("b3", "1 000 – 1 500 €", 1000, 1500), ("b4", "1 500 – 2 000 €", 1500, 2000), ("b5", "> 2 000 €", 2000, 1e9)]
MERCHANT_CLS = {"Amazon": "amazon", "Darty": "darty", "Fnac": "fnac", "Acer Store": "acer", "Geekom": "geekom",
                "Electro Dépôt": "electrodepot", "PC-Portable.net": "pcportable"}
# Marchands dont le programme d'affiliation est validé (lien rémunéré). Les autres sont de simples liens directs.
# À compléter à chaque validation (ex. Awin : "Darty", "Fnac", "Acer Store", "Geekom") : attributs rel et mentions suivent.
# Ordre de la liste = ordre des boutons marchands : Electro Dépôt (Effinity, validé le 12/10/2026) d'abord, puis Amazon.
AFFILIATED = ["Electro Dépôt", "PC-Portable.net", "Amazon"]   # PC-Portable.net : Effinity, validé en octobre 2026
_aff = sorted(AFFILIATED)
AFF_TXT = ", ".join(_aff[:-1]) + " et " + _aff[-1]


# Marchands dont le prix exact est affiché (prix lu dans un flux officiel, avec sa date) : Electro Dépôt (flux
# Effinity, effinity.py). Les autres marchands restent sans prix (comparateur en veille depuis le 05/10/2026).
PRIX_EXACTS = {"Electro Dépôt", "PC-Portable.net"}   # PC-Portable.net : flux Effinity, prix de la configuration indiquée


def prix_exact(o):
    return o["m"] in PRIX_EXACTS and o.get("dispo", True) and o.get("price")


def date_releve(o):
    r = o.get("releve") or ""
    return f"{r[8:10]}/{r[5:7]}/{r[:4]}" if len(r) == 10 else ""


def o_prix(o):
    """Bloc prix d'une offre (seulement pour les marchands à prix exact)."""
    if not prix_exact(o):
        return ""
    dt = date_releve(o)
    return f'<span class="o-p">{euro2(o["price"])}<small>{"prix du " + dt if dt else "prix relevé"}</small></span>'


RECO_NOTE = ("Produit reconditionné (grade B), contrôlé et garanti 2 ans par PC-Portable.net (garantie annoncée par le vendeur, à vérifier sur sa fiche avant d'acheter). L'état esthétique et la batterie varient d'un exemplaire à l'autre. "
             "Les tests presse portent sur le modèle neuf à sa sortie. Le prix est celui de la configuration indiquée (mémoire, stockage, système), à la date du relevé.")


def cta_txt(o):
    return f'{euro2(o["price"])} chez {E(o["m"])} →' if prix_exact(o) else f'Voir chez {E(o["m"])} →'


# Carte « Avant d'acheter : le n° 1 de ce top » en haut de fiche (point 5 de l'analyse du 20/10/2026) : prête, non retenue pour l'instant.
CARTE_N1 = False  # remplacée le 20/10/2026 (v13) par le radar de la fiche (radar_fiche) ;   # affichée sur ordinateur seulement (extra16.css), choix de Matthieu du 20/10/2026 sur la maquette


def buy_btn(o, i):
    """Bouton marchand du cadre d'achat (fiche produit, ordinateur) : le premier en couleur, les suivants en contour.
    Prix affiché seulement pour les marchands à prix exact (Electro Dépôt) ; sinon « Voir le prix »."""
    dt = date_releve(o) if prix_exact(o) else ""
    sub = " · ".join(x for x in (E(o.get("cfg") or ""), f"prix du {dt}" if dt else "") if x)
    right = f'{euro2(o["price"])} →' if prix_exact(o) else "Voir le prix →"
    return (f'<a class="p-b{" p-b1" if i == 0 else ""}" href="{E(o["url"])}" target="_blank" rel="{rel_m(o["m"])}" title="{E(o["name"])}">'
            f'<span class="p-b-m"><b>{E(o["m"])}</b>{f"<small>{sub}</small>" if sub else ""}</span><span class="p-b-go">{right}</span></a>')


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
    offers = sorted(offers, key=lambda o: (AFFILIATED.index(o["m"]) if o["m"] in AFFILIATED else len(AFFILIATED), o["price"]))
    d = dict(id=pid, cat=n["cat"], short=n["short"], ref=n["ref"], badge=n["badge"], idx=None,
             p=float(n.get("prix") or min(o["price"] for o in offers)),
             r=(n["rating"] if n.get("rating") and n.get("nrev", 0) >= 3 else -1), nrev=n.get("nrev", 0),
             verdict=n["verdict"], strengths=n["strengths"], weak=n["weak"], m=tuple(n["m"]),
             press=rated, tests=tests, offers=offers, img=n.get("img"), configs=None, url=offers[0]["url"], synthese=n.get("synthese"))
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


from classement import TOP_BADGE, SEUIL_NOTES, PRIOR_M, ZONE_NOTE, MARGE_CHOIX, moyenne_usage, note_ajustee, cle, badge_affiche, appliquer_choix
# Règle du 27/10/2026 : « notre choix » de préférence dans la zone « bonnes affaires » (voir classement.py)
CHOIX_CHANGES = {}
for _k in CAT:
    _rows = [dict(id=d["id"], badge=d["badge"], avg=(d["press"]["avg"] if d["press"] else None), n=(d["press"]["n"] if d["press"] else 0),
                  tests=d["tests"]["tests"], p=d["p"]) for d in ITEMS.values() if d["cat"] == _k]
    if not _rows:
        continue
    for _id, _b in appliquer_choix(_rows).items():
        CHOIX_CHANGES[_id] = (ITEMS[_id]["badge"], _b)
        ITEMS[_id]["badge"] = _b
CAT_MEAN = {k: moyenne_usage([d["press"]["avg"] for d in ITEMS.values() if d["cat"] == k and d["press"]]) for k in CAT}
for d in ITEMS.values():
    pr = d["press"]
    d["score"] = note_ajustee(pr["avg"], pr["n"], CAT_MEAN[d["cat"]]) if pr else None


def rank_key(d):
    """Classement : voir _source/classement.py (règle partagée avec les vidéos)."""
    pr = d["press"]
    return cle(d["badge"], pr["avg"] if pr else None, pr["n"] if pr else 0, d["tests"]["tests"], d["p"], CAT_MEAN[d["cat"]])


by_cat = {k: sorted([d for d in ITEMS.values() if d["cat"] == k], key=rank_key) for k in CAT}
for k in CAT:
    assert len(by_cat[k]) == 10 or k[:2] in ("s-", "t-", "a-", "v-"), k
    for i, d in enumerate(by_cat[k], 1):   # « le choix de la bande » rétrogradé faute de notes : badge honnête
        d["badge"] = badge_affiche(d["badge"], i)


# Usages « transversaux » (ex. Petit prix) : affichent aussi des produits classés dans un autre usage (clé « extra »).
# Les fiches produits, le comparateur de famille et le sitemap restent sur by_cat (une fiche = un usage d'origine).
by_cat_view = dict(by_cat)
for _k, _c in CAT.items():
    if _c.get("extra"):
        _items = by_cat[_k] + [dict(ITEMS[_i], badge=("Valeur sûre" if ITEMS[_i]["badge"] == TOP_BADGE else ITEMS[_i]["badge"])) for _i in _c["extra"]]
        by_cat_view[_k] = sorted(_items, key=lambda d: cle(d["badge"], d["press"]["avg"] if d["press"] else None, d["press"]["n"] if d["press"] else 0, d["tests"]["tests"], d["p"], CAT_MEAN[_k]))


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
def bubble_svg(items, aria, link_root=None, sid="bubbleChart", link_key="href", focus=None, ranks=None):
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
    for d in sorted(items, key=lambda d: (d["id"] == focus, -rad(d))):
        pr = d["press"]
        col = CAT[d["cat"]]["color"]
        cx = X(pr["avg"]) if pr else xs0
        tip = f'{d["short"]} — ' + (f'note presse {fr(pr["avg"])}/10 ({pr["n"]} note{"s" if pr["n"] > 1 else ""})' if pr else "testé par la presse, sans note chiffrée") + f', {d["price_txt"]}'
        cls = "bubble" + ("" if pr else " nopress")
        style = f' style="stroke:{col}"' if not pr else ""
        circ = f'<circle class="{cls}" data-id="{d["id"]}" data-cat="{d["cat"]}" data-budget="{d["bucket"]}" cx="{cx:.1f}" cy="{Y(d["p"]):.1f}" r="{rad(d):.1f}" fill="{col}"{style} tabindex="0" role="button" aria-label="{E(d["short"])}"><title>{E(tip)}</title></circle>'
        if focus is not None:
            circ = circ.replace(f'class="{cls}"', f'class="{cls}{" focus" if d["id"] == focus else " dim"}"')
        if link_root is not None and d["id"] != focus:
            lab = f'N° {ranks[d["id"]]} : {d["short"]}' if ranks else d["short"]
            circ = (f'<a href="{link_root}{d[link_key]}" aria-label="{E(lab)}">' + circ.replace(' tabindex="0" role="button"', '')
                    .replace(f' aria-label="{E(d["short"])}"', '') + "</a>")
        g.append(circ)
        if ranks:
            cy = Y(d["p"]); r = rad(d)
            g.append(f'<text class="b-rank{" focus" if d["id"] == focus else ""}" x="{cx + r * 0.72 + 2:.1f}" y="{cy - r * 0.72 - 2:.1f}" aria-hidden="true">{ranks[d["id"]]}</text>')

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
    return f"""<div class="detail-col"><div class="featured" id="detailCard" data-z="radar">
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
    <div class="d-buy">
      <div class="d-price"><span class="d-buy-k">Prix indicatif</span><span class="price-tag" id="detailPrice"></span><span class="price-from">{ind_txt(fam) if fam else IND}</span></div>
      <div class="offers" id="detailOffers"></div>
    </div>
    <a class="d-more" id="detailMore" href="#"><span class="d-more-t">Avis et tests détaillés<small id="detailMoreN"></small></span><span class="d-more-go" aria-hidden="true">→</span></a>
  </div>
</div></div>"""


def table(items, fam, show_cat=True, root='../'):
    rows = []
    for d in items:
        pr = d["press"]
        pcell = (f'<td class="num"><span class="press-chip">{fr(pr["avg"])}<small>·{pr["n"]}</small></span></td>' if pr else '<td class="num muted">sans note</td>')
        m0 = d["m"][0]
        rows.append(f"""<tr data-id="{d['id']}" data-cat="{d['cat']}" data-budget="{d['bucket']}" data-price="{d['p']}" data-press="{pr['avg'] if pr else -1}" data-idx="{d['idx'] or -1}" data-rating="{d['r']}" tabindex="0">
<td class="name-cell">{f'<img class="thumb" src="{root}assets/img/p/{d["img"]}" alt="{E(d["short"])}" width="48" height="36" loading="lazy">' if d['img'] else ''}<span class="dot {CAT[d['cat']]['cls'].replace('f-', '')}"></span><span>{E(d['short'])}</span></td>{f"<td>{CAT[d['cat']]['label']}</td>" if show_cat else ''}
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
UNIVERS = [("info", "Informatique", "PC, écrans et imprimantes", "assets/img/pose-tour.webp"),
           ("maison", "Maison", "TV, son, photo et robots", "assets/img/pose-video-hub.webp")]
NAV_PLURAL = {"pc-portable": "PC portables", "ordinateur-de-bureau": "PC de bureau", "ecran-pc": "Écrans", "imprimante": "Imprimantes",
              "aspirateur-robot": "Robots aspirateurs", "tv": "Téléviseurs", "audio": "Audio", "photo-video": "Photo et vidéo"}


def nav_html(root, active):
    """En-tête du site : deux onglets d'univers (Informatique, Maison) avec méga-menu, lien Méthode à l'écart, volets sur mobile."""
    items, msec = "", ""
    for k, kick, titre, pose in UNIVERS:
        fams = [f for f in FAMILIES if (f["slug"] in MAISON_SLUGS) == (k == "maison")]
        cur = " is-current" if active in {f["slug"] for f in fams} else ""
        cols = "".join(
            f'<div class="b-col{" is-active" if active == f["slug"] else ""}"><a class="b-col-t" href="{root}{f["slug"]}/">{NAV_PLURAL.get(f["slug"], f["plural"])}</a><ul>'
            + "".join(f'<li><a href="{root}{f["slug"]}/{c["slug"]}/"><span class="dot {c["cls"].replace("f-", "")}"></span>{c["label"]}</a></li>' for c in f["cats"])
            + "</ul></div>" for f in fams)
        items += (f'<div class="b-item u-{k}{cur}" data-u="{k}"><button class="b-trig" type="button" aria-expanded="false" aria-controls="bp-{k}">'
                  f'<span class="b-tab"><i class="bub"></i><span class="b-tt"><small>{kick}</small><b>{titre}</b></span><span class="caret">▾</span></span></button>\n'
                  f'  <div class="b-panel" id="bp-{k}"><div class="b-cols">{cols}</div><img class="b-mascot" src="{root}{pose}" alt="" width="170" height="250"></div></div>')
        n = sum(len(f["cats"]) for f in fams)
        det = "".join(
            f'<details class="m-fam"{" open" if active == f["slug"] else ""}><summary><span>{NAV_PLURAL.get(f["slug"], f["plural"])}</span><span class="n">{len(f["cats"])}</span></summary>'
            f'<a class="m-all" href="{root}{f["slug"]}/">Tout le comparatif</a><ul>'
            + "".join(f'<li><a href="{root}{f["slug"]}/{c["slug"]}/"><span class="dot {c["cls"].replace("f-", "")}"></span>{c["label"]}</a></li>' for c in f["cats"])
            + "</ul></details>" for f in fams)
        msec += f'<section class="m-uni u-{k}"><h2><i class="bub"></i><span>{titre}<small>{kick}, {n} usages</small></span></h2>{det}</section>'
    meth = ' aria-current="page"' if active == "methode" else ""
    return f"""<header class="hd hd-b">
  <div class="hd-row">
    <a class="brand-lockup" href="{root or "./"}">
      <img class="brand-mark" src="{root}assets/img/logo-face.webp" alt="Symbole Top 10 Geek" width="40" height="40">
      <div class="brand-text"><div class="brand">TOP<span class="dot">10</span>GEEK</div><div class="baseline">{BASELINE}</div></div>
    </a>
    <nav class="b-nav" aria-label="Rubriques">{items}</nav>
    <a class="hd-method" href="{root}methode"{meth}>Méthode</a>
    <button class="hd-toggle" id="hdToggle" type="button" aria-expanded="false" aria-controls="hdPanel">Menu</button>
  </div>
  <div class="hd-panel" id="hdPanel" hidden>{msec}<a class="m-method" href="{root}methode">Méthode</a></div>
</header>"""


PERSON_ID = DOMAIN + "/a-propos#matthieu-tixier"
ORG = {"@type": "Organization", "@id": DOMAIN + "/#organisation", "name": "Top 10 Geek", "alternateName": ["Top10Geek", "top10geek.fr"],
       "url": DOMAIN + "/", "description": "Comparatif high-tech francophone indépendant : synthèse des tests de la presse en une note sur 10.",
       "logo": {"@type": "ImageObject", "@id": DOMAIN + "/#logo", "url": DOMAIN + "/assets/img/logo-face.png", "width": 192, "height": 192},
       "image": {"@id": DOMAIN + "/#logo"}, "email": "contact@top10geek.fr", "founder": {"@id": PERSON_ID}, "foundingDate": "2026",
       "areaServed": "FR", "knowsLanguage": "fr",
       "publishingPrinciples": DOMAIN + "/methode", "ownershipFundingInfo": DOMAIN + "/a-propos",
       # profils officiels de la marque ; en ajouter un ici dès qu'il existe (LinkedIn, X…), même nom « Top 10 Geek »
       "sameAs": ["https://www.reddit.com/user/top10geek"]}
PERSON = {"@type": "Person", "@id": PERSON_ID, "name": "Matthieu Tixier", "url": DOMAIN + "/a-propos",
          "jobTitle": "Éditeur de Top 10 Geek", "worksFor": {"@id": DOMAIN + "/#organisation"}}


def ld_page(path, title):
    """Page web signée : auteur (Matthieu Tixier) et éditeur (Top 10 Geek)."""
    return {"@type": "WebPage", "@id": f"{DOMAIN}/{path}", "url": f"{DOMAIN}/{path}", "name": title, "inLanguage": "fr-FR",
            "author": {"@id": PERSON_ID}, "publisher": {"@id": DOMAIN + "/#organisation"}}


def byline(root, extra=""):
    return (f'<p class="byline">Sélection éditée par <a href="{root}a-propos">Matthieu Tixier</a> · '
            f'<a href="{root}methode#classement">critères de classement</a>{extra}</p>')


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


def og_pour(path):
    """Image de partage dédiée à une famille ou un usage (assets/img/og/<famille>[-<usage>].jpg), produite par _video/scripts/render-og.mjs.
    Sans fichier correspondant, on garde l'image générique."""
    slug = path.strip("/").replace("/", "-")
    if slug and os.path.exists(f"{OUT}/assets/img/og/{slug}.jpg"):
        return f"assets/img/og/{slug}.jpg"
    return "assets/img/og-image.jpg"


def indexable(d):
    """Fiche produit indexable si elle repose sur au moins 2 notes chiffrées OU au moins 2 tests presse recensés,
    même sans note publique (décision du 20/10/2026, après l'audit SEO du 10/10/2026 : ces fiches apportaient 43 % des clics Google).
    Les fiches à un seul test restent en ligne et dans les classements, mais en noindex,follow et hors sitemap.
    L'affichage ne change pas : pastilles « 1 seul test noté », « testé, sans note », fin de classement."""
    return (bool(d["press"]) and d["press"]["n"] >= 2) or d["tests"]["tests"] >= 2


# ---------------------------------------------------------------- Vitesse d'affichage (audit SEO du 10/10/2026)
# Polices hébergées sur le site (assets/fonts, fichiers @fontsource, sous-ensemble latin), polices de secours ajustées
# (size-adjust calculé sur Liberation Sans / Mono, métriques d'Arial et de Courier New) pour limiter le décalage au chargement.
FONTS_CSS = """@font-face{font-family:"Bricolage Grotesque";font-style:normal;font-display:swap;font-weight:200 800;font-stretch:100%;src:url(/assets/fonts/bricolage-grotesque.woff2) format("woff2-variations"),url(/assets/fonts/bricolage-grotesque.woff2) format("woff2");}
@font-face{font-family:"Plus Jakarta Sans";font-style:normal;font-display:swap;font-weight:200 800;src:url(/assets/fonts/plus-jakarta-sans.woff2) format("woff2-variations"),url(/assets/fonts/plus-jakarta-sans.woff2) format("woff2");}
@font-face{font-family:"IBM Plex Mono";font-style:normal;font-display:swap;font-weight:500;src:url(/assets/fonts/ibm-plex-mono-500.woff2) format("woff2");}
@font-face{font-family:"IBM Plex Mono";font-style:normal;font-display:swap;font-weight:600;src:url(/assets/fonts/ibm-plex-mono-600.woff2) format("woff2");}
@font-face{font-family:"IBM Plex Mono";font-style:normal;font-display:swap;font-weight:700;src:url(/assets/fonts/ibm-plex-mono-700.woff2) format("woff2");}
@font-face{font-family:"Bricolage Fallback";font-weight:100 599;src:local("Arial"),local("Liberation Sans"),local("Helvetica");size-adjust:99.3%;ascent-override:93.7%;descent-override:27.2%;line-gap-override:0%;}
@font-face{font-family:"Bricolage Fallback";font-weight:600 900;src:local("Arial Bold"),local("Arial-BoldMT"),local("Liberation Sans Bold"),local("Helvetica Bold");size-adjust:98%;ascent-override:95%;descent-override:27.6%;line-gap-override:0%;}
@font-face{font-family:"Jakarta Fallback";src:local("Arial"),local("Liberation Sans"),local("Helvetica");size-adjust:103.9%;ascent-override:99.9%;descent-override:21.4%;line-gap-override:0%;}
@font-face{font-family:"Plex Fallback";src:local("Courier New"),local("Liberation Mono"),local("Courier");size-adjust:100%;ascent-override:102.5%;descent-override:27.5%;line-gap-override:0%;}
"""


def build_css():
    css = FONTS_CSS + "".join(open(SRC + f, encoding="utf-8").read() for f in CSS_FILES)
    css = (css.replace('"Bricolage Grotesque",', '"Bricolage Grotesque","Bricolage Fallback",')
              .replace('"Plus Jakarta Sans",', '"Plus Jakarta Sans","Jakarta Fallback",')
              .replace('"IBM Plex Mono",', '"IBM Plex Mono","Plex Fallback",'))
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)                 # commentaires
    css = re.sub(r"\s*\n\s*", "", css)                                # retours à la ligne et indentation
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    return css.replace(";}", "}")


CSS_INLINE = build_css()


def variante(nom, largeur):
    """Image réduite (WebP) à côté de l'original : assets/img/<...>/<nom>-<largeur>.webp, créée une fois (Pillow)."""
    src = os.path.join(OUT, nom)
    dst = src[:-5] + f"-{largeur}.webp"
    if not os.path.exists(dst) and os.path.exists(src):
        try:
            from PIL import Image
            im = Image.open(src)
            if im.width > largeur:
                im.resize((largeur, round(im.height * largeur / im.width)), Image.LANCZOS).save(dst, "WEBP", quality=80, method=6)
        except Exception:
            return None
    return nom[:-5] + f"-{largeur}.webp" if os.path.exists(dst) else None


# largeur affichée des photos produits selon leur bloc (mesurée à 1280 et 390 px)
SIZES = {"tc-photo": "(max-width: 700px) 90vw, 540px", "f-photo": "(max-width: 700px) 90vw, 320px",
         "pick-photo": "(max-width: 700px) 70vw, 260px", "ch-photo": "(max-width: 700px) 70vw, 260px"}
def hero_scene(name, alt, pre):
    """Pose détourée de la mascotte (webp transparent 640 px + variante 320 px) pour les héros de l'univers Maison."""
    from PIL import Image
    w, h = Image.open(os.path.join(OUT, "assets/img", f"{name}.webp")).size
    return (f'<img class="hero-badge scene" src="{pre}assets/img/{name}.webp" srcset="{pre}assets/img/{name}-360.webp 320w, {pre}assets/img/{name}.webp 640w" '
            f'sizes="(max-width: 720px) 70vw, 380px" alt="{alt}" width="{w}" height="{h}" fetchpriority="high">')

EAGER = ("brand-mark", "hh-mascot", "hh-sticker", "hero-badge", "fetchpriority")


def images(html):
    """Images responsives (srcset) pour les photos produits et la mascotte ; chargement différé hors du haut de page."""
    def photo(m):
        tag, pre, nom = m.group(0), m.group(1), m.group(2)
        v = variante(f"assets/img/p/{nom}.webp", 280)
        if not v:
            return tag
        if 'width="560"' in tag:
            avant = html[max(0, m.start() - 200):m.start()] + tag
            cls = max(SIZES, key=lambda k: avant.rfind(k))
            sz = SIZES[cls] if avant.rfind(cls) >= 0 else "(max-width: 700px) 90vw, 320px"
            return tag.replace(f'src="{pre}assets/img/p/{nom}.webp"', f'src="{pre}assets/img/p/{nom}.webp" srcset="{pre}{v} 280w, {pre}assets/img/p/{nom}.webp 560w" sizes="{sz}"')
        return tag.replace(f'src="{pre}assets/img/p/{nom}.webp"', f'src="{pre}{v}"')
    html = re.sub(r'<img[^>]*src="((?:\.\./)*)assets/img/p/([^"/]+)\.webp"[^>]*>', photo, html)

    def mascotte(m):
        tag, pre = m.group(0), m.group(1)
        v = variante("assets/img/mascotte-persona-v2.webp", 400)
        return tag if not v else tag.replace(f'src="{pre}assets/img/mascotte-persona-v2.webp"',
                                             f'src="{pre}assets/img/mascotte-persona-v2.webp" srcset="{pre}{v} 400w, {pre}assets/img/mascotte-persona-v2.webp 800w" sizes="(max-width: 700px) 90vw, 500px"')
    html = re.sub(r'<img[^>]*src="((?:\.\./)*)assets/img/mascotte-persona-v2\.webp"[^>]*>', mascotte, html)

    def lazy(m):
        tag = m.group(0)
        if "loading=" in tag or any(k in tag for k in EAGER):
            return tag
        return tag[:-1] + ' loading="lazy" decoding="async">'
    return re.sub(r"<img\b[^>]*>", lazy, html)


def fit_title(t, limit=65):
    """SEO 29/10/2026 : title <= 65 caractères (Google tronque au-delà)."""
    for pat in (r" \| Top 10 Geek$", r"[ ,:]+tests et prix$", r" par usage$"):
        if len(t) <= limit:
            break
        t = re.sub(pat, "", t)
    return t


def fit_desc(d, limit=160):
    """SEO 29/10/2026 : meta description <= 160 caractères, sans couper une phrase au milieu si possible."""
    if len(d) <= limit:
        return d
    d = d.replace(", points forts et faibles.", ".").replace(", points forts et points faibles.", ".")
    d = d.replace(" classés d'après les tests de la presse : note sur 10, prix indicatif.", " classés par note presse, avec prix indicatif.")
    d = d.replace(" classés d\u2019après les tests de la presse : note sur 10, prix indicatif.", " classés par note presse, avec prix indicatif.")
    if len(d) > limit:
        m = re.match(r"^(.*? : )(.+?)(\. Prix indicatifs\.)$", d)
        if m:
            marques = m.group(2).split(", ")
            while len(marques) > 2 and len(m.group(1) + ", ".join(marques) + m.group(3)) > limit:
                marques.pop()
            d = m.group(1) + ", ".join(marques) + m.group(3)
    if len(d) > limit:
        d = d[:limit - 1].rsplit(" ", 1)[0].rstrip(",;: ") + "\u2026"
    return d


def page(root, title, desc, path, body, active="", extra="", body_cls="", og_img="assets/img/og-image.jpg", ld=None, robots=None):
    if og_img == "assets/img/og-image.jpg":
        og_img = og_pour(path)
    title = fit_title(title)  # SEO 27/10/2026 puis 29/10/2026 : Google tronque au-delà de ~65 caractères
    desc = fit_desc(desc)
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8"><script>document.documentElement.classList.add('js')</script>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{DOMAIN}/{path}">{f'<meta name="robots" content="{robots}">' if robots else ''}
<meta property="og:type" content="website"><meta property="og:site_name" content="Top 10 Geek"><meta property="og:url" content="{DOMAIN}/{path}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{DOMAIN}/{og_img}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{DOMAIN}/{og_img}">
<link rel="icon" type="image/png" href="{root}assets/img/logo-face.png">
<link rel="preload" href="/assets/fonts/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/fonts/plus-jakarta-sans.woff2" as="font" type="font/woff2" crossorigin>
<style>{CSS_INLINE}</style>
{ld_script(ld)}</head>
<body class="{(body_cls + " univers-maison").strip() if path.startswith(MAISON_SLUGS) else body_cls}">
<div class="wrap">
  {nav_html(root, active)}
{body}
  <footer>
    <div class="disclosure" id="affiliation">Certains liens de ce site sont des liens d'affiliation (à ce jour : {AFF_TXT}) : si vous achetez via ces liens, nous pouvons percevoir une commission. Cela n'entraîne aucun coût supplémentaire pour vous et n'influence pas nos verdicts, établis avant toute recherche de lien commercial. {AMAZON_MENTION}</div>
    <div class="foot-row">
      <div class="foot-sig"><img src="{root}assets/img/logo-face.webp" alt="" width="32" height="32">TOP 10 GEEK — {BASELINE}</div>
      {foot_tail(root)}
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
        content = images(content)
        assert 'class="fill"' not in content, path
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(content)


def usage_cards(fam, root):
    out = []
    for c in fam["cats"]:
        top = by_cat_view[c["key"]][0]
        pr = top["press"]
        note = f'{fr(pr["avg"])}/10 presse' if pr else "testé, sans note"
        out.append(f"""<a class="usage-card" href="{root}{fam['slug']}/{c['slug']}/">
  <div class="uc-art"><img src="{root}assets/img/badge-{c['badge']}.webp" alt="" loading="lazy" width="110" height="110"></div>
  <div class="uc-body"><span class="uc-tag">{c['tag']}</span><h3><span class="dot {c['cls'].replace('f-', '')}"></span>{c['h']}</h3>
  <p class="uc-pick">Notre n° 1 : <b>{E(top['short'])}</b> — {note}</p>
  <span class="uc-go">{'Voir le top 10' if not fam['provisional'] else 'Voir la sélection'} →</span></div></a>""")
    return "".join(out)


FAQ_L = [
    ("Comment est calculée la note presse ?", "C'est la moyenne simple des notes publiées par les médias spécialisés (Notebookcheck, Clubic, Les Numériques, Tom's Hardware, TechRadar…), toutes converties sur 10 : 4/5 devient 8/10, 87 % devient 8,7/10. Le nombre de tests est toujours affiché. Quand la note porte sur une autre configuration de la même gamme, nous l'indiquons."),
    ("Comment est établi le classement ?", "En tête : « le choix de la bande », notre recommandation pour l'usage : de préférence un produit de la zone « bonnes affaires » du radar (note presse d'au moins 8/10, prix sous la médiane de l'usage), si sa note repose sur au moins 3 notes presse. Ensuite viennent les ordinateurs notés par au moins 3 médias, puis ceux qui n'ont qu'1 ou 2 notes, puis ceux testés sans note chiffrée. Dans chaque groupe, ils sont classés par note presse ajustée : une note isolée pèse moins qu'une moyenne de nombreux tests."),
    ("Faut-il 16 ou 32 Go de RAM en 2026 ?", "16 Go reste le minimum confortable pour de la bureautique ou du gaming courant. Pour la création ou pour garder la machine plusieurs années, 32 Go évite de la remplacer prématurément."),
    ("Pourquoi certains ordinateurs n'ont pas de note presse ?", "Tous les ordinateurs de la sélection ont été testés par au moins un média. Mais certains tests ne donnent pas de note chiffrée : dans ce cas nous l'indiquons (bulle en pointillés) et nous donnons le lien vers le test plutôt que d'inventer une note."),
    ("D'où viennent les prix ?", f"Nous affichons un prix indicatif par ordinateur : le plus bas que nous avons constaté chez les marchands (Amazon, Darty, Acer Store, Geekom, Electro Dépôt) en {PRIX_DATE}, arrondi à la dizaine d'euros. Il sert à situer la machine, pas à comparer les marchands : le prix a pu changer depuis et la configuration exacte peut différer d'un marchand à l'autre. Pour Electro Dépôt, nous affichons en plus son prix exact, tiré de son flux produits officiel, avec la date du relevé. Seul le prix affiché par le marchand fait foi."),
]


def fam_faq(fam):
    return {"ecran": FAQ_E, "imprimante": FAQ_I, "robot": FAQ_S, "tv": FAQ_T, "audio": FAQ_A, "video": FAQ_V}.get(fam["key"], FAQ_L)


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
      {byline(root)}
      <div class="spec-row">
        <div><strong>{len(all_items)}</strong>{fam.get('stat_noun', fam['plural'])} sélectionné{'e' if fam['key'] == 'imprimante' else ''}s</div>
        <div><strong>{sum(d["tests"]["tests"] for d in all_items)}</strong>tests presse recensés</div>
        <div><strong>{len(cats)}</strong>usage{'s' if len(cats) > 1 else ''}</div>
      </div>
    </div>
    {hero_scene(fam['mascot'], fam['scene_alt'], '../') if fam.get('scene_alt') else f'<img class="hero-badge tall big" src="../assets/img/{fam["mascot"]}.webp" alt="La mascotte Top 10 Geek" width="220" height="260">'}
  </section>
  {PROVISIONAL_NOTE if fam['provisional'] else ''}
  <section class="comparator" id="comparateur">
    <div class="comparator-head">
      <div><h2>Ce qu'en dit la presse, et ce que ça coûte</h2>
      <p class="comparator-sub">Chaque bulle est {'une' if fam['key'] == 'imprimante' else 'un'} {fam['noun']}. <b>Plus elle est à droite, mieux la presse l'a noté ; plus elle est basse, moins il est cher.</b> Cliquez sur une bulle pour lire le verdict.</p></div>
      <img class="comparator-pose" src="../assets/img/{'badge-robots-laveurs-v2' if fam['key'] == 'robot' else 'pose-investigation'}.webp" alt="" width="88" height="88">
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
    title = ("Meilleur PC portable 2026 : tous les tests par usage | Top 10 Geek" if fam["key"] == "laptop"
             else "Meilleur ordinateur de bureau 2026 : tours, mini-PC, AIO | Top 10 Geek" if fam["key"] == "desktop" else fam["title"])
    desc = (f"{len(all_items)} PC portables 2026 classés par usage avec une note presse moyenne sur 10 : bureautique, création, gaming, polyvalent, low-cost."
            if fam["key"] == "laptop" else f"{len(all_items)} ordinateurs de bureau 2026 classés par usage avec une note presse sur 10 et un prix indicatif : bureautique, création, gaming, mini-PC, tout-en-un."
            if fam["key"] == "desktop" else fam["desc"])
    write(f"{fam['slug']}/index.html", page(root, title, desc, f"{fam['slug']}/", body, fam["slug"], js_data(sel, root, by_cat[cats[0]["key"]][0]["id"]),
          ld=[ld_crumbs(("Accueil", ""), (fam["plural"], f"{fam['slug']}/")), ld_page(f"{fam['slug']}/", title), PERSON, ld_faq(fam_faq(fam)),
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
        return f'<span class="pn">{fr(pr["avg"])}</span><span class="pd">/10</span> <span class="pc">note presse · {pr["n"]} note{"s" if pr["n"] > 1 else ""}{gam}</span>{few(d)}'
    return f'<span class="pn none">—</span> <span class="pc">{ts["tests"]} test{"s" if ts["tests"] > 1 else ""} presse, sans note chiffrée{gam}</span>'


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
      {f'<img src="{root}assets/img/p/{a["img"]}" alt="{E(a["short"])}" width="96" height="72" loading="lazy">' if a['img'] else ''}
      <b>{E(a['short'])}</b><span class="alt-why">{E(reason)}</span><span class="alt-meta">{meta}</span></a>''')
    return f"""<section class="pick" id="notre-choix" data-z="choix" data-pid="{d['id']}">
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
        <a class="cta big buy" href="{E(best['url'])}" target="_blank" rel="{rel_m(best['m'])}">{cta_txt(best)}</a>
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
RANK_RULE = ("<p class=\"rank-rule\"><b>Comment ce classement est établi.</b> En tête, notre choix pour l'usage : de préférence un produit de la zone « bonnes affaires » du radar "
             "(note presse d'au moins 8/10 et prix sous la médiane de l'usage), à condition que sa note repose sur au moins 3 notes presse. Ensuite : d'abord les produits notés par au moins 3 médias, puis ceux qui n'ont qu'1 ou 2 notes, "
             "puis ceux testés sans note chiffrée. Dans chaque groupe, nous classons par note presse ajustée : une note isolée compte moins "
             "qu'une moyenne de nombreux tests. La note affichée reste la moyenne simple des médias. "
             "<a href=\"{root}methode#classement\">Détail de la méthode</a>.</p>")


# Pages usage à titre, H1 et réponse en tête dédiés (rapport hebdo du 26/10/2026, préconisations 2 et 4 :
# « meilleur pc tout-en-un » en place 7 sans visite, /imprimante/photo/ 84 apparitions en place 64).
USAGE_SEO = {
    "reconditionne": dict(title="Meilleur PC portable reconditionné 2026 : le top 10 des tests | Top 10 Geek",
                          desc="Quel PC portable reconditionné choisir ? 10 PC pros (Dell Latitude, ThinkPad, EliteBook) classés par tests presse, avec le prix de la configuration vendue.",
                          h1='Meilleur <span class="flash">PC portable reconditionné</span> 2026 : le top 10'),
    "d-aio": dict(title="Meilleur ordinateur tout-en-un 2026 : le top 10 des tests",
                  desc="Quel est le meilleur PC tout-en-un en 2026 ? 10 ordinateurs tout-en-un classés par note presse, avec prix indicatif, points forts et points faibles.",
                  h1='Meilleur <span class="flash">ordinateur tout-en-un</span> 2026 : le top 10'),
    "d-mini": dict(title="Meilleur mini-PC 2026 : le top 10 des tests et des prix",
                   desc="Quel est le meilleur mini-PC en 2026 ? 10 mini-PC classés par note presse, avec prix indicatif, points forts et points faibles.",
                   h1='Meilleur <span class="flash">mini-PC</span> 2026 : le top 10'),
    "i-photo": dict(title="Meilleure imprimante photo 2026 : le top 10 des tests | Top 10 Geek",
                    desc="Quelle est la meilleure imprimante photo en 2026 ? 10 modèles classés par note presse, de l'imprimante de poche à l'A3+, avec prix indicatif et points faibles.",
                    h1='Meilleure <span class="flash">imprimante photo</span> 2026 : le top 10'),
}


def _lien(d, root):
    return f'<a href="{root}{d["purl"]}">{E(d["short"])}</a>'


def _note(d):
    pr = d["press"]
    if pr:
        return f'{fr(pr["avg"])}/10 sur {pr["n"]} note{"s" if pr["n"] > 1 else ""}, {d["price_txt"].replace(" ", "\u00a0")}'
    t = d["tests"]["tests"]
    return f'{t} test{"s" if t > 1 else ""} sans note chiffrée, {d["price_txt"].replace(" ", "\u00a0")}'


def reponse_usage(c, items, root):
    """Réponse directe en tête de page, calculée sur le classement (rien d'écrit à la main sur les produits)."""
    if c["key"] == "d-aio":
        a = items[0]
        out = [f'selon la presse, le meilleur PC tout-en-un est l\'{_lien(a, root)} ({_note(a)}).' if a["short"].startswith("Apple")
               else f'selon la presse, le meilleur PC tout-en-un est le {_lien(a, root)} ({_note(a)}).']
        vus = [a]
        if a["short"].startswith("Apple"):
            w = next((d for d in items if not d["short"].startswith("Apple")), None)
            if w:
                out.append(f'Sous Windows : {_lien(w, root)} ({_note(w)}).')
                vus.append(w)
        ch = min(items, key=lambda d: d["p"])
        if ch not in vus:
            out.append(f'Le moins cher de la sélection : {_lien(ch, root)} ({_note(ch)}).')
    elif c["key"] == "i-photo":
        grp = [("Pour des tirages de poche (papier Zink ou film Instax)", r"poche|instantan"),
               ("En 10 × 15", r"10 × 15"), ("En A4 ou A3+", r"A4|A3")]
        out = []
        for lab, rx in grp:
            d = next((x for x in items if re.search(rx, x["ref"], re.I)), None)
            if d:
                out.append(f'{lab} : {_lien(d, root)} ({_note(d)}).')
        if not out:
            return ""
        out[0] = out[0][0].lower() + out[0][1:]
        out.append("Le coût par photo dépend surtout du consommable : papier Zink ou film Instax pour les modèles de poche, "
                   "cartouche et papier vendus ensemble pour la sublimation, encre en cartouches ou en réservoirs pour l'A4 et l'A3+.")
    elif c["key"] == "d-mini":
        a = items[0]
        out = [f'selon la presse, le meilleur mini-PC est le {_lien(a, root)} ({_note(a)}).']
        ch = min(items, key=lambda d: d["p"])
        if ch is not a:
            out.append(f'Le moins cher de la sélection : {_lien(ch, root)} ({_note(ch)}).')
    elif c["key"] == "reconditionne":
        a = items[0]
        out = [f'selon la presse, le mieux placé est le {_lien(a, root)} ({_note(a)}).']
        ch = min(items, key=lambda d: d["p"])
        if ch is not a:
            out.append(f'Le moins cher de la sélection : {_lien(ch, root)} ({_note(ch)}).')
        out.append("Les notes portent sur le modèle neuf à sa sortie ; le prix est celui de la configuration reconditionnée indiquée sur chaque fiche.")
    else:
        return ""
    return f'<p class="answer"><b>En bref :</b> {" ".join(out)}</p>'


def usage_page(fam, c):
    root = "../../"
    items = by_cat_view[c["key"]]
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
            big = f'<span class="pn">{fr(pr["avg"])}</span><span class="pd">/10</span> <span class="pc">note presse · {pr["n"]} note{"s" if pr["n"] > 1 else ""}{gam}</span>{few(d)}'
        else:
            big = f'<span class="pn none">—</span> <span class="pc">{ts["tests"]} test{"s" if ts["tests"] > 1 else ""} presse, sans note chiffrée{gam}</span>'

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
            f'<a class="offer m-{MERCHANT_CLS.get(o["m"], "x")}{" has-p" if prix_exact(o) else ""}" href="{E(o["url"])}" target="_blank" rel="{rel_m(o["m"])}" title="{E(o["name"])}">'
            f'<span class="o-m">{E(o["m"])}</span><span class="o-c">{E(o.get("cfg") or "")}</span>{o_prix(o)}<span class="o-go">Voir →</span></a>' for o in d["offers"])
        onote = RECO_NOTE if d["cat"] == "reconditionne" else "La configuration peut différer d'un marchand à l'autre : vérifiez la fiche avant d'acheter."
        offers_html = f'<div class="offers"><span class="k">Où l\'acheter</span>{offs}<p class="o-note">{onote}</p></div>'
        rating = f'{fr(d["r"])} ★ <small>({d["nrev"]})</small>' if d["r"] > 0 else ""
        rank_lbl = "NOTRE CHOIX" if i == 1 else f"SUR {n}"
        photo = (f'<a class="f-photo" href="{E(d["url"])}" target="_blank" rel="{rel_m(d["offers"][0]["m"])}"><img src="../../assets/img/p/{d["img"]}" alt="{E(d["short"])}" width="560" height="420" loading="lazy"></a>' if d["img"] else "")
        best = d["offers"][0]
        fiches.append(f"""<article class="fiche tcard{' top' if i == 1 else ''}" id="{d['id']}" data-z="top10" data-pid="{d['id']}" data-budget="{d['bucket']}" data-rank="{i}" data-price="{d['p']}" data-press="{pr['avg'] if pr else -1}" data-tests="{ts['tests']}" style="--c:{c['color']}">
  <div class="tc-top"><span class="tc-rank">#{i}<small>{'notre choix' if i == 1 else f'sur {n}'}</small></span><span class="fbadge{' alt' if i != 1 else ''}">{E(d['badge'])}</span></div>
  {f'<a class="tc-photo" href="{root}{d["purl"]}"><img src="{root}assets/img/p/{d["img"]}" alt="{E(d["short"])}" width="560" height="420" loading="lazy"></a>' if d['img'] else '<div class="tc-photo tc-nophoto">Photo à venir</div>'}
  <h3 class="tc-name"><a href="{root}{d['purl']}">{E(d['short'])}</a></h3>
  <div class="tc-ref">{E(d['ref'])}</div>
  <p class="tc-verdict">{E(d['verdict'])}</p>
  <div class="tc-bottom"><div class="ch-score{'' if pr else ' none'}">{(f'<b>{fr(pr["avg"])}</b><small>/10</small> <em>{pr["n"]} note{"s" if pr["n"] > 1 else ""} presse{gam}</em>') if pr else f'<b>Testé</b><em>{ts["tests"]} test{"s" if ts["tests"] > 1 else ""}, sans note chiffrée</em>'}</div>{few(d, "few tc-few")}<span class="tc-price">{d['price_txt']}<small>prix indicatif</small></span></div>
  <div class="tc-actions"><a class="cta" href="{E(best['url'])}" target="_blank" rel="{rel_m(best['m'])}">{cta_txt(best)}</a><a class="see-all" href="{root}{d['purl']}">Avis et tests →</a></div>
</article>""")
    mascot = ('<img class="hero-badge tall" src="../../assets/img/pose-lowcost.webp" alt="La mascotte avec un PC en promo" width="170" height="260">' if c["key"] == "lowcost"
              else hero_scene("pose-" + c["scene"], c["scene_alt"], "../../") if c.get("scene")
              else f'<img class="hero-badge" src="../../assets/img/badge-{c["badge"]}.webp" alt="" width="190" height="190">')
    # peu de notes publiques (imprimantes : notes des associations réservées aux abonnés) :
    # on met en avant les tests de laboratoire plutôt qu'un « 0 notes compilées » trompeur
    labs = sum(1 for d in items for x in (d["tests"] or {}).get("notes", []) if x["src"] in ASSOC)
    if n_notes < 3 and labs:
        third_stat = f'<div><strong>{labs}</strong>tests en laboratoire (associations)</div>'
    else:
        third_stat = f'<div><strong>{n_notes}</strong>note{"s" if n_notes > 1 else ""} compilée{"s" if n_notes > 1 else ""}</div>'
    top_word = f"Le top 10 {c.get('top_label', c['label']).lower()}" if n == 10 else f"Notre sélection {c.get('top_label', c['label']).lower()}"
    body = f"""
  <div class="crumb"><a href="../../">Accueil</a> › <a href="../">{fam['plural']}</a> › {c['label']}</div>
  <section class="usage-hero">
    <div>
      <div class="eyebrow">{c['tag'].upper()} · MAJ {maj(fam)}</div>
      <h1>{USAGE_SEO.get(c['key'], c)['h1']}</h1>
      <p>{c['intro']}</p>
      {reponse_usage(c, items, root)}
      {byline(root)}
      <p class="hero-links"><a href="#top10">Voir le classement complet ↓</a> · <a href="#guide">Lire le guide d'achat</a></p>
      <div class="spec-row">
        <div><strong>{n}</strong>{c.get('plural_low') or fam.get('plural_low', fam['plural'].lower())} sélectionné{'e' if fam['key'] == 'imprimante' else ''}s</div>
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
      <img class="comparator-pose" src="../../assets/img/{'badge-robots-laveurs-v2' if fam['key'] == 'robot' else 'pose-investigation'}.webp" alt="" width="88" height="88">
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
    <div class="section-head"><h2><img class="section-badge" src="../../assets/img/badge-{c['badge']}.webp" alt="" width="50" height="50">{top_word}</h2><div class="tag">Notre choix, puis note presse ajustée</div></div>
    {RANK_RULE.format(root=root)}
    {sort_bar(fam)}
    <div class="top-list tgrid" id="topList">{''.join(fiches)}</div>
  </section>
"""
    if fam["key"] == "laptop":
        title = f"Top 10 PC portables {c['label'].lower()} 2026 : tests et verdict | Top 10 Geek"
        desc = f"Les 10 meilleurs PC portables {c['label'].lower()} en 2026, classés par note presse, avec photos, prix indicatif, poids, points forts et points faibles."
    elif fam["key"] == "desktop":
        title = f"Top 10 {'mini-PC' if c['key'] == 'd-mini' else 'tout-en-un' if c['key'] == 'd-aio' else 'ordinateurs de bureau ' + c['label'].lower()} 2026 : tests et prix | Top 10 Geek"
        desc = f"Les 10 meilleurs ordinateurs de bureau {c['label'].lower()} en 2026, classés par note presse, avec photos, prix indicatif, points forts et points faibles."
    else:
        lab = (plain(c["h"]).lower().replace("écrans portables", "portables").replace("imprimantes photo", "photo")
               .replace("réservoirs d'encre", "à réservoirs d'encre").replace(" & télétravail", ""))
        title = fam["usage_title"].format(label=lab)
        desc = fam["usage_desc"].format(label=lab)
        if c.get("seo_title"):
            title, desc = c["seo_title"], c["seo_desc"]
    if c["key"] in USAGE_SEO:
        title, desc = USAGE_SEO[c["key"]]["title"], USAGE_SEO[c["key"]]["desc"]
    write(f"{fam['slug']}/{c['slug']}/index.html", page(root, title, desc, f"{fam['slug']}/{c['slug']}/", body, fam["slug"], js_data(items, root, items[0]["id"]),
          ld=[ld_crumbs(("Accueil", ""), (fam["plural"], f"{fam['slug']}/"), (c["label"], f"{fam['slug']}/{c['slug']}/")),
              ld_page(f"{fam['slug']}/{c['slug']}/", title), PERSON,
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


def synthese_html(d):
    """Synthèse rédigée à partir des tests lus (_source/syntheses.py), avec sa date et ses sources."""
    sy = d.get("synthese")
    if not sy:
        return ""
    paras = "".join(f"<p>{E(p.strip())}</p>" for p in sy["texte"].split("\n\n") if p.strip())
    jj = "/".join(reversed(sy["date"].split("-")))
    return (f'<div class="p-synth"><h3>Ce que disent les tests</h3>{paras}'
            f'<p class="p-synth-meta">Synthèse du {jj}, établie à partir de {sy["tests"]} test{"s" if sy["tests"] > 1 else ""} cités plus bas '
            f'({E(", ".join(sy["sources"]))}).</p></div>')


def score_haut(d, ts, medias, last):
    """Note presse en grand dans le haut de la fiche, sur ordinateur (v13, 20/10/2026) ; le mobile garde press-big."""
    pr = d["press"]
    ntxt = f'{ts["tests"]} test{"s" if ts["tests"] > 1 else ""} recensé{"s" if ts["tests"] > 1 else ""}, {medias} média{"s" if medias > 1 else ""}'
    when = f'<span class="ps-w">{last}</span>' if last else ""
    if pr:
        return (f'<a class="p-score" href="#consensus"><span class="ps-big"><b>{fr(pr["avg"])}</b><small>/10</small></span>'
                f'<span class="ps-t"><span class="ps-k">Note presse</span><span class="ps-l">Moyenne de <b>{pr["n"]} note{"s" if pr["n"] > 1 else ""}</b> · {ntxt}</span>{when}{few(d)}</span></a>')
    return (f'<a class="p-score none" href="#tests"><span class="ps-big"><b>—</b></span>'
            f'<span class="ps-t"><span class="ps-k">Note presse</span><span class="ps-l"><b>Testé, sans note publique</b> · {ntxt}</span>{when}</span></a>')


def radar_fiche(d, items, root, usage_url, usage_txt):
    """Radar de la fiche (v13, 20/10/2026) : le produit parmi les 10 de son usage, bulles cliquables vers les fiches,
    lecture calculée, liste numérotée ; sur mobile, une ligne « note presse » et 3 lignes de la liste."""
    n = len(items)
    ranks = {x["id"]: i + 1 for i, x in enumerate(items)}
    rank = ranks[d["id"]]
    others = [x for x in items if x["id"] != d["id"]]
    pr = d["press"]
    chips, phr = [], []
    if pr:
        nv = lambda x: round(x["press"]["avg"], 1)   # comparaison sur la note affichée
        noted = [x for x in items if x["press"]]
        pos = 1 + sum(1 for x in noted if nv(x) > nv(d))
        tie = any(nv(x) == nv(d) for x in others if x["press"])
        chips.append(f'Note presse : <b>{pos}<sup>{"er" if pos == 1 else "e"}</sup></b>{" ex æquo" if tie else ""} sur {len(noted)}')
        better = sum(1 for x in others if not x["press"] or nv(x) < nv(d))
        phr.append(f'mieux noté que {better} des {n - 1} autres modèles du top' if better else f'parmi les moins bien notés du top')
    else:
        phr.append("testé par la presse sans note publique : il est placé à gauche, hors de l'axe des notes")
    ppos = 1 + sum(1 for x in others if x["p"] < d["p"])
    chips.append(f'Prix : <b>{ppos}<sup>{"er" if ppos == 1 else "e"}</sup></b> moins cher sur {n}')
    dearer = sum(1 for x in others if x["p"] > d["p"])
    if pr:
        phr.append(f'moins cher que {dearer} d&#39;entre eux' if dearer else "le plus cher du top")
    else:
        phr[-1] += "." 
        phr.append(f'Il est moins cher que {dearer} des {n - 1} autres modèles du top' if dearer else "Il est le plus cher du top")
    med = sorted(x["p"] for x in items)[n // 2]
    if pr and pr["avg"] >= 8 and d["p"] <= med:
        chips.append('<span class="rf-deal">Zone « bonnes affaires »</span>')
    lecture = f'{E(d["short"])} : {" et ".join(phr)}.' if pr else f'{E(d["short"])} : {phr[0]} {phr[1]}.'
    # liste numérotée ; sur mobile seulement le n° 1, le produit et ses voisins
    keep = {items[0]["id"], d["id"]}
    for x in sorted(others, key=lambda x: abs(ranks[x["id"]] - rank)):
        if len(keep) >= 3: break
        keep.add(x["id"])
    rows = "".join(
        (f'<li class="rf-row cur{" mk" if x["id"] in keep else ""}" aria-current="page">' if x["id"] == d["id"] else f'<li class="rf-row{" mk" if x["id"] in keep else ""}">')
        + (f'<span class="rf-n">{ranks[x["id"]]}</span>' + (f'<span class="rf-name">{E(x["short"])} <small>ce modèle</small></span>' if x["id"] == d["id"]
           else f'<a class="rf-name" href="{root}{x["purl"]}">{E(x["short"])}</a>')
           + f'<span class="rf-s">{fr(x["press"]["avg"]) + "/10" if x["press"] else "sans note"}</span><span class="rf-p">{x["price_txt"]}</span></li>')
        for x in items)
    # ligne « note presse » (mobile)
    lo = min([6] + [int(x["press"]["avg"]) for x in items if x["press"]])
    def px(x):
        return 4 if not x["press"] else 14 + (x["press"]["avg"] - lo) / (10 - lo) * 82
    dots = "".join(f'<span class="rf-dot{" cur" if x["id"] == d["id"] else ""}{" nn" if not x["press"] else ""}" style="left:{px(x):.1f}%"></span>' for x in sorted(items, key=lambda x: x["id"] == d["id"]))
    ticks = "".join(f'<span class="rf-tk" style="left:{14 + (v - lo) / (10 - lo) * 82:.1f}%">{v}</span>' for v in range(lo, 11))
    cap_t = "translateX(-100%)" if px(d) > 85 else ("none" if px(d) < 12 else "translateX(-50%)")
    strip = (f'<div class="rf-strip" aria-hidden="true"><span class="rf-cap" style="left:{px(d):.1f}%;transform:{cap_t}">Ce modèle</span><div class="rf-line">{dots}</div>'
             f'<div class="rf-ticks"><span class="rf-tk sn" style="left:4%">sans</span>{ticks}</div></div>')
    svg = bubble_svg(items, f"Graphe : {d['short']} parmi les {n} {usage_txt}, note presse contre prix", root, sid="ficheRadar", link_key="purl", focus=d["id"], ranks=ranks)
    return f"""
  <section class="section p-sec p-radar" id="radar" data-zi="radar-fiche">
    <div class="section-head"><h2>Où se place-t-il dans le top {n} ?</h2><div class="tag">Radar · {E(usage_txt)}</div></div>
    <div class="rf-grid">
      <div class="rf-chart"><div class="chart-pane">{svg}</div>
        <p class="rf-help"><span class="rf-key" aria-hidden="true"></span><b>Ce modèle</b> · les chiffres sont les rangs du top · → À droite : mieux noté par la presse · ↑ En haut : plus cher · Taille : nombre de notes · Cliquez sur une bulle pour ouvrir sa fiche.</p></div>
      <div class="rf-side">
        <div class="rf-chips">{"".join(f'<span class="rf-chip">{x}</span>' for x in chips)}</div>
        <p class="rf-read">{lecture}</p>
        {strip}
        <ol class="rf-list">{rows}</ol>
        <a class="rf-more" href="{usage_url}">Voir le top {n} et le comparatif →</a>
      </div>
    </div>
  </section>"""


def lf(t):
    """Minuscule initiale, sauf sigle ou nom propre en majuscules (OLED, USB-C…)."""
    return t[0].lower() + t[1:] if len(t) > 1 and t[1].islower() else t


def plus_verdict(d):
    """[Retiré de la fiche le 20/10/2026 (v13) : doublon du consensus, conservé pour mémoire.] Complément du verdict (v12, 20/10/2026) : points forts et réserve principale relevés par la presse (mêmes données que plus bas)."""
    st = [lf(x.strip().rstrip(".")) for x in d["strengths"] if x.strip()]
    wk = [lf(x.strip().rstrip(".")) for x in d["weak"] if x.strip()]
    out = []
    if st:
        out.append("La presse apprécie : " + (", ".join(st[:-1]) + " et " + st[-1] if len(st) > 1 else st[0]) + ".")
    if wk:
        out.append(("Réserve principale : " if len(wk) > 1 else "Sa réserve : ") + wk[0] + ".")
    return f'<p class="p-more">{E(" ".join(out))}</p>' if out else ""


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
        f'<a class="offer m-{MERCHANT_CLS.get(o["m"], "x")}{" has-p" if prix_exact(o) else ""}" href="{E(o["url"])}" target="_blank" rel="{rel_m(o["m"])}" title="{E(o["name"])}">'
        f'<span class="o-m">{E(o["m"])}</span><span class="o-c">{E(o.get("cfg") or "")}</span>{o_prix(o)}<span class="o-go">Voir chez {E(o["m"])} →</span></a>' for o in d["offers"])
    specs_t = "Configuration de référence" if fam["key"] in ("laptop", "desktop") else "Caractéristiques principales"
    specs = f'<span class="ps-k">{specs_t}</span><p class="ps-ref">{E(d["ref"])}</p>' + "".join(f'<div class="mini"><span class="k">{k}</span><span class="v">{v}</span></div>' for k, v in [
        (fam["m_labels"][0], E(d["m"][0])), (fam["m_labels"][1], E(d["m"][1])),
        ("Avis clients Darty", f'{fr(d["r"])} ★ ({d["nrev"]} avis)' if d["r"] > 0 else "")] if v and v != "n.c.")

    # --- alternatives : les voisins du classement
    others = [x for x in items if x["id"] != d["id"]]
    near = sorted(others, key=lambda x: (abs(items.index(x) - (rank - 1)), items.index(x)))[:3]
    near.sort(key=lambda x: items.index(x))
    alt = "".join(f"""<a class="alt-card" href="{root}{a['purl']}">
      <span class="alt-k">N° {items.index(a) + 1} · {E(a['badge'])}</span>
      {f'<img src="{root}assets/img/p/{a["img"]}" alt="{E(a["short"])}" width="96" height="72" loading="lazy">' if a['img'] else ''}
      <b>{E(a['short'])}</b><span class="alt-why">{E(a['verdict'])}</span>
      <span class="alt-meta">{(fr(a['press']['avg']) + '/10 presse · ') if a['press'] else ''}{a['price_txt']}</span></a>""" for a in near)

    usage_txt = f"{fam['plural']} {c['label'].lower()}" if c["key"] not in ("d-mini", "d-aio") else ("mini-PC" if c["key"] == "d-mini" else "ordinateurs tout-en-un")
    usage_url = f"{root}{fam['slug']}/{c['slug']}/"
    rank_txt = (f'<b>Notre choix</b> dans le <a href="{usage_url}">top {n_items} {usage_txt}</a>' if rank == 1
                else f'<b>N° {rank} sur {n_items}</b> dans le <a href="{usage_url}">top {n_items} {usage_txt}</a>')
    if d["cat"] == "reconditionne":
        rank_txt += ' · <span class="reco-tag">Reconditionné, grade B · garanti 2 ans</span>'

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

    # --- bloc d'achat du haut de page (v11, 20/10/2026) : visible dès le premier écran sur mobile, un bouton par marchand
    # v11c (20/10/2026) : mise en page de la maquette validée par Matthieu sur ordinateur (cadre d'achat à droite avec un bouton
    # par marchand, encadrés presse / pour vous si / à éviter si, carte « le n° 1 ») ; sur mobile, version discrète v11b
    # (photo réduite, un bouton, les autres marchands en liens texte). Les deux variantes sont dans la page, le CSS choisit.
    autres = " · ".join(f'<a href="{E(o["url"])}" target="_blank" rel="{rel_m(o["m"])}">{E(o["m"])}</a>' for o in d["offers"][1:])
    buy_btns = "".join(buy_btn(o, i) for i, o in enumerate(d["offers"]))
    aff = any(o["m"] in AFFILIATED for o in d["offers"])
    medias_l = list(dict.fromkeys(nt["src"] for nt in ts["notes"]))
    med_txt = ", ".join(medias_l[:3]) + ("…" if len(medias_l) > 3 else "")
    if pr:
        presse = f'<b>{fr(pr["avg"])}/10</b> sur {pr["n"]} note{"s" if pr["n"] > 1 else ""} presse{few(d)}'
    else:
        presse = f'<b>{ts["tests"]} test{"s" if ts["tests"] > 1 else ""}, sans note publique</b>'
    top1 = ""
    if CARTE_N1 and rank > 1:
        t = items[0]
        t_meta = (f'{fr(t["press"]["avg"])}/10 presse ({t["press"]["n"]} note{"s" if t["press"]["n"] > 1 else ""})' if t["press"]
                  else f'{t["tests"]["tests"]} test{"s" if t["tests"]["tests"] > 1 else ""} presse') + f' · {t["price_txt"]}'
        t_ed = next((o for o in t["offers"] if prix_exact(o)), None)
        if t_ed:
            t_meta += f' · {euro2(t_ed["price"])} chez {E(t_ed["m"])}'
        t_img = f'<img src="{root}assets/img/p/{t["img"]}" alt="{E(t["short"])}" width="72" height="54">' if t["img"] else ""
        top1 = (f'<a class="p-top1" href="{root}{t["purl"]}">{t_img}<span class="p-top1-t"><span class="p-top1-k">Avant d&#39;acheter : le n° 1 des {usage_txt if usage_txt[1:2].isupper() else low_first(usage_txt)}</span>'
                f'<span class="p-top1-m"><b>{E(t["short"])}</b> · {t_meta}</span></span><span class="p-top1-go">Voir la fiche →</span></a>')

    body = f"""
  <div class="crumb"><a href="{root or "./"}">Accueil</a> › <a href="{root}{fam['slug']}/">{fam['plural']}</a> › <a href="{usage_url}">{c['label']}</a> › {name}</div>
  <section class="p-hero v11">
    <div class="p-text">
      <div class="p-head">
        <div class="p-chips"><a class="p-chip" href="{usage_url}">{"Notre choix" if rank == 1 else f"N° {rank} sur {n_items}"} · {E(usage_txt)}</a><span class="p-maj">{E(d['badge'])} · MAJ {maj(fam)}</span></div>
        <h1>{name} : <span class="flash">avis, tests et prix</span></h1>
        {byline(root)}
        <div class="ref">{E(d['ref'])}</div>
        {score_haut(d, ts, medias, last)}
      </div>
      <div class="p-sum">
        <p class="p-verdict"><b>Le verdict.</b> {E(d['verdict'])}</p>
        <p class="p-rank">{rank_txt}.</p>
      </div>
      <div class="p-facts">
        <div class="p-fact"><span class="p-fact-k">Lu chez</span><span class="p-fact-v">{E(", ".join(medias_l[:4]))}{" et " + str(len(medias_l) - 4) + " autre" + ("s" if len(medias_l) > 5 else "") if len(medias_l) > 4 else ""}</span><a href="#tests">Tous les tests →</a></div>
        <div class="p-fact yes"><span class="p-fact-k">Pour vous si</span><span class="p-fact-v">{low_first(E(d['pour']))}</span></div>
        <div class="p-fact no"><span class="p-fact-k">À éviter si</span><span class="p-fact-v">{low_first(E(d['eviter']))}</span></div>
      </div>
    </div>
    <div class="p-side">
      <div class="p-card">
        {f'<div class="f-photo"><img src="{root}assets/img/p/{d["img"]}" alt="{name}" width="560" height="420" fetchpriority="high"></div>' if d['img'] else ''}
        <div class="press-big">{press_big(d)}</div>
        <div class="p-buy" id="buyBox" data-z="haut" data-pid="{d['id']}">
          <div class="p-buy-h"><span class="p-buy-k">Prix indicatif</span><span class="p-buy-p"><b>{d['price_txt']}</b><small>{"le plus bas relevé" if len(d["offers"]) > 1 else "prix indicatif"} · {pdate(fam)}</small></span></div>
          <div class="p-btns">{buy_btns}</div>
          <a class="cta big buy p-mob" href="{E(best['url'])}" target="_blank" rel="{rel_m(best['m'])}">{cta_txt(best)}</a>
          <p class="p-buy-n p-mob">{f'Aussi chez {autres} · ' if autres else ''}<a href="#prix">toutes les offres</a></p>
          {'<p class="p-buy-n p-desk">Liens affiliés : sans surcoût pour vous et sans effet sur le classement. Seul le prix affiché par le marchand fait foi.</p>' if aff else ''}
        </div>
      </div>
    </div>
    {top1}
  </section>

  {radar_fiche(d, items, root, usage_url, usage_txt)}

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
    {synthese_html(d)}
    <div class="pc-grid p-pc">
      <div class="strengths"><span class="pc-t pro">Ce que la presse apprécie</span>{st}</div>
      <div class="strengths weak"><span class="pc-t con">Les réserves qui reviennent</span>{wk}</div>
    </div>
  </section>

  <section class="section p-sec" id="prix">
    <div class="section-head"><h2>Où l'acheter</h2><div class="tag">Environ {euro_ind(d['p'])} · {ind_txt(fam)}</div></div>
    <div class="p-buywrap">
    <div class="offers p-offers" data-z="offres" data-pid="{d['id']}">{offs}<p class="o-note">{RECO_NOTE if d["cat"] == "reconditionne" else "La configuration peut différer d'un marchand à l'autre : vérifiez la fiche avant d'acheter."} Les prix Electro Dépôt et PC-Portable.net sont ceux de leur flux produits officiel à la date indiquée ; seul le prix affiché par le marchand fait foi. Seuls les liens {AFF_TXT} sont affiliés à ce jour ; les autres sont de simples liens directs. Aucun n'influence les notes ni le classement.</p></div>
    <aside class="p-specs v12">{specs}</aside>
    </div>
  </section>

  <section class="section p-sec" id="tests">
    <div class="section-head"><h2>Tous les tests recensés</h2><div class="tag">Sources</div></div>
    <p class="p-cons">Chaque ligne renvoie vers le test d'origine. Les notes sont converties sur 10 ; « test » signale un article sans note chiffrée. <a href="{root}methode">Notre méthode</a>.</p>
    <ul class="notes-list p-notes">{notes}</ul>
    {src}
  </section>

  <section class="section p-sec" id="alternatives" data-zi="alternatives">
    <div class="section-head"><h2>Les alternatives pour le même usage</h2><a class="see-all" href="{usage_url}">Tout le top {n_items} →</a></div>
    <div class="alt-grid">{alt}</div>
  </section>

  <section class="section p-sec" id="faq" style="border-bottom:none;">
    <div class="section-head"><h2>Questions fréquentes</h2><div class="tag">FAQ</div></div>
    <div class="faq-list">{faq_html}</div>
    <p class="p-final" data-z="bas" data-pid="{d['id']}"><a class="cta big buy" href="{E(best['url'])}" target="_blank" rel="{rel_m(best['m'])}">{cta_txt(best)}</a> <a class="see-all" href="{usage_url}">Revenir au classement</a></p>
  </section>
"""
    # Titre affiché dans Google (v11, 20/10/2026) : la note, le nombre de tests et le prix indicatif, ce que cherche
    # l'internaute qui tape « <modèle> test » ou « <modèle> avis ». Le plus complet qui tient en 65 caractères.
    s, T, P = d["short"], ts["tests"], d["price_txt"]
    t_txt = f'{T} test{"s" if T > 1 else ""} presse'
    if pr:
        n_txt = f'{pr["n"]} note{"s" if pr["n"] > 1 else ""}'
        cands_t = [f'{s} : avis et tests, {fr(pr["avg"])}/10 sur {n_txt} presse, {P} | Top 10 Geek',
                   f'{s} : avis et tests, {fr(pr["avg"])}/10 sur {n_txt} presse, {P}',
                   f'{s} : avis et tests, {fr(pr["avg"])}/10 ({n_txt}), {P}',
                   f'{s} : avis et tests ({fr(pr["avg"])}/10 presse), {P}',
                   f'{s} : avis et tests, {fr(pr["avg"])}/10 presse']
    else:
        cands_t = [f'{s} : avis de {t_txt}, prix {P} | Top 10 Geek', f'{s} : avis de {t_txt}, prix {P}',
                   f'{s} : avis et tests presse, {P}']
    title = next((x for x in cands_t if len(x) <= 65), f'{s} : avis, tests et prix')
    bar_alt = next((o for o in d["offers"][1:]), None)
    bar = (f'<div class="buy-bar" id="buyBar" data-z="barre" data-pid="{d["id"]}" aria-hidden="true">'
           + (f'<img src="{root}assets/img/p/{d["img"]}" alt="{E(d["short"])}" width="56" height="42">' if d["img"] else "")
           + f'<span class="bb-t"><b>{name}</b>'
           + (f'<a href="{E(bar_alt["url"])}" target="_blank" rel="{rel_m(bar_alt["m"])}" tabindex="-1">ou chez {E(bar_alt["m"])}</a>' if bar_alt else f'<span>{P}</span>')
           + f'</span><a class="cta buy" href="{E(best["url"])}" target="_blank" rel="{rel_m(best["m"])}" tabindex="-1">'
           + (f'{euro2(best["price"])} · {E(best["m"])} →' if prix_exact(best) else f'Voir chez {E(best["m"])} →') + '</a></div>')
    lead = (f'{pr["n"]} note{"s" if pr["n"] > 1 else ""} presse, moyenne {fr(pr["avg"])}/10. ' if pr else f'{ts["tests"]} test{"s" if ts["tests"] > 1 else ""} presse résumé{"s" if ts["tests"] > 1 else ""}. ')
    # méta-description complète, jamais tronquée : verdict entier, sinon sa première proposition, sinon une phrase générique
    v = d["verdict"].strip()
    court = re.split(r"\s[:;—–]\s|, (?=mais|et |avec|sans|pour)", v)[0].rstrip(" .,") + "."
    nom = f'{d["short"]} : '
    cands = (nom + lead + v, lead + v, nom + lead + court + " Avis, réserves et prix indicatif.", lead + court + " Points forts, réserves et prix indicatif.",
             nom + lead + court, lead + court, f'{nom}{lead}Avis de la presse, points forts, réserves et prix indicatif.')
    desc = next((x for x in cands if 80 <= len(x) <= 158), next((x for x in cands if len(x) <= 158), f"{d['short']} : avis de la presse et prix indicatif."))
    ind = int(euro_ind(d["p"]).replace(" ", "").replace("€", ""))
    product = {"@type": "Product", "@id": f"{DOMAIN}/{d['purl']}#produit", "name": d["short"], "description": d["verdict"],
               "brand": {"@type": "Brand", "name": brand_of(d["short"])}, "category": plain(f"{fam['label']} · {c['label']}"),
               "url": f"{DOMAIN}/{d['purl']}",
               # Pas d'AggregateRating : Google réserve ce balisage aux notes collectées sur le site lui-même, pas aux notes de la presse.
               # Prix indicatif affiché sur la page (arrondi), sans offre ni prix par marchand.
               "offers": ({"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": f"{ind:.2f}", "offerCount": len(d["offers"])} if len(d["offers"]) > 1
                          else {"@type": "Offer", "priceCurrency": "EUR", "price": f"{ind:.2f}", "availability": "https://schema.org/InStock",
                                "url": f"{DOMAIN}/{d['purl']}"})}
    if d["img"]:
        product["image"] = f"{DOMAIN}/assets/img/p/{d['img']}"
    write(d["purl"] + "index.html", page(root, title, desc, d["purl"], body, fam["slug"], extra=bar,
                                         robots=None if indexable(d) else "noindex,follow",
                                         og_img=(f'assets/img/p/{d["img"]}' if d["img"] else "assets/img/og-image.jpg"),
                                         ld=[ld_crumbs(("Accueil", ""), (fam["plural"], f"{fam['slug']}/"), (c["label"], f"{fam['slug']}/{c['slug']}/"), (d["short"], d["purl"])),
                                             ld_page(d["purl"], title), PERSON, product, ld_faq(faq)]))


for fam in FAMILIES:
    for c in fam["cats"]:
        for i, d in enumerate(by_cat_view[c["key"]], 1):
            if d["cat"] == c["key"]:   # les produits d'un autre usage gardent leur fiche d'origine
                product_page(fam, c, i, d, by_cat_view[c["key"]])

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
    score = (f'<span class="ch-score"><b>{fr(pr["avg"])}</b><small>/10</small> <em>{pr["n"]} note{"s" if pr["n"] > 1 else ""} presse</em></span>' if pr
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


CHAMP_LAB = {"pc-portable": "PC portables", "ordinateur-de-bureau": "Ordinateurs de bureau", "ecran-pc": "Écrans PC", "imprimante": "Imprimantes",
             "aspirateur-robot": "Robots aspirateurs", "tv": "TV et barres de son", "audio": "Audio", "photo-video": "Photo et vidéo"}


def mini_champ(d):
    """Carte compacte d'accueil : le choix n° 1 d'un usage (le même que « Notre choix » sur la page de l'usage)."""
    c = CAT[d["cat"]]
    pr = d["press"]
    note = f'<i>{fr(pr["avg"])}<small>/10</small></i>' if pr else '<i>Testé</i>'
    img = f'<img src="assets/img/p/{d["img"]}" alt="{E(d["short"])}" width="64" height="48" loading="lazy">' if d["img"] else ""
    return (f'<a class="mc" href="{d["href"]}" style="--c:{c["color"]}"><span class="mc-u"><span class="dot" style="background:{c["color"]}"></span>{c["label"]}</span>{img}'
            f'<span class="mc-t"><b>{E(d["short"])}</b><span class="mc-m">{note}<em>{d["price_txt"]}</em></span></span></a>')


def champions_html():
    out = ""
    for k, nom, cls in (("info", "Informatique", "info"), ("maison", "Maison", "maison")):
        out += f'<div class="ch2-uni {cls}">{nom}</div>'
        for f in FAMILIES:
            if (f["slug"] in MAISON_SLUGS) != (k == "maison"):
                continue
            cards = "".join(mini_champ(by_cat[c["key"]][0]) for c in f["cats"] if c["key"] != "reconditionne")
            out += (f'<div class="ch2-row"><div class="ch2-head"><h3>{CHAMP_LAB[f["slug"]]}</h3><a class="see-all" href="{f["slug"]}/">Tout le comparatif →</a></div>'
                    f'<div class="ch2-grid">{cards}</div></div>')
    return out


CHAMPIONS_HTML = champions_html()

radar_items = [by_cat[c["key"]][i] for c in LCATS for i in (0, 1, 2)]
ICON = {
    "laptop": '<path d="M5 6h14v9H5z"/><path d="M2.5 18.5h19"/>',
    "desktop": '<rect x="3" y="4" width="13" height="10" rx="1"/><path d="M9.5 14v3M6.5 17h6"/><rect x="18" y="6" width="3.5" height="11" rx="0.8"/>',
    "ecran": '<rect x="2.5" y="4" width="19" height="12" rx="1"/><path d="M12 16v3.5M8 19.5h8"/>',
    "imprimante": '<path d="M7 9V3.5h10V9"/><rect x="3" y="9" width="18" height="7.5" rx="1.2"/><path d="M7 14h10v6.5H7z"/>',
    "robot": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="3"/><path d="M12 3.5v2.5"/>',
    "tv": '<rect x="2.5" y="5" width="19" height="12" rx="1.5"/><path d="M8 20h8"/>',
    "audio": '<rect x="7" y="3" width="10" height="18" rx="2.5"/><circle cx="12" cy="14.5" r="3"/><circle cx="12" cy="7.5" r="1"/>',
    "video": '<path d="M4 8h3l1.5-2h7L17 8h3v11H4z"/><circle cx="12" cy="13.5" r="3.2"/>',
}
def fam_btn(fam):
    n = sum(len(by_cat[c["key"]]) for c in fam["cats"])
    return (f'<a class="fam-btn" href="{fam["slug"]}/"><span class="fb-ic"><svg viewBox="0 0 24 24" aria-hidden="true">{ICON[fam["key"]]}</svg></span>'
            f'<span class="fb-txt"><b>{fam["plural"]}</b><small>{len(fam["cats"])} usage{"s" if len(fam["cats"]) > 1 else ""} · {n} modèles</small></span><span class="fb-go" aria-hidden="true">→</span></a>')
FAM_BTNS = ('<div class="fb-group"><span class="fb-label">Informatique</span><div class="fb-row">'
            + "\n        ".join(fam_btn(f) for f in FAMILIES if f["slug"] not in MAISON_SLUGS) + '</div></div>'
            '<div class="fb-group maison"><span class="fb-label">Maison</span><div class="fb-row">'
            + "\n        ".join(fam_btn(f) for f in FAMILIES if f["slug"] in MAISON_SLUGS)
            + '</div></div>')

# ---------------------------------------------------------------- Black Friday : réglages, baisses constatées, bandeau d'accueil
BF_ACTIF = False           # INTERRUPTEUR : False retire le bandeau et le lien de l'accueil (la page /black-friday/ reste en ligne)
BF_DATE = "vendredi 27 novembre 2026"
BF_DEBUT = "2026-11-23"    # début de la semaine d'opérations ; la référence est le plus bas prix des 30 jours précédents
BF_FIN = "2026-11-30"      # Cyber Monday
BF_SEUIL_BAISSE = 5.0      # baisse minimale affichée (en %)
BF_BAISSE_MAX = 50.0       # au-delà, la « baisse » est presque sûrement une erreur de relevé (autre produit, autre configuration) : non affichée
BF_MIN_JOURS = 3           # nombre minimal de relevés de la période de référence pour parler de baisse
BF_MAX = 20                # nombre maximal de produits dans le bloc « baisses constatées »


def _jfr(iso):
    return f"{iso[8:10]}/{iso[5:7]}/{iso[:4]}"


def bf_baisses():
    """Produits dont le prix a baissé d'au moins BF_SEUIL_BAISSE % chez un marchand affilié, par rapport au plus bas prix
    constaté chez CE MÊME marchand pendant les 30 jours précédant BF_DEBUT (historique_prix.json, alimenté par bf_historique.py).
    Garde-fous : note presse d'au moins 7/10 sur au moins 3 notes (2 pour la Maison), ni reconditionnés ni vendeurs tiers.
    Renvoie (liste triée par baisse décroissante, date du dernier relevé)."""
    import datetime
    chemin = SRC + "historique_prix.json"
    h = json.load(open(chemin, encoding="utf-8")) if os.path.exists(chemin) else {}
    jours = sorted(h)
    if not jours:
        return [], None
    dernier = jours[-1]
    if dernier < BF_DEBUT:        # avant l'opération : pas de baisse affichée (les relevés servent à fixer la référence)
        return [], dernier
    deb = (datetime.date.fromisoformat(BF_DEBUT) - datetime.timedelta(days=30)).isoformat()
    ref_jours = [j for j in jours if deb <= j < BF_DEBUT]
    res = []
    for pid, d in ITEMS.items():
        pr = d["press"]
        if d["cat"] == "reconditionne" or not pr or pr["avg"] is None or pr["avg"] < 7:
            continue
        if pr["n"] < (2 if d["fslug"] in MAISON_SLUGS else 3):
            continue
        best = None
        for m, cur in h[dernier].get(pid, {}).items():
            if m not in AFFILIATED:
                continue
            avant = [h[j][pid][m] for j in ref_jours if pid in h[j] and m in h[j][pid]]
            if len(avant) < BF_MIN_JOURS:
                continue
            ref = min(avant)
            pct = (ref - cur) / ref * 100
            if BF_SEUIL_BAISSE <= pct <= BF_BAISSE_MAX and (best is None or pct > best["pct"]):
                best = dict(d=d, m=m, cur=cur, ref=ref, pct=pct)
        if best:
            res.append(best)
    res.sort(key=lambda x: -x["pct"])
    return res[:BF_MAX], dernier


def bf_banner():
    if not BF_ACTIF:
        return ""
    return """
  <aside class="bf-banner" aria-label="Black Friday 2026">
    <div class="bf-banner-txt"><span class="bf-pill">Black Friday</span>
      <b>Du 23 au 30 novembre : les vraies baisses, vérifiées par la presse.</b>
      <span class="bf-sub">PC, TV, audio, robots, photo… Chaque baisse est comparée au prix le plus bas des 30 jours précédents.</span></div>
    <a class="bf-go" href="black-friday/">Voir les baisses →</a>
  </aside>
"""


def bf_home_link():
    if not BF_ACTIF:
        return ""
    return '<p class="bf-home"><a class="see-all" href="black-friday/">Black Friday 2026 : les produits les mieux notés et les vraies baisses de prix →</a></p>'


home = f"""
{bf_banner()}
  <section class="home-hero">
    <div class="hh-text">
      <div class="eyebrow">LE COMPARATEUR QUI A LU TOUS LES TESTS · MAJ {MAJ}</div>
      <h1>Tous les tests high&#8209;tech, <span class="flash">résumés pour vous.</span></h1>
      <p>Nous lisons les tests de la presse spécialisée, nous en tirons une <b>note presse sur 10</b> et nous vous disons, usage par usage, quoi acheter — et pourquoi. Sans jargon, sans pub déguisée.</p>
      <div class="spec-row">
        <div><strong>{TOTAL_TESTS}</strong>tests presse recensés</div>
        <div><strong>{len(ITEMS)}</strong>produits sélectionnés</div>
        <div><strong>{len(CAT)}</strong>usages couverts</div>
      </div>
    </div>
    <div class="hh-visual">
      <div class="hh-blob"></div>
      <img class="hh-mascot trio" src="assets/img/hero-trio.webp" srcset="assets/img/hero-trio-600.webp 440w, assets/img/hero-trio.webp 660w" sizes="(max-width: 700px) 80vw, 440px" alt="Le jeune geek, son père et sa grand-mère, entourés de produits high-tech" width="660" height="900" fetchpriority="high">
      <img class="hh-sticker s1" src="assets/img/sticker-laptop.webp" alt="" width="120" height="120">
      <img class="hh-sticker s2" src="assets/img/sticker-tv.webp" alt="" width="120" height="120">
      <img class="hh-sticker s3" src="assets/img/sticker-robot.webp" alt="" width="120" height="120">
      <div class="hh-bubble">« J'ai lu {TOTAL_TESTS} tests pour vous. De rien. »</div>
    </div>
    <nav class="fam-btns row4 grouped" aria-label="Nos comparatifs">
        {FAM_BTNS}
    </nav>
  </section>

  {ticker()}

  <section class="section">
    <div class="section-head"><h2>Les champions du moment</h2><div class="tag">Un champion par usage, noté par la presse</div></div>
    {CHAMPIONS_HTML}
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

  <section class="section">
    <div class="section-head"><h2>Par où commencer ?</h2><div class="tag">{["", "Une", "Deux", "Trois", "Quatre", "Cinq", "Six", "Sept", "Huit"][len(FAMILIES)]} familles, {len(CAT)} usages</div></div>
    {bf_home_link()}
    <h3 class="univers-head">Informatique</h3>
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
    <h3 class="univers-head maison">Maison</h3>
    <div class="fam-grid maison">
      <a class="fam-card maison" href="aspirateur-robot/">
        <div class="fam-art"><img src="assets/img/badge-robots-laveurs-v2.webp" alt="" width="96" height="96"><img src="assets/img/badge-robots-balais-laveurs-v2.webp" alt="" width="96" height="96"><img src="assets/img/badge-robots-animaux-v2.webp" alt="" width="96" height="96"></div>
        <h3>Robots aspirateurs</h3><p>{sum(1 for d in ITEMS.values() if d['family'] == 'robot')} robots et aspirateurs classés par usage : laveurs, aspirateurs balais, balais laveurs, robots pour animaux et petits prix.</p>
        <div class="fam-chips">{''.join(f'<span>{c["label"]}</span>' for c in SCATS)}</div><span class="uc-go">Explorer →</span></a>
      <a class="fam-card maison" href="tv/">
        <div class="fam-art"><img src="assets/img/sticker-tv.webp" alt="" width="96" height="96" loading="lazy" decoding="async"><img src="assets/img/sticker-soundbar.webp" alt="" width="96" height="96" loading="lazy" decoding="async"></div>
        <h3>TV et home cinéma</h3><p>{sum(1 for d in ITEMS.values() if d['family'] == 'tv')} téléviseurs et barres de son classés par taille et par budget, d'après les tests de la presse.</p>
        <div class="fam-chips">{''.join(f'<span>{c["label"]}</span>' for c in TCATS)}</div><span class="uc-go">Explorer →</span></a>
      <a class="fam-card maison" href="audio/">
        <div class="fam-art"><img src="assets/img/sticker-speaker.webp" alt="" width="96" height="96" loading="lazy" decoding="async"><img src="assets/img/sticker-headphones.webp" alt="" width="96" height="96" loading="lazy" decoding="async"></div>
        <h3>Son, audio et hi-fi</h3><p>{sum(1 for d in ITEMS.values() if d['family'] == 'audio')} enceintes, écouteurs et casques classés par usage : Bluetooth, réduction de bruit, open-ear et gaming.</p>
        <div class="fam-chips">{''.join(f'<span>{c["label"]}</span>' for c in ACATS)}</div><span class="uc-go">Explorer →</span></a>
      {carte_video()}
    </div>
  </section>

"""
write("index.html", page("", "Top 10 Geek : tests high-tech résumés — PC, TV, audio, robots",
                         "Nous lisons les tests de la presse et vous donnons une note sur 10 et un verdict par usage : PC, écrans, imprimantes, TV, audio, photo, robots aspirateurs.",
                         "", home, "home", body_cls="home",
                         ld=[ORG, {"@type": "WebSite", "@id": DOMAIN + "/#site", "url": DOMAIN + "/", "name": "Top 10 Geek", "description": BASELINE,
                                   "inLanguage": "fr-FR", "publisher": {"@id": ORG["@id"]}}]))

# ---------------------------------------------------------------- Méthode
methode = f"""
  <div class="prose">
    <div class="prose-hero">
      <div><div class="eyebrow">MÉTHODE · MAJ {MAJ}</div><h1>Une note principale : celle de la presse</h1>
      <p>Nous ne testons pas les produits nous-mêmes : nous n'avons pas de laboratoire, et nous préférons le dire. Notre travail, c'est de lire tout ce qui a été publié, de trier le solide du marketing, et de vous le rendre lisible.</p>
      {byline("")}</div>
      <img src="assets/img/pose-investigation.webp" alt="La mascotte, loupe à la main" width="200" height="200">
    </div>
    <div class="method-grid">
      <div class="method-card"><span class="mono-big">1 · Sélection</span><h3>Deux conditions pour entrer</h3><p>Un produit n'entre dans un top 10 que s'il est <b>réellement en vente</b> chez au moins un des marchands que nous suivons et s'il a fait l'objet d'<b>au moins un test</b> dans la presse.</p></div>
      <div class="method-card"><span class="mono-big">2 · Presse</span><h3>La note principale</h3><p>Moyenne simple des notes publiées par les médias spécialisés, convertie sur 10, avec le nombre de notes. Chaque note renvoie vers le test d'origine. « Gamme » signale des notes obtenues sur une configuration ou une génération proche.</p></div>
      <div class="method-card"><span class="mono-big">3 · Prix</span><h3>Un prix indicatif</h3><p>Pour chaque produit, nous affichons un prix indicatif, avec le mois où nous l'avons constaté, et les liens vers les marchands où nous l'avons trouvée en vente.</p></div>
    </div>
    <h2 id="classement">Le classement : nos critères</h2>
    <p>En tête, <b>« le choix de la bande »</b> : notre recommandation pour l'usage, le meilleur compromis entre notes presse et prix. Nous la choisissons de préférence dans la <b>zone « bonnes affaires »</b> du radar (note presse d'au moins 8/10 et prix inférieur ou égal à la médiane de l'usage). Elle n'est placée en tête que si sa note repose sur <b>au moins {SEUIL_NOTES} notes presse</b> ; sinon elle est classée comme les autres et signalée « prometteur, peu testé ».</p>
    <p>Les autres produits sont classés en trois groupes : d'abord ceux notés par <b>au moins {SEUIL_NOTES} médias</b>, puis ceux qui n'ont qu'<b>1 ou 2 notes</b>, enfin ceux testés <b>sans note chiffrée</b> (nous donnons alors le lien vers le test plutôt que d'inventer une note). Dans chaque groupe, l'ordre suit la <b>note presse ajustée</b> : une moyenne bayésienne qui rapproche une note appuyée sur peu de tests de la moyenne de l'usage, comme si {PRIOR_M} notes moyennes s'y ajoutaient. Un 10/10 isolé ne peut donc pas devancer un 9/10 confirmé par dix médias. À égalité, le produit le plus noté puis le moins cher passe devant.</p>
    <p>La note affichée sur chaque produit reste la <b>moyenne simple</b> des médias, avec le nombre de notes ; la note ajustée ne sert qu'à l'ordre du classement. Aucun critère commercial (commission, marchand) n'intervient dans le classement.</p>
    <h2>Comment est calculée la note presse</h2>
    <p>Toutes les notes sont ramenées sur 10 : 4/5 devient 8/10, 87 % devient 8,7/10. Nous faisons une moyenne simple, sans pondérer les médias. Le nombre de notes est toujours affiché : une moyenne appuyée sur quinze tests est plus solide qu'une note unique. Les tests sans note chiffrée sont listés mais n'entrent pas dans la moyenne. Au {MAJ}, le site recense <b>{TOTAL_TESTS} tests</b> et <b>{TOTAL_NOTES} notes</b> pour {len(ITEMS)} produits.</p>
    <h2>Les imprimantes et les associations de consommateurs</h2>
    <p>Les imprimantes sont peu testées par la presse high-tech, mais très bien par les <b>associations de consommateurs</b> (Test-Achats, Que Choisir, Which?, Tænk), qui les mesurent en laboratoire. Ces associations réservent leurs notes à leurs abonnés : nous citons et lions leurs tests, sans note chiffrée, et la note presse n'est calculée que sur les notes publiées librement. C'est pourquoi beaucoup d'imprimantes affichent « testé, sans note ».</p>
    <h2>Comment lire le graphe à bulles</h2>
    <p>Chaque bulle est un produit. <b>Horizontalement</b> : la note presse. <b>Verticalement</b> : le prix indicatif. <b>Taille</b> : le nombre de notes (une grosse bulle = une note solide). <b>En pointillés</b>, à gauche : les produits testés mais sans note chiffrée. Les bonnes affaires se trouvent dans la <b>zone jaune, en bas à droite</b>.</p>
    <h2>Prix, photos et configurations</h2>
    <p>Le prix indicatif est le plus bas que nous avons constaté chez Amazon, Darty, sur l'Acer Store, chez Geekom ou chez Electro Dépôt (pour les écrans et les imprimantes : sur Amazon ou chez Electro Dépôt, en précisant quand le produit n'est proposé que par un vendeur tiers sur Amazon), arrondi à la dizaine d'euros ; le mois du constat est indiqué à côté. Nous le revoyons environ une fois par mois. Il situe la machine mais ne remplace pas une comparaison : <b>seul le prix affiché par le marchand fait foi</b>. Nous ne comparons pas, pour l'instant, les prix marchand par marchand : nous indiquons seulement où la machine est en vente. Exception : Electro Dépôt, dont nous affichons le prix exact, lu dans son flux produits officiel et mis à jour chaque semaine (la date du relevé est indiquée à côté). Un même modèle existe souvent en plusieurs configurations (mémoire, stockage, carte graphique) : celle de chaque offre est indiquée à côté du lien, et peut différer d'un marchand à l'autre. Les photos sont celles fournies par les marchands et les constructeurs.</p>
    <h2>Avis clients, poids et autonomie</h2>
    <p>La note « avis clients Darty » est celle affichée par Darty lors de notre dernier relevé ; nous ne l'affichons qu'à partir de trois avis. Poids et autonomie sont ceux annoncés par le constructeur, sauf mention « test ». « n.c. » : non communiqué.</p>
    <h2>Notre indépendance</h2>
    <p>Aucune marque ne paie pour figurer dans nos sélections. Certains liens sont des liens d'affiliation (à ce jour : {AFF_TXT}) : ils peuvent nous rapporter une commission, sans surcoût pour vous, et n'influencent ni les notes ni les classements.</p>
    <h2>Contact</h2>
    <p>Une remarque, une erreur repérée ? Écrivez-nous : <a href="mailto:contact@top10geek.fr">contact@top10geek.fr</a></p>
  </div>
"""
write("methode.html", page("", "Notre méthode : sélection, note presse, prix | Top 10 Geek",
                           "Comment Top 10 Geek sélectionne les produits, calcule la note presse, établit le classement et indique les prix.",
                           "methode", methode, "methode", ld=[ld_crumbs(("Accueil", ""), ("Méthode", "methode")), ld_page("methode", "Notre méthode"), PERSON]))

# ---------------------------------------------------------------- À propos
apropos = f"""
  <div class="prose">
    <div class="prose-hero">
      <div><div class="eyebrow">À PROPOS · MAJ {MAJ}</div><h1>Qui est derrière Top 10 Geek ?</h1>
      <p>Top 10 Geek est un site indépendant édité par <b>Matthieu Tixier</b>, à La Rochelle. Pas de rédaction parisienne ni de groupe de médias : un geek de toujours, qui en avait assez de lire dix tests avant chaque achat.</p></div>
      <img src="assets/img/pose-investigation.webp" alt="La mascotte de Top 10 Geek, loupe à la main" width="200" height="200">
    </div>
    <h2>L'éditeur</h2>
    <p><b>Matthieu Tixier</b> a commencé sa carrière comme consultant en informatique pendant sept ans, avant vingt ans de management. Passionné de high-tech depuis toujours, il a créé Top 10 Geek en 2026 pour répondre à une question simple : <i>que pense vraiment la presse de ce produit, toutes sources confondues ?</i></p>
    <p>Il choisit les produits suivis, valide les sélections et répond aux messages des lecteurs.</p>
    <h2>Ce que nous faisons, et ce que nous ne faisons pas</h2>
    <p>Nous <b>ne testons pas</b> les produits nous-mêmes. Nous recensons les tests publiés par la presse spécialisée et les associations de consommateurs, nous en tirons une note presse sur 10 et nous lions chaque test d'origine. La collecte des notes et des prix et la mise en forme des pages sont en partie automatisées (scripts et outils d'intelligence artificielle) ; les notes sont reprises telles que les médias les publient, et vérifiées régulièrement. Nos critères de classement sont détaillés dans <a href="methode#classement">notre méthode</a>.</p>
    <h2>Comment le site est financé</h2>
    <p>Par l'affiliation : certains liens vers les marchands (à ce jour : {AFF_TXT}) peuvent nous rapporter une commission, sans surcoût pour vous. Aucune marque ne paie pour figurer dans nos sélections, et les commissions n'interviennent pas dans le classement.</p>
    <h2>Contact</h2>
    <p>Une erreur, une note qui vous semble fausse, un produit à ajouter ? Écrivez à <a href="mailto:contact@top10geek.fr">contact@top10geek.fr</a> : chaque message est lu.</p>
    <p>Mentions légales : <a href="mentions-legales">éditeur, hébergeur et immatriculation</a>.</p>
  </div>
"""
write("a-propos.html", page("", "À propos : qui édite Top 10 Geek ? | Top 10 Geek",
                            "Top 10 Geek est un site indépendant édité par Matthieu Tixier à La Rochelle : synthèse des tests de la presse high-tech, méthode et financement.",
                            "a-propos", apropos, "", ld=[ld_crumbs(("Accueil", ""), ("À propos", "a-propos")),
                                                         {"@type": "AboutPage", "@id": DOMAIN + "/a-propos", "url": DOMAIN + "/a-propos", "name": "À propos de Top 10 Geek",
                                                          "inLanguage": "fr-FR", "mainEntity": {"@id": PERSON_ID}, "publisher": {"@id": ORG["@id"]}},
                                                         dict(PERSON, description="Éditeur de Top 10 Geek, ancien consultant en informatique, vingt ans de management."), ORG]))

# ---------------------------------------------------------------- Page Black Friday (toutes les rubriques)
BF_TIPS = [
    ("Partez du prix le plus bas", "Une promo n'est une affaire que si elle passe nettement sous le prix habituel. Pour chaque produit, nous gardons le plus bas prix constaté chez le même marchand pendant les 30 jours avant l'opération : c'est notre point de comparaison."),
    ("Vérifiez la référence exacte", "Un même nom de modèle cache souvent plusieurs versions : mémoire et stockage pour un ordinateur, taille ou génération pour une TV ou des écouteurs. Comparez la référence avant de comparer deux prix."),
    ("Regardez la note presse", "Un gros rabais sur un produit mal noté reste un mauvais achat. Mieux vaut une petite remise sur un produit que la presse recommande."),
    ("Méfiez-vous du prix barré", "Le prix barré est parfois un ancien prix conseillé que plus personne ne pratiquait. Seul l'écart avec le prix réellement constaté les semaines précédentes compte."),
]


def bf_card(d, root, label):
    pr = d["press"]
    note = (f'{fr(pr["avg"])}/10 presse · {pr["n"]} note{"s" if pr["n"] > 1 else ""}{" (prudence)" if pr["n"] < 3 else ""}' if pr
            else f'{d["tests"]["tests"]} test{"s" if d["tests"]["tests"] > 1 else ""} presse, sans note chiffrée')
    img = f'<img src="{root}assets/img/p/{d["img"]}" alt="{E(d["short"])}" width="96" height="72" loading="lazy">' if d["img"] else ""
    return f"""<a class="alt-card" href="{root}{d['purl']}">
      <span class="alt-k">{label}</span>
      {img}
      <b>{E(d['short'])}</b><span class="alt-why">{note}</span><span class="alt-meta">Prix repère : {d['price_txt']}</span></a>"""


def bf_deal(x, root, maj):
    """Carte d'un produit en baisse : écart, ancien plus bas prix, prix du jour, bouton vers le marchand (clic mesuré, zone « bf »)."""
    d, m = x["d"], x["m"]
    pr = d["press"]
    if m in PRIX_EXACTS:
        cur, ref, pct = euro2(x["cur"]), euro2(x["ref"]), f'−{int(round(x["pct"]))} %'
        qual = ""
    else:
        cur, ref, pct = "env. " + euro_ind(x["cur"]), "env. " + euro_ind(x["ref"]), f'env. −{int(round(x["pct"]))} %'
        qual = " (prix indicatif)"
    offre = next((o for o in d["offers"] if o["m"] == m and "tiers" not in (o.get("cfg") or "")), None)
    if not offre:
        return ""
    c = CAT[d["cat"]]
    img = f'<img src="{root}assets/img/p/{d["img"]}" alt="{E(d["short"])}" width="96" height="72" loading="lazy">' if d["img"] else ""
    return f"""<article class="bf-deal" data-pid="{d['id']}">
      <a class="alt-card bf-deal-main" href="{root}{d['purl']}" data-zi="bf-fiche">
        <span class="alt-k">{E(FAM[d['family']]['plural'])} · {E(c['label'])}</span>
        {img}
        <b>{E(d['short'])}</b><span class="alt-why">{fr(pr['avg'])}/10 presse · {pr['n']} note{'s' if pr['n'] > 1 else ''}</span>
        <span class="bf-prices"><span class="bf-pct">{pct}</span> <s>{ref}</s> <strong>{cur}</strong></span>
        <span class="alt-meta">chez {E(m)}{qual} · relevé du {maj}</span></a>
      <a class="cta bf-buy" data-z="bf" href="{E(offre['url'])}" target="_blank" rel="{rel_m(m)}">Voir l'offre chez {E(m)} →</a>
    </article>"""


def bf_baisses_section(root):
    liste, dernier = bf_baisses()
    if liste:
        maj = _jfr(dernier)
        cards = "".join(bf_deal(x, root, maj) for x in liste)
        corps = f"""<p class="bf-note">Relevé du {maj}. L'écart est mesuré chez le même marchand, par rapport au <b>prix le plus bas constaté pendant les 30 jours précédant le {_jfr(BF_DEBUT)}</b>. Seuls figurent les produits en baisse d'au moins {int(BF_SEUIL_BAISSE)} %, notés au moins 7/10 par la presse. Seul le prix affiché par le marchand fait foi.</p>
    <div class="alt-grid bf-two bf-deals">{cards}</div>"""
    elif dernier is None or dernier < BF_DEBUT:
        corps = f"""<p class="bf-note">L'opération démarre le lundi {_jfr(BF_DEBUT)}. Nous relevons déjà les prix pour fixer la référence : dès cette date, les produits dont le prix passe nettement sous leur plus bas des 30 jours précédents apparaîtront ici, avec l'écart constaté. En attendant, voici les produits que la presse recommande.</p>"""
    else:
        corps = f"""<p class="bf-note">Aucune baisse notable relevée à ce jour (seuil : {int(BF_SEUIL_BAISSE)} % sous le plus bas des 30 jours précédents, produit noté au moins 7/10). Les prix sont relevés chaque jour : revenez demain.</p>"""
    return f"""
  <section class="section" id="baisses">
    <div class="section-head"><h2>Baisses constatées</h2><div class="tag">Relevées chaque jour, du {_jfr(BF_DEBUT)} au {_jfr(BF_FIN)}</div></div>
    {corps}
  </section>"""


BF_PIEGES = [
    ("PC portables", "Le même nom cache plusieurs configurations : comparez processeur, mémoire et stockage avant le prix. Méfiez-vous des modèles de l'an dernier présentés comme des nouveautés."),
    ("Ordinateurs de bureau", "Une grosse carte graphique attire l'œil, mais une alimentation ou un stockage au rabais font souvent la différence de prix. Vérifiez aussi ce qui est fourni : écran, clavier, souris."),
    ("Écrans PC", "Regardez la dalle (IPS, VA, OLED), la définition et la fréquence, pas seulement la taille. Une révision plus ancienne d'un même modèle peut être vendue sous un nom proche."),
    ("Imprimantes", "Le prix d'achat compte moins que celui de l'encre. Une imprimante bradée avec des cartouches chères coûte vite plus cher qu'une imprimante à réservoirs."),
    ("Robots et aspirateurs", "Regardez le coût d'entretien : filtres, brosses, lingettes et sacs reviennent à la caisse. Vérifiez aussi la référence exacte, car plusieurs versions portent des noms très proches."),
    ("Téléviseurs", "Comparez le type de dalle, la luminosité et la fréquence, pas seulement la taille. Une même série existe en plusieurs diagonales dont les performances diffèrent : vérifiez la référence de la taille visée."),
    ("Audio", "Un même nom de gamme couvre plusieurs générations : vérifiez le numéro de version. La réduction de bruit, l'autonomie et le confort comptent davantage qu'une remise de quelques euros."),
    ("Photo et vidéo", "Vérifiez ce qui est inclus (objectif, carte mémoire, batterie, abonnement pour stocker les vidéos d'une caméra de surveillance). Un boîtier nu et un kit n'ont pas le même prix."),
]

# titre, nombre de produits par usage et pastille de chaque section, dans l'ordre d'affichage
BF_SECTIONS = [
    ("laptop", "Les PC portables à surveiller", 1, "Notre choix par usage"),
    ("desktop", "Les ordinateurs de bureau à surveiller", 1, "Notre choix par usage"),
    ("ecran", "Les écrans PC à surveiller", 1, "Notre choix par usage"),
    ("imprimante", "Les imprimantes à surveiller", 1, "Notre choix par usage"),
    ("robot", "Les robots et aspirateurs à surveiller", 1, "Notre choix par usage"),
    ("tv", "Les téléviseurs et barres de son à surveiller", 1, "Notre choix par usage"),
    ("audio", "Les enceintes, écouteurs et casques à surveiller", 1, "Notre choix par usage"),
    ("video", "Les caméras, vidéoprojecteurs et appareils photo à surveiller", 1, "Notre choix par usage"),
]


def bf_family(fam, root, n_top, title, tag):
    """Un « Notre choix » par usage, en grille ; les autres du top 10 sont à un clic (lien de l'usage)."""
    cards, liens = [], []
    for c in fam["cats"]:
        top = by_cat[c["key"]][:1]
        if not top:
            continue
        cards.append(bf_card(top[0], root, E(c["label"])))
        liens.append(f'<a href="{root}{fam["slug"]}/{c["slug"]}/">{E(c["label"])}</a>')
    return f"""
  <section class="section" id="bf-{fam['slug']}">
    <div class="section-head"><h2>{title}</h2><div class="tag">{tag}</div></div>
    <p class="bf-note">Prix repères ({ind_txt(fam)}), pas des promotions.</p>
    <div class="alt-grid">{''.join(cards)}</div>
    <p class="bf-more">Tous les tops 10 : {' · '.join(liens)}</p>
  </section>"""


def black_friday_page():
    root = "../"
    tips = "".join(f'<div class="g-card"><span class="g-num">0{i}</span><h3>{t}</h3><p>{x}</p></div>' for i, (t, x) in enumerate(BF_TIPS, 1))
    pieges = "".join(f'<div class="g-card"><span class="g-num">{t[:2].upper()}</span><h3>{t}</h3><p>{x}</p></div>' for t, x in BF_PIEGES)
    sections = [(FAM[k], t, n, tg) for k, t, n, tg in BF_SECTIONS if k in FAM]
    nav = '<a class="bf-chip bf-chip-hot" href="#baisses">Baisses constatées</a>' + "".join(f'<a class="bf-chip" href="#bf-{f["slug"]}">{f["plural"]}</a>' for f, *_ in sections)
    faq = [
        ("Quand a lieu le Black Friday 2026 ?", f"Le Black Friday tombe le {BF_DATE}. Il est suivi du Cyber Monday, le lundi 30 novembre 2026. Beaucoup de marchands lancent leurs offres plusieurs jours avant et les prolongent après : nous relevons les prix du {_jfr(BF_DEBUT)} au {_jfr(BF_FIN)}."),
        ("Comment calculez-vous les baisses de prix ?", f"Nous relevons les prix chaque jour chez les marchands que nous suivons. Pour chaque produit, nous comparons le prix du jour au plus bas prix constaté chez le même marchand pendant les 30 jours précédant le {_jfr(BF_DEBUT)}. Une baisse n'est affichée que si elle atteint {int(BF_SEUIL_BAISSE)} % et que le produit est noté au moins 7/10 par la presse. Les vendeurs tiers d'Amazon et les reconditionnés sont exclus."),
        ("Les prix des sections « à surveiller » sont-ils des promotions ?", "Non. Ce sont des prix repères : le prix indicatif de chaque produit avant le Black Friday, arrondi à la dizaine d'euros (mois du relevé indiqué dans chaque rubrique). Ils servent à juger si une offre est réellement intéressante. Seul le prix affiché par le marchand fait foi."),
        ("Comment savoir si une promo Black Friday est une vraie affaire ?", "Comparez le prix de l'offre au prix repère du produit, vérifiez que la référence et la configuration sont bien les mêmes, puis regardez la note presse. Une remise sur un produit mal noté n'est pas une bonne affaire."),
        ("Quels produits surveiller pendant le Black Friday ?", "Ceux que la presse recommande déjà au prix normal. Nous listons pour chaque usage les premiers de notre classement : PC, écrans, imprimantes, TV, audio, robots aspirateurs, photo et vidéo."),
        ("Faut-il acheter un écran PC pendant le Black Friday ?", "C'est souvent le bon moment pour les écrans gaming et les écrans 4K, très présents dans les promotions. Partez de l'usage (bureautique, jeu, création) et vérifiez la dalle et la définition : un gros écran mal adapté reste un mauvais achat."),
        ("Une imprimante en promo est-elle une bonne affaire ?", "Seulement si l'encre suit. Regardez le prix des cartouches ou des bouteilles et le nombre de pages qu'elles impriment. Pour imprimer régulièrement, une imprimante à réservoirs, même moins remisée, revient presque toujours moins cher."),
        ("Top 10 Geek teste-t-il les produits ?", "Non. Nous lisons les tests publiés par la presse spécialisée et les associations de consommateurs, et nous en tirons une note presse sur 10, avec le nombre de tests et les liens vers les sources."),
    ]
    faq_html = "".join(f'<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    fam_html = "".join(bf_family(f, root, n, t, tg) for f, t, n, tg in sections)
    body = f"""
  <div class="crumb"><a href="../">Accueil</a> › Black Friday 2026</div>
  <section class="usage-hero">
    <div>
      <div class="eyebrow">BLACK FRIDAY · {BF_DATE.upper()}</div>
      <h1>Black Friday 2026 : la high-tech qui <span class="flash">vaut vraiment le coup</span></h1>
      <p>Pendant le Black Friday, tout est « en promo ». Pour trier, nous partons de ce que dit la presse : voici les produits les mieux notés de nos comparatifs et, du {_jfr(BF_DEBUT)[:5]} au {_jfr(BF_FIN)[:5]}, ceux dont le prix baisse <b>vraiment</b>, par rapport à leur plus bas des 30 jours précédents.</p>
      <p class="bf-chips">{nav}</p>
      <p class="hero-links"><a href="#reconnaitre">Reconnaître une vraie promo</a> · <a href="#pieges">Les pièges par catégorie</a></p>
    </div>
    <img class="hero-badge tall" src="../assets/img/pose-lowcost.webp" alt="La mascotte avec un PC en promo" width="170" height="260">
  </section>
{bf_baisses_section(root)}
  <section class="guide" id="reconnaitre">
    <div class="section-head"><h2>Reconnaître une vraie promo</h2><div class="tag">4 réflexes</div></div>
    <div class="g-grid">{tips}</div>
  </section>
{fam_html}

  <section class="guide" id="pieges">
    <div class="section-head"><h2>Les pièges, catégorie par catégorie</h2><div class="tag">À vérifier avant de payer</div></div>
    <div class="g-grid">{pieges}</div>
  </section>

  <section class="section" style="border-bottom:none;">
    <div class="section-head"><h2>Questions fréquentes</h2><div class="tag">Black Friday</div></div>
    <div class="faq-list">{faq_html}</div>
  </section>
"""
    write("black-friday/index.html", page(root, "Black Friday 2026 : les vraies baisses high-tech | Top 10 Geek",
          "Black Friday 2026 : les baisses de prix vérifiées sur PC, TV, audio, robots et photo, et les produits les mieux notés par la presse pour chaque usage.",
          "black-friday/", body, "black-friday",
          ld=[ld_crumbs(("Accueil", ""), ("Black Friday 2026", "black-friday/")), ld_faq(faq)]))


black_friday_page()


# ---------------------------------------------------------------- Fichiers statiques
write("assets/style.css", CSS_INLINE)   # pour 404.html et les pages légales, écrites à la main
for _f in ("404.html", "mentions-legales.html", "politique-confidentialite.html"):   # leur lien vers style.css suit la version
    _p = os.path.join(OUT, _f)
    _t = open(_p, encoding="utf-8").read()
    _t = re.sub(r"style\.css\?v=[0-9a-f]+", f"style.css?v={VER}", _t)
    _t = re.sub(r"main\.js\?v=[0-9a-f]+", f"main.js?v={VER}", _t)
    _r = "/" if _f == "404.html" else ""      # la 404 est servie sous n'importe quelle URL : liens absolus
    _t = re.sub(r'  (?:<div class="topbar">.*?\n  </div>|<header class="hd hd-b">.*?</header>)\n', lambda m: "  " + nav_html(_r, "") + "\n", _t, count=1, flags=re.S)
    _t = re.sub(r'<div class="foot-links">.*?</div>\n    </div>', lambda m: foot_tail(_r), _t, count=1, flags=re.S)
    open(_p, "w", encoding="utf-8").write(_t)
shutil.copy(SRC + "main15.js", os.path.join(OUT, "assets/main.js"))
os.makedirs(os.path.join(OUT, "assets/img/p"), exist_ok=True)
for d in ITEMS.values():  # photos : copiées par build_data.py (img_p/) si présentes, sinon déjà dans assets/img/p
    if d["img"] and os.path.exists(SRC + "img_p/" + d["img"]):
        shutil.copy(SRC + "img_p/" + d["img"], os.path.join(OUT, "assets/img/p", d["img"]))
urls = [""] + [f"{f['slug']}/" for f in FAMILIES] + [f"{f['slug']}/{c['slug']}/" for f in FAMILIES for c in f["cats"]] + [d["purl"] for k in CAT for d in by_cat[k] if indexable(d)] + ["black-friday/", "methode", "a-propos", "mentions-legales", "politique-confidentialite"]


def lastmods(urls):
    """Date de dernière modification réelle de chaque page (balise <lastmod> du sitemap).
    On garde dans _source/sitemap_dates.json une empreinte du contenu de chaque page ; si l'empreinte change
    (prix, note, texte…), la date devient celle du jour. L'empreinte ignore le paramètre anti-cache ?v=."""
    import datetime
    from zoneinfo import ZoneInfo
    jour = datetime.datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d")
    chemin = SRC + "sitemap_dates.json"
    dates = json.load(open(chemin, encoding="utf-8")) if os.path.exists(chemin) else {}
    res = {}
    for u in urls:
        f = "index.html" if u == "" else (u + "index.html" if u.endswith("/") else u + ".html")
        brut = open(os.path.join(OUT, f), encoding="utf-8").read()
        h = hashlib.md5(re.sub(r"\?v=[0-9a-f]+|<style>.*?</style>", "", brut, flags=re.S).encode("utf-8")).hexdigest()[:12]
        ancien = dates.get(u)
        res[u] = ancien if ancien and ancien["h"] == h else {"h": h, "d": jour}
    json.dump(res, open(chemin, "w", encoding="utf-8"), ensure_ascii=False, indent=0, sort_keys=True)
    return {u: v["d"] for u, v in res.items()}


LASTMOD = lastmods(urls)
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
      "".join(f"  <url><loc>{DOMAIN}/{u}</loc><lastmod>{LASTMOD[u]}</lastmod></url>\n" for u in urls) + "</urlset>\n")
print("OK", len(ITEMS), "produits ;", TOTAL_NOTES, "notes ;", TOTAL_TESTS, "tests")
