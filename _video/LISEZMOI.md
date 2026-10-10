# _video — vidéos verticales et images de partage (Remotion)

Tout est généré depuis `_source/data.json` : même classement, mêmes notes presse, mêmes prix indicatifs que le site. Les images et la charte viennent de `assets/` (mascottes, badges, photos produits, polices Bricolage Grotesque / Plus Jakarta Sans / IBM Plex Mono, rouge `#FF3B57`).

## Installation (une fois, sur l'ordinateur qui fera les rendus)
```
cd _video
npm install
```
Remotion télécharge lui-même son Chrome au premier rendu. Python 3 est nécessaire pour l'export des données.

## Chaque fois
```
python3 export_data.py            # data.json -> src/data.generated.json  (à refaire après chaque mise à jour des données)
node scripts/render-og.mjs        # 24 images de partage -> ../assets/img/og/  (4 familles + 20 usages)
node scripts/render-videos.mjs                      # liste les 20 usages
node scripts/render-videos.mjs e-gaming             # un usage -> out/video/ecran-pc-gaming.mp4
node scripts/render-videos.mjs famille ecran-pc     # tous les usages d'une famille
npm run studio                    # aperçu interactif (réglages, nouvelles scènes)
```
Après `render-og.mjs`, relancer `python3 _source/gen10.py` : le générateur pose l'image dédiée dans `og:image` / `twitter:image` des pages famille et usage (fonction `og_pour`). Les pages produit gardent la photo du produit, les autres pages l'image générique.

## Vidéo « Top 3 » (1080×1920, 21 s, 30 i/s)
Intro (titre + mascotte + badge de l'usage) → #3 → #2 → #1 (photo, nom, note presse animée, nombre de notes et de tests, premier point fort, prix indicatif et mois) → outro (adresse de la page usage). Le garde-fou du site s'applique : « 1 seul test noté » / « 2 tests notés seulement » sous 3 notes ; un produit sans note publique s'affiche « testé, sans note ».
Les vidéos ne montrent aucun prix attribué à un marchand (règle du 05/10/2026) et ne contiennent aucun lien : l'adresse de la page est dans la vidéo, le lien va dans la description de la publication.

## Points d'attention
- Les photos produits sont celles du site : certaines gardent du texte marketing constructeur (ex. AOC Agon Q27G4ZD). À remplacer à la source (voir CLAUDE.md, section Photos), la vidéo suivra.
- Nouvelle famille ou nouvel usage : `export_data.py` lit `ECATS`/`ICATS` (`familles_new.py`) ; ajouter la famille dans la liste `FAMILLES` du script, plus un titre dans `H1` pour les PC.
- `_video/out/` et `src/data.generated.json` ne sont pas versionnés.
