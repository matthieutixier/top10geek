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

FAMILIES_NEW = [
    dict(key="ecran", slug="ecran-pc", label="Écran PC", plural="Écrans PC", plural_low="écrans PC", cats=ECATS, provisional=False,
         m_labels=("Taille et définition", "Fréquence"), col="Taille", mascot="pose-ecran", noun="écran", noun_det="l'écran",
         h1='Comparatif écrans PC 2026 : <span class="flash">le verdict par usage</span>',
         intro="50 écrans PC passés au crible : bureautique, gaming, création, écrans portables et petits prix, avec une note presse sur 10, un prix indicatif et les liens vers les marchands.",
         title="Meilleur écran PC 2026 : tous les tests résumés par usage | Top 10 Geek",
         desc="50 écrans PC 2026 classés par usage avec une note presse sur 10 et un prix indicatif : bureautique, gaming, création, écrans portables, petits prix.",
         usage_title="Top 10 écrans PC {label} 2026 : tests résumés et prix | Top 10 Geek",
         usage_desc="Les 10 meilleurs écrans PC {label} en 2026, classés par note presse, avec photos, prix indicatif, points forts et points faibles."),
    dict(key="imprimante", slug="imprimante", label="Imprimante", plural="Imprimantes", cats=ICATS, provisional=False,
         m_labels=("Technologie", "Fonctions"), col="Technologie", mascot="pose-imprimante", noun="imprimante", noun_det="l'imprimante",
         h1='Comparatif imprimantes 2026 : <span class="flash">le verdict par usage</span>',
         intro="50 imprimantes classées par usage : réservoirs d'encre, laser noir et blanc, laser couleur, photo et petits prix, avec les tests de la presse et des associations de consommateurs, un prix indicatif et les liens vers les marchands.",
         title="Meilleure imprimante 2026 : tous les tests résumés par usage | Top 10 Geek",
         desc="50 imprimantes 2026 classées par usage avec les tests de la presse et des associations de consommateurs : réservoirs, laser, photo, petits prix.",
         usage_title="Top 10 imprimantes {label} 2026 : tests résumés et prix | Top 10 Geek",
         usage_desc="Les 10 meilleures imprimantes {label} en 2026 : tests de la presse et des associations de consommateurs, prix indicatif, points forts et points faibles."),
]

FAQ_E = [
    ("Comment est calculée la note presse ?", "C'est la moyenne simple des notes publiées par les médias spécialisés (Les Numériques, Tom's Hardware, RTINGS, TechRadar, Clubic…), toutes converties sur 10 : 4/5 devient 8/10, 87 % devient 8,7/10. Le nombre de tests est toujours affiché. Quand la note porte sur une variante proche de la même gamme, nous l'indiquons."),
    ("Comment est établi le classement ?", "En tête : « le choix de la bande », notre recommandation pour l'usage. Ensuite, les écrans sont classés par note presse. Ceux dont les tests ne donnent pas de note chiffrée viennent en dernier."),
    ("QHD ou 4K : quelle définition choisir ?", "Sur 27 pouces, le QHD (2560 × 1440) est le bon équilibre pour jouer et travailler. La 4K apporte un texte plus fin et convient à la création, mais demande une carte graphique puissante en jeu. Sur 32 pouces, la 4K devient vraiment confortable."),
    ("OLED ou IPS ?", "L'OLED offre un contraste infini et une réactivité immédiate, idéal pour jouer et regarder des films, mais il coûte plus cher et peut marquer si des éléments fixes restent affichés très longtemps. L'IPS reste le choix raisonnable pour la bureautique et un usage de plusieurs heures avec des fenêtres fixes."),
    ("D'où viennent les prix ?", "Nous affichons un prix indicatif par écran : le prix constaté sur Amazon lors de notre dernier relevé, arrondi à la dizaine d'euros. Il sert à situer l'écran, pas à comparer les marchands. Seul le prix affiché par le marchand fait foi."),
]

FAQ_I = [
    ("D'où viennent les tests des imprimantes ?", "Les imprimantes sont surtout testées en laboratoire par les associations de consommateurs (Test-Achats, Que Choisir, Which?, Tænk) et par quelques médias (Les Numériques, TechRadar, RTINGS…). Les associations réservent leurs notes à leurs abonnés : nous citons et lions leurs tests sans note chiffrée, et la note presse n'est calculée que sur les notes publiques."),
    ("Comment est établi le classement ?", "En tête : « le choix de la bande », notre recommandation pour l'usage. Ensuite, les imprimantes sont classées par note presse. Celles dont les tests ne donnent pas de note chiffrée viennent en dernier."),
    ("Réservoir d'encre ou cartouches ?", "Au-delà de quelques pages par semaine, le réservoir est presque toujours gagnant : plus cher à l'achat, mais l'encre fournie suffit pour des milliers de pages. Pour imprimer très rarement, une imprimante à cartouches bon marché reste plus simple, à condition d'accepter des cartouches chères."),
    ("Laser ou jet d'encre ?", "La laser imprime vite, le toner ne sèche jamais et le texte est très net : c'est le meilleur choix pour les documents. Le jet d'encre reste indispensable pour les photos et polyvalent à la maison."),
    ("D'où viennent les prix ?", "Nous affichons un prix indicatif par imprimante : le prix constaté sur Amazon lors de notre dernier relevé, arrondi à la dizaine d'euros. Quand l'imprimante n'est proposée que par un vendeur tiers sur Amazon, nous l'indiquons. Seul le prix affiché par le marchand fait foi."),
]
