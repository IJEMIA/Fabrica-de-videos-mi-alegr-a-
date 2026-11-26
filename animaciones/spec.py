# -*- coding: utf-8 -*-
"""Especificación de video (spec.json): carga, validación y tiempos.

Un spec describe UN video completo: estilo, voz, música y la lista de
escenas. Cada escena lleva su rótulo en pantalla, su texto de narración
y su ilustración. El renderizador calcula la duración de cada escena a
partir de la duración real del audio de narración (+0.4 s de entrada y
+0.4 s de salida), salvo que la escena fije su propia duración.
"""
import json
import os

from .estilos import REGLAS_ESTILO
from .personajes import TIPOS_PERSONAJE
from .iconos import OBJETOS
from .escenarios import ESCENARIOS

LEAD = 0.4   # silencio antes de que empiece la narración de la escena
TAIL = 0.4   # silencio después de que termina

ELEMENTOS_APRENDIZ = {
    "personaje", "lampara_calle", "lampara_mano", "camara", "mapa", "hoja",
    "luna", "palomita", "texto_grande", "texto", "lista", "nota",
    "bolsa_dinero", "grupo", "cancha", "balon_futbol", "balon_basquet",
    "silbato", "corazon", "jupiter", "telescopio", "estrella", "nube",
    "flotador", "cazador", "termometro", "radiacion", "paraguas", "europa",
    "destellos", "objeto",
}
TIPOS_RETRO = {"portada", "intro", "tarjeta", "definicion", "fundido"}
SPRITES_RETRO = {"cerebro", "brazos", "rueda", "equipo", "libreta",
                 "telefono", "calculadora", "mapa", "papel", "llave",
                 "persona:otto", "persona:clark", "persona:chalmers",
                 "persona:persona"}


def cargar_spec(ruta):
    """Carga y valida un spec.json. Devuelve el dict."""
    with open(ruta, encoding="utf-8") as f:
        spec = json.load(f)
    validar_spec(spec)
    return spec


def validar_spec(spec):
    """Valida la estructura de un spec. Lanza ValueError si algo falta."""
    if not isinstance(spec, dict):
        raise ValueError("El spec debe ser un objeto JSON.")
    estilo = spec.get("estilo")
    if estilo not in REGLAS_ESTILO:
        raise ValueError(
            f"Estilo desconocido: {estilo!r}. Estilos: "
            + ", ".join(REGLAS_ESTILO))
    escenas = spec.get("escenas")
    if not escenas or not isinstance(escenas, list):
        raise ValueError("El spec necesita una lista no vacía de 'escenas'.")
    for i, esc in enumerate(escenas):
        if not isinstance(esc, dict):
            raise ValueError(f"Escena {i}: debe ser un objeto.")
        if esc.get("escenario") and esc["escenario"] not in ESCENARIOS:
            raise ValueError(
                f"Escena {i}: escenario desconocido {esc['escenario']!r}. "
                f"Escenarios: {', '.join(sorted(ESCENARIOS))}.")
        if estilo == "aprendiz":
            if "rotulo" not in esc:
                raise ValueError(f"Escena {i} (aprendiz): falta 'rotulo'.")
            for j, el in enumerate(esc.get("elementos", [])):
                if el.get("tipo") not in ELEMENTOS_APRENDIZ:
                    raise ValueError(
                        f"Escena {i}, elemento {j}: tipo desconocido "
                        f"{el.get('tipo')!r}.")
                if el.get("tipo") == "objeto" and el.get("nombre") not in OBJETOS:
                    raise ValueError(
                        f"Escena {i}, elemento {j}: objeto desconocido "
                        f"{el.get('nombre')!r}. Objetos: {', '.join(sorted(OBJETOS))}.")
                if el.get("tipo") == "personaje" and "personaje" in el \
                        and el["personaje"] not in TIPOS_PERSONAJE:
                    raise ValueError(
                        f"Escena {i}, elemento {j}: tipo de personaje "
                        f"desconocido {el['personaje']!r}. Tipos: "
                        f"{', '.join(sorted(TIPOS_PERSONAJE))}.")
        else:
            if esc.get("tipo") not in TIPOS_RETRO:
                raise ValueError(
                    f"Escena {i} ({estilo}): 'tipo' debe ser uno de "
                    + ", ".join(sorted(TIPOS_RETRO)) + f", no {esc.get('tipo')!r}.")
            for campo in ("sprite", "icono"):
                if campo in esc:
                    nombre = esc[campo]
                    base = nombre.split(":")[0]
                    ok = (nombre in SPRITES_RETRO or base in SPRITES_RETRO
                          or nombre.startswith("persona:")
                          or nombre in OBJETOS)
                    if not ok:
                        raise ValueError(
                            f"Escena {i}: sprite desconocido {nombre!r}.")
        if "duracion" in esc and not isinstance(esc["duracion"], (int, float)):
            raise ValueError(f"Escena {i}: 'duracion' debe ser un número.")
    return True


def guion_txt(spec):
    """El guion de narración completo como texto (para grabarlo aparte)."""
    lineas = [f"# {spec.get('titulo', 'Video')}  ({spec.get('estilo')})", ""]
    for i, esc in enumerate(spec["escenas"], 1):
        rotulo = esc.get("rotulo") or " ".join(esc.get("titulo", [])) or esc.get("tipo", "")
        lineas.append(f"[{i}] {rotulo}")
        if esc.get("narracion"):
            lineas.append(esc["narracion"])
        lineas.append("")
    return "\n".join(lineas)


def duraciones_escenas(spec, duraciones_audio):
    """Duración de cada escena: audio + lead + tail, o la fijada en el spec.

    ``duraciones_audio``: lista de duraciones (s) de la narración de cada
    escena, en el mismo orden (0 si la escena no tiene narración).
    """
    durs = []
    for esc, d_audio in zip(spec["escenas"], duraciones_audio):
        if "duracion" in esc:
            durs.append(float(esc["duracion"]))
        elif d_audio and d_audio > 0:
            durs.append(round(d_audio + LEAD + TAIL, 2))
        else:
            durs.append(2.0)
    return durs


def resumen_spec(spec):
    """Resumen en una línea por escena (para mostrarlo en la app)."""
    out = []
    for i, esc in enumerate(spec["escenas"], 1):
        rotulo = esc.get("rotulo") or " ".join(esc.get("titulo", [])) or esc.get("tipo", "")
        nar = (esc.get("narracion") or "")[:60]
        out.append(f"{i}. {rotulo} — {nar}")
    return "\n".join(out)
