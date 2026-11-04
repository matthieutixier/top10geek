# v15 — Black Friday 2026 (toutes rubriques)

- **Page `/black-friday/`** : bloc « Baisses constatées » (haut de page), réflexes, un « Notre choix » par usage pour les 8 rubriques, pièges par catégorie, FAQ.
- **Baisses** (`bf_baisses()` dans `gen10.py`) : prix du jour comparé au plus bas prix du MÊME marchand sur les 30 jours précédant `BF_DEBUT` (23/11/2026). Seuil 5 %, note presse ≥ 7/10 sur ≥ 3 notes (≥ 2 pour la Maison), marchands affiliés seulement, sans reconditionnés ni vendeurs tiers Amazon. Avant `BF_DEBUT`, le bloc affiche un message de préparation.
- **Historique** : `_source/historique_prix.json`, alimenté par `python3 _source/bf_historique.py` (à lancer après chaque relevé de prix, puis `gen10.py`). `--seed-git 35` reconstitue les jours passés depuis Git ; `--etat` résume.
- **Bandeau d'accueil** : interrupteur `"bf_actif"` à la racine de `_source/data.json` (absent ou `false` à la mise en ligne ; passé à `true` le 22/11/2026 et remis à `false` le 01/12/2026 par des tâches planifiées, via un fichier de modifications déposé dans `_publication/`). `false` + régénération = bandeau et lien d'accueil retirés (la page reste en ligne, le lien du pied de page aussi). `gen10.py` le lit dans `BF_ACTIF`.
- Clics : bouton marchand en zone `data-z="bf"`, lien vers la fiche en `data-zi="bf-fiche"`.
- CSS : `extra23.css`.
- Garde-fou : une baisse de plus de `BF_BAISSE_MAX` (50 %) n'est jamais affichée (erreur de relevé probable).
