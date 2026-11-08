import sys, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W = sys.argv[1]; OUT = os.path.join(W, "final"); SRC = os.path.join(W, "out")
STAGE = (38, 34, 31)          # graphite warmed by Blender orange
ORANGE = (232, 125, 13)
F = lambda n, s: ImageFont.truetype(os.path.join(r"C:\Windows\Fonts", n), s)

def rounded(im, r):
    m = Image.new("L", (im.width * 4, im.height * 4), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, m.width - 1, m.height - 1), r * 4, fill=255)
    return m.resize(im.size, Image.LANCZOS)

def place(canvas, im, x, y, r=14):
    mask = rounded(im, r)
    sh = Image.new("L", (canvas.width, canvas.height), 0)
    sh.paste(mask.point(lambda v: v * 0.55), (x, y + 18))
    sh = sh.filter(ImageFilter.GaussianBlur(28))
    canvas.paste(Image.new("RGB", canvas.size, (8, 7, 6)), (0, 0), sh)
    canvas.paste(im, (x, y), mask)
    # hairline edge
    edge = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(edge).rounded_rectangle((x, y, x + im.width - 1, y + im.height - 1), r, outline=(255, 255, 255, 34), width=1)
    canvas.paste(edge, (0, 0), edge)

def stage():
    return Image.new("RGB", (1920, 1080), STAGE)

# gallery: full windows 1:1, close-up 1:1
for name, src in [("02_edit_then_reload", "b_hover.png"), ("03_reloaded", "c_after.png")]:
    c = stage(); place(c, Image.open(os.path.join(SRC, src)).convert("RGB"), 160, 80); c.save(os.path.join(OUT, name + ".png"))
crop = Image.open(os.path.join(SRC, "d_picker_crop.png")).convert("RGB")
c = stage(); place(c, crop, 320, 170); c.save(os.path.join(OUT, "01_pick_from_top_bar.png"))

# featured: name + one line left, close-up right
c = stage()
place(c, crop.resize((1120, 630), Image.LANCZOS), 720, 225)
d = ImageDraw.Draw(c)
d.text((110, 380), "Addon Dev", font=F("segoeuib.ttf", 92), fill=(242, 238, 233))
d.text((110, 480), "Reloader", font=F("segoeuib.ttf", 92), fill=ORANGE)
d.text((114, 620), "Edit your add-on, click reload.\nNo restart.", font=F("segoeui.ttf", 40), fill=(190, 183, 175), spacing=14)
c.save(os.path.join(OUT, "featured.png"))

# icon 256: rounded tile, orange reload arc around a plug-in block
S = 1024
ic = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(ic)
d.rounded_rectangle((0, 0, S - 1, S - 1), 220, fill=(43, 40, 37, 255))
cx = cy = S // 2; R = 330; w = 78
d.arc((cx - R, cy - R, cx + R, cy + R), 312, 232, fill=ORANGE + (255,), width=w)
import math
a = math.radians(228); ex, ey = cx + R * math.cos(a), cy + R * math.sin(a)
# arrowhead at the arc end, pointing clockwise
tx, ty = -math.sin(a), math.cos(a)        # tangent (clockwise in screen coords)
nx, ny = math.cos(a), math.sin(a)
hw, hl = 120, 130
pts = [(ex + nx * hw, ey + ny * hw), (ex - nx * hw, ey - ny * hw), (ex + tx * hl, ey + ty * hl)]
d.polygon(pts, fill=ORANGE + (255,))
# the add-on: a block with a plug tab, in light grey
g = (226, 220, 212, 255)
b = 128
d.rounded_rectangle((cx - b, cy - b + 30, cx + b, cy + b + 30), 36, fill=g)
d.rounded_rectangle((cx - 70, cy - b - 40, cx - 26, cy - b + 40), 14, fill=g)
d.rounded_rectangle((cx + 26, cy - b - 40, cx + 70, cy - b + 40), 14, fill=g)
ic.resize((256, 256), Image.LANCZOS).save(os.path.join(OUT, "icon.png"))
ic.resize((64, 64), Image.LANCZOS).save(os.path.join(W, "out", "icon_64_check.png"))
print("done")
