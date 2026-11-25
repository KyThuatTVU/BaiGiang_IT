// Render deterministic frames from the scene page and mux with the audio mix.
import { chromium } from 'playwright-core';
import { spawn } from 'node:child_process';
import { once } from 'node:events';
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { startServer } from './server.mjs';

const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const arg = (k, d) => {
  const i = process.argv.indexOf(k);
  return i > 0 ? process.argv[i + 1] : d;
};
const tl = JSON.parse(readFileSync('build/timeline.json', 'utf8'));
const fps = tl.fps || 25;
const from = parseFloat(arg('--from', '0'));
const to = Math.min(tl.duration, parseFloat(arg('--to', String(tl.duration))));
const out = arg('--out', 'build/video.mp4');
const audio = arg('--audio', 'build/audio/mix.wav');
const mute = process.argv.includes('--mute');
const total = Math.max(1, Math.round((to - from) * fps));
const FF = arg('--ffmpeg', createRequire(import.meta.url)('ffmpeg-static'));

console.log(`rendering ${from.toFixed(1)}s..${to.toFixed(1)}s | ${total} frames @ ${fps}fps -> ${out}`);

const ffArgs = ['-y', '-v', 'error',
  '-f', 'image2pipe', '-framerate', String(fps), '-i', '-'];
if (!mute) {
  if (from > 0) ffArgs.push('-ss', String(from));
  ffArgs.push('-t', String(to - from), '-i', audio);
}
ffArgs.push('-map', '0:v');
if (!mute) ffArgs.push('-map', '1:a');
ffArgs.push('-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
  '-profile:v', 'high');
if (!mute) ffArgs.push('-c:a', 'aac', '-b:a', '192k');
ffArgs.push('-movflags', '+faststart');
if (!mute) ffArgs.push('-shortest');
ffArgs.push(out);

const ff = spawn(FF, ffArgs, { stdio: ['pipe', 'inherit', 'inherit'] });
const ffDone = new Promise((res, rej) => ff.on('close', (c) => c === 0 ? res() : rej(new Error('ffmpeg exit ' + c))));

const { server, url } = await startServer(process.cwd());
const browser = await chromium.launch({ executablePath: EDGE, headless: true, args: ['--hide-scrollbars', '--force-device-scale-factor=1'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
page.on('pageerror', (e) => console.log('[pageerror]', e.message));
await page.goto(url + '/src/index.html', { waitUntil: 'networkidle' });
await page.waitForFunction(() => window.__ready === true);
await page.evaluate(() => document.fonts.ready);
await page.addStyleTag({ content: '*{transition:none!important;animation:none!important;caret-color:transparent!important}' });

await page.evaluate((t) => window.renderFrame(t), from);
await page.screenshot({ type: 'jpeg', quality: 60 });

const t0 = Date.now();
for (let i = 0; i < total; i++) {
  const t = from + i / fps;
  await page.evaluate((x) => window.renderFrame(x), t);
  const buf = await page.screenshot({ type: 'jpeg', quality: 90 });
  if (!ff.stdin.write(buf)) await once(ff.stdin, 'drain');
  if (i % 250 === 0 || i === total - 1) {
    const el = (Date.now() - t0) / 1000;
    const rate = (i + 1) / Math.max(el, 0.001);
    const eta = (total - i - 1) / Math.max(rate, 0.001);
    console.log(`frame ${i + 1}/${total} | ${rate.toFixed(1)} fps | eta ${(eta / 60).toFixed(1)} min`);
  }
}
ff.stdin.end();
await ffDone;
await browser.close();
server.close();
console.log('done', out);
