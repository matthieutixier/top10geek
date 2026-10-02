# Top 10 Geek — générateur v8 (02/10/2026)

Chaîne de production du site :

1. `catalog.py` — les 100 ordinateurs (textes, usages, sources presse). C'est le fichier à modifier pour ajouter ou retirer une machine.
2. `profiles.py` — « pour qui » / « à éviter si » de chaque machine (fiches produits). À compléter pour toute nouvelle machine, sinon le générateur s'arrête.
3. `build_data.py` — assemble `data.json` : notes presse (`data/cc_det_*.json`, relevées sur CommentChoisir + tests saisis à la main), offres marchands (`darty_releve_2026-10-02.json`, `data/amazon.json`, `data/geekom.json`, Acer Store dans le script) et télécharge les photos produits (`assets/img/p/`).
4. `gen8.py` — génère les pages HTML, `assets/style.css` (concaténation des CSS, dont `extra9.css` pour la v8) et `assets/main.js` (`main8.js`). Se lance depuis n'importe où : `python3 _source/gen8.py` écrit directement à la racine du dépôt.

Nouveautés v8 :

- bloc « Notre choix » en haut de chaque page usage (verdict, 3 points forts, 1 réserve, bouton marchand) et 3 alternatives calculées sur les données (prix, note presse, poids pour les portables ou nombre de tests pour les ordinateurs de bureau) ;
- tableau supprimé sur les comparatifs, remplacé par un sélecteur « Trier par » sur les fiches ;
- une page par ordinateur (`/pc-portable/asus-zenbook-a14/`…) : consensus presse, pour qui / à éviter si, prix par marchand, tous les tests, alternatives, FAQ ;
- sitemap étendu aux 100 fiches.

Photos : aucune image ne vient d'Amazon (leur charte ne l'autorise que via leur API). Les 22 modèles concernés utilisent une photo officielle du constructeur, listée dans `photos_constructeurs.json` ; pour toute nouvelle machine sans visuel Darty/Geekom/Acer, ajouter une photo constructeur dans ce fichier.

Règles de sélection : chaque machine doit être en vente chez au moins un marchand partenaire (Amazon, Darty, Fnac, Acer Store, Geekom) et avoir au moins un test presse.

À renseigner : `AMAZON_TAG` dans `build_data.py` (identifiant Partenaires Amazon) pour que tous les liens Amazon soient affiliés ; les liens Darty / Acer / Geekom sont pour l'instant directs, à remplacer par les liens Awin une fois les programmes validés.

`build_data.py` utilise encore les chemins `/home/claude/` de l'espace de travail de Claude ; `gen8.py` n'en dépend plus.
