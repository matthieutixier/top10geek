# Top 10 Geek — générateur v10 (09/10/2026)

La v10 ajoute deux familles aux PC portables et ordinateurs de bureau : **Écrans PC** (`/ecran-pc/`) et **Imprimantes** (`/imprimante/`). 4 familles, 20 usages, 200 produits, 230 pages.

## Commandes

```
python3 _source/build_new.py   # (re)met les écrans et imprimantes dans data.json
python3 _source/gen10.py       # génère tout le site à la racine du dépôt
```

`gen9.py` est conservé (ancienne version, 2 familles) ; `gen8.py` reste la base pour réactiver le comparateur de prix.

## Fichiers ajoutés

| Fichier | Rôle |
|---|---|
| `catalog_ecrans.py` | les 50 écrans : textes, notes presse (source, note ou `None`, URL), ASIN Amazon, prix relevé, vendeur, « pour qui / à éviter si » |
| `catalog_imprimantes.py` | les 50 imprimantes, même format |
| `familles_new.py` | usages, titres, textes et FAQ des deux familles |
| `guides_new.py` | guides « Comment choisir » des 10 nouveaux usages |
| `build_new.py` | fusionne les deux catalogues dans `data.json` (garde prix et disponibilité d'un relevé `releve.py` antérieur) |
| `gen10.py` | générateur 4 familles |
| `extra12.css` | menu à 4 onglets, ligne « Nouveau » de l'accueil |

**Ajouter ou retirer un écran / une imprimante** : modifier `catalog_ecrans.py` ou `catalog_imprimantes.py` (10 produits exactement par usage, sinon `gen10.py` s'arrête), puis `build_new.py` et `gen10.py`.

## Usages

- Écrans : bureautique, gaming, création, portable (écrans USB-C nomades), petit-prix (< 200 €).
- Imprimantes : reservoir, laser-noir-et-blanc, laser-couleur, photo, petit-prix (< 150 €).

## Sources presse

- Écrans : Les Numériques, Tom's Hardware, RTINGS, TechRadar, Clubic, 01net, Monitornerds… (relevé via CommentChoisir puis vérifié).
- Imprimantes : surtout associations de consommateurs (Test-Achats, Que Choisir, Which?, Tænk). Leurs notes sont réservées aux abonnés : test cité et lié **sans note** ; la note presse ne porte que sur les notes publiques. Un produit sans aucune note publique s'affiche « testé, sans note » et passe en fin de classement.

## Offres et photos

- Offre unique Amazon (`geekconcept-21`). Quelques produits ne sont vendus que par un vendeur tiers sur Amazon : mention « vendu par un vendeur tiers ».
- Photos : fiches constructeurs via le catalogue ouvert Icecat (images fournies par les marques) ou sites constructeurs (Dell, Sony, Asus, Canon), détourées en 560×420 sur fond blanc. Source de chaque photo dans `photos_constructeurs.json`. Aucune photo Amazon. 17 produits sans photo (pas de visuel officiel fiable trouvé).

## Mise à jour hebdomadaire (une rubrique par semaine)

Tâche planifiée « Mise à jour hebdomadaire Top10Geek » (vendredi 9 h, ordinateur de Matthieu). Chaque semaine, la rubrique la moins récemment traitée est mise à jour (plus ancienne des deux dates `iso` et `tente` de `familles` dans `data.json`) : les données ont donc au plus 4 semaines.

```
python3 _source/releve.py --famille ecran --only Amazon,Geekom --duree 140 --apply   # relancer tant que « INCOMPLET »
python3 _source/releve.py --famille ecran --only Amazon,Geekom --cloturer --apply    # si captchas persistants : applique ce qui a été lu
python3 _source/releve.py --famille ecran --manuel _source/data/manuel.json --apply  # Acer Store lu à la main
python3 _source/ajout_tests.py _source/data/nouveaux_tests.json --apply             # nouveaux tests presse
python3 _source/gen10.py
```

- `--famille` (portable, bureau, ecran, imprimante) limite le relevé à une rubrique et note la tentative (`tente`) ; sa date affichée (`familles.<rubrique>`) n'avance que si au moins la moitié de ses offres ont été relues. Les pages d'une rubrique affichent sa propre date « MAJ » et son mois de prix ; les pages communes (accueil, Black Friday) affichent le mois le plus ancien.
- Amazon bloque vite (captchas) : après 3 passes espacées de 15 à 20 minutes, `--cloturer` applique les prix déjà relus ; les offres non relues gardent leur ancien prix. Constat du test du 09/10/2026 (PC portables) : 20 offres Amazon sur 41 relues avant blocage durable.
- `ajout_tests.py` ajoute des tests (une URL réelle par test, note ramenée sur 10 ou `null`), recalcule la note presse et marque l'ajout (`"ajout": "JJ/MM/AAAA"`). `build_new.py` conserve ces ajouts.
