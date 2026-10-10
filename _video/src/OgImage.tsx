import React from 'react';
import {AbsoluteFill, Img, staticFile} from 'remotion';
import {C, FONT, Usage, attendreLesPolices} from './theme';

export type OgProps = {
  mode: 'famille' | 'usage';
  usage: Usage;           // pour une famille : n'importe quel usage de la famille
  titre: string;
  soustitre: string;
};

export const OgImage: React.FC<OgProps> = ({mode, usage, titre, soustitre}) => {
  attendreLesPolices();
  return (
    <AbsoluteFill style={{background: '#33351f'}}>
      <Img src={staticFile('assets/img/og-image.jpg')} style={{position: 'absolute', inset: 0, width: 1200, height: 630, objectFit: 'cover'}} />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, #14151aF2 0%, #14151aE0 48%, #14151a00 78%)'}} />
      <div style={{position: 'absolute', left: 0, bottom: 0, width: 1200, height: 14, background: C.accent}} />
      <div style={{position: 'absolute', left: 0, top: 0, width: 14, height: 630, background: mode === 'usage' ? usage.couleur : C.accent}} />
      <div style={{position: 'absolute', left: 64, top: 52}}>
        <span style={{background: C.accent, color: '#fff', fontFamily: FONT.mono, fontWeight: 500, fontSize: 22, letterSpacing: 2, textTransform: 'uppercase', padding: '8px 18px', borderRadius: 999}}>
          Top 10 Geek
        </span>
        {mode === 'usage' && (
          <span style={{marginLeft: 14, background: usage.couleur, color: '#fff', fontFamily: FONT.mono, fontWeight: 500, fontSize: 22, letterSpacing: 2, textTransform: 'uppercase', padding: '8px 18px', borderRadius: 999}}>
            {usage.label}
          </span>
        )}
      </div>
      <div style={{position: 'absolute', left: 64, top: 140, width: 640, fontFamily: FONT.title, fontWeight: 800, fontSize: mode === 'usage' ? 68 : 76, lineHeight: 1.04, color: '#fff', letterSpacing: -1.5}}>
        {titre}
      </div>
      <div style={{position: 'absolute', left: 64, bottom: 76, width: 640, fontFamily: FONT.body, fontWeight: 700, fontSize: 28, color: C.highlight, lineHeight: 1.3}}>
        {soustitre}
      </div>
      <Img src={staticFile(`assets/img/${usage.mascotte}.webp`)} style={{position: 'absolute', right: 40, bottom: 14, height: 520, filter: 'drop-shadow(0 0 1.5px #fff) drop-shadow(0 0 1.5px #fff) drop-shadow(0 6px 18px rgba(0,0,0,.55))'}} />
      {mode === 'usage' && (
        <Img src={staticFile(usage.badge)} style={{position: 'absolute', right: 300, top: 40, width: 150, transform: 'rotate(-10deg)'}} />
      )}
    </AbsoluteFill>
  );
};
