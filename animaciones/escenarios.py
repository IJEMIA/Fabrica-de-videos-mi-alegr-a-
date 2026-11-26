# -*- coding: utf-8 -*-
"""Escenarios: fondos completos para los videos.

Cada escenario se dibuja con las mismas primitivas a cualquier resolución:
en el estilo aprendiz se renderiza a 720x1280 (plano, colores suaves) y en
snes/nes a baja resolución (180x320 / 144x256) para luego escalarlo con
vecino más cercano, que es lo que da el aspecto retro. Los fondos tienen
2-3 capas de parallax: la capa lejana se mueve despacio y la cercana rápido.

Uso desde un spec (aprendiz o retro):
    {"rotulo": "...", "narracion": "...", "escenario": "parque", ...}
La parte superior del cuadro se mantiene despejada para el rótulo.
"""
import math
import random

from PIL import Image, ImageDraw

from .core import WHITE, BLACK

# ---------------------------------------------------------------------------
# Primitivas (coordenadas en píxeles del lienzo que se esté dibujando)
# ---------------------------------------------------------------------------
def _sol(d, x, y, r, color=(250, 200, 40)):
    d.ellipse([x - r, y - r, x + r, y + r], fill=color)
    for i in range(8):
        ang = math.radians(i * 45)
        d.line([x + (r + 4) * math.cos(ang), y + (r + 4) * math.sin(ang),
                x + (r + 14) * math.cos(ang), y + (r + 14) * math.sin(ang)],
               fill=color, width=4)


def _luna(d, x, y, r):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(245, 245, 230))
    d.ellipse([x - r * 0.4, y - r * 0.2, x - r * 0.1, y + r * 0.1], fill=(220, 220, 200))
    d.ellipse([x + r * 0.2, y + r * 0.3, x + r * 0.45, y + r * 0.55], fill=(220, 220, 200))


def _nube(d, x, y, s, color=(255, 255, 255)):
    for dx, dy, r in [(-22, 6, 18), (0, -8, 24), (24, 6, 18)]:
        d.ellipse([x + (dx - r) * s, y + (dy - r) * s, x + (dx + r) * s, y + (dy + r) * s],
                  fill=color)
    d.rectangle([x - 38 * s, y + 2 * s, x + 38 * s, y + 18 * s], fill=color)


def _montana_pico(d, x, base_y, w, h, color):
    d.polygon([(x - w / 2, base_y), (x, base_y - h), (x + w / 2, base_y)], fill=color)
    d.polygon([(x - w * 0.18, base_y - h * 0.72), (x, base_y - h),
               (x + w * 0.18, base_y - h * 0.72)], fill=(255, 255, 255))


def _arbol(d, x, base_y, s, color=(60, 160, 80)):
    d.rectangle([x - 7 * s, base_y - 40 * s, x + 7 * s, base_y], fill=(150, 100, 50))
    for dx, dy, r in [(0, -62, 30), (-22, -42, 22), (22, -42, 22)]:
        d.ellipse([x + (dx - r) * s, base_y + (dy - r) * s,
                   x + (dx + r) * s, base_y + (dy + r) * s], fill=color)


def _pino(d, x, base_y, s, color=(40, 120, 60)):
    d.rectangle([x - 6 * s, base_y - 16 * s, x + 6 * s, base_y], fill=(120, 80, 40))
    for i, (w, y0) in enumerate([(56, -70), (44, -52), (32, -34)]):
        d.polygon([(x - w * s / 2, base_y + y0 * s), (x, base_y + (y0 - 26) * s),
                   (x + w * s / 2, base_y + y0 * s)], fill=color)


def _casa_dibujo(d, x, base_y, s, color=(240, 200, 140)):
    d.polygon([(x - 48 * s, base_y - 56 * s), (x, base_y - 98 * s),
               (x + 48 * s, base_y - 56 * s)], fill=(200, 70, 70))
    d.rectangle([x - 38 * s, base_y - 56 * s, x + 38 * s, base_y], fill=color)
    d.rectangle([x - 12 * s, base_y - 32 * s, x + 12 * s, base_y], fill=(120, 80, 40))
    d.rectangle([x + 16 * s, base_y - 46 * s, x + 30 * s, base_y - 30 * s],
                fill=(180, 230, 255))


def _edificio(d, x, base_y, w, h, color):
    d.rectangle([x, base_y - h, x + w, base_y], fill=color)
    for fila in range(max(1, int(h // 90))):
        for col in range(max(1, int(w // 60))):
            wx = x + 12 + col * 48
            wy = base_y - h + 16 + fila * 60
            if wx + 22 < x + w and wy + 26 < base_y:
                d.rectangle([wx, wy, wx + 22, wy + 26], fill=(255, 230, 150))


def _flor(d, x, y, s, color=(255, 120, 160)):
    d.line([x, y, x, y + 22 * s], fill=(70, 150, 70), width=max(2, int(3 * s)))
    for i in range(5):
        ang = math.radians(i * 72)
        px, py = x + 10 * s * math.cos(ang), y + 10 * s * math.sin(ang)
        d.ellipse([px - 7 * s, py - 7 * s, px + 7 * s, py + 7 * s], fill=color)
    d.ellipse([x - 6 * s, y - 6 * s, x + 6 * s, y + 6 * s], fill=(250, 210, 60))


def _olas(d, W, y, t, color=(255, 255, 255)):
    for wx in range(0, W + 90, 90):
        d.arc([wx - 40, y - 18, wx + 40, y + 30], start=180, end=360, fill=color, width=5)


def _estrellas(d, W, H, t, n=40, semilla=5):
    rnd = random.Random(semilla)
    for _ in range(n):
        sx = rnd.uniform(0, W)
        sy = rnd.uniform(0, H * 0.6)
        fase = rnd.uniform(0, 6.28)
        brillo = 0.5 + 0.5 * math.sin(2 * math.pi * t / 2.0 + fase)
        col = (int(255 * brillo),) * 3
        d.point((int(sx), int(sy)), fill=col)


def _cielo(d, W, H, color):
    d.rectangle([0, 0, W, H], fill=color)


def _suelo(d, W, H, y_frac, color):
    d.rectangle([0, H * y_frac, W, H], fill=color)


# ---------------------------------------------------------------------------
# Escenarios. Cada función recibe (d, W, H, t) y dibuja el fondo completo.
# Las capas se desplazan con t a distinta velocidad (parallax).
# ---------------------------------------------------------------------------
def _salon(d, W, H, t):
    _cielo(d, W, H, (245, 240, 225))
    # pizarrón (capa lejana)
    d.rectangle([W * 0.08, H * 0.42, W * 0.92, H * 0.58], fill=(60, 120, 80),
                outline=(150, 110, 60), width=6)
    d.line([W * 0.15, H * 0.47, W * 0.45, H * 0.47], fill=(255, 255, 255), width=3)
    d.line([W * 0.15, H * 0.51, W * 0.38, H * 0.51], fill=(255, 255, 255), width=3)
    # ventanas (capa media)
    for fx in (0.10, 0.78):
        d.rectangle([W * fx, H * 0.30, W * (fx + 0.12), H * 0.40], fill=(180, 220, 250),
                    outline=(120, 120, 120), width=3)
    # pupitres (capa cercana)
    for i, px in enumerate((0.12, 0.40, 0.68)):
        d.rectangle([W * px, H * 0.72, W * (px + 0.20), H * 0.75], fill=(180, 140, 90))
        d.rectangle([W * (px + 0.02), H * 0.75, W * (px + 0.05), H * 0.86], fill=(140, 100, 60))
        d.rectangle([W * (px + 0.15), H * 0.75, W * (px + 0.18), H * 0.86], fill=(140, 100, 60))
    _suelo(d, W, H, 0.86, (210, 180, 140))


def _oficina(d, W, H, t):
    _cielo(d, W, H, (235, 235, 240))
    d.rectangle([W * 0.06, H * 0.28, W * 0.34, H * 0.48], fill=(180, 220, 250),
                outline=(120, 120, 120), width=4)
    d.line([W * 0.20, H * 0.28, W * 0.20, H * 0.48], fill=(120, 120, 120), width=3)
    d.line([W * 0.06, H * 0.38, W * 0.34, H * 0.38], fill=(120, 120, 120), width=3)
    # escritorio con computadora (capa cercana)
    d.rectangle([W * 0.10, H * 0.68, W * 0.90, H * 0.71], fill=(150, 110, 70))
    d.rectangle([W * 0.14, H * 0.71, W * 0.18, H * 0.88], fill=(120, 85, 50))
    d.rectangle([W * 0.82, H * 0.71, W * 0.86, H * 0.88], fill=(120, 85, 50))
    d.rectangle([W * 0.55, H * 0.58, W * 0.75, H * 0.68], fill=(60, 70, 90))
    d.rectangle([W * 0.57, H * 0.60, W * 0.73, H * 0.66], fill=(140, 200, 250))
    _suelo(d, W, H, 0.88, (200, 190, 180))


def _parque(d, W, H, t):
    _cielo(d, W, H, (170, 220, 250))
    _sol(d, W * 0.82, H * 0.12, max(18, int(W * 0.05)))
    _nube(d, (W * 0.25 + 12 * t) % (W * 1.2) - W * 0.1, H * 0.16, W / 720)
    _nube(d, (W * 0.65 + 8 * t) % (W * 1.2) - W * 0.1, H * 0.24, W / 720 * 0.8)
    # árboles lejanos (parallax lento)
    for i in range(4):
        ax = (W * (0.1 + i * 0.25) + 4 * t) % (W * 1.1)
        _arbol(d, ax, H * 0.68, W / 720 * 0.9, (90, 170, 100))
    _suelo(d, W, H, 0.68, (120, 200, 110))
    # camino
    d.polygon([(W * 0.42, H * 0.68), (W * 0.58, H * 0.68), (W * 0.72, H), (W * 0.28, H)],
              fill=(230, 210, 170))
    # banca y flores (capa cercana)
    d.rectangle([W * 0.10, H * 0.74, W * 0.30, H * 0.76], fill=(150, 110, 60))
    d.rectangle([W * 0.12, H * 0.76, W * 0.14, H * 0.82], fill=(120, 85, 50))
    d.rectangle([W * 0.26, H * 0.76, W * 0.28, H * 0.82], fill=(120, 85, 50))
    for i, fx in enumerate((0.72, 0.80, 0.88)):
        _flor(d, W * fx, H * 0.80, W / 720, ((255, 120, 160), (255, 200, 60), (200, 120, 255))[i % 3])


def _calle(d, W, H, t):
    _cielo(d, W, H, (170, 210, 240))
    _nube(d, (W * 0.2 + 10 * t) % (W * 1.2) - W * 0.1, H * 0.14, W / 720)
    # edificios lejanos
    for i, (bx, bw, bh, col) in enumerate([(0.02, 0.16, 0.30, (180, 180, 200)),
                                           (0.24, 0.14, 0.38, (160, 160, 185)),
                                           (0.78, 0.18, 0.34, (175, 175, 195))]):
        _edificio(d, W * bx, H * 0.72, W * bw, H * bh, col)
    _suelo(d, W, H, 0.72, (140, 140, 145))
    # banqueta y calle
    d.rectangle([0, H * 0.72, W, H * 0.78], fill=(200, 200, 205))
    d.rectangle([0, H * 0.78, W, H], fill=(90, 90, 95))
    for i in range(5):
        lx = (W * (i * 0.22) + 30 * t) % (W * 1.1)
        d.rectangle([lx, H * 0.875, lx + W * 0.08, H * 0.885], fill=(250, 210, 60))
    # farola cercana
    d.rectangle([W * 0.12, H * 0.60, W * 0.13, H * 0.78], fill=(60, 60, 70))
    d.ellipse([W * 0.095, H * 0.575, W * 0.155, H * 0.615], fill=(250, 220, 120))


def _playa(d, W, H, t):
    _cielo(d, W, H, (150, 210, 245))
    _sol(d, W * 0.80, H * 0.12, max(18, int(W * 0.05)))
    _nube(d, (W * 0.3 + 10 * t) % (W * 1.2) - W * 0.1, H * 0.15, W / 720)
    # mar (capa media, con olas animadas)
    d.rectangle([0, H * 0.55, W, H * 0.72], fill=(70, 160, 220))
    _olas(d, W, H * 0.60, t)
    _olas(d, W, H * 0.68, t + 2)
    # arena (capa cercana)
    _suelo(d, W, H, 0.72, (245, 225, 170))
    # palmera
    d.line([W * 0.18, H * 0.72, W * 0.16, H * 0.52], fill=(150, 110, 60), width=8)
    for ang in (-60, -20, 20, 60):
        rad = math.radians(ang - 90)
        d.line([W * 0.16, H * 0.52, W * 0.16 + 60 * math.cos(rad) * W / 720,
                H * 0.52 + 60 * math.sin(rad) * W / 720], fill=(60, 160, 80), width=6)
    # sombrilla
    d.polygon([(W * 0.62, H * 0.72), (W * 0.78, H * 0.72), (W * 0.70, H * 0.60)],
              fill=(255, 120, 120))
    d.line([W * 0.70, H * 0.60, W * 0.70, H * 0.72], fill=(120, 90, 40), width=4)


def _espacio(d, W, H, t):
    _cielo(d, W, H, (12, 10, 35))
    _estrellas(d, W, H, t, n=60)
    # planeta lejano
    d.ellipse([W * 0.62, H * 0.10, W * 0.90, H * 0.24], fill=(200, 140, 80))
    d.ellipse([W * 0.58, H * 0.15, W * 0.94, H * 0.19], outline=(230, 200, 140), width=4)
    # luna cercana
    _luna(d, W * 0.18, H * 0.78, max(20, int(W * 0.07)))
    # nebulosa
    d.ellipse([W * 0.05, H * 0.40, W * 0.35, H * 0.55], fill=(80, 50, 130))
    d.ellipse([W * 0.12, H * 0.44, W * 0.28, H * 0.52], fill=(120, 70, 170))


def _ciudad(d, W, H, t):
    _cielo(d, W, H, (150, 190, 230))
    _sol(d, W * 0.15, H * 0.10, max(16, int(W * 0.045)))
    # edificios lejanos (parallax lento)
    for i, (bx, bw, bh) in enumerate([(0.0, 0.18, 0.34), (0.22, 0.15, 0.44),
                                      (0.42, 0.20, 0.30), (0.66, 0.16, 0.40), (0.86, 0.14, 0.32)]):
        _edificio(d, (W * bx + 6 * t) % (W * 1.1) - W * 0.05, H * 0.70, W * bw, H * bh,
                  (170, 170, 195))
    _suelo(d, W, H, 0.70, (120, 120, 130))
    d.rectangle([0, H * 0.70, W, H * 0.76], fill=(190, 190, 195))
    d.rectangle([0, H * 0.76, W, H], fill=(80, 80, 88))
    for i in range(6):
        lx = (W * (i * 0.18) + 40 * t) % (W * 1.1)
        d.rectangle([lx, H * 0.875, lx + W * 0.06, H * 0.885], fill=(250, 210, 60))


def _campo(d, W, H, t):
    _cielo(d, W, H, (160, 215, 245))
    _sol(d, W * 0.82, H * 0.11, max(18, int(W * 0.05)))
    _nube(d, (W * 0.25 + 8 * t) % (W * 1.2) - W * 0.1, H * 0.15, W / 720)
    # montañas lejanas
    _montana_pico(d, W * 0.25, H * 0.62, W * 0.5, H * 0.16, (140, 160, 190))
    _montana_pico(d, W * 0.75, H * 0.62, W * 0.45, H * 0.12, (160, 175, 200))
    _suelo(d, W, H, 0.62, (150, 200, 90))
    # surcos
    for i in range(5):
        d.line([W * (0.1 + i * 0.18), H * 0.66, W * (0.02 + i * 0.2), H], fill=(120, 170, 70), width=4)
    # granero y molino
    _casa_dibujo(d, W * 0.80, H * 0.72, W / 720 * 0.8, (200, 70, 70))
    d.line([W * 0.15, H * 0.62, W * 0.15, H * 0.72], fill=(120, 90, 40), width=5)
    for ang in (0, 90, 180, 270):
        rad = math.radians(ang + 20 * math.sin(t))
        d.line([W * 0.15, H * 0.58, W * 0.15 + 26 * math.cos(rad) * W / 720,
                H * 0.58 + 26 * math.sin(rad) * W / 720], fill=(240, 240, 240), width=4)


def _hospital(d, W, H, t):
    _cielo(d, W, H, (235, 245, 250))
    # cruz en la pared (fondo)
    d.rectangle([W * 0.44, H * 0.30, W * 0.56, H * 0.42], fill=(220, 60, 60))
    d.rectangle([W * 0.48, H * 0.26, W * 0.52, H * 0.46], fill=(220, 60, 60))
    # ventana
    d.rectangle([W * 0.08, H * 0.28, W * 0.26, H * 0.44], fill=(180, 220, 250),
                outline=(120, 120, 120), width=4)
    # camilla (capa cercana)
    d.rectangle([W * 0.14, H * 0.70, W * 0.86, H * 0.73], fill=(200, 220, 230))
    d.rectangle([W * 0.14, H * 0.62, W * 0.30, H * 0.70], fill=(240, 245, 250))
    for lx in (0.20, 0.78):
        d.rectangle([W * lx, H * 0.73, W * (lx + 0.03), H * 0.86], fill=(120, 120, 130))
    _suelo(d, W, H, 0.86, (210, 210, 215))


def _mercado(d, W, H, t):
    _cielo(d, W, H, (160, 210, 245))
    _sol(d, W * 0.85, H * 0.10, max(16, int(W * 0.045)))
    # puestos (capas)
    for i, (px, col) in enumerate([(0.06, (255, 120, 120)), (0.40, (255, 200, 60)),
                                   (0.74, (120, 200, 120))]):
        d.polygon([(W * px, H * 0.52), (W * (px + 0.20), H * 0.52),
                   (W * (px + 0.10), H * 0.44)], fill=col)
        d.rectangle([W * px, H * 0.52, W * (px + 0.20), H * 0.72], fill=(240, 230, 200))
        for j, fcol in enumerate([(255, 90, 90), (250, 200, 60), (90, 170, 90)]):
            d.ellipse([W * (px + 0.03 + j * 0.06), H * 0.58, W * (px + 0.07 + j * 0.06), H * 0.64],
                      fill=fcol)
    _suelo(d, W, H, 0.72, (190, 170, 140))


def _biblioteca(d, W, H, t):
    _cielo(d, W, H, (235, 225, 200))
    # estanterías (capa lejana)
    for i, sx in enumerate((0.06, 0.38, 0.70)):
        d.rectangle([W * sx, H * 0.30, W * (sx + 0.24), H * 0.66], fill=(150, 110, 60))
        for fila in range(3):
            d.rectangle([W * sx, H * (0.40 + fila * 0.10), W * (sx + 0.24), H * (0.41 + fila * 0.10)],
                        fill=(120, 85, 45))
            for j in range(5):
                d.rectangle([W * (sx + 0.015 + j * 0.045), H * (0.335 + fila * 0.10),
                             W * (sx + 0.05 + j * 0.045), H * (0.40 + fila * 0.10)],
                            fill=((200, 60, 60), (60, 120, 200), (60, 160, 80), (250, 200, 60), (160, 90, 200))[(j + fila) % 5])
    # mesa con libros (capa cercana)
    d.rectangle([W * 0.18, H * 0.74, W * 0.82, H * 0.77], fill=(150, 110, 60))
    d.rectangle([W * 0.22, H * 0.77, W * 0.25, H * 0.90], fill=(120, 85, 45))
    d.rectangle([W * 0.75, H * 0.77, W * 0.78, H * 0.90], fill=(120, 85, 45))
    for i, (lx, col) in enumerate([(0.32, (200, 60, 60)), (0.46, (60, 120, 200)), (0.60, (60, 160, 80))]):
        d.rectangle([W * lx, H * 0.68, W * (lx + 0.08), H * 0.74], fill=col)
    _suelo(d, W, H, 0.90, (200, 180, 150))


def _casa(d, W, H, t):
    _cielo(d, W, H, (250, 235, 210))
    # ventana con cortinas
    d.rectangle([W * 0.10, H * 0.26, W * 0.36, H * 0.46], fill=(170, 215, 245),
                outline=(120, 120, 120), width=4)
    d.rectangle([W * 0.10, H * 0.26, W * 0.16, H * 0.46], fill=(255, 150, 150))
    d.rectangle([W * 0.30, H * 0.26, W * 0.36, H * 0.46], fill=(255, 150, 150))
    # cuadro en la pared
    d.rectangle([W * 0.62, H * 0.28, W * 0.86, H * 0.42], fill=(200, 230, 180),
                outline=(150, 110, 60), width=5)
    _sol(d, W * 0.74, H * 0.35, max(10, int(W * 0.03)))
    # sofá (capa cercana)
    d.rectangle([W * 0.12, H * 0.66, W * 0.88, H * 0.78], fill=(200, 90, 90), )
    d.rectangle([W * 0.12, H * 0.58, W * 0.88, H * 0.68], fill=(220, 110, 110))
    d.rectangle([W * 0.12, H * 0.58, W * 0.20, H * 0.78], fill=(180, 70, 70))
    d.rectangle([W * 0.80, H * 0.58, W * 0.88, H * 0.78], fill=(180, 70, 70))
    # mesa con planta
    d.rectangle([W * 0.40, H * 0.80, W * 0.60, H * 0.82], fill=(150, 110, 60))
    d.rectangle([W * 0.48, H * 0.82, W * 0.52, H * 0.90], fill=(120, 85, 45))
    d.ellipse([W * 0.47, H * 0.74, W * 0.53, H * 0.80], fill=(220, 110, 60))
    _suelo(d, W, H, 0.90, (200, 170, 130))


def _estadio(d, W, H, t):
    _cielo(d, W, H, (150, 205, 245))
    _sol(d, W * 0.85, H * 0.10, max(16, int(W * 0.045)))
    # gradas (capas)
    d.polygon([(0, H * 0.62), (W, H * 0.62), (W, H * 0.44), (0, H * 0.44)], fill=(120, 120, 140))
    for fila in range(3):
        y0 = H * (0.47 + fila * 0.05)
        d.rectangle([0, y0, W, y0 + H * 0.02], fill=(90, 90, 110))
        for i in range(12):
            cx = W * (0.04 + i * 0.08)
            d.ellipse([cx, y0 + 2, cx + W * 0.02, y0 + H * 0.02], fill=((255, 90, 90), (255, 255, 255), (90, 160, 255), (255, 220, 90))[i % 4])
    # cancha (capa cercana)
    _suelo(d, W, H, 0.62, (90, 180, 90))
    d.ellipse([W * 0.30, H * 0.68, W * 0.70, H * 0.92], fill=WHITE, width=0)
    d.ellipse([W * 0.32, H * 0.70, W * 0.68, H * 0.90], fill=(90, 180, 90))
    d.ellipse([W * 0.46, H * 0.76, W * 0.54, H * 0.84], fill=WHITE)


def _jardin(d, W, H, t):
    _cielo(d, W, H, (165, 220, 250))
    _sol(d, W * 0.15, H * 0.10, max(16, int(W * 0.045)))
    _nube(d, (W * 0.5 + 9 * t) % (W * 1.2) - W * 0.1, H * 0.14, W / 720)
    _suelo(d, W, H, 0.60, (130, 200, 100))
    # seto
    d.rectangle([0, H * 0.60, W, H * 0.68], fill=(80, 160, 80))
    for i in range(8):
        d.ellipse([W * (i * 0.13), H * 0.585, W * (i * 0.13 + 0.10), H * 0.68], fill=(90, 175, 90))
    # flores y camino
    for i, (fx, col) in enumerate([(0.12, (255, 120, 160)), (0.24, (255, 200, 60)),
                                   (0.68, (200, 120, 255)), (0.80, (255, 120, 160)),
                                   (0.90, (255, 200, 60))]):
        _flor(d, W * fx, H * 0.80, W / 720)
    d.polygon([(W * 0.44, H * 0.68), (W * 0.56, H * 0.68), (W * 0.66, H), (W * 0.34, H)],
              fill=(230, 210, 170))


def _mar(d, W, H, t):
    _cielo(d, W, H, (140, 200, 240))
    _sol(d, W * 0.80, H * 0.11, max(18, int(W * 0.05)))
    _nube(d, (W * 0.2 + 10 * t) % (W * 1.2) - W * 0.1, H * 0.13, W / 720)
    # barco lejano
    d.polygon([(W * 0.30, H * 0.50), (W * 0.44, H * 0.50), (W * 0.40, H * 0.56), (W * 0.34, H * 0.56)],
              fill=(150, 90, 50))
    d.line([W * 0.37, H * 0.50, W * 0.37, H * 0.40], fill=(90, 60, 30), width=4)
    d.polygon([(W * 0.37, H * 0.40), (W * 0.47, H * 0.48), (W * 0.37, H * 0.48)], fill=(255, 255, 255))
    # mar con olas animadas (capas)
    d.rectangle([0, H * 0.56, W, H], fill=(50, 130, 200))
    _olas(d, W, H * 0.62, t)
    _olas(d, W, H * 0.74, t + 1.5)
    _olas(d, W, H * 0.88, t + 3)


def _desierto(d, W, H, t):
    _cielo(d, W, H, (255, 215, 150))
    _sol(d, W * 0.78, H * 0.12, max(20, int(W * 0.055)), color=(255, 180, 40))
    # dunas lejanas
    d.ellipse([-W * 0.2, H * 0.52, W * 0.5, H * 0.72], fill=(240, 200, 130))
    d.ellipse([W * 0.45, H * 0.55, W * 1.2, H * 0.75], fill=(235, 190, 120))
    _suelo(d, W, H, 0.68, (245, 210, 140))
    # cactus (capa cercana)
    for cx in (0.18, 0.82):
        d.rounded_rectangle([W * cx - 8, H * 0.62, W * cx + 8, H * 0.86], fill=(70, 160, 80),
                            radius=8)
        d.rounded_rectangle([W * cx - 26, H * 0.68, W * cx - 8, H * 0.78], fill=(70, 160, 80),
                            radius=6)
        d.rounded_rectangle([W * cx + 8, H * 0.72, W * cx + 26, H * 0.80], fill=(70, 160, 80),
                            radius=6)
    # piedras
    for px, pr in [(0.45, 14), (0.55, 10), (0.38, 8)]:
        d.ellipse([W * px - pr, H * 0.88 - pr // 2, W * px + pr, H * 0.88 + pr // 2],
                  fill=(200, 170, 110))


def _bosque(d, W, H, t):
    _cielo(d, W, H, (150, 200, 170))
    _sol(d, W * 0.80, H * 0.10, max(14, int(W * 0.04)))
    # pinos lejanos (parallax lento)
    for i in range(5):
        px = (W * (0.05 + i * 0.22) + 5 * t) % (W * 1.1)
        _pino(d, px, H * 0.66, W / 720 * 0.9, (60, 140, 80))
    _suelo(d, W, H, 0.66, (90, 150, 80))
    # pinos cercanos
    _pino(d, W * 0.15, H * 0.88, W / 720 * 1.5)
    _pino(d, W * 0.85, H * 0.88, W / 720 * 1.5)
    _arbol(d, W * 0.50, H * 0.86, W / 720 * 1.1, (70, 160, 80))
    # flores del suelo
    for i, fx in enumerate((0.30, 0.42, 0.62, 0.72)):
        _flor(d, W * fx, H * 0.92, W / 720 * 0.8)


def _montana(d, W, H, t):
    _cielo(d, W, H, (140, 190, 235))
    _sol(d, W * 0.82, H * 0.10, max(16, int(W * 0.045)))
    _nube(d, (W * 0.3 + 8 * t) % (W * 1.2) - W * 0.1, H * 0.16, W / 720)
    # cordillera lejana
    _montana_pico(d, W * 0.20, H * 0.64, W * 0.45, H * 0.22, (130, 150, 185))
    _montana_pico(d, W * 0.55, H * 0.64, W * 0.50, H * 0.28, (110, 135, 170))
    _montana_pico(d, W * 0.88, H * 0.64, W * 0.40, H * 0.18, (140, 160, 190))
    # ladera cercana con pinos
    d.polygon([(0, H * 0.64), (W * 0.35, H * 0.78), (0, H)], fill=(90, 140, 90))
    d.polygon([(W, H * 0.64), (W * 0.65, H * 0.78), (W, H)], fill=(80, 130, 85))
    _pino(d, W * 0.18, H * 0.82, W / 720 * 0.9)
    _pino(d, W * 0.82, H * 0.84, W / 720 * 0.9)
    _suelo(d, W, H, 0.92, (120, 170, 90))


# ---------------------------------------------------------------------------
# Registro y entrada principal
# ---------------------------------------------------------------------------
ESCENARIOS = {
    "salon": (_salon, "Salón de clases: pizarrón, ventanas y pupitres.", False),
    "oficina": (_oficina, "Oficina: ventana, escritorio y computadora.", False),
    "parque": (_parque, "Parque: árboles, camino, banca y flores.", False),
    "calle": (_calle, "Calle de día: edificios, banqueta y farola.", False),
    "playa": (_playa, "Playa: mar con olas, arena, palmera y sombrilla.", False),
    "espacio": (_espacio, "Espacio: estrellas, planeta, luna y nebulosa. Fondo oscuro.", True),
    "ciudad": (_ciudad, "Ciudad: rascacielos, calle y líneas viales.", False),
    "campo": (_campo, "Campo: montañas, surcos, granero y molino.", False),
    "hospital": (_hospital, "Hospital: cruz, ventana y camilla.", False),
    "mercado": (_mercado, "Mercado: puestos de colores con frutas.", False),
    "biblioteca": (_biblioteca, "Biblioteca: estanterías de libros y mesa de lectura.", False),
    "casa": (_casa, "Casa/sala: ventana, cuadro, sofá y mesa.", False),
    "estadio": (_estadio, "Estadio: gradas con público y cancha.", False),
    "jardin": (_jardin, "Jardín: seto, flores y camino.", False),
    "mar": (_mar, "Mar: barco, olas animadas y cielo abierto.", False),
    "desierto": (_desierto, "Desierto: dunas, sol fuerte y cactus.", False),
    "bosque": (_bosque, "Bosque: pinos en varias capas y flores.", False),
    "montana": (_montana, "Montaña: cordillera con nieve y ladera con pinos.", False),
}

ESCENARIOS_OSCUROS = {n for n, (_, _, oscuro) in ESCENARIOS.items() if oscuro}


def fondo_escenario(nombre, W, H, t=0.0):
    """Dibuja el fondo completo de un escenario (imagen RGB de W x H)."""
    if nombre not in ESCENARIOS:
        raise ValueError(f"Escenario desconocido: {nombre!r}. Ver ESCENARIOS en escenarios.py.")
    fn, _, _ = ESCENARIOS[nombre]
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    fn(d, W, H, t)
    return img
