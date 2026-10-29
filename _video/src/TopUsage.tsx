import React from 'react';
import {AbsoluteFill, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {BASELINE, C, FONT, Produit, Usage, attendreLesPolices, virgule} from './theme';

export const FPS = 30;
const INTRO = 90;
const SCENE = 150;
const OUTRO = 90;
export const DUREE_TOP3 = INTRO + 3 * SCENE + OUTRO;

const Fond: React.FC<{couleur: string}> = ({couleur}) => (
  <AbsoluteFill style={{background: C.paper}}>
    <AbsoluteFill style={{background: couleur.toUpperCase() === '#1F9E6E' ? '#7C3AED' : couleur, opacity: 0.22}} />
    <AbsoluteFill
      style={{
        backgroundImage: `radial-gradient(${C.ink}14 2px, transparent 2px)`,
        backgroundSize: '28px 28px',
      }}
    />
    <div style={{position: 'absolute', left: 0, top: 0, width: 1080, height: 26, background: couleur.toUpperCase() === '#1F9E6E' ? '#7C3AED' : couleur}} />
    <div style={{position: 'absolute', left: 0, bottom: 0, width: 1080, height: 26, background: C.accent}} />
  </AbsoluteFill>
);

const Pastille: React.FC<{children: React.ReactNode; fond?: string; couleur?: string; taille?: number}> = ({
  children, fond = C.ink, couleur = C.white, taille = 34,
}) => (
  <span
    style={{
      display: 'inline-block', background: fond, color: couleur, fontFamily: FONT.mono, fontWeight: 500, fontSize: taille,
      letterSpacing: 2, textTransform: 'uppercase', padding: '10px 22px', borderRadius: 999,
    }}
  >
    {children}
  </span>
);

const Intro: React.FC<{u: Usage}> = ({u}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 12}});
  const sortie = interpolate(f, [INTRO - 12, INTRO], [1, 0], {extrapolateLeft: 'clamp'});
  const mascotte = spring({frame: f - 8, fps, config: {damping: 11, mass: 0.8}});
  return (
    <AbsoluteFill style={{opacity: sortie}}>
      <div style={{position: 'absolute', left: 70, top: 110, transform: `translateY(${(1 - s) * -60}px)`, opacity: s}}>
        <Pastille fond={C.accent}>Top 10 Geek</Pastille>
      </div>
      <div
        style={{
          position: 'absolute', left: 70, right: 70, top: 230, fontFamily: FONT.title, fontWeight: 800, fontSize: 118,
          lineHeight: 1.02, color: C.ink, letterSpacing: -2, transform: `translateY(${(1 - s) * 80}px)`, opacity: s,
        }}
      >
        {u.titre3}
      </div>
      <Img
        src={staticFile(`assets/img/${u.mascotte}.webp`)}
        style={{
          position: 'absolute', right: 40, bottom: 110, height: 1180, transform: `translateY(${(1 - mascotte) * 500}px) rotate(${(1 - mascotte) * 6}deg)`,
        }}
      />
      <Img
        src={staticFile(u.badge)}
        style={{position: 'absolute', left: 70, bottom: 330, width: 340, transform: `rotate(-8deg) scale(${mascotte})`}}
      />
      <div style={{position: 'absolute', left: 70, bottom: 150, width: 560, fontFamily: FONT.body, fontWeight: 700, fontSize: 40, color: C.muted, lineHeight: 1.3}}>
        {BASELINE}
      </div>
    </AbsoluteFill>
  );
};

const Scene: React.FC<{p: Produit; u: Usage}> = ({p, u}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const entree = spring({frame: f, fps, config: {damping: 14}});
  const sortie = interpolate(f, [SCENE - 10, SCENE], [1, 0], {extrapolateLeft: 'clamp'});
  const compte = interpolate(f, [15, 60], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const note = p.note !== null ? p.note * compte : null;
  const seul = p.note !== null && p.nnotes < 3;
  const fade = (d: number) => interpolate(f, [d, d + 14], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{opacity: sortie}}>
      <div style={{position: 'absolute', left: 70, top: 100, display: 'flex', alignItems: 'baseline', gap: 20, opacity: entree}}>
        <span style={{fontFamily: FONT.title, fontWeight: 800, fontSize: 190, color: u.couleur, lineHeight: 0.9, letterSpacing: -6}}>#{p.rang}</span>
        <span style={{fontFamily: FONT.mono, fontWeight: 500, fontSize: 34, color: C.muted, textTransform: 'uppercase', letterSpacing: 2}}>
          du top 10<br />{u.label}
        </span>
      </div>
      <div style={{position: 'absolute', right: 70, top: 130, opacity: entree}}>
        <Pastille fond={p.rang === 1 ? C.accent : C.ink} taille={28}>{p.badge}</Pastille>
      </div>

      <div
        style={{
          position: 'absolute', left: 70, top: 340, width: 940, height: 640, background: C.white, border: `4px solid ${C.line}`,
          boxShadow: `14px 14px 0 ${C.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center',
          transform: `translateX(${(1 - entree) * 700}px) rotate(${(1 - entree) * 4}deg)`,
        }}
      >
        {p.img ? (
          <Img src={staticFile(p.img)} style={{width: 880, height: 580, objectFit: 'contain'}} />
        ) : (
          <div style={{textAlign: 'center', fontFamily: FONT.mono, color: C.faint, fontSize: 32}}>
            <Img src={staticFile(`assets/img/${u.mascotte}.webp`)} style={{height: 420, opacity: 0.5}} />
            <div>photo à venir</div>
          </div>
        )}
      </div>

      <div style={{position: 'absolute', left: 70, right: 70, top: 1025, display: 'flex', flexDirection: 'column', gap: 26}}>
        <div style={{opacity: fade(10)}}>
          <div style={{fontFamily: FONT.title, fontWeight: 800, fontSize: 76, lineHeight: 1.04, color: C.ink, letterSpacing: -1.5}}>{p.nom}</div>
          <div style={{fontFamily: FONT.mono, fontWeight: 500, fontSize: 26, color: C.muted, marginTop: 8}}>{p.ref}</div>
        </div>
        <div style={{display: 'flex', alignItems: 'center', gap: 28, opacity: fade(20)}}>
          {note !== null ? (
            <>
              <div style={{background: C.ink, color: C.white, borderRadius: 24, padding: '10px 32px', fontFamily: FONT.title, fontWeight: 800, fontSize: 110, lineHeight: 1}}>
                {virgule(note)}<span style={{fontSize: 48, color: C.faint}}>/10</span>
              </div>
              <div style={{fontFamily: FONT.body, fontWeight: 700, fontSize: 36, color: C.ink, lineHeight: 1.25}}>
                note presse<br />
                <span style={{color: C.muted, fontWeight: 600}}>{p.nnotes} note{p.nnotes > 1 ? 's' : ''} · {p.ntests} test{p.ntests > 1 ? 's' : ''}</span>
              </div>
            </>
          ) : (
            <div style={{fontFamily: FONT.body, fontWeight: 700, fontSize: 44, color: C.muted}}>
              Testé par la presse, sans note publique ({p.ntests} test{p.ntests > 1 ? 's' : ''})
            </div>
          )}
        </div>
        {seul && (
          <div style={{opacity: fade(28)}}>
            <Pastille fond={C.highlight} couleur={C.ink} taille={28}>{p.nnotes === 1 ? '1 seul test noté' : `${p.nnotes} tests notés seulement`}</Pastille>
          </div>
        )}
        <div style={{opacity: fade(40), fontFamily: FONT.body, fontWeight: 600, fontSize: 40, color: C.ink, lineHeight: 1.3, maxWidth: 640}}>
          <span style={{color: u.couleur, fontWeight: 700}}>+ </span>{p.fort}
        </div>
      </div>

      <Img
        src={staticFile(`assets/img/${u.mascotte}.webp`)}
        style={{position: 'absolute', right: 24, bottom: 175, height: 420, opacity: fade(25), filter: 'drop-shadow(0 0 1.5px #fff) drop-shadow(0 0 1.5px #fff) drop-shadow(0 6px 14px rgba(0,0,0,.35))'}}
      />

      <div style={{position: 'absolute', left: 70, bottom: 110, opacity: fade(55)}}>
        <span style={{fontFamily: FONT.title, fontWeight: 800, fontSize: 64, color: C.accent}}>env. {p.prix}</span>
        <span style={{fontFamily: FONT.mono, fontWeight: 500, fontSize: 26, color: C.muted, marginLeft: 18}}>prix indicatif · {u.prixDate}</span>
      </div>
    </AbsoluteFill>
  );
};

const Outro: React.FC<{u: Usage}> = ({u}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 13}});
  return (
    <AbsoluteFill>
      <Img src={staticFile(`assets/img/${u.mascotte}.webp`)} style={{position: 'absolute', left: 80, bottom: 150, height: 760, transform: `scale(${s})`, transformOrigin: 'bottom'}} />
      <div style={{position: 'absolute', left: 70, right: 70, top: 190, opacity: s, transform: `translateY(${(1 - s) * 60}px)`}}>
        <Pastille fond={C.accent}>Les 10 en détail</Pastille>
        <div style={{fontFamily: FONT.title, fontWeight: 800, fontSize: 108, lineHeight: 1.03, color: C.ink, marginTop: 36, letterSpacing: -2}}>
          Tous les tests,<br />résumés<br />pour vous.
        </div>
        <div style={{fontFamily: FONT.mono, fontWeight: 500, fontSize: 40, color: u.couleur, marginTop: 40, textTransform: 'none'}}>
          top10geek.fr/{u.famille}/{u.slug}
        </div>
      </div>
      <div style={{position: 'absolute', left: 70, right: 70, bottom: 70, fontFamily: FONT.body, fontWeight: 600, fontSize: 24, color: C.muted}}>
        Notes presse sur 10 : moyenne des tests de la presse, sources sur le site. Prix indicatifs, {u.prixDate}.
      </div>
    </AbsoluteFill>
  );
};

export const TopUsage: React.FC<{usage: Usage}> = ({usage}) => {
  attendreLesPolices();
  const [p1, p2, p3] = usage.top;
  return (
    <AbsoluteFill>
      <Fond couleur={usage.couleur} />
      <Sequence from={0} durationInFrames={INTRO}><Intro u={usage} /></Sequence>
      <Sequence from={INTRO} durationInFrames={SCENE}><Scene p={p3} u={usage} /></Sequence>
      <Sequence from={INTRO + SCENE} durationInFrames={SCENE}><Scene p={p2} u={usage} /></Sequence>
      <Sequence from={INTRO + 2 * SCENE} durationInFrames={SCENE}><Scene p={p1} u={usage} /></Sequence>
      <Sequence from={INTRO + 3 * SCENE} durationInFrames={OUTRO}><Outro u={usage} /></Sequence>
    </AbsoluteFill>
  );
};
