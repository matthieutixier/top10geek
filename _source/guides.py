# -*- coding: utf-8 -*-
"""Guides d'achat par usage — contenu éditorial original Top 10 Geek (septembre 2026)."""

GUIDES = {
"bureau": dict(
    titre="Comment choisir un PC portable pour la bureautique",
    intro="Traitement de texte, tableurs, visio, navigation : un PC bureautique n'a pas besoin d'être puissant, il doit être <b>endurant, léger et agréable à utiliser toute la journée</b>. La puissance brute est presque secondaire : n'importe quel processeur récent suffit. Ce qui fait la différence au quotidien, c'est ce que l'on voit, ce que l'on porte et ce que l'on recharge.",
    criteres=[
        ("Autonomie", "Visez au moins 10 heures annoncées. Les puces ARM (Snapdragon X, Apple M) dépassent souvent 15 heures réelles et permettent d'oublier le chargeur pour la journée."),
        ("Poids", "Si vous le transportez tous les jours, restez sous 1,5 kg. Un 14 pouces est le meilleur compromis entre confort de lecture et encombrement."),
        ("Écran", "Full HD minimum, idéalement en 16:10 (plus de lignes visibles dans un tableur). Une dalle IPS ou OLED lumineuse (300 nits et plus) fatigue moins les yeux."),
        ("Mémoire", "16 Go de RAM rendent la machine fluide pour plusieurs années ; 8 Go suffisent tout juste. Côté stockage, 512 Go en SSD est le bon standard."),
    ],
    pieges=[
        "La RAM soudée en 8 Go : impossible à faire évoluer, elle devient vite juste.",
        "Les écrans HD (1366 × 768) encore présents sur certains modèles : à éviter.",
        "Windows sur puce ARM : vérifiez la compatibilité de vos logiciels métier, VPN et imprimantes avant d'acheter.",
        "Le clavier non rétroéclairé, gênant dès qu'on travaille le soir.",
    ],
    budget=[("500 – 800 €", "Le bon rapport qualité-prix : tout le nécessaire, finition plus simple."),
            ("800 – 1 200 €", "Le confort : écran OLED, châssis métal, grosse autonomie."),
            ("Au-delà", "Le premium : poids plume, finition haut de gamme — un plaisir, pas une nécessité.")],
),
"creation": dict(
    titre="Comment choisir un PC portable pour la création",
    intro="Retouche photo, montage vidéo, graphisme : ici, <b>l'écran compte autant que le processeur</b>. Un PC très puissant avec une dalle aux couleurs fausses vous fera livrer des images qui ne ressemblent pas à ce que vous avez vu. Viennent ensuite la carte graphique, qui accélère les exports, et la mémoire, qui évite les ralentissements sur les gros projets.",
    criteres=[
        ("Fidélité de l'écran", "Pour la photo, 100 % sRGB au minimum ; pour la vidéo, visez une large couverture DCI-P3. Un calibrage d'usine certifié (Pantone, Calman) est un vrai plus. Les dalles OLED et Mini-LED offrent les meilleurs contrastes."),
        ("Carte graphique", "Une RTX 5060 ou 5070 accélère nettement l'export vidéo, les effets et les outils d'IA. Les puces Apple M sont, elles, remarquables en montage grâce à leurs accélérateurs dédiés."),
        ("Mémoire et stockage", "32 Go de RAM pour la vidéo 4K et les gros fichiers RAW, 1 To de SSD au minimum : les projets vidéo remplissent vite un disque."),
        ("Connectique", "Un lecteur de cartes SD et un port Thunderbolt ou USB4 font gagner un temps précieux pour décharger les rushs et brancher un écran externe."),
    ],
    pieges=[
        "Les écrans « 100 % sRGB » non calibrés : la couverture ne garantit pas la justesse des couleurs.",
        "Le scintillement (PWM) de certains OLED, fatigant pour les yeux sensibles lors de longues sessions.",
        "16 Go de RAM soudés sur une machine destinée à la vidéo : un goulot d'étranglement définitif.",
        "Confondre PC gaming et PC créateur : un écran 240 Hz rapide n'est pas forcément fidèle en couleurs.",
    ],
    budget=[("1 300 – 1 800 €", "L'entrée de gamme créateur : bonne dalle, GPU d'entrée de gamme."),
            ("1 800 – 2 500 €", "Le cœur du marché : écran calibré, RTX 5070 ou puce Apple M, 32 Go."),
            ("Au-delà", "Le matériel pro : Mini-LED ou OLED haut de gamme, GPU puissant, pour la 4K/6K.")],
),
"gaming": dict(
    titre="Comment choisir un PC portable gaming",
    intro="En jeu, <b>la carte graphique décide de presque tout</b> : c'est elle qui fixe la définition et la fluidité auxquelles vous jouerez. Mais un bon GPU mal refroidi perd une partie de ses performances et fait beaucoup de bruit. Un PC gaming se juge donc sur trois choses : le GPU, l'écran qui l'affiche, et le châssis qui le refroidit.",
    criteres=[
        ("Carte graphique", "RTX 5060 pour jouer en 1080p en qualité élevée, RTX 5070 pour le 1440p, RTX 5070 Ti ou 5080 pour tout pousser au maximum. Vérifiez sa puissance allouée (TGP) : la même carte peut être bridée d'un modèle à l'autre."),
        ("Écran", "144 Hz minimum, 165 à 240 Hz idéalement, en 1440p (2,5K) sur un 16 pouces. Un temps de réponse rapide évite les traînées dans les jeux nerveux."),
        ("Refroidissement et bruit", "C'est ce qui sépare les bons modèles des autres : un châssis bien ventilé tient ses performances sans hurler. Les tests presse sont précieux sur ce point."),
        ("Mémoire et stockage", "16 Go de RAM minimum, 32 Go pour être tranquille. 1 To de SSD : les jeux récents pèsent souvent plus de 100 Go chacun."),
    ],
    pieges=[
        "Deux PC avec la même RTX peuvent avoir des performances très différentes selon le TGP et le refroidissement.",
        "L'autonomie en jeu dépasse rarement 1 à 2 heures : un PC gaming se joue branché.",
        "Le poids réel : 2,4 kg et plus, sans compter un bloc d'alimentation souvent massif.",
        "Les écrans lents qui laissent des traînées, et les SSD de 512 Go vite saturés.",
    ],
    budget=[("1 000 – 1 300 €", "L'entrée de gamme : RTX 5050 ou 5060, pour le 1080p."),
            ("1 300 – 1 800 €", "Le meilleur équilibre : RTX 5060 ou 5070, écran rapide, bon refroidissement."),
            ("Au-delà de 2 000 €", "Le haut de gamme : RTX 5070 Ti et plus, grands écrans 240 Hz.")],
),
"polyvalent": dict(
    titre="Comment choisir un PC portable polyvalent",
    intro="Études, travail, loisirs, un peu de retouche : un PC polyvalent doit tout faire correctement <b>sans point faible rédhibitoire</b>. C'est la machine que l'on garde quatre ou cinq ans, donc celle où il faut éviter les économies qui se paient plus tard : mémoire trop juste, écran terne, processeur d'ancienne génération.",
    criteres=[
        ("Processeur récent", "Intel Core Ultra, AMD Ryzen AI, Snapdragon X ou Apple M : toutes ces puces récentes offrent un excellent équilibre entre performances et autonomie."),
        ("16 Go de RAM", "C'est le seuil qui garantit une machine fluide dans la durée, avec de nombreux onglets et applications ouverts. Associez-les à 512 Go ou 1 To de SSD."),
        ("Format", "13 à 14 pouces si vous le transportez beaucoup, 16 pouces si le confort d'affichage prime. Vérifiez le poids : sous 1,4 kg pour un 14 pouces nomade."),
        ("Connectique et webcam", "Au moins un USB-C pour la charge, un USB-A et un HDMI. Une webcam 1080p rend les visios nettement plus agréables."),
    ],
    pieges=[
        "Les « bonnes affaires » sur des générations anciennes : un prix bas cache parfois un processeur de trois ans.",
        "Les écrans ternes (moins de 300 nits, couleurs délavées) qui gâchent l'usage multimédia.",
        "Les 8 Go de RAM soudés sur une machine censée durer cinq ans.",
        "Les 2-en-1 lourds : pratiques en théorie, encombrants au quotidien.",
    ],
    budget=[("700 – 1 000 €", "Le meilleur ratio : processeur récent, 16 Go, souvent un écran OLED."),
            ("1 000 – 1 600 €", "Le premium polyvalent : finition métal, grosse autonomie, écran haut de gamme."),
            ("Au-delà", "Les ultraportables d'exception : légèreté et finition, à réserver aux nomades exigeants.")],
),
"lowcost": dict(
    titre="Comment choisir un PC portable à moins de 500 €",
    intro="À petit prix, <b>chaque compromis compte</b>. On peut trouver de très bonnes machines pour la bureautique, les cours et le multimédia, à condition de savoir où ne pas transiger : le processeur, le type de stockage et la qualité de l'écran. Le reconditionné avec garantie est aussi une excellente piste pour monter en gamme sans dépasser le budget.",
    criteres=[
        ("Processeur", "Privilégiez un AMD Ryzen 5 ou un Intel Core i5 / Core 3 récent. Les Celeron, Pentium et puces « N » conviennent seulement à un usage très basique (web, mails)."),
        ("Stockage", "Un vrai SSD de 256 Go minimum, 512 Go idéalement. Fuyez la mémoire eMMC : lente et souvent limitée à 64 ou 128 Go, elle se remplit avec les seules mises à jour de Windows."),
        ("Écran", "Full HD (1920 × 1080) en dalle IPS : c'est le seuil du confort. Les écrans HD et les dalles TN aux angles de vision médiocres sont à éviter."),
        ("RAM", "8 Go minimum. En dessous, Windows 11 rame dès quelques onglets ouverts."),
    ],
    pieges=[
        "Le stockage eMMC de 64 ou 128 Go, vite saturé et impossible à remplacer.",
        "Le « mode S » de Windows, qui limite l'installation de logiciels (désactivable, mais à savoir).",
        "Les 4 Go de RAM, encore présents sur certains modèles d'appel.",
        "Les faux prix barrés : un « −30 % » sur un prix de référence gonflé n'est pas une bonne affaire.",
    ],
    budget=[("350 – 450 €", "Usages basiques : web, mails, bureautique légère."),
            ("450 – 500 €", "Le meilleur compromis : Ryzen 5, SSD 512 Go, écran Full HD."),
            ("Reconditionné", "Un modèle de gamme supérieure, garanti, pour le même budget.")],
),
}
