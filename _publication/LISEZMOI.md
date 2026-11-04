# Publication par fichier de modifications

Les tâches planifiées (mise à jour Informatique du vendredi, Maison du mercredi, relevé quotidien Black Friday)
n'ont pas d'accès git en écriture. Elles déposent donc sur `main`, avec les outils GitHub, deux petits fichiers :

- `_publication/AAAA-MM-JJ-<tâche>.patch` : un `git diff` des SEULES sources de données
  (`_source/data.json`, `catalog_*.py`, `cc_fiches_*.json`, `syntheses_*.json`, `historique_prix.json`, `manuel_*.json`) ;
- `_publication/AAAA-MM-JJ-<tâche>.msg` : le message de commit (première ligne = titre, puis les lignes d'attribution).

Le workflow `.github/workflows/publier.yml` se déclenche sur ce dépôt de fichier et lance
`_source/publier_patch.py`, qui :

1. refuse tout patch qui touche autre chose que des données (jamais `gen10.py`, `classement.py`, HTML, robots…) ;
2. applique le patch, remet la date globale `date` de `data.json` à sa valeur d'avant (règle SEO 6) ;
3. régénère le site (`gen10.py`, Python 3.12 + Pillow) ;
4. contrôle les règles SEO du § 6 bis : aucune page ne passe en `noindex`, aucune URL retirée du sitemap,
   au plus 30 nouvelles pages indexables, canoniques et H1 inchangés, lastmod seulement pour les pages changées
   (jamais plus de 40 % des URL), JSON-LD valides, ni `Offer` seule, ni `AggregateRating`, ni `Review`,
   ni `shippingDetails`, pas de `utm_` ajouté, navigation légale non empilée ;
5. si tout est bon : commit au nom de Matthieu Tixier et push sur `main` (Cloudflare Pages déploie) ;
   sinon : RIEN n'est publié, le patch est rangé dans `_publication/refuses/` avec son journal `.log`,
   et le workflow passe au rouge (GitHub envoie un e-mail).

Ce que le patch ne contient jamais : le HTML, le sitemap et `sitemap_dates.json` (générés par le workflow),
les fichiers secrets (`effinity.local.json`). Les images de produits sont déposées par un autre moyen
(rubrique par PR) : ce parcours ne gère que les données.

Reprise manuelle : `Actions > Publier une mise à jour de données > Run workflow` retraite les fichiers
`_publication/*.patch` restants. Essai local :
`python3.12 _source/publier_patch.py chemin/vers/fichier.patch` (sur un dépôt propre ; ne commite rien).
