# -*- coding: utf-8 -*-
"""Guides d'achat des 4 pages de rubrique Informatique (décision de Matthieu du 13/11/2026, plan Gemini point C).

Conseils techniques généraux rédigés à la main : aucun prix, aucune note ni aucun produit n'est écrit ici.
Les fourchettes de prix par usage et les chiffres de l'introduction sont calculés par gen10.py à partir de data.json.
« pour_qui » : une phrase par usage (clé = clé d'usage dans familles), affichée dans le tableau « Quel usage pour vous ? ».
"""

GUIDES_RUB = {
    "laptop": {
        "titre": "Guide d'achat : bien choisir son PC portable",
        "intro": "Un PC portable se choisit d'abord par l'usage, ensuite par le budget. Les fiches techniques se ressemblent toutes ; ce qui sépare un bon achat d'une déception tient le plus souvent à quatre ou cinq points que la presse vérifie en test et que les vendeurs mettent rarement en avant.",
        "criteres": [
            ("Le processeur selon l'usage", "Pour la bureautique, n'importe quel processeur récent d'entrée de gamme suffit. La création et le jeu demandent un processeur de série H (Intel Core Ultra H, AMD Ryzen HX) et surtout une carte graphique dédiée. Les puces ARM (Snapdragon X, Apple M) offrent la meilleure autonomie, au prix d'une compatibilité à vérifier sous Windows."),
            ("La mémoire et le stockage", "16 Go de RAM sont devenus le bon standard ; 8 Go suffisent tout juste à la navigation. La mémoire est souvent soudée : ce que vous achetez est ce que vous garderez. Côté stockage, 512 Go en SSD est un minimum confortable, 1 To pour la photo, la vidéo ou les jeux."),
            ("L'écran", "La définition Full HD est le minimum ; le format 16:10 affiche plus de lignes qu'un 16:9 à diagonale égale. Une dalle OLED offre un contraste bien supérieur, une dalle IPS mate fatigue moins en plein jour. Pour le jeu, une fréquence de 120 Hz ou plus change la fluidité."),
            ("Le poids et l'autonomie", "Sous 1,4 kg, un portable se transporte tous les jours sans y penser ; au-delà de 2 kg, il reste surtout sur un bureau. L'autonomie annoncée par le fabricant est mesurée dans des conditions favorables : les tests de la presse donnent une durée plus réaliste."),
            ("La connectique", "Un port USB-C compatible charge et affichage permet de brancher un seul câble au bureau. Un port HDMI et un lecteur de carte évitent les adaptateurs. Vérifiez aussi le Wi-Fi 6E ou 7 si vous comptez garder la machine longtemps."),
        ],
        "pieges": [
            "La RAM soudée en 8 Go, impossible à faire évoluer.",
            "Une carte graphique « gaming » bridée par une puissance électrique (TGP) basse : à configuration égale, les performances varient beaucoup d'un modèle à l'autre.",
            "L'autonomie annoncée prise au pied de la lettre.",
            "Un modèle vendu sous le même nom dans plusieurs configurations : vérifiez celle de l'offre avant d'acheter.",
        ],
    },
    "desktop": {
        "titre": "Guide d'achat : bien choisir son ordinateur de bureau",
        "intro": "Un ordinateur de bureau ne se transporte pas : on peut donc privilégier la puissance, le silence et l'évolutivité. Le premier choix est le format, qui conditionne tout le reste.",
        "criteres": [
            ("Le format", "Le mini-PC tient dans une main et suffit à la bureautique et au multimédia. Le tout-en-un intègre l'écran et libère le bureau, mais se répare et s'améliore difficilement. La tour reste le seul format qui accepte une grosse carte graphique et des évolutions faciles."),
            ("Le processeur et la carte graphique", "Pour la bureautique, un processeur récent de milieu de gamme et la partie graphique intégrée suffisent. La création vidéo et le jeu demandent une carte graphique dédiée : c'est elle qui fait l'essentiel de la différence en jeu."),
            ("La mémoire et le stockage", "16 Go de RAM au minimum pour un usage général, 32 Go pour la création. Un SSD NVMe d'au moins 512 Go ; sur une tour ou certains mini-PC, un second emplacement permet d'ajouter du stockage plus tard."),
            ("Le bruit et la chauffe", "Un mini-PC très compact peut ventiler fort sous charge ; une tour bien ventilée reste plus silencieuse à puissance égale. Les tests de la presse mesurent souvent le bruit : c'est un critère à regarder si l'ordinateur reste dans une pièce de vie."),
            ("La connectique et l'évolutivité", "Comptez les ports USB en façade, la sortie vidéo (HDMI, DisplayPort, USB-C) et le nombre d'écrans pris en charge. Vérifiez si la RAM et le stockage sont accessibles : c'est ce qui prolonge la vie d'un ordinateur."),
        ],
        "pieges": [
            "Un mini-PC vendu sans système d'exploitation, ou avec une version d'évaluation.",
            "Un tout-en-un dont l'écran tombe en panne : tout l'ordinateur part en réparation.",
            "Une tour « gaming » avec une alimentation de qualité médiocre, qui limite les évolutions.",
            "Une configuration annoncée « jusqu'à » : vérifiez celle de l'offre réellement vendue.",
        ],
    },
    "ecran": {
        "titre": "Guide d'achat : bien choisir son écran PC",
        "intro": "Un écran se garde souvent plus longtemps que l'ordinateur qu'on y branche. Trois choix structurent l'achat : la taille et la définition, le type de dalle, puis la fréquence. Le reste (pied, connectique, réglages) fait la différence au quotidien.",
        "criteres": [
            ("La taille et la définition", "En 24 pouces, le Full HD reste lisible ; en 27 pouces, le QHD (2560 × 1440) est le bon standard ; au-delà, ou pour la retouche photo, la 4K apporte une image plus fine. Plus la définition monte, plus la carte graphique doit suivre en jeu."),
            ("Le type de dalle", "L'IPS offre de bonnes couleurs et de bons angles de vision ; la VA un meilleur contraste ; l'OLED un contraste infini et une réactivité immédiate, avec un risque de marquage sur les éléments fixes que les fabricants compensent par des garanties et des cycles de rafraîchissement."),
            ("La fréquence", "60 Hz suffisent pour la bureautique. En jeu, 144 Hz et plus apportent une fluidité nette ; au-delà de 240 Hz, la différence concerne surtout les joueurs compétitifs. La compatibilité FreeSync ou G-Sync évite les déchirures d'image."),
            ("La connectique", "Un port USB-C avec charge du portable (Power Delivery) permet de tout brancher avec un seul câble ; vérifiez la puissance annoncée, de 15 à 90 W selon les modèles. Un concentrateur USB intégré et une sortie DisplayPort pour chaîner un second écran sont des plus."),
            ("L'ergonomie", "Un pied réglable en hauteur et en inclinaison soulage la nuque. La compatibilité VESA permet de passer à un bras articulé. Une dalle mate limite les reflets dans une pièce lumineuse."),
        ],
        "pieges": [
            "Une luminosité HDR « 400 » qui ne donne pas un vrai rendu HDR.",
            "Un temps de réponse annoncé en « MPRT » ou mesuré en mode extrême, peu comparable d'un fabricant à l'autre.",
            "Un port USB-C qui transporte l'image mais ne charge pas le portable.",
            "Un écran 4K de petite taille utilisé sans mise à l'échelle : textes minuscules.",
        ],
    },
    "imprimante": {
        "titre": "Guide d'achat : bien choisir son imprimante",
        "intro": "Le prix d'une imprimante se joue sur la durée : le coût de l'encre ou du toner pèse vite plus que l'appareil. Le bon choix dépend d'abord du volume imprimé et du besoin de couleur.",
        "criteres": [
            ("Jet d'encre ou laser", "La laser imprime vite et proprement du texte, et le toner ne sèche pas : idéale si vous imprimez irrégulièrement. Le jet d'encre rend mieux les photos et les couleurs, mais les buses peuvent sécher si l'imprimante reste longtemps inutilisée."),
            ("Cartouches ou réservoirs", "Les modèles à réservoirs rechargeables coûtent plus cher à l'achat mais divisent le coût par page ; ils deviennent rentables dès que vous imprimez régulièrement. Les cartouches conviennent à un usage occasionnel."),
            ("Les fonctions", "Un multifonction ajoute la copie et la numérisation. Le chargeur automatique de documents fait gagner du temps pour scanner plusieurs pages ; le recto-verso automatique économise le papier."),
            ("La vitesse", "Comparez les vitesses mesurées selon la norme ISO (ipm), plus réalistes que les vitesses « brouillon » parfois mises en avant. Pour la photo, regardez plutôt le temps par tirage."),
            ("La connexion", "Le Wi-Fi et l'application mobile sont devenus la norme ; vérifiez la compatibilité avec votre système et la possibilité d'imprimer sans créer de compte en ligne."),
        ],
        "pieges": [
            "Les abonnements d'encre activés par défaut à l'installation.",
            "Les cartouches de démarrage, peu remplies, fournies avec l'imprimante.",
            "Les mises à jour qui bloquent les cartouches compatibles : vérifiez la politique du fabricant.",
            "Une laser couleur choisie pour la photo : le rendu reste en retrait du jet d'encre.",
        ],
    },
}

# Pour qui, par usage (clé d'usage de familles). Phrase courte, sans prix ni produit.
POUR_QUI = {
    # PC portables
    "bureau": "Traitement de texte, tableurs, visio et navigation, au bureau comme en déplacement.",
    "creation": "Retouche photo, montage vidéo, 3D : écran fidèle et carte graphique dédiée.",
    "gaming": "Jeux récents en bonne qualité : carte graphique dédiée et écran rapide.",
    "polyvalent": "Un seul ordinateur pour tout faire, du travail aux loisirs.",
    "lowcost": "Les besoins essentiels à petit budget.",
    "reconditionne": "Un PC portable professionnel reconditionné, contrôlé et garanti par le vendeur.",
    # Ordinateurs de bureau
    "d-bureau": "Bureautique, gestion et navigation, pour la maison ou le bureau.",
    "d-creation": "Montage vidéo, 3D, gros fichiers : processeur et carte graphique puissants.",
    "d-gaming": "Jeux récents en haute qualité, avec une carte graphique dédiée.",
    "d-mini": "Un ordinateur discret à poser derrière un écran ou sous une TV.",
    "d-aio": "Un ordinateur et son écran en un seul appareil, sans câbles sur le bureau.",
    # Écrans
    "e-bureau": "Travail et télétravail : confort visuel et un seul câble pour le portable.",
    "e-gaming": "Jeu : fréquence élevée, faible temps de réponse.",
    "e-creation": "Photo et graphisme : couleurs fidèles et bonne couverture colorimétrique.",
    "e-portable": "Un second écran léger pour le portable, en déplacement.",
    "e-lowcost": "Un écran correct à petit budget.",
    # Imprimantes
    "i-reservoir": "Impression régulière en couleur, avec un coût par page réduit.",
    "i-laser-mono": "Beaucoup de texte, vite, sans souci d'encre qui sèche.",
    "i-laser-couleur": "Documents en couleur au bureau, en volume.",
    "i-photo": "Tirages photo à la maison.",
    "i-lowcost": "Impression occasionnelle à petit budget.",
}
