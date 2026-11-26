# -*- coding: utf-8 -*-
"""Objetos pixel art: libreta, teléfono, calculadora, mapa, papel, llave."""
import math
from PIL import Image, ImageDraw, ImageFont
from .core import font, clamp

INK = (43, 43, 58)


def notebook_img(scale=6):
    wpx, hpx = 26 * scale, 30 * scale
    img = Image.new("RGBA", (wpx, hpx), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    S = scale
    # portada azul dos tonos
    d.rectangle([3 * S, 1 * S, 24 * S - 1, 28 * S - 1], fill=(45, 110, 210))
    d.rectangle([13 * S, 1 * S, 24 * S - 1, 28 * S - 1], fill=(30, 80, 180))
    d.rectangle([3 * S, 1 * S, 24 * S - 1, 28 * S - 1], outline=INK, width=max(1, S // 3))
    # espiral
    for y in range(4 * S, 27 * S, 4 * S):
        d.ellipse([0, y - S // 2, 3 * S - 1, y + S // 2], outline=(200, 200, 210), width=max(1, S // 4))
    # etiqueta blanca con líneas
    d.rectangle([7 * S, 5 * S, 20 * S - 1, 13 * S - 1], fill=(245, 245, 240))
    for yy in (7 * S, 9 * S, 11 * S):
        d.rectangle([8 * S, yy, 19 * S - 1, yy + max(1, S // 5)], fill=(120, 140, 200))
    return img


def phone_img(scale=6, notif=True):
    wpx, hpx = 18 * scale, 30 * scale
    img = Image.new("RGBA", (wpx, hpx), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    S = scale
    d.rounded_rectangle([1 * S, 1 * S, 17 * S - 1, 29 * S - 1], radius=2 * S, fill=(25, 25, 35))
    d.rectangle([3 * S, 3 * S, 15 * S - 1, 25 * S - 1], fill=(120, 200, 240))
    # rejilla de 9 apps
    app_cols = [(255, 107, 157), (74, 222, 128), (250, 204, 21),
                (45, 212, 191), (167, 139, 250), (251, 146, 60),
                (255, 255, 255), (255, 143, 171), (120, 200, 240)]
    k = 0
    for r in range(3):
        for c in range(3):
            x0 = (4 + c * 4) * S
            y0 = (5 + r * 4) * S
            d.rectangle([x0, y0, x0 + 3 * S - 1, y0 + 3 * S - 1], fill=app_cols[k])
            k += 1
    # botón home
    d.ellipse([8 * S, 26 * S, 10 * S - 1, 27 * S - 1], outline=(180, 180, 200), width=max(1, S // 4))
    if notif:
        d.ellipse([13 * S, 0, 17 * S - 1, 4 * S - 1], fill=(230, 40, 60))
        d.ellipse([14 * S, 1 * S, 16 * S - 1, 3 * S - 1], fill=(255, 255, 255))
    return img


def calculator_img(scale=6):
    wpx, hpx = 22 * scale, 28 * scale
    img = Image.new("RGBA", (wpx, hpx), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    S = scale
    d.rounded_rectangle([1 * S, 1 * S, 21 * S - 1, 27 * S - 1], radius=2 * S, fill=(90, 95, 110))
    d.rounded_rectangle([1 * S, 1 * S, 21 * S - 1, 27 * S - 1], radius=2 * S, outline=INK, width=max(1, S // 3))
    # pantalla con dígitos
    d.rectangle([3 * S, 3 * S, 19 * S - 1, 7 * S - 1], fill=(200, 230, 190))
    dd = ImageDraw.Draw(img)
    dd.text((4 * S, int(3.2 * S)), "123", font=font(int(3.4 * S)), fill=(40, 60, 40))
    # teclas
    cols = [(240, 240, 240), (200, 210, 230), (250, 204, 21), (230, 60, 60)]
    for r in range(4):
        for c in range(4):
            x0 = (3 + c * 4) * S
            y0 = (9 + r * 4) * S
            col = cols[3] if (r == 0 and c == 3) else (cols[2] if r == 3 and c == 3 else cols[r % 2])
            d.rectangle([x0, y0, x0 + 3 * S - 1, y0 + 3 * S - 1], fill=col)
    return img


def map_img(scale=6):
    wpx, hpx = 34 * scale, 24 * scale
    img = Image.new("RGBA", (wpx, hpx), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    S = scale
    d.rectangle([1 * S, 1 * S, 33 * S - 1, 23 * S - 1], fill=(245, 235, 200))
    d.rectangle([1 * S, 1 * S, 33 * S - 1, 23 * S - 1], outline=INK, width=max(1, S // 3))
    # manzanas moradas
    for (x0, y0, x1, y1) in [(4, 3, 9, 8), (22, 3, 28, 7), (24, 15, 30, 20), (4, 16, 10, 21)]:
        d.rectangle([x0 * S, y0 * S, x1 * S - 1, y1 * S - 1], fill=(167, 139, 250))
    # río azul
    for i, yy in enumerate(range(2 * S, 22 * S, 2 * S)):
        x = 15 * S + int(2 * S * math.sin(i * 0.9))
        d.rectangle([x, yy, x + 2 * S - 1, yy + 2 * S - 1], fill=(90, 170, 240))
    # ruta amarilla punteada
    for i in range(8):
        x = (4 + i * 3) * S
        y = (18 - i) * S
        d.rectangle([x, y, x + 2 * S - 1, y + S - 1], fill=(250, 204, 21))
    # pin rojo
    px, py = 26 * S, 6 * S
    d.ellipse([px, py, px + 4 * S - 1, py + 4 * S - 1], fill=(230, 40, 60))
    d.polygon([(px + S, py + 4 * S), (px + 3 * S, py + 4 * S), (px + 2 * S, py + 7 * S)],
              fill=(230, 40, 60))
    return img


def paper_pencil_img(scale=6):
    wpx, hpx = 30 * scale, 28 * scale
    img = Image.new("RGBA", (wpx, hpx), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    S = scale
    # papel con esquina doblada
    d.polygon([(3 * S, 2 * S), (20 * S, 2 * S), (20 * S, 6 * S), (24 * S, 6 * S),
               (24 * S, 26 * S), (3 * S, 26 * S)], fill=(250, 250, 245))
    d.polygon([(20 * S, 2 * S), (20 * S, 6 * S), (24 * S, 6 * S)], fill=(200, 200, 190))
    d.rectangle([3 * S, 2 * S, 24 * S - 1, 26 * S - 1], outline=INK, width=max(1, S // 3))
    for yy in (8 * S, 12 * S, 16 * S, 20 * S):
        d.rectangle([5 * S, yy, 21 * S - 1, yy + max(1, S // 5)], fill=(120, 140, 200))
    # lápiz diagonal
    d.polygon([(22 * S, 22 * S), (25 * S, 24 * S), (29 * S, 10 * S), (26 * S, 8 * S)],
              fill=(250, 204, 21))
    d.polygon([(26 * S, 8 * S), (29 * S, 10 * S), (29 * S, 7 * S)], fill=(255, 205, 170))
    d.polygon([(29 * S, 7 * S), (29 * S, 10 * S), (30 * S - 1, 9 * S)], fill=(60, 60, 70))
    d.polygon([(22 * S, 22 * S), (25 * S, 24 * S), (24 * S, 25 * S), (21 * S, 23 * S)],
              fill=(255, 143, 171))
    return img


def wrench_img(scale=6):
    """Llave inglesa pixelada (intro 3)."""
    wpx, hpx = 24 * scale, 12 * scale
    img = Image.new("RGBA", (wpx, hpx), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    S = scale
    d.rectangle([2 * S, 5 * S, 20 * S - 1, 7 * S - 1], fill=(200, 205, 215))
    d.ellipse([18 * S, 2 * S, 24 * S - 1, 10 * S - 1], fill=(200, 205, 215))
    d.polygon([(21 * S, 2 * S), (24 * S - 1, 2 * S), (24 * S - 1, 5 * S), (22 * S, 5 * S)],
              fill=(0, 0, 0, 0))
    d.rectangle([0, 4 * S, 4 * S - 1, 8 * S - 1], fill=(200, 205, 215))
    return img
