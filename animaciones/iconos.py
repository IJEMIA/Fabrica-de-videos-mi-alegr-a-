# -*- coding: utf-8 -*-
"""Íconos del estilo aprendiz: farolas, cámaras, Júpiter, deportes, etc."""
import math
from PIL import Image, ImageDraw, ImageFont
from .core import (W, H, WHITE, BLACK, MINT, MINT2, SKIN, SKIN_D, HAIR, PURPLE,
                   PURPLE_D, BLUE, BLUE_D, BROWN, GREEN, GREEN_D, YELLOW,
                   YELLOW_L, RED, RED_D, GRAY, GRAY_D, POLE, ORANGE, COURT_G,
                   JUP_CREAM, JUP_TAN, JUP_BROWN, JUP_WHITE, JUP_ORANGE,
                   SPOT_RED, ICE, ICE_LINE, OCEAN, OCEAN_D, CLOUD,
                   font_hand, font_bold, ease_out, pop, blink)


def draw_street_lamp(d, x, base_y, s=1.0, on=False, glow=1.0):
    """Farola de calle. base_y = suelo."""
    h = int(300 * s)
    top_y = base_y - h
    d.rounded_rectangle([x - int(7 * s), top_y, x + int(7 * s), base_y], radius=int(7 * s), fill=POLE)
    d.line([x, top_y, x + int(70 * s), top_y], fill=POLE, width=int(12 * s))
    lx = x + int(78 * s)
    d.polygon([(lx - int(26 * s), top_y), (lx + int(26 * s), top_y),
               (lx + int(16 * s), top_y + int(30 * s)), (lx - int(16 * s), top_y + int(30 * s))],
              fill=GRAY_D)
    if on:
        # Resplandor: elipse amarilla pálida detrás de la lámpara (sin alfa)
        d.ellipse([lx - int(120 * s), top_y - int(90 * s), lx + int(120 * s), top_y + int(150 * s)],
                  fill=(255, 240, 180))
        d.polygon([(lx - int(16 * s), top_y + int(30 * s)), (lx + int(16 * s), top_y + int(30 * s)),
                   (lx + int(55 * s), top_y + int(150 * s)), (lx - int(55 * s), top_y + int(150 * s))],
                  fill=(255, 224, 130))
        d.ellipse([lx - int(16 * s), top_y + int(14 * s), lx + int(16 * s), top_y + int(46 * s)], fill=YELLOW)
    else:
        d.ellipse([lx - int(16 * s), top_y + int(14 * s), lx + int(16 * s), top_y + int(46 * s)], fill=(200, 200, 200))
    return d


def draw_hand_lamp(d, x, y, s=1.0, on=True):
    """Lámpara ahorradora pequeña (bombillo) en la mano."""
    r = int(30 * s)
    d.ellipse([x - r, y - r, x + r, y + r], fill=YELLOW if on else (210, 210, 210))
    d.rounded_rectangle([x - int(12 * s), y + r - int(4 * s), x + int(12 * s), y + r + int(18 * s)],
                        radius=int(5 * s), fill=GRAY)
    if on:
        for a in range(8):
            ang = a * math.pi / 4
            x1, y1 = x + int((r + 8) * math.cos(ang)), y + int((r + 8) * math.sin(ang))
            x2, y2 = x + int((r + 20) * math.cos(ang)), y + int((r + 20) * math.sin(ang))
            d.line([x1, y1, x2, y2], fill=YELLOW, width=int(5 * s))


def draw_camera(d, x, y, s=1.0):
    """Cámara de vigilancia sobre poste."""
    d.rounded_rectangle([x - int(6 * s), y, x + int(6 * s), y + int(150 * s)], radius=int(6 * s), fill=POLE)
    d.rounded_rectangle([x - int(45 * s), y - int(40 * s), x + int(55 * s), y + int(5 * s)],
                        radius=int(12 * s), fill=(240, 240, 240), outline=GRAY, width=int(3 * s))
    d.ellipse([x + int(30 * s), y - int(30 * s), x + int(62 * s), y - int(2 * s)], fill=(40, 60, 90))
    d.ellipse([x + int(38 * s), y - int(22 * s), x + int(54 * s), y - int(10 * s)], fill=(120, 180, 230))
    d.line([x, y + int(150 * s), x - int(30 * s), y + int(150 * s)], fill=POLE, width=int(10 * s))
    d.line([x, y + int(150 * s), x + int(30 * s), y + int(150 * s)], fill=POLE, width=int(10 * s))


def draw_check(d, cx, cy, r, color=GREEN):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    d.line([cx - int(r * 0.45), cy, cx - int(r * 0.1), cy + int(r * 0.4)], fill=(255, 255, 255), width=int(r * 0.28))
    d.line([cx - int(r * 0.1), cy + int(r * 0.4), cx + int(r * 0.5), cy - int(r * 0.4)], fill=(255, 255, 255), width=int(r * 0.28))


def draw_small_person(d, x, y, s, color):
    d.ellipse([x - int(14 * s), y - int(34 * s), x + int(14 * s), y - int(6 * s)], fill=SKIN)
    d.rounded_rectangle([x - int(18 * s), y - int(4 * s), x + int(18 * s), y + int(34 * s)],
                        radius=int(10 * s), fill=color)


def draw_money_bag(d, cx, cy, s=1.0):
    d.ellipse([cx - int(70 * s), cy - int(20 * s), cx + int(70 * s), cy + int(80 * s)], fill=(232, 197, 120))
    d.polygon([(cx - int(30 * s), cy - int(20 * s)), (cx + int(30 * s), cy - int(20 * s)),
               (cx + int(14 * s), cy - int(62 * s)), (cx - int(14 * s), cy - int(62 * s))], fill=(214, 172, 92))
    d.line([cx - int(34 * s), cy - int(26 * s), cx + int(34 * s), cy - int(26 * s)], fill=(180, 140, 70), width=int(6 * s))
    f = font_bold(int(44 * s))
    t = "$"
    w = d.textlength(t, font=f)
    d.text((cx - w / 2, cy + int(2 * s)), t, font=f, fill=(90, 60, 20))


def draw_soccer_ball(d, cx, cy, s=1.0):
    r = int(48 * s)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=BLACK, width=int(4 * s))
    pr = int(15 * s)
    d.polygon([(cx, cy - pr), (cx + pr, cy - int(pr * 0.3)), (cx + int(pr * 0.6), cy + pr),
               (cx - int(pr * 0.6), cy + pr), (cx - pr, cy - int(pr * 0.3))], fill=BLACK)
    for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, -1.4)]:
        px, py = cx + int(dx * r * 0.62), cy + int(dy * r * 0.55)
        d.polygon([(px, py - int(9 * s)), (px + int(9 * s), py), (px, py + int(9 * s)),
                   (px - int(9 * s), py)], fill=BLACK)


def draw_basketball(d, cx, cy, s=1.0):
    r = int(48 * s)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ORANGE, outline=(120, 60, 20), width=int(4 * s))
    d.line([cx - r, cy, cx + r, cy], fill=(120, 60, 20), width=int(4 * s))
    d.line([cx, cy - r, cx, cy + r], fill=(120, 60, 20), width=int(4 * s))
    # Costuras curvas dentro del círculo (arcos superior e inferior)
    d.arc([cx - r, cy - r, cx + r, cy + r], start=300, end=60, fill=(120, 60, 20), width=int(4 * s))
    d.arc([cx - r, cy - r, cx + r, cy + r], start=120, end=240, fill=(120, 60, 20), width=int(4 * s))


def draw_whistle(d, cx, cy, s=1.0):
    d.ellipse([cx - int(42 * s), cy - int(34 * s), cx + int(42 * s), cy + int(34 * s)], fill=(200, 205, 210), outline=GRAY, width=int(3 * s))
    d.ellipse([cx - int(12 * s), cy - int(10 * s), cx + int(12 * s), cy + int(10 * s)], fill=GRAY_D)
    d.rounded_rectangle([cx + int(30 * s), cy - int(14 * s), cx + int(78 * s), cy + int(14 * s)],
                        radius=int(10 * s), fill=(200, 205, 210), outline=GRAY, width=int(3 * s))


def draw_heart(d, cx, cy, s=1.0):
    r = int(34 * s)
    d.ellipse([cx - r, cy - int(r * 0.7), cx, cy + int(r * 0.5)], fill=RED)
    d.ellipse([cx, cy - int(r * 0.7), cx + r, cy + int(r * 0.5)], fill=RED)
    d.polygon([(cx - r, cy), (cx + r, cy), (cx, cy + int(r * 1.4))], fill=RED)


def draw_court(d, x0, y0, x1, y1):
    d.rounded_rectangle([x0, y0, x1, y1], radius=24, fill=COURT_G, outline=WHITE, width=5)
    d.line([(x0 + x1) / 2, y0, (x0 + x1) / 2, y1], fill=WHITE, width=5)
    d.ellipse([(x0 + x1) / 2 - 55, (y0 + y1) / 2 - 55, (x0 + x1) / 2 + 55, (y0 + y1) / 2 + 55],
              outline=WHITE, width=5)
    # Aro de básquet a la derecha: tablero + aro visto desde arriba
    d.rectangle([x1 - 48, y0 + 22, x1 - 18, y0 + 82], fill=WHITE, outline=ORANGE, width=4)
    d.ellipse([x1 - 58, y0 + 78, x1 - 8, y0 + 102], outline=ORANGE, width=5)


def draw_jupiter_img(img, cx, cy, r, spot=True, bob=0.0):
    """Versión con capas: dibuja Júpiter con bandas recortadas en círculo."""
    cy = cy + bob
    tmp = Image.new("RGB", (W, H), (0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.ellipse([cx - r, cy - r, cx + r, cy + r], fill=JUP_CREAM)
    bands = [
        (-0.82, -0.62, JUP_TAN),
        (-0.55, -0.38, JUP_WHITE),
        (-0.30, -0.12, JUP_BROWN),
        (-0.05, 0.12, JUP_WHITE),
        (0.18, 0.36, JUP_ORANGE),
        (0.42, 0.60, JUP_TAN),
        (0.66, 0.84, JUP_WHITE),
    ]
    for y0f, y1f, col in bands:
        td.rectangle([cx - r, cy + y0f * r, cx + r, cy + y1f * r], fill=col)
    if spot:
        # Gran Mancha Roja (óvalo) con borde más oscuro
        sx, sy, sr = cx + int(0.28 * r), cy + int(0.42 * r), int(0.30 * r)
        td.ellipse([sx - sr, sy - int(sr * 0.55), sx + sr, sy + int(sr * 0.55)], fill=SPOT_RED)
        td.ellipse([sx - int(sr * 0.7), sy - int(sr * 0.35), sx + int(sr * 0.7), sy + int(sr * 0.35)], fill=(215, 105, 70))
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    img.paste(tmp, (0, 0), mask)
    return ImageDraw.Draw(img)


def draw_telescope(d, x, base_y, s=1.0):
    """Telescopio sobre trípode, apuntando arriba a la derecha."""
    # Trípode
    d.line([x, base_y - int(110 * s), x - int(55 * s), base_y], fill=GRAY_D, width=int(9 * s))
    d.line([x, base_y - int(110 * s), x + int(55 * s), base_y], fill=GRAY_D, width=int(9 * s))
    d.line([x, base_y - int(110 * s), x, base_y], fill=GRAY_D, width=int(9 * s))
    # Tubo inclinado
    x0, y0 = x - int(30 * s), base_y - int(150 * s)
    x1, y1 = x + int(110 * s), base_y - int(215 * s)
    d.line([x0, y0, x1, y1], fill=(70, 90, 130), width=int(34 * s))
    d.line([x0, y0, x1, y1], fill=(100, 130, 180), width=int(22 * s))
    # Lente (boca ancha)
    d.ellipse([x1 - int(20 * s), y1 - int(26 * s), x1 + int(26 * s), y1 + int(20 * s)], fill=(150, 200, 240))
    d.ellipse([x1 - int(12 * s), y1 - int(16 * s), x1 + int(14 * s), y1 + int(10 * s)], fill=(210, 235, 250))


def draw_star(d, cx, cy, r, color=YELLOW):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)


def draw_cloud(d, cx, cy, s=1.0, color=CLOUD):
    for dx, dy, r in [(-40, 8, 34), (0, -12, 44), (44, 8, 34), (0, 14, 40)]:
        d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s,
                   cx + dx * s + r * s, cy + dy * s + r * s], fill=color, outline=(220, 220, 220))


def draw_floater(d, cx, cy, s=1.0, color=(255, 190, 90), bob=0.0):
    """Criatura globo (flotador): cuerpo redondo, aletas y colita."""
    cy = cy + bob
    r = int(62 * s)
    # Colita
    d.line([cx, cy + r, cx - int(10 * s), cy + r + int(46 * s)], fill=color, width=int(10 * s))
    d.line([cx, cy + r, cx + int(12 * s), cy + r + int(40 * s)], fill=color, width=int(10 * s))
    # Aletas laterales
    d.ellipse([cx - r - int(26 * s), cy - int(10 * s), cx - r + int(18 * s), cy + int(30 * s)], fill=color)
    d.ellipse([cx + r - int(18 * s), cy - int(10 * s), cx + r + int(26 * s), cy + int(30 * s)], fill=color)
    # Cuerpo
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    d.ellipse([cx - int(r * 0.55), cy - int(r * 0.7), cx + int(r * 0.55), cy - int(r * 0.1)], fill=(255, 225, 170))
    # Ojo y boca
    d.ellipse([cx - int(18 * s), cy - int(8 * s), cx - int(2 * s), cy + int(8 * s)], fill=BLACK)
    d.ellipse([cx + int(6 * s), cy - int(8 * s), cx + int(22 * s), cy + int(8 * s)], fill=BLACK)
    d.arc([cx - int(16 * s), cy + int(16 * s), cx + int(16 * s), cy + int(36 * s)],
          start=0, end=180, fill=BLACK, width=int(4 * s))


def draw_hunter(d, cx, cy, s=1.0, bob=0.0):
    """Cazador: criatura alargada con boca grande y dientes."""
    cy = cy + bob
    # Cuerpo alargado
    d.ellipse([cx - int(95 * s), cy - int(45 * s), cx + int(95 * s), cy + int(45 * s)], fill=(150, 90, 160))
    # Aleta dorsal
    d.polygon([(cx - int(20 * s), cy - int(45 * s)), (cx + int(10 * s), cy - int(95 * s)),
               (cx + int(50 * s), cy - int(45 * s))], fill=(120, 70, 135))
    # Cola
    d.polygon([(cx - int(95 * s), cy), (cx - int(150 * s), cy - int(40 * s)),
               (cx - int(150 * s), cy + int(40 * s))], fill=(120, 70, 135))
    # Boca grande con dientes
    d.ellipse([cx + int(20 * s), cy - int(5 * s), cx + int(95 * s), cy + int(35 * s)], fill=(255, 255, 255))
    for tx in range(5):
        x0 = cx + int((30 + tx * 12) * s)
        d.polygon([(x0, cy - int(5 * s)), (x0 + int(6 * s), cy + int(10 * s)), (x0 + int(12 * s), cy - int(5 * s))],
                  fill=WHITE)
    # Ojo
    d.ellipse([cx + int(30 * s), cy - int(38 * s), cx + int(55 * s), cy - int(13 * s)], fill=(255, 255, 255))
    d.ellipse([cx + int(38 * s), cy - int(32 * s), cx + int(50 * s), cy - int(20 * s)], fill=BLACK)


def draw_thermometer(d, x, y, s=1.0, cold=True):
    """Termómetro vertical: frío (azul) o caliente (rojo)."""
    w = int(30 * s)
    h = int(150 * s)
    d.rounded_rectangle([x - w // 2, y, x + w // 2, y + h], radius=w // 2, fill=(255, 255, 255),
                        outline=GRAY, width=int(3 * s))
    col = (60, 140, 220) if cold else (230, 70, 50)
    fill_h = int(h * 0.35) if cold else int(h * 0.85)
    d.rectangle([x - w // 2 + int(5 * s), y + h - fill_h, x + w // 2 - int(5 * s), y + h - int(5 * s)], fill=col)
    d.ellipse([x - int(26 * s), y + h - int(16 * s), x + int(26 * s), y + h + int(32 * s)], fill=col)
    # Marcas
    for i in range(4):
        yy = y + int(20 * s) + i * int(32 * s)
        d.line([x + w // 2 - int(10 * s), yy, x + w // 2, yy], fill=GRAY, width=int(3 * s))
    # Símbolo
    f = font_bold(int(40 * s))
    sym = "❄" if cold else "☀"
    try:
        tw = d.textlength(sym, font=f)
        d.text((x - tw / 2, y - int(52 * s)), sym, font=f, fill=col)
    except Exception:
        pass


def draw_radiation(d, cx, cy, t, s=1.0):
    """Rayos de radiación: zigzags amarillos que bajan con parpadeo suave."""
    for i, (rx, ry) in enumerate([(-120, -40), (-40, -70), (40, -50), (120, -30)]):
        a = 0.55 + 0.45 * math.sin(2 * math.pi * t / 0.9 + i * 1.3)
        col = (255, 200, 40) if a > 0.6 else (255, 225, 120)
        x, y = cx + rx, cy + ry
        d.line([(x, y), (x - 14, y + 34), (x + 6, y + 34), (x - 8, y + 68)],
               fill=col, width=int(8 * s), joint="curve")


def draw_umbrella(d, x, y, s=1.0):
    """Paraguas/escudo sobre el personaje."""
    r = int(150 * s)
    d.pieslice([x - r, y - int(r * 0.55), x + r, y + int(r * 0.55)], start=180, end=360, fill=(60, 140, 220))
    d.pieslice([x - r, y - int(r * 0.55), x + r, y + int(r * 0.55)], start=180, end=360,
               outline=(40, 100, 170), width=int(4 * s))
    # Gajos
    for fx in (-0.5, 0.0, 0.5):
        d.arc([x - r, y - int(r * 0.55), x + r, y + int(r * 0.55)],
              start=180 + 0, end=360, fill=(40, 100, 170), width=int(3 * s))
    d.line([x, y, x, y + int(150 * s)], fill=(90, 60, 30), width=int(7 * s))
    d.ellipse([x - int(8 * s), y - int(r * 0.55) - int(10 * s), x + int(8 * s), y - int(r * 0.55) + int(10 * s)],
              fill=(90, 60, 30))


# ---------------------------------------------------------------------------
# Objetos genéricos (estilo aprendiz, formas suaves)
# ---------------------------------------------------------------------------
# Cada función dibuja un objeto centrado en (cx, cy), de ~100*s px de alto.
# ``color`` cambia el color principal. El registro OBJETOS permite usarlos
# desde un spec con {"tipo": "objeto", "nombre": "...", "x": .., "y": ..}.
# Para SNES/NES se pixelizan automáticamente (ver estilos.pixelizar_objeto).

def _r(d, cx, cy, w, h, s, fill, outline=None, radius=0):
    x0, y0 = cx - w * s / 2, cy - h * s / 2
    x1, y1 = cx + w * s / 2, cy + h * s / 2
    if radius:
        d.rounded_rectangle([x0, y0, x1, y1], radius=radius * s, fill=fill,
                            outline=outline, width=max(1, int(2 * s)) if outline else 1)
    else:
        d.rectangle([x0, y0, x1, y1], fill=fill, outline=outline,
                    width=max(1, int(2 * s)) if outline else 1)


def obj_libro(d, cx, cy, s=1.0, color=(200, 60, 60), t=0.0):
    _r(d, cx, cy, 70, 90, s, color, outline=(120, 30, 30), radius=6)
    d.line([cx, cy - 45 * s, cx, cy + 45 * s], fill=WHITE, width=max(1, int(3 * s)))
    for yy in (-25, -5, 15, 35):
        d.line([cx - 26 * s, cy + yy * s, cx - 8 * s, cy + yy * s], fill=WHITE, width=max(1, int(2 * s)))
        d.line([cx + 8 * s, cy + yy * s, cx + 26 * s, cy + yy * s], fill=WHITE, width=max(1, int(2 * s)))


def obj_monedas(d, cx, cy, s=1.0, color=(250, 200, 60), t=0.0):
    for i, (dx, dy, r) in enumerate([(-18, 18, 20), (14, 22, 20), (0, -12, 22)]):
        d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s],
                  fill=color, outline=(200, 150, 30), width=max(1, int(2 * s)))
        d.text((cx + dx * s, cy + dy * s), "$", font=font_bold(max(8, int(22 * s))),
               fill=(180, 130, 20), anchor="mm")


def obj_billetes(d, cx, cy, s=1.0, color=(120, 200, 120), t=0.0):
    for i, dy in enumerate([-16, 0, 16]):
        _r(d, cx + (i - 1) * 8, cy + dy, 76, 34, s, color, outline=(60, 140, 60), radius=4)
        d.ellipse([cx + (i - 1) * 8 - 12 * s, cy + dy - 10 * s, cx + (i - 1) * 8 + 12 * s, cy + dy + 10 * s],
                  fill=(240, 250, 240))
        d.text((cx + (i - 1) * 8, cy + dy), "$", font=font_bold(max(8, int(16 * s))),
               fill=(60, 140, 60), anchor="mm")


def obj_alcancia(d, cx, cy, s=1.0, color=(255, 150, 180), t=0.0):
    d.ellipse([cx - 42 * s, cy - 30 * s, cx + 42 * s, cy + 30 * s], fill=color,
              outline=(200, 90, 130), width=max(1, int(2 * s)))
    d.ellipse([cx - 30 * s, cy - 44 * s, cx - 8 * s, cy - 24 * s], fill=color)  # oreja
    d.ellipse([cx - 22 * s, cy - 8 * s, cx - 8 * s, cy + 6 * s], fill=(40, 40, 40))  # ojo
    d.line([cx + 22 * s, cy - 6 * s, cx + 42 * s, cy - 6 * s], fill=(200, 90, 130), width=max(1, int(3 * s)))
    d.rectangle([cx - 8 * s, cy - 34 * s, cx + 8 * s, cy - 28 * s], fill=(200, 90, 130))
    for dx in (-24, 24):
        d.rectangle([cx + dx * s - 6 * s, cy + 26 * s, cx + dx * s + 6 * s, cy + 40 * s], fill=color)


def obj_grafico(d, cx, cy, s=1.0, color=(70, 130, 200), t=0.0):
    _r(d, cx, cy, 90, 80, s, WHITE, outline=BLACK, radius=6)
    d.line([cx - 36 * s, cy + 30 * s, cx + 36 * s, cy + 30 * s], fill=BLACK, width=max(1, int(2 * s)))
    d.line([cx - 36 * s, cy + 30 * s, cx - 36 * s, cy - 30 * s], fill=BLACK, width=max(1, int(2 * s)))
    for i, h in enumerate([18, 34, 26, 46]):
        x0 = cx - 28 * s + i * 18 * s
        d.rectangle([x0, cy + 30 * s - h * s, x0 + 12 * s, cy + 30 * s],
                    fill=color if i % 2 == 0 else (255, 150, 60))


def obj_puerta(d, cx, cy, s=1.0, color=(150, 100, 50), t=0.0):
    _r(d, cx, cy, 64, 96, s, color, outline=(90, 60, 30), radius=4)
    d.ellipse([cx + 16 * s, cy + 6 * s, cx + 26 * s, cy + 16 * s], fill=(250, 210, 60))
    d.rectangle([cx - 24 * s, cy - 36 * s, cx + 24 * s, cy - 20 * s], fill=(255, 255, 255, 120))


def obj_arbol(d, cx, cy, s=1.0, color=(60, 160, 80), t=0.0):
    d.rectangle([cx - 7 * s, cy + 10 * s, cx + 7 * s, cy + 50 * s], fill=(150, 100, 50))
    for dx, dy, r in [(0, -28, 34), (-24, -6, 24), (24, -6, 24)]:
        d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s],
                  fill=color)
    for dx, dy in [(-14, -30), (12, -38), (0, -12)]:
        d.ellipse([cx + dx * s - 4 * s, cy + dy * s - 4 * s, cx + dx * s + 4 * s, cy + dy * s + 4 * s],
                  fill=(255, 90, 90))


def obj_planta(d, cx, cy, s=1.0, color=(70, 170, 90), t=0.0):
    d.polygon([(cx - 26 * s, cy + 14 * s), (cx + 26 * s, cy + 14 * s),
               (cx + 18 * s, cy + 48 * s), (cx - 18 * s, cy + 48 * s)], fill=(220, 110, 60))
    for ang in (-50, -20, 10, 40):
        rad = math.radians(ang - 90)
        ex = cx + 30 * s * math.cos(rad)
        ey = cy + 10 * s + 34 * s * math.sin(rad)
        d.line([cx, cy + 14 * s, ex, ey], fill=color, width=max(2, int(6 * s)))


def obj_casa(d, cx, cy, s=1.0, color=(240, 200, 140), t=0.0):
    d.polygon([(cx - 48 * s, cy - 6 * s), (cx, cy - 48 * s), (cx + 48 * s, cy - 6 * s)],
              fill=(200, 70, 70))
    _r(d, cx, cy + 22, 76, 56, s, color, outline=(180, 140, 80), radius=2)
    _r(d, cx - 14, cy + 30, 24, 36, s, (120, 80, 40), radius=2)
    _r(d, cx + 20, cy - 2, 20, 20, s, (180, 230, 255), outline=(120, 120, 120), radius=2)
    d.line([cx - 14 * s, cy - 2 * s, cx + 14 * s, cy - 2 * s], fill=(180, 140, 80), width=max(1, int(2 * s)))


def obj_escuela(d, cx, cy, s=1.0, color=(250, 220, 150), t=0.0):
    _r(d, cx, cy + 10, 92, 64, s, color, outline=(180, 150, 80), radius=4)
    d.polygon([(cx - 52 * s, cy - 22 * s), (cx, cy - 48 * s), (cx + 52 * s, cy - 22 * s)],
              fill=(200, 70, 70))
    for dx in (-28, 0, 28):
        _r(d, cx + dx, cy - 2, 18, 18, s, (180, 230, 255), outline=(120, 120, 120), radius=2)
    _r(d, cx, cy + 34, 22, 30, s, (120, 80, 40), radius=2)
    d.line([cx, cy - 48 * s, cx, cy - 66 * s], fill=(60, 60, 60), width=max(1, int(3 * s)))
    d.polygon([(cx, cy - 66 * s), (cx + 22 * s, cy - 58 * s), (cx, cy - 50 * s)], fill=(255, 90, 90))


def obj_carro(d, cx, cy, s=1.0, color=(220, 60, 60), t=0.0):
    _r(d, cx, cy + 12, 88, 26, s, color, outline=(120, 30, 30), radius=10)
    d.polygon([(cx - 30 * s, cy - 2 * s), (cx - 18 * s, cy - 24 * s),
               (cx + 22 * s, cy - 24 * s), (cx + 34 * s, cy - 2 * s)], fill=color)
    _r(d, cx - 12, cy - 12, 22, 16, s, (180, 230, 255), radius=2)
    _r(d, cx + 16, cy - 12, 20, 16, s, (180, 230, 255), radius=2)
    for dx in (-26, 26):
        d.ellipse([cx + (dx - 12) * s, cy + 20 * s, cx + (dx + 12) * s, cy + 44 * s],
                  fill=(30, 30, 30))
        d.ellipse([cx + (dx - 5) * s, cy + 27 * s, cx + (dx + 5) * s, cy + 37 * s],
                  fill=(200, 200, 200))


def obj_autobus(d, cx, cy, s=1.0, color=(250, 200, 40), t=0.0):
    _r(d, cx, cy, 92, 52, s, color, outline=(200, 150, 20), radius=10)
    for dx in (-30, -6, 18, 36):
        _r(d, cx + dx, cy - 8, 18, 18, s, (180, 230, 255), outline=(120, 120, 120), radius=2)
    for dx in (-28, 28):
        d.ellipse([cx + (dx - 12) * s, cy + 18 * s, cx + (dx + 12) * s, cy + 42 * s],
                  fill=(30, 30, 30))
        d.ellipse([cx + (dx - 5) * s, cy + 25 * s, cx + (dx + 5) * s, cy + 35 * s],
                  fill=(200, 200, 200))


def obj_trofeo(d, cx, cy, s=1.0, color=(250, 210, 60), t=0.0):
    d.ellipse([cx - 22 * s, cy - 36 * s, cx + 22 * s, cy + 4 * s], fill=color,
              outline=(200, 150, 20), width=max(1, int(2 * s)))
    d.arc([cx - 40 * s, cy - 36 * s, cx - 12 * s, cy - 4 * s], start=90, end=270,
          fill=color, width=max(2, int(5 * s)))
    d.arc([cx + 12 * s, cy - 36 * s, cx + 40 * s, cy - 4 * s], start=270, end=90,
          fill=color, width=max(2, int(5 * s)))
    d.rectangle([cx - 5 * s, cy + 4 * s, cx + 5 * s, cy + 26 * s], fill=color)
    _r(d, cx, cy + 36, 44, 12, s, (180, 130, 40), radius=2)


def obj_sol(d, cx, cy, s=1.0, color=(250, 200, 40), t=0.0):
    for i in range(8):
        ang = math.radians(i * 45)
        x0, y0 = cx + 30 * s * math.cos(ang), cy + 30 * s * math.sin(ang)
        x1, y1 = cx + 44 * s * math.cos(ang), cy + 44 * s * math.sin(ang)
        d.line([x0, y0, x1, y1], fill=color, width=max(2, int(5 * s)))
    d.ellipse([cx - 26 * s, cy - 26 * s, cx + 26 * s, cy + 26 * s], fill=color,
              outline=(220, 160, 20), width=max(1, int(2 * s)))
    d.ellipse([cx - 12 * s, cy - 14 * s, cx + 2 * s, cy - 2 * s], fill=(255, 255, 255))
    d.arc([cx - 12 * s, cy - 2 * s, cx + 12 * s, cy + 16 * s], start=10, end=170,
          fill=(180, 120, 20), width=max(2, int(3 * s)))


def obj_nube(d, cx, cy, s=1.0, color=(245, 245, 250), t=0.0):
    for dx, dy, r in [(-22, 6, 18), (0, -8, 24), (24, 6, 18)]:
        d.ellipse([cx + (dx - r) * s, cy + (dy - r) * s, cx + (dx + r) * s, cy + (dy + r) * s],
                  fill=color)
    d.rectangle([cx - 38 * s, cy + 2 * s, cx + 38 * s, cy + 18 * s], fill=color)


def obj_lluvia(d, cx, cy, s=1.0, color=(120, 170, 230), t=0.0):
    obj_nube(d, cx, cy - 18, s=0.8 * s, color=(240, 240, 245))
    for dx in (-24, 0, 24):
        p = (t * 30 + dx) % 20
        d.line([cx + dx * s, cy + 12 * s + p, cx + (dx - 6) * s, cy + 28 * s + p],
               fill=color, width=max(2, int(4 * s)))


def obj_cohete(d, cx, cy, s=1.0, color=(230, 230, 240), t=0.0):
    d.polygon([(cx, cy - 48 * s), (cx - 16 * s, cy - 10 * s), (cx + 16 * s, cy - 10 * s)],
              fill=(220, 60, 60))
    _r(d, cx, cy + 8, 32, 44, s, color, outline=(150, 150, 160), radius=10)
    d.ellipse([cx - 9 * s, cy - 10 * s, cx + 9 * s, cy + 8 * s], fill=(120, 200, 250),
              outline=(60, 100, 140), width=max(1, int(2 * s)))
    d.polygon([(cx - 16 * s, cy + 14 * s), (cx - 30 * s, cy + 36 * s), (cx - 16 * s, cy + 30 * s)],
              fill=(220, 60, 60))
    d.polygon([(cx + 16 * s, cy + 14 * s), (cx + 30 * s, cy + 36 * s), (cx + 16 * s, cy + 30 * s)],
              fill=(220, 60, 60))
    llama = 14 + 6 * math.sin(2 * math.pi * t / 0.4)
    d.polygon([(cx - 8 * s, cy + 30 * s), (cx + 8 * s, cy + 30 * s), (cx, cy + (30 + llama) * s)],
              fill=(255, 160, 40))


def obj_planeta(d, cx, cy, s=1.0, color=(200, 140, 80), t=0.0):
    d.ellipse([cx - 34 * s, cy - 34 * s, cx + 34 * s, cy + 34 * s], fill=color)
    d.arc([cx - 34 * s, cy - 12 * s, cx + 34 * s, cy + 12 * s], start=0, end=180,
          fill=(160, 100, 50), width=max(2, int(4 * s)))
    d.arc([cx - 34 * s, cy + 2 * s, cx + 34 * s, cy + 26 * s], start=0, end=180,
          fill=(160, 100, 50), width=max(2, int(4 * s)))
    d.ellipse([cx - 48 * s, cy - 8 * s, cx + 48 * s, cy + 8 * s], outline=(230, 200, 140),
              width=max(2, int(4 * s)))
    d.ellipse([cx + 12 * s, cy + 8 * s, cx + 26 * s, cy + 20 * s], fill=(180, 60, 60))


def obj_microscopio(d, cx, cy, s=1.0, color=(90, 90, 110), t=0.0):
    d.line([cx - 14 * s, cy - 34 * s, cx + 14 * s, cy - 6 * s], fill=color, width=max(3, int(8 * s)))
    d.ellipse([cx + 10 * s, cy - 18 * s, cx + 26 * s, cy - 2 * s], fill=(120, 200, 250),
              outline=color, width=max(1, int(2 * s)))
    d.ellipse([cx - 22 * s, cy - 42 * s, cx - 6 * s, cy - 30 * s], fill=color)
    _r(d, cx, cy + 22, 40, 26, s, (180, 180, 190), radius=4)
    d.line([cx - 4 * s, cy + 2 * s, cx - 4 * s, cy + 12 * s], fill=color, width=max(2, int(5 * s)))
    _r(d, cx - 22, cy + 40, 44, 8, s, color, radius=2)


def obj_adn(d, cx, cy, s=1.0, color=(70, 130, 200), t=0.0):
    for i in range(6):
        yy = cy + (i - 2.5) * 14 * s
        off = 14 * math.sin(i * 1.1)
        d.ellipse([cx - 20 * s + off, yy - 6 * s, cx - 8 * s + off, yy + 6 * s], fill=color)
        d.ellipse([cx + 8 * s - off, yy - 6 * s, cx + 20 * s - off, yy + 6 * s], fill=(255, 120, 120))
        if i % 2 == 0:
            d.line([cx - 14 * s + off, yy, cx + 14 * s - off, yy], fill=(120, 120, 120),
                   width=max(1, int(2 * s)))


def obj_foco(d, cx, cy, s=1.0, color=(250, 210, 60), t=0.0):
    d.ellipse([cx - 26 * s, cy - 34 * s, cx + 26 * s, cy + 18 * s], fill=color,
              outline=(200, 150, 20), width=max(1, int(2 * s)))
    d.arc([cx - 12 * s, cy - 20 * s, cx + 12 * s, cy + 4 * s], start=200, end=340,
          fill=(255, 255, 255), width=max(2, int(3 * s)))
    _r(d, cx, cy + 28, 22, 12, s, (150, 150, 160), radius=2)
    _r(d, cx, cy + 42, 14, 8, s, (150, 150, 160), radius=2)
    for i in range(5):
        ang = math.radians(-90 + (i - 2) * 36)
        d.line([cx + 32 * s * math.cos(ang), cy - 8 * s + 32 * s * math.sin(ang),
                cx + 42 * s * math.cos(ang), cy - 8 * s + 42 * s * math.sin(ang)],
               fill=color, width=max(2, int(3 * s)))


def obj_reloj(d, cx, cy, s=1.0, color=(245, 245, 245), t=0.0):
    d.ellipse([cx - 34 * s, cy - 34 * s, cx + 34 * s, cy + 34 * s], fill=color,
              outline=BLACK, width=max(2, int(3 * s)))
    for i in range(12):
        ang = math.radians(i * 30)
        d.line([cx + 28 * s * math.cos(ang), cy + 28 * s * math.sin(ang),
                cx + 31 * s * math.cos(ang), cy + 31 * s * math.sin(ang)],
               fill=BLACK, width=max(1, int(2 * s)))
    d.line([cx, cy, cx, cy - 20 * s], fill=BLACK, width=max(2, int(4 * s)))
    d.line([cx, cy, cx + 14 * s, cy + 8 * s], fill=BLACK, width=max(2, int(4 * s)))
    d.ellipse([cx - 4 * s, cy - 4 * s, cx + 4 * s, cy + 4 * s], fill=(220, 60, 60))


def obj_calendario(d, cx, cy, s=1.0, color=(255, 255, 255), t=0.0):
    _r(d, cx, cy, 80, 76, s, color, outline=BLACK, radius=6)
    _r(d, cx, cy - 26, 80, 24, s, (220, 60, 60), radius=6)
    for dx in (-22, 22):
        d.rectangle([cx + (dx - 4) * s, cy - 46 * s, cx + (dx + 4) * s, cy - 28 * s],
                    fill=(60, 60, 60))
    for fila in range(2):
        for col in range(4):
            d.rectangle([cx + (-30 + col * 16) * s, cy + (-8 + fila * 16) * s,
                         cx + (-20 + col * 16) * s, cy + (2 + fila * 16) * s],
                        fill=(200, 200, 210))
    d.rectangle([cx + 14 * s, cy + 8 * s, cx + 28 * s, cy + 22 * s], fill=(220, 60, 60))


def obj_martillo(d, cx, cy, s=1.0, color=(150, 150, 160), t=0.0):
    d.line([cx - 20 * s, cy + 36 * s, cx + 10 * s, cy - 26 * s], fill=(150, 110, 60),
           width=max(3, int(8 * s)))
    d.line([cx - 8 * s, cy - 34 * s, cx + 30 * s, cy - 14 * s], fill=color, width=max(4, int(14 * s)))
    d.line([cx + 26 * s, cy - 16 * s, cx + 34 * s, cy - 4 * s], fill=color, width=max(3, int(8 * s)))


def obj_estetoscopio(d, cx, cy, s=1.0, color=(50, 50, 60), t=0.0):
    d.arc([cx - 26 * s, cy - 30 * s, cx + 26 * s, cy + 30 * s], start=0, end=270,
          fill=color, width=max(3, int(6 * s)))
    d.ellipse([cx - 32 * s, cy - 36 * s, cx - 20 * s, cy - 24 * s], fill=color)
    d.ellipse([cx + 20 * s, cy + 20 * s, cx + 36 * s, cy + 36 * s], fill=color)
    d.ellipse([cx + 24 * s, cy + 24 * s, cx + 32 * s, cy + 32 * s], fill=(200, 200, 210))


def obj_manzana(d, cx, cy, s=1.0, color=(220, 50, 50), t=0.0):
    d.ellipse([cx - 26 * s, cy - 18 * s, cx + 2 * s, cy + 30 * s], fill=color)
    d.ellipse([cx - 2 * s, cy - 18 * s, cx + 26 * s, cy + 30 * s], fill=color)
    d.line([cx, cy - 18 * s, cx + 6 * s, cy - 34 * s], fill=(120, 90, 40), width=max(2, int(4 * s)))
    d.ellipse([cx + 4 * s, cy - 36 * s, cx + 26 * s, cy - 22 * s], fill=(90, 170, 90))
    d.arc([cx - 18 * s, cy - 10 * s, cx + 2 * s, cy + 14 * s], start=180, end=300,
          fill=(255, 255, 255, 160), width=max(2, int(3 * s)))


def obj_comida(d, cx, cy, s=1.0, color=(245, 245, 245), t=0.0):
    d.ellipse([cx - 40 * s, cy - 14 * s, cx + 40 * s, cy + 26 * s], fill=color,
              outline=(180, 180, 190), width=max(1, int(2 * s)))
    d.ellipse([cx - 26 * s, cy - 8 * s, cx + 26 * s, cy + 14 * s], fill=(250, 220, 160))
    for dx, dy in [(-12, -2), (4, 2), (12, -4)]:
        d.ellipse([cx + (dx - 6) * s, cy + (dy - 5) * s, cx + (dx + 6) * s, cy + (dy + 5) * s],
                  fill=(90, 170, 90))
    d.ellipse([cx + 28 * s, cy - 22 * s, cx + 40 * s, cy - 10 * s], fill=(220, 60, 60))


def obj_regalo(d, cx, cy, s=1.0, color=(220, 60, 90), t=0.0):
    _r(d, cx, cy + 12, 72, 56, s, color, outline=(160, 30, 60), radius=4)
    _r(d, cx, cy - 26, 78, 18, s, tuple(max(0, c - 30) for c in color), radius=4)
    d.rectangle([cx - 7 * s, cy - 34 * s, cx + 7 * s, cy + 40 * s], fill=(250, 210, 60))
    d.ellipse([cx - 20 * s, cy - 48 * s, cx - 2 * s, cy - 30 * s], outline=(250, 210, 60),
              width=max(2, int(4 * s)))
    d.ellipse([cx + 2 * s, cy - 48 * s, cx + 20 * s, cy - 30 * s], outline=(250, 210, 60),
              width=max(2, int(4 * s)))


def obj_bandera(d, cx, cy, s=1.0, color=(60, 150, 220), t=0.0):
    d.line([cx - 20 * s, cy - 46 * s, cx - 20 * s, cy + 46 * s], fill=(120, 90, 40),
           width=max(2, int(5 * s)))
    ondeo = 4 * math.sin(2 * math.pi * t / 1.2)
    d.polygon([(cx - 20 * s, cy - 46 * s), (cx + 34 * s, cy - 40 * s + ondeo),
               (cx + 34 * s, cy - 10 * s + ondeo), (cx - 20 * s, cy - 16 * s)], fill=color)
    d.ellipse([cx + 8 * s, cy - 36 * s + ondeo, cx + 18 * s, cy - 26 * s + ondeo], fill=WHITE)


def obj_lapiz(d, cx, cy, s=1.0, color=(250, 200, 60), t=0.0):
    d.polygon([(cx - 34 * s, cy - 8 * s), (cx + 22 * s, cy - 8 * s),
               (cx + 36 * s, cy), (cx + 22 * s, cy + 8 * s), (cx - 34 * s, cy + 8 * s)],
              fill=color)
    d.polygon([(cx + 22 * s, cy - 8 * s), (cx + 36 * s, cy), (cx + 22 * s, cy + 8 * s)],
              fill=(245, 220, 180))
    d.polygon([(cx + 30 * s, cy - 4 * s), (cx + 36 * s, cy), (cx + 30 * s, cy + 4 * s)],
              fill=(60, 60, 70))
    d.rectangle([cx - 40 * s, cy - 8 * s, cx - 34 * s, cy + 8 * s], fill=(220, 100, 120))


def obj_mochila(d, cx, cy, s=1.0, color=(70, 130, 200), t=0.0):
    _r(d, cx, cy, 64, 76, s, color, outline=(40, 80, 140), radius=16)
    _r(d, cx, cy + 8, 44, 34, s, tuple(max(0, c - 30) for c in color), radius=10)
    d.arc([cx - 16 * s, cy - 48 * s, cx + 16 * s, cy - 20 * s], start=180, end=360,
          fill=(40, 80, 140), width=max(2, int(5 * s)))


def obj_flor(d, cx, cy, s=1.0, color=(255, 120, 160), t=0.0):
    d.line([cx, cy + 6 * s, cx, cy + 46 * s], fill=(70, 150, 70), width=max(2, int(5 * s)))
    d.ellipse([cx - 16 * s, cy + 22 * s, cx, cy + 34 * s], fill=(70, 150, 70))
    for i in range(6):
        ang = math.radians(i * 60)
        px, py = cx + 18 * s * math.cos(ang), cy - 12 * s + 18 * s * math.sin(ang)
        d.ellipse([px - 11 * s, py - 11 * s, px + 11 * s, py + 11 * s], fill=color)
    d.ellipse([cx - 10 * s, cy - 22 * s, cx + 10 * s, cy - 2 * s], fill=(250, 210, 60))


def obj_computadora(d, cx, cy, s=1.0, color=(60, 70, 90), t=0.0):
    _r(d, cx, cy - 12, 84, 56, s, color, outline=(30, 35, 45), radius=6)
    _r(d, cx, cy - 12, 72, 44, s, (140, 200, 250), radius=4)
    d.line([cx - 20 * s, cy + 20 * s, cx + 20 * s, cy + 20 * s], fill=(30, 35, 45),
           width=max(2, int(5 * s)))
    _r(d, cx, cy + 28, 52, 8, s, (30, 35, 45), radius=3)
    d.line([cx - 24 * s, cy - 24 * s, cx + 12 * s, cy - 24 * s], fill=(255, 255, 255),
           width=max(1, int(2 * s)))


def obj_gota(d, cx, cy, s=1.0, color=(90, 170, 250), t=0.0):
    d.polygon([(cx, cy - 40 * s), (cx - 22 * s, cy + 4 * s), (cx + 22 * s, cy + 4 * s)], fill=color)
    d.ellipse([cx - 22 * s, cy - 2 * s, cx + 22 * s, cy + 40 * s], fill=color)
    d.ellipse([cx - 14 * s, cy + 6 * s, cx - 2 * s, cy + 26 * s], fill=(255, 255, 255, 160))


OBJETOS = {
    "libro": obj_libro, "monedas": obj_monedas, "billetes": obj_billetes,
    "alcancia": obj_alcancia, "grafico": obj_grafico, "puerta": obj_puerta,
    "arbol": obj_arbol, "planta": obj_planta, "casa": obj_casa,
    "escuela": obj_escuela, "carro": obj_carro, "autobus": obj_autobus,
    "trofeo": obj_trofeo, "sol": obj_sol, "nube": obj_nube, "lluvia": obj_lluvia,
    "cohete": obj_cohete, "planeta": obj_planeta, "microscopio": obj_microscopio,
    "adn": obj_adn, "foco": obj_foco, "reloj": obj_reloj,
    "calendario": obj_calendario, "martillo": obj_martillo,
    "estetoscopio": obj_estetoscopio, "manzana": obj_manzana,
    "comida": obj_comida, "regalo": obj_regalo, "bandera": obj_bandera,
    "lapiz": obj_lapiz, "mochila": obj_mochila, "flor": obj_flor,
    "computadora": obj_computadora, "gota": obj_gota,
}


def dibujar_objeto(d, nombre, cx, cy, s=1.0, color=None, t=0.0):
    """Dibuja un objeto del catálogo centrado en (cx, cy)."""
    fn = OBJETOS.get(nombre)
    if fn is None:
        raise ValueError(f"Objeto desconocido: {nombre!r}. Ver OBJETOS en iconos.py.")
    if color is not None:
        fn(d, cx, cy, s=s, color=tuple(color), t=t)
    else:
        fn(d, cx, cy, s=s, t=t)
