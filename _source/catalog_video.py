# -*- coding: utf-8 -*-
"""Catalogue Top 10 Geek — PHOTO / VIDÉO (rubrique ouverte le 28/10/2026), usage « Caméras de surveillance » (intérieur et extérieur).
Les tests de la presse viennent de CommentChoisir (cc_fiche.py), conservés dans cc_fiches_video.json : une ligne par média
(moyenne si plusieurs tests du même média), tests datés de 2024 ou après (les tests sans date lisible sont écartés).
La confirmation à la source (champ `verifie`) reste à faire.
Prix : relevé Amazon du 28/10/2026 (navigateur), à renouveler ; prix Electro Dépôt : flux Effinity du 28/10/2026.
Points forts / faibles : ceux cités par les tests."""
import json, os
from catalog_sols import S, TOP

_HERE = os.path.dirname(os.path.abspath(__file__))
VSV = "v-surv"
VID = {}


def notes_vid(fiche, src="cc_fiches_video.json"):
    """[(média, note /10 ou None, url)] — une ligne par média, les mieux notés d'abord ; tests sans date lisible écartés."""
    brut = json.load(open(os.path.join(_HERE, src), encoding="utf-8"))[fiche]["tests"]
    par = {}
    for t in brut:
        if t.get("date", "")[-4:] in ("", "1970") or int(t["date"][-4:]) < 2024:
            continue
        m = t["media"].replace("\x92", "’").strip()
        par.setdefault(m, dict(notes=[], url=t["url"]))
        if t["note10"] is not None:
            par[m]["notes"].append(t["note10"])
    out = [(m, round(sum(v["notes"]) / len(v["notes"]), 1) if v["notes"] else None, v["url"]) for m, v in par.items()]
    out.sort(key=lambda x: (x[1] is None, -(x[1] or 0), x[0].lower()))
    return out


def add(pid, cat, short, ref, badge, verdict, strengths, weak, m, fiche, asin, amz, price, pour, eviter, scope="modele", seller="Amazon", ed=None):
    VID[pid] = S(cat, short, ref, badge, verdict, strengths, weak, m, notes_vid(fiche), asin, amz, price, pour, eviter, scope=scope, seller=seller, ed=ed)


def ed(url_slug, name, price, ean, edid):
    return {"url": "https://track.effiliation.com/servlet/effi.redir?id_compteur=23321274&url=https%3A%2F%2Fwww.electrodepot.fr%2F" + url_slug + ".html",
            "name": name, "price": price, "ean": ean, "edid": edid}


# ============================================================ CAMÉRAS DE SURVEILLANCE
add("eufy-solocam-s340", VSV, "eufy SoloCam S340", "3K · double objectif · solaire · PTZ", TOP,
    "Une caméra extérieure autonome à deux objectifs et panneau solaire, très bien notée (9,1/10) et sans abonnement obligatoire. Pas de stockage sur NAS ni dans le cloud, et un Wi-Fi stable est nécessaire.",
    ["Deux caméras : grand angle 3K et téléobjectif 2K", "Installation sans fil, batterie et panneau solaire", "Pivotement et inclinaison motorisés"],
    ["Wi-Fi stable nécessaire", "Aucun stockage sur NAS ni dans le cloud", "Pas de mode privé"],
    ("3K", "Solaire, PTZ"), "Eufy SoloCam S340",
    "B0CF8R2P24", "eufy SoloCamS340 3K Caméra surveillance wifi extérieur sans fil", 127.65,
    "Vous voulez une caméra extérieure sans fil qui suit les mouvements et se recharge toute seule au soleil.",
    "Vous voulez stocker vos vidéos sur un NAS ou dans le cloud.", seller="AnkerDirect FR")

add("reolink-duo-3-poe", VSV, "Reolink Duo 3 PoE", "16 MP · 180° · PoE", "Panorama 180°",
    "La meilleure note de la sélection (8,8/10) : deux objectifs pour un panorama de 180° et une détection efficace, sans abonnement. Filaire (PoE) : l'alimentation n'est pas fournie et il n'existe pas de stockage cloud.",
    ["Champ de vision de 180°", "Belle qualité d'image de jour et avec les projecteurs de nuit", "Détection très efficace, sans option payante"],
    ["Alimentation PoE non fournie", "Vision infrarouge un peu décevante", "Pas de stockage cloud"],
    ("16 MP", "PoE, 180°"), "Reolink Duo 3",
    "B0CM34VG3X", "Reolink 16MP Camera PoE avec Double Objectif Vue Panor à 180°, Duo 3 PoE", 199.99,
    "Vous voulez couvrir une grande façade avec une seule caméra filaire et sans abonnement.",
    "Vous n'avez pas de câble Ethernet ou de switch PoE sur place.", seller="ReolinkEU")

add("eufycam-s4", VSV, "eufyCam S4", "4K · triple objectif · solaire · PTZ", "Haut de gamme",
    "Le système le plus complet et le plus cher de la sélection (8,7/10) : trois objectifs, PTZ motorisé et panneau solaire. Les fonctions d'IA exigent la station HomeBase S380, vendue à part, et l'ensemble coûte cher.",
    ["Triple objectif avec grand angle 4K et PTZ motorisé", "Autonome grâce au panneau solaire, batterie amovible 10 000 mAh", "Certifiée IP65"],
    ["Prix élevé pour le système complet", "HomeBase S380 nécessaire pour les fonctions d'IA", "Images enregistrées pas en 4K"],
    ("4K", "Triple objectif"), "Eufy EufyCam S4",
    "B0FH52BSZ7", "eufy Security eufyCam S4 4K UHD Caméra Surveillance WiFi extérieur sans Fil", 299.0,
    "Vous voulez un système extérieur très complet et acceptez de payer plus cher.",
    "Vous cherchez une caméra seule et peu chère.", seller="AnkerDirect FR")

add("tapo-c660", VSV, "Tapo C660 Kit", "4K · 360° · solaire", "Solaire 360°",
    "Une caméra extérieure 4K à 360°, livrée avec son panneau solaire, très bien notée (8,6/10) : installation sans fil, suivi de mouvement et filtre personnes, véhicules et animaux. Projecteur et sirène un peu faibles.",
    ["Installation sans fil, panneau solaire fourni", "Détection et suivi de mouvement efficaces", "Application claire et complète"],
    ["Projecteur pas très puissant", "Notifications enrichies payantes", "Sirène et haut-parleur faibles"],
    ("4K", "Solaire 360°"), "TP-Link Tapo C660",
    "B0FDQTRVSZ", "Tapo 4K Camera Exterieur sans fil solaire 360° Suivi IA, C660 KIT", 144.99,
    "Vous voulez une caméra 360° autonome en énergie pour le jardin ou la cour.",
    "Vous voulez des notifications enrichies sans abonnement.", seller="TP-Link France")

add("tapo-c425", VSV, "Tapo C425", "2K+ · batterie 300 jours", "Sans câble",
    "Une caméra extérieure à batterie (10 000 mAh) très simple à poser, bien notée (8,4/10) : image 2K+, vision nocturne en couleur et bonne reconnaissance. Chargement lent via micro-USB.",
    ["Montage flexible, indépendant de la prise électrique", "Haute résolution (2 560 × 1 440), grand champ", "Vision nocturne en couleur"],
    ["Pas de protection contre le vandalisme", "Connecteur micro-USB obsolète, charge lente", "Mouvements rapides mal détectés dans l'obscurité"],
    ("2K+", "Batterie"), "TP-Link Tapo C425",
    "B0CMCWXPFX", "Tapo 2K+ Camera Exterieur sans fil Batterie 10000mAh Autonomie de 300j, C425", 98.98,
    "Vous voulez une caméra extérieure sans câble ni prise à proximité.",
    "Vous voulez éviter de recharger une batterie.")

add("reolink-argus-4-pro", VSV, "Reolink Argus 4 Pro", "4K · 180° · solaire", "Grand angle solaire",
    "Une caméra solaire à deux objectifs (panorama 180°) et vision nocturne en couleur, notée 8,3/10 par dix médias. L'enregistrement est limité à 15 images par seconde et l'autonomie sur panneau solaire n'est pas exceptionnelle.",
    ["Deux objectifs, 5 120 × 1 440 px, champ de 180°", "Vision nocturne couleur (capteur ColorX)", "Wi-Fi 6 bibande, grande batterie"],
    ["Autonomie moyenne avec panneau solaire", "Enregistrement à seulement 15 images/s", "Inscription obligatoire auprès du fabricant"],
    ("4K", "180°, solaire"), "Reolink Argus 4 Pro",
    "B0D1BNPRR6", "Reolink 4K 180° Camera Exterieur sans Fil Solaire, ColorX, Argus 4 Pro", 195.51,
    "Vous voulez surveiller une large zone avec une seule caméra sans fil.",
    "Vous voulez une fluidité d'image maximale.", seller="SmartBuy-Online")

add("reolink-argus-eco-ultra", VSV, "Reolink Argus Eco Ultra", "4K · solaire · sans abonnement", "Petit prix solaire",
    "Une caméra solaire 4K abordable, aux finitions soignées, notée 8,5/10 par deux médias. Un peu imposante.",
    ["Finitions exemplaires", "Tarif abordable", "Vision nocturne en couleur, sans abonnement"],
    ["Caméra plutôt imposante"],
    ("4K", "Solaire"), "Reolink Argus Eco Ultra",
    "B0CFL6Z141", "Reolink 4K Camera Exterieur Solaire, Vision Nuit Couleur, Argus Eco Ultra", 119.99,
    "Vous voulez une caméra extérieure solaire 4K à prix contenu.",
    "Vous cherchez un modèle discret.", seller="ReolinkEU")

add("reolink-e1-zoom", VSV, "Reolink E1 Zoom", "4K · intérieur · zoom ×3 · pan-tilt", "Intérieur 4K",
    "La caméra d'intérieur de la sélection : pan-tilt motorisé, zoom optique ×3 et suivi d'objet, sans compte en ligne obligatoire. Rotation manuelle imprécise et application parfois capricieuse.",
    ["Grande qualité d'image avec zoom ×3", "Pivotement et inclinaison motorisés, suivi d'objet", "Pas de coûts supplémentaires pour l'IA"],
    ["Pas de géo-clôture", "Rotation manuelle imprécise", "Application parfois buguée"],
    ("4K", "Intérieur, zoom ×3"), "Reolink E1 Zoom",
    "B0F18235L4", "Reolink 4K 360° Caméra Surveillance WiFi Intérieure, E1 Zoom", 99.99,
    "Vous voulez surveiller une pièce (salon, chambre, animaux) avec un zoom et un suivi automatique.",
    "Vous cherchez une caméra pour l'extérieur.")

add("tapo-c520ws", VSV, "Tapo C520WS", "2K+ · pan-tilt 360° · filaire", "Petit prix pan-tilt",
    "La caméra extérieure pan-tilt la moins chère de la sélection (43 €) : un seul test de presse recensé (9/10 pour Le Café du Geek), donc une note à lire avec prudence.",
    ["Pan-tilt 360° et image 2K+", "Vision nocturne couleur", "Connexion Wi-Fi ou Ethernet"],
    ["Un seul test de presse recensé"],
    ("2K+", "Pan-tilt 360°"), "TP-Link Tapo C520WS",
    "B0CCW8GHT8", "Tapo 2K+ Camera Exterieur WiFi 360° Vision Nocturne Couleur Avancée, C520WS", 42.99,
    "Vous voulez une caméra extérieure motorisée à très petit prix, branchée sur secteur.",
    "Vous voulez une caméra sans fil ou un avis de presse abondant.",
    ed=ed("camera-tapo-c520ws-ex-mo-fil-2k", "Camera Tapo C520ws 4mp 2k", 42.99, "4895252501599", "10009498"))

add("blink-outdoor-4", VSV, "Blink Outdoor 4", "HD · piles 2 ans · module Sync requis", "Piles longue durée",
    "Une caméra extérieure bon marché, à piles (environ deux ans), simple à installer, notée 7,2/10. Elle exige un module de synchronisation Blink, n'est compatible qu'avec Alexa et plusieurs fonctions passent par un abonnement. L'offre relevée est celle de la caméra seule.",
    ["Bon marché", "Piles : environ deux ans d'autonomie", "Petite et facile à installer"],
    ["Pas de détection des animaux, véhicules et colis", "Fonctionne uniquement avec Alexa", "Plusieurs fonctions sous abonnement"],
    ("HD", "Piles 2 ans"), "Blink Outdoor 4",
    "B0B1N5RL1Q", "Caméra Blink Outdoor 4 : caméra de surveillance connectée HD sans fil, 2 ans d'autonomie (caméra supplémentaire uniquement)", 74.99,
    "Vous êtes déjà dans l'écosystème Amazon/Alexa et voulez une caméra à piles.",
    "Vous voulez une caméra autonome sans module ni abonnement.")


def build():
    return dict(VID)
