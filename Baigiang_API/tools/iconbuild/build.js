const sharp = require('sharp');
const fs = require('fs');
const OUT = 'D:/Edit/Kit/tools/icons';
const items = [['react', '#61DAFB'], ['node', '#5FA04E'], ['mysql', '#4479A1']];
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  for (const [name, color] of items) {
    const svg = fs.readFileSync(name + '.svg', 'utf8').replace('<svg ', '<svg fill="' + color + '" ');
    await sharp(Buffer.from(svg), { density: 600 }).resize(256, 256).png().toFile(OUT + '/' + name + '.png');
    console.log(name, 'ok');
  }
})();
