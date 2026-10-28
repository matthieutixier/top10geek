# -*- coding: utf-8 -*-
"""Catalogue Top 10 Geek — TV & HOME CINÉMA (rubrique ouverte le 28/10/2026), usage « 50–55 pouces ».
Les tests de la presse viennent de CommentChoisir (cc_fiche.py), conservés dans cc_fiches_tv.json : une ligne par média
(moyenne si plusieurs tests du même média), tests datés de 2024 ou après. La confirmation à la source reste à faire.
Taille de référence : 55 pouces (50 pouces pour le Samsung QN90F, seule taille vendue par Amazon.fr au moment du relevé).
Prix : relevé Amazon du 27/10/2026 (navigateur), à renouveler par releve.py. Points forts / faibles : ceux cités par les tests."""
import json, os
from catalog_sols import S, TOP

_HERE = os.path.dirname(os.path.abspath(__file__))
T55 = "t-55"
TPF = "t-petit"
T65 = "t-65"
TV = {}


def notes_tv(fiche):
    """[(média, note /10 ou None, url)] — une ligne par média, les mieux notés d'abord."""
    brut = json.load(open(os.path.join(_HERE, "cc_fiches_tv.json"), encoding="utf-8"))[fiche]["tests"]
    par = {}
    for t in brut:
        m = t["media"].replace("\x92", "’").strip()
        par.setdefault(m, dict(notes=[], url=t["url"]))
        if t["note10"] is not None:
            par[m]["notes"].append(t["note10"])
    out = [(m, round(sum(v["notes"]) / len(v["notes"]), 1) if v["notes"] else None, v["url"]) for m, v in par.items()]
    out.sort(key=lambda x: (x[1] is None, -(x[1] or 0), x[0].lower()))
    return out


def add(pid, cat, short, ref, badge, verdict, strengths, weak, m, fiche, asin, amz, price, pour, eviter, scope="modele", seller="Amazon"):
    TV[pid] = S(cat, short, ref, badge, verdict, strengths, weak, m, notes_tv(fiche), asin, amz, price, pour, eviter, scope=scope, seller=seller)


add("lg-oled-g5", T55, "LG OLED G5 55\"", "OLED evo · 4 000 nits · 144 Hz", TOP,
    "Le téléviseur le mieux noté de la sélection : une image très lumineuse et des noirs parfaits, avec un équipement complet pour le jeu. Son prix est celui du haut de gamme.",
    ["Luminosité de crête très élevée", "Qualité d'image excellente, nette et colorée", "Excellent ensemble de fonctionnalités pour les joueurs"],
    ["Son terne", "Luminosité réduite en mode Jeu", "Pas de support de l'audio DTS"],
    ("OLED evo", "Prix élevé"), "LG OLED G5",
    "B0F3D88VP6", "LG OLED55G54LW TV 55 pouces OLED Evo 4K Smart TV AI G5", 1299.0,
    "Vous voulez la meilleure image du moment, pour le cinéma comme pour le jeu, et acceptez un prix haut de gamme.",
    "Vous cherchez un téléviseur à moins de 800 € ou vous comptez sur le son intégré.", scope="gamme", seller="Icoza")

add("samsung-qn90f-50", T55, "Samsung Neo QLED QN90F 50\"", "Mini-LED · anti-reflets · 144 Hz", "Le mini-LED premium",
    "Un Mini-LED Samsung très bien noté pour ses noirs profonds et sa luminosité HDR, avec un traitement anti-reflets. Pas de Dolby Vision et un prix élevé pour la taille.",
    ["Qualité d'image époustouflante avec des noirs profonds", "Excellente luminosité HDR", "Écran anti-éblouissement"],
    ["Pas de Dolby Vision", "Cher par rapport aux téléviseurs concurrents", "Niveaux de noir moins bons en mode Jeu"],
    ("Mini-LED", "Anti-reflets"), "Samsung Neo QLED QN90F",
    "B0F2241BR4", "Samsung Mini TV 50 Pouces Neo QLED QN90F 4K Mini LED Smart TV", 799.0,
    "Vous regardez dans une pièce lumineuse et voulez un Mini-LED haut de gamme sans passer à l'OLED.",
    "Vous tenez au Dolby Vision ou cherchez le meilleur prix.", scope="gamme", seller="Icoza")

add("sony-bravia-3-55", T55, "Sony Bravia 3 55\"", "Direct LED · Google TV · HDMI 2.1", "Le traitement d'image Sony",
    "Un téléviseur Sony abordable au traitement d'image reconnu et à l'interface Google TV, mais à la luminosité HDR limitée.",
    ["Traitement d'image Sony", "Interface Google TV", "Rapport qualité-prix attractif"],
    ["Manque de luminosité HDR", "Luminosité limitée dans les pièces très éclairées", "Dalle native 50/60 Hz, sans 120 Hz"],
    ("Direct LED", "Google TV"), "Sony Bravia 3",
    "B0F4KXJQ42", "Sony BRAVIA 3 Direct LED 55 pouces Google TV (2025)", 649.0,
    "Vous voulez un téléviseur Sony simple, avec Google TV, pour un usage familial.",
    "Vous regardez surtout des films HDR dans une pièce lumineuse ou jouez à 120 Hz.", scope="gamme")

add("samsung-qn80f-55", T55, "Samsung Neo QLED QN80F 55\"", "Mini-LED · Quantum Matrix · Tizen", "Mini-LED Samsung",
    "Un Mini-LED Samsung aux belles couleurs naturelles et au design plat, mais sans Dolby Vision et à la classe énergétique F.",
    ["Rétroéclairage Mini-LED à points quantiques", "Belles couleurs naturelles", "Son harmonieux et dynamique"],
    ["Pas de Dolby Vision (HDR10 uniquement)", "Classe énergétique F", "Quelques zones d'assombrissement"],
    ("Mini-LED", "Tizen"), "Samsung QN80F",
    "B0F2FJY819", "Samsung TV AI 55QN80F Neo QLED 4K 55 pouces Smart TV 2025", 589.0,
    "Vous voulez un Mini-LED Samsung aux couleurs naturelles pour le salon.",
    "Vous tenez au Dolby Vision ou à une faible consommation.", scope="gamme")

add("hisense-u7q-55", T55, "Hisense U7Q 55\"", "Mini-LED · HDMI 2.1 · VIDAA", "Le bon compromis",
    "Un Mini-LED abordable au contraste élevé et au mode jeu réactif, mais dont la luminosité HDR reste limitée.",
    ["Contraste natif élevé grâce à la dalle VA", "Mode jeu performant, input lag très faible", "HDMI 2.1 (VRR 144 Hz, ALLM, eARC)"],
    ["Rétroéclairage Mini-LED peu dense", "Luminosité HDR limitée", "Revêtement semi-brillant sujet aux reflets"],
    ("Mini-LED", "HDMI 2.1"), "Hisense U7Q",
    "B0F32M68DW", "Hisense TV 55U7Q (2025) 55 ULED Mini-LED UHD 4K", 509.0,
    "Vous voulez un Mini-LED contrasté et réactif pour le jeu, à un prix contenu.",
    "Vous regardez dans une pièce très lumineuse ou exigez un HDR éclatant.", scope="gamme", seller="Icoza")

add("lg-qned85-55", T55, "LG QNED85 55\"", "Mini-LED · 120 Hz · HDMI 2.1", "Lumineux et abordable",
    "Un téléviseur LG lumineux, vendu à un prix contenu, qui gère bien les reflets ; les couleurs sont moins vives et le son modeste.",
    ["Grande luminosité maximale", "Gestion décente des reflets", "Angle de vision cohérent"],
    ["Couleurs peu vives", "Son assez médiocre", "Mise en œuvre de l'IA pas entièrement réussie"],
    ("Mini-LED", "120 Hz"), "LG QNED85",
    "B0GWFRGP27", "LG TV QNED Evo AI MiniLED 55QNED85 55 pouces 4K UHD Smart TV 120Hz", 509.99,
    "Vous voulez un téléviseur lumineux pour un salon éclairé, sans y mettre plus de 550 €.",
    "Vous cherchez des couleurs éclatantes ou un bon son intégré.", scope="gamme")

add("hisense-e7q-pro-55", T55, "Hisense E7Q Pro 55\"", "Mini-LED · 144 Hz · FreeSync", "Le moins cher",
    "Le moins cher de la sélection : une dalle Mini-LED à 144 Hz bien équipée pour le jeu, mais à la gestion des halos et aux angles de vision limités.",
    ["Dalle Mini-LED, 1 000 nits de luminosité crête", "144 Hz natifs, FreeSync Premium", "Dolby Vision IQ et HDR10"],
    ["Finition brillante sensible aux reflets", "Système VIDAA moins fourni en applications", "Halos Mini-LED perfectibles, angles de vision limités"],
    ("Mini-LED", "144 Hz"), "Hisense E7Q Pro",
    "B0F1N7WT6C", "Hisense 55E7Q Pro TV QLED 4K 55 pouces 144Hz Dolby Vision FreeSync Premium", 489.0,
    "Vous voulez jouer à 144 Hz sur grand écran pour moins de 500 €.",
    "Vous regardez dans la pénombre des scènes très contrastées ou à plusieurs, de côté.", scope="gamme", seller="Icoza")


# ============================================================ PETITS FORMATS (jusqu'à 48 pouces)
add("lg-oled-c5-48", TPF, "LG OLED C5 48\"", "OLED evo · 120 Hz · α9 Gen 8", TOP,
    "L'OLED de référence de LG en petit format : noirs parfaits, couleurs précises et image lumineuse, avec une télécommande sans rétroéclairage et un HDR10 jugé étrange dans les scènes sombres.",
    ["Rapport de contraste quasi infini, noirs parfaits", "Angle de vision très large", "Couleurs vibrantes, réalistes et précises"],
    ["HDR10 avec un contour inhabituel dans les scènes sombres", "Réflectance significative de la dalle", "Classe énergétique F"],
    ("OLED evo", "120 Hz"), "LG OLED C5",
    "B0FQP2W4Z4", "LG TV OLED OLED48C5 OLED Evo Noir Profond 120 Hz 4K 121 cm 2025", 999.0,
    "Vous voulez un vrai OLED sur un bureau, une chambre ou un petit salon, et jouer en 120 Hz.",
    "Vous cherchez un téléviseur à moins de 600 € ou regardez dans une pièce très éclairée.", scope="gamme", seller="Icoza")

add("samsung-s90f-42", TPF, "Samsung OLED S90F 42\"", "QD-OLED · 144 Hz · anti-reflets", "Les couleurs vives",
    "Un OLED Samsung très bien noté pour ses couleurs vibrantes et sa gestion des reflets, mais sans Dolby Vision et aux basses limitées. À noter : les dalles diffèrent selon la diagonale.",
    ["Noirs parfaits sans halo", "Excellente gestion des reflets", "Couleurs très vibrantes et précises"],
    ["Pas de Dolby Vision", "Luminosité en retrait face aux meilleurs OLED", "Dalles distinctes selon la diagonale"],
    ("OLED", "Anti-reflets"), "Samsung S90F",
    "B0FT879YNJ", "Samsung TV AI OLED 42 Pouces S90F 4K Smart TV 2025", 861.44,
    "Vous voulez un OLED compact aux couleurs vives, pour un bureau ou une pièce lumineuse.",
    "Vous tenez au Dolby Vision ou à la même dalle que les grandes diagonales.", scope="gamme", seller="Super10count")

add("sony-bravia-3-43", TPF, "Sony Bravia 3 43\"", "Direct LED · Google TV · HDMI 2.1", "Le plus abordable",
    "Un petit téléviseur Sony abordable, au traitement d'image reconnu et à l'interface Google TV, mais à la luminosité HDR limitée.",
    ["Traitement d'image Sony", "Interface Google TV", "Rapport qualité-prix attractif"],
    ["Manque de luminosité HDR", "Luminosité limitée dans les pièces très éclairées", "Dalle native 50/60 Hz, sans 120 Hz"],
    ("Direct LED", "Google TV"), "Sony Bravia 3",
    "B0F4KVZSKW", "Sony BRAVIA 3 Direct LED 43 pouces Google TV (2025)", 469.0,
    "Vous voulez un petit téléviseur Sony simple et abordable, pour une chambre ou une cuisine.",
    "Vous jouez à 120 Hz ou regardez des films HDR dans une pièce lumineuse.", scope="gamme")

add("samsung-qn80f-50", TPF, "Samsung Neo QLED QN80F 50\"", "Mini-LED · Quantum Matrix · 144 Hz", "Le Mini-LED compact",
    "Un Mini-LED Samsung aux belles couleurs naturelles, ici dans sa version 50 pouces ; il n'a pas de Dolby Vision et sa classe énergétique est F.",
    ["Rétroéclairage Mini-LED à points quantiques", "Belles couleurs naturelles", "Son harmonieux et dynamique"],
    ["Pas de Dolby Vision (HDR10 uniquement)", "Classe énergétique F", "Quelques zones d'assombrissement"],
    ("Mini-LED", "144 Hz"), "Samsung QN80F",
    "B0F22914WP", "Samsung Mini TV 50 Pouces Neo QLED QN80F 4K Mini LED Smart TV", 720.11,
    "Vous voulez un Mini-LED Samsung de taille raisonnable, pour une pièce de taille moyenne ou un bureau.",
    "Vous tenez au Dolby Vision ou cherchez un tarif plus bas : le 55 pouces coûte moins cher.", scope="gamme", seller="Super10count")


# ============================================================ 65 POUCES ET PLUS (taille de référence : 65 pouces)
add("samsung-s90f-65", T65, "Samsung OLED S90F 65\"", "QD-OLED · 144 Hz · anti-reflets", TOP,
    "Un OLED Samsung très bien noté pour ses couleurs vibrantes et sa gestion des reflets, mais sans Dolby Vision et nettement plus cher que les Mini-LED.",
    ["Noirs parfaits sans halo", "Excellente gestion des reflets", "Couleurs très vibrantes et précises"],
    ["Pas de Dolby Vision", "Luminosité en retrait face aux meilleurs OLED", "Basses limitées"],
    ("OLED", "Anti-reflets"), "Samsung S90F",
    "B0F2FLZW69", "Samsung TV 65 Pouces OLED S90F 4K Smart TV avec Vision AI Motion Xcelerator 144Hz", 1649.0,
    "Vous voulez un OLED aux couleurs vives pour un salon lumineux, et acceptez un prix élevé.",
    "Vous tenez au Dolby Vision ou cherchez un téléviseur à moins de 1 000 €.", scope="gamme", seller="Icoza")

add("samsung-qn80f-65", T65, "Samsung Neo QLED QN80F 65\"", "Mini-LED · Quantum Matrix · Tizen", "Mini-LED Samsung",
    "Un Mini-LED Samsung aux belles couleurs naturelles, vendu à un prix intermédiaire en 65 pouces, mais sans Dolby Vision et en classe énergétique F.",
    ["Rétroéclairage Mini-LED à points quantiques", "Belles couleurs naturelles", "Son harmonieux et dynamique"],
    ["Pas de Dolby Vision (HDR10 uniquement)", "Classe énergétique F", "Quelques zones d'assombrissement"],
    ("Mini-LED", "Tizen"), "Samsung QN80F",
    "B0F2FM1YNY", "Samsung TV AI 65QN80F Neo QLED 4K 65 pouces Smart TV 2025", 986.48,
    "Vous voulez un Mini-LED Samsung de grande taille, aux couleurs naturelles, pour un salon.",
    "Vous tenez au Dolby Vision ou à une faible consommation.", scope="gamme", seller="You Get - Innovation & Technology")

add("hisense-e7q-pro-65", T65, "Hisense E7Q Pro 65\"", "Mini-LED · 144 Hz · FreeSync", "Le jeu à petit prix",
    "Un grand téléviseur à dalle 144 Hz, bien équipé pour le jeu et vendu sous 750 €, mais aux halos Mini-LED et aux angles de vision limités.",
    ["Dalle Mini-LED, 1 000 nits de luminosité crête", "144 Hz natifs, FreeSync Premium", "Dolby Vision IQ et HDR10"],
    ["Finition brillante sensible aux reflets", "Système VIDAA moins fourni en applications", "Halos Mini-LED perfectibles, angles de vision limités"],
    ("Mini-LED", "144 Hz"), "Hisense E7Q Pro",
    "B0F1N62VSW", "Hisense 65E7Q Pro TV QLED 4K 65 pouces 144Hz Dolby Vision IQ", 749.0,
    "Vous voulez un grand écran 144 Hz pour la console ou le PC sans dépasser 750 €.",
    "Vous regardez dans la pénombre des scènes très contrastées ou à plusieurs, de côté.", scope="gamme", seller="best 4me")

add("lg-qned85-65", T65, "LG QNED85 65\"", "Mini-LED · 120 Hz · HDMI 2.1", "Lumineux et abordable",
    "Un téléviseur LG lumineux, qui gère bien les reflets, au prix contenu en 65 pouces ; les couleurs sont moins vives et le son modeste.",
    ["Grande luminosité maximale", "Gestion décente des reflets", "Angle de vision cohérent"],
    ["Couleurs peu vives", "Son assez médiocre", "Mise en œuvre de l'IA pas entièrement réussie"],
    ("Mini-LED", "120 Hz"), "LG QNED85",
    "B0GWFPJH72", "LG TV QNED 65 pouces 4K UHD QNED85 Smart TV 120Hz MiniLED", 799.0,
    "Vous voulez un grand téléviseur lumineux pour un salon éclairé, sans dépasser 800 €.",
    "Vous cherchez des couleurs éclatantes ou un bon son intégré.", scope="gamme", seller="Son-Video")

add("sony-bravia-3-65", T65, "Sony Bravia 3 65\"", "Direct LED · Google TV · HDMI 2.1", "Le traitement d'image Sony",
    "Un grand téléviseur Sony au traitement d'image reconnu et à l'interface Google TV, mais à la luminosité HDR limitée.",
    ["Traitement d'image Sony", "Interface Google TV", "Rapport qualité-prix attractif"],
    ["Manque de luminosité HDR", "Luminosité limitée dans les pièces très éclairées", "Dalle native 50/60 Hz, sans 120 Hz"],
    ("Direct LED", "Google TV"), "Sony Bravia 3",
    "B0F4KX8CK4", "Sony BRAVIA 3 Direct LED 65 pouces Google TV (2025)", 750.0,
    "Vous voulez un grand téléviseur Sony simple, avec Google TV, pour un usage familial.",
    "Vous regardez surtout des films HDR dans une pièce lumineuse ou jouez à 120 Hz.", scope="gamme")


def build():
    return dict(TV)
