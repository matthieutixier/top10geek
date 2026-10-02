# Top 10 Geek — générateur v7 (02/10/2026)

Chaîne de production du site :

1. `catalog.py` — les 100 ordinateurs (textes, usages, sources presse). C'est le fichier à modifier pour ajouter ou retirer une machine.
2. `build_data.py` — assemble `data.json` : notes presse (`data/cc_det_*.json`, relevées sur CommentChoisir + tests saisis à la main), offres marchands (`darty_releve_2026-10-02.json`, `data/amazon.json`, `data/geekom.json`, Acer Store dans le script) et télécharge les photos produits (`assets/img/p/`).
3. `gen7.py` — génère les pages HTML, `assets/style.css` (concaténation des CSS dont `extra7.css`, `extra8.css` (confort mobile)) et `assets/main.js` (`main7.js`).

Règles de sélection : chaque machine doit être en vente chez au moins un marchand partenaire (Amazon, Darty, Fnac, Acer Store, Geekom) et avoir au moins un test presse.

À renseigner : `AMAZON_TAG` dans `build_data.py` (identifiant Partenaires Amazon) pour que tous les liens Amazon soient affiliés ; les liens Darty / Acer / Geekom sont pour l'instant directs, à remplacer par les liens Awin une fois les programmes validés.

Les scripts utilisent les chemins `/home/claude/` de l'espace de travail de Claude (comme les versions précédentes).
