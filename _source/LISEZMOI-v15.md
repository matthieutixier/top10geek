# v15 — Black Friday 2026 (toutes rubriques)

- **Page `/black-friday/`** : bloc « Baisses constatées » (haut de page), réflexes, un « Notre choix » par usage pour les 8 rubriques, pièges par catégorie, FAQ.
- **Baisses** (`bf_baisses()` dans `gen10.py`) : prix du jour comparé au plus bas prix du MÊME marchand sur les 30 jours précédant `BF_DEBUT` (23/11/2026). Seuil 5 %, note presse ≥ 7/10 sur ≥ 3 notes (≥ 2 pour la Maison), marchands affiliés seulement, sans reconditionnés ni vendeurs tiers Amazon. Avant `BF_DEBUT`, le bloc affiche un message de préparation.
- **Historique** : `_source/historique_prix.json`, alimenté par `python3 _source/bf_historique.py` (à lancer après chaque relevé de prix, puis `gen10.py`). `--seed-git 35` reconstitue les jours passés depuis Git ; `--etat` résume.
- **Bandeau d'accueil** : interrupteur `BF_ACTIF` dans `gen10.py`. `False` + régénération = bandeau et lien d'accueil retirés (la page reste en ligne, le lien du pied de page aussi).
- Clics : bouton marchand en zone `data-z="bf"`, lien vers la fiche en `data-zi="bf-fiche"`.
- CSS : `extra23.css`.
