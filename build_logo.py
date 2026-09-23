from PIL import Image
import os

SRC = r"C:\Users\leonildo.sousa\AppData\Local\Temp\redmine\dbonfim\DBonfim.jpg"
OUT = r"C:\Users\leonildo.sousa\AppData\Local\Temp\redmine\dbonfim"

RED = (216, 0, 24)
W = (255, 255, 255)
B = (15, 15, 15)

img = Image.open(SRC).convert("RGB")
w, h = img.size
px = img.load()
lum = img.convert("L")
lp = lum.load()

# bbox do lockup
xs, ys = [], []
step = 2
for y in range(0, h, step):
    for x in range(0, w, step):
        r, g, b = px[x, y]
        red_like = r > g + 40 and r > b + 40
        if not red_like:
            L = lp[x, y]
            if L > 185 or L < 95:
                xs.append(x); ys.append(y)

x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
pad = 26
x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
x1 = min(w, x1 + pad); y1 = min(h, y1 + pad)
crop = img.crop((x0, y0, x1, y1))
cw, ch = crop.size
cp = crop.load()

out = Image.new("RGB", (cw, ch), RED)
op = out.load()
for y in range(ch):
    for x in range(cw):
        r, g, b = cp[x, y]
        L = (int(r)*299 + int(g)*587 + int(b)*114) // 1000
        red_like = r > g + 40 and r > b + 40
        out_r, out_g, out_b = RED
        if not red_like:
            aw = max(0.0, min(1.0, (L - 150) / (245 - 150)))   # branco
            ad = max(0.0, min(1.0, (110 - L) / (110 - 55)))    # preto
            if aw > 0:
                out_r += (W[0]-out_r)*aw; out_g += (W[1]-out_g)*aw; out_b += (W[2]-out_b)*aw
            if ad > 0:
                out_r += (B[0]-out_r)*ad; out_g += (B[1]-out_g)*ad; out_b += (B[2]-out_b)*ad
        op[x, y] = (int(out_r), int(out_g), int(out_b))

out.save(os.path.join(OUT, "logo-clean.jpg"), quality=93)
big = out.copy()
if big.width > 1400:
    ratio = 1400 / big.width
    big = big.resize((1400, int(big.height*ratio)), Image.LANCZOS)
big.save(os.path.join(OUT, "logo-clean-lg.jpg"), quality=91)
print("logo:", out.size, "-> lg:", big.size)
