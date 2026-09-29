# -*- coding: utf-8 -*-
"""Guides d'achat — ordinateurs de bureau (version préparatoire)."""

GUIDES_DESK = {
"d-bureau": dict(
    titre="Comment choisir un ordinateur de bureau pour la bureautique",
    intro="Pour le travail et la famille, pas besoin d'une machine de guerre : un processeur récent de milieu de gamme suffit largement. Misez plutôt sur <b>la fiabilité, le silence et la capacité à évoluer</b> — c'est le grand avantage du fixe sur le portable.",
    criteres=[
        ("Processeur", "Un Intel Core i5 / Core Ultra 5 ou un AMD Ryzen 5 récent couvre tous les usages bureautiques pour des années. Une puce Apple M4 fait aussi très bien l'affaire."),
        ("Mémoire", "16 Go de RAM pour être tranquille, et un SSD de 512 Go. Sur une tour, vous pourrez en ajouter plus tard."),
        ("Format", "Tour pour évoluer, tour compacte pour gagner de la place, mini-PC pour disparaître derrière l'écran."),
        ("Connectique", "Des ports USB en façade, du Wi-Fi 6 et au moins deux sorties vidéo si vous travaillez sur deux écrans."),
    ],
    pieges=["Les disques durs mécaniques seuls (sans SSD) : l'ordinateur paraîtra lent dès le premier jour.",
            "Les 8 Go de RAM soudés sur les modèles compacts.",
            "Oublier le budget de l'écran, du clavier et de la souris, souvent non fournis."],
    budget=[("400 – 700 €", "L'essentiel pour la bureautique familiale."), ("700 – 1 000 €", "Le confort : plus rapide, plus silencieux, plus évolutif.")],
),
"d-creation": dict(
    titre="Comment choisir un ordinateur de bureau pour la création",
    intro="Photo, vidéo, 3D : le fixe reste le roi de la <b>puissance soutenue</b>. Il ne chauffe pas, ne bride pas ses performances et accepte plusieurs écrans. Le choix se joue entre l'écosystème Apple, très efficace, et les stations Windows, plus évolutives.",
    criteres=[
        ("Processeur et GPU", "Apple M4 Pro / M4 Max, ou un processeur Intel / AMD haut de gamme associé à une carte graphique NVIDIA RTX pour l'accélération des exports et de la 3D."),
        ("Mémoire", "32 Go au minimum pour la vidéo 4K, 64 Go et plus pour la 3D et les gros projets."),
        ("Stockage", "1 To de SSD rapide pour le système et les projets en cours, plus un disque d'archive."),
        ("Connectique", "Thunderbolt pour les disques externes rapides, et assez de sorties vidéo pour un écran de retouche calibré."),
    ],
    pieges=["Un bel ordinateur branché sur un écran médiocre : prévoyez un écran fidèle en couleurs.",
            "La mémoire non évolutive des Mac : choisissez la bonne quantité dès l'achat.",
            "Les cartes graphiques « gaming » sans pilotes certifiés pour certains logiciels pros."],
    budget=[("1 500 – 2 500 €", "Le cœur du marché créatif."), ("Au-delà", "Les stations de travail pour la 3D et la vidéo 8K.")],
),
"d-gaming": dict(
    titre="Comment choisir un PC gamer fixe",
    intro="À budget égal, une tour gaming offre <b>plus de puissance et moins de bruit</b> qu'un portable, et peut évoluer au fil des années. Comme pour les portables, la carte graphique décide de presque tout.",
    criteres=[
        ("Carte graphique", "RTX 5060 Ti pour le 1080p/1440p, RTX 5070 pour le 1440p élevé, RTX 5080 et plus pour la 4K."),
        ("Processeur", "Un Core i5/i7 ou Ryzen 5/7 récent suffit ; les processeurs AMD X3D sont les plus efficaces en jeu."),
        ("Alimentation et refroidissement", "Une alimentation de marque et un boîtier bien ventilé garantissent la stabilité et le silence."),
        ("Évolutivité", "Vérifiez qu'il reste de la place pour une carte graphique plus grosse et des emplacements libres pour la mémoire et les SSD."),
    ],
    pieges=["Les PC « gamer » à gros processeur mais petite carte graphique.",
            "Les alimentations sans marque, sources de pannes.",
            "Les formats propriétaires qui empêchent de changer les pièces."],
    budget=[("1 000 – 1 500 €", "Le 1080p/1440p confortable."), ("1 500 – 2 500 €", "Le 1440p élevé et la 4K raisonnable."), ("Au-delà", "La 4K sans compromis.")],
),
"d-mini": dict(
    titre="Comment choisir un mini-PC",
    intro="Pas plus gros qu'un livre, un mini-PC se fixe derrière l'écran et remplace une tour pour la bureautique, le multimédia et même un peu de création. La clé : <b>ne pas sous-estimer le processeur</b>.",
    criteres=[
        ("Processeur", "Intel N100/N150 pour le web et la vidéo ; Ryzen 5/7 ou Core i5/i7 pour un vrai usage polyvalent ; Ryzen AI 9 pour la création légère."),
        ("Mémoire et stockage", "16 Go et un SSD NVMe de 512 Go. Vérifiez que la RAM n'est pas soudée."),
        ("Connectique", "Deux sorties vidéo, de l'USB-C et un port Ethernet ; le Wi-Fi 6 au minimum."),
        ("Bruit", "Les modèles puissants ventilent : lisez les tests si le silence compte."),
    ],
    pieges=["Les marques inconnues sans support ni mises à jour du BIOS.",
            "Les stockages eMMC lents sur les modèles d'entrée de gamme.",
            "Les licences Windows douteuses sur certains modèles très bon marché."],
    budget=[("250 – 400 €", "Bureautique, multimédia, PC de salon."), ("400 – 900 €", "Polyvalent et rapide."), ("Au-delà", "Mini-stations pour la création.")],
),
"d-aio": dict(
    titre="Comment choisir un ordinateur tout-en-un",
    intro="Un seul câble, un bureau épuré : le tout-en-un intègre l'ordinateur dans l'écran. Revers de la médaille, <b>on ne peut presque rien faire évoluer</b> : l'écran et la configuration doivent être bien choisis dès le départ.",
    criteres=[
        ("L'écran avant tout", "24 pouces pour un coin famille, 27 à 32 pouces pour travailler. Au-delà du Full HD, une définition 4K ou 4,5K change le confort de lecture."),
        ("Processeur et mémoire", "16 Go de RAM et un processeur récent, puisque rien ne s'upgrade ensuite."),
        ("Ergonomie", "Pied réglable en hauteur, webcam de qualité et haut-parleurs corrects : on s'en sert tous les jours."),
        ("Connectique", "Assez de ports USB accessibles, idéalement sur le côté ou en façade."),
    ],
    pieges=["Les écrans Full HD en 27 pouces : image peu nette de près.",
            "Les configurations 8 Go non évolutives.",
            "Les pieds non réglables, sources de mauvaise posture."],
    budget=[("700 – 1 000 €", "L'usage familial."), ("1 000 – 2 000 €", "Grand écran de qualité pour travailler."), ("Au-delà", "Les modèles haut de gamme 4K et plus.")],
),
}
