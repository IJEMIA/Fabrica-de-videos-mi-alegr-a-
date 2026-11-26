# -*- coding: utf-8 -*-
"""Ayudas compartidas: colores, fuentes, easing, texto, manchas."""
import math, os
from PIL import Image, ImageDraw, ImageFont

W, H = 720, 1280
FPS = 15

def _ruta_fuente(nombre):
    base = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts")
    p = os.path.join(base, nombre)
    return p if os.path.exists(p) else None

def font_hand(size):
    """Letra manuscrita (Patrick Hand) del repo, con respaldo DejaVu."""
    p = _ruta_fuente("PatrickHand-Regular.ttf")
    if p:
        return ImageFont.truetype(p, size)
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)

def font_bold(size):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)

def font(size):
    """Fuente negrita genérica (compatibilidad con el código pixel art)."""
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


WHITE = (255, 255, 255)


BLACK = (17, 17, 17)


MINT = (205, 238, 219)


MINT2 = (185, 228, 204)


SKIN = (246, 200, 159)


SKIN_D = (232, 168, 120)


HAIR = (107, 66, 38)


PURPLE = (126, 87, 194)


PURPLE_D = (106, 69, 176)


BLUE = (47, 109, 179)


BLUE_D = (36, 90, 148)


BROWN = (122, 74, 33)


GREEN = (46, 158, 91)


GREEN_D = (31, 122, 66)


YELLOW = (255, 210, 63)


YELLOW_L = (255, 224, 130)


RED = (228, 87, 46)


GRAY = (90, 90, 90)


GRAY_D = (60, 60, 60)


POLE = (70, 70, 78)


ORANGE = (240, 130, 50)


COURT_G = (178, 222, 178)


JUP_CREAM = (232, 205, 165)


JUP_TAN = (205, 165, 120)


JUP_BROWN = (170, 120, 80)


JUP_WHITE = (240, 228, 205)


JUP_ORANGE = (214, 140, 90)


SPOT_RED = (200, 80, 50)


ICE = (225, 238, 245)


ICE_LINE = (190, 90, 70)


OCEAN = (70, 140, 200)


OCEAN_D = (40, 100, 170)


CLOUD = (245, 245, 245)


RED_D = (190, 60, 40)


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def pop(t0, t, dur=0.35):
    """Factor de escala 0.7->1 con rebote suave al aparecer en t0."""
    p = (t - t0) / dur
    if p <= 0:
        return 0.0
    if p >= 1:
        return 1.0
    return ease_out(p)


def blink(t):
    return (t % 3.7) < 0.12


def draw_blob(d, cx, cy, rx, ry, color, seed=0):
    """Mancha grande irregular: varias elipses superpuestas."""
    for dx, dy, sx, sy in [(0, 0, 1.0, 1.0), (-0.55, 0.18, 0.72, 0.78),
                           (0.55, -0.12, 0.7, 0.82), (-0.2, -0.55, 0.66, 0.6),
                           (0.25, 0.55, 0.62, 0.55), (0.75, 0.35, 0.5, 0.5),
                           (-0.8, -0.3, 0.45, 0.55)]:
        d.ellipse([cx + dx * rx - sx * rx, cy + dy * ry - sy * ry,
                   cx + dx * rx + sx * rx, cy + dy * ry + sy * ry], fill=color)


def wrap_title(d, text, size, max_w):
    f = font_hand(size)
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines, f


def draw_title(d, text, y_top=110, size=102, max_w=640, color=None):
    lines, f = wrap_title(d, text, size, max_w)
    lh = int(size * 1.02)
    y = y_top
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.text(((W - w) / 2, y), ln, font=f, fill=color or BLACK)
        y += lh
    return y


def ease_out_back(t):
    t = max(0.0, min(1.0, t))
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def clamp(v, a, b):
    return max(a, min(b, v))


def norm_rows(rows):
    w = max(len(r) for r in rows)
    return [r.ljust(w, '.')[:w] for r in rows]


def draw_map(base, rows, palette, x, y, scale):
    """Dibuja un mapa de píxeles ('.' = transparente) sobre base (RGBA)."""
    rows = norm_rows(rows)
    d = ImageDraw.Draw(base)
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == '.' or ch not in palette:
                continue
            d.rectangle([x + c * scale, y + r * scale,
                         x + (c + 1) * scale - 1, y + (r + 1) * scale - 1],
                        fill=palette[ch])
    return len(rows[0]), len(rows)


def wrap_text(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def pop_scale(ts):
    """Escala de aparición con rebote (0.5 s)."""
    return ease_out_back(ts / 0.5)
