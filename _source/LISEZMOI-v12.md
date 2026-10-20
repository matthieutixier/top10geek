# Générateur v12 (20/10/2026) : ajustements de mise en page

Commande inchangée : `python3 _source/gen10.py` (fichiers v12 : `extra17.css` et `main12.js` ; prochains : `extra18.css`, `main13.js`).

1. **Accueil** : les chiffres (tests, produits, usages) remontent sous le texte ; les 4 rubriques forment une ligne sous le haut de page (2 par ligne sous 1 000 px ; une colonne sur mobile, placée avant la mascotte).
2. **Hubs famille** : mascotte du haut agrandie (`hero-badge tall big`).
3. **Carte du radar** (hubs et pages usage) : prix indicatif et marchands regroupés (`.d-buy`) ; le bouton « Voir chez … » en doublon est retiré ; grand bouton « Avis et tests détaillés » avec le nombre de tests et de notes (`#detailMore`, rempli par `main12.js`).
4. **Fiche produit, haut de page (ordinateur)** : verdict complété par `plus_verdict()` (points forts et réserve principale, mêmes données que la section consensus) et le rang ; encadrés Presse / Pour vous si / À éviter si calés en bas, le cadre d'achat s'étire pour finir à la même hauteur ; carte « le n° 1 » sous les deux colonnes. Mobile inchangé.
5. **Où l'acheter** : offres à gauche, encadré « Configuration de référence » à droite (`.p-buywrap`, `.p-specs.v12`), empilés sous 900 px.
