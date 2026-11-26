# -*- coding: utf-8 -*-
"""Audio: narración TTS, música de pads y mezcla final con ffmpeg.

Narración:
- ``edge`` (por defecto, gratuito, sin clave): Microsoft Edge TTS
  (``edge-tts``), voz en español neutro de México: ``es-MX-DaliaNeural``
  (femenina) o ``es-MX-JorgeNeural`` (masculina). Funciona en cualquier
  computadora con internet; no necesita clave de API.
- ``comando``: un comando externo de TTS (por ejemplo el binario local
  ``tts``) con la plantilla ``{texto}`` / ``{salida}``.
- ``ninguno``: sin voz; el video sale con música o en silencio y el guion
  se guarda para grabarlo en TikTok/CapCut.
"""
import asyncio
import json
import os
import subprocess
import wave

import numpy as np

SR = 44100
VOCES_EDGE = {
    "dalia": "es-MX-DaliaNeural",
    "jorge": "es-MX-JorgeNeural",
}
# Progresión de pads suaves C – Am – F – G (como en la mente extendida).
ACORDES = [
    ("C", [130.81, 261.63, 329.63, 392.00]),
    ("Am", [110.00, 220.00, 261.63, 329.63]),
    ("F", [87.31, 174.61, 220.00, 261.63]),
    ("G", [98.00, 196.00, 246.94, 293.66]),
]


def duracion_audio(ruta):
    """Duración en segundos de un mp3/wav con ffprobe."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", ruta],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


class TTS:
    """Narración por texto. backend: edge | comando | ninguno."""

    def __init__(self, backend="edge", voz="dalia", velocidad=1.0,
                 comando=None):
        self.backend = backend
        self.voz = voz
        self.velocidad = velocidad
        self.comando = comando

    def voz_edge(self):
        return VOCES_EDGE.get(self.voz, self.voz)

    def hablar(self, texto, salida):
        """Genera un mp3 con la narración de ``texto`` en ``salida``."""
        if self.backend == "ninguno":
            return None
        if self.backend == "edge":
            return self._edge(texto, salida)
        if self.backend == "comando":
            return self._comando(texto, salida)
        raise ValueError(f"Backend TTS desconocido: {self.backend}")

    def _edge(self, texto, salida):
        try:
            import edge_tts
        except ImportError as e:
            raise RuntimeError(
                "edge-tts no está instalado. Instálalo con:\n"
                "    pip install edge-tts\n"
                "o usa --tts-backend ninguno y graba el guion en TikTok/CapCut."
            ) from e
        # velocidad: edge-tts usa rate como porcentaje ("-10%", "+10%"...)
        pct = int(round((self.velocidad - 1.0) * 100))
        rate = f"{pct:+d}%" if pct else "+0%"

        async def _run():
            # En redes con proxy de salida (como algunas VMs), edge-tts
            # necesita el proxy explícito: aiohttp no lo toma del entorno.
            proxy = (os.environ.get("HTTPS_PROXY")
                     or os.environ.get("https_proxy")
                     or os.environ.get("HTTP_PROXY")
                     or os.environ.get("http_proxy"))
            kwargs = {}
            if proxy:
                kwargs["proxy"] = proxy
            # edge-tts verifica el TLS con el bundle de certifi, que no
            # incluye la CA de un proxy de salida con interceptación TLS.
            # Si el sistema define un bundle propio (SSL_CERT_FILE), se
            # sustituye el contexto SSL de edge-tts por uno que lo use.
            # En una computadora normal (sin esa variable) no cambia nada.
            cafile = (os.environ.get("SSL_CERT_FILE")
                      or os.environ.get("REQUESTS_CA_BUNDLE"))
            if cafile and os.path.exists(cafile):
                import ssl
                import edge_tts.communicate as _ec
                _ec._SSL_CTX = ssl.create_default_context(cafile=cafile)
            com = edge_tts.Communicate(texto, self.voz_edge(), rate=rate,
                                       # Redes lentas o con proxy: dar más
                                       # margen antes de dar por perdida la
                                       # respuesta de voz (por defecto 60 s).
                                       receive_timeout=180, **kwargs)
            await com.save(salida)

        asyncio.run(_run())
        return salida

    def _comando(self, texto, salida):
        if not self.comando:
            raise RuntimeError("Falta --tts-comando para el backend 'comando'.")
        cmd = self.comando.format(texto=texto, salida=salida)
        proc = subprocess.run(cmd, shell=True, input=texto.encode(),
                              capture_output=True)
        if proc.returncode != 0 or not os.path.exists(salida):
            raise RuntimeError(f"El comando TTS falló: {proc.stderr.decode()[:300]}")
        return salida


def generar_musica(duracion, salida):
    """Música de pads suave (C–Am–F–G, 4 s por acorde, crossfade). WAV mono."""
    n = int(SR * duracion)
    t = np.arange(n) / SR
    audio = np.zeros(n)

    def pad(freqs, start, length):
        m = int(SR * length)
        tt = np.arange(m) / SR
        sig = np.zeros(m)
        for f in freqs:
            for det in (-1.5, 0.0, 1.5):
                ff = f * 2 ** (det / 1200.0)
                amp = 0.30 if f < 150 else 0.22
                sig += amp * np.sin(2 * np.pi * ff * tt)
                sig += 0.06 * np.sin(2 * np.pi * (ff * 2) * tt)
        sig *= 1.0 + 0.08 * np.sin(2 * np.pi * 0.25 * tt)
        env = np.ones(m)
        a = int(SR * 0.8)
        r = int(SR * 0.8)
        env[:a] = np.linspace(0, 1, a)
        env[-r:] = np.linspace(1, 0, r)
        sig *= env
        s0 = int(SR * start)
        e0 = min(n, s0 + m)
        audio[s0:e0] += sig[:e0 - s0]

    pos, i = 0.0, 0
    while pos < duracion:
        _, freqs = ACORDES[i % len(ACORDES)]
        pad(freqs, pos, 4.0)
        pos += 4.0 - 0.8
        i += 1
    fade = int(SR * 1.5)
    audio[-fade:] *= np.linspace(1, 0, fade)
    peak = np.max(np.abs(audio)) or 1.0
    audio = audio / peak * 0.5
    pcm = (audio * 32767).astype(np.int16)
    with wave.open(salida, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return salida


def mezclar(segmentos, musica_wav, salida, duracion_total, volumen_musica=0.12):
    """Mezcla narraciones (mp3, con su inicio en ms) + música en un WAV.

    ``segmentos``: lista de (ruta_mp3, inicio_ms). La música suena de fondo
    a ``volumen_musica`` (0.12 ≈ 18 dB por debajo de la voz).
    """
    entradas = []
    filtros = []
    for i, (ruta, inicio) in enumerate(segmentos):
        entradas += ["-i", ruta]
        filtros.append(f"[{i}:a]adelay={inicio}:all=1[n{i}]")
    idx_mus = len(segmentos)
    if musica_wav:
        entradas += ["-i", musica_wav]
        filtros.append(f"[{idx_mus}:a]volume={volumen_musica}[mus]")
        mezcla = "".join(f"[n{i}]" for i in range(len(segmentos))) + "[mus]"
        n_in = len(segmentos) + 1
    else:
        mezcla = "".join(f"[n{i}]" for i in range(len(segmentos)))
        n_in = len(segmentos)
    filtros.append(f"{mezcla}amix=inputs={n_in}:normalize=0:duration=longest[aout]")
    cmd = (["ffmpeg", "-y", "-v", "error"] + entradas +
           ["-filter_complex", ";".join(filtros), "-map", "[aout]",
            "-t", str(duracion_total), "-ac", "2", "-ar", "44100", salida])
    subprocess.run(cmd, check=True)
    return salida


def unir_video_audio(video_sin_audio, audio_wav, salida, duracion_total):
    """Une el mp4 de video con el audio mezclado."""
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", video_sin_audio,
           "-i", audio_wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
           "-t", str(duracion_total), "-movflags", "+faststart", salida]
    subprocess.run(cmd, check=True)
    return salida
