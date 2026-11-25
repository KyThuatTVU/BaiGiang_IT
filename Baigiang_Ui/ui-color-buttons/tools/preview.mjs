// Render still frames of selected scenes with synthetic cue timing (visual QA, no audio).
import { chromium } from 'playwright-core';
import { mkdirSync, readFileSync } from 'node:fs';
import { startServer } from './server.mjs';

const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const script = JSON.parse(readFileSync('build/script.json', 'utf8'));

// synthetic timeline: 5.2 s per cue (quiz questions hold 3.4 s) so layouts are fully populated
let t = 0;
const scenes = script.scenes.map((sc) => {
  const start = t;
  let cursor = 0.7;
  const cues = sc.cues.map((c) => {
    const dur = 4.9 + (c.hold || 0);
    const cue = { id: c.id, say: c.say, start: start + cursor, end: start + cursor + 4.9, dur: 4.9 };
    cursor += dur + 0.3;
    return cue;
  });
  const dur = cursor + 0.8;
  t = start + dur;
  return { id: sc.id, type: sc.type, part: sc.part, title: sc.title, start: +start.toFixed(2), dur: +dur.toFixed(2), lead: 0.7, cues };
});
const timeline = { fps: 25, width: 1920, height: 1080, duration: t, scenes, captions: [], sfx: [] };

const want = process.argv.slice(2);
const ids = want.length ? want : scenes.map((s) => s.id);
mkdirSync('build/previews', { recursive: true });

const { server, url } = await startServer(process.cwd());
const browser = await chromium.launch({ executablePath: EDGE, headless: true });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
await page.route('**/timeline.js', (route) =>
  route.fulfill({ contentType: 'application/javascript', body: 'window.__TIMELINE=' + JSON.stringify(timeline) + ';' }));
page.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') console.log('[page]', m.text()); });
page.on('pageerror', (e) => console.log('[pageerror]', e.message));
await page.goto(url + '/src/index.html', { waitUntil: 'networkidle' });
await page.waitForFunction(() => window.__ready === true);
await page.evaluate(() => document.fonts.ready);

for (const s of scenes) {
  if (!ids.includes(s.id)) continue;
  const shots = process.env.PREVIEW_FULL ? [0.92, 0.55] : [0.92];
  for (const frac of shots) {
    const at = s.start + s.dur * frac;
    await page.evaluate((x) => window.renderFrame(x), at);
    await page.waitForTimeout(120);
    const suffix = frac === 0.92 ? '' : '-mid';
    const file = `build/previews/${s.id}${suffix}.png`;
    await page.screenshot({ path: file, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
    console.log('shot', file);
  }
}
await browser.close();
server.close();
