# -*- coding: utf-8 -*-
"""Rubrique « Reconditionnés » (ajoutée le 26/10/2026) : 10 PC portables professionnels reconditionnés vendus par
PC-Portable.net (programme Effinity). Le test presse porte sur le MODÈLE (testé neuf à sa sortie), pas sur l'exemplaire vendu.

Champs : short, ref, badge, verdict, strengths, weak, m (poids, autonomie), pour / eviter, notes
(média, note sur 10 ou None, adresse du test, date du test, date de relecture à la source ou None), flux (identifiant de
l'annonce retenue dans le flux PC-Portable.net, expression de recherche et exclusion pour retrouver une annonce
équivalente si elle disparaît : voir pcportable.py).
Notebookcheck note sur 100 : la note du site est ce pourcentage divisé par 10, arrondi à 0,1 (84,8 % -> 8,5).
Relecture à la source faite le 26/10/2026 sur la page du média (champ « verifie »). LaptopMedia et LaptopMag ne publient
pas de note chiffrée : test cité et lié, sans note."""

V = "26/10/2026"

RECO = {
    "latitude-5420": dict(
        short="Dell Latitude 5420", ref='14" · Core i5-1145G7 · Thunderbolt 4',
        badge="Le plus récent du lot",
        verdict="Le plus récent des dix (11e génération Intel) : connectique complète, deux ports Thunderbolt 4 et une autonomie de deux journées de bureau dans le test LaptopMedia. L'écran, terne, est son point faible.",
        strengths=["Deux ports Thunderbolt 4, RJ-45, lecteur de carte à puce", "Entretien facile, mémoire non soudée", "Autonomie annoncée sur deux journées (LaptopMedia)"],
        weak=["Écran peu lumineux, 54 % du sRGB", "Pavé tactile sans boutons dédiés ni trackpoint, jugé en retrait"],
        m=("≈ 1,5 kg", "≈ 19 h (web, LaptopMedia)"),
        pour="Vous voulez le portable pro reconditionné le plus récent de la sélection, avec Thunderbolt 4 et un port Ethernet.",
        eviter="Vous retouchez des photos ou regardez beaucoup de vidéos : la dalle est terne et peu lumineuse.",
        notes=[("Notebookcheck", 8.5, "https://www.notebookcheck.net/Dell-Latitude-14-5420-review-A-laptop-so-close-to-claiming-the-business-crown.595678.0.html", "2022-01-27", V),
               ("LaptopMedia", None, "https://laptopmedia.com/gb/review/dell-latitude-14-5420-review-it-will-effortlessly-last-you-through-two-workdays-on-a-single-charge/", "2021-06-01", None)],
        flux=dict(ppid="4741", re=r"\b5420\b", non=r"SFF|QWERTZ")),
    "thinkpad-t14-gen1": dict(
        short="Lenovo ThinkPad T14 Gen 1 (AMD)", ref='14" · Ryzen 5 PRO 4650U',
        badge="Le plus puissant",
        verdict="La puce Ryzen 5 PRO 4650U surclasse les Intel de son époque, l'écran est lumineux et contrasté pour un PC pro : le test Notebookcheck le décrit comme le meilleur portable d'entreprise qu'on puisse acheter à sa sortie.",
        strengths=["Ryzen 5 PRO 4650U, très rapide pour de la bureautique", "Écran lumineux et contrasté, dalle mate", "Mémoire extensible, HDMI 2.0 (4K à 60 Hz)"],
        weak=["Pas de Thunderbolt 3", "Écran lent, images rémanentes visibles", "Mémoire en simple canal sur l'exemplaire testé"],
        m=("≈ 1,5 kg", "n.c."),
        pour="Vous voulez la machine la plus rapide de la sélection pour travailler, avec un bon écran mat.",
        eviter="Vous avez besoin de Thunderbolt pour une station d'accueil, ou d'un écran très réactif pour jouer.",
        notes=[("Notebookcheck", 8.9, "https://www.notebookcheck.org/Review-del-Lenovo-ThinkPad-T14-AMD-El-mejor-portatil-para-empresas-que-se-puede-comprar.505020.0.html", "2020-11-18", V)],
        flux=dict(ppid="5106", re=r"\bT14\b.*RYZEN|\bT14 G1\b", non=r"QWERTZ")),
    "thinkpad-t490": dict(
        short="Lenovo ThinkPad T490", ref='14" · Core i5 8e génération',
        badge="Le plus équilibré",
        verdict="Plus fin et plus léger que le T480, avec un écran plus lumineux et le clavier hérité du T480 : un bon compromis pour travailler au quotidien. Écran lent et maintenance plus délicate.",
        strengths=["Plus fin et plus léger que le T480", "Écran plus lumineux, meilleure couverture des couleurs", "Clavier hérité du T480, port Ethernet RJ-45 intégral"],
        weak=["Écran lent, à éviter pour jouer", "Lecteur microSD au lieu du lecteur SD", "Démontage compliqué, Wi-Fi soudé"],
        m=("≈ 1,5 kg", "≈ 11,5 h (web, LaptopMedia)"),
        pour="Vous voulez un portable pro léger et robuste, avec un excellent clavier, pour travailler au quotidien.",
        eviter="Vous comptez agrandir la mémoire ou réparer vous-même : le démontage est plus délicat que sur les modèles précédents.",
        notes=[("Notebookcheck", 8.7, "https://www.notebookcheck.net/Lenovo-ThinkPad-T490-i7-MX250-Low-Power-FHD-Laptop-Review.421150.0.html", "2019-05-22", V),
               ("LaptopMedia", None, "https://laptopmedia.com/review/lenovo-thinkpad-t490-review-a-businessmans-companion/", "2019-06-17", None)],
        flux=dict(ppid="3052", re=r"\bT490\b", non=r"QWERTZ|T490S")),
    "thinkpad-t480": dict(
        short="Lenovo ThinkPad T480", ref='14" · Core i5 8e génération · double batterie possible',
        badge="Le meilleur clavier",
        verdict="Notebookcheck salue le meilleur clavier de sa catégorie, un écran très contrasté et une sécurité complète. Le châssis est un peu souple et l'écran couvre peu de couleurs.",
        strengths=["Clavier jugé le meilleur de sa catégorie", "Écran très contrasté (1228:1), assez lumineux pour l'extérieur", "TPM 2.0, lecteur d'empreintes, NFC"],
        weak=["Écran avec des fuites de lumière, 59 % du sRGB", "Châssis qui plie et craque", "Pas de trappe de maintenance"],
        m=("≈ 1,5 kg", "≈ 8 h (batterie standard, LaptopMag)"),
        pour="Vous tapez beaucoup et voulez un portable pro éprouvé, avec une sécurité complète.",
        eviter="Vous aimeriez un châssis rigide ou un écran aux couleurs étendues.",
        notes=[("Notebookcheck", 9.0, "https://www.notebookcheck.net/Lenovo-ThinkPad-T480-i7-8550U-MX150-FHD-Laptop-Review.293682.0.html", "2018-03-31", V),
               ("LaptopMag", None, "https://www.laptopmag.com/reviews/laptops/lenovo-thinkpad-t480", "2018-03-25", None)],
        flux=dict(ppid="2289", re=r"\bT480\b", non=r"T480S|QWERTZ")),
    "latitude-7490": dict(
        short="Dell Latitude 7490", ref='14" · Core i5/i7 8e génération',
        badge="Châssis magnésium",
        verdict="Notebookcheck lui donne 90 % : châssis en magnésium robuste, clavier parmi les meilleurs testés, Wi-Fi très rapide et une journée d'autonomie. L'écran est la seule vraie réserve.",
        strengths=["Châssis en magnésium robuste", "Clavier parmi les meilleurs testés par Notebookcheck", "Wi-Fi rapide, démontage simple"],
        weak=["Écran moins lumineux et moins précis que les concurrents, fuites de lumière", "SSD SATA, moins rapide que le NVMe", "Pas de Thunderbolt"],
        m=("≈ 1,6 kg", "≈ 9 h (web, LaptopMag)"),
        pour="Vous voulez un portable pro robuste et bien fini, pour travailler sans soucis toute la journée.",
        eviter="Vous avez besoin de Thunderbolt ou d'un écran aux couleurs précises.",
        notes=[("Notebookcheck", 9.0, "https://www.notebookcheck.com/Test-Dell-Latitude-7490-i5-8350U-FHD-Notebook.313394.0.html", "2018-06-28", V),
               ("LaptopMag", None, "https://laptopmag.com/reviews/laptops/dell-latitude-7490", "2018-04-23", None)],
        flux=dict(ppid="2903", re=r"\bE?7490\b", non=r"QWERTZ")),
    "thinkpad-t470s": dict(
        short="Lenovo ThinkPad T470s", ref='14" · Core i5 7e génération',
        badge="Léger et solide",
        verdict="Léger pour un 14 pouces (1,36 kg) et solide grâce à son châssis en magnésium, avec Thunderbolt 3 et un clavier réputé. L'écran est sombre et la puce, de 7e génération, n'est pas officiellement compatible avec Windows 11.",
        strengths=["1,36 kg et châssis en magnésium", "Thunderbolt 3, charge par USB-C", "Clavier et pavé tactile parmi les meilleurs de sa classe"],
        weak=["Écran sombre, 60 % du sRGB, scintillement à faible luminosité", "Puce de 7e génération : Windows 11 non pris en charge officiellement", "Une barrette de mémoire soudée"],
        m=("≈ 1,4 kg", "n.c."),
        pour="Vous cherchez un 14 pouces léger et solide à petit prix, pour des tâches simples.",
        eviter="Vous tenez à un système à jour : Windows 10 n'est plus pris en charge et la puce n'est pas compatible officiellement avec Windows 11.",
        notes=[("Notebookcheck", 8.8, "https://www.notebookcheck.com/Test-Lenovo-ThinkPad-T470s-7300U-FHD-Laptop.220792.0.html", "2017-05-14", V),
               ("LaptopMag", None, "https://www.laptopmag.com/reviews/laptops/lenovo-thinkpad-t470s", "2017-04-29", None)],
        flux=dict(ppid="3888", re=r"\bT470S\b", non=r"QWERTZ")),
    "elitebook-840-g6": dict(
        short="HP EliteBook 840 G6", ref='14" · Core i5 8e génération',
        badge="Finition premium",
        verdict="Châssis en aluminium, silencieux et frais en charge, connectique complète avec Thunderbolt et port d'accueil, et une autonomie d'environ 16 heures dans le test LaptopMedia.",
        strengths=["Châssis aluminium soigné, silencieux et frais", "Thunderbolt et port d'accueil", "Autonomie d'environ 16 h (web, LaptopMedia)"],
        weak=["Prix neuf élevé à sa sortie (moins pertinent en reconditionné)", "Un seul test détaillé disponible"],
        m=("≈ 1,5 kg", "≈ 16 h (web, LaptopMedia)"),
        pour="Vous voulez une belle machine en aluminium, silencieuse, avec une grosse autonomie et une station d'accueil.",
        eviter="Vous voulez plusieurs avis détaillés avant d'acheter : un seul test complet est disponible.",
        notes=[("LaptopMedia", None, "https://laptopmedia.com/review/hp-elitebook-840-g6-review-one-for-the-classy-business-people-out-there/", "2019-09-19", None)],
        flux=dict(ppid="4668", re=r"\b840 G6\b", non=r"QWERTZ")),
    "latitude-5510": dict(
        short="Dell Latitude 5510", ref='15,6" · Core i5 10e génération',
        badge="Le grand écran endurant",
        verdict="Le seul 15,6 pouces de la sélection : un des meilleurs claviers testés par LaptopMedia, beaucoup de ports et près de 15 heures d'autonomie. Plus lourd (1,8 kg), écran peu étendu en couleurs.",
        strengths=["Un des meilleurs claviers de portable testés par LaptopMedia", "Autonomie de plus de 15 h (web, LaptopMedia)", "Beaucoup de ports, évolutif"],
        weak=["1,8 kg : plus lourd que les 14 pouces", "Écran à 50 % du sRGB", "Scintillement (PWM) à faible luminosité"],
        m=("≈ 1,8 kg", "≈ 15 h (web, LaptopMedia)"),
        pour="Vous voulez un grand écran 15,6 pouces avec un excellent clavier, surtout posé sur un bureau.",
        eviter="Vous transportez votre PC tous les jours : 1,8 kg se sent.",
        notes=[("LaptopMedia", None, "https://laptopmedia.com/review/dell-latitude-15-5510-review-a-sustainable-laptop-with-a-great-keyboard/", "2020-09-17", None)],
        flux=dict(ppid="5137", re=r"\b5510\b", non=r"QWERTZ")),
    "thinkpad-l14-gen1": dict(
        short="Lenovo ThinkPad L14 Gen 1 (Intel)", ref='14" · Core i5 10e génération',
        badge="L'entrée de gamme pro",
        verdict="Plus simple que les T : châssis tout en plastique, mais le test LaptopMedia relève de bonnes performances, un clavier confortable, un écran sans scintillement et une connectique riche.",
        strengths=["Performances solides pour un modèle de milieu de gamme", "Clavier confortable, résistant aux éclaboussures", "Écran sans scintillement, charge par USB-C"],
        weak=["Châssis tout en plastique", "Écran à 51 % du sRGB", "Un seul test détaillé disponible"],
        m=("≈ 1,6 kg", "≈ 9,5 h (web, LaptopMedia)"),
        pour="Vous voulez un portable pro simple et confortable pour la bureautique, sans payer la finition haut de gamme.",
        eviter="Vous tenez à une finition en métal ou à un écran aux couleurs étendues.",
        notes=[("LaptopMedia", None, "https://laptopmedia.com/gb/review/lenovo-thinkpad-l14-review-even-the-intel-version-brings-performance-to-the-table/", "2020-10-20", None)],
        flux=dict(ppid="5166", re=r"\bL14\b.*(INTEL|I[357]-)", non=r"RYZEN|QWERTZ")),
    "thinkpad-x280": dict(
        short="Lenovo ThinkPad X280", ref='12,5" · Core i5 8e génération',
        badge="Le plus compact",
        verdict="L'ultraportable 12,5 pouces de la sélection (environ 1,35 kg) : écran vif, bonnes performances et frappe agréable selon LaptopMag, mais une autonomie sous la moyenne.",
        strengths=["Format compact, environ 1,35 kg", "Écran vif et coloré (LaptopMag)", "Bonne frappe, nombreux ports"],
        weak=["Autonomie en dessous de la moyenne (LaptopMag)", "Un seul test détaillé disponible"],
        m=("≈ 1,4 kg", "n.c."),
        pour="Vous voulez le plus compact des ThinkPad de la sélection, pour voyager léger.",
        eviter="Vous passez la journée loin d'une prise : l'autonomie est sous la moyenne.",
        notes=[("LaptopMag", None, "https://www.laptopmag.com/reviews/laptops/lenovo-thinkpad-x280", "2018-03-02", None)],
        flux=dict(ppid="4071", re=r"\bX280\b", non=r"QWERTZ")),
}


GUIDE_RECO = dict(
    titre="Comment choisir un PC portable reconditionné",
    intro="Un PC professionnel reconditionné offre une machine robuste (clavier, charnières, connectique) pour une fraction du prix du neuf. Le compromis : l'âge de la puce, l'usure de la batterie et le sérieux du vendeur. <b>Les tests presse portent sur le modèle neuf</b> : ils disent si la machine était bonne à sa sortie, pas dans quel état est l'exemplaire que vous recevrez.",
    criteres=[
        ("Génération du processeur", "Visez la 8e génération Intel (ou un Ryzen 4000) au minimum : c'est le seuil à partir duquel Windows 11 est officiellement pris en charge. Une puce plus ancienne fonctionne, mais sans garantie de mises à jour à terme."),
        ("Windows 11 plutôt que 10", "Windows 10 n'est plus pris en charge par Microsoft depuis octobre 2025. Préférez une annonce livrée sous Windows 11."),
        ("Mémoire et stockage", "8 Go de RAM et un SSD de 250 Go suffisent pour la bureautique ; 16 Go si vous gardez beaucoup d'onglets ou de logiciels ouverts."),
        ("Grade, garantie et batterie", "Le grade (A, B, C…) décrit l'état esthétique, avec une définition propre à chaque vendeur. Lisez la durée de garantie, les conditions de retour et ce que le vendeur annonce sur la batterie avant de commander."),
    ],
    pieges=[
        "Les annonces au clavier QWERTY ou QWERTZ : vérifiez que le clavier est bien AZERTY.",
        "Les configurations qui diffèrent pour un même modèle : le prix suit la mémoire et le stockage.",
        "Un « prix barré » élevé sur un produit reconditionné : comparez avec le prix des autres configurations.",
        "Les écrans de ces PC pros sont souvent ternes : à éviter pour la retouche photo ou la vidéo.",
    ],
    budget=[("230 – 300 €", "Bureautique et navigation : 8 Go, SSD 250 Go, un ThinkPad ou un Latitude de 2017 à 2019."),
            ("300 – 400 €", "Le meilleur compromis : 8e à 11e génération, 8 à 16 Go, Windows 11."),
            ("400 € et plus", "Le plus récent ou le plus équipé : 16 Go, SSD de 500 Go à 1 To.")],
)
