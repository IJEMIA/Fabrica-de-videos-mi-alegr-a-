# -*- coding: utf-8 -*-
"""Personajes: hombre cartoon (estilo aprendiz) y sprites pixel art."""
import math
from PIL import Image, ImageDraw, ImageFont
from .core import (WHITE, BLACK, SKIN, SKIN_D, HAIR, PURPLE, PURPLE_D,
                   BLUE, BLUE_D, BROWN, font_hand, font_bold, font,
                   ease_out, ease_out_back, clamp, norm_rows, draw_map, blink)

# Paleta del cerebro pixel art
PINK = (255, 143, 171)
PINK_L = (255, 194, 212)
PINK_D = (205, 55, 115)
BRAIN_K = (122, 46, 90)
INK = (43, 43, 58)
WHEEL_COLORS = [(74, 222, 128), (255, 107, 157), (45, 212, 191),
                (251, 146, 60), (250, 204, 21), (167, 139, 250)]


def draw_person(d, x, feet_y, s=1.0, t=0.0, pose="stand", smile=False, walk_phase=0.0, float_y=0.0,
                camisa=None, pantalon=None, cabello=None):
    """Hombre cartoon: cabello castaño, camisa morada, pantalón azul, zapatos marrones.
    (x, feet_y) = centro de los pies. s = escala (altura ~ 380*s).
    camisa/pantalon/cabello permiten reutilizarlo con otros colores."""
    camisa = camisa or PURPLE
    camisa_d = tuple(max(0, c - 20) for c in camisa)
    pantalon = pantalon or BLUE
    cabello = cabello or HAIR
    bob = 3 * math.sin(2 * math.pi * t / 1.6) if pose in ("stand", "hold_lamp", "thumbs") else 0
    by = feet_y + bob + float_y
    bl = blink(t)
    # Piernas (pantalón azul)
    leg_w, leg_h = int(34 * s), int(150 * s)
    hip_y = by - leg_h
    if pose == "walk":
        off = int(26 * s * math.sin(walk_phase))
        d.rounded_rectangle([x - leg_w - 6 * s + off, hip_y, x - 6 * s + off, by - 8 * s],
                            radius=int(14 * s), fill=pantalon)
        d.rounded_rectangle([x + 6 * s - off, hip_y, x + leg_w + 6 * s - off, by - 8 * s],
                            radius=int(14 * s), fill=pantalon)
    else:
        d.rounded_rectangle([x - leg_w - 6 * s, hip_y, x - 6 * s, by - 8 * s],
                            radius=int(14 * s), fill=pantalon)
        d.rounded_rectangle([x + 6 * s, hip_y, x + leg_w + 6 * s, by - 8 * s],
                            radius=int(14 * s), fill=pantalon)
    # Zapatos marrones
    shoe_h, shoe_w = int(26 * s), int(52 * s)
    d.ellipse([x - leg_w - 14 * s, by - shoe_h, x + 4 * s, by], fill=BROWN)
    d.ellipse([x - 4 * s, by - shoe_h, x + leg_w + 14 * s, by], fill=BROWN)
    # Camisa morada
    sh_y = hip_y - int(150 * s)
    d.rounded_rectangle([x - int(62 * s), sh_y, x + int(62 * s), hip_y + int(10 * s)],
                        radius=int(26 * s), fill=camisa)
    d.rounded_rectangle([x - int(62 * s), sh_y, x + int(62 * s), sh_y + int(18 * s)],
                        radius=int(9 * s), fill=camisa_d)
    # Brazos
    arm_w = int(26 * s)
    if pose == "thumbs":
        # brazo derecho levantado con pulgar
        d.rounded_rectangle([x + int(52 * s), sh_y + int(10 * s), x + int(78 * s), sh_y + int(110 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x + int(48 * s), sh_y - int(28 * s), x + int(84 * s), sh_y + int(8 * s)], fill=SKIN)
        d.rounded_rectangle([x + int(58 * s), sh_y - int(48 * s), x + int(74 * s), sh_y - int(22 * s)],
                            radius=int(6 * s), fill=SKIN)  # pulgar
        d.rounded_rectangle([x - int(78 * s), sh_y + int(10 * s), x - int(52 * s), sh_y + int(150 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x - int(78 * s), sh_y + int(140 * s), x - int(52 * s), sh_y + int(166 * s)], fill=SKIN)
    elif pose == "hold_lamp":
        d.rounded_rectangle([x + int(52 * s), sh_y + int(10 * s), x + int(78 * s), sh_y + int(120 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x + int(48 * s), sh_y - int(10 * s), x + int(84 * s), sh_y + int(26 * s)], fill=SKIN)
        d.rounded_rectangle([x - int(78 * s), sh_y + int(10 * s), x - int(52 * s), sh_y + int(150 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x - int(78 * s), sh_y + int(140 * s), x - int(52 * s), sh_y + int(166 * s)], fill=SKIN)
    elif pose == "point":
        d.rounded_rectangle([x + int(52 * s), sh_y + int(40 * s), x + int(140 * s), sh_y + int(66 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x + int(128 * s), sh_y + int(38 * s), x + int(156 * s), sh_y + int(66 * s)], fill=SKIN)
        d.rounded_rectangle([x - int(78 * s), sh_y + int(10 * s), x - int(52 * s), sh_y + int(150 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x - int(78 * s), sh_y + int(140 * s), x - int(52 * s), sh_y + int(166 * s)], fill=SKIN)
    elif pose == "telescope":
        # brazo derecho extendido hacia el telescopio (a la derecha, arriba)
        d.rounded_rectangle([x + int(52 * s), sh_y + int(20 * s), x + int(120 * s), sh_y + int(46 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x + int(110 * s), sh_y + int(18 * s), x + int(138 * s), sh_y + int(46 * s)], fill=SKIN)
        d.rounded_rectangle([x - int(78 * s), sh_y + int(10 * s), x - int(52 * s), sh_y + int(150 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x - int(78 * s), sh_y + int(140 * s), x - int(52 * s), sh_y + int(166 * s)], fill=SKIN)
    elif pose == "shield":
        # brazo izquierdo levantado sosteniendo el paraguas/escudo
        d.rounded_rectangle([x - int(78 * s), sh_y - int(30 * s), x - int(52 * s), sh_y + int(90 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x - int(78 * s), sh_y - int(56 * s), x - int(52 * s), sh_y - int(30 * s)], fill=SKIN)
        d.rounded_rectangle([x + int(52 * s), sh_y + int(10 * s), x + int(78 * s), sh_y + int(150 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x + int(52 * s), sh_y + int(140 * s), x + int(78 * s), sh_y + int(166 * s)], fill=SKIN)
    elif pose == "float":
        # brazos abiertos hacia arriba, flotando
        d.rounded_rectangle([x - int(96 * s), sh_y - int(10 * s), x - int(60 * s), sh_y + int(110 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x - int(100 * s), sh_y - int(36 * s), x - int(56 * s), sh_y], fill=SKIN)
        d.rounded_rectangle([x + int(60 * s), sh_y - int(10 * s), x + int(96 * s), sh_y + int(110 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x + int(56 * s), sh_y - int(36 * s), x + int(100 * s), sh_y], fill=SKIN)
    else:  # stand / walk: brazos a los lados, leve balanceo
        sw = 4 * math.sin(2 * math.pi * t / 1.6 + 1.2) if pose == "walk" else 2 * math.sin(2 * math.pi * t / 1.6)
        d.rounded_rectangle([x - int(78 * s) + sw, sh_y + int(10 * s), x - int(52 * s) + sw, sh_y + int(150 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x - int(78 * s) + sw, sh_y + int(140 * s), x - int(52 * s) + sw, sh_y + int(166 * s)], fill=SKIN)
        d.rounded_rectangle([x + int(52 * s) - sw, sh_y + int(10 * s), x + int(78 * s) - sw, sh_y + int(150 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x + int(52 * s) - sw, sh_y + int(140 * s), x + int(78 * s) - sw, sh_y + int(166 * s)], fill=SKIN)
    # Cabeza
    hr = int(56 * s)
    hy = sh_y - hr - int(6 * s)
    d.ellipse([x - hr, hy - hr, x + hr, hy + hr], fill=SKIN)
    # Cabello castaño (casquete + mechón)
    d.pieslice([x - hr, hy - hr, x + hr, hy + hr], start=180, end=360, fill=cabello)
    d.ellipse([x - hr, hy - hr - int(8 * s), x - int(10 * s), hy - int(2 * s)], fill=cabello)
    d.ellipse([x + int(20 * s), hy - hr - int(14 * s), x + hr, hy - int(10 * s)], fill=cabello)
    # Ojos
    ex, ey, er = int(22 * s), hy - int(6 * s), int(9 * s)
    if bl:
        d.line([x - ex - er, ey, x - ex + er, ey], fill=BLACK, width=int(4 * s))
        d.line([x + ex - er, ey, x + ex + er, ey], fill=BLACK, width=int(4 * s))
    else:
        d.ellipse([x - ex - er, ey - er, x - ex + er, ey + er], fill=(255, 255, 255))
        d.ellipse([x + ex - er, ey - er, x + ex + er, ey + er], fill=(255, 255, 255))
        d.ellipse([x - ex - 4 * s, ey - 4 * s, x - ex + 4 * s, ey + 4 * s], fill=BLACK)
        d.ellipse([x + ex - 4 * s, ey - 4 * s, x + ex + 4 * s, ey + 4 * s], fill=BLACK)
    # Cejas preocupadas (ángulos hacia arriba al centro) o normales si sonríe
    bw = int(16 * s)
    if smile:
        d.line([x - ex - bw, ey - int(20 * s), x - ex + bw, ey - int(24 * s)], fill=cabello, width=int(5 * s))
        d.line([x + ex - bw, ey - int(24 * s), x + ex + bw, ey - int(20 * s)], fill=cabello, width=int(5 * s))
    else:
        d.line([x - ex - bw, ey - int(26 * s), x - ex + bw, ey - int(16 * s)], fill=cabello, width=int(5 * s))
        d.line([x + ex - bw, ey - int(16 * s), x + ex + bw, ey - int(26 * s)], fill=cabello, width=int(5 * s))
    # Boca
    my = hy + int(28 * s)
    if smile:
        d.arc([x - int(18 * s), my - int(6 * s), x + int(18 * s), my + int(18 * s)],
              start=0, end=180, fill=BLACK, width=int(4 * s))
    else:
        d.arc([x - int(14 * s), my, x + int(14 * s), my + int(16 * s)],
              start=180, end=360, fill=BLACK, width=int(4 * s))


BRAIN_ROWS = [
    "........KKKKKKKKKKKKKKKK........",
    "......KKPPPPPPPPPPPPPPPPKK......",
    "....KKPPPPPPPPPPPPPPPPPPPPKK....",
    "...KPPPPPPPPPPPPPPPPPPPPPPPPK...",
    "..KPPPPDDPPPPPPPPPPPPDDDDPPPPK..",
    "..KPPDDDDPPPPPPPPPPPPPPDDDDPPK..",
    "..KPPPPPPPPPPPPPPPPPPPPPPPPPPK..",
    "..KPPPPPPDDPPPPPPPPPPDDPPPPPPK..",
    "..KPPPPPPPPPPPPPPPPPPPPPPPPPPK..",
    "..KPPDDPPPPPPPPPPPPPPPPDDPPPK...",
    "...KPPPPPPPPPPPPPPPPPPPPPPPPK...",
    "...KPPPPPPPWWEPPPPPPPPWWEPPPK...",
    "....KPPPPPPPPPPPPPPPPPPPPPPK....",
    ".....KKPPPPPPPPPPPPPPPPPPKK.....",
    ".......KKKKKKKKKKKKKKKKKK.......",
]


BRAIN_PAL = {'K': BRAIN_K, 'P': PINK, 'p': PINK_L, 'D': PINK_D,
             'W': WHITE, 'E': INK}


ARM_ROWS = ["KPK", "KPK", "KPK", "KPK", "KKK"]


ARM_PAL = {'K': BRAIN_K, 'P': PINK}


def brain_img(scale=8, blink=False):
    rows = [r for r in BRAIN_ROWS]
    if blink:
        # ojos cerrados: líneas oscuras en vez de W/E
        rows[11] = rows[11].replace("WWE", "KKK").replace("WWE", "KKK")
    wpx, hpx = len(rows[0]) * scale, len(rows) * scale
    img = Image.new("RGBA", (wpx + 40, hpx + 30), (0, 0, 0, 0))
    draw_map(img, rows, BRAIN_PAL, 20, 8, scale)
    # brillos
    d = ImageDraw.Draw(img)
    d.rectangle([20 + 6 * scale, 8 + 2 * scale, 20 + 8 * scale, 8 + 3 * scale], fill=PINK_L)
    d.rectangle([20 + 22 * scale, 8 + 3 * scale, 20 + 24 * scale, 8 + 4 * scale], fill=PINK_L)
    return img


def arm_img(scale=8):
    img = Image.new("RGBA", (3 * scale, 5 * scale), (0, 0, 0, 0))
    draw_map(img, ARM_ROWS, ARM_PAL, 0, 0, scale)
    return img


def wheel_img(diameter=300, angle_deg=0, suave=False):
    s = 90  # lienzo pequeño para bordes pixelados
    tiny = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(tiny)
    cx = cy = s // 2
    r = s // 2 - 2
    for i, col in enumerate(WHEEL_COLORS):
        d.pieslice([cx - r, cy - r, cx + r, cy + r],
                   start=-90 + i * 60, end=-90 + (i + 1) * 60, fill=col + (255,))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK + (255,), width=3)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(212, 175, 55, 255),
              outline=INK + (255,), width=2)
    # brillos
    d.arc([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6], start=200, end=330,
          fill=(255, 255, 255, 160), width=3)
    if suave:
        tiny = tiny.rotate(angle_deg, resample=Image.BICUBIC, center=(cx, cy))
        return tiny.resize((diameter, diameter), Image.BICUBIC)
    tiny = tiny.rotate(angle_deg, resample=Image.NEAREST, center=(cx, cy))
    return tiny.resize((diameter, diameter), Image.NEAREST)


def person_img(hair=(60, 40, 20), shirt=(70, 130, 200), pants=(50, 50, 90),
               skin=SKIN, blink=False, scale=6, paso=0, vestido=False,
               pelo_largo=False, sombrero=None, barba=False, bata=False):
    """Persona pixel art 20x28. paso=0/1 alterna las piernas (caminata de 2 fotogramas,
    como los sprites de plataformas de SNES). vestido: falda en vez de pantalón.
    sombrero: 'casco' (amarillo), 'casco_rojo', 'gorra' (azul), 'sombrero' (paja).
    barba: barba blanca (anciano). bata: bata blanca de científico/doctora."""
    wpx, hpx = 20 * scale, 28 * scale
    img = Image.new("RGBA", (wpx, hpx), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    S = scale
    # piernas (el paso desplaza una pierna hacia adelante y la otra hacia atrás)
    off = S if paso else 0
    if vestido:
        # falda: trapecio en vez de piernas
        d.polygon([(4 * S, 19 * S), (16 * S, 19 * S), (18 * S, 26 * S), (2 * S, 26 * S)],
                  fill=tuple(max(0, c - 10) for c in shirt))
        d.rectangle([5 * S, 26 * S, 9 * S - 1, 27 * S - 1], fill=(30, 30, 40))
        d.rectangle([10 * S, 26 * S, 14 * S - 1, 27 * S - 1], fill=(30, 30, 40))
    else:
        d.rectangle([6 * S, 19 * S, 8 * S - 1, 26 * S - 1], fill=pants)
        d.rectangle([11 * S, 19 * S, 13 * S - 1, 26 * S - 1], fill=pants)
        # zapatos
        d.rectangle([5 * S - off, 26 * S, 9 * S - 1 - off, 27 * S - 1], fill=(30, 30, 40))
        d.rectangle([10 * S + off, 26 * S, 14 * S - 1 + off, 27 * S - 1], fill=(30, 30, 40))
    # torso (camisa con sombra)
    d.rectangle([4 * S, 11 * S, 15 * S - 1, 19 * S - 1], fill=shirt)
    d.rectangle([13 * S, 11 * S, 15 * S - 1, 19 * S - 1], fill=tuple(max(0, c - 30) for c in shirt))
    if bata:
        # bata blanca abierta sobre la camisa
        d.rectangle([4 * S, 11 * S, 7 * S - 1, 19 * S - 1], fill=(240, 240, 240))
        d.rectangle([12 * S, 11 * S, 15 * S - 1, 19 * S - 1], fill=(240, 240, 240))
    # brazos
    d.rectangle([2 * S, 12 * S, 3 * S - 1, 18 * S - 1], fill=shirt)
    d.rectangle([16 * S, 12 * S, 17 * S - 1, 18 * S - 1], fill=shirt)
    d.rectangle([2 * S, 18 * S, 3 * S - 1, 19 * S - 1], fill=skin)
    d.rectangle([16 * S, 18 * S, 17 * S - 1, 19 * S - 1], fill=skin)
    # cuello
    d.rectangle([8 * S, 10 * S, 11 * S - 1, 11 * S - 1], fill=SKIN_D)
    # cabeza
    d.rectangle([6 * S, 2 * S, 13 * S - 1, 10 * S - 1], fill=skin)
    # pelo
    d.rectangle([6 * S, 1 * S, 13 * S - 1, 3 * S - 1], fill=hair)
    d.rectangle([5 * S, 2 * S, 6 * S - 1, 5 * S - 1], fill=hair)
    d.rectangle([13 * S, 2 * S, 14 * S - 1, 5 * S - 1], fill=hair)
    if pelo_largo:
        d.rectangle([4 * S, 2 * S, 5 * S - 1, 12 * S - 1], fill=hair)
        d.rectangle([14 * S, 2 * S, 15 * S - 1, 12 * S - 1], fill=hair)
    if sombrero == "casco":
        d.rectangle([5 * S, 0, 14 * S - 1, 2 * S - 1], fill=(250, 200, 40))
        d.rectangle([4 * S, 2 * S, 15 * S - 1, 3 * S - 1], fill=(250, 200, 40))
    elif sombrero == "casco_rojo":
        d.rectangle([5 * S, 0, 14 * S - 1, 2 * S - 1], fill=(200, 40, 40))
        d.rectangle([4 * S, 2 * S, 15 * S - 1, 3 * S - 1], fill=(200, 40, 40))
    elif sombrero == "gorra":
        d.rectangle([5 * S, 0, 14 * S - 1, 2 * S - 1], fill=(40, 60, 120))
        d.rectangle([4 * S, 2 * S, 15 * S - 1, 3 * S - 1], fill=(40, 60, 120))
    elif sombrero == "sombrero":
        d.rectangle([3 * S, 2 * S, 16 * S - 1, 3 * S - 1], fill=(230, 200, 120))
        d.rectangle([7 * S, 0, 12 * S - 1, 2 * S - 1], fill=(210, 175, 90))
    # ojos
    if blink:
        d.rectangle([7 * S, 6 * S, 9 * S - 1, 6 * S], fill=INK)
        d.rectangle([11 * S, 6 * S, 13 * S - 1, 6 * S], fill=INK)
    else:
        d.rectangle([7 * S, 6 * S, 8 * S - 1, 7 * S - 1], fill=INK)
        d.rectangle([11 * S, 6 * S, 12 * S - 1, 7 * S - 1], fill=INK)
    # boca
    d.rectangle([9 * S, 8 * S, 10 * S - 1, 8 * S], fill=INK)
    # barba blanca
    if barba:
        d.rectangle([6 * S, 8 * S, 13 * S - 1, 10 * S - 1], fill=(230, 230, 230))
    return img


# Variantes pixel art por tipo (para los sprites snes/nes).
PERSONAJE_PIXEL = {
    "hombre": dict(),
    "mujer": dict(hair=(60, 40, 20), shirt=(214, 90, 130), pants=(90, 60, 120),
                  vestido=True, pelo_largo=True),
    "nino": dict(hair=(60, 40, 20), shirt=(70, 160, 90), pants=BLUE),
    "nina": dict(hair=(60, 40, 20), shirt=(250, 200, 60), pants=(200, 90, 130),
                 vestido=True, pelo_largo=True),
    "anciano": dict(hair=(225, 225, 225), shirt=(190, 175, 150), pants=(90, 85, 75),
                    barba=True),
    "anciana": dict(hair=(225, 225, 225), shirt=(150, 110, 170), pants=(90, 85, 75),
                    vestido=True, pelo_largo=True),
    "maestro": dict(hair=(60, 40, 20), shirt=(240, 240, 240), pants=(60, 60, 80)),
    "estudiante": dict(hair=(60, 40, 20), shirt=(90, 160, 220), pants=BLUE),
    "cientifico": dict(hair=(60, 40, 20), shirt=(240, 240, 240), pants=(60, 60, 80),
                       bata=True),
    "doctora": dict(hair=(60, 40, 20), shirt=(240, 240, 240), pants=(60, 90, 110),
                    vestido=True, pelo_largo=True, bata=True),
    "trabajador": dict(hair=(60, 40, 20), shirt=(240, 130, 40), pants=(70, 70, 90),
                       sombrero="casco"),
    "campesino": dict(hair=(60, 40, 20), shirt=(90, 150, 70), pants=(120, 90, 60),
                      sombrero="sombrero"),
    "deportista": dict(hair=(60, 40, 20), shirt=(220, 60, 60), pants=(40, 60, 140)),
    "policia": dict(hair=(60, 40, 20), shirt=(40, 60, 120), pants=(30, 45, 90),
                    sombrero="gorra"),
    "bombero": dict(hair=(60, 40, 20), shirt=(180, 40, 40), pants=(60, 55, 55),
                    sombrero="casco_rojo"),
    "vendedor": dict(hair=(60, 40, 20), shirt=(70, 160, 90), pants=(70, 70, 90)),
}


def personaje_pixel(tipo, scale=2, blink=False, paso=0):
    """Sprite pixel art de un tipo de personaje (ver PERSONAJE_PIXEL)."""
    params = PERSONAJE_PIXEL.get(tipo, PERSONAJE_PIXEL["hombre"])
    return person_img(scale=scale, blink=blink, paso=paso, **params)
    # torso (camisa con sombra)
    d.rectangle([4 * S, 11 * S, 15 * S - 1, 19 * S - 1], fill=shirt)
    d.rectangle([13 * S, 11 * S, 15 * S - 1, 19 * S - 1], fill=tuple(max(0, c - 30) for c in shirt))
    # brazos
    d.rectangle([2 * S, 12 * S, 3 * S - 1, 18 * S - 1], fill=shirt)
    d.rectangle([16 * S, 12 * S, 17 * S - 1, 18 * S - 1], fill=shirt)
    d.rectangle([2 * S, 18 * S, 3 * S - 1, 19 * S - 1], fill=skin)
    d.rectangle([16 * S, 18 * S, 17 * S - 1, 19 * S - 1], fill=skin)
    # cuello
    d.rectangle([8 * S, 10 * S, 11 * S - 1, 11 * S - 1], fill=SKIN_D)
    # cabeza
    d.rectangle([6 * S, 2 * S, 13 * S - 1, 10 * S - 1], fill=skin)
    # pelo
    d.rectangle([6 * S, 1 * S, 13 * S - 1, 3 * S - 1], fill=hair)
    d.rectangle([5 * S, 2 * S, 6 * S - 1, 5 * S - 1], fill=hair)
    d.rectangle([13 * S, 2 * S, 14 * S - 1, 5 * S - 1], fill=hair)
    # ojos
    if blink:
        d.rectangle([7 * S, 6 * S, 9 * S - 1, 6 * S], fill=INK)
        d.rectangle([11 * S, 6 * S, 13 * S - 1, 6 * S], fill=INK)
    else:
        d.rectangle([7 * S, 6 * S, 8 * S - 1, 7 * S - 1], fill=INK)
        d.rectangle([11 * S, 6 * S, 12 * S - 1, 7 * S - 1], fill=INK)
    # boca
    d.rectangle([9 * S, 8 * S, 10 * S - 1, 8 * S], fill=INK)
    return img


# ---------------------------------------------------------------------------
# Personajes ampliados (estilo aprendiz, formas suaves)
# ---------------------------------------------------------------------------
# Tipos disponibles (ver catalogo.py). Cada tipo define pelo, ropa y
# accesorios por defecto; todo se puede cambiar con los parámetros.
TIPOS_PERSONAJE = {
    "hombre":     dict(pelo="corto",  camisa=PURPLE,      pantalon=BLUE,   piel=SKIN),
    "mujer":      dict(pelo="largo",  camisa=(214, 90, 130), pantalon=(90, 60, 120), piel=SKIN, falda=True),
    "nino":       dict(pelo="corto",  camisa=(70, 160, 90),  pantalon=BLUE, piel=SKIN, escala=0.72),
    "nina":       dict(pelo="coletas", camisa=(250, 200, 60), pantalon=(200, 90, 130), piel=SKIN, escala=0.72, falda=True),
    "anciano":    dict(pelo="canas",  camisa=(190, 175, 150), pantalon=(90, 85, 75), piel=SKIN, barba=True, baston=True),
    "anciana":    dict(pelo="mono",   camisa=(150, 110, 170), pantalon=(90, 85, 75), piel=SKIN, baston=True, falda=True),
    "maestro":    dict(pelo="corto",  camisa=(240, 240, 240), pantalon=(60, 60, 80), piel=SKIN, libro=True, corbata=True),
    "estudiante": dict(pelo="corto",  camisa=(90, 160, 220), pantalon=BLUE, piel=SKIN, mochila=True),
    "cientifico": dict(pelo="corto",  camisa=(240, 240, 240), pantalon=(60, 60, 80), piel=SKIN, bata=True, gafas=True),
    "doctora":    dict(pelo="mono",   camisa=(240, 240, 240), pantalon=(60, 90, 110), piel=SKIN, bata=True, estetoscopio=True),
    "trabajador": dict(pelo="casco",  camisa=(240, 130, 40), pantalon=(70, 70, 90), piel=SKIN, chaleco=True),
    "campesino":  dict(pelo="sombrero", camisa=(90, 150, 70), pantalon=(120, 90, 60), piel=SKIN),
    "deportista": dict(pelo="corto",  camisa=(220, 60, 60), pantalon=(40, 60, 140), piel=SKIN, numero="10"),
    "policia":    dict(pelo="gorra",  camisa=(40, 60, 120), pantalon=(30, 45, 90), piel=SKIN, placa=True),
    "bombero":    dict(pelo="casco_rojo", camisa=(180, 40, 40), pantalon=(60, 55, 55), piel=SKIN),
    "vendedor":   dict(pelo="corto",  camisa=(70, 160, 90), pantalon=(70, 70, 90), piel=SKIN, delantal=True),
}

EXPRESIONES = ("contento", "preocupado", "pensando", "sorprendido")
POSES = ("pie", "caminando", "senalando", "sentado", "saludando")


def _pelo(d, x, hy, hr, s, estilo, color):
    """Peinados. (x, hy) = centro de la cabeza, hr = radio."""
    if estilo == "corto":
        d.pieslice([x - hr, hy - hr, x + hr, hy + hr], start=180, end=360, fill=color)
        d.ellipse([x - hr, hy - hr - int(8 * s), x - int(10 * s), hy - int(2 * s)], fill=color)
        d.ellipse([x + int(20 * s), hy - hr - int(14 * s), x + hr, hy - int(10 * s)], fill=color)
    elif estilo == "largo":
        d.pieslice([x - hr, hy - hr, x + hr, hy + hr], start=180, end=360, fill=color)
        d.rounded_rectangle([x - hr - int(6 * s), hy - hr, x - hr + int(14 * s), hy + hr + int(60 * s)],
                            radius=int(10 * s), fill=color)
        d.rounded_rectangle([x + hr - int(14 * s), hy - hr, x + hr + int(6 * s), hy + hr + int(60 * s)],
                            radius=int(10 * s), fill=color)
    elif estilo == "coletas":
        d.pieslice([x - hr, hy - hr, x + hr, hy + hr], start=180, end=360, fill=color)
        for lado in (-1, 1):
            d.ellipse([x + lado * (hr + int(14 * s)) - int(16 * s), hy - hr,
                       x + lado * (hr + int(14 * s)) + int(16 * s), hy - hr + int(44 * s)],
                      fill=color)
            d.ellipse([x + lado * (hr + int(14 * s)) - int(6 * s), hy - hr - int(6 * s),
                       x + lado * (hr + int(14 * s)) + int(6 * s), hy - hr + int(6 * s)],
                      fill=(250, 100, 140))
    elif estilo == "mono":
        d.pieslice([x - hr, hy - hr, x + hr, hy + hr], start=180, end=360, fill=color)
        d.ellipse([x - int(18 * s), hy - hr - int(22 * s), x + int(18 * s), hy - hr + int(6 * s)],
                  fill=color)
    elif estilo == "canas":
        d.pieslice([x - hr, hy - hr, x + hr, hy + hr], start=180, end=360,
                   fill=(225, 225, 225))
    elif estilo == "rizado":
        for dx, dy in [(-30, -20), (0, -34), (30, -20)]:
            d.ellipse([x + dx * s - int(20 * s), hy + dy * s - int(20 * s),
                       x + dx * s + int(20 * s), hy + dy * s + int(20 * s)], fill=color)
    elif estilo == "casco":
        d.pieslice([x - hr - int(6 * s), hy - hr - int(10 * s),
                    x + hr + int(6 * s), hy + int(4 * s)], start=180, end=360,
                   fill=(250, 200, 40))
        d.rectangle([x - hr - int(6 * s), hy - int(14 * s),
                     x + hr + int(6 * s), hy - int(4 * s)], fill=(250, 200, 40))
    elif estilo == "casco_rojo":
        d.pieslice([x - hr - int(6 * s), hy - hr - int(10 * s),
                    x + hr + int(6 * s), hy + int(4 * s)], start=180, end=360,
                   fill=(200, 40, 40))
        d.rectangle([x - hr - int(6 * s), hy - int(14 * s),
                     x + hr + int(6 * s), hy - int(4 * s)], fill=(200, 40, 40))
        d.ellipse([x - int(10 * s), hy - hr - int(18 * s), x + int(10 * s),
                   hy - hr + int(2 * s)], fill=(200, 40, 40))
    elif estilo == "gorra":
        d.pieslice([x - hr, hy - hr, x + hr, hy + hr], start=180, end=360,
                   fill=(40, 60, 120))
        d.ellipse([x - hr - int(4 * s), hy - int(14 * s), x + hr + int(14 * s),
                   hy + int(2 * s)], fill=(40, 60, 120))
    elif estilo == "sombrero":
        d.ellipse([x - hr - int(26 * s), hy - int(16 * s), x + hr + int(26 * s),
                   hy + int(6 * s)], fill=(230, 200, 120))
        d.pieslice([x - hr + int(10 * s), hy - hr - int(6 * s),
                    x + hr - int(10 * s), hy + int(2 * s)], start=180, end=360,
                   fill=(210, 175, 90))


def dibujar_personaje(d, x, feet_y, s=1.0, t=0.0, tipo="hombre",
                      expresion="contento", pose="pie", camisa=None,
                      pantalon=None, pelo=None, piel=None, walk_phase=0.0):
    """Personaje cartoon parametrizable (estilo aprendiz).

    tipo: hombre, mujer, nino, nina, anciano, anciana, maestro, estudiante,
    cientifico, doctora, trabajador, campesino, deportista, policia,
    bombero, vendedor.
    expresion: contento, preocupado, pensando, sorprendido.
    pose: pie, caminando, senalando, sentado, saludando.
    camisa/pantalon/pelo/piel cambian los colores del tipo.
    (x, feet_y) = centro de los pies. Altura total ~ 380*s (adultos).
    """
    base = TIPOS_PERSONAJE.get(tipo, TIPOS_PERSONAJE["hombre"])
    s = s * base.get("escala", 1.0)
    camisa = camisa or base["camisa"]
    camisa_d = tuple(max(0, c - 20) for c in camisa)
    pantalon = pantalon or base["pantalon"]
    piel = piel or base["piel"]
    estilo_pelo = pelo or base["pelo"]
    bl = blink(t)
    bob = 3 * math.sin(2 * math.pi * t / 1.6) if pose in ("pie", "saludando") else 0
    by = feet_y + bob

    # --- piernas ---
    leg_w, leg_h = int(34 * s), int(150 * s)
    hip_y = by - leg_h
    if pose == "sentado":
        # cadera más baja, muslos horizontales hacia adelante, espinillas abajo
        hip_y = by - int(130 * s)
        d.rounded_rectangle([x - int(10 * s), hip_y, x + int(78 * s), hip_y + int(34 * s)],
                            radius=int(14 * s), fill=pantalon)
        d.rounded_rectangle([x + int(48 * s), hip_y + int(20 * s), x + int(78 * s), by - int(8 * s)],
                            radius=int(12 * s), fill=pantalon)
        d.ellipse([x + int(44 * s), by - int(26 * s), x + int(96 * s), by], fill=BROWN)
    elif pose == "caminando":
        off = int(26 * s * math.sin(walk_phase))
        d.rounded_rectangle([x - leg_w - 6 * s + off, hip_y, x - 6 * s + off, by - 8 * s],
                            radius=int(14 * s), fill=pantalon)
        d.rounded_rectangle([x + 6 * s - off, hip_y, x + leg_w + 6 * s - off, by - 8 * s],
                            radius=int(14 * s), fill=pantalon)
        d.ellipse([x - leg_w - 14 * s + off, by - int(26 * s), x + 4 * s + off, by], fill=BROWN)
        d.ellipse([x - 4 * s - off, by - int(26 * s), x + leg_w + 14 * s - off, by], fill=BROWN)
    else:
        d.rounded_rectangle([x - leg_w - 6 * s, hip_y, x - 6 * s, by - 8 * s],
                            radius=int(14 * s), fill=pantalon)
        d.rounded_rectangle([x + 6 * s, hip_y, x + leg_w + 6 * s, by - 8 * s],
                            radius=int(14 * s), fill=pantalon)
        d.ellipse([x - leg_w - 14 * s, by - int(26 * s), x + 4 * s, by], fill=BROWN)
        d.ellipse([x - 4 * s, by - int(26 * s), x + leg_w + 14 * s, by], fill=BROWN)
    # falda (mujer, niña, anciana)
    if base.get("falda"):
        d.polygon([(x - int(66 * s), hip_y + int(6 * s)),
                   (x + int(66 * s), hip_y + int(6 * s)),
                   (x + int(86 * s), hip_y + int(120 * s)),
                   (x - int(86 * s), hip_y + int(120 * s))],
                  fill=tuple(max(0, c - 10) for c in camisa))
    # --- torso ---
    sh_y = hip_y - int(150 * s)
    d.rounded_rectangle([x - int(62 * s), sh_y, x + int(62 * s), hip_y + int(10 * s)],
                        radius=int(26 * s), fill=camisa)
    d.rounded_rectangle([x - int(62 * s), sh_y, x + int(62 * s), sh_y + int(18 * s)],
                        radius=int(9 * s), fill=camisa_d)
    # número del deportista
    if base.get("numero"):
        f = font_bold(max(10, int(56 * s)))
        d.text((x, sh_y + int(75 * s)), base["numero"], font=f, fill=WHITE, anchor="mm")
    # bata blanca (científico, doctora)
    if base.get("bata"):
        d.rounded_rectangle([x - int(66 * s), sh_y, x + int(66 * s), hip_y + int(14 * s)],
                            radius=int(24 * s), outline=(230, 230, 230), width=max(2, int(6 * s)))
        d.line([x, sh_y + int(10 * s), x, hip_y], fill=(210, 210, 210), width=max(2, int(4 * s)))
    # chaleco (trabajador)
    if base.get("chaleco"):
        d.rectangle([x - int(62 * s), sh_y + int(20 * s), x + int(62 * s), sh_y + int(44 * s)],
                    fill=(240, 240, 240))
    # delantal (vendedor)
    if base.get("delantal"):
        d.rounded_rectangle([x - int(48 * s), sh_y + int(30 * s), x + int(48 * s), hip_y + int(8 * s)],
                            radius=int(12 * s), fill=(245, 245, 245))
    # corbata (maestro)
    if base.get("corbata"):
        d.polygon([(x - int(10 * s), sh_y + int(14 * s)), (x + int(10 * s), sh_y + int(14 * s)),
                   (x + int(6 * s), sh_y + int(80 * s)), (x - int(6 * s), sh_y + int(80 * s))],
                  fill=(180, 40, 40))
    # placa (policía)
    if base.get("placa"):
        d.ellipse([x - int(44 * s), sh_y + int(44 * s), x - int(20 * s), sh_y + int(68 * s)],
                  fill=(250, 210, 60))
    # --- brazos ---
    if pose == "senalando":
        d.rounded_rectangle([x + int(52 * s), sh_y + int(40 * s), x + int(140 * s), sh_y + int(66 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x + int(128 * s), sh_y + int(38 * s), x + int(156 * s), sh_y + int(66 * s)], fill=piel)
        d.rounded_rectangle([x - int(78 * s), sh_y + int(10 * s), x - int(52 * s), sh_y + int(150 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x - int(78 * s), sh_y + int(140 * s), x - int(52 * s), sh_y + int(166 * s)], fill=piel)
    elif pose == "saludando":
        onda = int(8 * s * math.sin(2 * math.pi * t / 0.7))
        d.rounded_rectangle([x + int(52 * s) + onda, sh_y - int(70 * s), x + int(78 * s) + onda, sh_y + int(60 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x + int(48 * s) + onda, sh_y - int(96 * s), x + int(82 * s) + onda, sh_y - int(62 * s)], fill=piel)
        d.rounded_rectangle([x - int(78 * s), sh_y + int(10 * s), x - int(52 * s), sh_y + int(150 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x - int(78 * s), sh_y + int(140 * s), x - int(52 * s), sh_y + int(166 * s)], fill=piel)
    elif expresion == "pensando":
        d.rounded_rectangle([x + int(52 * s), sh_y + int(10 * s), x + int(78 * s), sh_y + int(110 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x + int(52 * s), sh_y - int(60 * s), x + int(86 * s), sh_y - int(26 * s)], fill=piel)
        d.rounded_rectangle([x - int(78 * s), sh_y + int(10 * s), x - int(52 * s), sh_y + int(150 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x - int(78 * s), sh_y + int(140 * s), x - int(52 * s), sh_y + int(166 * s)], fill=piel)
    else:
        sw = 4 * math.sin(2 * math.pi * t / 1.6 + 1.2) if pose == "caminando" else 2 * math.sin(2 * math.pi * t / 1.6)
        d.rounded_rectangle([x - int(78 * s) + sw, sh_y + int(10 * s), x - int(52 * s) + sw, sh_y + int(150 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x - int(78 * s) + sw, sh_y + int(140 * s), x - int(52 * s) + sw, sh_y + int(166 * s)], fill=piel)
        d.rounded_rectangle([x + int(52 * s) - sw, sh_y + int(10 * s), x + int(78 * s) - sw, sh_y + int(150 * s)],
                            radius=int(10 * s), fill=camisa)
        d.ellipse([x + int(52 * s) - sw, sh_y + int(140 * s), x + int(78 * s) - sw, sh_y + int(166 * s)], fill=piel)
    # libro (maestro) en la mano izquierda
    if base.get("libro"):
        d.rectangle([x - int(96 * s), sh_y + int(120 * s), x - int(46 * s), sh_y + int(160 * s)],
                    fill=(200, 60, 60), outline=(120, 30, 30), width=max(1, int(2 * s)))
        d.line([x - int(71 * s), sh_y + int(120 * s), x - int(71 * s), sh_y + int(160 * s)],
               fill=(255, 255, 255), width=max(1, int(2 * s)))
    # mochila (estudiante) a la espalda
    if base.get("mochila"):
        d.rounded_rectangle([x - int(92 * s), sh_y + int(30 * s), x - int(62 * s), sh_y + int(130 * s)],
                            radius=int(10 * s), fill=(250, 180, 40))
    # --- cabeza ---
    hy = sh_y - int(52 * s)
    hr = int(52 * s)
    d.rectangle([x - int(18 * s), hy + int(20 * s), x + int(18 * s), sh_y + int(6 * s)], fill=SKIN_D)
    d.ellipse([x - hr, hy - hr, x + hr, hy + hr], fill=piel)
    _pelo(d, x, hy, hr, s, estilo_pelo, base.get("color_pelo", HAIR))
    # gafas (científico)
    if base.get("gafas"):
        for ex in (-1, 1):
            d.ellipse([x + ex * int(26 * s) - int(16 * s), hy - int(16 * s),
                       x + ex * int(26 * s) + int(16 * s), hy + int(16 * s)],
                      outline=(40, 40, 40), width=max(2, int(3 * s)))
        d.line([x - int(10 * s), hy, x + int(10 * s), hy], fill=(40, 40, 40), width=max(2, int(3 * s)))
    # estetoscopio (doctora)
    if base.get("estetoscopio"):
        d.arc([x - int(44 * s), sh_y + int(10 * s), x + int(44 * s), sh_y + int(90 * s)],
              start=0, end=180, fill=(40, 40, 40), width=max(2, int(4 * s)))
        d.ellipse([x + int(28 * s), sh_y + int(84 * s), x + int(52 * s), sh_y + int(108 * s)],
                  fill=(60, 60, 60))
    # barba (anciano)
    if base.get("barba"):
        d.pieslice([x - hr + int(6 * s), hy, x + hr - int(6 * s), hy + hr + int(10 * s)],
                   start=0, end=180, fill=(230, 230, 230))
    # --- cara según expresión ---
    ex = int(22 * s)
    ey = hy - int(6 * s)
    ew = int(7 * s)
    if bl:
        d.line([x - ex - ew, ey, x - ex + ew, ey], fill=(40, 30, 30), width=max(1, int(3 * s)))
        d.line([x + ex - ew, ey, x + ex + ew, ey], fill=(40, 30, 30), width=max(1, int(3 * s)))
    elif expresion == "sorprendido":
        for sx in (-ex, ex):
            d.ellipse([x + sx - int(10 * s), ey - int(10 * s), x + sx + int(10 * s), ey + int(10 * s)],
                      fill=(255, 255, 255))
            d.ellipse([x + sx - int(5 * s), ey - int(5 * s), x + sx + int(5 * s), ey + int(5 * s)],
                      fill=(30, 30, 40))
        d.line([x - ex - ew, ey - int(24 * s), x - ex + ew, ey - int(28 * s)], fill=HAIR, width=int(4 * s))
        d.line([x + ex - ew, ey - int(28 * s), x + ex + ew, ey - int(24 * s)], fill=HAIR, width=int(4 * s))
    else:
        for sx in (-ex, ex):
            d.ellipse([x + sx - ew, ey - int(10 * s), x + sx + ew, ey + int(10 * s)],
                      fill=(255, 255, 255))
            d.ellipse([x + sx - int(4 * s), ey - int(5 * s), x + sx + int(4 * s), ey + int(5 * s)],
                      fill=(30, 30, 40))
        if expresion == "preocupado":
            d.line([x - ex - ew, ey - int(22 * s), x - ex + ew, ey - int(14 * s)], fill=HAIR, width=int(4 * s))
            d.line([x + ex - ew, ey - int(14 * s), x + ex + ew, ey - int(22 * s)], fill=HAIR, width=int(4 * s))
        elif expresion == "pensando":
            d.line([x - ex - ew, ey - int(26 * s), x - ex + ew, ey - int(20 * s)], fill=HAIR, width=int(4 * s))
            d.line([x + ex - ew, ey - int(20 * s), x + ex + ew, ey - int(26 * s)], fill=HAIR, width=int(4 * s))
        else:
            d.line([x - ex - ew, ey - int(20 * s), x - ex + ew, ey - int(24 * s)], fill=HAIR, width=int(4 * s))
            d.line([x + ex - ew, ey - int(24 * s), x + ex + ew, ey - int(20 * s)], fill=HAIR, width=int(4 * s))
    # boca
    my = hy + int(22 * s)
    if expresion == "contento":
        d.arc([x - int(16 * s), my - int(8 * s), x + int(16 * s), my + int(14 * s)],
              start=10, end=170, fill=(120, 60, 50), width=max(2, int(4 * s)))
    elif expresion == "preocupado":
        d.arc([x - int(16 * s), my - int(4 * s), x + int(16 * s), my + int(16 * s)],
              start=190, end=350, fill=(120, 60, 50), width=max(2, int(4 * s)))
    elif expresion == "pensando":
        d.line([x - int(12 * s), my, x + int(12 * s), my], fill=(120, 60, 50), width=max(2, int(4 * s)))
    elif expresion == "sorprendido":
        d.ellipse([x - int(9 * s), my - int(4 * s), x + int(9 * s), my + int(12 * s)],
                  fill=(120, 60, 50))
    # bastón (anciano, anciana)
    if base.get("baston"):
        d.line([x + int(88 * s), sh_y + int(20 * s), x + int(88 * s), by], fill=(150, 110, 60),
               width=max(2, int(5 * s)))
        d.arc([x + int(72 * s), sh_y + int(4 * s), x + int(104 * s), sh_y + int(36 * s)],
              start=180, end=360, fill=(150, 110, 60), width=max(2, int(5 * s)))
    return by
