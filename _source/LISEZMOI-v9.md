# Top 10 Geek — générateur v9 (05/10/2026)

Le comparateur de prix est mis en veille : Darty et l'Acer Store bloquent toute lecture automatique,
et Amazon affiche des captchas après une soixantaine de pages. Le site affiche désormais :

- **un prix indicatif par produit** (`prix` dans `data.json`, constaté `prix_date`), arrondi à la dizaine ;
- **les liens vers les marchands où le produit est en vente**, sans prix par marchand (le marchand affilié en premier ;
  une offre marquée `"dispo": false` n'est plus affichée, sauf s'il ne reste qu'elle).

Les prix par marchand restent dans `data.json` (`price` de chaque offre) pour réactiver le comparateur
quand les flux affiliés (Awin, API Amazon) seront disponibles : repartir alors de `gen8.py` pour l'affichage.

Commande : `python3 _source/gen9.py` (CSS : `extra10.css` ; JS : `main9.js`). `gen8.py` est conservé pour référence.

Mise à jour mensuelle :

- `python3 _source/releve.py --only Amazon,Geekom --duree 140 --apply` (à relancer jusqu'à la fin ; s'arrêter si Amazon
  affiche des captchas et reprendre plus tard) ;
- Acer Store : lecture à la main dans un navigateur, puis `python3 _source/releve.py --manuel fichier.json --apply` ;
- Darty : non lisible (anti-robot) ; le dernier prix connu est conservé.

Le reste de la chaîne (catalog.py, profiles.py, build_data.py) est inchangé : voir `LISEZMOI-v8.md`.
