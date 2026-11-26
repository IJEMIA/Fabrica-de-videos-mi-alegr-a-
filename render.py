# -*- coding: utf-8 -*-
"""Renderizador por línea de comandos.

Uso:
    python3 render.py videos/<slug>/spec.json [--salida video.mp4]
                                              [--audio-dir audios/]
                                              [--tts-backend edge|comando|ninguno]
                                              [--voz dalia|jorge]
                                              [--velocidad 1.0]
                                              [--sin-musica]
                                              [--solo-fotogramas DIR]
                                              [--fps 15]

El pipeline es:
  1. Carga y valida el spec.
  2. Narra cada escena (edge-tts, o reutiliza mp3 de --audio-dir, o sin voz).
  3. Calcula la duración de cada escena (audio + 0.4 s + 0.4 s).
  4. Renderiza los fotogramas con PIL (15 fps) y codifica el video con ffmpeg.
  5. Mezcla narración + música de pads (si el spec la pide) y une audio y video.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from animaciones.audio import (TTS, duracion_audio, generar_musica, mezclar,
                               unir_video_audio)
from animaciones.estilos import renderizar_escena
from animaciones.spec import (cargar_spec, duraciones_escenas, guion_txt)

FPS = 15
SALIDA_FPS = 30


def _nombre_audio(i, escena):
    rotulo = (escena.get("rotulo") or " ".join(escena.get("titulo", []))
              or escena.get("tipo", "escena"))
    limpio = "".join(c if c.isalnum() else "_" for c in rotulo)[:24].strip("_")
    return f"{i:02d}_{limpio or 'escena'}.mp3"


def renderizar(spec_path, salida=None, audio_dir=None, tts_backend="edge",
               voz="dalia", velocidad=1.0, tts_comando=None, sin_musica=False,
               solo_fotogramas=None, fps=FPS, trabajo=None):
    """Renderiza un spec completo. Devuelve (ruta_mp4, duracion_total, info)."""
    spec = cargar_spec(spec_path)
    slug = os.path.basename(os.path.dirname(os.path.abspath(spec_path)))
    salida = salida or f"{slug}.mp4"
    trabajo = trabajo or os.path.join(os.path.dirname(os.path.abspath(salida)),
                                     f".trabajo-{slug}")
    os.makedirs(trabajo, exist_ok=True)
    frames_dir = os.path.join(trabajo, "frames")
    audio_dir_out = os.path.join(trabajo, "audio")
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(audio_dir_out, exist_ok=True)

    estilo = spec["estilo"]
    musica = spec.get("musica", False) and not sin_musica

    # pool de audios disponibles para reutilizar (cada archivo, una sola vez)
    pool_audio = []
    if audio_dir and os.path.isdir(audio_dir):
        pool_audio = sorted(f for f in os.listdir(audio_dir) if f.endswith(".mp3"))

    def _reutilizar(i, nombre):
        """Busca un mp3 existente para la escena i: nombre exacto, luego
        prefijo 00_ (base 0) o 01_ (base 1). Lo saca del pool."""
        for cand in (nombre, f"{i:02d}_", f"{i + 1:02d}_"):
            for f in list(pool_audio):
                if cand == nombre:
                    if f == nombre:
                        pool_audio.remove(f)
                        return os.path.join(audio_dir, f)
                elif f.startswith(cand):
                    pool_audio.remove(f)
                    return os.path.join(audio_dir, f)
        return None

    # 1) Narración ------------------------------------------------------------
    tts = TTS(backend=tts_backend, voz=voz, velocidad=velocidad,
              comando=tts_comando)
    duraciones_audio = []
    rutas_audio = []
    for i, esc in enumerate(spec["escenas"]):
        nar = esc.get("narracion", "").strip()
        nombre = _nombre_audio(i, esc)
        destino = os.path.join(audio_dir_out, nombre)
        reutilizado = _reutilizar(i, nombre) if audio_dir else None
        if reutilizado:
            shutil.copy(reutilizado, destino)
        elif nar and tts_backend != "ninguno":
            print(f"  narrando escena {i + 1}/{len(spec['escenas'])}: {nar[:50]}...")
            tts.hablar(nar, destino)
        if nar and os.path.exists(destino):
            d = duracion_audio(destino)
        else:
            d = 0.0
        duraciones_audio.append(d)
        rutas_audio.append(destino if os.path.exists(destino) else None)

    durs = duraciones_escenas(spec, duraciones_audio)
    total = round(sum(durs), 2)
    print(f"  escenas: {len(durs)}  duraciones: {durs}  total: {total:.1f} s")

    # 2) Fotogramas -------------------------------------------------------------
    if solo_fotogramas:
        os.makedirs(solo_fotogramas, exist_ok=True)
    n_frame = 0
    t_acum = 0.0
    for i, (esc, dur) in enumerate(zip(spec["escenas"], durs)):
        n = max(1, int(round(dur * fps)))
        for k in range(n):
            t_local = k / fps
            frame = renderizar_escena(estilo, esc, t_local, dur)
            ruta = os.path.join(frames_dir, f"f{n_frame:05d}.png")
            frame.save(ruta)
            if solo_fotogramas and n_frame % max(1, fps) == 0:
                frame.save(os.path.join(solo_fotogramas, f"esc{i + 1}_t{t_local:.1f}.png"))
            n_frame += 1
        t_acum += dur
    print(f"  fotogramas: {n_frame} a {fps} fps")

    video_sin_audio = os.path.join(trabajo, "video_sin_audio.mp4")
    cmd = ["ffmpeg", "-y", "-v", "error", "-framerate", str(fps),
           "-i", os.path.join(frames_dir, "f%05d.png"),
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(SALIDA_FPS),
           video_sin_audio]
    subprocess.run(cmd, check=True)

    # 3) Audio -----------------------------------------------------------------
    segmentos = []
    t_ms = 0
    for ruta, dur in zip(rutas_audio, durs):
        if ruta:
            segmentos.append((ruta, int(round((t_ms + 0.4) * 1000))))
        t_ms += dur
    musica_wav = None
    if musica:
        musica_wav = os.path.join(trabajo, "musica.wav")
        generar_musica(total, musica_wav)
    if segmentos or musica_wav:
        audio_final = os.path.join(trabajo, "audio_final.wav")
        mezclar(segmentos, musica_wav, audio_final, total)
        unir_video_audio(video_sin_audio, audio_final, salida, total)
    else:
        shutil.copy(video_sin_audio, salida)

    # guion al lado del video
    guion_path = os.path.splitext(salida)[0] + "-guion.txt"
    with open(guion_path, "w", encoding="utf-8") as f:
        f.write(guion_txt(spec))

    info = {"estilo": estilo, "escenas": len(durs), "duraciones": durs,
            "total_s": total, "musica": musica, "salida": salida,
            "guion": guion_path}
    return salida, total, info


def main():
    ap = argparse.ArgumentParser(description="Renderiza un video desde su spec.json")
    ap.add_argument("spec", help="Ruta al spec.json del video")
    ap.add_argument("--salida", help="Ruta del mp4 de salida")
    ap.add_argument("--audio-dir", help="Carpeta con mp3 de narración ya generados")
    ap.add_argument("--tts-backend", default="edge",
                    choices=["edge", "comando", "ninguno"],
                    help="Motor de narración (por defecto: edge, gratuito)")
    ap.add_argument("--voz", default="dalia",
                    help="Voz edge-tts: dalia (es-MX-DaliaNeural) o jorge (es-MX-JorgeNeural)")
    ap.add_argument("--velocidad", type=float, default=1.0,
                    help="Velocidad de la voz (1.0 = normal; 0.9 = más pausada)")
    ap.add_argument("--tts-comando", help="Comando TTS externo con {texto} y {salida}")
    ap.add_argument("--sin-musica", action="store_true")
    ap.add_argument("--solo-fotogramas", help="Guarda fotogramas de muestra en esta carpeta")
    ap.add_argument("--fps", type=int, default=FPS)
    args = ap.parse_args()

    salida, total, info = renderizar(
        args.spec, salida=args.salida, audio_dir=args.audio_dir,
        tts_backend=args.tts_backend, voz=args.voz, velocidad=args.velocidad,
        tts_comando=args.tts_comando, sin_musica=args.sin_musica,
        solo_fotogramas=args.solo_fotogramas, fps=args.fps)
    print(json.dumps(info, indent=2, ensure_ascii=False))
    print(f"OK: {salida}  ({total:.1f} s)")


if __name__ == "__main__":
    main()
