import React from 'react';
import {Composition, Still} from 'remotion';
import data from './data.generated.json';
import {DUREE_TOP3, FPS, TopUsage} from './TopUsage';
import {OgImage} from './OgImage';
import {DUREE_LONG, FPS_LONG, Top10Long} from './Top10Long';
import type {Usage} from './theme';

const usages = data.usages as unknown as Usage[];

export const Root: React.FC = () => (
  <>
    <Composition
      id="TopUsage"
      component={TopUsage}
      durationInFrames={DUREE_TOP3}
      fps={FPS}
      width={1080}
      height={1920}
      defaultProps={{usage: usages.find((u) => u.cle === 'e-gaming') ?? usages[0]}}
    />
    <Composition
      id="Top10Long"
      component={Top10Long}
      durationInFrames={DUREE_LONG}
      fps={FPS_LONG}
      width={1920}
      height={1080}
      defaultProps={{usage: usages.find((u) => u.cle === 'e-gaming') ?? usages[0]}}
    />
    <Still
      id="Og"
      component={OgImage}
      width={1200}
      height={630}
      defaultProps={{
        mode: 'usage' as const,
        usage: usages.find((u) => u.cle === 'e-gaming') ?? usages[0],
        titre: 'Les 10 meilleurs écrans gaming',
        soustitre: 'Notes de la presse résumées · prix indicatifs',
      }}
    />
  </>
);
