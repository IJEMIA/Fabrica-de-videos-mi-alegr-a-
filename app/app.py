# -*- coding: utf-8 -*-
"""Fábrica de videos Mi Alegría — app web (Gradio).

Flujo:
  1. El usuario pega su clave de Groq (o la guarda en .env) y escribe el
     tema y el contenido del video.
  2. Groq (Llama 3.3 70B) genera el spec JSON del video siguiendo el esquema
     exacto del framework y el catálogo de recursos disponibles.
  3. El spec se muestra para revisarlo/editarlo y se renderiza con el
     framework (PIL + ffmpeg), con narración gratuita de edge-tts
     (es-MX-DaliaNeural o es-MX-JorgeNeural).
  4. El video se muestra y se puede DESCARGAR (botón de descarga del video
     y archivo mp4 explícito).

La clave de Groq NUNCA se commitea: vive en .env (local) o en el campo de
la interfaz. Obtenerla gratis: https://console.groq.com/keys
"""
import json
import os
import sys
import time

# El framework vive en la raíz del repo (un nivel arriba de app/).
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from animaciones.catalogo import catalogo_para_groq  # noqa: E402
from animaciones.spec import validar_spec  # noqa: E402
from render import renderizar  # noqa: E402

MODELO_GROQ = "llama-3.3-70b-versatile"
ENLACE_CLAVE = "https://console.groq.com/keys"
SALIDAS = os.path.join(RAIZ, "salidas")
os.makedirs(SALIDAS, exist_ok=True)

DURACIONES = {
    "30 segundos": 30,
    "1 minuto": 60,
    "1 minuto y medio": 90,
    "2 minutos": 120,
    "3 minutos": 180,
}

# ---------------------------------------------------------------------------
# Clave de Groq
# ---------------------------------------------------------------------------
def _leer_env(ruta):
    datos = {}
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea or linea.startswith("#") or "=" not in linea:
                    continue
                k, v = linea.split("=", 1)
                datos[k.strip()] = v.strip().strip('"').strip("'")
    return datos


def obtener_clave(campo=""):
    """Clave de Groq: primero el campo de la interfaz, luego .env, luego
    la variable de entorno GROQ_API_KEY. Devuelve '' si falta."""
    if campo and campo.strip():
        return campo.strip()
    env = _leer_env(os.path.join(RAIZ, ".env"))
    if env.get("GROQ_API_KEY"):
        return env["GROQ_API_KEY"]
    return os.environ.get("GROQ_API_KEY", "")


def guardar_clave(clave):
    """Guarda la clave en .env (local, nunca se commitea)."""
    clave = (clave or "").strip()
    if not clave:
        return "Pega tu clave primero. Consíguela gratis en " + ENLACE_CLAVE
    ruta = os.path.join(RAIZ, ".env")
    lineas = []
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            lineas = [l for l in f if not l.strip().startswith("GROQ_API_KEY=")]
    lineas.append(f"GROQ_API_KEY={clave}\n")
    with open(ruta, "w", encoding="utf-8") as f:
        f.writelines(lineas)
    return "Clave guardada en .env (solo en esta computadora, no se sube al repo)."


# ---------------------------------------------------------------------------
# Prompt de Groq
# ---------------------------------------------------------------------------
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
    n_escenas = max(3, round(duracion_s / 8))
    return (
        "Eres un guionista de videos educativos verticales (9:16, estilo TikTok).\n\n"
        f"TEMA: {tema}\n\nCONTENIDO (datos del usuario, úsalos tal cual):\n{contenido}\n\n"
        f"ESTILO: {estilo}\nDURACIÓN OBJETIVO: {duracion_s} segundos "
        f"(unas {n_escenas} escenas).\n\n"
        + ESQUEMA + "\n" + REGLAS + "\n" + catalogo_para_groq()
    )


def generar_spec_con_groq(tema, contenido, estilo, duracion_s, clave):
    """Llama a Groq y devuelve el spec (dict). Lanza RuntimeError si falla."""
    try:
        from groq import Groq
    except ImportError as e:
        raise RuntimeError(
            "Falta el paquete groq. Instala las dependencias con:\n"
            "    pip install -r requirements.txt") from e
    cliente = Groq(api_key=clave)
    respuesta = cliente.chat.completions.create(
        model=MODELO_GROQ,
        messages=[
            {"role": "system", "content": "Eres un guionista de videos educativos. Devuelves solo JSON válido."},
            {"role": "user", "content": construir_prompt(tema, contenido, estilo, duracion_s)},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )
    texto = respuesta.choices[0].message.content
    try:
        spec = json.loads(texto)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Groq devolvió algo que no es JSON válido: {e}\n{texto[:500]}")
    validar_spec(spec)
    return spec


# ---------------------------------------------------------------------------
# Renderizado
# ---------------------------------------------------------------------------
def _slug(tema):
    limpio = "".join(c.lower() if c.isalnum() else "-" for c in (tema or "video"))
    limpio = "-".join(p for p in limpio.split("-") if p)[:40]
    return limpio or "video"


def renderizar_spec(spec, voz="dalia", con_musica=None):
    """Renderiza un spec (dict) y devuelve (ruta_mp4, info)."""
    slug = _slug(spec.get("titulo", "video"))
    marca = time.strftime("%Y%m%d-%H%M%S")
    spec_path = os.path.join(SALIDAS, f"{slug}-{marca}-spec.json")
    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
    salida = os.path.join(SALIDAS, f"{slug}-{marca}.mp4")
    musica = spec.get("musica", False) if con_musica is None else con_musica
    spec_render = dict(spec)
    spec_render["musica"] = musica
    # renderizar() espera un archivo; escribimos el spec ajustado
    with open(spec_path, "w", encoding="utf-8") as f:
        json.dump(spec_render, f, ensure_ascii=False, indent=2)
    ruta, total, info = renderizar(
        spec_path, salida=salida,
        # Backend de voz: edge por defecto; se puede forzar con la variable
        # FABRICA_TTS_BACKEND (edge | comando | ninguno) para probar la app
        # sin voz o en redes donde edge-tts no llega.
        tts_backend=os.environ.get("FABRICA_TTS_BACKEND", "edge"),
        voz=voz, velocidad=float(spec.get("velocidad", 1.0)))
    return ruta, total, info


# ---------------------------------------------------------------------------
# Acciones de la interfaz
# ---------------------------------------------------------------------------
def accion_generar(tema, contenido, estilo, duracion_txt, voz, con_musica, clave_campo):
    """Genera el spec con Groq y renderiza el video. Devuelve
    (video, archivo, spec_json, estado)."""
    clave = obtener_clave(clave_campo)
    if not clave:
        return (None, None, "",
                "Falta tu clave de Groq. Pégala arriba o guárdala en .env. "
                f"Consíguela gratis en {ENLACE_CLAVE}")
    if not (tema or "").strip() or not (contenido or "").strip():
        return (None, None, "", "Escribe el tema y el contenido del video.")
    duracion_s = DURACIONES.get(duracion_txt, 60)
    try:
        spec = generar_spec_con_groq(tema, contenido, estilo, duracion_s, clave)
    except Exception as e:
        return (None, None, "", f"No se pudo generar el guion con Groq: {e}")
    spec_txt = json.dumps(spec, ensure_ascii=False, indent=2)
    try:
        ruta, total, info = renderizar_spec(spec, voz=voz, con_musica=con_musica)
    except Exception as e:
        return (None, None, spec_txt,
                f"El guion salió bien, pero el renderizado falló: {e}")
    estado = (f"Listo: {spec.get('titulo', 'video')} — {total:.1f} s, "
              f"{len(spec['escenas'])} escenas, estilo {estilo}. "
              f"Descarga el video con el botón de abajo.")
    return (ruta, ruta, spec_txt, estado)


def accion_renderizar(spec_txt, voz, con_musica):
    """Renderiza el spec que está en el cuadro de texto (ya editado)."""
    try:
        spec = json.loads(spec_txt)
        validar_spec(spec)
    except Exception as e:
        return (None, None, f"El spec no es válido: {e}")
    try:
        ruta, total, info = renderizar_spec(spec, voz=voz, con_musica=con_musica)
    except Exception as e:
        return (None, None, f"El renderizado falló: {e}")
    estado = (f"Listo: {spec.get('titulo', 'video')} — {total:.1f} s, "
              f"{len(spec['escenas'])} escenas. Descarga el video con el botón de abajo.")
    return (ruta, ruta, estado)


# ---------------------------------------------------------------------------
# Interfaz
# ---------------------------------------------------------------------------
def construir_interfaz():
    import gradio as gr

    with gr.Blocks(title="Fábrica de videos Mi Alegría") as demo:
        gr.Markdown(
            "# 🎬 Fábrica de videos Mi Alegría\n"
            "Escribe el tema y el contenido, y la app genera el video sola: "
            "Groq escribe el guion y el framework lo dibuja, lo narra y lo "
            "convierte en mp4. **El video se descarga** con el botón de descarga.\n\n"
            "📍 **Estás dentro de la app:** si la abriste en tu computadora, la "
            "dirección es **http://localhost:7860**. Si la abriste en Hugging Face, "
            "la dirección es la del Space (arriba, en el navegador)."
        )
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown(
                    "### 🔑 Tu clave de Groq\n"
                    "La clave es gratis y solo vive en tu computadora (archivo `.env`) "
                    "o en este campo: nunca se sube al repo.\n\n"
                    f"👉 [Obtener tu clave gratis]({ENLACE_CLAVE}) "
                    "(console.groq.com/keys: crea una cuenta, entra a API Keys y "
                    "copia la clave que empieza por `gsk_`.)"
                )
                clave_txt = gr.Textbox(
                    label="Tu clave de Groq", type="password",
                    placeholder="gsk_...",
                    info="Si la dejas vacía, la app usa la del archivo .env.")
                guardar_btn = gr.Button("💾 Guardar clave en .env", size="sm")
                clave_estado = gr.Textbox(label="Clave", interactive=False, value="")
                guardar_btn.click(guardar_clave, inputs=[clave_txt], outputs=[clave_estado])

                gr.Markdown("### 📝 Tu video")
                tema_txt = gr.Textbox(label="Tema", placeholder="Ej.: Iluminando tu futuro")
                contenido_txt = gr.Textbox(
                    label="Contenido (misión, visión, datos o hechos)",
                    lines=8,
                    placeholder=("Ej.:\nMisión: dotar de lámparas ahorradoras y vigilancia a Tlatelolco.\n"
                                 "Visión: Cuauhtémoc, una de las alcaldías más seguras y sustentables.\n"
                                 "Objetivo: 50 lámparas nuevas y 4 vigilantes.\n"
                                 "Recursos: 50,000 pesos y 5 voluntarios."))
                estilo_dd = gr.Dropdown(
                    label="Estilo",
                    choices=["aprendiz", "alebrigma", "snes", "nes"],
                    value="aprendiz",
                    info=("aprendiz: cartoon 2D fondo blanco · alebrigma: formas suaves "
                          "fondo morado · snes: pixel art 16 bits · nes: pixel art 8 bits"))
                duracion_dd = gr.Dropdown(
                    label="Duración",
                    choices=list(DURACIONES.keys()),
                    value="1 minuto",
                    info="A más duración, más escenas y más tarda el renderizado.")
                voz_dd = gr.Dropdown(
                    label="Voz de la narración",
                    choices=["dalia", "jorge"],
                    value="dalia",
                    info="Dalia (femenina) o Jorge (masculina), español neutro de México.")
                musica_chk = gr.Checkbox(
                    label="Música de fondo (pads suaves)",
                    value=False,
                    info="Recomendada en alebrigma/snes/nes; en aprendiz el original no lleva música.")
                generar_btn = gr.Button("🎬 Generar video", variant="primary", size="lg")
            with gr.Column(scale=1):
                gr.Markdown("### 👀 Resultado")
                estado_txt = gr.Textbox(label="Estado", interactive=False, value="")
                video_out = gr.Video(label="Video generado", interactive=False)
                archivo_out = gr.File(label="⬇️ Descargar el video (mp4)")
                spec_txt = gr.Textbox(
                    label="Spec JSON (puedes editarlo y volver a renderizar)",
                    lines=18, interactive=True)
                render_btn = gr.Button("🔄 Renderizar con este spec", size="sm")

        generar_btn.click(
            accion_generar,
            inputs=[tema_txt, contenido_txt, estilo_dd, duracion_dd, voz_dd,
                    musica_chk, clave_txt],
            outputs=[video_out, archivo_out, spec_txt, estado_txt])
        render_btn.click(
            accion_renderizar,
            inputs=[spec_txt, voz_dd, musica_chk],
            outputs=[video_out, archivo_out, estado_txt])
    return demo


def main():
    demo = construir_interfaz()
    print("Fábrica de videos Mi Alegría — abre http://localhost:7860 en tu navegador.")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)


if __name__ == "__main__":
    main()
