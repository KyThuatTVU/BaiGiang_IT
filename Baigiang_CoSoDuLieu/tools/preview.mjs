// Render still frames of selected scenes with synthetic cue timing (visual QA, no audio).
import { chromium } from 'playwright-core';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { startServer } from './server.mjs';

const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const script = JSON.parse(readFileSync('build/script.json', 'utf8'));

// synthetic timeline: every cue ~5.2s so layouts are fully populated
let t = 0;
const scenes = script.scenes.map((sc) => {
  const start = t;
  const cues = sc.cues.map((c, i) => ({
    ...c, start: start + 0.8 + i * 5.2, end: start + 0.8 + i * 5.2 + 4.9, dur: 4.9
  }));
  const dur = 0.8 + sc.cues.length * 5.2 + 1.0;
  t = start + dur;
  return { id: sc.id, type: sc.type, part: sc.part, title: sc.title, start: +start.toFixed(2), dur: +dur.toFixed(2), lead: 0.8, cues };
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
  const at = s.start + s.dur - 0.9;
  await page.evaluate((x) => window.renderFrame(x), at);
  await page.waitForTimeout(90);
  const file = `build/previews/${s.id}.png`;
  await page.screenshot({ path: file, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
  console.log('shot', file);
}
await browser.close();
server.close();
