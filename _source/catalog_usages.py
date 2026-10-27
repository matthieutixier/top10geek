# -*- coding: utf-8 -*-
"""Catalogue Top 10 Geek — ROBOTS & ASPIRATEURS · usages « Aspirateurs balais », « Balais laveurs » et « Animaux » (27/10/2026).
Les tests de la presse viennent de CommentChoisir (cc_fiche.py), conservés dans data/cc_fiches_usages.json : une ligne par média
(moyenne si plusieurs tests du même média). La confirmation à la source (champ `verifie`) reste à faire.
Prix : indicatifs (idealo, 27/10/2026) → PROVISOIRES, à remplacer par le relevé Amazon (releve.py) ; les prix Electro Dépôt viennent du flux Effinity.
Les points forts / faibles reprennent ce que citent les tests ; rien n'est ajouté.
Pas encore d'usage « Petit prix » : sous 300 € il n'y a pas assez de robots avec des tests notés (voir LISEZMOI)."""
import json, os, re
from catalog_sols import S, TOP

_HERE = os.path.dirname(os.path.abspath(__file__))
_ED = "https://track.effiliation.com/servlet/effi.redir?id_compteur=23321274&url="


def _ed_url(u):
    from urllib.parse import quote
    return _ED + quote(u, safe="")


def notes_cc(fiche):
    """[(média, note /10 ou None, url)] — une ligne par média, les mieux notés d'abord."""
    brut = json.load(open(os.path.join(_HERE, "data", "cc_fiches_usages.json"), encoding="utf-8"))[fiche]["tests"]
    par = {}
    for t in brut:
        m = t["media"].replace("\x92", "’").strip()
        par.setdefault(m, dict(notes=[], url=t["url"]))
        if t["note10"] is not None:
            par[m]["notes"].append(t["note10"])
    out = [(m, round(sum(v["notes"]) / len(v["notes"]), 1) if v["notes"] else None, v["url"]) for m, v in par.items()]
    out.sort(key=lambda x: (x[1] is None, -(x[1] or 0), x[0].lower()))
    return out


BAL, LAV, ANI = "s-aspirateur-balai", "s-aspirateur-laveur", "s-robot-animaux"
U = {}


def add(pid, cat, short, ref, badge, verdict, strengths, weak, m, fiche, asin, amz, price, pour, eviter, scope="modele", ed=None):
    U[pid] = S(cat, short, ref, badge, verdict, strengths, weak, m, notes_cc(fiche), asin, amz, price, pour, eviter, scope=scope, ed=ed)


# ============================================================ ASPIRATEURS BALAIS (secs)
add("dyson-v11-absolute", BAL, "Dyson V11 Absolute", "Puissance auto · écran de suivi", TOP,
    "Le balai le mieux noté de la sélection : aspiration très puissante, écran d'autonomie et puissance qui s'ajuste seule.",
    ["Aspiration très puissante", "Puissance ajustée automatiquement selon le sol", "Écran d'autonomie restante"],
    ["Une seule batterie", "Prix élevé", "Ne se charge pas pendant l'utilisation"],
    ("Puissance auto", "Sans station"), "Dyson V11 Absolute",
    "B07Q4FZKNY", "Dyson V11 Absolute aspirateur balai sans fil", 428.99,  # PROVISOIRE (idealo « V11 », 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez un balai très bien noté dont la puissance s'adapte seule au sol.",
    "Vous voulez un modèle récent : les tests portent sur un modèle de 2019 encore commercialisé.", scope="gamme")

add("dyson-v15-detect-absolute", BAL, "Dyson V15 Detect Absolute", "Capteur de poussière · laser", "Le haut de gamme",
    "Le plus complet des Dyson testés : brosse anti-enchevêtrement et capteurs de poussière très appréciés, mais tarif très élevé.",
    ["Brosse anti-enchevêtrement efficace sur les poils d'animaux", "Capteurs acoustique et laser de détection de poussière", "Plus de puissance et meilleure autonomie"],
    ["Prix très élevé", "Capteurs jugés excessifs par certains testeurs"],
    ("Capteur de poussière", "Sans station"), "Dyson V15 Detect Absolute",
    "B099NLCLZH", "Dyson V15 Detect Absolute aspirateur balai sans fil", 579.0,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez le balai le plus abouti et acceptez un prix premium.",
    "Vous cherchez un modèle à petit prix.", scope="gamme")

add("dyson-v12-detect-slim", BAL, "Dyson V12 Detect Slim", "150 AW · laser · léger", "Le plus léger",
    "Un Dyson léger et puissant, plus compact que le V15, mais cher et avec moins de capacité.",
    ["Léger", "Aspiration puissante", "Brosse à éclairage intégré"],
    ["Prix élevé", "Capacité et aspiration inférieures à celles du V15"],
    ("150 AW", "Sans station"), "Dyson V12 Detect Slim",
    "B0BSHHKLFJ", "Dyson V12 Detect Slim Absolute aspirateur balai sans fil", 649.0,  # PROVISOIRE (idealo, modèle 2022, 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez un Dyson léger, facile à manier.",
    "Vous avez un grand logement et voulez une grande capacité de bac.", scope="gamme")

add("dyson-v16-piston-animal", BAL, "Dyson V16 Piston Animal", "315 AW · ajustement auto", "Le plus récent",
    "Un Dyson récent à l'aspiration très puissante, mais plus mitigé que ses aînés sur certains points.",
    ["Puissance d'aspiration impressionnante", "Ajustement automatique de la puissance", "Très bien conçu"],
    ["Prix élevé", "Ne tient pas debout tout seul", "Mécanisme d'essuyage automatique décevant"],
    ("315 AW", "Sans station"), "Dyson V16 Piston Animal",
    "B0FZN79QDP", "Dyson V16 Piston Animal aspirateur balai sans fil", 750.0,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez le dernier Dyson et une grande puissance d'aspiration.",
    "Vous attendez un balai qui tient debout seul ou un tarif contenu.")

add("samsung-bespoke-jet", BAL, "Samsung Bespoke Jet", "Station de vidage CleanStation", "La station ingénieuse",
    "Un balai Samsung à station de vidage ingénieuse et forte aspiration ; cher.",
    ["Station d'extraction ingénieuse", "Forte puissance d'aspiration", "Bonne prise en main"],
    ["Prix élevé", "La seconde batterie ne se charge pas sur la station", "Accès au filtre HEPA peu pratique"],
    ("Forte aspiration", "Station de vidage"), "Samsung Bespoke Jet",
    "B09WVQG81R", "Samsung Bespoke Jet VS20A95973B aspirateur balai sans fil", 742.9,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez ne plus toucher à la poussière : la station vide le bac toute seule.",
    "Vous comptez utiliser deux batteries en alternance sans changer de station.")

add("samsung-jet-90", BAL, "Samsung Jet 90", "200 AW · station de charge", "Le polyvalent",
    "Un balai léger et polyvalent, avec station de charge, mais cher pour un modèle ancien et sans lavage.",
    ["Filtre HEPA qui retient les poussières fines", "Nombreux accessoires", "Construction légère"],
    ["Brosse qui peut s'emmêler avec les cheveux", "Recharge de 3 h 30", "Pas de nettoyage humide"],
    ("200 AW", "Station de charge"), "Samsung Jet 90",
    "B09CNDT1C2", "Samsung Jet 90 Complete VS20R9046T3 aspirateur balai sans fil", 490.0,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez un balai léger avec beaucoup d'accessoires.",
    "Vous avez de longs cheveux à aspirer ou voulez laver vos sols.", scope="gamme")

add("dreame-z30", BAL, "Dreame Z30", "310 AW · batterie amovible", "Le plus accessible",
    "Un balai Dreame à prix modéré, avec batterie amovible et beaucoup d'accessoires ; lourd et au réservoir un peu petit.",
    ["Batterie amovible", "Prix modéré", "Nombreux accessoires"],
    ["Réservoir un peu petit", "Corps lourd et peu maniable", "Finition en plastique"],
    ("310 AW", "Sans station"), "Dreame Z30",
    "B0DFXS37KW", "Dreame Z30 aspirateur balai sans fil 310 AW", 293.0,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez un balai puissant à un prix modéré, avec une batterie qu'on change.",
    "Vous avez un grand logement ou un poignet fragile : le corps est lourd.")

add("dreame-r20", BAL, "Dreame R20", "190 AW · LED", "Le petit prix endurant",
    "Un balai endurant à bonne aspiration pour un prix contenu ; bac à poussière petit.",
    ["Bonnes performances d'aspiration", "Aspiration continue ou fractionnée au choix", "Très endurant en mode auto"],
    ["Tête à choisir selon la surface", "Brosse dure qui repousse les détritus vers l'arrière", "Bac à poussière de 0,6 L"],
    ("190 AW", "Sans station"), "Dreame R20",
    "B0C5MDCNLZ", "Dreame R20 aspirateur balai sans fil 190 AW", 209.0,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez un balai endurant sous les 250 €.",
    "Vous avez un grand logement : le bac est petit.")

_ed_h60 = {"url": _ed_url("https://www.electrodepot.fr/aspirateur-balai-roborock-h60-hub-station-de-vidage.html"),
           "name": "Aspirateur Balai Roborock H60 Hub Station De Vidage", "price": 149.98, "ean": "6974653813628", "edid": "10020540"}
add("roborock-h60-hub", BAL, "Roborock H60 Hub", "Base de vidage automatique", "Le moins cher",
    "Un balai d'entrée de gamme avec base de vidage automatique rapide, jugé moins convaincant que les modèles du dessus.",
    ["Base de vidage automatique rapide (10 secondes)", "Bonne autonomie, batterie modulaire", "Très bon sur sol dur au niveau maximal"],
    ["Base encombrante", "Sachets de rechange à acheter", "Une seule batterie incluse"],
    ("Aspiration sols durs", "Vidage auto"), "Roborock H60 Hub",
    None, None, None,
    "Vous voulez une base qui vide le bac toute seule pour 150 €.",
    "Vous avez des tapis épais ou un grand logement.", ed=_ed_h60)


_ed_rowenta = {"url": _ed_url("https://www.electrodepot.fr/aspirateur-balai-rowenta-14-60-yy5640fe-x-force-flex-auto.html"),
               "name": "Aspirateur Balai Rowenta 14.60 Yy5640fe X Force Flex Auto", "price": 295.0, "ean": "3700342483376", "edid": "10009171"}
add("rowenta-x-force-flex-14-60", BAL, "Rowenta X-Force Flex 14.60", "Fabriqué en France · réparable", "Le made in France",
    "Un balai Rowenta fabriqué en France et réparable, mais très peu testé par la presse : les tests suivis portent sur le modèle voisin 14.80.",
    ["Fabriqué en France et réparable", "LED sur la tête motorisée", "Bonne autonomie"],
    ["Pas de base de vidange"],
    ("Fabriqué en France", "Sans station"), "Rowenta X-Force Flex 14.80",
    None, None, None,
    "Vous voulez un balai français, réparable, vendu en magasin.",
    "Vous voulez un modèle largement testé : les tests suivis portent sur le 14.80.", scope="gamme", ed=_ed_rowenta)

# ============================================================ BALAIS LAVEURS
_ed_h15 = {"url": _ed_url("https://www.electrodepot.fr/nettoyeur-de-sols-dreame-h15-pro.html"),
           "name": "Aspirateur Laveur Dreame H15 Pro", "price": 339.0, "ean": "6977328063854", "edid": "10009023"}
add("dreame-h15-pro", LAV, "Dreame H15 Pro", "21 000 Pa · eau chaude", TOP,
    "Le balai laveur le plus testé : aspiration puissante, lavage à l'eau chaude et taches vite effacées ; prix élevé.",
    ["Aspiration puissante, lavage à l'eau chaude très efficace", "Mode automatique", "Conception à plat"],
    ["Prix élevé", "Application nécessaire pour toutes les fonctions", "Pas de LED à l'avant"],
    ("21 000 Pa", "Autonettoyant"), "Dreame H15 Pro",
    "B0DT9Y8RWH", "Dreame H15 Pro aspirateur laveur sans fil", 343.22,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez le balai laveur le plus éprouvé par la presse.",
    "Vous voulez un modèle à moins de 250 €.", ed=_ed_h15)

add("dreame-h12-pro", LAV, "Dreame H12 Pro", "Rouleau bord à bord · séchage", "Le mieux noté",
    "Le balai laveur le mieux noté et l'un des moins chers : nettoyage intelligent bord à bord et séchage de la brosse ; lourd.",
    ["Rouleau bord à bord", "Autonettoyage et séchage de la brosse", "Mode électrolyse pour la désinfection"],
    ["Recharge un peu longue", "Appareil lourd et peu maniable", "Tête de lavage imposante"],
    ("Bord à bord", "Séchage air chaud"), "Dreame H12 Pro",
    "B0BJVN2LH7", "Dreame H12 Pro aspirateur laveur sans fil", 189.0,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez un balai laveur bien noté à moins de 200 €.",
    "Vous avez du mal à porter un appareil lourd.")

_ed_h14 = {"url": _ed_url("https://www.electrodepot.fr/nettoyeur-de-sols-dreame-h14.html"),
           "name": "Aspirateur Laveur Dreame H14", "price": 229.0, "ean": "6976233676067", "edid": "10019413"}
add("dreame-h14", LAV, "Dreame H14", "Pose à plat 180°", "Le bon compromis",
    "Un balai laveur Dreame abordable, très bon nettoyage et pose à plat, mais autonomie limitée.",
    ["Excellentes performances de nettoyage", "Se couche à 180° sous les meubles", "Intégration à l'application"],
    ["Autonomie limitée", "Poids conséquent", "Tarif jugé élevé par certains"],
    ("Pose à plat 180°", "Autonettoyant"), "Dreame H14",
    None, None, None,
    "Vous voulez nettoyer sous les meubles bas pour environ 230 €.",
    "Vous avez un grand logement : l'autonomie est limitée.", ed=_ed_h14)

add("tineco-floor-one-s7-pro", LAV, "Tineco Floor One S7 Pro", "Auto-propulsion", "L'auto-propulsé",
    "Un balai laveur à auto-propulsion qui rend le nettoyage sans effort ; petit réservoir et autonomie courte.",
    ["Forte aspiration et lavage à la serpillière", "Auto-propulsion, nettoyage sans effort", "Plusieurs modes selon l'usage"],
    ["Réservoir d'eau de 0,85 L", "Réservoir d'eau sale à vider et rincer après chaque usage", "Autonomie de 40 minutes"],
    ("Auto-propulsion", "Autonettoyant"), "Tineco Floor One S7 Pro",
    "B088H28VPM", "Tineco Floor One S7 Pro aspirateur laveur sans fil", 249.99,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez un balai laveur qui avance seul.",
    "Vous avez une grande surface à laver d'une seule charge.")

add("tineco-floor-one-s9-artist", LAV, "Tineco Floor One S9 Artist", "22 000 Pa · design", "Le plus élégant",
    "Un balai laveur à très bonne aspiration et entretien facile, mais au prix très élevé.",
    ["Design élégant", "Très bonne aspiration et très bon nettoyage", "Entretien facile"],
    ["Prix très élevé", "Un peu lourd à la longue", "Bouton de réglage au fonctionnement confus"],
    ("22 000 Pa", "Autonettoyant"), "Tineco Floor One S9 Artist",
    "B0DPP6C5YP", "Tineco Floor One S9 Artist aspirateur laveur sans fil", 429.99,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez un balai laveur élégant, au nettoyage très abouti.",
    "Vous cherchez un modèle sous 300 €.")

add("mova-m50-ultra", LAV, "Mova M50 Ultra", "Manche pliable · station séchage", "Le manche pliable",
    "Un balai laveur à manche pliable et extensible, aspiration puissante et station à séchage rapide ; moins testé.",
    ["Manche pliable et extensible inédit", "Aspiration puissante, lavage efficace", "Station d'accueil avec séchage rapide"],
    ["Pas de lavage du sol à l'eau chaude", "Niveau sonore perfectible", "Pas de phare LED"],
    ("22 000 Pa", "Station séchage"), "Mova M50 Ultra",
    "B0FM3HH8NG", "Mova M50 Ultra aspirateur laveur sans fil", 322.0,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous rangez l'appareil dans un petit espace : le manche se plie.",
    "Vous voulez un lavage du sol à l'eau chaude.")

# ============================================================ ROBOTS ANIMAUX
add("roborock-s8-maxv-ultra", ANI, "Roborock S8 MaxV Ultra", "10 000 Pa · station 8 en 1", TOP,
    "Le robot le mieux noté de la sélection : aspiration quasi parfaite et station multifonction compacte ; prix élevé.",
    ["Aspiration puissante", "Station multifonction compacte avec réservoir de produit nettoyant", "Puissance d'aspiration quasi parfaite"],
    ["Prix élevé, jugé justifié", "Progrès à faire dans les coins", "Détecte mal les petits obstacles"],
    ("10 000 Pa", "Station 8 en 1"), "Roborock S8 MaxV Ultra",
    "B0CRV7F37B", "Roborock S8 MaxV Ultra robot aspirateur laveur", 1299.0,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez le robot le plus complet et le mieux testé de la sélection.",
    "Vous cherchez un robot à moins de 800 €.")

add("dreame-l20-ultra", ANI, "Dreame L20 Ultra", "7 000 Pa · retrait des patins", "Le meilleur rapport",
    "Un robot à navigation efficace et excellente aspiration, qui relève ses patins sur les tapis ; encombrant.",
    ["Navigation efficace", "À l'aise dans les environnements encombrés", "Retrait automatique des patins sur les tapis"],
    ["Encombrement conséquent", "Voit parfois des obstacles inexistants", "Filtre HEPA à nettoyer régulièrement"],
    ("7 000 Pa", "Station Ultra"), "Dreame L20 Ultra",
    "B0CF1R9BCQ", "Dreame L20 Ultra robot aspirateur laveur", 689.0,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous avez des tapis et un intérieur encombré.",
    "Vous manquez de place pour la station.")

add("roborock-qrevo-maxv", ANI, "Roborock Qrevo MaxV", "Station complète · détection d'obstacles", "Le plus abordable",
    "Un robot bien noté dont l'entretien est automatisé, avec une application très complète ; station imposante.",
    ["Principales tâches d'entretien automatisées", "Application très complète", "Détection d'obstacles efficace"],
    ["Station imposante", "Aspiration moins efficace sur tapis à poils longs", "Plusieurs passages pour les taches incrustées"],
    ("Détection d'obstacles", "Station complète"), "Roborock QRevo MaxV",
    "B0CZH7B4QX", "Roborock Qrevo MaxV robot aspirateur laveur", 609.0,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez un robot bien noté à moins de 700 €.",
    "Vous avez des tapis à poils longs.")

add("mova-v70-ultra", ANI, "Mova V70 Ultra", "Vadrouille extensible · marches 4,5 cm", "Le franchisseur",
    "Un robot à vadrouille extensible et franchissement de marches, station sans sac ; prix élevé.",
    ["Vadrouille extensible qui atteint 16 cm sous les meubles", "Franchit des marches jusqu'à 4,5 cm (9 cm en transitions composées)", "Station sans sac, bac à poussière lavable"],
    ["Prix élevé", "Petit rouleau avant qui ramasse encore des poils", "Détection d'obstacles prise en défaut sur un support plat"],
    ("40 000 Pa", "Station sans sac"), "Mova V70 Ultra",
    "B0GXW3NHKY", "Mova V70 Ultra Complete robot aspirateur laveur", 948.0,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous avez des seuils ou des marches à franchir.",
    "Vous voulez un robot à moins de 800 €.", scope="gamme")

add("dji-romo-p2", ANI, "DJI Romo P2", "36 000 Pa · jambes robotisées", "Le plus innovant",
    "Un robot très bien noté, qui franchit des obstacles de 8,5 cm et lave sous les meubles ; tarif premium.",
    ["Cartographie et évitement d'obstacles de très haut niveau", "Franchit jusqu'à 8,5 cm", "Bras oscillant qui lave sous les meubles et le long des plinthes"],
    ["Tarif premium", "Design transparent qui ne fera pas l'unanimité", "Assistant vocal indisponible dans certains pays au lancement"],
    ("36 000 Pa", "Station complète"), "DJI Romo P2",
    "B0H8DJ99LD", "DJI ROMO P2 robot aspirateur laveur", 1199.0,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez la navigation la plus avancée du moment.",
    "Vous cherchez un robot à moins de 1 000 €.")

add("narwal-flow-2", ANI, "Narwal Flow 2", "31 000 Pa · rouleaux de lavage", "Le lavage par rouleau",
    "Un robot à très forte aspiration et rouleaux de lavage à la place des tampons ; auto-nettoyage de la base perfectible.",
    ["31 000 Pa de puissance d'aspiration", "Rouleaux de lavage à la place des tampons", "Détection d'obstacles Narmind 2.0"],
    ["Brosse latérale non rétractable", "Auto-nettoyage de la base jugé insuffisant", "Franchissement de seuils élevés limité"],
    ("31 000 Pa", "Station FlowWash"), "Narwal Flow 2",
    "B0GRHDJBQ6", "Narwal Flow 2 robot aspirateur laveur", 1038.05,  # PROVISOIRE (idealo, 27/10/2026) ; prix à relever (releve.py)
    "Vous voulez une très forte aspiration et un lavage par rouleau.",
    "Vous avez des seuils hauts à franchir.")


def build():
    return dict(U)
