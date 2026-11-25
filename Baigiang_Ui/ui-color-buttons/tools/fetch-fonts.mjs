// Download Vietnamese + Latin woff2 subsets for the two display fonts.
import { writeFileSync, mkdirSync } from 'node:fs';

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36';
const OUT = 'assets/fonts';
mkdirSync(OUT, { recursive: true });

const families = [
  { css: 'Quicksand:wght@400;500;600;700', slug: 'quicksand' },
  { css: 'Plus+Jakarta+Sans:wght@400;500;600;700;800', slug: 'plus-jakarta-sans' }
];

for (const fam of families) {
  const url = `https://fonts.googleapis.com/css2?family=${fam.css}&display=swap`;
  const css = await (await fetch(url, { headers: { 'User-Agent': UA } })).text();
  const blocks = css.split('/*').slice(1);
  for (const raw of blocks) {
    const subset = raw.slice(0, raw.indexOf('*/')).trim();
    if (!['vietnamese', 'latin'].includes(subset)) continue;
    const weight = (raw.match(/font-weight:\s*(\d+)/) || [])[1];
    const src = (raw.match(/url\((https:\/\/[^)]+)\)/) || [])[1];
    if (!weight || !src) continue;
    const file = `${fam.slug}-${subset}-${weight}.woff2`;
    const buf = Buffer.from(await (await fetch(src, { headers: { 'User-Agent': UA } })).arrayBuffer());
    writeFileSync(`${OUT}/${file}`, buf);
    console.log(file, buf.length);
  }
}
