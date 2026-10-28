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
VSP = "v-sport"
VPRJ = "v-proj"
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


# ============================================================ CAMÉRAS SPORT / 360° / VLOG
# Prix Amazon relevés le 28/10/2026 dans le navigateur ; vendeur indiqué quand ce n'est pas Amazon.
add("dji-osmo-action-5-pro", VSP, "DJI Osmo Action 5 Pro", "4K 120 · double écran · 20 m", TOP,
    "La caméra d'action la mieux placée en rapport qualité/prix : très bien stabilisée, double écran tactile et étanche à 20 mètres, avec une autonomie en hausse. Pas d'interface HDMI et pas de GPS intégré.",
    ["Deux écrans tactiles", "Excellente stabilisation", "Étanche à 20 mètres, autonomie en hausse"],
    ["Pas de GPS intégré", "Pas d'interface HDMI", "Bouton déclencheur un peu dur"],
    ("4K 120", "Double écran"), "DJI Osmo Action 5 Pro",
    "B07FW4CZZL", "Bundle Aventure DJI Osmo Action 5 Pro, caméra d'action 4K voyage/vlog, capteur 1/1,3, 12 h d'autonomie avec 3 batteries", 362.0,
    "Vous voulez une caméra d'action polyvalente pour le sport, le voyage ou le vélo, avec trois batteries fournies.",
    "Vous voulez filmer en 8K ou en 360°.")

add("dji-osmo-action-6", VSP, "DJI Osmo Action 6", "8K · capteur 1/1,1\" · ouverture variable", "Meilleure note",
    "La note la plus haute de la sélection (9,6/10, sur 4 tests) : un grand capteur carré, une ouverture variable et d'excellentes performances en faible lumière. Un peu plus lourde, toujours sans GPS.",
    ["Ouverture variable de f/2,0 à f/4,0", "Excellente performance en faible luminosité", "Longue durée de vie de la batterie"],
    ["Pas de GPS", "Légèrement plus lourde que sa devancière", "Micro mal placé, risque d'obstruction"],
    ("8K", "Capteur 1/1,1\""), "DJI Osmo Action 6",
    "B0FNMP8LZX", "DJI Bundle Essentiel Osmo Action 6, caméra d'action 8K à démarrage rapide, capteur carré de 1/1,1 pouce", 426.0,
    "Vous filmez souvent en faible lumière et voulez le meilleur capteur d'une caméra d'action.",
    "Vous cherchez la caméra la plus légère ou la moins chère.")

add("gopro-hero13-black", VSP, "GoPro HERO13 Black", "5.3K 60 · objectifs HB · 27 MP", "Valeur sûre",
    "La caméra d'action de référence : une stabilisation exceptionnelle, une très bonne image de jour et des objectifs interchangeables. Plus en retrait en basse lumière que la concurrence récente.",
    ["Stabilisation exceptionnelle", "Excellente qualité d'image de jour", "Objectifs interchangeables et autonomie à toute épreuve"],
    ["En retrait en basse lumière", "Surchauffe à haute résolution", "Carte SD non fournie"],
    ("5.3K 60", "Objectifs HB"), "GoPro Hero 13 Black",
    "B0F8PHLFX1", "GoPro HERO13 Black en Vert forêt (Couleur en édition limitée) - Caméra d'action étanche avec vidéo 5.3K60, Photo 27MP", 384.16,
    "Vous voulez l'écosystème d'accessoires GoPro et une stabilisation de référence.",
    "Vous filmez surtout de nuit ou en intérieur.")

add("insta360-ace-pro-2", VSP, "Insta360 Ace Pro 2", "8K · objectif Leica · écran rabattable", "8K polyvalente",
    "Une caméra d'action 8K à objectif Leica, très bonne en faible lumière, avec un écran tactile rabattable. Les couleurs HDR sont parfois artificielles et le boîtier un peu plus lourd.",
    ["Vidéo 8K", "Très bonne stabilisation d'image", "Performance élevée en faible luminosité"],
    ["Couleurs HDR parfois artificielles", "Un peu plus lourde que la concurrence", "Écran avant peu exploité"],
    ("8K", "Leica"), "Insta360 Ace Pro 2",
    "B0DHD6SFJB", "Insta360 Ace Pro 2 Noir Minuit - Caméra d'action 8K Objectif Leica, capteur 1/1,3, HDR 4K", 379.0,
    "Vous voulez une caméra d'action 8K à écran rabattable pour le vlog et le sport.",
    "Vous voulez des couleurs HDR toujours naturelles.", seller="Insta360 Official Store EU")

add("dji-osmo-pocket-3", VSP, "DJI Osmo Pocket 3", "CMOS 1\" · 4K 120 · nacelle 3 axes", "Vlog de poche",
    "La caméra de vlog de poche à nacelle 3 axes : une stabilisation efficace, une bonne image et une grande autonomie pour un format très compact. Autofocus parfois capricieux et batterie inamovible. Peu de tests récents.",
    ["Stabilisation efficace", "Bonne qualité d'image, compacte", "Longue durée de vie de la batterie"],
    ["Autofocus parfois capricieux", "Batterie inamovible", "Gestion du bruit en haute sensibilité"],
    ("4K 120", "Nacelle 3 axes"), "DJI Osmo Pocket 3",
    "B0CG19QXWD", "DJI Osmo Pocket 3, Caméra Vlogging CMOS 1'' et Vidéo 4K/120 IPS, stabilisation à 3 axes", 336.45,
    "Vous faites du vlog, du voyage ou du YouTube et voulez une caméra de poche très stable.",
    "Vous filmez dans l'eau ou dans des conditions extrêmes : elle n'est pas étanche.")

add("dji-osmo-pocket-4p", VSP, "DJI Osmo Pocket 4P", "Double objectif · zoom 3x · 4K 240", "Double objectif",
    "La nouvelle caméra de poche de DJI : deux objectifs, un zoom optique 3x et une qualité d'image exceptionnelle selon les tests. Chère, sans protection contre les intempéries et avec quelques limites en D-Log 2.",
    ["Qualité d'image exceptionnelle", "Deux objectifs, zoom optique 3x", "Plage dynamique améliorée"],
    ["Très chère", "Pas de protection contre les intempéries", "Limites en D-Log 2"],
    ("4K 240", "Zoom 3x"), "DJI Osmo Pocket 4P",
    "B0H2MRDB2C", "DJI Bundle Standard Osmo Pocket 4P, caméra vlog 4K à Double Objectif, zoom optique 3×", 599.0,
    "Vous cherchez la meilleure caméra de vlog de poche, avec un vrai téléobjectif.",
    "Vous avez un budget limité ou filmez sous la pluie.")

add("insta360-x5", VSP, "Insta360 X5", "8K 360° · capteurs 1/1,28\" · objectifs remplaçables", "360° de référence",
    "La caméra 360° la mieux couverte par la presse (11 tests) : vidéo 8K, bonne qualité jour et nuit, objectifs remplaçables. Grande et lourde, avec une autonomie moyenne et un prix élevé.",
    ["Vidéo 8K, mode InstaFrame", "Objectifs remplaçables", "Grand écran tactile, étanche"],
    ["Prix élevé", "Batterie médiocre", "Grande et lourde"],
    ("8K 360°", "Objectifs remplaçables"), "Insta360 x5",
    "B0DZCBYCNY", "Insta360 X5 - Caméra 360 8K, Double Capteur 1/1,28, objectifs robustes & remplaçables, étanche", 582.0,
    "Vous voulez filmer en 360° avec une qualité d'image haut de gamme et recadrer ensuite.",
    "Vous cherchez une caméra compacte ou un petit prix.", seller="Tim Schüerhoff")

add("dji-osmo-360", VSP, "DJI Osmo 360", "8K 360° · capteur 1\" · perche invisible", "360° plus abordable",
    "Une caméra 360° à grand capteur 1 pouce : image nette, très bonne stabilisation et mode perche invisible convaincant. Objectifs fragiles et non interchangeables, application Windows décevante.",
    ["Images nettes et de haute qualité", "Stabilisation de haut niveau", "Mode perche invisible convaincant"],
    ["Objectifs fragiles, non interchangeables", "Application Windows décevante", "Écran tactile un peu petit"],
    ("8K 360°", "Capteur 1\""), "DJI Osmo 360",
    "B0FXGWJNNZ", "Bundle Essentiel DJI Osmo 360, Caméra Moto 360, imagerie 360° de 1 pouce, vidéo 360° en 8K native, perche invisible 1,2 m", 408.08,
    "Vous voulez une caméra 360° à grand capteur, à un prix plus doux que l'Insta360 X5.",
    "Vous voulez des objectifs remplaçables.", seller="M.BUR")

add("insta360-go-ultra", VSP, "Insta360 GO Ultra", "4K · 53 g · magnétique · mains libres", "Mains libres",
    "Une mini-caméra magnétique de 53 grammes à poser sur un vêtement, avec une image nettement améliorée et une bonne autonomie grâce à l'Action Pod. Chère, et l'étanchéité est limitée avec le boîtier.",
    ["Mise à niveau massive de la qualité d'image", "Connexion magnétique bien plus forte", "Légère : 53 grammes"],
    ["Très chère", "Étanchéité IPX4 avec l'Action Pod", "Montage IA un peu bâclé"],
    ("4K", "53 g"), "Insta360 GO Ultra",
    "B0FH22RB4S", "Insta360 GO Ultra Noir - Caméra Vlog 4K Mains Libres, caméra d'action magnétique portable", 429.0,
    "Vous voulez filmer en point de vue, mains libres, pour le vélo, la course ou le vlog.",
    "Vous cherchez une caméra d'action classique et robuste.", seller="Insta360 Official Store EU")

# ============================================================ VIDÉOPROJECTEURS
add("benq-gp520", VPRJ, "BenQ GP520", "4K · 2 600 lumens · Google TV · LED", TOP,
    "Un projecteur 4K à LED sous Google TV, noté 8/10 par trois médias, nettement moins cher que les autres modèles 4K du comparatif. Image lumineuse, installation automatique et son intégré correct ; les noirs restent limités et il ne gère pas les hauts taux de rafraîchissement.",
    ["Image lumineuse et nette, large prise en charge du HDR", "Système audio intégré performant", "Installation automatique réussie"],
    ["Niveaux de noir limités", "Pas de jeux à haut taux de rafraîchissement", "Distance de projection importante"],
    ("4K", "Google TV, 2 600 lm"), "BenQ GP520",
    "B0DKFBSLSQ", "BenQ GP520 Vidéoprojecteur Home Cinéma 4K HDR, 2600 LM, Google TV | Mode Auto Cinéma, réglage auto de l’image, MEMC & Pro-Sports, HDR10+, 98% Rec.709, 2x12W, eARC", 990.0,
    "Vous voulez un vrai projecteur 4K pour le salon, simple à installer, sans viser 2 000 €.",
    "Vous jouez en 120 Hz ou vous projetez dans une pièce où la lumière ne peut pas être coupée.", seller="Icoza")

add("xgimi-horizon-20-max", VPRJ, "XGIMI Horizon 20 Max", "4K · triple laser · 5 700 ISO lumens", "Très lumineux",
    "Le plus lumineux du comparatif : un triple laser 4K très précis, bien noté (9/10 de moyenne) par la presse. Son contraste est limité par la technologie DLP, le son n'est pas au niveau et le prix est élevé.",
    ["Luminosité record", "Image 4K triple laser très précise", "Couleurs justes et Google TV fluide"],
    ["Prix élevé", "Contraste et noirs limités par le DLP", "Effet arc-en-ciel pour les personnes sensibles"],
    ("4K", "Triple laser"), "XGIMI Horizon 20 Max",
    "B0FMXYZCZF", "XGIMI Horizon 20 Max 4K Videoprojecteur 5700 ISO Triple Laser Home Cinéma | Zoom & Lens Shift, IMAX Enhanced, Dolby Vision, Jusqu'à 300 , 1ms/240Hz VRR, Harman Kardon, Google TV Netflix", 2374.05,
    "Vous voulez une grande image 4K très lumineuse, y compris dans une pièce pas tout à fait sombre.",
    "Vous cherchez de beaux noirs profonds ou un budget serré.", seller="XGIMI Official Store")

add("xgimi-aura-2", VPRJ, "XGIMI Aura 2", "4K · triple laser · ultra courte focale", "Ultra courte focale",
    "Un projecteur laser 4K à ultra courte focale à poser près du mur, bien noté (8,3/10 sur sept tests). Image lumineuse et son Harman Kardon intégré ; en contrepartie, un prix très élevé et des performances limitées pour le jeu.",
    ["Image 4K HDR lumineuse et détaillée", "Système audio Harman Kardon intégré", "Connectique riche, interface Android TV"],
    ["Prix très élevé", "Pas de HDMI 2.1, limité à 60 Hz en jeu", "Quelques ralentissements de l'interface"],
    ("4K", "Ultra courte focale"), "XGIMI Aura 2",
    "B0D87FKHSD", "XGIMI AURA2 Videoprojecteur 4K Triple Laser Ultra Courte Focale | 2300 ISO, 1M:1 contraste, 0.177:1 (100  à 17.8cm), Dolby Vision, IMAX, 60W HK, Compatible avec Google TV,Home Cinéma", 2599.0,
    "Vous voulez remplacer le téléviseur par une grande image sans installer le projecteur au plafond.",
    "Vous jouez beaucoup : le 60 Hz limite l'intérêt pour la console.", seller="XGIMI Official Store")

add("benq-x3100i", VPRJ, "BenQ X3100i", "4K · 4LED · 3 300 lumens · 4 ms", "Gaming 4K",
    "Un projecteur 4K pensé pour la console, avec une latence très basse et une image lumineuse. Les trois tests chiffrés le notent entre 8 et 10/10 ; la presse relève un contraste un peu en retrait pour le cinéma et une gestion délicate du HDR.",
    ["Latence très faible pour un projecteur", "Image nette et lumineuse", "Décalage vertical de l'objectif"],
    ["Contraste un peu en retrait pour les cinéphiles", "Gestion délicate du HDR", "Construction surtout en plastique"],
    ("4K", "4 ms de latence"), "BenQ X3100i",
    "B0CMHBJ7W3", "BenQ X3100i Vidéoprojecteur Gaming pour Consoles - Véritable 4k UHD HDR 4LED 3300 ANSI Lumens | 4 ms de Latence | Mode Jeu Automatique | Xbox, PS5, Switch", 2239.13,
    "Vous jouez sur une grande image 4K avec une latence faible.",
    "Vous regardez surtout des films dans le noir complet.", seller="Son-Video")

add("benq-w2720i", VPRJ, "BenQ W2720i", "4K · LED · 2 500 lumens · Android TV", "Cinéma réglé",
    "Un projecteur 4K orienté cinéma, étalonné en usine, noté 9/10 de moyenne sur deux tests. Colorimétrie précise et connectique complète ; le son intégré est modeste et le contraste natif limité.",
    ["Colorimétrie précise, calibrage en sortie de carton", "Image convaincante avec toutes les sources", "Connectique complète, compact"],
    ["Contraste natif limité", "Son intégré modeste", "Pas de préréglage de jeu simple"],
    ("4K", "Étalonné en usine"), "BenQ W2720i",
    "B0DMV8HNMK", "BenQ W2720i | Projecteur Home Cinema intelligent 2500 lm 4K à LED avec mode cinéma géré par AI, DCI-P3, HDR, Delta E<3, Rec.709, étalonnage en usine, eARC, Dolby, 7.1 canaux, Android TV", 1783.91,
    "Vous voulez des couleurs justes pour regarder des films sans passer par les réglages.",
    "Vous comptez sur le son intégré : prévoyez une barre de son.", seller="Projecteur-Discount")

add("benq-x500i", VPRJ, "BenQ X500i", "4K · 4LED · courte focale · 2 200 lumens", "Courte focale",
    "Un projecteur 4K à courte focale qui se contente de petits espaces, noté 9, 8 et 7/10 par trois médias. Contraste et couleurs soignés ; la luminosité est juste dès qu'il y a de la lumière et le ventilateur s'entend en 4K.",
    ["Contraste solide, noirs profonds dans le noir", "Large gamme de couleurs, bon pré-étalonnage", "Adapté aux petits espaces"],
    ["Luminosité juste avec un peu de lumière", "Pas de HDMI 2.1", "Bruit de fonctionnement en 4K"],
    ("4K", "Courte focale"), "BenQ X500i",
    "B0CMHCHPMV", "BenQ X500i Vidéoprojecteur Gaming Véritable 4K UHD HDR 4LED 2200 ANSI Lumens Courte focale | 4 ms de Latence | Mode Jeux Automatique | Xbox, PS5, Switch", 1358.8,
    "Vous avez une petite pièce et voulez une grande image 4K à courte distance.",
    "Vous projetez dans une pièce claire.", seller="B2BFLIX")

add("epson-eh-ls800", VPRJ, "Epson EH-LS800B", "4K PRO-UHD · laser · 4 000 lumens · ultra courte focale", "Laser 3LCD",
    "Un projecteur laser 3LCD à ultra courte focale qui remplace un téléviseur, noté 8/10 par deux médias. Image lumineuse, bon son Yamaha ; il manque l'eARC, le HDR10+ et le Dolby Vision, et la ventilation s'entend à pleine puissance.",
    ["Image lumineuse, belles couleurs", "Excellent système audio", "Ultra courte focale, installation souple"],
    ["Pas d'eARC", "Ni HDR10+ ni Dolby Vision", "Ventilation bruyante à pleine puissance"],
    ("4K PRO-UHD", "Laser, 4 000 lm"), "Epson EH-LS800",
    "B0B988BSBC", "Epson Lifestudio Grand Plus EH-LS800B | Project. laser TV intelligente 4K home cinéma ultracourte focale | 4 000 lumens | 3LCD | Sound by YAMAHA | Android TV | Affichage 150 po | Garantie 5 ans | Noir", 2390.59,
    "Vous voulez une grande image lumineuse, en plein salon, avec le son intégré et sans passer par le plafond.",
    "Vous tenez au HDR dynamique ou à l'eARC.")

add("xgimi-mogo-4", VPRJ, "XGIMI MoGo 4", "1080p · portable · batterie 2,5 h", "Portable",
    "Un petit projecteur 1080p à batterie, qui se transporte et se pose partout, bien noté par la presse (8/10 pour la plupart des médias). Il manque de luminosité en plein jour, le contraste est faible et les haut-parleurs manquent de profondeur.",
    ["Batterie intégrée, très portable", "Tient un film long sur batterie", "Keystone utilisable même en mode jeu"],
    ["Luminosité limitée en plein jour", "Contraste natif faible", "Haut-parleurs sans profondeur"],
    ("1080p", "Batterie 2,5 h"), "XGIMI MoGo 4",
    "B0F37QW5NF", "XGIMI MoGo 4 Mini Videoprojecteur Portable 1080p | 450 ISO, Compatible avec Google TV, Netflix officiel, 360° rotation, 2.5h batterie, 2×6W Harman Kardon, WiFi Bluetooth", 539.0,
    "Vous voulez un projecteur à emporter dans le jardin, en vacances ou d'une pièce à l'autre.",
    "Vous projetez en plein jour.", seller="XGIMI Official Store")

add("benq-gv50", VPRJ, "BenQ GV50", "1080p · laser · portable · batterie", "Laser portable",
    "Un projecteur laser portable 1080p à batterie et à tête rotative, noté 8/10 par trois médias. Compact, calibré en sortie de carton et bien équipé en applications ; la luminosité reste faible et il n'y a ni 4K ni HDR10+.",
    ["Compact et facile à installer", "Corrections automatiques efficaces", "Netflix et applications disponibles"],
    ["Faible luminosité", "Pas de 4K", "Pas de HDR10+ ni de Dolby Vision"],
    ("1080p", "Laser portable"), "BenQ GV50",
    "B0DL9HH3VR", "BenQ GV50 Vidéoprojecteur Laser Portable 1080p, 500 lumens, Google TV | Batterie intégrée, projection rotative, haut-parleur basses 18W 2.1, réglage auto de l’image, Bluetooth, Netflix", 598.98,
    "Vous voulez un petit projecteur nomade qui se règle seul et qui s'oriente au plafond.",
    "Vous voulez une image 4K ou très lumineuse.")

add("epson-co-w01", VPRJ, "Epson CO-W01", "WXGA · 3LCD · 3 000 lumens", "Petit prix",
    "Le plus abordable du comparatif : un projecteur 3LCD de 3 000 lumens, noté entre 6 et 7,5/10. Il fait le travail pour un film à la maison, mais l'image n'est pas en 1080p natif, le contraste est faible et il n'y a pas de fonctions connectées.",
    ["Rapport qualité-prix", "Qualité de projection correcte", "Bonne luminosité pour le prix"],
    ["Résolution WXGA : mise à l'échelle nécessaire en 1080p", "Contraste faible, noirs grisâtres", "Un seul port HDMI, pas de Wi-Fi"],
    ("WXGA", "3 000 lm"), "Epson CO-W01",
    "B0B985KPML", "Epson CO-W01 | Projecteur WXGA abordable | 3LCD | 3 000 lumens ANSI | Affichage 378 Pouces (9,6 m) | Configuration Facile | Correction du trapèze | HDMI | Utilisation à Domicile et au Bureau | Blanc", 334.54,
    "Vous voulez essayer le projecteur sans dépenser plus de 350 €.",
    "Vous voulez une image nette en 1080p ou la TV connectée intégrée.", seller="AC Electro")


def build():
    return dict(VID)
