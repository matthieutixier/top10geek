# v16 — mesure des canaux de communication (29/10/2026)

- `main15.js` (copie de `main14.js` + source de la visite) : lit `utm_source` dans l'adresse d'arrivée (ex. `?utm_source=pinterest`), la garde le temps de la session (`sessionStorage`, ni cookie ni identifiant) et la joint aux signaux de clic ; envoie en plus un signal `m = 'arrivee'` par session quand une source est connue.
- `functions/api/clic.js` : nouvelle colonne `source` dans la table D1 `clics` (ajoutée automatiquement, `ALTER TABLE` ignoré si déjà présente).
- `politique-confidentialite.html` : une phrase ajoutée sur le canal d'arrivée.
- Lecture, par canal :
  - arrivées : `SELECT source, COUNT(*) n FROM clics WHERE marchand='arrivee' AND ts >= date('now','-30 day') GROUP BY 1 ORDER BY n DESC;`
  - clics marchands : `SELECT source, marchand, COUNT(*) n FROM clics WHERE marchand<>'arrivee' AND marchand<>'interne' AND ts >= date('now','-30 day') GROUP BY 1,2 ORDER BY n DESC;`
- Canaux utilisés : `pinterest` (épingles, via `_source/pins.py`), puis `reddit`, `linkedin`, `youtube`, `tiktok`, `instagram` (liens à étiqueter par `?utm_source=<canal>&utm_medium=social`).
