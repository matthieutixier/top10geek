import {Config} from '@remotion/cli/config';

// Les images du site (assets/img/...) sont servies telles quelles : le « dossier public » est la racine du dépôt.
Config.setPublicDir('..');
Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
