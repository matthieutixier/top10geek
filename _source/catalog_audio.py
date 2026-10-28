# -*- coding: utf-8 -*-
"""Catalogue Top 10 Geek — SON / AUDIO / HI-FI (rubrique ouverte le 28/10/2026), usage « Enceintes Bluetooth portables ».
Les tests de la presse viennent de CommentChoisir (cc_fiche.py), conservés dans cc_fiches_audio.json : une ligne par média
(moyenne si plusieurs tests du même média), tests datés de 2024 ou après (les tests sans date lisible sont écartés).
La confirmation à la source (champ `verifie`) reste à faire.
Prix : relevé Amazon du 28/10/2026 (navigateur), à renouveler par releve.py ; prix Electro Dépôt : flux Effinity du 28/10/2026.
Points forts / faibles : ceux cités par les tests."""
import json, os
from catalog_sols import S, TOP

_HERE = os.path.dirname(os.path.abspath(__file__))
ABT = "a-bt"
AANC = "a-anc"
AUD = {}


def notes_aud(fiche, src="cc_fiches_audio.json"):
    """[(média, note /10 ou None, url)] — une ligne par média, les mieux notés d'abord ; tests sans date lisible écartés."""
    brut = json.load(open(os.path.join(_HERE, src), encoding="utf-8"))[fiche]["tests"]
    par = {}
    for t in brut:
        if t.get("date", "")[-4:] in ("", "1970"):
            continue
        m = t["media"].replace("\x92", "’").strip()
        par.setdefault(m, dict(notes=[], url=t["url"]))
        if t["note10"] is not None:
            par[m]["notes"].append(t["note10"])
    out = [(m, round(sum(v["notes"]) / len(v["notes"]), 1) if v["notes"] else None, v["url"]) for m, v in par.items()]
    out.sort(key=lambda x: (x[1] is None, -(x[1] or 0), x[0].lower()))
    return out


def add(pid, cat, short, ref, badge, verdict, strengths, weak, m, fiche, asin, amz, price, pour, eviter, scope="modele", seller="Amazon", ed=None):
    AUD[pid] = S(cat, short, ref, badge, verdict, strengths, weak, m, notes_aud(fiche), asin, amz, price, pour, eviter, scope=scope, seller=seller, ed=ed)


def ed(url_slug, name, price, ean, edid):
    return {"url": "https://track.effiliation.com/servlet/effi.redir?id_compteur=23321274&url=https%3A%2F%2Fwww.electrodepot.fr%2F" + url_slug + ".html",
            "name": name, "price": price, "ean": ean, "edid": edid}


# ============================================================ ENCEINTES BLUETOOTH PORTABLES
add("marshall-emberton-3", ABT, "Marshall Emberton III", "IP67 · 32 h · Auracast", TOP,
    "L'enceinte la mieux notée de la sélection : compacte, résistante à l'eau et à la poussière, avec une autonomie annoncée de plus de 32 heures. Pas d'égaliseur personnalisé, et le son force un peu à volume élevé.",
    ["Meilleure autonomie que ses prédécesseurs", "Niveaux de volume améliorés", "Facile à utiliser, avec ou sans application"],
    ["Pas d'égaliseur personnalisé", "Distorsion à fort volume"],
    ("IP67", "32 h"), "Marshall Emberton III",
    "B0DDCJMDJC", "Marshall Emberton III Enceintes Bluetooth Portables, sans Fil, IP67", 162.90,
    "Vous voulez une enceinte nomade au son abouti et à l'autonomie très longue, avec un design reconnaissable.",
    "Vous cherchez un égaliseur détaillé ou un budget serré.")

add("jbl-charge-6", ABT, "JBL Charge 6", "IP68 · 28 h · batterie externe", "Avec batterie externe",
    "Une enceinte puissante et bien équipée, très bien notée par la presse, qui sert aussi de batterie externe. Plus lourde que sa devancière et un peu terne à faible volume.",
    ["Volume élevé", "Audio sans perte via USB-C", "Son équilibré et expansif"],
    ["Son tiède à faible volume", "Aucun câble USB-C fourni", "Plus lourde que sa devancière"],
    ("IP68", "28 h"), "JBL Charge 6",
    "B0DXKNBQS6", "JBL Charge 6, Enceinte Bluetooth Portable sans Fil, Noir, IP68, 28 h, Auracast", 149.0,
    "Vous voulez une enceinte puissante pour la terrasse ou les sorties, qui recharge aussi votre téléphone.",
    "Vous écoutez surtout à faible volume ou cherchez un format très compact.")

add("jbl-flip-7", ABT, "JBL Flip 7", "IP68 · 16 h · Auracast", "Valeur sûre",
    "La petite enceinte JBL la plus répandue : un son percutant et détaillé pour sa taille et une construction robuste, mais des notes très dispersées selon les médias.",
    ["Son percutant et détaillé", "Grande autonomie", "Construction robuste"],
    ["Recharge lente", "Ne se couple pas avec les Flip précédents", "Disparition du mode PartyBoost"],
    ("IP68", "16 h"), "JBL Flip 7",
    "B0DXKMXPXW", "JBL Flip 7, Enceinte Bluetooth Portable sans Fil, Étanche, Noir", 109.0,
    "Vous voulez une enceinte nomade robuste, simple et bien diffusée, pour la plage ou les voyages.",
    "Vous voulez des graves profonds : le format limite l'extension dans les basses.")

add("sony-ult-field-1", ABT, "Sony ULT Field 1", "IP67 · 12 h · mode ULT", "Tout-terrain",
    "Une enceinte robuste au son charpenté et un mode ULT pensé pour l'extérieur, bien notée par la presse. Volume maximal limité et pas de multipoint.",
    ["Signature sonore charpentée", "Solide et étanche (IP67)", "Mode ULT adapté à l'extérieur"],
    ["Volume maximal limité", "Pas de Bluetooth multipoint", "Pas de radio FM ni de prise AUX"],
    ("IP67", "12 h"), "Sony ULT Field 1",
    "B0CX1WXP8M", "Sony ULT Field 1 - Enceinte Portable sans Fil Bluetooth ULT Power Sound, IP67", 79.0,
    "Vous voulez des basses marquées et une enceinte antichoc pour l'extérieur, à moins de 100 €.",
    "Vous cherchez une enceinte très puissante pour animer une soirée.")

add("jbl-go-5", ABT, "JBL Go 5", "Étanche · 10 h · Bluetooth 6.0", "Ultra-compacte",
    "La plus petite enceinte de la sélection : un son musical pour sa taille et un prix bas, mais des basses limitées par le format.",
    ["Audio USB-C sans perte", "Son musical pour sa taille", "Design ultra-portable"],
    ["Basses limitées", "Aucun câble USB-C fourni", "Autonomie battue par d'autres modèles"],
    ("Étanche", "10 h"), "JBL Go 5",
    "B0GPQ5H2LM", "JBL Go 5, Enceinte Bluetooth Ultra-Portable, Étanche, Bleu", 44.99,
    "Vous voulez une enceinte de poche pour le sac ou la douche, à petit prix.",
    "Vous attendez des basses profondes ou un grand volume.",
    ed=ed("enceinte-jbl-go-5-noir", "Enceinte Jbl Go 5 Noir", 49.99, "1200130034282", "10018105"))

add("sonos-roam-2", ABT, "Sonos Roam 2", "Étanche · Wi-Fi + Bluetooth · 10 h", "Wi-Fi et Bluetooth",
    "Une enceinte nomade qui devient une enceinte Wi-Fi à la maison, avec un son équilibré, mais une autonomie limitée et un prix élevé pour sa puissance.",
    ["Équilibre tonal convaincant", "Son sans perte en Wi-Fi", "Charge sans fil possible"],
    ["Autonomie limitée à 10 heures", "Assez chère pour sa puissance", "Stéréo seulement en Wi-Fi"],
    ("Étanche", "Wi-Fi + BT"), "Sonos Roam 2",
    "B0D37ZDYLH", "Sonos Roam 2 | Enceinte Nomade légère et étanche avec Bluetooth, Wi-Fi", 199.0,
    "Vous avez déjà ou voulez un système Sonos et une enceinte qui suit de la maison au jardin.",
    "Vous cherchez la plus longue autonomie ou le meilleur prix.")

add("bose-soundlink-flex-2", ABT, "Bose SoundLink Flex 2e gén.", "IP67 · 12 h", "Le son équilibré",
    "Une enceinte au son propre et équilibré, étanche IP67, mais très proche du modèle précédent et d'autonomie moyenne.",
    ["Audio propre et équilibré", "Étanche et résistante à la poussière (IP67)", "Égaliseur graphique dans l'application"],
    ["Autonomie moyenne", "Peu de changements par rapport au modèle précédent", "Son qui s'excite à fort volume"],
    ("IP67", "12 h"), "Bose SoundLink Flex 2",
    "B0D6WD2QSQ", "Bose SoundLink Flex (2e génération) Enceinte Bluetooth, Enceinte d'extérieur ultra-portable", 146.10,
    "Vous voulez un son propre et neutre dans une enceinte compacte et robuste.",
    "Vous possédez déjà la première génération.", seller="Nydolia")

add("ue-wonderboom-4", ABT, "UE Wonderboom 4", "Étanche · son 360° · flottante", "Flotte sur l'eau",
    "Une petite enceinte ludique au son à 360° qui flotte, robuste et dotée du multipoint. La presse regrette un lifting timide.",
    ["Robuste, étanche et ludique", "Boucle élastique, format ultra-portable", "Bluetooth multipoint"],
    ["Lifting timide par rapport à la génération précédente", "Pas d'égaliseur personnalisé", "Un test juge la Wonderboom 3 meilleure en rapport qualité-prix"],
    ("Étanche", "Son 360°"), "UE Wonderboom 4",
    "B0D3X3YKVF", "Ultimate Ears WONDERBOOM 4, enceinte Bluetooth portable et étanche", 74.72,
    "Vous voulez une enceinte de poche qui flotte et se fixe au sac, pour la plage ou la piscine.",
    "Vous attendez des progrès marqués par rapport à une Wonderboom 3.", seller="M.BUR")

add("jbl-grip", ABT, "JBL Grip", "IP68 · 14 h · éclairage d'ambiance", "Compacte et lumineuse",
    "Une enceinte compacte au design réussi et à l'éclairage d'ambiance, abordable, mais des notes très dispersées : le son est jugé énergique par certains, mince et brillant par d'autres.",
    ["Design réussi", "Éclairage d'ambiance", "Compatible Auracast"],
    ["Son brillant et mince selon certains tests", "Autonomie inférieure à l'annonce", "Beaucoup de concurrence à ce prix"],
    ("IP68", "14 h"), "JBL Grip",
    "B0FMGXH38Q", "JBL Grip, Enceinte Bluetooth compacte, Noir, IP68, 14 h", 69.0,
    "Vous voulez une enceinte compacte et décorative, pour moins de 80 €.",
    "Vous cherchez un son plein et des basses marquées.",
    ed=ed("enceinte-jbl-grip-noire", "Enceinte Jbl Grip Noire", 74.99, "1200130024849", "10013118"))

# --- Offre Electro Dépôt (flux Effinity du 28/10/2026) : un seul test noté à ce jour, signalé comme tel (exception Electro Dépôt) ---
add("jbl-go-essential-2", ABT, "JBL Go Essential 2", "IP68 · 5 h · Bluetooth 4.2", "Petit prix",
    "Le plus petit prix de la sélection (29 €) : une enceinte de poche étanche dont le seul test de presse, sévère, relève surtout un manque de basses. À prendre pour le prix.",
    ["Belle présence dans les médiums", "Abordable et compacte"],
    ["Gros manque de basses", "Volume modeste"],
    ("IP68", "5 h"), "JBL Go Essential 2",
    "B0DSG1NYJJ", "JBL GO Essential 2, Enceinte Bluetooth Portable, Noir, IP68, 5 h", 29.0,
    "Vous voulez une enceinte de dépannage ou un cadeau à moins de 30 €.",
    "Vous attendez de la puissance ou des basses.",
    ed=ed("enceinte-jbl-go-essential-2-noir", "Enceinte Jbl Go Essential 2 Noir", 29.0, "1200130018589", "10005191"))


# ============================================================ ÉCOUTEURS SANS FIL À RÉDUCTION DE BRUIT
# Prix Amazon relevés le 28/10/2026 dans le navigateur (vendu et expédié par Amazon) ; à renouveler par releve.py.
add("galaxy-buds4-pro", AANC, "Samsung Galaxy Buds4 Pro", "Double haut-parleur · 26 h avec boîtier", TOP,
    "Les mieux placés en rapport qualité/prix : un son généreux, une des meilleures réductions de bruit du moment et un prix déjà redescendu à 152 €. Les fonctions avancées sont surtout réservées aux téléphones Samsung.",
    ["ANC parmi les meilleures de la catégorie", "Son généreux, grave texturé et rapide", "Mode transparence très naturel"],
    ["Fonctions avancées réservées à l'écosystème Samsung", "Pas de LDAC ni d'aptX hors Samsung", "Maintien perfectible"],
    ("n.c.", "26 h"), "Samsung Galaxy Buds 4 Pro",
    "B0G59QG1TR", "Samsung Galaxy Buds4 Pro, Écouteurs Bluetooth sans Fil, Son Hi-FI de qualité Studio, Double Haut-Parleur", 152.0,
    "Vous avez un smartphone Samsung Galaxy et voulez un excellent son avec une très bonne réduction de bruit.",
    "Vous avez un iPhone ou un téléphone d'une autre marque : plusieurs fonctions sont perdues.")

add("airpods-pro-3", AANC, "Apple AirPods Pro 3", "IP57 · capteur cardiaque", "Pour iPhone",
    "La référence pour l'iPhone : réduction de bruit parmi les meilleures du marché, très bon confort et capteur de fréquence cardiaque, avec une autonomie en recul face à la génération précédente.",
    ["L'un des meilleurs ANC du marché", "Très bon confort, excellent maintien", "Kit mains-libres de haut vol"],
    ["Régression de l'autonomie totale", "Expérience tronquée sur Android", "Étui plus grand"],
    ("IP57", "Cardio"), "Apple AirPods Pro 3",
    "B0FQF32239", "Apple AirPods Pro 3 Écouteurs sans Fil, réduction Active du Bruit, détection de la fréquence Cardiaque", 209.0,
    "Vous utilisez un iPhone et voulez la meilleure intégration, avec un excellent kit mains-libres.",
    "Vous êtes sur Android : de nombreuses fonctions exigent un iPhone.")

add("bose-qc-ultra-earbuds-2", AANC, "Bose QuietComfort Ultra Earbuds (2e gén.)", "ANC référence · IPX4", "Meilleure note",
    "La meilleure note moyenne de la sélection : une réduction de bruit de premier plan, un son riche et un maintien exemplaire. Autonomie tout juste correcte et prix élevé.",
    ["Réduction de bruit très efficace", "Graves profonds, son riche et détaillé", "Maintien et confort exemplaires"],
    ["Autonomie tout juste correcte", "Parmi les plus chers", "Microphones perfectibles"],
    ("IPX4", "6 h"), "Bose QuietComfort Ultra 2",
    "B0F7M3HPBD", "Bose QuietComfort Ultra Écouteurs (2e génération), écouteurs sans Fil à réduction de Bruit, IPx4", 286.99,
    "Vous voulez la réduction de bruit la plus efficace, pour les transports ou l'open space.",
    "Vous cherchez une grande autonomie ou un budget serré.")

add("sony-wf-1000xm6", AANC, "Sony WF-1000XM6", "ANC premium · Hi-Res · IPX4", "Haut de gamme",
    "Le haut de gamme de Sony : un son naturel et détaillé, une réduction de bruit impressionnante et une bonne qualité d'appel. Le prix est élevé et l'étui encombrant.",
    ["Annulation de bruit exceptionnelle", "Son naturel et musical", "Confortable à porter"],
    ["Prix élevé", "Étui encombrant", "Mode adaptatif parfois capricieux"],
    ("IPX4", "24 h"), "Sony WF-1000XM6",
    "B0GF9ZNLWM", "Sony WF-1000XM6 Écouteurs sans Fil Premium avec réduction de Bruit ANC, Hi-Res, IPX4", 299.0,
    "Vous voulez un son très abouti et une réduction de bruit au sommet, sur iPhone comme sur Android.",
    "Vous cherchez de gros graves ou un étui compact.")

add("sennheiser-mtw5", AANC, "Sennheiser Momentum True Wireless 5", "aptX Lossless · batterie remplaçable", "Son audiophile",
    "Un son nuancé et équilibré, le Bluetooth 6.0 avec aptX Lossless et une batterie remplaçable par l'utilisateur. La réduction de bruit reste un cran derrière Apple, Sony et Bose, et le prix est élevé.",
    ["Son impressionnant, nuancé et équilibré", "Bluetooth 6.0, multipoint, aptX Lossless", "Batterie remplaçable"],
    ["ANC en retrait des leaders", "Qualité des appels moyenne", "Très cher"],
    ("n.c.", "40 h"), "Sennheiser Momentum True Wireless 5",
    "B0HC72BMGT", "Sennheiser Momentum True Wireless 5 écouteurs Bluetooth, Batterie 40h, ANC", 299.0,
    "Vous privilégiez la qualité sonore et les codecs haute résolution.",
    "Vous voulez la meilleure réduction de bruit ou un petit prix.")

add("pixel-buds-pro-2", AANC, "Google Pixel Buds Pro 2", "Gemini · 12 h", "Pour Pixel",
    "Légers, très confortables et bien intégrés à Android avec Gemini : un son agréable et une réduction de bruit enfin au niveau de la concurrence, mais sans codecs haute qualité.",
    ["Mode transparence cristallin", "Très confortables, design compact", "Autonomie jusqu'à 12 heures"],
    ["Pas de codecs Bluetooth haute qualité", "ANC en retrait de Bose", "Micros perfectibles"],
    ("n.c.", "12 h"), "Google Pixel Buds Pro 2",
    "B0FJGBYK8B", "Google Pixel Buds Pro 2 – Écouteurs sans Fil avec Suppression Active du Bruit – Quartz Gris", 197.42,
    "Vous êtes sur Android, de préférence un Pixel, et voulez des écouteurs légers pour la journée.",
    "Vous cherchez des codecs haute résolution ou le meilleur ANC.")

add("airpods-4-anc", AANC, "Apple AirPods 4 (ANC)", "Réduction active · sans embouts", "Sans embouts",
    "Les AirPods à réduction de bruit sans embouts : un son plutôt riche, une ANC valable et une très bonne intégration à l'iPhone. Autonomie moyenne et fonctions limitées hors Apple.",
    ["Performances acoustiques", "Réduction de bruit active valable", "Mode transparence très naturel"],
    ["Autonomie correcte sans plus", "Limitations hors appareils Apple", "Pas de multipoint approprié"],
    ("IP54", "ANC"), "Apple AirPods 4",
    "B0DGHYDYJL", "Apple AirPods 4 Écouteurs sans Fil, écouteurs Bluetooth, avec Réduction Active du Bruit", 134.0,
    "Vous avez un iPhone et préférez des écouteurs sans embouts en silicone.",
    "Vous voulez une isolation passive forte ou vous êtes sur Android.")

add("sony-wf-c710n", AANC, "Sony WF-C710N", "ANC · 40 h · IPX4", "Autonomie",
    "Une réduction de bruit efficace pour le prix, un son agréable et une grande autonomie. Peu de codecs compatibles et une application un peu compliquée.",
    ["Annulation de bruit efficace", "Excellente autonomie", "Ajustement confortable"],
    ["Peu de codecs compatibles", "Pas de recharge sans fil", "Commandes tactiles confuses"],
    ("IPX4", "40 h"), "Sony WF-C710N",
    "B0FDBD6WQ3", "Sony WF-C710N Écouteurs sans Fil avec réduction de Bruit Active, IPX4, autonomie 40h", 99.0,
    "Vous voulez de la réduction de bruit sous les 100 € et une grosse autonomie.",
    "Vous attendez un son haut de gamme ou la recharge sans fil.")

add("nothing-ear-3a", AANC, "Nothing Ear (3a)", "Bluetooth 6.0 · LDAC · multipoint", "Petit prix",
    "Un excellent rapport fonctionnalités/prix : LDAC, Bluetooth 6.0, multipoint, un son équilibré et une bonne autonomie. La réduction de bruit est un cran sous le haut de gamme.",
    ["Bluetooth 6.0, LDAC, multipoint", "Signature sonore équilibrée", "Excellente autonomie"],
    ["ANC en retrait des références", "Coque qui fait un peu cheap", "Fonctions complètes avec un téléphone Nothing"],
    ("n.c.", "LDAC"), "Nothing Ear 3a",
    "B0GZW9B97V", "Nothing Ear (3a) – Écouteurs sans Fil avec ANC Jusqu'à 45 DB, Hi-Res Audio, double connexion Bluetooth", 99.95,
    "Vous voulez des écouteurs complets pour 100 €, avec LDAC et multipoint.",
    "Vous cherchez la meilleure réduction de bruit.")

add("cmf-buds-pro-2", AANC, "CMF Buds Pro 2", "ANC 50 dB · égaliseur · 64,95 €", "Le moins cher",
    "Le plus petit prix de la sélection : une bonne réduction de bruit, un égaliseur personnalisable et une autonomie solide. Basses marquées par défaut et matériaux simples.",
    ["Très bonne réduction de bruit pour le prix", "Égaliseur personnalisable", "Autonomie solide"],
    ["Son déséquilibré par défaut", "Pas de vrai multipoint", "Matériaux bon marché"],
    ("n.c.", "ANC 50 dB"), "Nothing CMF Buds Pro 2",
    "B0F5B56X84", "CMF by Nothing Buds Pro 2 Écouteurs sans Fil avec Son Hi-FI, 50 DB Suppression Active du Bruit Hybride", 64.95,
    "Vous voulez de l'ANC pour moins de 70 €.",
    "Vous cherchez un son très travaillé ou un étui premium.")


def build():
    return dict(AUD)
