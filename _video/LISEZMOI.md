# _video — vidéos verticales et images de partage (Remotion)

Tout est généré depuis `_source/data.json` : même classement, mêmes notes presse, mêmes prix indicatifs que le site. Les images et la charte viennent de `assets/` (mascottes, badges, photos produits, polices Bricolage Grotesque / Plus Jakarta Sans / IBM Plex Mono, rouge `#FF3B57`).

## Installation (une fois, sur l'ordinateur qui fera les rendus)
```
cd _video
npm install
```
Remotion télécharge lui-même son Chrome au premier rendu (ou utilise celui indiqué par la variable `REMOTION_CHROME`). Python 3 est nécessaire pour l'export des données.

## Chaque fois
```
python3 export_data.py            # data.json -> src/data.generated.json  (à refaire après chaque mise à jour des données)
node scripts/render-og.mjs        # 24 images de partage -> ../assets/img/og/  (4 familles + 20 usages)
node scripts/render-videos.mjs                      # liste les 20 usages
node scripts/render-videos.mjs e-gaming             # un usage -> out/video/ecran-pc-gaming.mp4
node scripts/render-videos.mjs famille ecran-pc     # tous les usages d'une famille
node scripts/render-long.mjs                        # liste les usages pour la vidéo longue
node scripts/render-long.mjs d-mini apercu          # une image par scène -> out/long/apercu/ (à contrôler avant le rendu)
node scripts/render-long.mjs d-mini                 # vidéo longue « Top 10 » -> out/long/ordinateur-de-bureau-mini-pc.mp4
npm run studio                    # aperçu interactif (réglages, nouvelles scènes)
```
Après `render-og.mjs`, relancer `python3 _source/gen10.py` : le générateur pose l'image dédiée dans `og:image` / `twitter:image` des pages famille et usage (fonction `og_pour`). Les pages produit gardent la photo du produit, les autres pages l'image générique.

## Vidéo « Top 3 » (1080×1920, 21 s, 30 i/s)
Intro (titre + mascotte + badge de l'usage) → #3 → #2 → #1 (photo, nom, note presse animée, nombre de notes et de tests, premier point fort, prix indicatif et mois) → outro (adresse de la page usage). Le garde-fou du site s'applique : « 1 seul test noté » / « 2 tests notés seulement » sous 3 notes ; un produit sans note publique s'affiche « testé, sans note ».
Les vidéos ne montrent aucun prix attribué à un marchand (règle du 05/10/2026) et ne contiennent aucun lien : l'adresse de la page est dans la vidéo, le lien va dans la description de la publication.

L'écran final dit « Retrouvez-nous sur top10geek.fr pour en savoir plus » (12/11/2026), avec l'adresse de la page.

## Vidéo longue « Top 10 » (1920×1080, 2 min 15, 30 i/s, avec musique) — `src/Top10Long.tsx`
Pour YouTube, où le lien de la description est cliquable (il ne l'est pas sous un Short). Intro (titre, nombre de tests) → « Comment on classe » (tests recensés, notes, aucun marchand mis en avant) → compte à rebours du n° 10 au n° 1 (9 s par produit, 14 s pour le podium avec le verdict) → classement complet → fin (adresse de la page, « lien dans la description »). Un rail en bas d'écran montre où l'on en est. Mêmes garde-fous que le Top 3 : « 1 seul test noté », « testé, sans note », aucun prix attribué à un marchand.
- Une fiche chargée (nom sur deux lignes, textes longs) passe seule en mise en page resserrée ; contrôler quand même l'aperçu avant chaque rendu.
- À réserver aux usages dont la plupart des produits ont une note presse : avec beaucoup de « testé, sans note », la vidéo perd son intérêt.
- Musique de fond : `audio/newer-wave.mp3` (Kevin MacLeod, CC BY 4.0). **Le crédit de `audio/LISEZMOI.md` doit figurer dans la description YouTube de chaque vidéo.**
- `export_data.py` exporte pour cela `forts` (3 points forts) et `faibles` (2 points faibles) par produit.

## Points d'attention
- Les photos produits sont celles du site : certaines gardent du texte marketing constructeur (ex. AOC Agon Q27G4ZD). À remplacer à la source (voir CLAUDE.md, section Photos), la vidéo suivra.
- Nouvelle famille ou nouvel usage : `export_data.py` lit `ECATS`/`ICATS` (`familles_new.py`) ; ajouter la famille dans la liste `FAMILLES` du script, plus un titre dans `H1` pour les PC.
- `_video/out/` et `src/data.generated.json` ne sont pas versionnés.
