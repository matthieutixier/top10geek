# -*- coding: utf-8 -*-
"""Règle de classement unique du site (audit SEO du 10/10/2026), partagée par gen10.py et _video/export_data.py.

1. « Le choix de la bande » en tête, seulement si sa note repose sur au moins SEUIL_NOTES notes presse ;
2. puis trois groupes : produits notés par au moins SEUIL_NOTES médias, puis 1 ou 2 notes, puis testés sans note ;
3. dans chaque groupe : note ajustée (moyenne bayésienne vers la moyenne de l'usage, PRIOR_M notes fictives),
   puis nombre de notes (ou de tests), puis prix.
Un « choix de la bande » qui n'arrive pas premier affiche BADGE_RETRO.
"""
TOP_BADGE = "Le choix de la bande"
BADGE_RETRO = "Prometteur, peu testé"
SEUIL_NOTES = 3
PRIOR_M = 3


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
