# -*- coding: utf-8 -*-
"""Bloc « Face à ses rivaux directs » des fiches du noyau (décision de Matthieu du 13/11/2026).

Données : _source/rivaux_specs.json = caractéristiques ANNONCÉES PAR LES FABRICANTS, relevées sur leur site
(une adresse source par produit, date de relevé), jamais estimées. Une caractéristique introuvable n'est pas écrite :
la ligne affiche « — » pour ce produit, et disparaît si aucun des produits comparés ne l'a.
Format : {"<id produit>": {"source": "<url>", "releve": "AAAA-MM-JJ", "v": {"<critère>": valeur}}}

Rivaux d'une fiche : jusqu'à 3 autres fiches du noyau du même usage, les plus proches en prix ; s'il y en a moins
de 2, on complète avec les produits du même usage les plus proches en prix (leurs caractéristiques sont aussi relevées).
"""
import html
import json
import os

E = html.escape
SRC = os.path.dirname(os.path.abspath(__file__)) + "/"

# critère -> (libellé, meilleur : "max" | "min" | None, format)
CRITERES = {
    "laptop": [
        ("processeur", "Processeur", None, "t"), ("gpu", "Carte graphique", None, "t"),
        ("ram_go", "Mémoire vive", "max", "Go"), ("stockage_go", "Stockage", "max", "Go"),
        ("ecran", "Écran", None, "t"), ("poids_kg", "Poids", "min", "kg"), ("batterie_wh", "Batterie", "max", "Wh"),
    ],
    "desktop": [
        ("processeur", "Processeur", None, "t"), ("gpu", "Carte graphique", None, "t"),
        ("ram_go", "Mémoire vive", "max", "Go"), ("stockage_go", "Stockage", "max", "Go"),
        ("ecran", "Écran intégré", None, "t"), ("format", "Format", None, "t"),
    ],
    "ecran": [
        ("taille", "Diagonale (classe)", None, "pouces"), ("definition", "Définition", None, "t"), ("dalle", "Dalle", None, "t"),
        ("frequence_hz", "Fréquence", "max", "Hz"), ("luminosite_cd", "Luminosité annoncée", "max", "cd/m²"),
        ("usbc_w", "Charge USB-C d'un portable", "max", "W"),
        ("poids_kg", "Poids (sans pied)", "min", "kg"),
    ],
    "imprimante": [
        ("technologie", "Technologie", None, "t"), ("vitesse_noir", "Vitesse noir (ISO)", "max", "ppm"),
        ("vitesse_couleur", "Vitesse couleur (ISO)", "max", "ppm"), ("recto_verso", "Recto-verso automatique", None, "t"),
        ("chargeur", "Chargeur de documents", None, "t"), ("format_max", "Format maximal", None, "t"),
        ("fonctions", "Fonctions", None, "t"), ("temps_tirage_s", "Temps par tirage annoncé", "min", "s"),
        ("batterie", "Batterie intégrée", None, "t"), ("poids_kg", "Poids", "min", "kg"),
    ],
}


def charger():
    p = SRC + "rivaux_specs.json"
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def noyau():
    p = SRC + "sitemap_v2.json"
    return set(json.load(open(p, encoding="utf-8"))["fiches"]) if os.path.exists(p) else set()


MIN_MOY = 5   # nombre minimal de produits relevés pour afficher une moyenne de caractéristique
SPECS = charger()
NOYAU = noyau()


def choisir_rivaux(d, items):
    """items = les produits de l'usage (dict du générateur, avec 'id' et 'p' = prix indicatif)."""
    autres = sorted([x for x in items if x["id"] != d["id"]], key=lambda x: (abs(x["p"] - d["p"]), x["p"]))
    riv = [x for x in autres if x["id"] in NOYAU][:3]
    if len(riv) < 2:
        riv += [x for x in autres if x not in riv][:2 - len(riv)]
    return riv


def _nombre(x):
    """Nombre à la française : espace insécable fine pour les milliers, virgule décimale, zéros inutiles retirés."""
    if isinstance(x, float) and not x.is_integer():
        s = f"{x:,.3f}".rstrip("0").rstrip(".")
    else:
        s = f"{int(x):,}"
    return s.replace(",", "\u202f").replace(".", ",")


def _aff(v, fmt):
    if v is None or v == "":
        return "—"
    if fmt == "t" or not isinstance(v, (int, float)):
        txt = str(v)
        return E(txt if fmt == "t" or fmt in txt else f"{txt} {fmt}")
    if fmt == "Go" and v >= 1000:
        return f"{_nombre(v / 1000)} To"
    return f"{_nombre(v)} {fmt}"


def bloc(d, fam_key, items, rang, fr, euro_ind, root):
    """Rend la section, ou "" si la fiche n'est pas du noyau ou n'a pas de caractéristiques relevées.
    Renvoie (html, nombre de critères comparés)."""
    if d["id"] not in NOYAU or d["id"] not in SPECS or fam_key not in CRITERES:
        return "", 0
    riv = choisir_rivaux(d, items)
    if not riv:
        return "", 0
    cols = [d] + riv
    rangs = {x["id"]: i + 1 for i, x in enumerate(items)}
    lignes = []   # (libellé, [valeurs affichées], indice du meilleur ou None)

    mieux = []   # critères où la fiche fait mieux que la moyenne de son top 10

    def moyenne(valeurs):
        """Moyenne du top 10 de l'usage, seulement si au moins MIN_MOY produits ont la valeur (sinon None)."""
        num = [v for v in valeurs if isinstance(v, (int, float))]
        return (sum(num) / len(num), len(num)) if len(num) >= MIN_MOY else (None, len(num))

    def ajouter(lib, vals, fmt, sens, moy=(None, 0)):
        if all(v is None or v == "" for v in vals[1:]) or vals[0] is None or vals[0] == "":
            return  # une ligne n'a de sens que si le produit ET au moins un rival ont la valeur
        best = None
        num = [v for v in vals if isinstance(v, (int, float))]
        if sens and len(num) >= 2:
            cible = max(num) if sens == "max" else min(num)
            if sum(1 for v in num if v == cible) == 1:
                best = vals.index(cible)
        m, nm = moy
        if m is None:
            cell = "—"
        else:
            cell = _aff(round(m, 2) if fmt == "kg" else round(m), fmt) + (f' <span class="riv-n">({nm} modèles)</span>' if nm < len(items) else "")
            if sens and isinstance(vals[0], (int, float)) and ((sens == "max" and vals[0] > m * 1.02) or (sens == "min" and vals[0] < m * 0.98)):
                mieux.append(lib.lower())
        lignes.append((lib, [_aff(v, fmt) for v in vals], best, cell))

    for cle, lib, sens, fmt in CRITERES[fam_key]:
        moy = moyenne([SPECS.get(x["id"], {}).get("v", {}).get(cle) for x in items]) if sens else (None, 0)
        ajouter(lib, [SPECS.get(x["id"], {}).get("v", {}).get(cle) for x in cols], fmt, sens, moy)

    def note(x):
        return round(x["press"]["avg"], 1) if x["press"] else None

    def ecart(x):
        s = [n["score"] for n in x["tests"]["notes"] if n["score"] is not None]
        return round(max(s) - min(s), 1) if len(s) >= 2 else None

    def moy_site(valeurs, aff):
        num = [v for v in valeurs if v is not None]
        if not num:
            return "—"
        return aff(sum(num) / len(num)) + (f' <span class="riv-n">({len(num)} modèles)</span>' if len(num) < len(items) else "")

    vals = [note(x) for x in cols]
    lignes.append(("Note presse", [f"{fr(v)}/10" if v is not None else "sans note" for v in vals],
                   (vals.index(max(v for v in vals if v is not None)) if sum(1 for v in vals if v is not None and v == max(w for w in vals if w is not None)) == 1 else None) if any(v is not None for v in vals) else None,
                   moy_site([note(x) for x in items], lambda m: f"{fr(m)}/10")))
    vals = [x["tests"]["tests"] for x in cols]
    lignes.append(("Tests recensés", [str(v) for v in vals], vals.index(max(vals)) if vals.count(max(vals)) == 1 else None,
                   moy_site([x["tests"]["tests"] for x in items], lambda m: fr(m))))
    vals = [ecart(x) for x in cols]
    if vals[0] is not None:
        lignes.append(("Écart entre médias", [f"{fr(v)} pt" if v is not None else "—" for v in vals], None,
                       moy_site([ecart(x) for x in items], lambda m: f"{fr(m)} pt")))
    vals = [x["p"] for x in cols]
    lignes.append(("Prix indicatif", [euro_ind(v) for v in vals], vals.index(min(vals)) if vals.count(min(vals)) == 1 else None,
                   moy_site([x["p"] for x in items], euro_ind)))
    vals = [rangs.get(x["id"]) for x in cols]
    lignes.append(("Rang dans le top 10", [f"n° {v}" for v in vals], vals.index(min(vals)) if vals.count(min(vals)) == 1 else None, "—"))
    n0 = note(d)
    notes_top = [note(x) for x in items if note(x) is not None]
    if n0 is not None and notes_top and n0 > sum(notes_top) / len(notes_top) + 0.05:
        mieux.append("note presse")

    # lecture : les critères où la fiche est seule en tête
    gagnes = [lib.lower() for lib, _, b, _m in lignes if b == 0]
    noms = ", ".join(E(x["short"]) for x in riv[:-1]) + (" et " if len(riv) > 1 else "") + E(riv[-1]["short"])
    if gagnes:
        lecture = f"Face à {noms}, ce modèle est seul en tête sur : {', '.join(gagnes)}."
    else:
        lecture = f"Face à {noms}, ce modèle n'est seul en tête sur aucun des critères comparés : ses atouts sont à chercher dans la synthèse des tests."
    if mieux:
        lecture += f" Par rapport à la moyenne de son top 10, il fait mieux sur : {', '.join(mieux)}."
    else:
        lecture += " Il ne dépasse la moyenne de son top 10 sur aucun critère chiffré."

    tete = "<th></th>" + "".join(
        f'<th class="{"moi" if i == 0 else ""}">' + (E(x["short"]) if i == 0 else f'<a href="{root}{x["purl"]}" data-zi="rivaux">{E(x["short"])}</a>') + "</th>"
        for i, x in enumerate(cols)) + '<th class="moy">Moyenne du top 10</th>'
    corps = "".join("<tr><th>" + E(lib) + "</th>" + "".join(
        f'<td class="{" ".join(c for c in ("moi" if i == 0 else "", "best" if b == i else "") if c)}">{v}</td>' for i, v in enumerate(vs)) + f'<td class="moy">{m}</td></tr>'
        for lib, vs, b, m in lignes)
    sources = sorted({SPECS[x["id"]]["source"] for x in cols if x["id"] in SPECS})
    dates = sorted({SPECS[x["id"]].get("releve", "") for x in cols if x["id"] in SPECS})
    jj = "/".join(reversed(dates[-1].split("-"))) if dates and dates[-1] else ""
    liens = " · ".join(f'<a href="{E(s)}" target="_blank" rel="noopener nofollow">{i + 1}</a>' for i, s in enumerate(sources))
    n = len(lignes)
    out = f"""
  <section class="section p-sec" id="rivaux">
    <div class="section-head"><h2>Face à ses rivaux directs</h2><div class="tag">{n} critères comparés</div></div>
    <p class="p-cons riv-lecture">{lecture}</p>
    <div class="riv-table"><table><thead><tr>{tete}</tr></thead><tbody>{corps}</tbody></table></div>
    <p class="riv-note">Rivaux : les produits du même top 10 les plus proches en prix. En surligné, le seul meilleur de la ligne (hors moyenne). Moyenne du top 10 : calculée sur les produits du même top 10 dont la valeur est relevée, et seulement si au moins 5 le sont ; le nombre de modèles est indiqué quand il en manque. Caractéristiques annoncées par les fabricants et configuration de l'offre suivie{f", relevées le {jj}" if jj else ""} (sources : {liens}) ; notes, tests et prix : relevé Top 10 Geek.</p>
  </section>"""
    return out, n
