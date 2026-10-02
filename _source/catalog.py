# -*- coding: utf-8 -*-
"""Catalogue Top 10 Geek — relevé du 02/10/2026.
100 ordinateurs (50 PC portables, 50 ordinateurs de bureau). Chaque machine est :
  - disponible chez au moins un marchand partenaire (Amazon, Darty, Fnac, Acer Store, Geekom) ;
  - couverte par au moins un test de la presse.
Champs : cat, short (nom lisible), ref (configuration de référence), badge, verdict, strengths, weak, m (2 mesures),
press (voir build_data.py), et les clés d'offres marchands sont dans offers_*.json (même identifiant)."""

TOP = "Le choix de la bande"


def cc(name, since="2025-01-01", inc=None, exc=None, scope="modele"):
    return dict(kind="cc", name=name, since=since, inc=inc, exc=exc, scope=scope)


def man(notes, scope="modele"):
    """notes : liste (média, note sur 10 ou None, url)"""
    return dict(kind="manual", notes=notes, scope=scope)


def P(cat, short, ref, badge, verdict, strengths, weak, m, *press):
    return dict(cat=cat, short=short, ref=ref, badge=badge, verdict=verdict, strengths=strengths, weak=weak, m=m, press=list(press))


CAT = {}

# =====================================================================================================================
#                                                   PC PORTABLES
# =====================================================================================================================
# ---------------------------------------------------------------- Bureautique & mobilité
CAT["zenbook-a14"] = P("bureau", "Asus Zenbook A14", "UX3407QA · Snapdragon X · 16 Go · OLED 14\"", TOP,
    "Moins d'un kilo, un écran OLED et une autonomie qui dépasse largement la journée : l'ultraportable le plus facile à recommander pour travailler partout.",
    ["0,98 kg seulement", "Autonomie de plus d'une journée", "Écran OLED 14\""],
    ["Puce Snapdragon X d'entrée de gamme : performances modestes", "Quelques logiciels Windows encore mal adaptés à ARM"],
    ("0,98 kg", "32 h (vidéo, annoncée)"), cc("Asus+_Zenbook+A14"))
CAT["mba13-m5"] = P("bureau", "Apple MacBook Air 13\" M5", "Puce M5 · 16 Go · 512 Go", "La valeur sûre",
    "Silencieux, rapide et endurant : la puce M5 et le SSD plus véloce en font la référence des ultraportables, si l'écran 60 Hz ne vous gêne pas.",
    ["Totalement silencieux (sans ventilateur)", "Puce M5 très rapide, Wi-Fi 7", "512 Go de stockage dès l'entrée de gamme"],
    ["Écran toujours limité à 60 Hz, pas d'OLED", "RAM et SSD non évolutifs"],
    ("1,24 kg", "≈ 12 h (tests)"), cc("Apple_MacBook+Air+M5", "2026-01-01", exc=r"air-15|air 15"))
CAT["macbook-neo"] = P("bureau", "Apple MacBook Neo", "13\" · puce A18 Pro · 8 Go · 256 Go", "Le Mac à petit prix",
    "Le Mac le moins cher jamais lancé : finition aluminium et puce A18 Pro parfaites pour le quotidien, mais 8 Go de RAM et des économies visibles.",
    ["Prix très bas pour un Mac", "Finition aluminium irréprochable", "Puce A18 Pro fluide au quotidien"],
    ["8 Go de RAM et 256 Go sur le modèle de base", "Clavier non rétroéclairé, Touch ID réservé au modèle 512 Go", "Batterie de capacité limitée"],
    ("n.c.", "n.c."), cc("Apple_MacBook+Neo", "2026-01-01"))
CAT["surface-pro-12"] = P("bureau", "Microsoft Surface Pro 12\"", "Snapdragon X Plus · 16 Go · 256 Go · tablette 12\"", "Le plus mobile",
    "Une tablette Windows de 686 g, silencieuse et endurante. La presse est partagée : clavier vendu à part et connectique réduite au strict minimum.",
    ["686 g en tablette seule", "Silencieuse, ne chauffe pas", "Bonne autonomie"],
    ["Clavier (et chargeur) vendus séparément", "Deux ports USB-C seulement", "Écran LCD 90 Hz perfectible"],
    ("0,69 kg (tablette)", "16 h (annoncée)"), cc("Microsoft_Surface+Pro+12", "2025-04-01"))
CAT["surface-laptop-13"] = P("bureau", "Microsoft Surface Laptop 13\"", "Snapdragon X Plus · 16 Go · 256 Go", "Le plus soigné",
    "Petit, léger, très bien fini et toujours silencieux : un compagnon de travail agréable, mais vendu un peu cher pour son écran LCD.",
    ["Châssis compact et très bien fini", "Clavier et pavé tactile confortables", "Ne chauffe pas, ne fait pas de bruit"],
    ["Connectique légère", "Écran LCD réfléchissant, pas d'OLED", "Prix un peu élevé"],
    ("1,22 kg", "n.c."), cc("Microsoft_Surface+Laptop+13", "2025-04-01"))
CAT["zenbook-a16"] = P("bureau", "Asus Zenbook A16", "UX3607 · Snapdragon X · OLED 16\"", "Le grand écran poids plume",
    "Un 16 pouces OLED de 1,2 kg à l'autonomie remarquable : idéal pour travailler confortablement sans s'alourdir. Les versions X2 Elite sont nettement plus chères.",
    ["Châssis ultraléger pour un 16\" (1,2 kg)", "Autonomie remarquable", "Belle dalle OLED"],
    ["Dalle brillante", "Pas de pavé numérique", "Versions haut de gamme très chères"],
    ("≈ 1,2 kg", "n.c."), cc("Asus+_Zenbook+A16"))
CAT["omnibook5-14"] = P("bureau", "HP OmniBook 5 14", "14-he · Snapdragon X · 16 Go · OLED 14\"", "Le marathonien",
    "Une autonomie de plusieurs jours et un écran OLED dans un châssis métal sobre : très bon en bureautique, limité dès qu'on lui demande de la puissance.",
    ["Autonomie impressionnante", "Dalle OLED", "Châssis métallique de qualité"],
    ["Partie graphique très juste", "Écran très brillant", "Peu de ports"],
    ("≈ 1,3 kg", "n.c."), cc("HP_OmniBook+5+14"))
CAT["ideapad-slim3x"] = P("bureau", "Lenovo IdeaPad Slim 3x 15", "15Q8X10 · Snapdragon X · 16 Go", "Le silencieux abordable",
    "Un 15 pouces qui ne chauffe pas, ne fait pas de bruit et tient très longtemps : bon choix pour la bureautique, avec un écran simplement correct.",
    ["Excellente autonomie", "Ni bruit ni chauffe", "16 Go de RAM de série"],
    ["Écran loin du haut de gamme", "Performances limitées hors bureautique"],
    ("1,6 kg", "n.c."), cc("Lenovo_Ideapad+Slim+3x"))
CAT["galaxy-book4-edge"] = P("bureau", "Samsung Galaxy Book4 Edge 15", "15,6\" · Snapdragon X · 16 Go · 512 Go", "L'allié des smartphones Galaxy",
    "Fin, endurant et bien intégré à l'écosystème Samsung. Un bon PC de travail, à choisir surtout si vous avez déjà un téléphone Galaxy.",
    ["Très bonne autonomie", "Châssis fin et bien fini", "Synergies avec les appareils Galaxy"],
    ["RAM et SSD non évolutifs", "Compatibilité logicielle ARM à vérifier", "Écran LCD sur le 15,6\""],
    ("≈ 1,5 kg", "27 h (annoncée)"), cc("Samsung_Galaxy+Book4+Edge", "2024-05-01", scope="gamme"))
CAT["swift-air-14"] = P("bureau", "Acer Swift Air 14", "SFA14 · 14\" 120 Hz antireflet", "Le poids plume étudiant",
    "Compact, léger et doté d'un écran 120 Hz antireflet : tout ce qu'il faut pour un étudiant, avec une puissance et une luminosité limitées.",
    ["Format compact et léger", "Écran 120 Hz antireflet", "Clavier rétroéclairé, Windows Hello"],
    ["Luminosité limitée", "Puissance modeste", "Châssis un peu souple"],
    ("n.c.", "n.c."), cc("Acer_Swift+Air+14"))

# ---------------------------------------------------------------- Création & photo
CAT["mbp14-m5"] = P("creation", "Apple MacBook Pro 14\" M5", "Puce M5 · 16 Go · 1 To · mini-LED", TOP,
    "Écran mini-LED parfaitement calibré, puce M5 polyvalente et connectique complète : la presse lui donne les meilleures notes de la catégorie.",
    ["Écran mini-LED très bien calibré", "Puce M5 rapide et sobre", "Connectique complète (HDMI, SD, MagSafe)"],
    ["RAM et SSD non évolutifs", "Ventilation audible en charge soutenue", "Encoche toujours présente"],
    ("1,55 kg", "24 h (annoncée)"), cc("Apple_MacBook+Pro+14+M5", "2025-09-01"))
CAT["xps14"] = P("creation", "Dell XPS 14 (2026)", "Core Ultra X7 · 32 Go · OLED ou LCD", "Le retour gagnant",
    "Nouveau châssis très réussi, superbe écran et excellente autonomie : l'ultraportable premium de l'année, vendu au prix fort.",
    ["Design et finition irréprochables", "Magnifique écran, bon son", "Excellente autonomie"],
    ["Prix très élevé", "Uniquement des ports USB-C", "Processeur en retrait en multicœur"],
    ("1,36 kg", "12 à 17 h (test Clubic)"), cc("Dell_XPS+14", "2026-01-01"))
CAT["proart-p16"] = P("creation", "Asus ProArt P16", "H7606 · Ryzen AI 9 · RTX · OLED 16\" tactile", "La station des créatifs",
    "Écran OLED tactile calibré, molette DialPad et carte graphique RTX : une vraie station de création mobile, lourde sur le budget.",
    ["Écran OLED tactile très fidèle", "Carte graphique RTX dédiée", "DialPad et lecteur de cartes SD"],
    ["Prix très élevé", "Dalle brillante"],
    ("1,85 kg", "n.c."), cc("Asus+_ProArt+P16", "2024-06-01", scope="gamme"))
CAT["proart-px13"] = P("creation", "Asus ProArt PX13", "HN7306 · Ryzen AI Max · OLED 13,3\" tactile 360°", "Le concentré de puissance",
    "Un 13 pouces convertible qui embarque une puce Ryzen AI Max : des performances extrêmes dans un sac à main, avec une autonomie moyenne.",
    ["Performances extrêmes pour un 13\"", "Écran OLED tactile pivotant à 360°", "Stylet, DialPad et lecteur microSD"],
    ["Prix très élevé", "Autonomie en retrait", "Ventilation bruyante en rendu"],
    ("≈ 1,4 kg", "n.c."), cc("Asus+_ProArt+PX13", "2025-06-01"))
CAT["yoga-pro9"] = P("creation", "Lenovo Yoga Pro 9i 16", "16\" OLED 120 Hz · Core Ultra · RTX", "L'écran le plus abouti",
    "Un écran OLED tandem exceptionnel (jusqu'à 1 600 nits), de la puissance et une finition premium : le rival direct du MacBook Pro sous Windows.",
    ["Écran OLED très lumineux et fidèle", "GPU NVIDIA dédié", "Connectique complète"],
    ["Prix élevé", "Bruyant en mode performance"],
    ("n.c.", "n.c."), cc("Lenovo_Yoga+Pro+9i"), cc("Lenovo_Yoga+Pro+9"))
CAT["yoga-pro7"] = P("creation", "Lenovo Yoga Pro 7 15", "15IPH11 · Core Ultra 7 · 32 Go · 15,3\" 165 Hz", "Le multimédia équilibré",
    "Un 15 pouces multimédia très bien noté pour son écran et son équilibre général, plus raisonnable que le Yoga Pro 9i.",
    ["Très bel écran lumineux", "32 Go de RAM", "Bon équilibre puissance / autonomie"],
    ["Prix en hausse", "Peu de tests de cette configuration"],
    ("n.c.", "n.c."), cc("Lenovo_Yoga+Pro+7i", scope="gamme"))
CAT["zenbook-duo"] = P("creation", "Asus Zenbook Duo", "UX8406 · deux écrans OLED 14\" tactiles", "Le double écran",
    "Deux écrans OLED superposés et un clavier détachable : un gain de surface de travail unique pour le montage et la retouche en déplacement.",
    ["Deux écrans OLED 14\" tactiles", "Béquille et clavier détachable bien pensés", "Bonnes performances"],
    ["Plus épais et plus lourd qu'un 14\" classique", "Autonomie réduite avec les deux écrans", "Prix élevé"],
    ("≈ 1,65 kg", "n.c."), cc("Asus_ZenBook+Duo"))
CAT["aero-x16"] = P("creation", "Gigabyte Aero X16", "Ryzen AI · RTX 5060 · 16\" 165 Hz", "Le moins cher avec une RTX",
    "Un 16 pouces fin avec carte RTX à prix contenu. Bon pour jouer et monter en 1080p, mais son écran ne conviendra pas aux créatifs exigeants.",
    ["Beau design pour le prix", "Bon couple processeur / carte graphique", "RAM et SSD évolutifs"],
    ["Écran peu adapté à la retouche couleur", "Ventilateurs bruyants", "Chargeur propriétaire"],
    ("≈ 1,9 kg", "n.c."), cc("Gigabyte_Aero+X16"))
CAT["mba15-m5"] = P("creation", "Apple MacBook Air 15\" M5", "Puce M5 · 16 Go · 512 Go", "Le Mac grand écran",
    "Grand écran, silence total et puce M5 : parfait pour la photo et le montage léger, sans ventilateur ni encombrement.",
    ["Totalement silencieux", "Grand écran 15\" fidèle", "Puce M5 très performante"],
    ["Écran limité à 60 Hz", "Pas de GPU dédié pour la vidéo lourde", "RAM et SSD non évolutifs"],
    ("1,51 kg", "18 h (annoncée)"), cc("Apple_MacBook+Air+M5", "2026-01-01", inc=r"15"), cc("Apple_MacBook+Air+15", "2025-01-01", scope="gamme"))
CAT["zephyrus-g16"] = P("creation", "Asus ROG Zephyrus G16", "GU606 · Core Ultra 9 · RTX · OLED 240 Hz", "Le plus puissant",
    "Très puissant dans un châssis fin en aluminium, avec un superbe écran OLED 240 Hz : le haut de gamme pour la vidéo, la 3D… et le jeu.",
    ["Écran OLED 2,5K 240 Hz", "Châssis aluminium fin pour sa puissance", "Jusqu'à la RTX 5090"],
    ["Prix très élevé", "Chauffe et bruit en charge"],
    ("≈ 1,95 kg", "≈ 5 h 30 (test, travail)"), cc("Asus_ROG+Zephyrus+G16", scope="gamme"))

# ---------------------------------------------------------------- Gaming
CAT["legion5"] = P("gaming", "Lenovo Legion 5 15", "15AHP11 · Ryzen AI 7 · RTX 5060 · OLED 165 Hz", TOP,
    "Un écran OLED 165 Hz, un châssis soigné et un prix encore raisonnable : le meilleur rapport qualité-prix des PC gamer de cette génération selon la presse.",
    ["Excellent écran OLED 165 Hz", "Châssis élégant et solide", "Connectique variée"],
    ["Écran très réfléchissant", "Pas de configuration très haut de gamme"],
    ("≈ 1,9 kg", "n.c."), cc("Lenovo_Legion+5", "2025-06-01"))
CAT["omen-max-16"] = P("gaming", "HP Omen Max 16", "16\" WQXGA 240 Hz · RTX 5070 Ti", "Le plus musclé",
    "Grosses performances, écran 240 Hz et refroidissement efficace : une machine de jeu haut de gamme, lourde et chère.",
    ["Très grosses performances en jeu", "Écran 16\" 240 Hz", "Refroidissement efficace"],
    ["Lourd et encombrant", "Prix élevé", "Autonomie faible"],
    ("≈ 2,7 kg", "n.c."), cc("HP_Omen+Max+16"))
CAT["helios-neo-16"] = P("gaming", "Acer Predator Helios Neo 16 AI", "Core Ultra 9 · RTX 5070 Ti · OLED", "L'OLED pour jouer",
    "Une dalle OLED superbe et une RTX 5070 Ti à l'aise en QHD. En contrepartie : ça chauffe fort et l'autonomie est anecdotique.",
    ["Dalle OLED contrastée", "RTX 5070 Ti à l'aise en QHD", "Clavier complet, réseau 2,5 Gbit/s"],
    ["Chauffe importante", "Autonomie de 2 à 3 heures", "Reflets sur l'écran"],
    ("≈ 2,7 kg", "2 à 3 h (tests)"), cc("Acer_Predator+Helios+Neo+16", "2025-03-01", scope="gamme"))
CAT["loq15"] = P("gaming", "Lenovo LOQ 15", "Ryzen 7 ou Core i7 · RTX 5060 · 15,6\" 144 Hz", "L'entrée de gamme sérieuse",
    "Une porte d'entrée solide dans le jeu sur PC portable : bonnes performances et châssis sérieux, mais écran et clavier très basiques.",
    ["Bonnes performances en 1080p", "Construction sérieuse, évolutif", "Connectique complète"],
    ["Écran Full HD daté", "Clavier peu agréable", "Châssis plastique"],
    ("≈ 2,4 kg", "n.c."), cc("Lenovo_LOQ+15"))
CAT["katana15"] = P("gaming", "MSI Katana 15 HX", "Core i7 HX · RTX 5060 · 15,6\" 144 Hz", "Le rapport performances/prix",
    "Beaucoup de puissance pour le prix et un clavier confortable. L'écran est en retrait et la machine se fait entendre à pleine charge.",
    ["Bonnes performances en jeu", "Clavier confortable", "Tarif compétitif"],
    ["Écran pas au niveau", "Bruyant et chaud à pleine charge"],
    ("≈ 2,4 kg", "n.c."), cc("MSI_Katana+15"))
CAT["cyborg15"] = P("gaming", "MSI Cyborg 15", "Core 7 · RTX 5060 · 15,6\" 144 Hz", "Le gamer léger et abordable",
    "Un PC gamer d'entrée de gamme plus léger que la moyenne, correct en 1080p. Les tests sont partagés à cause de son écran sombre et de ses plastiques.",
    ["Jeu en 1080p sans difficulté", "Moins de 2 kg", "Bonne sélection de ports"],
    ["Écran assez sombre", "Finition plastique"],
    ("≈ 2 kg", "n.c."), cc("MSI_Cyborg+15"))
CAT["crosshair16"] = P("gaming", "MSI Crosshair 16 HX AI", "Core Ultra 7 HX · RTX 5070 · 16\" QHD+ 240 Hz", "Le bon élève",
    "Écran QHD+ 240 Hz et processeur HX : une configuration homogène, régulièrement notée 8/10, pour jouer confortablement en haute définition.",
    ["Écran 16\" QHD+ 240 Hz", "Processeur Core Ultra HX puissant", "Bon refroidissement"],
    ["Châssis plastique", "Autonomie limitée"],
    ("≈ 2,5 kg", "n.c."), cc("MSI_Crosshair+16+HX+AI"))
CAT["strix-g16"] = P("gaming", "Asus ROG Strix G16", "G614 / G615 · RTX 50 · 16\" jusqu'à 300 Hz", "Le plus consensuel",
    "Une machine de jeu très complète, saluée par de nombreux tests : écran rapide, grosses performances, mais châssis plastique et prix élevé.",
    ["Grosses performances en jeu", "Écran 16\" rapide et lumineux", "Accès facile aux composants"],
    ["Châssis majoritairement plastique", "Bruyant en charge", "Prix élevé"],
    ("2,5 kg", "≈ 5 h (test)"),
    man([("Labo Fnac", 10, None), ("Windows Central", 9, None), ("Notebookcheck", 8.7, None), ("Fortress of Solitude", 8.7, None), ("CowCotLand", 8, None),
         ("Geeknetic", 8, None), ("Pokde", 8, None), ("GamesRadar", 8, None), ("PCWorld", 8, None), ("GadgetByte", 8, None), ("Tom's Hardware", 8, None),
         ("Clubic", 8, None), ("IGN", 7, None), ("RTINGS", 6, None)]))
CAT["strix-g16"]["press_src"] = ("Synthèse CommentChoisir", "https://www.commentchoisir.fr/en/review-Asus_ROG+Strix+G16.htm")
CAT["gigabyte-a16"] = P("gaming", "Gigabyte Gaming A16", "Ryzen 7 · RTX 5060 · 16\" 165 Hz", "Le moins cher du top",
    "Un 16 pouces RTX 50 à prix serré, plutôt silencieux et endurant pour un gamer. L'écran et la connectique sont les postes d'économie.",
    ["Bon rapport qualité-prix", "Bruit et chauffe contenus", "Autonomie au-dessus de la moyenne"],
    ["Écran aux couleurs limitées", "Un seul port USB-C, lent"],
    ("≈ 2,2 kg", "n.c."), cc("Gigabyte_A16", scope="gamme"))
CAT["nitro-v16"] = P("gaming", "Acer Nitro V 16 AI", "ANV16 · Ryzen 7 · RTX 5060 · 16\" 165-180 Hz", "Le polyvalent du jeu",
    "Un grand écran rapide et une RTX 5060 dans un châssis sobre : un PC gamer accessible, bien noté par la presse sur cette génération.",
    ["Écran 16\" WUXGA rapide", "RTX 5060 efficace en 1080p", "Design sobre"],
    ["Châssis plastique", "Autonomie limitée"],
    ("≈ 2,5 kg", "n.c."), cc("Acer_Nitro+16", scope="gamme"))

# ---------------------------------------------------------------- Polyvalent
CAT["yoga-slim7"] = P("polyvalent", "Lenovo Yoga Slim 7 14", "14ILL · Core Ultra · 16 Go · OLED 14\"", TOP,
    "Châssis léger, écran OLED bien calibré, grande autonomie et connectique complète : aucun vrai point faible, et un prix redevenu raisonnable.",
    ["Châssis léger et confortable", "Écran OLED bien calibré", "Excellente autonomie"],
    ["Webcam moyenne", "Performances en jeu limitées"],
    ("≈ 1,3 kg", "n.c."), cc("Lenovo_Yoga+Slim+7", scope="gamme"), cc("Lenovo_Yoga+Slim+7i", scope="gamme"))
CAT["yoga-slim7x"] = P("polyvalent", "Lenovo Yoga Slim 7x", "14Q8X9 · Snapdragon X Elite · OLED 3K 90 Hz", "Le meilleur PC Snapdragon",
    "Écran OLED 3K superbe, finesse et autonomie : pour beaucoup de testeurs, le PC Snapdragon le plus abouti. Attention à la compatibilité de vos logiciels.",
    ["Écran OLED 3K 90 Hz très lumineux", "Fin et léger", "Très bonne autonomie"],
    ["Compatibilité logicielle ARM à vérifier", "Pas de prise casque", "Jeu limité"],
    ("1,28 kg", "n.c."), cc("Lenovo_Yoga+Slim+7x", "2024-06-01"))
CAT["vivobook-s14"] = P("polyvalent", "Asus Vivobook S14", "OLED 14\" · Core Ultra ou Ryzen AI · 16 Go", "L'OLED sous les 1 000 €",
    "Un écran OLED, une douzaine d'heures d'autonomie et un châssis fin pour moins de 1 000 € : un excellent rapport qualité-prix.",
    ["Écran OLED à prix serré", "Autonomie confortable (≈ 12 h)", "Reconnaissance faciale"],
    ["Dalle brillante, pas très lumineuse", "Partie graphique limitée"],
    ("≈ 1,3 kg", "≈ 12 h (tests)"), cc("Asus_VivoBook+S14"))
CAT["zenbook-s14"] = P("polyvalent", "Asus Zenbook S 14", "UX5406 · Core Ultra · OLED 14\"", "Le plus fin",
    "Très fin, très léger, silencieux et endurant : un ultraportable premium unanimement salué, avec un superbe écran OLED.",
    ["Finesse et légèreté (1,2 kg)", "Écran OLED superbe", "Silencieux, bonne autonomie"],
    ["Puissance graphique limitée", "RAM soudée"],
    ("1,2 kg", "n.c."), cc("Asus_ZenBook+S+14", "2024-09-01", scope="gamme"))
CAT["zenbook-s16"] = P("polyvalent", "Asus Zenbook S 16", "UM5606 · Ryzen AI · OLED 16\" 120 Hz", "Le grand écran fin",
    "Un 16 pouces OLED 120 Hz de 1,5 kg : grand confort d'affichage et bonnes performances dans un châssis étonnamment fin.",
    ["Écran OLED 16\" 3K 120 Hz", "1,5 kg seulement", "Bonnes performances Ryzen AI"],
    ["Chauffe en charge", "RAM soudée"],
    ("1,5 kg", "n.c."), cc("Asus_ZenBook+S+16", "2024-07-01", scope="gamme"), cc("Asus_ZenBook+S16", "2024-07-01", scope="gamme"))
CAT["omnibook-x-flip14"] = P("polyvalent", "HP OmniBook X Flip 14", "2-en-1 · OLED 14\" tactile · Core Ultra ou Ryzen AI", "Le 2-en-1 compact",
    "Un convertible compact au clavier très confortable et à l'écran OLED tactile. Les avis sont partagés sur son autonomie et ses haut-parleurs.",
    ["Format 2-en-1 très maîtrisé", "Clavier confortable", "Écran OLED tactile bien calibré"],
    ["Haut-parleurs décevants", "Écran très brillant", "Autonomie moyenne"],
    ("≈ 1,4 kg", "n.c."), cc("HP_OmniBook+X+Flip+14"))
CAT["yoga7-2in1"] = P("polyvalent", "Lenovo Yoga 7 2-en-1", "14\" ou 16\" OLED tactile · Ryzen AI", "Le convertible familial",
    "Un convertible OLED bien construit et bien noté, à l'aise pour travailler comme pour regarder un film en mode tablette.",
    ["Écran OLED tactile", "Charnière 360° solide", "Bonne autonomie"],
    ["Un peu lourd en mode tablette", "Stylet pas toujours fourni"],
    ("n.c.", "n.c."), cc("Lenovo_Yoga+7", scope="gamme"))
CAT["ideapad-slim5-16"] = P("polyvalent", "Lenovo IdeaPad Slim 5 16", "16IPH11 · Core Ultra 5 · 16 Go · OLED 16\"", "Le grand écran raisonnable",
    "Un 16 pouces OLED bien équipé sous les 1 000 € : un choix familial sûr, sans prétention pour le jeu.",
    ["Grand écran OLED 16\"", "16 Go de RAM", "Prix contenu"],
    ["Pas de carte graphique dédiée", "Finition simple"],
    ("n.c.", "n.c."), cc("Lenovo_Ideapad+Slim+5+16"))
CAT["swift16ai"] = P("polyvalent", "Acer Swift 16 AI", "SF16 · Core Ultra · 32 Go · OLED 16\" tactile", "Le multimédia discret",
    "Écran OLED brillant de qualité, fonctionnement frais et silencieux, bonne endurance : un grand ultraportable très homogène.",
    ["Bel écran OLED 16\"", "Reste frais et silencieux", "Bonne autonomie"],
    ["Prix de la configuration haut de gamme", "Dalle brillante"],
    ("≈ 1,5 kg", "n.c."), cc("Acer_Swift+16+AI"))
CAT["lg-gram17"] = P("polyvalent", "LG Gram 17", "17Z90TL · Core Ultra 7 · 17\" QHD+", "Le 17 pouces de 1,4 kg",
    "Un écran 17 pouces dans moins de 1,4 kg, avec une autonomie respectable. La presse est partagée : le Labo Fnac sanctionne le calibrage de l'écran.",
    ["17\" pour moins de 1,4 kg", "Silencieux, chauffe maîtrisée", "Autonomie de 12 à 13 h"],
    ["Écran IPS mal calibré", "Wi-Fi 6 seulement", "Quelques soucis de finition"],
    ("1,39 kg", "12 à 13 h (tests)"), cc("LG_Gram+17"))

# ---------------------------------------------------------------- Low-cost (< 500 €)
CAT["aspire-go-15"] = P("lowcost", "Acer Aspire Go 15", "AG15 · 15,6\" Full HD · 8 Go · 512 Go", TOP,
    "Le petit prix le mieux testé : un 15 pouces simple et honnête, suffisant pour le web, les cours et la bureautique.",
    ["Prix plancher", "Bonne autonomie pour la gamme", "Connectique complète"],
    ["Écran terne", "8 Go de RAM sur les premiers prix", "Finition plastique"],
    ("1,75 kg", "n.c."), cc("Acer_Aspire+Go+15", "2024-01-01", scope="gamme"))
CAT["ideapad-slim3"] = P("lowcost", "Lenovo IdeaPad Slim 3", "15,6\" Full HD · Athlon ou Ryzen · 8 Go", "Le classique",
    "Une valeur connue de l'entrée de gamme. Les tests sont mitigés : choisissez au minimum une version Ryzen 5 avec un vrai SSD.",
    ["Prix d'appel très bas", "Clavier correct", "Nombreuses configurations"],
    ["Version Athlon / 128 Go très limitée", "Écran terne", "Autonomie moyenne"],
    ("≈ 1,6 kg", "n.c."), cc("Lenovo_Ideapad+Slim+3", scope="gamme"))
CAT["ideapad1"] = P("lowcost", "Lenovo IdeaPad 1 15", "15ALC7 · Ryzen 5 · 16 Go · 512 Go", "Le mieux équipé",
    "16 Go de RAM et 512 Go de SSD à ce prix, c'est rare. Le reste est basique : la presse note sévèrement son écran et sa finition.",
    ["16 Go de RAM et 512 Go de SSD", "Prix très bas", "Très nombreux avis acheteurs positifs"],
    ["Écran peu lumineux", "Processeur d'ancienne génération", "Finition plastique"],
    ("≈ 1,6 kg", "n.c."), cc("Lenovo_IdeaPad+1", "2022-01-01", scope="gamme"))
CAT["chromebook-315"] = P("lowcost", "Acer Chromebook 315", "15,6\" · MediaTek Kompanio · ChromeOS", "Le grand écran à 300 €",
    "Un Chromebook 15 pouces simple et endurant pour le web, les mails et les documents en ligne. À condition d'accepter ChromeOS.",
    ["Prix très bas", "Grand écran 15,6\"", "ChromeOS simple et sûr"],
    ["Limité aux usages web", "Stockage réduit", "Écran basique"],
    ("≈ 1,6 kg", "n.c."), cc("Acer_Chromebook+315"))
CAT["chromebook-plus-514"] = P("lowcost", "Acer Chromebook Plus 514", "14\" · Core 3 · 8 Go · ChromeOS", "Le Chromebook musclé",
    "Solide, confortable et assez rapide pour ne jamais ralentir sous ChromeOS : le Chromebook à choisir si le budget le permet.",
    ["Construction solide", "Clavier et pavé tactile confortables", "Performances à l'aise sous ChromeOS"],
    ["Écran peu lumineux", "Autonomie moyenne", "Pas de lecteur d'empreintes"],
    ("≈ 1,4 kg", "n.c."), cc("Acer_Chromebook+Plus+514", "2023-01-01", scope="gamme"))
CAT["chromebook-duet"] = P("lowcost", "Lenovo Chromebook Duet 11", "Tablette 11\" + clavier + stylet · ChromeOS", "La tablette-PC",
    "Une tablette ChromeOS livrée avec clavier (et souvent stylet) : idéale pour prendre des notes et regarder des vidéos, pas pour travailler lourd.",
    ["Clavier détachable fourni", "Très légère", "Bonne autonomie"],
    ["Petit écran pour travailler longtemps", "Puissance limitée"],
    ("≈ 0,5 kg (tablette)", "n.c."), cc("Lenovo_Chromebook+Duet", "2024-06-01"))
CAT["vivobook-14"] = P("lowcost", "Asus Vivobook 14", "E1404 · 14\" · Intel N150 · 8 Go", "Le plus petit prix Windows",
    "Un 14 pouces Windows à moins de 350 € : suffisant pour le web et le traitement de texte, pas davantage.",
    ["Prix très bas", "Compact et léger", "Silencieux"],
    ["Processeur d'entrée de gamme", "128 Go de stockage eMMC", "Écran basique"],
    ("≈ 1,4 kg", "n.c."), cc("Asus_Vivobook+14", scope="gamme"))
CAT["vivobook-go-14"] = P("lowcost", "Asus Vivobook Go 14", "E1404 · 14\" Full HD · Intel N150 · 8 Go", "Le compact sans prétention",
    "Proche du Vivobook 14, avec un écran Full HD et un SSD : un petit portable d'appoint que la presse juge correct, sans plus.",
    ["Écran Full HD", "Format compact", "Prix contenu"],
    ["Puissance très limitée", "Stockage réduit"],
    ("≈ 1,4 kg", "n.c."), cc("Asus_VivoBook+Go+15", "2023-01-01", scope="gamme"))
CAT["lenovo-v15"] = P("lowcost", "Lenovo V15 G4", "15,6\" Full HD · Ryzen 3 · 8 Go", "Le bureautique pro",
    "Un 15 pouces pensé pour le bureau : écran correct et clavier complet, mais autonomie décevante et finition économique.",
    ["Écran correct pour la gamme", "Clavier avec pavé numérique", "Suffisant pour la bureautique"],
    ["Autonomie décevante", "Plastiques bon marché", "Haut-parleurs et webcam médiocres"],
    ("≈ 1,65 kg", "n.c."), cc("Lenovo_V15", "2024-01-01", scope="gamme"))
CAT["chromebook-cx14"] = P("lowcost", "Asus Chromebook CX14", "CX1405 · 14\" Full HD · Core 3 · ChromeOS", "Le Chromebook équilibré",
    "Un Chromebook 14 pouces Full HD bien équipé pour son prix. La presse le trouve honnête, sans éclat.",
    ["Écran Full HD", "Bon équipement pour le prix", "ChromeOS simple et sûr"],
    ["Finition plastique", "Limité aux usages web"],
    ("≈ 1,4 kg", "n.c."), cc("Asus_Chromebook+CX1", "2024-01-01", scope="gamme"))

# =====================================================================================================================
#                                               ORDINATEURS DE BUREAU
# =====================================================================================================================
CR = "Consumer Reports"
# ---------------------------------------------------------------- Bureautique
CAT["mac-mini-m6"] = P("d-bureau", "Apple Mac mini M6", "Puce M6 · 16 Go · 256 Go", TOP,
    "Minuscule, silencieux et très rapide : toujours le meilleur petit ordinateur de bureau, même si son prix a nettement augmenté.",
    ["Puce M6 très performante", "Ni bruit ni chauffe", "Format minuscule, finition exemplaire"],
    ["Prix en forte hausse", "Aucune évolutivité", "Bouton d'alimentation mal placé"],
    ("Mini (12,7 cm de côté)", "Apple M6"), cc("Apple_Mac+mini+M6", "2026-01-01"))
CAT["ideacentre-mini"] = P("d-bureau", "Lenovo IdeaCentre Mini", "01IRH · Intel Core 5 · 16 Go · 512 Go", "Le mini discret",
    "Un mini-PC de grande marque, compact et suffisant pour la bureautique, avec Thunderbolt 4. La partie graphique est en retrait.",
    ["Très compact", "Bonnes performances en bureautique", "Thunderbolt 4 et HDMI 2.1"],
    ["Partie graphique limitée", "512 Go de stockage seulement"],
    ("Mini-PC", "Intel Core 5 / i5"), cc("Lenovo_IdeaCentre+Mini+01IRH", scope="gamme"))
CAT["omnidesk-slim"] = P("d-bureau", "HP OmniDesk Slim", "S03 · Intel Core · 8 Go · 512 Go", "Le plus discret",
    "Une tour fine qui se glisse sous un écran, suffisante pour le web, les mails et la bureautique.",
    ["Encombrement réduit", "Prix contenu", "Nombreux ports USB"],
    ["8 Go de RAM sur l'entrée de gamme", "Peu évolutif"],
    ("Tour compacte", "Intel Core i3 / i5"), man([(CR, None, "https://www.consumerreports.org/electronics-computers/computers/hp-omnidesk-slim-desktop-s03-0034/m417304/")], "gamme"))
CAT["dell-slim"] = P("d-bureau", "Dell Slim", "ECS1250 · Intel Core i5 · 512 Go", "Le plus classique",
    "Une tour compacte silencieuse et sobre en énergie, facile à faire évoluer, pour la bureautique familiale ou professionnelle.",
    ["Silencieux et économe", "Évolutif (RAM, stockage)", "Connectique complète"],
    ["Performances modestes", "Pas de carte graphique dédiée"],
    ("Tour compacte", "Intel Core i5"), man([(CR, None, "https://www.consumerreports.org/electronics-computers/computers/dell-slim-desktop-ecs1250/m417764/")]))
CAT["ideacentre-tower"] = P("d-bureau", "Lenovo IdeaCentre Tower", "08AKP10 / 08IRR9 · 16 Go · 512 Go", "Le plus évolutif",
    "Une tour familiale classique, qui laisse de la place pour ajouter un disque ou une carte graphique plus tard.",
    ["Place pour évoluer", "16 Go de RAM", "Bon rapport prix / équipement"],
    ["Design quelconque", "Alimentation limitée pour un gros GPU"],
    ("Tour", "Ryzen AI 7 / Core i5"), man([(CR, None, "https://www.consumerreports.org/electronics-computers/computers/lenovo-ideacentre-tower-desktop-91cf000dus/m419469/")], "gamme"))
CAT["asus-v500"] = P("d-bureau", "Asus V500", "V501 · Intel Core · 16 Go · 512 Go", "Le compact stylé",
    "Une petite tour au design soigné, correcte pour le travail quotidien ; son évolutivité reste limitée.",
    ["Format compact, design soigné", "Silencieux", "Processeur Core récent"],
    ["Évolutivité limitée", "Pas de carte graphique dédiée sur les premiers prix"],
    ("Mini-tour (15 L)", "Intel Core 5 / 7"),
    man([("Pokde", None, "https://pokde.net/review/asus-v500mv-mini-tower-review"),
         (CR, None, "https://www.consumerreports.org/electronics-computers/computers/asus-v500-mini-tower-15l-desktop-v500mv-is706/m417716/")], "gamme"))
CAT["aspire-xc"] = P("d-bureau", "Acer Aspire XC", "XC-1860 · Core Ultra 5 · 8 Go · 512 Go", "Le petit budget",
    "Une tour compacte à prix serré, peu gourmande en énergie : la génération précédente avait été saluée pour son rapport qualité-prix.",
    ["Prix abordable", "Faible consommation", "Format compact"],
    ["8 Go de RAM sur l'entrée de gamme", "Clavier et souris non inclus"],
    ("Tour compacte", "Intel Core Ultra 5"), man([("IT Pro", 8.0, "https://www.itpro.com/hardware/368654/acer-aspire-xc-1660-review-a-clear-winner-for-value")], "gamme"))
CAT["geekom-a5"] = P("d-bureau", "Geekom A5", "Édition 2027 · Ryzen 5 ou 7 · 16 Go", "Le mini pour le bureau",
    "Un mini-PC bien construit, quasi inaudible et très sobre : tout ce qu'il faut pour la bureautique, à moins de 500 €.",
    ["Quasi silencieux, températures basses", "Facile à ouvrir (RAM, SSD)", "Bon rapport qualité-prix"],
    ["Processeur d'ancienne génération", "Puce graphique modeste", "Prix en hausse"],
    ("Mini-PC", "AMD Ryzen 5 7430U / Ryzen 7 7730U"), cc("Geekom_A5", "2026-01-01"), cc("Geekom_A5+-+2025", "2025-01-01"))
CAT["geekom-air12-lite"] = P("d-bureau", "Geekom Mini Air12 Lite", "Intel N95 / N100 · 8 Go · 256 Go", "Le moins cher",
    "Le mini-PC à tout petit prix pour un usage basique : web, bureautique, vidéo. Compact et élégant, mais vite à court de puissance.",
    ["Tarif très raisonnable", "Compact et élégant", "2 sorties HDMI"],
    ["Seulement 8 Go de RAM", "Puissance graphique très limitée", "Pas d'USB-C"],
    ("Mini-PC", "Intel N95 / N100"), cc("Geekom_Air12+Lite", "2024-01-01"), cc("Geekom_Mini+Air12", "2024-10-01", inc="lite"))
CAT["geekom-it12"] = P("d-bureau", "Geekom Mini IT12", "Intel Core 12e gén. · 16 Go", "Le Core à prix doux",
    "Un mini-PC Intel Core compact, à la connectique généreuse et facile à ouvrir. Son ventilateur s'entend presque toujours.",
    ["Boîtier compact et solide", "Connectique très complète (USB4)", "Facile à ouvrir"],
    ["Ventilateur souvent audible", "Processeur de 12e génération"],
    ("Mini-PC", "Intel Core i3 / i5 / i7 (12e gén.)"), cc("Geekom_Mini+IT12", "2023-01-01"), cc("Geekom_IT12", "2025-01-01"))

# ---------------------------------------------------------------- Création & station de travail
CAT["mac-mini-m5pro"] = P("d-creation", "Apple Mac mini M5 Pro", "Puce M5 Pro · 24 Go · 512 Go", TOP,
    "La puissance d'une station de travail dans un boîtier de 12,7 cm, avec Thunderbolt 5 : le meilleur compromis pour la photo et le montage.",
    ["Puce M5 Pro très puissante", "Silencieux et minuscule", "Trois ports Thunderbolt 5"],
    ["Prix des options (RAM, SSD)", "Aucune évolutivité"],
    ("Mini (12,7 cm de côté)", "Apple M5 Pro"),
    man([("ZDNet", 8.0, "https://www.zdnet.com/tech/apple-mac-mini-m5-pro-review/"), ("PCMag", None, "https://www.pcmag.com/reviews/apple-mac-mini-2026-m5-pro")]),
    cc("Apple_Mac+mini", "2026-09-01", inc="m5 pro|m5-pro"))
CAT["mac-studio-m5max"] = P("d-creation", "Apple Mac Studio M5 Max", "Puce M5 Max · 36 Go · 512 Go", "La puissance au calme",
    "Des performances de très haut niveau dans un boîtier compact et silencieux, avec une connectique exhaustive.",
    ["Performances au sommet", "Chauffe et bruit minimes", "Connectique exhaustive"],
    ["Aucune modularité", "Prix élevé"],
    ("Compact (19,7 cm de côté)", "Apple M5 Max"), cc("Apple_Mac+Studio+M5+Max", "2026-01-01"), cc("Apple_Mac+Studio", "2026-09-01"))
CAT["geekom-a9max"] = P("d-creation", "Geekom A9 Max", "Ryzen AI 9 HX · 32 Go · 2 To", "Le mini-PC le plus testé",
    "Un mini-PC très puissant et bien fini, livré avec 32 Go de RAM évolutifs et 2 To de SSD. La puce graphique intégrée reste sa limite.",
    ["Processeur Ryzen AI 9 très puissant", "32 Go de RAM évolutifs, 2 To de SSD", "Connectique complète"],
    ["Prix élevé", "Puissance graphique limitée", "Démontage peu aisé"],
    ("Mini-PC", "AMD Ryzen AI 9 HX 370 / 470"), cc("Geekom_A9+Max"))
CAT["geekom-it15"] = P("d-creation", "Geekom IT15", "Core Ultra 9 285H · 32 Go · 1 To", "Le Core Ultra compact",
    "Les 16 cœurs du Core Ultra 9 dans un boîtier de poche, avec deux ports USB4 et un Windows sans logiciels superflus.",
    ["Processeur Core Ultra 9 puissant", "32 Go de RAM, RAM et SSD évolutifs", "Deux ports USB4"],
    ["Puce graphique peu adaptée au jeu", "Chauffe perceptible en charge", "Pas d'USB-C en façade"],
    ("Mini-PC", "Intel Core Ultra 9 285H"), cc("Geekom_IT15"))
CAT["geekom-gt1mega"] = P("d-creation", "Geekom GT1 Mega", "Core Ultra 9 185H · 16 ou 32 Go", "Le bon plan puissance",
    "Processeur haut de gamme, Wi-Fi 7, double USB4 et double réseau 2,5 GbE pour moins de 900 € : beaucoup de puissance pour le prix.",
    ["Performances processeur élevées", "Connectique très complète (Wi-Fi 7, 2 × USB4)", "RAM et SSD accessibles"],
    ["Bruyant à pleine puissance", "Chauffe sous forte charge"],
    ("Mini-PC", "Intel Core Ultra 9 185H"), cc("Geekom_GT1+Mega", "2024-09-01"))
CAT["hp-z2-mini"] = P("d-creation", "HP Z2 Mini G1a", "Ryzen AI Max Pro · jusqu'à 128 Go", "La station de travail mini",
    "Une vraie station de travail professionnelle au format mini : mémoire unifiée jusqu'à 128 Go, idéale pour la 3D et l'IA en local.",
    ["Processeur et GPU intégré de premier ordre", "Jusqu'à 128 Go de mémoire unifiée", "Compacte, conception professionnelle"],
    ["Peut devenir très bruyante", "Tarif élevé"],
    ("Mini station de travail", "AMD Ryzen AI Max Pro"), cc("HP_Z2+Mini"))
CAT["thinkstation-p3"] = P("d-creation", "Lenovo ThinkStation P3 Tiny", "Gen 2 · Intel Core · carte NVIDIA RTX pro", "La station certifiée",
    "Une station de travail d'un litre, prête pour la CAO et le rendu 3D, avec une connectique abondante. Ventilation sonore en charge.",
    ["Beaucoup de puissance pour la taille", "Connectique abondante", "Prête pour la CAO et le rendu"],
    ["Ventilateurs bruyants", "Prix"],
    ("Mini station de travail (1 L)", "Intel Core / Core Ultra"), cc("Lenovo_ThinkStation+P3", scope="gamme"))
CAT["minisforum-ai-x1-pro"] = P("d-creation", "Minisforum AI X1 Pro", "Ryzen AI 9 HX · 32 Go · 1 To", "Le mini tout métal",
    "Boîtier métal, alimentation intégrée, lecteur d'empreintes et refroidissement efficace : un mini-PC haut de gamme calme et bien pensé.",
    ["Boîtier métal de qualité", "Refroidissement performant et calme", "Alimentation intégrée"],
    ["RAM livrée sur un seul module", "Prix élevé sans carte graphique dédiée"],
    ("Mini-PC", "AMD Ryzen AI 9 HX 370 / 470"), cc("Minisforum_AI+X1+Pro"))
CAT["minisforum-ms-s1-max"] = P("d-creation", "Minisforum MS-S1 Max", "Ryzen AI Max+ 395 · 64 ou 128 Go", "La mini-station IA",
    "16 cœurs Zen 5 et jusqu'à 128 Go de mémoire unifiée : une mini-station taillée pour l'IA locale et le calcul lourd.",
    ["Jusqu'à 128 Go de mémoire unifiée", "Processeur 16 cœurs très puissant", "Connectique complète"],
    ["Mémoire non évolutive", "Prix élevé"],
    ("Mini station de travail", "AMD Ryzen AI Max+ 395"), cc("Minisforum_MS-S1+Max"))
CAT["gmktec-evo-x2"] = P("d-creation", "GMKtec EVO-X2", "Ryzen AI Max+ 395 · 64 Go · 1 To", "Le graphique intégré record",
    "La puce graphique intégrée la plus rapide du marché, au niveau d'une RTX 4060 mobile, et beaucoup de mémoire pour l'IA locale.",
    ["Puce graphique intégrée du niveau d'une RTX 4060 mobile", "Jusqu'à 128 Go de mémoire unifiée", "Processeur 16 cœurs"],
    ["Mémoire soudée", "Tarif élevé", "Consommation jusqu'à 130 W"],
    ("Mini-PC", "AMD Ryzen AI Max+ 395"), cc("GMKtec_EVO-X2"))

# ---------------------------------------------------------------- Gaming
CAT["omen35l"] = P("d-gaming", "HP Omen 35L", "Ryzen 7 ou Core Ultra · 32 Go · RTX 5070 à 5080", TOP,
    "La tour gaming la mieux notée de la sélection : puissante, polyvalente, évolutive et plutôt élégante.",
    ["Très bonnes performances en jeu", "32 Go de RAM, évolutive", "Design réussi"],
    ["Un peu chère", "Logiciels préinstallés envahissants"],
    ("Tour gaming (35 L)", "Ryzen 7 / Core Ultra"), cc("HP_Omen+35L", "2024-09-01"))
CAT["omen16l"] = P("d-gaming", "HP Omen 16L", "Ryzen 5 ou Core i5 · 16 Go · RTX 5050 / 5060", "La tour compacte",
    "Une petite tour gaming élégante, à l'aise en 1080p : le Labo Fnac lui a donné la note maximale à deux reprises.",
    ["Format compact", "Très à l'aise en 1080p", "Design élégant"],
    ["Évolutivité limitée par le format", "512 Go de SSD sur certaines versions"],
    ("Tour compacte (16 L)", "Ryzen 5 / Core i5"), cc("HP_Omen+16", "2025-01-01", inc="16l"))
CAT["loq-tower"] = P("d-gaming", "Lenovo LOQ Tower", "Ryzen 7 ou Core i5 · 16 Go · RTX 5060 à 5070", "L'entrée de gamme sérieuse",
    "La tour gaming abordable de Lenovo : à l'aise en 1080p, simple et sobre, mais avec une marge d'évolution limitée.",
    ["Prix accessible", "Bonnes performances en 1080p", "Design sobre"],
    ["Évolutivité limitée", "Refroidissement basique"],
    ("Tour gaming", "Ryzen 7 / Core i5"), cc("Lenovo_LOQ", "2025-01-01", inc="tower", scope="gamme"))
CAT["legion-tower-5"] = P("d-gaming", "Lenovo Legion Tower 5 (Gen 10)", "Core Ultra ou Ryzen · 32 Go · RTX 5060 à 5070 Ti", "Le bon rapport performances/prix",
    "Une tour très rapide pour son prix, surtout en 1080p et 1440p. CNET salue sa valeur, IGN regrette quelques choix de conception.",
    ["Très bon rapport performances/prix", "32 Go de RAM", "Composants standards, évolutive"],
    ["Quelques choix de conception discutables", "Ventilation audible"],
    ("Tour gaming (30 L)", "Core Ultra / Ryzen 7"),
    man([("CNET", 8.4, "https://www.cnet.com/tech/computing/lenovo-legion-tower-5-gen-10-desktop-review-mighty-good-value-if-a-little-quirky/"),
         ("IGN", 6.0, "https://www.ign.com/articles/lenovo-legion-tower-5-2025-review")]))
CAT["orion-7000"] = P("d-gaming", "Acer Predator Orion 7000", "PO7-655 · Core i7 · 32 Go · RTX 4080 Super", "La vitrine RGB",
    "Un grand châssis spectaculaire, beaucoup de puissance et de ports. Très lourd, encombrant et cher.",
    ["Hautes performances", "Châssis magnifique, éclairage RGB", "Large sélection de ports"],
    ["Très lourd et encombrant", "Ventilateurs parfois bruyants", "Cher"],
    ("Grande tour gaming", "Intel Core i7-14700KF"), cc("Acer_Predator+Orion+7000", "2023-01-01", scope="gamme"))
CAT["nitro-60"] = P("d-gaming", "Acer Nitro 60", "Core i5 / i7 · RTX 5060 à 5070", "L'essentiel bien fait",
    "Une tour qui soigne l'essentiel, d'après le test de Tom's Hardware : de bonnes performances en jeu dans un boîtier sobre.",
    ["Bonnes performances en jeu", "Tour sobre et compacte", "Connectique correcte"],
    ["Processeur d'ancienne génération", "Peu de marge d'évolution"],
    ("Tour gaming", "Intel Core i5 / i7 (14e gén.)"), man([("Tom's Hardware", 8.0, "https://www.tomshardware.com/desktops/gaming-pcs/acer-nitro-60-review")]))
CAT["nitro-50"] = P("d-gaming", "Acer Nitro 50", "N50-656 · Core i5 · 16 Go · RTX 5060", "Le premier prix",
    "La tour gaming la moins chère de la sélection avec une RTX 5060. Les générations précédentes ont été critiquées pour leur stockage et leur évolutivité.",
    ["Prix d'accès très bas", "RTX 5060 pour jouer en 1080p", "Format compact"],
    ["Évolutivité limitée", "Composants d'entrée de gamme"],
    ("Tour gaming compacte", "Intel Core i5"), man([("PC Gamer", 6.5, "https://www.pcgamer.com/acer-nitro-50-gaming-pc-review/")], "gamme"))
CAT["rog-g700"] = P("d-gaming", "Asus ROG G700", "Ryzen 7 ou Core Ultra 7 · 32 Go · RTX 5060 à 5080", "La tour ROG",
    "Une tour gaming rapide en toutes circonstances et très polyvalente, testée par le Labo Fnac.",
    ["Très bonnes performances graphiques", "Rapide en toutes circonstances", "Polyvalente"],
    ["Stockage réel inférieur à l'annonce", "Prix élevé"],
    ("Tour gaming", "Ryzen 7 / Core Ultra 7"), cc("Asus+_ROG+G700TF-7265KF104W", "2025-01-01", scope="gamme"))
CAT["aorus-prime-5"] = P("d-gaming", "Gigabyte Aorus Prime 5", "Ryzen 7 9800X3D · 32 Go · RTX 5070 Ti / 5080", "Le silence haut de gamme",
    "Des performances de premier plan avec une acoustique et des températures très maîtrisées. Un PC préassemblé soigné, vendu cher.",
    ["Performances de premier plan", "Très silencieux, températures maîtrisées", "Montage propre"],
    ["Prix élevé", "Peu de configurations"],
    ("Tour gaming", "AMD Ryzen 7 9800X3D"),
    man([("Club386", 8.0, "https://www.club386.com/gigabyte-aorus-prime-5-review/"), ("PC Guide", 9.0, "https://www.pcguide.com/gaming-pc/gigabyte-aorus-prime-5-review/")]))
CAT["area-51"] = P("d-gaming", "Alienware Area-51", "Core Ultra 9 285K · RTX 5080 / 5090", "Le sans-limite",
    "Le vaisseau amiral d'Alienware : une puissance démesurée et, enfin, des composants standards faciles à remplacer. Prix à l'avenant.",
    ["Puissance maximale", "Composants standards, évolutif", "Refroidissement très efficace"],
    ["Prix très élevé", "Énorme et très lourd"],
    ("Grande tour gaming (80 L)", "Intel Core Ultra 9 285K"), cc("Alienware_Area+51", "2025-01-01"))

# ---------------------------------------------------------------- Mini-PC
CAT["geekom-a8"] = P("d-mini", "Geekom A8", "Ryzen 7 8745HS · 16 Go · 1 To", "Le plus puissant du top",
    "Très puissant pour sa taille et bien fini, avec une puce graphique Radeon 780M capable de jouer léger.",
    ["Très puissant pour sa taille", "Belle finition", "Puce graphique Radeon 780M"],
    ["Pas de place pour un second SSD", "Ventilation audible en charge"],
    ("11,2 cm de côté", "AMD Ryzen 7 8745HS"), cc("Geekom_A8", "2024-06-01"))
CAT["geekom-a5pro"] = P("d-mini", "Geekom A5 Pro", "Édition 2026 · Ryzen 5 ou 7 · 16 Go", "Le sobre",
    "Compact, sobre et suffisant pour la bureautique, avec deux emplacements SSD. La presse aimerait le voir passer sous les 500 €.",
    ["Compact et élégant", "Consommation très basse", "Deux emplacements M.2"],
    ["16 Go de RAM sans emplacement libre", "Pas d'USB4", "Puissance limitée"],
    ("Mini-PC", "AMD Ryzen 5 7530U / Ryzen 7 5825U"), cc("Geekom_A5+Pro"))
CAT["geekom-a6"] = P("d-mini", "Geekom A6", "Ryzen 7 6800H · 16 Go · 512 Go ou 1 To", "Le bon plan AMD",
    "Un mini-PC très bien construit avec un processeur encore vaillant et de l'USB4, à prix intéressant. Sa ventilation s'entend.",
    ["Fabrication de qualité", "USB4 et large choix de ports", "Bonnes performances au quotidien"],
    ["Processeur de 2022", "Généralement audible"],
    ("Mini-PC", "AMD Ryzen 7 6800H"), cc("Geekom_A6+Mini"))
CAT["geekom-a7"] = P("d-mini", "Geekom A7", "Ryzen 5 7535HS à Ryzen 9 7940HS · 16 Go", TOP,
    "Le mini-PC le mieux noté de la sélection : boîtier très fin et bien fini, deux ports USB4, processeur performant, et un prix devenu abordable.",
    ["Design fin et soigné", "2 × USB4, nombreux ports", "Processeur performant"],
    ["Livré avec une seule barrette de RAM", "Chauffe bien présente", "Pas de second SSD"],
    ("Mini-PC", "AMD Ryzen 5 7535HS / Ryzen 9 7940HS"), cc("Geekom_A7", "2024-01-01"))
CAT["geekom-it13"] = P("d-mini", "Geekom IT13", "Core i5-13600H à i9-13900HK · 16 ou 32 Go", "L'Intel bien équipé",
    "Beaucoup de puissance dans un petit volume, avec lecteur de cartes et emplacement 2,5 pouces. Monte vite en température.",
    ["Grosse puissance, petit volume", "Connectique riche, lecteur de cartes", "Emplacement SSD 2,5\" en plus"],
    ["Ventilateur bruyant en charge", "Pas d'USB-C en façade"],
    ("Mini-PC", "Intel Core i5-13600H / i9-13900HK"), cc("Geekom_IT13", "2023-06-01", exc="max"), cc("Geekom_Mini+IT13", "2023-06-01", exc="max"))
CAT["beelink-eq14"] = P("d-mini", "Beelink EQ14", "Intel N150 · 16 Go · 500 Go", "Le silencieux",
    "Un mini-PC très silencieux à alimentation intégrée, pour le web, la bureautique ou un petit serveur domestique.",
    ["Très silencieux, même en charge", "Alimentation intégrée", "Deux emplacements SSD"],
    ["Puissance limitée", "Pas de sortie vidéo par USB-C"],
    ("Mini-PC", "Intel N150"), cc("Beelink_EQ14"), man([("Clubic", 7.0, "https://www.clubic.com/ordinateur-pc/mini-pc/comparatif/")]))
CAT["beelink-ser9pro"] = P("d-mini", "Beelink SER9 Pro", "Ryzen 7 H 255 · 24 Go · 500 Go", "Le compact pour jouer léger",
    "Compact et silencieux, avec une bonne puce graphique intégrée pour le jeu occasionnel.",
    ["Bonne puce graphique intégrée", "Fonctionnement silencieux", "Format compact"],
    ["Pas de NPU pour les fonctions d'IA", "Les jeux récents exigeants restent hors de portée"],
    ("Mini-PC", "AMD Ryzen 7 H 255"), cc("Beelink_SER9+Pro"))
CAT["nipogi-am06pro"] = P("d-mini", "NiPoGi AM06 Pro", "Ryzen 5 7430U ou Ryzen 7 7730U · 16 ou 32 Go", "Le petit prix Ryzen",
    "Un Ryzen à prix serré, avec double réseau et un accès facile aux composants. Boîtier plastique et SSD lent.",
    ["Bon rapport qualité-prix", "Double réseau (dont 2,5 GbE)", "Composants faciles d'accès"],
    ["SSD lent", "RAM sur un seul module", "Boîtier plastique"],
    ("Mini-PC", "AMD Ryzen 5 7430U / Ryzen 7 7730U"), cc("NiPoGi_AM06+Pro"))
CAT["acemagic-k1"] = P("d-mini", "Acemagic K1", "Ryzen 5 7430U ou Core i5-12600H · 16 Go", "L'évolutif à petit prix",
    "Beaucoup de cœurs pour le prix, deux emplacements de RAM et deux emplacements SSD. Le matériel accuse toutefois son âge.",
    ["Très bon rapport performances/prix", "RAM et stockage évolutifs", "Sélection de ports utile"],
    ["Matériel vieillissant", "Puce graphique limitée"],
    ("Mini-PC", "AMD Ryzen 5 7430U / Intel Core i5-12600H"), cc("Acemagic_K1"), man([("Clubic", 7.0, "https://www.clubic.com/ordinateur-pc/mini-pc/comparatif/")]))
CAT["gmktec-k13"] = P("d-mini", "GMKtec NucBox K13", "Core Ultra 7 256V · 16 Go", "L'ultra-fin efficace",
    "Très fin, très discret et remarquablement sobre grâce à la plateforme Lunar Lake. La RAM soudée limite son évolution.",
    ["Format ultra-fin et léger", "Silencieux, chauffe maîtrisée", "Grande efficacité énergétique"],
    ["16 Go de RAM soudés", "Multicœur en retrait face aux Ryzen H"],
    ("Mini-PC ultra-fin", "Intel Core Ultra 7 256V"), cc("GMKtec_NucBox+K13"))

# ---------------------------------------------------------------- Tout-en-un
CAT["imac-m4"] = P("d-aio", "Apple iMac 24\" M4", "Écran 4,5K · puce M4 · 16 Go · 256 Go", TOP,
    "Le tout-en-un le plus abouti : écran 4,5K aux belles couleurs, puce M4 instantanée et design inimitable.",
    ["Puce M4 très réactive", "Écran 4,5K aux belles couleurs", "Design fin, sept couleurs"],
    ["Écran un peu juste en luminosité", "256 Go sur le modèle de base", "Aucune évolutivité"],
    ("Tout-en-un 24\"", "Apple M4"), cc("Apple_iMac+M4", "2024-10-01"))
CAT["omnistudio-x32"] = P("d-aio", "HP OmniStudio X 31,5\"", "Écran 4K · Core Ultra 7 · 32 Go", "Le plus grand écran",
    "Un grand écran 4K de 31,5 pouces, le Wi-Fi 7 et un seul câble sur le bureau : l'alternative Windows à l'iMac.",
    ["Grand écran 4K 31,5\"", "Clavier et souris inclus", "Wi-Fi 7"],
    ["Écran limité à 60 Hz", "Peu évolutif"],
    ("Tout-en-un 31,5\" 4K", "Intel Core Ultra 7"), cc("HP_OmniStudio+X+32", "2025-01-01"),
    man([("ITdaily", None, "https://itdaily.com/reviews/workplace/hp-omnistudio-x-review-modern-all-rounder/")]))
CAT["omnistudio-x27"] = P("d-aio", "HP OmniStudio X 27\"", "Core Ultra 7 · 16 à 24 Go · 1 To", "Le 27 pouces premium",
    "La version 27 pouces de l'OmniStudio X : même soin de fabrication, encombrement réduit.",
    ["Écran 27\" de qualité", "Finition soignée", "Bonne webcam"],
    ["Prix élevé", "Peu évolutif"],
    ("Tout-en-un 27\"", "Intel Core Ultra 7"), cc("HP_OmniStudio+X", "2025-01-01"))
CAT["hp-omnistudio-27"] = P("d-aio", "HP OmniStudio 27\"", "27-cv · Ryzen 5 · 8 Go · 512 Go", "Le 27 pouces abordable",
    "Un grand écran et un seul câble pour un budget contenu : suffisant pour la famille et la bureautique.",
    ["Grand écran 27\"", "Prix abordable", "Encombrement réduit"],
    ["8 Go de RAM", "Performances modestes"],
    ("Tout-en-un 27\" Full HD", "AMD Ryzen 5"), man([(CR, None, "https://www.consumerreports.org/electronics-computers/computers/hp-27-touch-screen-all-in-one-27-cr0044/m417619/")], "gamme"))
CAT["yoga-aio-32"] = P("d-aio", "Lenovo Yoga AIO 32", "31,5\" · Core Ultra · 32 Go · 1 To", "Le haut de gamme Windows",
    "Écran 31,5 pouces superbe, design travaillé et très bon son : le tout-en-un Windows le plus ambitieux, noté 9/10 dans sa version précédente.",
    ["Grand écran 4K superbe", "Design et son soignés", "32 Go de RAM"],
    ["Prix très élevé", "Peu évolutif"],
    ("Tout-en-un 31,5\"", "Intel Core Ultra"), cc("Lenovo_Yoga+AIO+9i", "2025-01-01", scope="gamme"))
CAT["ideacentre-aio-27"] = P("d-aio", "Lenovo IdeaCentre AIO 27", "27\" · Ryzen AI ou Core · 16 Go · 512 Go", "Le familial",
    "Un tout-en-un 27 pouces économe. PCMag et CNET regrettent sa définition Full HD et sa webcam.",
    ["Grand écran pour le prix", "16 Go de RAM", "Encombrement réduit"],
    ["Définition Full HD sur 27\"", "Webcam médiocre"],
    ("Tout-en-un 27\"", "Ryzen AI 5 / Core 5"),
    man([("CNET", 6.4, "https://www.cnet.com/tech/computing/lenovo-ideacentre-aio-27-review-this-budget-all-in-one-pc-is-bigger-not-better/"),
         ("PCMag", None, "https://www.pcmag.com/reviews/lenovo-ideacentre-aio-27")], "gamme"))
CAT["asus-v400"] = P("d-aio", "Asus V400 AiO", "V440 / V470 · 24\" ou 27\" · Intel Core", "Le minimaliste",
    "Un tout-en-un fin et sobre, en 24 ou 27 pouces, bien équipé en mémoire et en stockage dans ses versions Core 7.",
    ["Design fin et minimaliste", "Jusqu'à 32 Go de RAM et 2 To", "Écran 100 Hz sur certaines versions"],
    ["Écran Full HD", "Peu de tests presse"],
    ("Tout-en-un 23,8\" ou 27\"", "Intel Core 5 / 7"), man([("All of the Above", None, "https://www.alloftheaboveph.com/2025/10/review-asus-v400-aio-all-in-one-you-need.html")], "gamme"))
CAT["aspire-c27"] = P("d-aio", "Acer Aspire C 27", "C27B · 27\" Full HD 144 Hz · Ryzen 5 · 8 Go", "Le 144 Hz",
    "Un tout-en-un 27 pouces à l'écran fluide et bien réglable. Les générations précédentes étaient notées autour de 4/5.",
    ["Écran 27\" 144 Hz", "Pied réglable", "Design sobre"],
    ["8 Go de RAM sur l'entrée de gamme", "Clavier et souris non inclus"],
    ("Tout-en-un 27\"", "AMD Ryzen 5"), cc("Acer_Aspire+C27", "2022-01-01", scope="gamme"),
    man([("PCMag (prise en main)", None, "https://www.pcmag.com/news/hands-on-acers-aspire-c27-all-in-one-pc-brings-class-and-speed-to-office")], "gamme"))
CAT["dell-24-aio"] = P("d-aio", "Dell 24 Tout-en-un", "EC24250 · 23,8\" Full HD · Core i5", "Le milieu de gamme sûr",
    "Un tout-en-un abordable avec un écran aux couleurs vives, un bon son et une webcam efficace, selon PCMag.",
    ["Écran coloré", "Son et webcam de qualité", "Prix abordable"],
    ["Performances moyennes", "Écran 24\" Full HD seulement"],
    ("Tout-en-un 23,8\"", "Intel Core i5"), man([("PCMag", 7.0, "https://www.pcmag.com/reviews/dell-24-all-in-one-ec24250")]))
CAT["msi-modern-am273"] = P("d-aio", "MSI Modern AM273Q AI", "27\" WQHD · Core Ultra · 16 ou 32 Go", "Le tout-en-un écran",
    "Un 27 pouces WQHD qui peut aussi servir d'écran pour un autre appareil : une polyvalence rare sur un tout-en-un.",
    ["Écran 27\" WQHD", "Utilisable comme moniteur externe", "RAM et stockage accessibles"],
    ["Peu de tests presse", "Design classique"],
    ("Tout-en-un 27\" WQHD", "Intel Core Ultra 5 / 7"), man([("The Shortcut", None, "https://www.theshortcut.com/p/msi-modern-am273q-ai-aio-pc-audioscenic-amphi")]))
