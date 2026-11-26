---
title: Fábrica de videos Mi Alegría
emoji: 🎬
colorFrom: purple
colorTo: pink
sdk: gradio
sdk_version: 6.32.0
app_file: app.py
pinned: false
license: mit
---

# Fábrica de videos Mi Alegría

App web que genera videos educativos verticales (9:16) con Groq (guion) y
un framework propio de dibujo por código (PIL + ffmpeg) con narración
gratuita (edge-tts, español de México).

Para usarla en este Space, el dueño debe pegar su clave de Groq como
**Secret** con el nombre `GROQ_API_KEY` (Settings → Repository secrets).
La clave es gratis: https://console.groq.com/keys
