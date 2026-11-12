// Rend les vidéos longues « Top 10 » (1920x1080, ~2 min 15, sans son).
//   node scripts/render-long.mjs                  -> liste les usages disponibles
//   node scripts/render-long.mjs d-mini           -> rend un usage -> out/long/<famille>-<usage>.mp4
//   node scripts/render-long.mjs d-mini apercu    -> une image par scène -> out/long/apercu/ (contrôle avant rendu)
import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';
import {mkdirSync, readFileSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const racine = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const data = JSON.parse(readFileSync(path.join(racine, 'src/data.generated.json'), 'utf-8'));
const [cle, mode] = process.argv.slice(2);

if (!cle) {
  console.log('Usages disponibles :');
  for (const u of data.usages) console.log(`  ${u.cle.padEnd(16)} ${u.famille}/${u.slug}`);
  process.exit(0);
}
const usage = data.usages.find((u) => u.cle === cle);
if (!usage) {
  console.error('Aucun usage trouvé pour :', cle);
  process.exit(1);
}
if (usage.top.length < 10) {
  console.error(`L'usage ${cle} n'a que ${usage.top.length} produits : la vidéo longue en demande 10.`);
  process.exit(1);
}

const browserExecutable = process.env.REMOTION_CHROME || null;
const serveUrl = await bundle({entryPoint: path.join(racine, 'src/index.ts'), publicDir: path.resolve(racine, '..')});
const composition = await selectComposition({browserExecutable, serveUrl, id: 'Top10Long', inputProps: {usage}});

if (mode === 'apercu') {
  // Une image vers la fin de chaque scène : intro, méthode, n° 10 à n° 1, récapitulatif, fin.
  const durees = [150, 210, ...Array(7).fill(270), ...Array(3).fill(420), 300, 240];
  const noms = ['intro', 'methode', 'n10', 'n09', 'n08', 'n07', 'n06', 'n05', 'n04', 'n03', 'n02', 'n01', 'recap', 'fin'];
  mkdirSync(path.join(racine, 'out/long/apercu'), {recursive: true});
  let debut = 0;
  for (let i = 0; i < durees.length; i++) {
    const frame = debut + Math.round(durees[i] * 0.8);
    const output = path.join(racine, `out/long/apercu/${String(i + 1).padStart(2, '0')}-${noms[i]}.jpeg`);
    await renderStill({browserExecutable, composition, serveUrl, frame, output, inputProps: {usage}, imageFormat: 'jpeg', jpegQuality: 85});
    debut += durees[i];
  }
  console.log('OK apercu', usage.cle);
} else {
  mkdirSync(path.join(racine, 'out/long'), {recursive: true});
  const sortie = path.join(racine, `out/long/${usage.famille}-${usage.slug}.mp4`);
  await renderMedia({browserExecutable, composition, serveUrl, codec: 'h264', outputLocation: sortie, inputProps: {usage}, crf: 20});
  console.log('OK', path.relative(racine, sortie));
}
