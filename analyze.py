from PIL import Image, ImageOps
import os, json

SRC = r"C:\Users\leonildo.sousa\AppData\Local\Temp\redmine\dbonfim\DBonfim.jpg"
OUT = r"C:\Users\leonildo.sousa\AppData\Local\Temp\redmine\dbonfim"

img = Image.open(SRC).convert("RGB")
w, h = img.size
px = img.load()

# mapa: pixels "nao vermelhos" (branco/preto) = marca
def is_mark(r, g, b):
    # vermelho: r alto, g/b baixos
    if r > 140 and g < 110 and b < 110:
        return False
    return (r + g + b) < 600  # excluir claro demais? nao - branco tb marca

# melhor: marca = pixels BRANCOS ou PRETOS (baixa saturacao de vermelho)
def is_white(r, g, b):
    return r > 190 and g > 190 and b > 190
def is_dark(r, g, b):
    return r < 90 and g < 90 and b < 90

xs, ys = [], []
step = 2
for y in range(0, h, step):
    for x in range(0, w, step):
        r, g, b = px[x, y]
        if is_white(r, g, b) or is_dark(r, g, b):
            xs.append(x); ys.append(y)

x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
pad = 30
x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
x1 = min(w, x1 + pad); y1 = min(h, y1 + pad)
print("lockup bbox:", (x0, y0, x1, y1), "size:", (x1-x0, y1-y0))

# salvar preview do crop para eu conferir
crop = img.crop((x0, y0, x1, y1))
crop.thumbnail((1200, 800))
crop.save(os.path.join(OUT, "preview_lockup.jpg"), quality=88)

# amostrar cores do fundo vermelho (canto)
corners = [px[20,20], px[w-20,20], px[20,h-20], px[w-20,h-20], px[w//2, 15]]
print("fundo (cantos/topo):", corners)

# amostrar cores da marca
print("centro (texto?):", px[x0+ (x1-x0)//3, y0+(y1-y0)//3])
