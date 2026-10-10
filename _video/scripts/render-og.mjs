// Rend les images de partage (OG, 1200x630) : une par famille (4) et une par usage (20).
//   node scripts/render-og.mjs
// Fichiers écrits dans assets/img/og/ (à la racine du dépôt) :
//   <famille>.jpg et <famille>-<usage>.jpg   (ex. ecran-pc.jpg, ecran-pc-gaming.jpg)
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import {mkdirSync, readFileSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const racine = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const depot = path.resolve(racine, '..');
const data = JSON.parse(readFileSync(path.join(racine, 'src/data.generated.json'), 'utf-8'));
const dossier = path.join(process.env.OG_OUT || depot, 'assets/img/og');
mkdirSync(dossier, {recursive: true});

const jobs = [];
for (const f of data.familles) {
  const us = data.usages.filter((u) => u.famille === f.slug);
  jobs.push({
    fichier: `${f.slug}.jpg`,
    props: {mode: 'famille', usage: us[0], titre: `Comparatif ${f.noun} 2026 : le verdict par usage`, soustitre: '50 produits · notes de la presse résumées'},
  });
  for (const u of us) {
    jobs.push({
      fichier: `${f.slug}-${u.slug}.jpg`,
      props: {mode: 'usage', usage: u, titre: u.titre10.replace(/ en 2026$/, ''), soustitre: 'Note presse sur 10 · prix indicatif'},
    });
  }
}

// Chrome à utiliser (facultatif) : REMOTION_CHROME=/chemin/vers/chrome ; sinon Remotion télécharge le sien.
const browserExecutable = process.env.REMOTION_CHROME || null;
const bundleLocation = await bundle({entryPoint: path.join(racine, 'src/index.ts'), publicDir: depot});
for (const j of jobs) {
  const composition = await selectComposition({browserExecutable, serveUrl: bundleLocation, id: 'Og', inputProps: j.props});
  await renderStill({browserExecutable, composition, serveUrl: bundleLocation, output: path.join(dossier, j.fichier), imageFormat: 'jpeg', jpegQuality: 86, inputProps: j.props});
  console.log('OK', j.fichier);
}
