import os, re, subprocess, sys
from PIL import Image

ROOT = "D:/Edit/Baigiang_Apriori"
ICONS = ROOT + "/assets/icons"
HTML = ROOT + "/assets/icons_html"
BLACK = ROOT + "/assets/icons_black"
EDGE = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
os.makedirs(HTML, exist_ok=True)
os.makedirs(BLACK, exist_ok=True)

names = sorted(f[:-4] for f in os.listdir(ICONS) if f.endswith(".svg"))

def render_all():
    for n in names:
        out = f"{BLACK}/{n}.png"
        if os.path.exists(out):
            continue
        svg = open(f"{ICONS}/{n}.svg", encoding="utf-8").read()
        svg = svg.replace('width="24"', 'width="140"').replace('height="24"', 'height="140"')
        svg = re.sub(r'stroke-width="2"', 'stroke-width="1.6"', svg)
        html = ('<!doctype html><html><head><style>html,body{margin:0;padding:0;width:200px;height:200px;'
                'background:#ffffff;display:flex;align-items:center;justify-content:center}svg{color:#000000}'
                '</style></head><body>' + svg + '</body></html>')
        hp = f"{HTML}/{n}.html"
        open(hp, "w", encoding="utf-8").write(html)
        subprocess.run([EDGE, "--headless", "--disable-gpu", "--hide-scrollbars",
                        "--allow-file-access-from-files", "--window-size=200,200",
                        f"--screenshot={out}", "file:///" + hp], capture_output=True)
        print("rendered", n, flush=True)

# recolor cache helper used by renderer
def icon_rgba(name, hexcolor):
    hexcolor = hexcolor.lstrip("#")
    cache = f"{ROOT}/assets/icons_png/{name}_{hexcolor}.png"
    if os.path.exists(cache):
        return Image.open(cache).convert("RGBA")
    g = Image.open(f"{BLACK}/{name}.png").convert("L")
    mask = g.point(lambda v: 255 - v)
    r, gg, b = int(hexcolor[0:2], 16), int(hexcolor[2:4], 16), int(hexcolor[4:6], 16)
    col = Image.new("RGBA", g.size, (r, gg, b, 255))
    col.putalpha(mask)
    col.save(cache)
    return col

if __name__ == "__main__":
    render_all()
    print("ICONS_DONE", len(names))