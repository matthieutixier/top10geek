# Générateur v13 (20/10/2026) : note presse en grand et radar de la fiche

Commande inchangée : `python3 _source/gen10.py` (fichiers v13 : `extra18.css` et `main13.js` ; prochains : `extra19.css`, `main14.js`).

1. **Verdict v12 allégé** : le complément `plus_verdict()` (doublon du consensus) n'est plus affiché.
1. **Note presse en grand** dans le haut de fiche, sur ordinateur (`score_haut()`) : note, nombre de notes, tests et médias, date du dernier test ; lien vers le consensus. Le mobile garde son bloc `press-big`. L'encadré « Presse » devient « Lu chez » (médias + lien vers tous les tests).
2. **Radar de la fiche** (`radar_fiche()`, section `#radar` sous le haut de fiche) : les 10 produits de l'usage (note presse × prix), bulles numérotées par rang et cliquables vers leur fiche, produit de la fiche mis en avant ; à droite, pastilles calculées (rang par note, rang par prix, zone « bonnes affaires »), phrase de lecture, liste du top 10, bouton « Voir le top 10 et le comparatif → ». Mobile : ligne « note presse » et 3 lignes de la liste (n° 1, ce modèle, son voisin). Remplace la carte « le n° 1 » (`CARTE_N1 = False`).
3. **Mesure des clics internes** (`main13.js`) : un lien interne n'est compté que dans une zone `data-zi` ; il est enregistré avec marchand = `interne`, produit = page visée, zone = `i-radar-fiche` ou `i-alternatives`.

Lecture (console D1) :

```sql
SELECT zone, COUNT(*) n FROM clics WHERE marchand = 'interne' AND ts >= date('now','-30 day') GROUP BY 1;
```
