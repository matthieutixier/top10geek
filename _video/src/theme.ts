import '@fontsource-variable/bricolage-grotesque';
import '@fontsource/plus-jakarta-sans/400.css';
import '@fontsource/plus-jakarta-sans/600.css';
import '@fontsource/plus-jakarta-sans/700.css';
import '@fontsource/ibm-plex-mono/500.css';
import {continueRender, delayRender} from 'remotion';

// Charte du site (assets/style.css)
export const C = {
  accent: '#FF3B57',
  ink: '#15171C',
  muted: '#5A5E6B',
  faint: '#9297A3',
  paper: '#F7F6F1',
  paperAlt: '#EFECE3',
  white: '#FFFFFF',
  highlight: '#FFC93D',
  line: '#15171C',
};
export const FONT = {
  title: "'Bricolage Grotesque Variable', 'Bricolage Grotesque', sans-serif",
  body: "'Plus Jakarta Sans', sans-serif",
  mono: "'IBM Plex Mono', monospace",
};
export const BASELINE = 'Tous les tests high-tech, résumés pour vous';

/** Attend que les polices soient chargées avant de rendre une image. */
export const attendreLesPolices = () => {
  const h = delayRender('polices');
  Promise.all([
    document.fonts.load("800 40px 'Bricolage Grotesque Variable'"),
    document.fonts.load("700 40px 'Plus Jakarta Sans'"),
    document.fonts.load("400 40px 'Plus Jakarta Sans'"),
    document.fonts.load("500 40px 'IBM Plex Mono'"),
  ]).then(() => document.fonts.ready).then(() => continueRender(h)).catch(() => continueRender(h));
};

export type Produit = {
  rang: number; id: string; nom: string; ref: string; badge: string; verdict: string; fort: string;
  img: string | null; prix: string; note: number | null; nnotes: number; ntests: number;
};
export type Usage = {
  famille: string; familleLabel: string; noun: string; mascotte: string; cle: string; slug: string; label: string;
  couleur: string; badge: string; titre3: string; titre10: string; prixDate: string; maj: string; top: Produit[];
};

export const virgule = (n: number) => n.toFixed(1).replace('.', ',');
