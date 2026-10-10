// Rend les vidéos verticales « Top 3 » (1080x1920, ~21 s).
//   node scripts/render-videos.mjs                 -> liste les usages disponibles
//   node scripts/render-videos.mjs e-gaming        -> rend un usage (clé : e-gaming, i-photo, gaming, d-mini…)
//   node scripts/render-videos.mjs famille ecran-pc -> rend tous les usages d'une famille (dossier d'URL)
// Fichiers écrits dans _video/out/video/<famille>-<usage>.mp4
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import {mkdirSync, readFileSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const racine = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const data = JSON.parse(readFileSync(path.join(racine, 'src/data.generated.json'), 'utf-8'));
const args = process.argv.slice(2);

if (!args.length) {
  console.log('Usages disponibles :');
  for (const u of data.usages) console.log(`  ${u.cle.padEnd(16)} ${u.famille}/${u.slug}`);
  process.exit(0);
}
const choisis = args[0] === 'famille' ? data.usages.filter((u) => u.famille === args[1]) : data.usages.filter((u) => u.cle === args[0]);
if (!choisis.length) {
  console.error('Aucun usage trouvé pour :', args.join(' '));
  process.exit(1);
}

const bundleLocation = await bundle({entryPoint: path.join(racine, 'src/index.ts'), publicDir: path.resolve(racine, '..')});
mkdirSync(path.join(racine, 'out/video'), {recursive: true});
for (const usage of choisis) {
  const composition = await selectComposition({serveUrl: bundleLocation, id: 'TopUsage', inputProps: {usage}});
  const sortie = path.join(racine, `out/video/${usage.famille}-${usage.slug}.mp4`);
  await renderMedia({composition, serveUrl: bundleLocation, codec: 'h264', outputLocation: sortie, inputProps: {usage}, crf: 20});
  console.log('OK', path.relative(racine, sortie));
}
