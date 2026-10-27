# -*- coding: utf-8 -*-
"""Règle de classement unique du site (audit SEO du 10/10/2026), partagée par gen10.py et _video/export_data.py.

1. « Le choix de la bande » en tête, seulement si sa note repose sur au moins SEUIL_NOTES notes presse ;
2. puis trois groupes : produits notés par au moins SEUIL_NOTES médias, puis 1 ou 2 notes, puis testés sans note ;
3. dans chaque groupe : note ajustée (moyenne bayésienne vers la moyenne de l'usage, PRIOR_M notes fictives),
   puis nombre de notes (ou de tests), puis prix.
Un « choix de la bande » qui n'arrive pas premier affiche BADGE_RETRO.

Règle du 27/10/2026 (toutes les rubriques) : « notre choix » est, de préférence, un produit de la zone « bonnes affaires »
du radar (note presse affichée d'au moins ZONE_NOTE, prix indicatif au plus égal à la médiane des prix de l'usage) dont la
note repose sur au moins SEUIL_NOTES notes. Si le choix éditorial n'y est pas, on lui préfère le mieux classé des produits
de la zone, pourvu que sa note ajustée ne soit pas inférieure de plus de MARGE_CHOIX point à celle du choix éditorial.
Sinon (aucun candidat, ou écart trop grand), le choix éditorial est conservé. Calculé à chaque génération : il suit les prix.
"""
TOP_BADGE = "Le choix de la bande"
BADGE_RETRO = "Prometteur, peu testé"
SEUIL_NOTES = 3
PRIOR_M = 3
ZONE_NOTE = 8.0
MARGE_CHOIX = 0.5
BADGE_MIEUX_NOTE = "Le mieux noté"
BADGE_SURE = "La valeur sûre"
BADGE_HAUT = "Le haut de gamme"


def moyenne_usage(avgs):
    """Moyenne simple des notes presse d'un usage (7,5 à défaut)."""
    avgs = [a for a in avgs if a is not None]
    return sum(avgs) / len(avgs) if avgs else 7.5


def note_ajustee(avg, n, moyenne):
    return (n * avg + PRIOR_M * moyenne) / (n + PRIOR_M) if avg is not None and n else None


def cle(badge, avg, n, tests, prix, moyenne):
    """Clé de tri. avg = None et n = 0 pour un produit testé sans note chiffrée."""
    n = n if avg is not None else 0
    top = 0 if badge == TOP_BADGE and n >= SEUIL_NOTES else 1
    tier = 0 if n >= SEUIL_NOTES else (1 if avg is not None else 2)
    return (top, tier, -round(note_ajustee(avg, n, moyenne) or 0, 4), -(n or tests), prix)


def badge_affiche(badge, rang):
    return BADGE_RETRO if badge == TOP_BADGE and rang > 1 else badge


def mediane_prix(prix):
    """Médiane (valeur haute) des prix d'un usage, comme dans le radar des bonnes affaires."""
    return sorted(prix)[len(prix) // 2]


def en_zone(avg, prix, mediane):
    """Zone « bonnes affaires » du radar : bien noté (note affichée >= ZONE_NOTE) et pas cher (<= médiane de l'usage)."""
    return avg is not None and round(avg, 1) >= ZONE_NOTE and prix <= mediane


def appliquer_choix(rows):
    """rows : produits d'UN usage, dicts avec id, badge, avg (None si sans note), n, tests, p.
    Retourne {id: nouveau badge} pour les produits dont le badge change (vide si le choix éditorial est déjà bon)."""
    moy = moyenne_usage([r["avg"] for r in rows])
    med = mediane_prix([r["p"] for r in rows])
    key = lambda r: cle(r["badge"], r["avg"], r["n"] if r["avg"] is not None else 0, r["tests"], r["p"], moy)
    ordre = sorted(rows, key=key)
    actuel = ordre[0]
    zone = lambda r: en_zone(r["avg"], r["p"], med)
    if zone(actuel) and actuel["n"] >= SEUIL_NOTES:
        return {}
    cands = [r for r in rows if zone(r) and r["n"] >= SEUIL_NOTES]
    if not cands:
        return {}
    adj = lambda r: note_ajustee(r["avg"], r["n"], moy) or 0
    best = min(cands, key=lambda r: (-round(adj(r), 4), -r["n"], r["p"]))
    if best is actuel or adj(best) < (adj(actuel) if actuel["avg"] is not None else 0) - MARGE_CHOIX:
        return {}
    out = {best["id"]: TOP_BADGE}
    if actuel["badge"] == TOP_BADGE:
        notes = [r for r in rows if r["avg"] is not None and r["n"] >= SEUIL_NOTES]
        if notes and actuel is max(notes, key=lambda r: (round(r["avg"], 1), r["n"])):
            out[actuel["id"]] = BADGE_MIEUX_NOTE
        elif actuel["p"] == max(r["p"] for r in rows):
            out[actuel["id"]] = BADGE_HAUT
        else:
            out[actuel["id"]] = BADGE_SURE
    return out
