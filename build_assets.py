from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

SRC = r"C:\Users\leonildo.sousa\AppData\Local\Temp\redmine\dbonfim\DBonfim.jpg"
OUT = r"C:\Users\leonildo.sousa\AppData\Local\Temp\redmine\dbonfim"

RED = (216, 0, 24)          # vermelho da marca (uniformizado)
W = (255, 255, 255)
B = (15, 15, 15)

img = Image.open(SRC).convert("RGB")
w, h = img.size

# bbox do lockup (mesmo criterio de analyze.py)
px = img.load()
xs, ys = [], []
step = 2
for y in range(0, h, step):
    for x in range(0, w, step):
        r, g, b = px[x, y]
        white = r > 190 and g > 190 and b > 190
        dark  = r < 90 and g < 90 and b < 90
        if white or dark:
            xs.append(x); ys.append(y)

x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
pad = 24
x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
x1 = min(w, x1 + pad); y1 = min(h, y1 + pad)
crop = img.crop((x0, y0, x1, y1))
cw, ch = crop.size

# ---- reconstruir: fundo vermelho uniforme + marca com anti-aliasing preservado ----
lum = crop.convert("L")
lp = lum.load()
out = Image.new("RGB", (cw, ch), RED)
op = out.load()
for y in range(ch):
    for x in range(cw):
        L = lp[x, y]
        # branco: acima do vermelho (~76)
        aw = max(0.0, min(1.0, (L - 80) / (245 - 80)))
        # preto: abaixo do vermelho
        ad = max(0.0, min(1.0, (70 - L) / (70 - 25)))
        r = RED[0]; g = RED[1]; b = RED[2]
        if aw > 0:
            r = r + (W[0]-r)*aw; g = g + (W[1]-g)*aw; b = b + (W[2]-b)*aw
        if ad > 0:
            r = r + (B[0]-r)*ad; g = g + (B[1]-g)*ad; b = b + (B[2]-b)*ad
        op[x, y] = (int(r), int(g), int(b))

out.save(os.path.join(OUT, "logo-clean.jpg"), quality=92)
print("logo-clean:", out.size)

# versao maior para telas (1400px)
big = out.copy()
if big.width > 1400:
    ratio = 1400 / big.width
    big = big.resize((1400, int(big.height*ratio)), Image.LANCZOS)
big.save(os.path.join(OUT, "logo-clean-lg.jpg"), quality=90)
print("logo-clean-lg:", big.size)

# ---- FAVICON: quadrado vermelho arredondado com D branco italico ----
def make_fav(size, path):
    s = size * 4  # sup
    canvas = Image.new("RGBA", (s, s), (0,0,0,0))
    # fundo vermelho rounded
    rad = int(s * 0.22)
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle([0, 0, s-1, s-1], radius=rad, fill=RED+(255,))
    # D
    font_path = r"C:\Windows\Fonts\arialbd.ttf"
    fs = int(s * 0.62)
    font = ImageFont.truetype(font_path, fs)
    txt = "D"
    tb = d.textbbox((0,0), txt, font=font)
    tw, th = tb[2]-tb[0], tb[3]-tb[1]
    d.text(((s-tw)/2 - tb[0], (s-th)/2 - tb[1] - s*0.01), txt, font=font, fill=W+(255,))
    # italo (shear horizontal)
    shear = s * 0.18
    canvas = canvas.transform((s, s), Image.AFFINE,
        (1, 0, -shear/2, 0, 1, 0), resample=Image.BICUBIC)
    # recortar bordas cortadas pelo shear
    m = int(shear/2)
    canvas = canvas.crop((m, 0, s-m, s))
    canvas = canvas.resize((size, size), Image.LANCZOS)
    canvas.save(path)
    print("fav", size, os.path.basename(path))

make_fav(180, os.path.join(OUT, "apple-touch-icon.png"))
make_fav(64,  os.path.join(OUT, "icon-64.png"))
make_fav(32,  os.path.join(OUT, "icon-32.png"))
make_fav(16,  os.path.join(OUT, "icon-16.png"))
imgs = [Image.open(os.path.join(OUT, f"icon-{n}.png")) for n in (16,32,64)]
imgs[0].save(os.path.join(OUT, "favicon.ico"), sizes=[(16,16),(32,32),(48,48)])
print("favicon.ico ok")
