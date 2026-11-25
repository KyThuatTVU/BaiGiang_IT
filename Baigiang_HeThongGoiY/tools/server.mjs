// Static server for the scene page (root = project dir).
import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';

const MIME = {
  '.html': 'text/html; charset=utf-8', '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8', '.woff2': 'font/woff2', '.png': 'image/png',
  '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.json': 'application/json; charset=utf-8',
  '.wav': 'audio/wav', '.mp3': 'audio/mpeg'
};

export function startServer(root, port = 0) {
  const server = createServer(async (req, res) => {
    try {
      let p = decodeURIComponent(new URL(req.url, 'http://x').pathname);
      if (p === '/') p = '/src/index.html';
      const file = normalize(join(root, p));
      if (!file.startsWith(normalize(root))) { res.writeHead(403); return res.end(); }
      const st = await stat(file);
      if (!st.isFile()) { res.writeHead(404); return res.end(); }
      const buf = await readFile(file);
      res.writeHead(200, { 'content-type': MIME[extname(file)] || 'application/octet-stream', 'cache-control': 'no-store' });
      res.end(buf);
    } catch {
      res.writeHead(404); res.end();
    }
  });
  return new Promise((resolve) => {
    server.listen(port, '127.0.0.1', () => resolve({ server, url: `http://127.0.0.1:${server.address().port}` }));
  });
}
