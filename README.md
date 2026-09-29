# Top 10 Geek — site statique (v6)

Structure : accueil (`index.html`), familles `pc-portable/` et `ordinateur-de-bureau/` (page comparatif + une page par usage), `methode.html`, pages légales.

## Régénérer le site
Sources dans `_source/` : `gen6.py` (générateur), `laptops.json` + `press.py` + `specs.py` (PC portables), `desk.py` (ordinateurs de bureau — sélection provisoire), `guides.py` / `guides_desk.py` (guides d'achat).

## Publication
Dépôt Git → Cloudflare Pages. Ne pas publier `_archive_v2` (ignoré par .gitignore).
