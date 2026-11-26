# -*- coding: utf-8 -*-
"""Renderizadores de escenas por estilo.

Estilos:
- ``aprendiz``: fondo blanco, mancha menta, rótulos manuscritos, personaje
  de camisa morada. Las escenas se describen con una lista de *elementos*
  (personaje, lámpara, mapa, texto, lista...).
- ``alebrigma`` / ``snes`` / ``nes``: escenas de tipo portada / intro /
  tarjeta / definición / fundido sobre fondo estrellado. La diferencia
  está en cómo se dibujan los sprites:
    * alebrigma: formas suaves a 720x1280.
    * snes: canvas interno 180x320 (16 bits), máximo 16 colores por sprite,
      contornos negros, sombreado con dithering, parallax de 3 capas,
      sprites con 2-4 fotogramas (parpadeo, caminata, flotación).
    * nes: canvas interno 144x256 (8 bits), máximo 4 colores por sprite,
      píxeles más grandes, mismo sistema.
  En snes/nes el lienzo interno se escala a 720x1280 con vecino más cercano
  (sin suavizado), que es lo que da el aspecto retro.
"""
import math
import random
from collections import Counter

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .core import (W, H, WHITE, BLACK, MINT, MINT2, SKIN, SKIN_D, HAIR,
                   PURPLE, PURPLE_D, BLUE, BLUE_D, BROWN, GREEN, GREEN_D,
                   YELLOW, YELLOW_L, RED, RED_D, GRAY, GRAY_D, POLE, ORANGE,
                   COURT_G, JUP_CREAM, JUP_TAN, JUP_BROWN, JUP_WHITE,
                   JUP_ORANGE, SPOT_RED, ICE, ICE_LINE, OCEAN, OCEAN_D,
                   CLOUD, font_hand, font_bold, font, ease_out, ease_out_back,
                   pop, blink, clamp, draw_blob, wrap_title, draw_title,
                   wrap_text, pop_scale)
from .personajes import (draw_person, dibujar_personaje, TIPOS_PERSONAJE,
                         brain_img, arm_img, wheel_img, person_img,
                         personaje_pixel, PERSONAJE_PIXEL,
                         PINK, PINK_L, PINK_D, BRAIN_K, INK, WHEEL_COLORS)
from .iconos import (draw_street_lamp, draw_hand_lamp, draw_camera,
                     draw_check, draw_small_person, draw_money_bag,
                     draw_soccer_ball, draw_basketball, draw_whistle,
                     draw_heart, draw_court, draw_jupiter_img,
                     draw_telescope, draw_star, draw_cloud, draw_floater,
                     draw_hunter, draw_thermometer, draw_radiation,
                     draw_umbrella, OBJETOS, dibujar_objeto)
from .objetos import (notebook_img, phone_img, calculator_img, map_img,
                      paper_pencil_img, wrench_img)
from .escenarios import fondo_escenario, ESCENARIOS, ESCENARIOS_OSCUROS


def pixelizar_objeto(nombre, tamano=28, n_colores=16):
    """Convierte un objeto suave en sprite pixel art (para snes/nes).

    Lo dibuja en un lienzo de 100x100 y lo reduce con vecino más cercano,
    luego limita la paleta. Así los 30+ objetos existen también en pixel art.
    """
    from PIL import Image as _Image
    lienzo = _Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    dd = ImageDraw.Draw(lienzo)
    dibujar_objeto(dd, nombre, 50, 50, s=1.0, t=0.0)
    px = lienzo.resize((tamano, tamano), _Image.NEAREST)
    if n_colores:
        px = cuantizar_sprite(px, n_colores)
    return px

# ---------------------------------------------------------------------------
# Reglas de los estilos retro (documentadas también en el README)
# ---------------------------------------------------------------------------
REGLAS_ESTILO = {
    "aprendiz": {
        "descripcion": "Cartoon 2D: fondo blanco, mancha menta, rótulos manuscritos.",
        "resolucion": (720, 1280),
    },
    "alebrigma": {
        "descripcion": "Formas suaves sobre fondo morado estrellado, tarjetas burbuja.",
        "resolucion": (720, 1280),
    },
    "snes": {
        "descripcion": "Pixel art 16 bits: canvas 180x320, máx. 16 colores por sprite, "
                       "dithering, parallax de 3 capas, sprites de 2-4 fotogramas.",
        "resolucion": (180, 320),
        "colores_por_sprite": 16,
    },
    "nes": {
        "descripcion": "Pixel art 8 bits: canvas 144x256, máx. 4 colores por sprite, "
                       "píxeles más grandes, mismo sistema que snes.",
        "resolucion": (144, 256),
        "colores_por_sprite": 4,
    },
}

# Matriz de Bayer 4x4 para el dithering ordenado (valores 0..15).
BAYER_4 = np.array([[0, 8, 2, 10],
                    [12, 4, 14, 6],
                    [3, 11, 1, 9],
                    [15, 7, 13, 5]], dtype=float) / 16.0

BG_OSCURO = (30, 27, 75)      # morado oscuro (fondo retro)
BG_OSCURO_2 = (48, 38, 110)   # morado claro (resplandor central)
BG_PASTEL = (240, 240, 245)   # fondo suave de las tarjetas


def cuantizar_sprite(img, n_colores):
    """Reduce los colores opacos de un sprite RGBA a ``n_colores`` como máximo.

    Mantiene el contorno negro y los colores más usados; los demás se mapean
    al color kept más cercano. Es la regla de paleta de SNES (16) y NES (4).
    Si el sprite ya usa <= n colores, se devuelve tal cual.
    """
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    alpha = img.split()[3]
    rgb = img.convert("RGB")
    px = rgb.load()
    al = alpha.load()
    conteo = Counter()
    for y in range(img.height):
        for x in range(img.width):
            if al[x, y] > 0:
                conteo[px[x, y]] += 1
    if len(conteo) <= n_colores:
        return img
    top = [c for c, _ in conteo.most_common(n_colores)]

    def cercano(c):
        mejor, mejor_d = top[0], None
        for t in top:
            d = (c[0] - t[0]) ** 2 + (c[1] - t[1]) ** 2 + (c[2] - t[2]) ** 2
            if mejor_d is None or d < mejor_d:
                mejor, mejor_d = t, d
        return mejor

    mapa = {c: cercano(c) for c in conteo}
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    op = out.load()
    for y in range(img.height):
        for x in range(img.width):
            if al[x, y] > 0:
                op[x, y] = mapa[px[x, y]] + (255,)
    return out


def fondo_estrellado(ancho, alto, t, pixel=False, semilla=7):
    """Fondo morado estrellado con parallax de 3 capas y dithering.

    El degradado se cuantiza con dithering de Bayer (4 niveles) cuando
    ``pixel`` es True, como en los fondos de SNES. Las estrellas se mueven
    a distinta velocidad por capa (parallax) y parpadean.
    """
    # --- degradado radial con dithering ---
    yy, xx = np.mgrid[0:alto, 0:ancho].astype(float)
    cx, cy = ancho / 2, alto * 0.35
    dist = np.sqrt(((xx - cx) / (ancho * 0.75)) ** 2 + ((yy - cy) / (alto * 0.75)) ** 2)
    glow = np.clip(1.0 - dist, 0, 1) ** 1.6
    if pixel:
        # dithering ordenado: 4 niveles de resplandor
        bayer = np.tile(BAYER_4, (alto // 4 + 1, ancho // 4 + 1))[:alto, :ancho]
        niveles = np.floor(glow * 4 + bayer) / 4.0
        glow = np.clip(niveles, 0, 1)
    c1 = np.array(BG_OSCURO, float)
    c2 = np.array(BG_OSCURO_2, float)
    arr = (c1[None, None, :] * (1 - glow[..., None])
           + c2[None, None, :] * glow[..., None]).astype(np.uint8)
    img = Image.fromarray(arr, "RGB")
    d = ImageDraw.Draw(img)
    # --- estrellas en 3 capas de parallax ---
    rnd = random.Random(semilla)
    for capa, (n, vel, tam, alfa) in enumerate([
            (40, 1.5, 1, 140),   # lejos: pocas, lentas, tenues
            (30, 4.0, 1, 200),   # medio
            (16, 10.0, 2, 255),  # cerca: grandes, rápidas, brillantes
    ]):
        for _ in range(n):
            sx = rnd.uniform(0, ancho)
            sy = rnd.uniform(0, alto)
            fase = rnd.uniform(0, 6.28)
            # desplazamiento horizontal por parallax (envuelve)
            dx = (vel * t * (ancho / 720.0)) % ancho
            x = int((sx + dx) % ancho)
            y = int(sy)
            brillo = 0.55 + 0.45 * math.sin(2 * math.pi * t / 2.0 + fase)
            col = (int(255 * brillo), int(255 * brillo), int(255 * brillo))
            if tam == 1 or not pixel:
                d.point((x, y), fill=col)
            else:
                d.rectangle([x, y, x + 1, y + 1], fill=col)
            if capa == 2 and rnd.random() < 0.3:
                # estrella con destello en cruz
                d.line([x - 3, y, x + 3, y], fill=col)
                d.line([x, y - 3, x, y + 3], fill=col)
    return img


def destellos(d, x, y, t, escala=1.0):
    """Tres destellos pulsantes alrededor de (x, y)."""
    for i, (dx, dy, r) in enumerate([(-70, -30, 8), (60, -60, 6), (90, 20, 5)]):
        p = 0.5 + 0.5 * math.sin(2 * math.pi * t / 0.9 + i * 2.1)
        rr = int(r * escala * (0.6 + 0.6 * p))
        d.ellipse([x + dx * escala - rr, y + dy * escala - rr,
                   x + dx * escala + rr, y + dy * escala + rr],
                  fill=(255, 255, 200))


# ---------------------------------------------------------------------------
# Sprites suaves (modo alebrigma)
# ---------------------------------------------------------------------------
def cerebro_suave(ancho_px):
    """Cerebro rosa con formas suaves (sin píxeles), del tamaño pedido."""
    alto = int(ancho_px * 0.62)
    img = Image.new("RGBA", (ancho_px, alto), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    w, h = ancho_px, alto
    # cuerpo
    d.ellipse([w * 0.05, h * 0.08, w * 0.95, h * 0.92], fill=PINK + (255,),
              outline=BRAIN_K + (255,), width=max(2, w // 40))
    # pliegues
    for (x0, y0, x1, y1, a0, a1) in [
            (0.15, 0.20, 0.55, 0.60, 200, 340),
            (0.45, 0.15, 0.85, 0.55, 180, 320),
            (0.25, 0.45, 0.65, 0.85, 20, 160)]:
        d.arc([w * x0, h * y0, w * x1, h * y1], start=a0, end=a1,
              fill=PINK_D + (255,), width=max(2, w // 50))
    # brillo
    d.arc([w * 0.15, h * 0.12, w * 0.6, h * 0.5], start=180, end=300,
          fill=(255, 255, 255, 180), width=max(2, w // 45))
    # ojos
    for ex in (0.38, 0.62):
        d.ellipse([w * ex - w * 0.03, h * 0.55, w * ex + w * 0.03, h * 0.68],
                  fill=(255, 255, 255, 255))
        d.ellipse([w * ex - w * 0.015, h * 0.58, w * ex + w * 0.015, h * 0.65],
                  fill=(30, 30, 40, 255))
    # boca
    d.arc([w * 0.42, h * 0.68, w * 0.58, h * 0.85], start=20, end=160,
          fill=BRAIN_K + (255,), width=max(2, w // 50))
    return img


def persona_suave(ancho_px, camisa=(70, 130, 200), pantalon=(50, 50, 90),
                  cabello=(60, 40, 20), sonrie=True):
    """Persona suave reutilizando draw_person sobre un lienzo temporal."""
    alto = int(ancho_px * 1.4)
    img = Image.new("RGBA", (ancho_px, alto), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = ancho_px / 160.0
    draw_person(d, ancho_px // 2, alto - 4, s=s, t=0.0, pose="stand",
                smile=sonrie, camisa=camisa, pantalon=pantalon, cabello=cabello)
    return img


def objeto_suave(nombre, ancho_px):
    """Objetos suaves (libreta, teléfono, calculadora, mapa, papel, llave)."""
    alto = int(ancho_px * 1.1)
    img = Image.new("RGBA", (ancho_px, alto), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    w, h = ancho_px, alto
    u = w / 100.0  # unidad
    if nombre == "libreta":
        d.rounded_rectangle([8 * u, 6 * u, 92 * u, 94 * u], radius=6 * u,
                            fill=(52, 152, 219, 255), outline=INK + (255,), width=max(2, int(2 * u)))
        d.rounded_rectangle([8 * u, 6 * u, 92 * u, 30 * u], radius=6 * u,
                            fill=(41, 128, 185, 255))
        for i, yy in enumerate([42, 54, 66, 78]):
            d.line([16 * u, yy * u, 84 * u, yy * u], fill=(255, 255, 255, 220),
                   width=max(2, int(2 * u)))
        d.ellipse([46 * u, 12 * u, 54 * u, 20 * u], fill=(255, 255, 255, 255))
    elif nombre == "telefono":
        d.rounded_rectangle([18 * u, 4 * u, 82 * u, 96 * u], radius=10 * u,
                            fill=(40, 44, 66, 255), outline=INK + (255,), width=max(2, int(2 * u)))
        d.rounded_rectangle([24 * u, 12 * u, 76 * u, 78 * u], radius=4 * u,
                            fill=(180, 230, 255, 255))
        for i, (ax, ay) in enumerate([(32, 22), (50, 22), (68, 22), (32, 40), (50, 40), (68, 40),
                                      (32, 58), (50, 58), (68, 58)]):
            d.rounded_rectangle([ax * u, ay * u, (ax + 10) * u, (ay + 10) * u],
                                radius=2 * u, fill=(255, 190, 80, 255))
        d.ellipse([46 * u, 84 * u, 54 * u, 92 * u], fill=(255, 255, 255, 255))
    elif nombre == "calculadora":
        d.rounded_rectangle([14 * u, 4 * u, 86 * u, 96 * u], radius=8 * u,
                            fill=(90, 96, 120, 255), outline=INK + (255,), width=max(2, int(2 * u)))
        d.rounded_rectangle([22 * u, 10 * u, 78 * u, 28 * u], radius=3 * u,
                            fill=(200, 255, 210, 255))
        for fila in range(3):
            for col in range(3):
                x0 = 22 * u + col * 20 * u
                y0 = 36 * u + fila * 18 * u
                d.rounded_rectangle([x0, y0, x0 + 14 * u, y0 + 12 * u], radius=2 * u,
                                    fill=(230, 230, 240, 255))
        d.rounded_rectangle([22 * u, 90 * u, 36 * u, 102 * u], radius=2 * u,
                            fill=(255, 90, 90, 255))
    elif nombre == "mapa":
        d.rounded_rectangle([4 * u, 8 * u, 96 * u, 92 * u], radius=6 * u,
                            fill=(245, 235, 200, 255), outline=INK + (255,), width=max(2, int(2 * u)))
        d.line([4 * u, 40 * u, 96 * u, 40 * u], fill=(180, 180, 180, 255), width=max(2, int(3 * u)))
        d.line([50 * u, 8 * u, 50 * u, 92 * u], fill=(180, 180, 180, 255), width=max(2, int(3 * u)))
        d.ellipse([12 * u, 55 * u, 38 * u, 85 * u], fill=(160, 220, 160, 255))
        d.ellipse([70 * u, 55 * u, 78 * u, 63 * u], fill=(255, 90, 90, 255),
                  outline=INK + (255,), width=max(1, int(u)))
    elif nombre == "papel":
        d.rounded_rectangle([16 * u, 4 * u, 84 * u, 88 * u], radius=4 * u,
                            fill=(255, 255, 255, 255), outline=INK + (255,), width=max(2, int(2 * u)))
        for yy in [22, 34, 46, 58, 70]:
            d.line([24 * u, yy * u, 76 * u, yy * u], fill=(120, 120, 140, 255),
                   width=max(2, int(2 * u)))
        d.rounded_rectangle([60 * u, 70 * u, 92 * u, 78 * u], radius=3 * u,
                            fill=(255, 190, 80, 255))
    elif nombre == "llave":
        d.rounded_rectangle([44 * u, 20 * u, 56 * u, 92 * u], radius=4 * u,
                            fill=(200, 200, 210, 255), outline=INK + (255,), width=max(2, int(2 * u)))
        d.ellipse([28 * u, 4 * u, 72 * u, 44 * u], fill=(200, 200, 210, 255),
                  outline=INK + (255,), width=max(2, int(2 * u)))
        d.pieslice([38 * u, 8 * u, 62 * u, 32 * u], start=200, end=340,
                   fill=(0, 0, 0, 0))
    return img


# ---------------------------------------------------------------------------
# Estilo aprendiz: escenas por elementos
# ---------------------------------------------------------------------------
def _pop_aparece(elem, t):
    """Escala de aparición (pop) según el campo "aparece" del elemento."""
    ap = elem.get("aparece", 0.0)
    if t < ap:
        return 0.0
    return pop(ap, t)


def _s_con_pop(elem, t):
    """Escala con pop si el elemento tiene "aparece" (0 antes de aparecer)."""
    s = elem.get("escala", 1.0)
    ap = elem.get("aparece", 0.0)
    if ap > 0:
        return s * pop(ap, t)
    return s


def _dibujar_texto(d, texto, x, y, tamano, fuente="bold", color=BLACK,
                   centrado=True):
    f = font_hand(tamano) if fuente == "hand" else font_bold(tamano)
    if centrado:
        bb = d.textbbox((0, 0), texto, font=f)
        d.text((x - (bb[2] + bb[0]) / 2, y - (bb[3] + bb[1]) / 2), texto,
               font=f, fill=color)
    else:
        d.text((x, y), texto, font=f, fill=color)


def dibujar_elemento(img, elem, t, dur):
    """Dibuja un elemento de una escena aprendiz sobre ``img`` (RGB 720x1280)."""
    d = ImageDraw.Draw(img)
    tipo = elem["tipo"]
    ap = elem.get("aparece", 0.0)
    if t < ap:
        return
    s = elem.get("escala", 1.0)

    if tipo == "personaje":
        x, y = elem["x"], elem["y"]
        pose = elem.get("pose", "stand")
        camina = elem.get("camina")
        fase = 0.0
        if camina:
            p = clamp(t / dur, 0, 1)
            x = camina["de_x"] + (camina["a_x"] - camina["de_x"]) * p
            pose = "walk"
            fase = 2 * math.pi * t / 0.9
        float_y = 0.0
        if elem.get("flota"):
            float_y = 10 * math.sin(2 * math.pi * t / 2.2)
            pose = "float"
        tipo_p = elem.get("personaje")
        # Poses genéricas con tipo de personaje -> dibujar_personaje
        mapa_poses = {"stand": "pie", "pie": "pie", "walk": "caminando",
                      "caminando": "caminando", "point": "senalando",
                      "senalando": "senalando", "sentado": "sentado",
                      "thumbs": "saludando", "saludando": "saludando"}
        if tipo_p and pose in mapa_poses:
            dibujar_personaje(
                d, int(x), int(y + float_y), s=s, t=t, tipo=tipo_p,
                expresion=elem.get("expresion",
                                   "contento" if elem.get("sonrie", False) else "preocupado"),
                pose=mapa_poses[pose], walk_phase=fase,
                camisa=tuple(elem["camisa"]) if "camisa" in elem else None,
                pantalon=tuple(elem["pantalon"]) if "pantalon" in elem else None,
                pelo=tuple(elem["pelo"]) if "pelo" in elem else None,
                piel=tuple(elem["piel"]) if "piel" in elem else None)
        else:
            draw_person(d, int(x), int(y), s=s, t=t, pose=pose,
                        smile=elem.get("sonrie", False), walk_phase=fase,
                        float_y=float_y,
                        camisa=tuple(elem["camisa"]) if "camisa" in elem else None,
                        pantalon=tuple(elem["pantalon"]) if "pantalon" in elem else None,
                        cabello=tuple(elem["cabello"]) if "cabello" in elem else None)

    elif tipo == "lampara_calle":
        enc = elem.get("encendida", True)
        if enc == "al_final":
            enc = t > dur * elem.get("umbral", 0.55)
        glow = 0.85 + 0.15 * math.sin(2 * math.pi * t / 1.5) if enc else 1.0
        draw_street_lamp(d, elem["x"], elem["y"], s=s, on=bool(enc), glow=glow)

    elif tipo == "lampara_mano":
        draw_hand_lamp(d, elem["x"], elem["y"], s=_s_con_pop(elem, t),
                       on=elem.get("encendida", True))

    elif tipo == "camara":
        draw_camera(d, elem["x"], elem["y"], s=_s_con_pop(elem, t))

    elif tipo == "mapa":
        x, y, w, h = elem["x"], elem["y"], elem["w"], elem["h"]
        d.rounded_rectangle([x, y, x + w, y + h], radius=24,
                            fill=(245, 235, 200), outline=BLACK, width=4)
        d.line([x, y + int(h * 0.45), x + w, y + int(h * 0.45)],
               fill=(190, 190, 190), width=6)
        d.line([x + int(w * 0.5), y, x + int(w * 0.5), y + h],
               fill=(190, 190, 190), width=6)
        if "parque" in elem:
            px0, py0, px1, py1 = elem["parque"]
            d.ellipse([px0, py0, px1, py1], fill=(160, 220, 160))
        for cancha in elem.get("canchas", []):
            draw_court(d, *cancha)
        for (px, py) in elem.get("pines", []):
            d.ellipse([px - 14, py - 14, px + 14, py + 14], fill=GREEN)
            d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=WHITE)
        if "corazon" in elem:
            cx, cy, cs = elem["corazon"]
            draw_heart(d, cx, cy, s=cs)
        if "titulo" in elem:
            ty = (y + h + 48) if elem.get("titulo_pos", "abajo") == "abajo" else y - 48
            _dibujar_texto(d, elem["titulo"], x + w // 2, ty, 44, "bold")

    elif tipo == "hoja":
        x, y = elem["x"], elem["y"]
        d.pieslice([x - 40 * s, y - 45 * s, x + 40 * s, y + 45 * s],
                   start=200, end=340, fill=GREEN)
        d.line([x, y + 40 * s, x, y - 35 * s], fill=GREEN_D, width=5)

    elif tipo == "luna":
        x, y, r = elem["x"], elem["y"], elem["radio"]
        d.ellipse([x - r, y - r, x + r, y + r], fill=(245, 245, 230))
        d.ellipse([x - r * 0.4, y - r * 0.2, x - r * 0.1, y + r * 0.1],
                  fill=(220, 220, 200))
        d.ellipse([x + r * 0.2, y + r * 0.3, x + r * 0.45, y + r * 0.55],
                  fill=(220, 220, 200))

    elif tipo == "palomita":
        draw_check(d, elem["x"], elem["y"], r=elem.get("radio", 34))

    elif tipo == "texto_grande":
        _dibujar_texto(d, elem["texto"], elem["x"], elem["y"],
                       elem.get("tamano", 200), elem.get("fuente", "hand"),
                       elem.get("color", BLACK))

    elif tipo == "texto":
        _dibujar_texto(d, elem["texto"], elem["x"], elem["y"],
                       elem.get("tamano", 44), elem.get("fuente", "bold"),
                       elem.get("color", BLACK),
                       centrado=elem.get("alineacion", "centrado") != "izquierda")

    elif tipo == "lista":
        x, y = elem["x"], elem["y"]
        tam = elem.get("tamano", 44)
        intervalo = elem.get("intervalo", 1.2)
        for i, item in enumerate(elem["items"]):
            ap_i = 0.4 + i * intervalo
            if t < ap_i:
                continue
            sc = pop(ap_i, t)
            if sc <= 0.02:
                continue
            if elem.get("check", True):
                d.ellipse([x, y + i * 100 - 34 * sc, x + 68 * sc, y + i * 100 + 34 * sc],
                          fill=GREEN)
                d.text((x + 34 * sc, y + i * 100 - 18 * sc), "✓",
                       font=font_bold(max(1, int(44 * sc))), fill=WHITE, anchor="mm")
            f = font_hand(tam)
            d.text((x + 92, y + i * 100 - tam // 2), item, font=f, fill=BLACK)

    elif tipo == "nota":
        _dibujar_texto(d, elem["texto"], elem["x"], elem["y"],
                       elem.get("tamano", 32), elem.get("fuente", "bold"),
                       elem.get("color", (120, 120, 130)),
                       centrado=elem.get("alineacion", "centrado") != "izquierda")

    elif tipo == "bolsa_dinero":
        draw_money_bag(d, elem["x"], elem["y"], s=_s_con_pop(elem, t))
        if "texto" in elem:
            _dibujar_texto(d, elem["texto"], elem["x"], elem["y"] + 150 * s,
                           elem.get("tamano_texto", 48), "bold", GREEN_D)

    elif tipo == "grupo":
        x, y = elem["x"], elem["y"]
        colores = elem.get("colores", [GREEN, (255, 107, 107), (70, 130, 200)])
        n = len(colores)
        sep = elem.get("separacion", 68)
        sg = _s_con_pop(elem, t)
        for i, col in enumerate(colores):
            draw_small_person(d, x + (i - (n - 1) / 2) * sep, y, sg,
                              tuple(col))

    elif tipo == "cancha":
        draw_court(d, elem["x0"], elem["y0"], elem["x1"], elem["y1"])

    elif tipo == "balon_futbol":
        draw_soccer_ball(d, elem["x"], elem["y"], s=_s_con_pop(elem, t))

    elif tipo == "balon_basquet":
        draw_basketball(d, elem["x"], elem["y"], s=_s_con_pop(elem, t))

    elif tipo == "silbato":
        draw_whistle(d, elem["x"], elem["y"], s=_s_con_pop(elem, t))

    elif tipo == "corazon":
        draw_heart(d, elem["x"], elem["y"], s=_s_con_pop(elem, t))

    elif tipo == "jupiter":
        x, y, r = elem["x"], elem["y"], elem["radio"]
        bob = 8 * math.sin(2 * math.pi * t / 2.0)
        draw_jupiter_img(img, x, y, r, spot=elem.get("mancha", True), bob=bob)
        if elem.get("flecha"):
            fx, fy = elem.get("flecha_xy", (x - r - 90, y + r * 0.6))
            d.line([fx, fy, x - r - 10, y + r * 0.4], fill=RED, width=7)
            d.polygon([(x - r - 10, y + r * 0.4 - 14), (x - r - 10, y + r * 0.4 + 14),
                       (x - r + 16, y + r * 0.4)], fill=RED)

    elif tipo == "telescopio":
        draw_telescope(d, elem["x"], elem["y"], s=s)

    elif tipo == "estrella":
        draw_star(d, elem["x"], elem["y"], r=elem.get("radio", 40))

    elif tipo == "nube":
        draw_cloud(d, elem["x"], elem["y"], s=s)

    elif tipo == "flotador":
        colores_flotador = {"rosa": (255, 150, 180), "naranja": (255, 190, 90),
                            "verde": (140, 200, 120)}
        col = elem.get("color", "naranja")
        col = colores_flotador.get(col, tuple(col) if isinstance(col, list) else (255, 190, 90))
        draw_floater(d, elem["x"], elem["y"], s=s, color=col,
                     bob=8 * math.sin(2 * math.pi * t / 1.8))

    elif tipo == "cazador":
        draw_hunter(d, elem["x"], elem["y"], s=s,
                    bob=6 * math.sin(2 * math.pi * t / 1.5))

    elif tipo == "termometro":
        draw_thermometer(d, elem["x"], elem["y"], s=s, cold=elem.get("frio", True))

    elif tipo == "radiacion":
        draw_radiation(d, elem["x"], elem["y"], t)

    elif tipo == "paraguas":
        draw_umbrella(d, elem["x"], elem["y"], s=s)

    elif tipo == "europa":
        # Luna Europa con grietas y, abajo, la franja de océano bajo el hielo.
        x, y, r = elem["x"], elem["y"], elem["radio"]
        d.ellipse([x - r, y - r, x + r, y + r], fill=ICE)
        d.ellipse([x - r, y - r, x + r, y + r], outline=ICE_LINE, width=4)
        for (x0, y0, x1, y1) in [(-0.79, -0.32, -0.21, -0.05), (-0.63, 0.32, -0.05, 0.11),
                                 (-0.32, -0.79, -0.11, -0.32), (0.32, 0.63, 0.58, 0.21)]:
            d.line([x + x0 * r, y + y0 * r, x + x1 * r, y + y1 * r],
                   fill=ICE_LINE, width=5)
        # franja de océano (ancho completo, abajo)
        oy = 1000
        d.rectangle([60, oy, 660, 1120], fill=OCEAN)
        d.rectangle([60, oy, 660, oy + 14], fill=OCEAN_D)
        for wx in range(90, 640, 90):
            d.arc([wx - 40, oy - 18, wx + 40, oy + 30], start=180, end=360,
                  fill=WHITE, width=6)
        for i, (bx, by) in enumerate([(200, 1060), (360, 1080), (520, 1050)]):
            rr = 7 + 3 * math.sin(2 * math.pi * t / 1.1 + i * 2)
            d.ellipse([bx - rr, by - rr, bx + rr, by + rr],
                      fill=(180, 220, 245))

    elif tipo == "objeto":
        dibujar_objeto(d, elem["nombre"], elem["x"], elem["y"],
                       s=_s_con_pop(elem, t),
                       color=elem.get("color"), t=t)

    elif tipo == "destellos":
        puntos = elem.get("puntos")
        if puntos:
            for i, (sx, sy) in enumerate(puntos):
                rr = 8 + 4 * math.sin(2 * math.pi * t / 0.8 + i)
                d.ellipse([sx - rr, sy - rr, sx + rr, sy + rr], fill=YELLOW)
        else:
            destellos(d, elem["x"], elem["y"], t, escala=s)

    else:
        raise ValueError(f"Elemento aprendiz desconocido: {tipo}")


def escena_aprendiz(escena, t, dur):
    """Un fotograma del estilo aprendiz: escenario (opcional) + mancha menta
    + rótulo + elementos."""
    if escena.get("escenario"):
        img = fondo_escenario(escena["escenario"], W, H, t)
    else:
        img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    if escena.get("mancha", "escenario" not in escena):
        draw_blob(d, 360, 780, 330, 330, MINT)
        draw_blob(d, 400, 810, 264, 247, MINT2)
    color_titulo = WHITE if escena.get("escenario") in ESCENARIOS_OSCUROS else BLACK
    draw_title(d, escena["rotulo"], y_top=100, color=color_titulo)
    for elem in escena.get("elementos", []):
        dibujar_elemento(img, elem, t, dur)
    return img


# ---------------------------------------------------------------------------
# Estilos retro: alebrigma / snes / nes
# ---------------------------------------------------------------------------
# Escenas de "mente extendida" y su sprite asociado (para los specs).
SPRITES_PERSONA = {
    "otto": dict(hair=(60, 40, 20), shirt=(70, 130, 200), pants=(50, 50, 90)),
    "clark": dict(hair=(200, 200, 200), shirt=(90, 90, 110), pants=(50, 50, 70)),
    "chalmers": dict(hair=(30, 30, 30), shirt=(60, 90, 60), pants=(50, 50, 70)),
    "persona": dict(hair=(60, 40, 20), shirt=(120, 60, 140), pants=(50, 50, 90)),
}
SPRITES_OBJETO = {
    "libreta": "libreta", "telefono": "telefono", "calculadora": "calculadora",
    "mapa": "mapa", "papel": "papel", "llave": "llave",
}


class Retro:
    """Renderizador de escenas retro (alebrigma / snes / nes).

    ``modo``: "alebrigma" (formas suaves, 720x1280), "snes" (180x320, 16
    colores por sprite) o "nes" (144x256, 4 colores por sprite). En snes/nes
    el fotograma interno se escala a 720x1280 con vecino más cercano.
    """

    def __init__(self, modo):
        if modo not in ("alebrigma", "snes", "nes"):
            raise ValueError(f"Modo retro desconocido: {modo}")
        self.modo = modo
        self.W, self.H = REGLAS_ESTILO[modo]["resolucion"]
        self.pixel = modo in ("snes", "nes")
        self.max_colores = REGLAS_ESTILO[modo].get("colores_por_sprite")
        self.f = self.W / 720.0  # factor de escala de textos y tamaños
        self._fondo_cache = None

    # -- fuentes y tamaños --------------------------------------------------
    def _ft(self, tamano_720):
        return max(6, int(tamano_720 * self.f))

    def _font(self, tamano_720):
        return font(self._ft(tamano_720))

    # -- sprites -------------------------------------------------------------
    def _esc(self, celdas, fraccion):
        """Escala de un sprite pixel para que ocupe ``fraccion`` del ancho."""
        return max(1, round(fraccion * self.W / celdas))

    def _cuantizar(self, img):
        if self.max_colores:
            return cuantizar_sprite(img, self.max_colores)
        return img

    def sprite(self, nombre, **kw):
        """Devuelve el sprite (RGBA) en el modo actual.

        nombre: cerebro | brazos | rueda | persona:<clave> | <objeto>."""
        if self.modo == "alebrigma":
            return self._sprite_suave(nombre, **kw)
        return self._sprite_pixel(nombre, **kw)

    def _sprite_pixel(self, nombre, **kw):
        if nombre == "cerebro":
            return self._cuantizar(brain_img(scale=self._esc(32, 0.40),
                                             blink=kw.get("blink", False)))
        if nombre == "brazos":
            return self._cuantizar(arm_img(scale=self._esc(32, 0.40)))
        if nombre == "rueda":
            d = int(self.W * kw.get("diametro", 0.44))
            return wheel_img(diameter=d, angle_deg=kw.get("angulo", 0))
        if nombre.startswith("persona"):
            clave = nombre.split(":", 1)[1] if ":" in nombre else "otto"
            if clave in SPRITES_PERSONA:
                p = SPRITES_PERSONA[clave]
                return self._cuantizar(person_img(
                    scale=self._esc(20, 0.20), blink=kw.get("blink", False),
                    paso=kw.get("paso", 0), **p))
            # cualquier otro tipo de personaje (mujer, nino, policia...)
            return self._cuantizar(personaje_pixel(
                clave, scale=self._esc(20, 0.20), blink=kw.get("blink", False),
                paso=kw.get("paso", 0)))
        if nombre in OBJETOS:
            # cualquier objeto del catálogo, pixelizado a la paleta del modo
            return pixelizar_objeto(nombre, tamano=28,
                                    n_colores=self.max_colores or 16)
        if nombre in SPRITES_OBJETO:
            fn = {"libreta": notebook_img, "telefono": phone_img,
                  "calculadora": calculator_img, "mapa": map_img,
                  "papel": paper_pencil_img, "llave": wrench_img}[nombre]
            celdas = {"libreta": 26, "telefono": 18, "calculadora": 22,
                      "mapa": 34, "papel": 30, "llave": 26}[nombre]
            fraccion = {"libreta": 0.28, "telefono": 0.22, "calculadora": 0.25,
                        "mapa": 0.45, "papel": 0.30, "llave": 0.25}[nombre]
            return self._cuantizar(fn(scale=self._esc(celdas, fraccion)))
        if nombre == "equipo":
            # equipo de tres personas: se compone en la escena, no es un sprite
            return None
        raise ValueError(f"Sprite retro desconocido: {nombre}")

    def _sprite_suave(self, nombre, **kw):
        if nombre == "cerebro":
            return cerebro_suave(int(self.W * 0.40))
        if nombre == "brazos":
            return None
        if nombre == "rueda":
            d = int(self.W * kw.get("diametro", 0.44))
            return wheel_img(diameter=d, angle_deg=kw.get("angulo", 0), suave=True)
        if nombre.startswith("persona"):
            clave = nombre.split(":", 1)[1] if ":" in nombre else "otto"
            if clave in SPRITES_PERSONA:
                p = SPRITES_PERSONA[clave]
                return persona_suave(int(self.W * 0.20), camisa=p["shirt"],
                                     pantalon=p["pants"], cabello=p["hair"])
            # cualquier otro tipo de personaje, con dibujar_personaje
            from PIL import Image as _Image
            alto = int(self.W * 0.20 * 1.4)
            tmp = _Image.new("RGBA", (int(self.W * 0.20), alto), (0, 0, 0, 0))
            dd = ImageDraw.Draw(tmp)
            dibujar_personaje(dd, int(self.W * 0.10), alto - 4,
                              s=self.W * 0.20 / 160.0, t=0.0, tipo=clave,
                              expresion="contento", pose="pie")
            return tmp
        if nombre in OBJETOS:
            from PIL import Image as _Image
            lado = int(self.W * 0.28)
            tmp = _Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
            dd = ImageDraw.Draw(tmp)
            dibujar_objeto(dd, nombre, lado // 2, lado // 2, s=lado / 100.0, t=0.0)
            return tmp
        if nombre in SPRITES_OBJETO:
            fraccion = {"libreta": 0.28, "telefono": 0.22, "calculadora": 0.25,
                        "mapa": 0.45, "papel": 0.30, "llave": 0.25}[nombre]
            return objeto_suave(nombre, int(self.W * fraccion))
        if nombre == "equipo":
            return None
        raise ValueError(f"Sprite retro desconocido: {nombre}")

    # -- fondo ----------------------------------------------------------------
    def fondo(self, t):
        if self._fondo_cache is None:
            # el degradado con dithering es estático; las estrellas se mueven
            self._fondo_cache = fondo_estrellado(self.W, self.H, 0,
                                                 pixel=self.pixel)
        img = self._fondo_cache.copy()
        # capa de estrellas en movimiento (parallax) sobre el fondo base
        d = ImageDraw.Draw(img)
        rnd = random.Random(99)
        for capa, (n, vel, alfa) in enumerate([(40, 1.5, 140), (30, 4.0, 200),
                                               (16, 10.0, 255)]):
            for _ in range(n):
                sx = rnd.uniform(0, self.W)
                sy = rnd.uniform(0, self.H)
                fase = rnd.uniform(0, 6.28)
                dx = (vel * t * self.f) % self.W
                x = int((sx + dx) % self.W)
                y = int(sy)
                brillo = 0.55 + 0.45 * math.sin(2 * math.pi * t / 2.0 + fase)
                col = (int(255 * brillo), int(255 * brillo), int(255 * brillo))
                d.point((x, y), fill=col)
        return img

    # -- texto ------------------------------------------------------------------
    def _subtitulo(self, d, texto, y_centro, tamano=42, max_ancho=None,
                   fade=1.0):
        """Subtítulo blanco con contorno, centrado, en varias líneas."""
        f = self._font(tamano)
        max_ancho = max_ancho or int(self.W * 0.88)
        lineas = wrap_text(texto, f, max_ancho)
        th = self._ft(52)
        y = y_centro - len(lineas) * th / 2
        for linea in lineas:
            bb = d.textbbox((0, 0), linea, font=f)
            x = self.W // 2 - (bb[2] + bb[0]) / 2
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                d.text((x + dx * self.f, y + dy * self.f), linea, font=f,
                       fill=(20, 16, 45, int(255 * fade)))
            d.text((x, y), linea, font=f, fill=(255, 255, 255, int(255 * fade)))
            y += th
        return y

    def _etiqueta(self, d, texto, cx, y, fade=1.0):
        """Píldora oscura con texto blanco (etiqueta de definición)."""
        f = self._font(34)
        pad = self._ft(18)
        bb = d.textbbox((0, 0), texto, font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        x0 = cx - tw / 2 - pad
        x1 = cx + tw / 2 + pad
        y0, y1 = y, y + th + pad * 2
        d.rounded_rectangle([x0, y0, x1, y1], radius=self._ft(40),
                            fill=(43, 43, 58, int(230 * fade)),
                            outline=(255, 255, 255, int(255 * fade)),
                            width=max(1, int(3 * self.f)))
        d.text((cx - tw / 2, y + pad), texto, font=f,
               fill=(255, 255, 255, int(255 * fade)))

    def _pegar(self, img, sprite, cx, cy):
        if sprite is None:
            return
        img.paste(sprite, (int(cx - sprite.width / 2), int(cy - sprite.height / 2)),
                  sprite)

    # -- escenas ------------------------------------------------------------------
    def fotograma(self, escena, t, dur):
        """Un fotograma retro (interno) para la escena dada."""
        tipo = escena["tipo"]
        if escena.get("escenario"):
            img = fondo_escenario(escena["escenario"], self.W, self.H, t)
        else:
            img = self.fondo(t)
        d = ImageDraw.Draw(img)
        if tipo == "portada":
            self._portada(img, d, escena, t, dur)
        elif tipo == "intro":
            self._intro(img, d, escena, t, dur)
        elif tipo == "tarjeta":
            self._tarjeta(img, d, escena, t, dur)
        elif tipo == "definicion":
            self._definicion(img, d, escena, t, dur)
        elif tipo == "fundido":
            self._fundido(img, d, escena, t, dur)
        else:
            raise ValueError(f"Escena retro desconocida: {tipo}")
        if self.pixel:
            img = img.resize((720, 1280), Image.NEAREST)
        return img.convert("RGB")

    def _portada(self, img, d, escena, t, dur):
        W, H = self.W, self.H
        # rueda girando detrás del cerebro
        rueda = self.sprite("rueda", angulo=t * 10, diametro=0.44)
        self._pegar(img, rueda, W / 2, H * 0.30)
        # cerebro flotando y parpadeando
        bob = 6 * math.sin(2 * math.pi * t / 1.6) * self.f
        blink_on = (t % 3.4) < 0.15
        cerebro = self.sprite("cerebro", blink=blink_on)
        self._pegar(img, cerebro, W / 2, H * 0.30 + bob)
        # destellos de ideas
        for i in range(5):
            sx = W * (0.2 + 0.15 * i) + 8 * math.sin(2 * math.pi * t / 1.2 + i)
            sy = H * 0.30 - 60 * self.f - i * 14 * self.f - 12 * math.sin(
                2 * math.pi * t / 0.8 + i * 1.3) * self.f
            r = max(1, int(3 * self.f))
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 220, 100))
        # título por letras con entrada escalonada
        titulo = escena.get("titulo", [])
        y_tit = H * 0.58
        f_tit = self._font(64)
        for li, linea in enumerate(titulo):
            colores = [WHEEL_COLORS[i % len(WHEEL_COLORS)] for i in range(len(linea))]
            ancho = sum(d.textbbox((0, 0), ch, font=f_tit)[2] for ch in linea)
            x = W / 2 - ancho / 2
            y = y_tit + li * self._ft(78)
            for ci, ch in enumerate(linea):
                ap = 0.15 + ci * 0.06 + li * 0.3
                sc = ease_out_back(clamp((t - ap) / 0.35, 0, 1))
                if sc <= 0:
                    continue
                f_ch = self._font(int(64 * sc)) if self.pixel else f_tit
                col = colores[ci]
                d.text((x, y - (1 - sc) * 20 * self.f), ch, font=f_ch, fill=col)
                x += d.textbbox((0, 0), ch, font=f_tit)[2]
        # gancho (pregunta) con fundido y deslizamiento
        if "gancho" in escena:
            gancho = escena["gancho"]
            ap = escena.get("gancho_en", 0.8)
            fade = clamp((t - ap) / 0.6, 0, 1)
            if fade > 0:
                self._subtitulo(d, gancho, H * 0.88, tamano=42, fade=fade)

    def _intro(self, img, d, escena, t, dur):
        W, H = self.W, self.H
        fade = clamp(t / 0.5, 0, 1)
        self._subtitulo(d, escena["subtitulo"], H * 0.28, tamano=42, fade=fade)
        sprite = escena.get("sprite", "cerebro")
        if sprite == "equipo":
            self._equipo(img, d, t, W / 2, H * 0.62, 1.0)
        else:
            sp = self.sprite(sprite, blink=(t % 3.4) < 0.15)
            bob = 5 * math.sin(2 * math.pi * t / 1.6) * self.f
            self._pegar(img, sp, W / 2, H * 0.62 + bob)

    def _tarjeta(self, img, d, escena, t, dur):
        W, H = self.W, self.H
        # icono rebotando arriba
        icono = escena.get("icono", "libreta")
        rebote = abs(math.sin(2 * math.pi * t / 1.1)) * -14 * self.f
        sp = self.sprite(icono)
        self._pegar(img, sp, W / 2, H * 0.30 + rebote)
        # burbuja bicolor con el título en 2 líneas
        l1, l2 = escena.get("titulo", ["", ""])
        c1 = tuple(escena.get("color1", [255, 107, 157]))
        c2 = tuple(escena.get("color2", [255, 190, 80]))
        f = self._font(76)
        w1 = d.textbbox((0, 0), l1, font=f)[2]
        w2 = d.textbbox((0, 0), l2, font=f)[2]
        bw = max(w1, w2) + self._ft(72)
        bh = self._ft(190)
        bx0 = W / 2 - bw / 2
        by0 = H * 0.52
        d.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=self._ft(40),
                            fill=BG_PASTEL, outline=INK, width=max(2, self._ft(4)))
        pop1 = ease_out_back(clamp((t - 0.15) / 0.4, 0, 1))
        pop2 = ease_out_back(clamp((t - 0.35) / 0.4, 0, 1))
        if pop1 > 0:
            d.text((W / 2 - w1 / 2, by0 + self._ft(28) * pop1), l1, font=f, fill=c1)
        if pop2 > 0:
            d.text((W / 2 - w2 / 2, by0 + self._ft(100) * pop2), l2, font=f, fill=c2)

    def _definicion(self, img, d, escena, t, dur):
        W, H = self.W, self.H
        fade = clamp(t / 0.5, 0, 1)
        self._subtitulo(d, escena["subtitulo"], H * 0.24, tamano=42, fade=fade)
        sprite = escena.get("sprite", "cerebro")
        if sprite == "equipo":
            self._equipo(img, d, t, W / 2, H * 0.58, 1.0)
        else:
            sp = self.sprite(sprite, blink=(t % 3.4) < 0.15)
            bob = 5 * math.sin(2 * math.pi * t / 1.6) * self.f
            self._pegar(img, sp, W / 2, H * 0.58 + bob)
        if "etiqueta" in escena:
            self._etiqueta(d, escena["etiqueta"], W / 2, H * 0.86, fade=fade)

    def _equipo(self, img, d, t, cx, cy, escala):
        """Tres personas juntas (trabajo en equipo), con parpadeo escalonado."""
        for i, clave in enumerate(["otto", "persona", "clark"]):
            dx = (i - 1) * self.W * 0.16
            blink_on = ((t + i * 0.5) % 3.4) < 0.15
            sp = self.sprite(f"persona:{clave}", blink=blink_on)
            self._pegar(img, sp, cx + dx, cy)

    def _fundido(self, img, d, escena, t, dur):
        a = int(255 * math.sin(math.pi * clamp(t / dur, 0, 1)))
        overlay = Image.new("RGB", (self.W, self.H), (0, 0, 0))
        img.paste(Image.blend(img.convert("RGB"), overlay, a / 255.0))


def renderizar_escena(estilo, escena, t, dur):
    """Un fotograma (720x1280 RGB) para cualquier estilo."""
    if estilo == "aprendiz":
        return escena_aprendiz(escena, t, dur)
    retro = Retro(estilo)
    return retro.fotograma(escena, t, dur)
