import React from 'react';
import {AbsoluteFill, Audio, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {C, FONT, Produit, Usage, attendreLesPolices, virgule} from './theme';

// Vidéo longue « Top 10 » (1920×1080, 30 i/s) : intro, méthode, compte à rebours du n° 10 au n° 1, récapitulatif, fin.
// Mêmes données que le site et que les vidéos « Top 3 » (src/data.generated.json).
export const FPS_LONG = 30;
const INTRO = 150;
const METHODE = 210;
const RANG = 270; // n° 10 à n° 4
const PODIUM = 420; // n° 3 à n° 1
const RECAP = 300;
const FIN = 240;
export const DUREE_LONG = INTRO + METHODE + 7 * RANG + 3 * PODIUM + RECAP + FIN;

// Piste sous licence CC BY 4.0, plus longue que la vidéo (2 min 54). Volume réglé pour environ -16 LUFS.
const MUSIQUE = '_video/audio/newer-wave.mp3';
const VOLUME = 0.6;

const W = 1920;
const H = 1080;
const MARGE = 90;
const borne = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
// Charte : pas de vert en fond (règle des visuels du 29/10/2026), le vert de l'usage gaming devient violet.
const teinte = (u: Usage) => (u.couleur.toUpperCase() === '#1F9E6E' ? '#7C3AED' : u.couleur);
const pluriel = (n: number, mot: string) => `${n} ${mot}${n > 1 ? 's' : ''}`;

const Fond: React.FC<{u: Usage}> = ({u}) => (
  <AbsoluteFill style={{background: C.paper}}>
    <AbsoluteFill style={{background: teinte(u), opacity: 0.1}} />
    <AbsoluteFill style={{backgroundImage: `radial-gradient(${C.ink}12 2px, transparent 2px)`, backgroundSize: '30px 30px'}} />
    <div style={{position: 'absolute', left: 0, top: 0, width: 22, height: H, background: teinte(u)}} />
    <div style={{position: 'absolute', left: 22, top: 0, width: 8, height: H, background: C.ink}} />
  </AbsoluteFill>
);

const Pastille: React.FC<{children: React.ReactNode; fond?: string; couleur?: string; taille?: number}> = ({
  children, fond = C.ink, couleur = C.white, taille = 26,
}) => (
  <span
    style={{
      display: 'inline-block', background: fond, color: couleur, fontFamily: FONT.mono, fontWeight: 500, fontSize: taille,
      letterSpacing: 2, textTransform: 'uppercase', padding: '9px 20px', borderRadius: 999, whiteSpace: 'nowrap',
    }}
  >
    {children}
  </span>
);

/** Bandeau du haut, présent du début à la fin : marque, usage, adresse. */
const Bandeau: React.FC<{u: Usage}> = ({u}) => (
  <div style={{position: 'absolute', left: MARGE, right: MARGE, top: 44, display: 'flex', alignItems: 'center', justifyContent: 'space-between'}}>
    <Pastille fond={C.accent}>Top 10 Geek</Pastille>
    <span style={{fontFamily: FONT.mono, fontWeight: 500, fontSize: 24, letterSpacing: 2, textTransform: 'uppercase', color: C.muted}}>
      {u.familleLabel} · {u.label}
    </span>
    <span style={{fontFamily: FONT.mono, fontWeight: 500, fontSize: 26, color: C.ink}}>top10geek.fr</span>
  </div>
);

/** Rail du compte à rebours : dix cases, de 10 à 1 ; la case en cours est en couleur. */
const Rail: React.FC<{u: Usage; rang: number}> = ({u, rang}) => (
  <div style={{position: 'absolute', left: MARGE, right: MARGE, bottom: 46, display: 'flex', alignItems: 'center', gap: 14}}>
    <span style={{fontFamily: FONT.mono, fontWeight: 500, fontSize: 22, letterSpacing: 2, textTransform: 'uppercase', color: C.muted, marginRight: 10}}>
      Compte à rebours
    </span>
    {[10, 9, 8, 7, 6, 5, 4, 3, 2, 1].map((n) => {
      const actif = n === rang;
      const passe = n > rang;
      return (
        <div
          key={n}
          style={{
            flex: actif ? '0 0 150px' : 1, height: actif ? 58 : 44, borderRadius: 10, display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontFamily: FONT.title, fontWeight: 800, fontSize: actif ? 36 : 24,
            background: actif ? teinte(u) : passe ? C.ink : 'transparent', color: actif || passe ? C.white : C.faint,
            border: `3px solid ${actif ? teinte(u) : passe ? C.ink : C.faint}`,
          }}
        >
          {actif ? `n° ${n}` : n}
        </div>
      );
    })}
  </div>
);

const Intro: React.FC<{u: Usage}> = ({u}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 13}});
  const m = spring({frame: f - 10, fps, config: {damping: 11, mass: 0.8}});
  const sortie = interpolate(f, [INTRO - 12, INTRO], [1, 0], borne);
  const ligne = (d: number) => interpolate(f, [d, d + 16], [0, 1], borne);
  const tests = u.top.reduce((t, p) => t + p.ntests, 0);
  return (
    <AbsoluteFill style={{opacity: sortie}}>
      <div style={{position: 'absolute', left: MARGE, top: 190, width: 1080}}>
        <div style={{opacity: s, transform: `translateY(${(1 - s) * 50}px)`}}>
          <Pastille fond={C.ink} taille={28}>Le classement de la presse</Pastille>
        </div>
        <div
          style={{
            fontFamily: FONT.title, fontWeight: 800, fontSize: u.titre10.length > 44 ? 104 : 124, lineHeight: 1.0, letterSpacing: -3, color: C.ink,
            marginTop: 34, opacity: s, transform: `translateY(${(1 - s) * 70}px)`,
          }}
        >
          {u.titre10.replace(/ en 2026$/, '')}
        </div>
        <div style={{display: 'flex', gap: 18, marginTop: 44, opacity: ligne(26)}}>
          <Pastille fond={teinte(u)} taille={30}>{pluriel(tests, 'test')} de la presse</Pastille>
          <Pastille fond={C.white} couleur={C.ink} taille={30}>du n° 10 au n° 1</Pastille>
        </div>
        <div style={{fontFamily: FONT.body, fontWeight: 600, fontSize: 36, color: C.muted, marginTop: 34, opacity: ligne(40)}}>
          Tous les tests high-tech, résumés pour vous.
        </div>
      </div>
      <Img
        src={staticFile(`assets/img/${u.mascotte}.webp`)}
        style={{position: 'absolute', right: 70, bottom: 40, height: 860, transform: `translateY(${(1 - m) * 420}px) rotate(${(1 - m) * 5}deg)`}}
      />
      <Img src={staticFile(u.badge)} style={{position: 'absolute', right: 560, bottom: 110, width: 250, transform: `rotate(-8deg) scale(${m})`}} />
    </AbsoluteFill>
  );
};

const Methode: React.FC<{u: Usage}> = ({u}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const entree = interpolate(f, [0, 14], [0, 1], borne);
  const sortie = interpolate(f, [METHODE - 12, METHODE], [1, 0], borne);
  const tests = u.top.reduce((t, p) => t + p.ntests, 0);
  const notes = u.top.reduce((t, p) => t + p.nnotes, 0);
  const cartes = [
    {chiffre: String(tests), titre: 'tests de la presse recensés', texte: 'pour ces dix modèles. Nous ne testons rien nous-mêmes : nous lisons les tests publiés.'},
    {chiffre: String(notes), titre: 'notes publiées', texte: 'Ramenées sur 10 : la note presse est leur moyenne. Sous trois notes, nous le signalons à l’écran.'},
    {chiffre: '0', titre: 'marchand mis en avant', texte: `Les prix sont indicatifs, relevés en ${u.prixDate}. Le classement ne dépend pas des commissions.`},
  ];
  return (
    <AbsoluteFill style={{opacity: Math.min(entree, sortie)}}>
      <div style={{position: 'absolute', left: MARGE, top: 170, fontFamily: FONT.title, fontWeight: 800, fontSize: 92, letterSpacing: -2, color: C.ink}}>
        Comment on classe
      </div>
      <div style={{position: 'absolute', left: MARGE, right: MARGE, top: 340, display: 'flex', gap: 36}}>
        {cartes.map((c, i) => {
          const s = spring({frame: f - 14 - i * 12, fps, config: {damping: 14}});
          return (
            <div
              key={c.titre}
              style={{
                flex: 1, background: C.white, border: `4px solid ${C.line}`, boxShadow: `12px 12px 0 ${C.ink}`, padding: '38px 40px 44px',
                opacity: s, transform: `translateY(${(1 - s) * 80}px)`,
              }}
            >
              <div style={{fontFamily: FONT.title, fontWeight: 800, fontSize: 150, lineHeight: 0.95, letterSpacing: -4, color: i === 2 ? C.accent : teinte(u)}}>
                {c.chiffre}
              </div>
              <div style={{fontFamily: FONT.title, fontWeight: 800, fontSize: 44, lineHeight: 1.1, color: C.ink, marginTop: 14}}>{c.titre}</div>
              <div style={{fontFamily: FONT.body, fontWeight: 600, fontSize: 30, lineHeight: 1.4, color: C.muted, marginTop: 18}}>{c.texte}</div>
            </div>
          );
        })}
      </div>
      <div style={{position: 'absolute', left: MARGE, bottom: 70, fontFamily: FONT.mono, fontWeight: 500, fontSize: 26, color: C.muted}}>
        Sources et liens vers chaque test : top10geek.fr/{u.famille}/{u.slug}
      </div>
    </AbsoluteFill>
  );
};

const Rang: React.FC<{p: Produit; u: Usage; duree: number}> = ({p, u, duree}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const podium = p.rang <= 3;
  const entree = spring({frame: f, fps, config: {damping: 15}});
  const sortie = interpolate(f, [duree - 10, duree], [1, 0], borne);
  const fondu = (d: number) => interpolate(f, [d, d + 14], [0, 1], borne);
  const compte = interpolate(f, [18, 66], [0, 1], borne);
  const note = p.note !== null ? p.note * compte : null;
  const peu = p.note !== null && p.nnotes < 3;
  const forts = (p.forts && p.forts.length ? p.forts : [p.fort]).filter(Boolean).slice(0, podium ? 3 : 2);
  const faible = (p.faibles || [])[0];
  const hPhoto = podium ? 520 : 700;
  // Fiche chargée (nom sur deux lignes, textes longs, quatre lignes de points) : on resserre pour ne jamais toucher le rail.
  const dense = p.nom.length > 26 || forts.length + (faible ? 1 : 0) >= 4 || [...forts, faible || ''].some((t) => t.length > 44);
  const ecart = dense ? 20 : 30;
  const corps = dense ? 29 : 32;
  return (
    <AbsoluteFill style={{opacity: sortie}}>
      {/* Colonne de gauche : photo, puis verdict pour le podium */}
      <div
        style={{
          position: 'absolute', left: MARGE, top: 150, width: 820, height: hPhoto, background: C.white, border: `4px solid ${C.line}`,
          boxShadow: `14px 14px 0 ${p.rang === 1 ? C.accent : C.ink}`, display: 'flex', alignItems: 'center', justifyContent: 'center',
          transform: `translateX(${(1 - entree) * -500}px) rotate(${(1 - entree) * -3}deg)`, opacity: entree,
        }}
      >
        {p.img ? (
          <Img src={staticFile(p.img)} style={{width: 740, height: hPhoto - 70, objectFit: 'contain'}} />
        ) : (
          <div style={{textAlign: 'center', fontFamily: FONT.mono, color: C.faint, fontSize: 28}}>
            <Img src={staticFile(`assets/img/${u.mascotte}.webp`)} style={{height: hPhoto - 200, opacity: 0.5}} />
            <div>photo à venir</div>
          </div>
        )}
        <div style={{position: 'absolute', left: -18, top: -24, transform: 'rotate(-3deg)'}}>
          <Pastille fond={p.rang === 1 ? C.accent : C.ink} taille={26}>{p.badge}</Pastille>
        </div>
      </div>
      {podium && (
        <div
          style={{
            position: 'absolute', left: MARGE, top: 150 + hPhoto + 44, width: 820, opacity: fondu(70),
            borderLeft: `8px solid ${teinte(u)}`, padding: '4px 0 4px 28px',
          }}
        >
          <div style={{fontFamily: FONT.mono, fontWeight: 500, fontSize: 22, letterSpacing: 2, textTransform: 'uppercase', color: C.muted}}>En résumé</div>
          <div style={{fontFamily: FONT.body, fontWeight: 600, fontSize: 30, lineHeight: 1.38, color: C.ink, marginTop: 8}}>{p.verdict}</div>
        </div>
      )}

      {/* Colonne de droite : rang, nom, note, points forts, prix */}
      <div style={{position: 'absolute', left: 990, right: MARGE, top: 130, display: 'flex', flexDirection: 'column'}}>
        <div style={{display: 'flex', alignItems: 'flex-end', gap: 22, opacity: entree, transform: `translateY(${(1 - entree) * -40}px)`}}>
          <span style={{fontFamily: FONT.title, fontWeight: 800, fontSize: dense ? 132 : 170, lineHeight: 0.82, letterSpacing: -6, color: teinte(u)}}>n°&nbsp;{p.rang}</span>
          <span style={{fontFamily: FONT.mono, fontWeight: 500, fontSize: 24, letterSpacing: 2, textTransform: 'uppercase', color: C.muted, paddingBottom: 6}}>
            sur 10
          </span>
        </div>
        <div style={{marginTop: ecart, opacity: fondu(8)}}>
          <span
            style={{
              fontFamily: FONT.title, fontWeight: 800, fontSize: p.nom.length > 26 ? 60 : 74, lineHeight: 1.05, letterSpacing: -1.5, color: C.ink,
              background: p.rang === 1 ? `linear-gradient(transparent 62%, ${C.highlight} 62%)` : 'none',
            }}
          >
            {p.nom}
          </span>
          <div style={{fontFamily: FONT.mono, fontWeight: 500, fontSize: 26, color: C.muted, marginTop: 10, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{p.ref}</div>
        </div>

        <div style={{display: 'flex', alignItems: 'center', gap: 28, marginTop: ecart, opacity: fondu(18)}}>
          {note !== null ? (
            <>
              <div style={{background: C.ink, color: C.white, borderRadius: 22, padding: '8px 30px 12px', fontFamily: FONT.title, fontWeight: 800, fontSize: 112, lineHeight: 1}}>
                {virgule(note)}<span style={{fontSize: 44, color: C.faint}}>/10</span>
              </div>
              <div style={{flex: 1}}>
                <div style={{fontFamily: FONT.body, fontWeight: 700, fontSize: 32, color: C.ink}}>
                  Note presse <span style={{color: C.muted, fontWeight: 600}}>· {pluriel(p.nnotes, 'note')} · {pluriel(p.ntests, 'test')}</span>
                </div>
                <div style={{height: 22, marginTop: 14, background: C.white, border: `3px solid ${C.ink}`, borderRadius: 999, overflow: 'hidden'}}>
                  <div style={{height: '100%', width: `${(note / 10) * 100}%`, background: teinte(u)}} />
                </div>
                {peu && (
                  <div style={{marginTop: 14}}>
                    <Pastille fond={C.highlight} couleur={C.ink} taille={22}>{p.nnotes === 1 ? '1 seul test noté' : `${p.nnotes} tests notés seulement`}</Pastille>
                  </div>
                )}
              </div>
            </>
          ) : (
            <div style={{fontFamily: FONT.body, fontWeight: 700, fontSize: 38, color: C.muted}}>
              Testé par la presse, sans note publique ({pluriel(p.ntests, 'test')})
            </div>
          )}
        </div>

        <div style={{marginTop: ecart, display: 'flex', flexDirection: 'column', gap: dense ? 8 : 12}}>
          {forts.map((t, i) => (
            <div key={t} style={{display: 'flex', gap: 16, opacity: fondu(40 + i * 14), fontFamily: FONT.body, fontWeight: 600, fontSize: corps, lineHeight: 1.3, color: C.ink}}>
              <span style={{flex: '0 0 34px', height: 34, marginTop: 4, borderRadius: 8, background: teinte(u), color: C.white, fontFamily: FONT.title, fontWeight: 800, fontSize: 30, lineHeight: '32px', textAlign: 'center'}}>+</span>
              <span>{t}</span>
            </div>
          ))}
          {faible && (
            <div style={{display: 'flex', gap: 16, opacity: fondu(40 + forts.length * 14), fontFamily: FONT.body, fontWeight: 600, fontSize: corps, lineHeight: 1.3, color: C.muted}}>
              <span style={{flex: '0 0 34px', height: 34, marginTop: 4, borderRadius: 8, background: C.white, border: `3px solid ${C.muted}`, color: C.muted, fontFamily: FONT.title, fontWeight: 800, fontSize: 30, lineHeight: '26px', textAlign: 'center', boxSizing: 'border-box'}}>−</span>
              <span>{faible}</span>
            </div>
          )}
        </div>

        <div style={{marginTop: ecart, opacity: fondu(90)}}>
          <span style={{fontFamily: FONT.title, fontWeight: 800, fontSize: dense ? 54 : 62, color: C.accent}}>env. {p.prix}</span>
          <span style={{fontFamily: FONT.mono, fontWeight: 500, fontSize: 24, color: C.muted, marginLeft: 18}}>prix indicatif · {u.prixDate}</span>
        </div>
      </div>
      <Rail u={u} rang={p.rang} />
    </AbsoluteFill>
  );
};

const Recap: React.FC<{u: Usage}> = ({u}) => {
  const f = useCurrentFrame();
  const sortie = interpolate(f, [RECAP - 12, RECAP], [1, 0], borne);
  const ligne = (p: Produit) => {
    const a = interpolate(f, [10 + (p.rang - 1) * 7, 26 + (p.rang - 1) * 7], [0, 1], borne);
    return (
      <div key={p.id} style={{display: 'flex', alignItems: 'center', gap: 20, opacity: a, transform: `translateX(${(1 - a) * 40}px)`, height: 118, borderBottom: `3px solid ${C.ink}22`}}>
        <span style={{flex: '0 0 76px', fontFamily: FONT.title, fontWeight: 800, fontSize: 60, letterSpacing: -2, color: p.rang <= 3 ? teinte(u) : C.faint, textAlign: 'right'}}>{p.rang}</span>
        <div style={{flex: 1, minWidth: 0}}>
          <div style={{fontFamily: FONT.title, fontWeight: 800, fontSize: p.nom.length > 26 ? 32 : 38, lineHeight: 1.1, color: C.ink, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{p.nom}</div>
          <div style={{fontFamily: FONT.mono, fontWeight: 500, fontSize: 22, color: C.muted, marginTop: 4}}>env. {p.prix} · {pluriel(p.ntests, 'test')}</div>
        </div>
        <span style={{flex: '0 0 132px', textAlign: 'center', background: p.note !== null ? C.ink : 'transparent', color: p.note !== null ? C.white : C.muted, border: p.note !== null ? 'none' : `3px solid ${C.faint}`, borderRadius: 14, padding: '8px 0', fontFamily: FONT.title, fontWeight: 800, fontSize: p.note !== null ? 46 : 24, boxSizing: 'border-box'}}>
          {p.note !== null ? virgule(p.note) : 'sans note'}
        </span>
      </div>
    );
  };
  return (
    <AbsoluteFill style={{opacity: sortie}}>
      <div style={{position: 'absolute', left: MARGE, top: 130, fontFamily: FONT.title, fontWeight: 800, fontSize: 76, letterSpacing: -2, color: C.ink}}>
        Le classement complet
      </div>
      <div style={{position: 'absolute', left: MARGE, right: MARGE, top: 260, display: 'flex', gap: 70}}>
        <div style={{flex: 1}}>{u.top.slice(0, 5).map(ligne)}</div>
        <div style={{flex: 1}}>{u.top.slice(5, 10).map(ligne)}</div>
      </div>
      <div style={{position: 'absolute', left: MARGE, bottom: 56, fontFamily: FONT.mono, fontWeight: 500, fontSize: 24, color: C.muted}}>
        Note presse sur 10 : moyenne des notes publiées. Prix indicatifs, {u.prixDate}.
      </div>
    </AbsoluteFill>
  );
};

const Fin: React.FC<{u: Usage}> = ({u}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 13}});
  const m = spring({frame: f - 8, fps, config: {damping: 11, mass: 0.8}});
  const pouls = 1 + 0.03 * Math.sin((f / fps) * Math.PI * 2);
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: MARGE, top: 180, width: 1120, opacity: s, transform: `translateY(${(1 - s) * 60}px)`}}>
        <Pastille fond={C.ink} taille={28}>Pour aller plus loin</Pastille>
        <div style={{fontFamily: FONT.title, fontWeight: 800, fontSize: 112, lineHeight: 1.02, letterSpacing: -3, color: C.ink, marginTop: 30}}>
          Les tests, les sources<br />et les prix à jour
        </div>
        <div style={{display: 'inline-block', marginTop: 44, background: C.white, border: `4px solid ${C.line}`, boxShadow: `12px 12px 0 ${C.accent}`, padding: '20px 34px', fontFamily: FONT.mono, fontWeight: 500, whiteSpace: 'nowrap', fontSize: Math.min(46, Math.floor(1040 / (0.61 * `top10geek.fr/${u.famille}/${u.slug}`.length))), color: C.ink}}>
          top10geek.fr/{u.famille}/{u.slug}
        </div>
        <div style={{marginTop: 50, transform: `scale(${pouls})`, transformOrigin: 'left center'}}>
          <Pastille fond={C.accent} taille={34}>Lien dans la description ↓</Pastille>
        </div>
      </div>
      <Img
        src={staticFile(`assets/img/${u.mascotte}.webp`)}
        style={{position: 'absolute', right: 80, bottom: 40, height: 820, transform: `translateY(${(1 - m) * 400}px)`}}
      />
      <div style={{position: 'absolute', left: MARGE, bottom: 56, width: 1100, fontFamily: FONT.body, fontWeight: 600, fontSize: 24, lineHeight: 1.4, color: C.muted}}>
        Top 10 Geek est financé par l’affiliation ; le classement ne dépend pas des commissions. Prix indicatifs relevés en {u.prixDate}, susceptibles d’avoir changé.
      </div>
    </AbsoluteFill>
  );
};

export const Top10Long: React.FC<{usage: Usage}> = ({usage}) => {
  attendreLesPolices();
  const ordre = [...usage.top].sort((a, b) => b.rang - a.rang); // du n° 10 au n° 1
  let t = INTRO + METHODE;
  return (
    <AbsoluteFill>
      {/* Musique de fond (crédit obligatoire dans la description, voir audio/LISEZMOI.md) : entrée en 1 s, sortie en 3 s. */}
      <Audio
        src={staticFile(MUSIQUE)}
        startFrom={20}
        volume={(f) => VOLUME * Math.min(interpolate(f, [0, 30], [0, 1], borne), interpolate(f, [DUREE_LONG - 90, DUREE_LONG - 5], [1, 0], borne))}
      />
      <Fond u={usage} />
      <Bandeau u={usage} />
      <Sequence from={0} durationInFrames={INTRO}><Intro u={usage} /></Sequence>
      <Sequence from={INTRO} durationInFrames={METHODE}><Methode u={usage} /></Sequence>
      {ordre.map((p) => {
        const duree = p.rang <= 3 ? PODIUM : RANG;
        const debut = t;
        t += duree;
        return (
          <Sequence key={p.id} from={debut} durationInFrames={duree}><Rang p={p} u={usage} duree={duree} /></Sequence>
        );
      })}
      <Sequence from={DUREE_LONG - RECAP - FIN} durationInFrames={RECAP}><Recap u={usage} /></Sequence>
      <Sequence from={DUREE_LONG - FIN} durationInFrames={FIN}><Fin u={usage} /></Sequence>
    </AbsoluteFill>
  );
};
