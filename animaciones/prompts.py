# -*- coding: utf-8 -*-
"""Prompt de Groq para la Fábrica de videos Mi Alegría (módulo compartido).

Lo usan dos clientes, para que el prompt sea UNO solo y no se duplique:
  - app/app.py (la app Gradio local),
  - scripts/generar_spec.py (el workflow de GitHub Actions).

El catálogo viene de animaciones/catalogo.py (nunca se duplica aquí).
"""
from .catalogo import catalogo_para_groq

MODELO_GROQ = "llama-3.3-70b-versatile"
ENLACE_CLAVE = "https://console.groq.com/keys"

ESQUEMA = """ESQUEMA EXACTO DEL SPEC (JSON, sin markdown ni explicaciones):

Estilo "aprendiz" (cartoon 2D, fondo blanco con mancha menta):
{
  "titulo": "Título del video",
  "estilo": "aprendiz",
  "musica": false,
  "voz": "dalia",
  "velocidad": 0.95,
  "escenas": [
    {"rotulo": "TÍTULO EN MAYÚSCULAS", "narracion": "Texto que se escucha (6 a 10 segundos al leerlo en voz alta).", "escenario": "parque",
     "elementos": [
       {"tipo": "personaje", "personaje": "doctora", "x": 360, "y": 1080, "escala": 1.0, "pose": "pie", "expresion": "contento"},
       {"tipo": "objeto", "nombre": "arbol", "x": 200, "y": 800, "escala": 1.0},
       {"tipo": "texto", "texto": "50", "x": 360, "y": 500, "tamano": 120, "fuente": "hand"},
       {"tipo": "lista", "items": ["Punto uno", "Punto dos"], "x": 90, "y": 580, "tamano": 44, "intervalo": 2.0, "check": true}
     ]}
  ]
}
Coordenadas del lienzo aprendiz: 720 de ancho x 1280 de alto. El suelo está en y=1080.
Tipos de elemento: personaje, objeto, texto, texto_grande, lista, nota,
bolsa_dinero, grupo, lampara_calle, lampara_mano, camara, mapa, hoja, luna,
palomita, cancha, balon_futbol, balon_basquet, silbato, corazon, jupiter,
telescopio, estrella, nube, flotador, cazador, termometro, radiacion,
paraguas, europa, destellos.

Estilos retro ("alebrigma", "snes", "nes": fondo oscuro estrellado, escenas
de tipo portada/intro/tarjeta/definicion/fundido):
{
  "titulo": "Título del video",
  "estilo": "snes",
  "musica": true,
  "voz": "dalia",
  "velocidad": 1.0,
  "escenas": [
    {"tipo": "portada", "titulo": ["LÍNEA 1", "LÍNEA 2"], "gancho": "¿Pregunta gancho?", "narracion": "¿Pregunta gancho?"},
    {"tipo": "intro", "subtitulo": "Frase que se escucha y se lee en pantalla.", "sprite": "cerebro", "narracion": "Frase que se escucha y se lee en pantalla."},
    {"tipo": "tarjeta", "titulo": ["PALABRA 1", "PALABRA 2"], "color1": [74, 222, 128], "color2": [255, 107, 157], "icono": "libreta", "narracion": "Palabra 1 palabra 2."},
    {"tipo": "definicion", "subtitulo": "Definición o ejemplo.", "sprite": "persona:otto", "etiqueta": "Etiqueta corta", "narracion": "Definición o ejemplo."},
    {"tipo": "fundido", "duracion": 0.5}
  ]
}
En retro, "sprite"/"icono" es un nombre del catálogo (cerebro, libreta,
telefono, calculadora, mapa, papel, llave, equipo, persona:otto,
persona:doctora, arbol, casa, sol...). "escenario" también se puede poner
en cualquier escena retro (por ejemplo "bosque" o "espacio").
"""

REGLAS = """REGLAS (obligatorias):
- Devuelve SOLO el JSON del spec, sin texto antes ni después, sin ```json.
- Usa EXCLUSIVAMENTE los datos que da el usuario. No inventes cifras,
  nombres, fechas, lugares ni hechos. Si algo falta, no lo inventes: usa
  solo lo que hay.
- Lo hipotético va marcado como hipotético ("imaginaron", "si existiera",
  "según los científicos", "podría").
- La narración va en español neutro de México, en frases cortas y claras.
- El rótulo de cada escena va en MAYÚSCULAS, corto (máximo 4 palabras por línea).
- Cada escena lleva su narración completa (lo que se escucha). La duración
  de cada escena la marca su narración (unos 6-10 segundos por escena).
- El número de escenas depende de la duración pedida: unas 4 escenas para
  30 segundos, 7-8 para 1 minuto, 11 para 1 minuto y medio, 15 para
  2 minutos y 22 para 3 minutos.
- Estructura recomendada: gancho (pregunta) -> tema -> puntos principales
  (uno por escena) -> cierre con llamada a la acción, si el contenido la trae.
- En aprendiz, reparte los elementos por la escena sin tapar el rótulo
  (el rótulo ocupa la parte superior, y=100 a y=350). El suelo es y=1080.
- No uses recursos que no estén en el catálogo de abajo.
"""


def construir_prompt(tema, contenido, estilo, duracion_s):
    """Prompt completo para Groq: tema + contenido + estilo + duración
    + esquema + reglas + catálogo."""
    n_escenas = max(3, round(duracion_s / 8))
    return (
        "Eres un guionista de videos educativos verticales (9:16, estilo TikTok).\n\n"
        f"TEMA: {tema}\n\nCONTENIDO (datos del usuario, úsalos tal cual):\n{contenido}\n\n"
        f"ESTILO: {estilo}\nDURACIÓN OBJETIVO: {duracion_s} segundos "
        f"(unas {n_escenas} escenas).\n\n"
        + ESQUEMA + "\n" + REGLAS + "\n" + catalogo_para_groq()
    )
