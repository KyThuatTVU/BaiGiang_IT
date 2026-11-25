import { writeFileSync, mkdirSync } from 'node:fs';
import { scenes } from '../src/data/script.mjs';
mkdirSync('build', { recursive: true });
writeFileSync('build/script.json', JSON.stringify({ scenes }, null, 2));
console.log('scenes', scenes.length, 'cues', scenes.reduce((a, s) => a + s.cues.length, 0));
