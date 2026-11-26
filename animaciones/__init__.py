# -*- coding: utf-8 -*-
"""Framework reutilizable para programar videos animados (PIL + ffmpeg).

Estilos: aprendiz, alebrigma, snes (16 bits), nes (8 bits).
Cada video nuevo es solo un spec.json; el dibujo ya está escrito.
"""
from .estilos import REGLAS_ESTILO, renderizar_escena, Retro
from .spec import cargar_spec, validar_spec, duraciones_escenas, guion_txt
from .audio import TTS, generar_musica, mezclar

__all__ = ["REGLAS_ESTILO", "renderizar_escena", "Retro", "cargar_spec",
           "validar_spec", "duraciones_escenas", "guion_txt", "TTS",
           "generar_musica", "mezclar"]
