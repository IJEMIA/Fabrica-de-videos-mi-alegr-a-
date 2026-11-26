# INSTRUCCIONES — Flujo de trabajo de la Fábrica de videos Mi Alegría

Este archivo lo puede editar el usuario. Describe cómo trabajamos juntos
para hacer videos con este repositorio.

## El flujo

1. **El usuario da el tema y el contenido.** Por ejemplo, para un proyecto:
   misión, visión, objetivo, resultado, actividades y recursos. Para un
   tema de ciencia: los hechos, con sus fuentes si las hay (nombres, años,
   lugares). Cuanto más completo venga el contenido, menos preguntas hacen
   falta.
2. **Yo escribo el spec** (`videos/<slug>/spec.json`): el guion completo
   (rótulo en pantalla + narración de cada escena) y las escenas con sus
   ilustraciones, usando solo personajes, objetos y escenarios del
   catálogo (`animaciones/catalogo.py` y README). El guion queda también
   en `videos/<slug>/guion.txt`.
3. **Yo renderizo el mp4 con narración** (`python3 render.py
   videos/<slug>/spec.json`) y lo verifico con ffprobe (duración y
   formato) y revisando fotogramas.
4. **Lo entrego** con el enlace o el archivo, diciendo qué se verificó y
   qué no.

Si el usuario usa la app web, los pasos 2 y 3 los hace Groq + la app, y
el usuario solo revisa el spec y descarga el video.

## Reglas

- **Nunca inventar datos.** Solo se usa lo que da el usuario o lo que
  está verificado (nombres, cifras, fechas, lugares). Si falta un dato,
  se pregunta antes de redactar, no se rellena.
- **Lo hipotético, como hipotético.** Si algo es una idea, una hipótesis
  o una posibilidad (por ejemplo, vida en Júpiter), se marca con palabras
  como «imaginaron», «si existiera», «según los científicos», «podría».
  Nunca se afirma como hecho lo que no lo es.
- **Reportar las limitaciones con honestidad.** La narración se verifica
  por duraciones y energía de voz, no escuchando palabra por palabra. Si
  algo no se pudo comprobar en vivo, se dice. Si una herramienta no puede
  hacer algo (por ejemplo, la exportación de un generador web no lleva
  voz), se dice antes de prometerlo.
- **Un video nuevo = un spec nuevo.** No se reescribe el código de
  dibujo: se reutilizan los personajes, objetos, escenarios y estilos del
  framework. Si falta un recurso (un personaje o un objeto nuevo), se
  añade al framework una sola vez y queda para todos los videos.
- **Estilos:** `aprendiz` (cartoon 2D, fondo blanco), `alebrigma`
  (formas suaves, fondo morado), `snes` (pixel art 16 bits, principal) y
  `nes` (pixel art 8 bits, variante). El usuario elige el estilo en la
  app o lo dice al pedir el video.
- **Duración:** 30 segundos, 1 minuto (por defecto), 1 minuto y medio,
  2 minutos o 3 minutos. A más duración, más escenas y más tarda el
  renderizado.
- **La clave de Groq nunca se escribe en el chat ni se commitea.** Vive
  en `.env` o en el campo de la app. El repo es público.

## Antes de pedir un video, conviene tener

- Tema y estilo (si no se dice, se pregunta o se usa `aprendiz`).
- El contenido: misión/visión/datos o hechos, con cifras exactas.
- Duración deseada (si no se dice, 1 minuto).
- Voz: Dalia (femenina) o Jorge (masculina). Si no se dice, Dalia.
- Música: sí o no (en `aprendiz` el original no lleva; en retro sí).
