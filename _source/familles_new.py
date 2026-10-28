# -*- coding: utf-8 -*-
"""Rubriques Écrans PC et Imprimantes (ajoutées le 09/10/2026) : usages, textes des pages, FAQ.
Les couleurs reprennent les 5 couleurs d'usage du site (classes f-bureau, f-creation, f-gaming, f-polyvalent, f-lowcost)."""

ECATS = [
    dict(key="e-bureau", slug="bureautique", label="Bureautique", h="Bureautique &amp; télétravail", tag="Confort au quotidien", color="var(--cat-bureau)", cls="f-bureau", badge="bureau-fixe",
         h1='Les 10 meilleurs écrans PC pour la <span class="flash">bureautique</span>',
         intro="Pour travailler toute la journée, la définition, le confort visuel et la connectique (un seul câble USB-C pour le portable) comptent plus que la fréquence."),
    dict(key="e-gaming", slug="gaming", label="Gaming", h="Gaming", tag="Fluidité et réactivité", color="var(--cat-gaming)", cls="f-gaming", badge="gaming",
         h1='Les 10 meilleurs <span class="flash">écrans gaming</span> en 2026',
         intro="L'OLED a tout changé : contraste infini et réactivité instantanée. Reste à choisir la bonne définition et la bonne fréquence pour votre carte graphique."),
    dict(key="e-creation", slug="creation", label="Création", h="Création &amp; photo", tag="Couleurs fidèles", color="var(--cat-creation)", cls="f-creation", badge="creation",
         h1='Les 10 meilleurs écrans pour la <span class="flash">photo et la création</span>',
         intro="Retouche, graphisme, vidéo : ce qui compte, c'est la fidélité des couleurs, la gamme couverte et la calibration, bien avant la fréquence."),
    dict(key="e-portable", slug="portable", label="Portable", h="Écrans portables", tag="Un deuxième écran dans le sac", color="var(--cat-poly)", cls="f-polyvalent", badge="ecran-portable",
         h1='Les 10 meilleurs <span class="flash">écrans portables</span>',
         intro="Un écran de 14 à 16 pouces, alimenté par un seul câble USB-C, pour doubler l'écran d'un portable au bureau, en voyage ou en télétravail."),
    dict(key="e-lowcost", slug="petit-prix", label="Petit prix", h="Petit prix (&lt; 200 €)", tag="Le bon écran sans se ruiner", color="var(--cat-lowcost)", cls="f-lowcost", badge="ecran-lowcost",
         h1='Les 10 meilleurs écrans PC <span class="flash">à moins de 200 €</span>',
         intro="Sous 200 €, on trouve désormais du QHD à 180 Hz et plus. La presse teste moins ces modèles : nous indiquons le nombre de tests derrière chaque note."),
]

ICATS = [
    dict(key="i-reservoir", slug="reservoir", label="Réservoirs", h="Réservoirs d'encre", tag="L'encre pour des années", color="var(--cat-poly)", cls="f-polyvalent", badge="reservoir",
         h1='Les 10 meilleures imprimantes <span class="flash">à réservoirs d\'encre</span>',
         intro="Plus chères à l'achat, les imprimantes à réservoirs impriment des milliers de pages avec l'encre fournie : le coût par page s'effondre dès qu'on imprime régulièrement."),
    dict(key="i-laser-mono", slug="laser-noir-et-blanc", label="Laser N&amp;B", h="Laser noir et blanc", tag="Texte net, vite", color="var(--cat-bureau)", cls="f-bureau", badge="laser-mono",
         h1='Les 10 meilleures imprimantes <span class="flash">laser noir et blanc</span>',
         intro="Pour les documents, rien ne bat une laser monochrome : rapide, fiable, un toner qui ne sèche jamais et un coût par page très bas."),
    dict(key="i-laser-couleur", slug="laser-couleur", label="Laser couleur", h="Laser couleur", tag="La couleur au bureau", color="var(--cat-gaming)", cls="f-gaming", badge="laser-couleur",
         h1='Les 10 meilleures imprimantes <span class="flash">laser couleur</span>',
         intro="Devis, présentations, documents scolaires : la laser couleur imprime vite et proprement, sans encre qui sèche. Elle n'est pas faite pour les photos."),
    dict(key="i-photo", slug="photo", label="Photo", h="Imprimantes photo", tag="Vos photos sur papier", color="var(--cat-creation)", cls="f-creation", badge="photo",
         h1='Les 10 meilleures <span class="flash">imprimantes photo</span>',
         intro="De la petite imprimante de poche qui sort des photos autocollantes à l'imprimante A3+ à six encres : le bon choix dépend du format et du volume de tirages."),
    dict(key="i-lowcost", slug="petit-prix", label="Petit prix", h="Petit prix (&lt; 150 €)", tag="Imprimer sans se ruiner", color="var(--cat-lowcost)", cls="f-lowcost", badge="imprimante-lowcost",
         h1='Les 10 meilleures imprimantes <span class="flash">à moins de 150 €</span>',
         intro="Pour imprimer de temps en temps, une multifonction jet d'encre à petit prix suffit. Attention au prix des cartouches : au-delà de quelques pages par semaine, mieux vaut un réservoir."),
]

SCATS = [
    dict(key="s-robot-laveur", slug="robots-aspirateurs-laveurs", label="Robot aspirateur laveur", top_label="robots laveurs", h="Robots aspirateurs laveurs", tag="Aspire et lave, sans y penser", color="var(--cat-poly)", cls="f-polyvalent", badge="robots-laveurs-v2", scene="robot-laveur", scene_alt="La mascotte, assise sur un seau « sol mouillé », regarde un robot laveur travailler",
         h1='Les 10 meilleurs <span class="flash">robots aspirateurs laveurs</span> en 2026',
         intro="Aspiration, lavage, vidage et séchage automatiques : les robots à station font presque tout seuls. La presse les teste en détail, et c'est la navigation et la qualité du lavage qui font la différence."),
    dict(key="s-aspirateur-balai", slug="aspirateurs-balais", label="Aspirateur balai", top_label="aspirateurs balais", h="Aspirateur balai", tag="Léger, puissant, sans fil", color="var(--cat-bureau)", cls="f-bureau", badge="robots-aspirateurs-balais-v2",
         h1='Les meilleurs <span class="flash">aspirateurs balais sans fil</span> en 2026',
         intro="Pas de station à installer : on décroche le balai et on aspire. Puissance, autonomie, poids et brosse anti-enchevêtrement font la différence, et c'est là que Dyson, Samsung et Dreame se disputent la première place."),
    dict(key="s-aspirateur-laveur", slug="aspirateurs-balais-laveurs", label="Balais laveurs", top_label="aspirateurs balais laveurs", h="Aspirateurs balais laveurs", tag="Aspire et lave en un passage", color="var(--cat-creation)", cls="f-creation", badge="robots-balais-laveurs-v2", scene="robot-balai-laveur", scene_alt="La mascotte pousse un aspirateur balai laveur sur un sol brillant",
         h1='Les meilleurs <span class="flash">aspirateurs balais laveurs</span> en 2026',
         intro="Ils aspirent et lavent en un seul passage, puis nettoient et sèchent leur brosse. Les tests départagent la qualité du lavage, le poids et la facilité d'entretien."),
    dict(key="s-robot-animaux", slug="robots-aspirateurs-animaux", label="Robots pour animaux", top_label="robots pour animaux", h="Robots pour animaux", tag="Poils et passages incessants", color="var(--cat-gaming)", cls="f-gaming", badge="robots-animaux-v2", scene="robot-animaux", scene_alt="La mascotte et son chien regardent un robot aspirateur passer",
         h1='Les meilleurs <span class="flash">robots aspirateurs pour animaux</span> en 2026',
         intro="Les poils s'enroulent dans la brosse et les petits accidents se détectent mal : on retient ici les robots les mieux notés, à forte aspiration, anti-enchevêtrement et bonne détection des obstacles."),
    dict(key="s-petit-prix", slug="petit-prix", label="Petit prix", top_label="aspirateurs et robots à petit prix", h="Petit prix (&lt; 400 €)", tag="Bien testés, sans se ruiner", color="var(--cat-lowcost)", cls="f-lowcost", badge="robots-petit-prix-v2", scene="robot-petit-prix", scene_alt="La mascotte compare des étiquettes de prix devant un robot aspirateur",
         extra=["dreame-l10s-ultra", "mova-e40-ultra", "dreame-h12-pro", "dreame-h14", "tineco-floor-one-s7-pro", "dreame-h15-pro", "mova-m50-ultra"],
         h1='Les meilleurs <span class="flash">robots et aspirateurs à petit prix</span> en 2026',
         intro="Moins de 400 € : on retient les robots et les balais laveurs bien notés par la presse, avec le prix constaté chez Amazon. Plusieurs figurent aussi dans leur usage d'origine (robots laveurs, balais laveurs)."),
]

TCATS = [
    dict(key="t-prix", slug="petit-prix", label="Petit prix", top_label="téléviseurs à petit prix", h="Petit prix (moins de 600 €)", tag="Bien testés, sans se ruiner", color="var(--cat-lowcost)", cls="f-lowcost", badge="tv-petit-prix",
         scene="tv-petit-prix", scene_alt="Le père de famille geek, étiquette promo dans une main, un téléviseur sous l'autre bras",
         seo_title="Meilleurs téléviseurs à petit prix 2026 : moins de 600 € | Top 10 Geek",
         seo_desc="Les meilleurs téléviseurs à moins de 600 € en 2026, classés par note presse : TCL, Samsung, Hisense, LG, Sony. Prix indicatifs, points forts et faibles.",
         extra=["hisense-e7q-pro-55", "sony-bravia-3-43", "hisense-u7q-55", "lg-qned85-55", "samsung-qn80f-55"],
         h1='Les meilleurs <span class="flash">téléviseurs à petit prix</span> en 2026',
         intro="Moins de 600 € : la presse a testé peu de modèles à ce tarif, mais plusieurs tiennent la comparaison. Voici ceux qui ont des notes chiffrées et une offre d'achat ; certains figurent aussi dans l'usage de leur taille."),
    dict(key="t-petit", slug="petits-formats", label="Petits formats", top_label="téléviseurs jusqu'à 50 pouces", h="Petits formats (jusqu'à 50″)", tag="Pour la chambre ou le bureau", color="var(--cat-creation)", cls="f-creation", badge="tv-petits-formats",
         scene="tv-petits-formats", scene_alt="Le père de famille geek, assis sur un lit d'enfant, un seau de pop-corn dans les bras, devant un petit téléviseur",
         extra=["samsung-qn90f-50"],
         h1='Les meilleurs <span class="flash">petits téléviseurs</span> jusqu\'à 50 pouces',
         intro="Chambre, bureau, cuisine ou studio : de 42 à 50 pouces, la presse teste peu de modèles. Voici ceux qui ont des notes chiffrées et une offre d'achat. Le Samsung QN90F 50″ figure aussi dans l'usage 50–55″."),
    dict(key="t-55", slug="50-55-pouces", label="50–55″", top_label="téléviseurs 50–55 pouces", h="50–55 pouces", tag="La taille du salon", color="var(--cat-gaming)", cls="f-gaming", badge="tv-55",
         scene="tv-55", scene_alt="Le père de famille geek, assis sur son canapé, télécommande en main et pouce levé, devant un téléviseur",
         h1='Les meilleurs <span class="flash">téléviseurs 50–55 pouces</span> en 2026',
         intro="Le 55 pouces est la taille la plus vendue : assez grand pour le salon, accessible en OLED comme en Mini-LED. La presse départage la luminosité, le contraste, le jeu et le son intégré."),
    dict(key="t-65", slug="65-pouces-et-plus", label="65″ et plus", top_label="téléviseurs 65 pouces et plus", h="65 pouces et plus", tag="Le cinéma à la maison", color="var(--cat-poly)", cls="f-polyvalent", badge="tv-65",
         scene="tv-65", scene_alt="Le père de famille geek, bras écartés devant un immense écran mural affichant ses applications de streaming",
         h1='Les meilleurs <span class="flash">téléviseurs 65 pouces et plus</span> en 2026',
         intro="À partir de 65 pouces, l'écran devient le centre du salon. Le prix grimpe vite : la presse départage la luminosité, le contraste dans une pièce sombre et le jeu en 120 Hz, et le rapport qualité-prix compte autant que l'image."),
    dict(key="t-barres", slug="barres-de-son", label="Barres de son", top_label="barres de son", h="Barres de son", tag="Le son à la hauteur de l'image", color="var(--cat-creation)", cls="f-creation", badge="tv-barres-son",
         scene="tv-barres-son", scene_alt="Le père de famille geek, casque autour du cou, affalé dans son canapé devant une barre de son et ses ondes lumineuses",
         plural_low="barres de son",
         seo_title="Meilleures barres de son 2026 : tests et prix | Top 10 Geek",
         seo_desc="Les meilleures barres de son en 2026, classées par note presse : Sonos, Samsung, Sony, JBL, TCL, Hisense. Prix indicatifs, points forts et faibles.",
         h1='Les meilleures <span class="flash">barres de son</span> en 2026',
         intro="Les haut-parleurs d'un téléviseur sont rarement à la hauteur : une barre de son change l'expérience pour peu de frais. La presse départage les dialogues, les basses, l'effet Dolby Atmos et le prix ; la sélection va de 109 à 800 €."),
]

ACATS = [
    dict(key="a-bt", slug="enceintes-bluetooth", label="Enceintes Bluetooth", top_label="enceintes Bluetooth portables", h="Enceintes Bluetooth portables", tag="Le son qui vous suit partout", color="var(--cat-gaming)", cls="f-gaming", badge="enceintes-bluetooth", scene="audio-bt", scene_alt="Le père de famille geek, assis sur un muret, une canette à la main, à côté d'une enceinte Bluetooth qui diffuse sa musique",
         plural_low="enceintes",
         seo_title="Meilleures enceintes Bluetooth portables 2026 : tests et prix | Top 10 Geek",
         seo_desc="Les meilleures enceintes Bluetooth portables en 2026, classées par note presse : JBL, Marshall, Sony, Bose, Sonos, Ultimate Ears. Prix indicatifs, points forts et faibles.",
         h1='Les meilleures <span class="flash">enceintes Bluetooth portables</span> en 2026',
         intro="De la petite enceinte de poche à l'enceinte de terrasse : la presse départage le son, l'autonomie, la résistance à l'eau et le prix. Voici les modèles qui ont des notes chiffrées et une offre d'achat, avec un prix indicatif relevé chez Amazon ou Electro Dépôt."),
]

VCATS = [
    dict(key="v-surv", slug="cameras-de-surveillance", label="Caméras de surveillance", top_label="caméras de surveillance", h="Caméras de surveillance", tag="Voir chez soi, même à distance", color="var(--cat-creation)", cls="f-creation", badge="cameras-surveillance", scene="video-surv", scene_alt="Le père de famille geek regarde sur son téléphone l'image de la caméra de surveillance posée au-dessus de sa porte",
         plural_low="caméras",
         seo_title="Meilleures caméras de surveillance 2026 : tests et prix | Top 10 Geek",
         seo_desc="Les meilleures caméras de surveillance connectées en 2026, intérieur et extérieur, classées par note presse : Tapo, Ezviz, Reolink, Eufy, Arlo. Prix indicatifs, points forts et faibles.",
         h1='Les meilleures <span class="flash">caméras de surveillance</span> en 2026',
         intro="Intérieur ou extérieur, filaires ou sur batterie : la presse départage la qualité d'image de jour comme de nuit, la détection, le stockage et l'abonnement éventuel. Voici les caméras qui ont des notes chiffrées et une offre d'achat."),
]

FAMILIES_NEW = [
    dict(key="ecran", slug="ecran-pc", label="Écran PC", plural="Écrans PC", plural_low="écrans PC", cats=ECATS, provisional=False,
         m_labels=("Taille et définition", "Fréquence"), col="Taille", mascot="pose-ecran", noun="écran", noun_det="l'écran",
         h1='Comparatif écrans PC 2026 : <span class="flash">le verdict par usage</span>',
         intro="50 écrans PC passés au crible : bureautique, gaming, création, écrans portables et petits prix, avec une note presse sur 10, un prix indicatif et les liens vers les marchands.",
         title="Meilleur écran PC 2026 : tous les tests par usage | Top 10 Geek",
         desc="50 écrans PC 2026 classés par usage avec une note presse sur 10 et un prix indicatif : bureautique, gaming, création, écrans portables, petits prix.",
         usage_title="Top 10 écrans PC {label} 2026 : tests et prix | Top 10 Geek",
         usage_desc="Les 10 meilleurs écrans PC {label} en 2026, classés par note presse, avec prix indicatif, points forts et points faibles."),
    dict(key="imprimante", slug="imprimante", label="Imprimante", plural="Imprimantes", cats=ICATS, provisional=False,
         m_labels=("Technologie", "Fonctions"), col="Technologie", mascot="pose-imprimante", noun="imprimante", noun_det="l'imprimante",
         h1='Comparatif imprimantes 2026 : <span class="flash">le verdict par usage</span>',
         intro="50 imprimantes classées par usage : réservoirs d'encre, laser noir et blanc, laser couleur, photo et petits prix, avec les tests de la presse et des associations de consommateurs, un prix indicatif et les liens vers les marchands.",
         title="Meilleure imprimante 2026 : tous les tests par usage | Top 10 Geek",
         desc="50 imprimantes 2026 classées par usage avec les tests de la presse et des associations de consommateurs : réservoirs, laser, photo, petits prix.",
         usage_title="Top 10 imprimantes {label} 2026 : tests et prix | Top 10 Geek",
         usage_desc="Les 10 meilleures imprimantes {label} en 2026 : tests de la presse et des associations, prix indicatif, points forts et faibles."),
    dict(key="robot", slug="aspirateur-robot", label="Robot aspirateur", plural="Robots et aspirateurs", plural_low="robots et aspirateurs", cats=SCATS, provisional=False,
         m_labels=("Puissance", "Station"), col="Puissance", mascot="pose-robot-hub", scene_alt="La mascotte, bras croisés, entourée de trois robots aspirateurs", noun="robot", noun_det="le robot",
         h1='Comparatif robots aspirateurs 2026 : <span class="flash">le verdict par usage</span>',
         intro="Robots aspirateurs laveurs, aspirateurs balais et laveurs : les modèles les mieux testés par la presse, avec une note sur 10, un prix indicatif et les liens vers les marchands.",
         title="Meilleur robot aspirateur laveur 2026 : tous les tests | Top 10 Geek",
         desc="Les meilleurs robots aspirateurs laveurs 2026 classés d'après les tests de la presse : note sur 10, prix indicatif, points forts et faibles.",
         usage_title="Meilleurs robots et aspirateurs : {label} 2026, tests et prix | Top 10 Geek",
         usage_desc="Les meilleurs modèles « {label} » en 2026, classés par note presse, avec prix indicatif, points forts et points faibles."),
    dict(key="tv", slug="tv", label="Téléviseur", plural="Téléviseurs", plural_low="téléviseurs", cats=TCATS, provisional=False,
         m_labels=("Technologie", "Atout"), col="Technologie", mascot="pose-tv", noun="modèle", noun_det="le modèle", stat_noun="Modèles",
         h1='Comparatif téléviseurs 2026 : <span class="flash">le verdict par taille et par usage</span>',
         intro="Les téléviseurs les mieux testés par la presse, avec une note sur 10, un prix indicatif relevé chez Amazon et les liens vers les marchands.",
         title="Meilleur téléviseur 2026 : tous les tests par taille | Top 10 Geek",
         desc="Les meilleurs téléviseurs 2026 classés d'après les tests de la presse : note sur 10, prix indicatif, points forts et faibles.",
         usage_title="Meilleurs téléviseurs {label} 2026 : tests et prix | Top 10 Geek",
         usage_desc="Les meilleurs téléviseurs « {label} » en 2026, classés par note presse, avec prix indicatif, points forts et points faibles."),
    dict(key="audio", slug="audio", label="Audio", plural="Audio", plural_low="produits audio", cats=ACATS, provisional=False,
         m_labels=("Étanchéité", "Atout"), col="Étanchéité", mascot="pose-audio-hub", noun="modèle", noun_det="le modèle", stat_noun="Modèles",
         h1='Comparatif audio 2026 : <span class="flash">le verdict par usage</span>',
         intro="Enceintes, écouteurs, casques et hi-fi : les modèles les mieux testés par la presse, avec une note sur 10, un prix indicatif relevé chez Amazon ou Electro Dépôt et les liens vers les marchands.",
         title="Meilleur son et audio 2026 : tous les tests par usage | Top 10 Geek",
         desc="Les meilleures enceintes, écouteurs, casques et chaînes hi-fi 2026 classés d'après les tests de la presse : note sur 10, prix indicatif, points forts et faibles.",
         usage_title="Meilleur audio : {label} 2026, tests et prix | Top 10 Geek",
         usage_desc="Les meilleurs modèles « {label} » en 2026, classés par note presse, avec prix indicatif, points forts et points faibles."),
    dict(key="video", slug="photo-video", label="Photo / Vidéo", plural="Photo et vidéo", plural_low="appareils", cats=VCATS, provisional=False,
         m_labels=("Résolution", "Atout"), col="Résolution", mascot="pose-video-hub", noun="modèle", noun_det="le modèle", stat_noun="Modèles",
         h1='Comparatif photo et vidéo 2026 : <span class="flash">le verdict par usage</span>',
         intro="Caméras de surveillance, caméras d'action, vidéoprojecteurs, appareils photo et drones : les modèles les mieux testés par la presse, avec une note sur 10, un prix indicatif et les liens vers les marchands.",
         title="Meilleure caméra et appareil photo 2026 : tous les tests par usage | Top 10 Geek",
         desc="Les meilleures caméras de surveillance, caméras d'action, vidéoprojecteurs, appareils photo et drones 2026 classés d'après les tests de la presse : note sur 10, prix indicatif.",
         usage_title="Meilleur(e)s {label} 2026 : tests et prix | Top 10 Geek",
         usage_desc="Les meilleurs modèles « {label} » en 2026, classés par note presse, avec prix indicatif, points forts et points faibles."),
]

FAQ_E = [
    ("Comment est calculée la note presse ?", "C'est la moyenne simple des notes publiées par les médias spécialisés (Les Numériques, Tom's Hardware, RTINGS, TechRadar, Clubic…), toutes converties sur 10 : 4/5 devient 8/10, 87 % devient 8,7/10. Le nombre de tests est toujours affiché. Quand la note porte sur une variante proche de la même gamme, nous l'indiquons."),
    ("Comment est établi le classement ?", "En tête : « le choix de la bande », notre recommandation pour l'usage : de préférence un produit de la zone « bonnes affaires » du radar (note presse d'au moins 8/10, prix sous la médiane de l'usage), si sa note repose sur au moins 3 notes presse. Ensuite viennent les écrans notés par au moins 3 médias, puis ceux qui n'ont qu'1 ou 2 notes, puis ceux testés sans note chiffrée. Dans chaque groupe, ils sont classés par note presse ajustée : une note isolée pèse moins qu'une moyenne de nombreux tests."),
    ("QHD ou 4K : quelle définition choisir ?", "Sur 27 pouces, le QHD (2560 × 1440) est le bon équilibre pour jouer et travailler. La 4K apporte un texte plus fin et convient à la création, mais demande une carte graphique puissante en jeu. Sur 32 pouces, la 4K devient vraiment confortable."),
    ("OLED ou IPS ?", "L'OLED offre un contraste infini et une réactivité immédiate, idéal pour jouer et regarder des films, mais il coûte plus cher et peut marquer si des éléments fixes restent affichés très longtemps. L'IPS reste le choix raisonnable pour la bureautique et un usage de plusieurs heures avec des fenêtres fixes."),
    ("D'où viennent les prix ?", "Nous affichons un prix indicatif par écran : le plus bas constaté sur Amazon ou chez Electro Dépôt lors de notre dernier relevé, arrondi à la dizaine d'euros. Pour Electro Dépôt, nous affichons aussi son prix exact, tiré de son flux produits officiel, avec la date du relevé. Il sert à situer l'écran, pas à comparer les marchands. Seul le prix affiché par le marchand fait foi."),
]

FAQ_I = [
    ("D'où viennent les tests des imprimantes ?", "Les imprimantes sont surtout testées en laboratoire par les associations de consommateurs (Test-Achats, Que Choisir, Which?, Tænk) et par quelques médias (Les Numériques, TechRadar, RTINGS…). Les associations réservent leurs notes à leurs abonnés : nous citons et lions leurs tests sans note chiffrée, et la note presse n'est calculée que sur les notes publiques."),
    ("Comment est établi le classement ?", "En tête : « le choix de la bande », notre recommandation pour l'usage : de préférence un produit de la zone « bonnes affaires » du radar (note presse d'au moins 8/10, prix sous la médiane de l'usage), si sa note repose sur au moins 3 notes presse. Ensuite viennent les imprimantes notées par au moins 3 médias, puis celles qui n'ont qu'1 ou 2 notes, puis celles testées sans note chiffrée (souvent par les associations de consommateurs). Dans chaque groupe, elles sont classées par note presse ajustée : une note isolée pèse moins qu'une moyenne de nombreux tests."),
    ("Réservoir d'encre ou cartouches ?", "Au-delà de quelques pages par semaine, le réservoir est presque toujours gagnant : plus cher à l'achat, mais l'encre fournie suffit pour des milliers de pages. Pour imprimer très rarement, une imprimante à cartouches bon marché reste plus simple, à condition d'accepter des cartouches chères."),
    ("Laser ou jet d'encre ?", "La laser imprime vite, le toner ne sèche jamais et le texte est très net : c'est le meilleur choix pour les documents. Le jet d'encre reste indispensable pour les photos et polyvalent à la maison."),
    ("D'où viennent les prix ?", "Nous affichons un prix indicatif par imprimante : le plus bas constaté sur Amazon ou chez Electro Dépôt lors de notre dernier relevé, arrondi à la dizaine d'euros. Pour Electro Dépôt, nous affichons aussi son prix exact, tiré de son flux produits officiel, avec la date du relevé. Quand l'imprimante n'est proposée que par un vendeur tiers sur Amazon, nous l'indiquons. Seul le prix affiché par le marchand fait foi."),
]


FAQ_S = [
    ("Comment est calculée la note presse ?", "C'est la moyenne simple des notes publiées par les médias spécialisés (Les Numériques, Frandroid, 01net, Que Choisir, Tom's Guide…), toutes converties sur 10 : 4/5 devient 8/10. Le nombre de tests est toujours affiché. Quand la note porte sur une variante proche de la même gamme, nous l'indiquons."),
    ("Comment est établi le classement ?", "En tête : « le choix de la bande », notre recommandation pour l'usage : de préférence un produit de la zone « bonnes affaires » du radar (note presse d'au moins 8/10, prix sous la médiane de l'usage), si sa note repose sur au moins 3 notes presse. Ensuite viennent les robots notés par au moins 3 médias, puis ceux qui n'ont qu'1 ou 2 notes. Dans chaque groupe, ils sont classés par note presse ajustée : une note isolée pèse moins qu'une moyenne de nombreux tests."),
    ("Faut-il une station qui vide et lave toute seule ?", "Si vous voulez ne toucher au robot qu'une fois par mois, oui : la station vide le bac, lave et sèche la serpillière. Elle prend de la place et coûte plus cher. Pour un petit logement ou un budget serré, un robot sans station suffit souvent."),
    ("D'où viennent les prix ?", "Nous affichons un prix indicatif par robot : le plus bas constaté sur Amazon ou chez Electro Dépôt lors de notre dernier relevé, arrondi à la dizaine d'euros. Pour Electro Dépôt, nous affichons aussi son prix exact, tiré de son flux produits officiel. Quand le robot n'est proposé que par un vendeur tiers sur Amazon, nous l'indiquons. Seul le prix affiché par le marchand fait foi."),
]

FAQ_T = [
    ("Comment est calculée la note presse ?", "C'est la moyenne simple des notes publiées par les médias spécialisés (Les Numériques, RTINGS, Clubic, Trusted Reviews, What Hi-Fi?…), toutes converties sur 10 : 4/5 devient 8/10. Le nombre de tests est toujours indiqué à côté de la note."),
    ("Comment est établi le classement ?", "En tête : « le choix de la bande », notre recommandation pour l'usage : de préférence un produit de la zone « bonnes affaires » du radar (note presse d'au moins 8/10, prix sous la médiane de l'usage), si sa note repose sur au moins trois tests. Le reste du classement suit la note presse, corrigée du nombre de tests."),
    ("OLED ou Mini-LED : que choisir ?", "L'OLED offre des noirs parfaits et un contraste infini : c'est le meilleur choix pour les films dans une pièce sombre ou tamisée. Le Mini-LED est plus lumineux et souvent moins cher : il convient mieux à un salon éclairé. Pour un même budget, un bon Mini-LED vaut souvent mieux qu'un OLED d'entrée de gamme."),
    ("Les tests portent-ils sur la taille indiquée ?", "Pas toujours : la presse teste souvent une seule taille d'une gamme (55 ou 65 pouces) et ses conclusions valent pour toute la série. Le prix affiché est celui de la taille de l'usage, 55 pouces sauf mention contraire ; la mention « gamme » signale que les tests portent sur une taille ou une variante proche."),
    ("D'où viennent les prix ?", "Nous affichons un prix indicatif par téléviseur : celui constaté sur Amazon lors de notre dernier relevé, arrondi à la dizaine d'euros. Les téléviseurs étant souvent en promotion, vérifiez le prix et le vendeur sur la fiche du marchand avant d'acheter."),
]

FAQ_A = [
    ("Comment est calculée la note presse ?", "C'est la moyenne simple des notes publiées par les médias spécialisés (Les Numériques, 01net, Clubic, FrAndroid, TechRadar, Trusted Reviews, SoundGuys…), toutes converties sur 10 : 4/5 devient 8/10. Le nombre de tests est toujours indiqué à côté de la note ; un modèle à un seul test noté est signalé comme tel."),
    ("Comment est établi le classement ?", "En tête : « le choix de la bande », notre recommandation pour l'usage : de préférence un produit de la zone « bonnes affaires » du radar (note presse d'au moins 8/10, prix sous la médiane de l'usage), si sa note repose sur au moins trois tests. Le reste du classement suit la note presse ajustée au nombre de tests."),
    ("Quelle autonomie et quelle étanchéité choisir ?", "Pour la plage ou la douche, visez au moins l'indice IP67 (poussière et immersion) ; pour un usage à la maison, l'étanchéité compte moins que l'autonomie. Les durées annoncées par les fabricants sont mesurées à volume modéré : les tests de la presse les trouvent souvent surévaluées à fort volume."),
    ("Faut-il une enceinte Wi-Fi ou Bluetooth ?", "Le Bluetooth suffit pour l'extérieur et les déplacements. Une enceinte Wi-Fi (type Sonos) offre un meilleur son sans perte et le multiroom à la maison, mais elle coûte plus cher et dépend d'un réseau. Quelques modèles nomades, comme la Sonos Roam 2, proposent les deux."),
    ("D'où viennent les prix ?", "Nous affichons un prix indicatif par enceinte : le plus bas constaté sur Amazon ou chez Electro Dépôt lors de notre dernier relevé, arrondi à la dizaine d'euros. Pour Electro Dépôt, nous affichons aussi son prix exact, tiré de son flux produits officiel, avec la date du relevé. Vérifiez le prix et le vendeur sur la fiche du marchand avant d'acheter."),
]

FAQ_V = [
    ("Comment est calculée la note presse ?", "C'est la moyenne simple des notes publiées par les médias spécialisés (Les Numériques, 01net, Clubic, FrAndroid, Tom's Guide, TechRadar…), toutes converties sur 10 : 4/5 devient 8/10. Le nombre de tests est toujours indiqué à côté de la note ; un modèle à un seul test noté est signalé comme tel."),
    ("Comment est établi le classement ?", "En tête : « le choix de la bande », notre recommandation pour l'usage : de préférence un produit de la zone « bonnes affaires » du radar (note presse d'au moins 8/10, prix sous la médiane de l'usage), si sa note repose sur au moins trois tests. Le reste du classement suit la note presse ajustée au nombre de tests."),
    ("Faut-il un abonnement pour une caméra de surveillance ?", "Pas forcément : beaucoup de caméras enregistrent sur une carte microSD sans abonnement. L'abonnement du fabricant donne en général un stockage dans le cloud et des alertes intelligentes (personne, colis, animal) ; vérifiez ce qui est inclus avant d'acheter."),
    ("Que dit la loi sur la vidéosurveillance chez soi ?", "Filmer l'intérieur de son logement est libre, mais il faut informer les personnes filmées (invités, aide à domicile). En extérieur, la caméra ne doit pas filmer la voie publique ni le terrain du voisin. En cas de doute, consultez les recommandations de la CNIL."),
    ("D'où viennent les prix ?", "Nous affichons un prix indicatif par produit : le plus bas constaté sur Amazon ou chez Electro Dépôt lors de notre dernier relevé, arrondi à la dizaine d'euros. Pour Electro Dépôt, nous affichons aussi son prix exact, tiré de son flux produits officiel, avec la date du relevé. Vérifiez le prix et le vendeur sur la fiche du marchand avant d'acheter."),
]
