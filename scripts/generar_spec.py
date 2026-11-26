# -*- coding: utf-8 -*-
"""Genera el spec.json de un video llamando a Groq (utilidad local por línea
de comandos).

La clave de Groq llega por la variable de entorno GROQ_API_KEY o por
--clave (nunca se guarda en archivos ni se sube al repo).

Uso:
    python3 scripts/generar_spec.py --tema "Iluminando tu futuro" \
        --contenido "Misión: ... Visión: ..." \
        --estilo aprendiz --duracion-segundos 60 --salida salida/spec.json

    # Sin llamar a Groq (para probar el pipeline): escribe un spec mínimo válido.
    python3 scripts/generar_spec.py --tema Prueba --contenido "Dato uno." \
        --estilo aprendiz --duracion-segundos 30 --salida /tmp/spec.json --simular

El prompt es el mismo de la app Gradio (animaciones/prompts.py) y el
catálogo el mismo de animaciones/catalogo.py: no se duplica ninguno.
"""
import argparse
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from animaciones.prompts import MODELO_GROQ, construir_prompt  # noqa: E402
from animaciones.spec import validar_spec  # noqa: E402

ESTILOS = ["aprendiz", "alebrigma", "snes", "nes"]


def generar_con_groq(tema, contenido, estilo, duracion_s, clave):
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
            {"role": "system",
             "content": "Eres un guionista de videos educativos. Devuelves solo JSON válido."},
            {"role": "user",
             "content": construir_prompt(tema, contenido, estilo, duracion_s)},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )
    texto = respuesta.choices[0].message.content
    try:
        spec = json.loads(texto)
    except json.JSONDecodeError as e:
        raise RuntimeError(
            f"Groq devolvió algo que no es JSON válido: {e}\n{texto[:500]}")
    validar_spec(spec)
    return spec


def spec_simulado(tema, estilo):
    """Spec mínimo válido (sin llamar a Groq), solo para probar el pipeline."""
    if estilo == "aprendiz":
        return {
            "titulo": tema or "Video de prueba",
            "estilo": "aprendiz",
            "musica": False,
            "voz": "dalia",
            "velocidad": 1.0,
            "escenas": [
                {"rotulo": "PRUEBA UNO",
                 "narracion": "Esta es la primera escena de prueba.",
                 "escenario": "parque",
                 "elementos": [
                     {"tipo": "personaje", "personaje": "doctora",
                      "x": 360, "y": 1080, "pose": "pie", "expresion": "contento"},
                     {"tipo": "objeto", "nombre": "arbol", "x": 200, "y": 800}]},
                {"rotulo": "PRUEBA DOS",
                 "narracion": "Esta es la segunda escena de prueba.",
                 "escenario": "salon",
                 "elementos": [
                     {"tipo": "personaje", "personaje": "maestro",
                      "x": 360, "y": 1080, "pose": "senalando", "expresion": "contento"}]},
            ],
        }
    return {
        "titulo": tema or "Video de prueba",
        "estilo": estilo,
        "musica": True,
        "voz": "dalia",
        "velocidad": 1.0,
        "escenas": [
            {"tipo": "portada", "titulo": ["PRUEBA"],
             "gancho": "¿Funciona la prueba?",
             "narracion": "¿Funciona la prueba?"},
            {"tipo": "definicion", "subtitulo": "La prueba funciona.",
             "sprite": "cerebro", "etiqueta": "PRUEBA",
             "narracion": "La prueba funciona."},
        ],
    }


def main():
    ap = argparse.ArgumentParser(
        description="Genera el spec.json de un video con Groq.")
    ap.add_argument("--tema", required=True, help="Tema del video")
    ap.add_argument("--contenido", default="",
                    help="Contenido del video (misión, visión, datos o hechos)")
    ap.add_argument("--contenido-archivo",
                    help="Archivo con el contenido (alternativa a --contenido)")
    ap.add_argument("--estilo", default="aprendiz", choices=ESTILOS)
    ap.add_argument("--duracion-segundos", type=int, default=60)
    ap.add_argument("--voz", default="dalia", choices=["dalia", "jorge"])
    ap.add_argument("--musica", action="store_true",
                    help="Música de fondo (pads suaves)")
    ap.add_argument("--salida", required=True, help="Ruta del spec.json")
    ap.add_argument("--clave", default="",
                    help="Clave de Groq (si no, variable GROQ_API_KEY)")
    ap.add_argument("--simular", action="store_true",
                    help="No llamar a Groq: escribe un spec mínimo válido")
    args = ap.parse_args()

    contenido = args.contenido
    if args.contenido_archivo:
        with open(args.contenido_archivo, encoding="utf-8") as f:
            contenido = f.read()
    if not contenido.strip() and not args.simular:
        ap.error("Falta el contenido: usa --contenido o --contenido-archivo.")

    if args.simular:
        spec = spec_simulado(args.tema, args.estilo)
    else:
        clave = (args.clave or "").strip() or os.environ.get("GROQ_API_KEY", "")
        if not clave:
            ap.error("Falta la clave de Groq: pon GROQ_API_KEY en el entorno "
                     "o usa --clave. Consíguela gratis en "
                     "https://console.groq.com/keys")
        spec = generar_con_groq(args.tema, contenido, args.estilo,
                                args.duracion_segundos, clave)

    spec.setdefault("voz", args.voz)
    spec["musica"] = bool(args.musica)
    validar_spec(spec)

    os.makedirs(os.path.dirname(os.path.abspath(args.salida)), exist_ok=True)
    with open(args.salida, "w", encoding="utf-8") as f:
        json.dump(spec, f, ensure_ascii=False, indent=2)
    print(f"OK: spec guardado en {args.salida} "
          f"({len(spec['escenas'])} escenas, estilo {spec['estilo']})")


if __name__ == "__main__":
    main()
