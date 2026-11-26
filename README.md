# 🎬 Fábrica de videos Mi Alegría

Framework reutilizable en Python para programar **videos educativos
verticales (9:16, estilo TikTok)** dibujados por código (PIL + ffmpeg),
con narración. Un solo renderizador lee un archivo `spec.json` por video
y produce el mp4: cada video nuevo es escribir un spec pequeño, no
reescribir el código de dibujo.

El producto principal es la **app web estática en `docs/`**, publicada
con GitHub Pages: escribes el tema y el contenido, la IA (Groq o Gemini,
con TU propia clave) escribe el guion, y el video se dibuja y se descarga
**en el navegador**, sin servidores, sin instalar nada.

## Entrar a la app (producto principal)

**https://ijemia.github.io/Fabrica-de-videos-mi-alegr-a-/**

El flujo es como el de PsicologIA:

1. **Conecta tu clave** — la primera pantalla pide tu propia clave de
   Groq o de Gemini. La clave se guarda **solo en tu dispositivo**
   (localStorage del navegador) y nunca se envía a ningún servidor del
   sitio: solo a la API del proveedor que elijas. También puedes entrar
   sin clave y escribir el guion a mano.
2. **Escribe el tema y el contenido** (misión, visión, datos o hechos),
   elige **estilo** y **duración**.
3. **Genera el guion con IA** — Groq o Gemini escribe el spec con el
   catálogo de abajo.
4. **Revisa y edita las escenas** en el editor (rótulo, narración,
   escenario, sprite; y el JSON completo si quieres afinar).
5. **Vista previa** con la voz de tu dispositivo y música generada.
6. **Descarga el video** (WebM/MP4), la portada PNG o copia el guion.

Para activar la página: en el repo, **Settings → Pages → Deploy from a
branch → main → /docs** (solo se hace una vez).

### Tu clave de Groq o Gemini

La clave es gratis y **nunca se sube al repositorio** (el repo es público
y una clave ahí la robaría cualquiera). Va solo en el campo de la primera
pantalla de la app (tipo contraseña), que la guarda en el localStorage de
tu navegador. Hay un botón **«Probar clave y continuar»** que la valida
con una llamada pequeña a la API.

- **Groq** (rápido y gratuito, modelos Llama): consíguela en
  https://console.groq.com/keys — crea una cuenta, entra a **API Keys**
  y copia la clave (empieza por `gsk_`).
- **Gemini** (Google, modelos Gemini Flash): consíguela en
  https://aistudio.google.com/apikey.

### Limitación honesta de la app web

**El video exportado NO incluye la voz:** el navegador no puede capturar
la voz del dispositivo (speechSynthesis) dentro de la grabación. El video
sí lleva la música generada, y la vista previa sí suena con la voz de tu
dispositivo. Copia el guion con el botón **«Copiar guion»** y graba la
narración en TikTok o CapCut. (Es la misma limitación de las herramientas
«Generador de videos educativos» y «Generador de videos estilo Aprendiz
Financiero».)

Detalle técnico: en la app web los estilos SNES/NES usan los mismos
sprites pixel art del framework, escalados con vecino más cercano; no hay
lienzo interno de 180×320 como en el render Python, así que el aspecto es
pixel art pero la resolución interna es 720×1280.

## La app local (Gradio) y el render por línea de comandos

El framework Python sigue en el repo como referencia y utilidad local.
La app Gradio corre en tu computadora:

- Después de `python app.py`, abre **http://localhost:7860**.
- En la app pones tu clave de Groq (campo "Tu clave de Groq" tipo
  contraseña + botón "Guardar clave en .env", solo en tu computadora),
  o en un archivo `.env` (copia `.env.example` a `.env` y pega tu clave
  en `GROQ_API_KEY=...`; `.env` está en `.gitignore`).

## ¿Por qué cuesta menos tokens?

Antes, cada video era un script de render escrito desde cero (cientos de
líneas). Ahora el código de dibujo vive una sola vez en `animaciones/` y
cada video nuevo es solo:

1. leer el framework (o el catálogo de abajo),
2. escribir un `spec.json` pequeño (guion + escenas),
3. renderizar: `python3 render.py videos/<slug>/spec.json`.

El ahorro está en no reescribir personajes, ilustraciones, escenas,
mezcla de audio ni codificación de video en cada video. La app web de
`docs/` lleva ese mismo catálogo en JavaScript, así que el guion que
genera la IA usa los mismos recursos.

## Instalación

```bash
pip install -r requirements.txt
# además ffmpeg en el sistema:
sudo apt install ffmpeg        # Linux
brew install ffmpeg            # macOS
```

## Uso por línea de comandos

```bash
# Renderizar un video de ejemplo (usa los audios ya grabados si existen):
python3 render.py videos/jugando-por-la-salud/spec.json

# Con narración nueva (edge-tts, gratis, español de México):
python3 render.py videos/iluminando-tu-futuro/spec.json --tts-backend edge --voz dalia

# Sin voz (guion para grabar en TikTok/CapCut):
python3 render.py videos/evolucion-en-jupiter/spec.json --tts-backend ninguno

# Reutilizar audios ya grabados de otro render:
python3 render.py videos/jugando-por-la-salud/spec.json --audio-dir ~/workspace/your_files/jugando-por-la-salud/audio
```

Opciones: `--voz dalia|jorge`, `--velocidad 0.95`, `--sin-musica`,
`--solo-fotogramas`, `--fps 15`.

## Uso con la app

```bash
python app.py
# abre http://localhost:7860
```

1. Pega tu clave de Groq (o guárdala en `.env`).
2. Escribe el **tema** y el **contenido** (misión, visión, datos o hechos).
3. Elige **estilo** y **duración** (ver abajo).
4. Pulsa **Generar video**: Groq escribe el spec, la app lo muestra para
   que lo revises o edites, lo renderiza con narración y te deja
   descargarlo.
5. Si editas el spec, pulsa **Renderizar con este spec**.

## Duración

Desplegable en la app: **30 segundos, 1 minuto, 1 minuto y medio,
2 minutos y 3 minutos** (por defecto **1 minuto**, el formato de los
videos de hoy: 57–72 s). La duración controla el número de escenas y la
longitud de la narración que genera Groq (unas 4 escenas para 30 s, 7–8
para 1 min, 11 para 1:30, 15 para 2 min, 22 para 3 min).

**A más duración, más tarda el renderizado.** Referencia: un video de
60 s tarda unos 65 s en renderizarse (15 fps, 720×1280); uno de 3 minutos
tarda unos 3–4 minutos.

## Estilos

### `aprendiz` — cartoon 2D estilo Aprendiz Financiero
Fondo blanco con mancha verde menta, rótulos grandes en letra manuscrita
(Patrick Hand), personaje de camisa morada dibujado por código, escenas
con listas de elementos. Voz pausada, sin música por defecto.

### `alebrigma` — formas suaves estilo Alebrigma
Fondo morado oscuro estrellado, tarjetas burbuja bicolores, subtítulos
blancos, ilustraciones suaves. Con música de pads suaves.

### `snes` — pixel art 16 bits estilo Super Nintendo
- Resolución interna **180×320** (vertical), escalada a 720×1280 con
  vecino más cercano (sin suavizado).
- Paleta limitada por sprite: **máximo 16 colores**, colores saturados
  de la era 16 bits, contornos negros.
- Sombreado con **dithering** (punteado Bayer 4×4) en los fondos.
- Fondos con **parallax de 2–3 capas** (estrellas, montañas, suelo).
- Personajes como sprites de 16 bits con 2–4 fotogramas de animación:
  parpadeo, caminata en 2 pasos, flotación.

### `nes` — pixel art 8 bits estilo Nintendo
Igual sistema que `snes`, aún más limitado: resolución interna
**144×256**, píxeles más grandes, paleta de **4 colores por sprite**.

Ejemplo de spec `snes`:

```json
{
  "titulo": "La mente extendida",
  "estilo": "snes",
  "musica": true,
  "voz": "dalia",
  "velocidad": 1.0,
  "escenas": [
    {"tipo": "portada", "titulo": ["¿SABÍAS QUE", "TU MENTE NO", "TERMINA EN", "TU CABEZA?"], "gancho": "¿Sabías que tu mente no termina en tu cabeza?", "narracion": "¿Sabías que tu mente no termina en tu cabeza?"},
    {"tipo": "definicion", "subtitulo": "Otto apunta todo en su cuaderno.", "sprite": "persona:otto", "etiqueta": "MEMORIA EXTERNA", "narracion": "Otto apunta todo en su cuaderno, y su cuaderno es parte de su memoria."}
  ]
}
```

Ejemplo de spec `nes` (misma estructura, cambia solo `"estilo": "nes"`):

```json
{
  "titulo": "El cerebro",
  "estilo": "nes",
  "musica": true,
  "voz": "jorge",
  "velocidad": 1.0,
  "escenas": [
    {"tipo": "portada", "titulo": ["EL", "CEREBRO"], "gancho": "¿Qué hace tu cerebro?", "narracion": "¿Qué hace tu cerebro?"},
    {"tipo": "intro", "subtitulo": "Tu cerebro piensa con ayuda de las herramientas.", "sprite": "cerebro", "narracion": "Tu cerebro piensa con ayuda de las herramientas."}
  ]
}
```

## Catálogo de recursos

Groq solo puede usar estos nombres exactos (el prompt de la app incluye
este catálogo). En `aprendiz`, el personaje va en
`{"tipo": "personaje", "personaje": "doctora", "x": 360, "y": 1080,
"pose": "pie", "expresion": "contento"}` (poses: pie, caminando,
senalando, sentado, saludando; expresiones: contento, preocupado,
pensando, sorprendido) y el objeto en
`{"tipo": "objeto", "nombre": "arbol", "x": 200, "y": 800}`.
En retro, el personaje va en `"sprite": "persona:doctora"` y el objeto en
`"sprite": "arbol"`. El escenario va en `"escenario": "parque"` en la escena.

### Personajes

- **hombre**: Hombre adulto, camisa morada.
- **mujer**: Mujer adulta, pelo largo y falda.
- **nino**: Niño, más bajito, camisa verde.
- **nina**: Niña, coletas y falda.
- **anciano**: Anciano de pelo blanco, barba y bastón.
- **anciana**: Anciana de pelo blanco recogido, falda y bastón.
- **maestro**: Maestro con corbata y libro en la mano.
- **estudiante**: Estudiante con mochila.
- **cientifico**: Científico con bata blanca y gafas.
- **doctora**: Doctora con bata blanca y estetoscopio.
- **trabajador**: Trabajador con casco amarillo y chaleco.
- **campesino**: Campesino con sombrero de paja.
- **deportista**: Deportista con camiseta roja número 10.
- **policia**: Policía con gorra y uniforme azul.
- **bombero**: Bombero con casco rojo.
- **vendedor**: Vendedor con delantal.

### Objetos

- **libro**: Libro abierto con líneas de texto.
- **monedas**: Tres monedas de oro con el signo $.
- **billetes**: Tres billetes verdes apilados.
- **alcancia**: Alcancía en forma de cerdito rosa.
- **grafico**: Gráfico de barras en un cuadro.
- **puerta**: Puerta de madera con manija dorada.
- **arbol**: Árbol con tronco y copa con manzanas.
- **planta**: Planta en maceta con hojas.
- **casa**: Casa con techo rojo, puerta y ventana.
- **escuela**: Escuela con techo, ventanas y bandera.
- **carro**: Carro rojo de cuatro ruedas.
- **autobus**: Autobús amarillo escolar.
- **trofeo**: Trofeo dorado de copa.
- **sol**: Sol sonriente con rayos.
- **nube**: Nube blanca esponjosa.
- **lluvia**: Nube con gotas de lluvia cayendo.
- **cohete**: Cohete con llama encendida.
- **planeta**: Planeta con anillos y mancha.
- **microscopio**: Microscopio de laboratorio.
- **adn**: Doble hélice de ADN azul y roja.
- **foco**: Foco encendido (idea).
- **reloj**: Reloj de pared con manecillas.
- **calendario**: Calendario con un día marcado en rojo.
- **martillo**: Martillo de carpintero.
- **estetoscopio**: Estetoscopio médico.
- **manzana**: Manzana roja con hoja.
- **comida**: Plato con comida y verduras.
- **regalo**: Caja de regalo con moño.
- **bandera**: Bandera ondeando en un mástil.
- **lapiz**: Lápiz amarillo con punta.
- **mochila**: Mochila escolar con asa.
- **flor**: Flor de pétalos rosas y centro amarillo.
- **computadora**: Computadora portátil encendida.
- **gota**: Gota de agua azul.
- **lampara_calle**: Farola de calle que se puede encender.
- **lampara_mano**: Lámpara ahorradora de mano.
- **camara**: Cámara de vigilancia.
- **telefono**: Teléfono celular con aplicaciones.
- **calculadora**: Calculadora con pantalla y teclas.
- **cuaderno**: Cuaderno espiral con notas.
- **mapa**: Mapa con calles, parque y pin.
- **balon_futbol**: Balón de fútbol blanco y negro.
- **balon_basquet**: Balón de básquet naranja.
- **silbato**: Silbato de entrenador.
- **corazon**: Corazón rojo de salud/amor.
- **estrella**: Estrella amarilla de cinco puntas.
- **luna**: Luna llena con cráteres.
- **telescopio**: Telescopio para mirar las estrellas.
- **cerebro**: Cerebro rosa (sprite pixel art y suave).
- **llave**: Llave inglesa de herramienta.
- **jupiter**: Planeta Júpiter con bandas y la Gran Mancha Roja.

### Escenarios

- **salon**: Salón de clases: pizarrón, ventanas y pupitres.
- **oficina**: Oficina: ventana, escritorio y computadora.
- **parque**: Parque: árboles, camino, banca y flores.
- **calle**: Calle de día: edificios, banqueta y farola.
- **playa**: Playa: mar con olas, arena, palmera y sombrilla.
- **espacio**: Espacio: estrellas, planeta, luna y nebulosa. Fondo oscuro.
- **ciudad**: Ciudad: rascacielos, calle y líneas viales.
- **campo**: Campo: montañas, surcos, granero y molino.
- **hospital**: Hospital: cruz, ventana y camilla.
- **mercado**: Mercado: puestos de colores con frutas.
- **biblioteca**: Biblioteca: estanterías de libros y mesa de lectura.
- **casa**: Casa/sala: ventana, cuadro, sofá y mesa.
- **estadio**: Estadio: gradas con público y cancha.
- **jardin**: Jardín: seto, flores y camino.
- **mar**: Mar: barco, olas animadas y cielo abierto.
- **desierto**: Desierto: dunas, sol fuerte y cactus.
- **bosque**: Bosque: pinos en varias capas y flores.
- **montana**: Montaña: cordillera con nieve y ladera con pinos.

## Videos de ejemplo

| Video | Estilo | Escenas | Duración original |
|---|---|---|---|
| `videos/mente-extendida/` | snes | 18 | 57.0 s |
| `videos/iluminando-tu-futuro/` | aprendiz | 8 | 71.8 s |
| `videos/jugando-por-la-salud/` | aprendiz | 8 | 60.2 s |
| `videos/evolucion-en-jupiter/` | aprendiz | 6 | 69.9 s |

Cada carpeta trae su `spec.json` y su `guion.txt` (los guiones originales,
sin reescribir). Validación: al re-renderizar «Jugando por la salud»
desde su spec reutilizando sus audios, el mp4 salió de **60.27 s frente a
60.20 s del original (diferencia 0.07 s)**.

## Limitaciones honestas

- **La app web exporta el video sin voz** (ver arriba): el navegador no
  puede capturar la voz del dispositivo; la vista previa sí suena, el
  video lleva música, y el guion se copia para grabarlo en TikTok o
  CapCut.
- La narración de la app local usa **edge-tts** (gratuito, sin clave). Si
  en tu red no llega a Microsoft, la app puede renderizar sin voz
  (`FABRICA_TTS_BACKEND=ninguno`) y el guion se graba en TikTok o CapCut.
- La narración se verifica por duraciones y energía de voz, no escuchando
  palabra por palabra.
- Groq genera el guion a partir de tus datos: **revisa el spec antes de
  renderizar**; la app lo muestra para editarlo.
- El render en el navegador es en tiempo real: un video de 3 minutos
  tarda 3 minutos en exportarse.

## Publicar la app local en Hugging Face Spaces (opcional)

Sin desplegar nada desde aquí; dos pasos cuando lo decidas (solo para la
app Gradio; la app principal ya es la página de GitHub Pages de arriba):

1. Crea un Space en https://huggingface.co/new-space (SDK: Gradio) y
   sube el contenido del repo (el `app.py` de la raíz es el punto de
   entrada; `requirements.txt` ya está; la carpeta `huggingface-space/`
   trae el README del Space).
2. En el Space, ve a **Settings → Repository secrets** y pega tu clave
   como Secret con el nombre `GROQ_API_KEY`.

El enlace del Space es entonces la dirección pública de la app Gradio.

## Estructura

```
docs/index.html           App web estática (producto principal, GitHub Pages)
render.py                 Renderizador por línea de comandos
app.py                    Lanzador de la app Gradio (http://localhost:7860)
app/app.py                Interfaz Gradio + llamada a Groq + descarga
scripts/generar_spec.py   Genera un spec con Groq desde la terminal
animaciones/
  core.py                 Lienzo, fuentes, texto, mezcla
  estilos.py              Estilos aprendiz / alebrigma / snes / nes
  personajes.py           16 personajes (suave + pixel SNES/NES)
  iconos.py               34 objetos nuevos + objetos de los videos
  objetos.py              Objetos de los videos originales (lámpara, etc.)
  escenarios.py           18 escenarios con parallax
  catalogo.py             Catálogo para Groq y para este README
  prompts.py              Prompt y esquema del spec (compartido con la app web)
  spec.py                 Esquema y validación del spec.json
  audio.py                TTS (edge-tts / comando / ninguno) + música
videos/<slug>/            4 videos de ejemplo (spec.json + guion.txt)
INSTRUCCIONES.md          Flujo de trabajo para el agente (editable)
```

## Licencia

MIT — código original. Ver `LICENSE`.
