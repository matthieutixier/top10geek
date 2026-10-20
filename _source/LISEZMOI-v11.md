# Générateur v11 (20/10/2026) : fiche produit orientée achat et mesure des clics

Commande inchangée : `python3 _source/gen10.py` (les fichiers v11 sont `extra16.css` et `main11.js` ; prochains : `extra17.css`, `main12.js`).

## Ce qui change

1. **Indexation** (`indexable()`) : une fiche produit est indexée si elle a au moins 2 notes chiffrées **ou** au moins 2 tests presse recensés (même sans note publique). Les fiches à un seul test restent en `noindex,follow` et hors sitemap. Affichage inchangé (« peu testé », « testé, sans note »).
2. **Fiche produit, haut de page** (`product_page`, `buy_btn`, v11c) : deux variantes dans la page, le CSS choisit.
   - **Ordinateur et tablette** (maquette validée par Matthieu) : à gauche, rang dans le top, titre, verdict, trois encadrés (Presse / Pour vous si / À éviter si ; la section « Pour qui » plus bas est alors masquée) et carte « Avant d'acheter : le n° 1 des … » (`CARTE_N1`) ; à droite, un cadre avec photo, prix indicatif « le plus bas relevé » et un bouton par marchand en vente (le premier en couleur, ordre de `AFFILIATED`).
   - **Mobile (≤ 700 px)** : version discrète v11b : photo réduite à côté du verdict, note, prix, un seul bouton, les autres marchands en liens texte « Aussi chez … · toutes les offres » ; ni encadrés ni carte n° 1.
3. **Barre d'achat fixe sur mobile** (`#buyBar`, `main11.js`) : apparaît une fois le bloc d'achat dépassé, se masque sur la liste des offres et le pied de page.
4. **Titres des fiches** : note, nombre de notes presse et prix indicatif quand ils tiennent en 65 caractères (ex. « Geekom IT13 : avis et tests, 8,3/10 (21 notes), env. 590 € »).
5. **Mesure des clics marchands** : `main11.js` envoie au clic un signal (`navigator.sendBeacon`) vers `/api/clic` (`functions/api/clic.js`, Cloudflare Pages Functions). Données : page, marchand, produit, zone du lien (`data-z` : haut, offres, bas, barre, choix, top10, radar), appareil, date. Ni cookie, ni IP, ni identifiant. Les liens marchands restent des liens directs (aucune redirection).

## Mise en service de la mesure (une fois, tableau de bord Cloudflare)

1. Workers & Pages > D1 > Créer une base : `top10geek-clics`.
2. Projet Pages `top10geek` > Paramètres > Liaisons > Ajouter > Base de données D1 : nom de variable `DB`, base `top10geek-clics` (production et aperçu).
3. Redéployer (ou attendre le prochain push). La table `clics` se crée seule au premier clic.

Sans liaison, `/api/clic` répond 204 et n'enregistre rien.

## Lire les chiffres (console D1)

```sql
SELECT page, marchand, zone, COUNT(*) AS n FROM clics
WHERE ts >= date('now', '-30 day') GROUP BY 1, 2, 3 ORDER BY n DESC;
```
