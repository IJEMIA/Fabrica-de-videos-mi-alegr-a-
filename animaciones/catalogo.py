# -*- coding: utf-8 -*-
"""Catálogo de recursos disponibles para los videos.

Lo usa la app (el prompt de sistema de Groq) para que el spec que genera
solo pida recursos que existen, y el README para documentarlos.
Nombres exactos: en el spec se escriben tal cual aparecen aquí.
"""
from .personajes import TIPOS_PERSONAJE
from .iconos import OBJETOS
from .escenarios import ESCENARIOS

# --- Personajes (estilos: aprendiz, alebrigma, snes, nes) -------------------
# En el spec (aprendiz): {"tipo": "personaje", "personaje": "doctora",
#                         "x": 360, "y": 1080, "expresion": "contento",
#                         "pose": "pie"}  (pose: pie, caminando, senalando,
#                         sentado, saludando). Expresiones: contento,
#                         preocupado, pensando, sorprendido.
# En el spec (retro): "sprite": "persona:doctora".
PERSONAJES = {
    "hombre": "Hombre adulto, camisa morada.",
    "mujer": "Mujer adulta, pelo largo y falda.",
    "nino": "Niño, más bajito, camisa verde.",
    "nina": "Niña, coletas y falda.",
    "anciano": "Anciano de pelo blanco, barba y bastón.",
    "anciana": "Anciana de pelo blanco recogido, falda y bastón.",
    "maestro": "Maestro con corbata y libro en la mano.",
    "estudiante": "Estudiante con mochila.",
    "cientifico": "Científico con bata blanca y gafas.",
    "doctora": "Doctora con bata blanca y estetoscopio.",
    "trabajador": "Trabajador con casco amarillo y chaleco.",
    "campesino": "Campesino con sombrero de paja.",
    "deportista": "Deportista con camiseta roja número 10.",
    "policia": "Policía con gorra y uniforme azul.",
    "bombero": "Bombero con casco rojo.",
    "vendedor": "Vendedor con delantal.",
}

# --- Objetos (estilos: aprendiz, alebrigma; y en snes/nes pixelizados) -----
# En el spec (aprendiz): {"tipo": "objeto", "nombre": "arbol", "x": 200,
#                         "y": 800, "escala": 1.0, "color": [60, 160, 80]}.
# En el spec (retro): "sprite": "arbol" o "icono": "arbol".
OBJETOS_DESC = {
    "libro": "Libro abierto con líneas de texto.",
    "monedas": "Tres monedas de oro con el signo $.",
    "billetes": "Tres billetes verdes apilados.",
    "alcancia": "Alcancía en forma de cerdito rosa.",
    "grafico": "Gráfico de barras en un cuadro.",
    "puerta": "Puerta de madera con manija dorada.",
    "arbol": "Árbol con tronco y copa con manzanas.",
    "planta": "Planta en maceta con hojas.",
    "casa": "Casa con techo rojo, puerta y ventana.",
    "escuela": "Escuela con techo, ventanas y bandera.",
    "carro": "Carro rojo de cuatro ruedas.",
    "autobus": "Autobús amarillo escolar.",
    "trofeo": "Trofeo dorado de copa.",
    "sol": "Sol sonriente con rayos.",
    "nube": "Nube blanca esponjosa.",
    "lluvia": "Nube con gotas de lluvia cayendo.",
    "cohete": "Cohete con llama encendida.",
    "planeta": "Planeta con anillos y mancha.",
    "microscopio": "Microscopio de laboratorio.",
    "adn": "Doble hélice de ADN azul y roja.",
    "foco": "Foco encendido (idea).",
    "reloj": "Reloj de pared con manecillas.",
    "calendario": "Calendario con un día marcado en rojo.",
    "martillo": "Martillo de carpintero.",
    "estetoscopio": "Estetoscopio médico.",
    "manzana": "Manzana roja con hoja.",
    "comida": "Plato con comida y verduras.",
    "regalo": "Caja de regalo con moño.",
    "bandera": "Bandera ondeando en un mástil.",
    "lapiz": "Lápiz amarillo con punta.",
    "mochila": "Mochila escolar con asa.",
    "flor": "Flor de pétalos rosas y centro amarillo.",
    "computadora": "Computadora portátil encendida.",
    "gota": "Gota de agua azul.",
    # Objetos que ya existían en el framework (elementos con nombre propio):
    "lampara_calle": "Farola de calle que se puede encender.",
    "lampara_mano": "Lámpara ahorradora de mano.",
    "camara": "Cámara de vigilancia.",
    "telefono": "Teléfono celular con aplicaciones.",
    "calculadora": "Calculadora con pantalla y teclas.",
    "cuaderno": "Cuaderno espiral con notas.",
    "mapa": "Mapa con calles, parque y pin.",
    "balon_futbol": "Balón de fútbol blanco y negro.",
    "balon_basquet": "Balón de básquet naranja.",
    "silbato": "Silbato de entrenador.",
    "corazon": "Corazón rojo de salud/amor.",
    "estrella": "Estrella amarilla de cinco puntas.",
    "luna": "Luna llena con cráteres.",
    "telescopio": "Telescopio para mirar las estrellas.",
    "cerebro": "Cerebro rosa (sprite pixel art y suave).",
    "llave": "Llave inglesa de herramienta.",
    "jupiter": "Planeta Júpiter con bandas y la Gran Mancha Roja.",
}

# --- Escenarios (estilos: aprendiz, alebrigma, snes, nes) -------------------
# En el spec: "escenario": "parque" (en la escena, junto a rotulo).
ESCENARIOS_DESC = {
    nombre: desc for nombre, (_, desc, _) in ESCENARIOS.items()
}


def catalogo_para_groq():
    """El catálogo en texto, para el prompt de sistema de Groq."""
    lineas = ["CATÁLOGO DE RECURSOS DISPONIBLES (usa SOLO estos nombres exactos):",
              "",
              "PERSONAJES (campo \"personaje\" en aprendiz, \"persona:<nombre>\" en retro):"]
    for nombre, desc in PERSONAJES.items():
        lineas.append(f"- {nombre}: {desc}")
    lineas += ["",
               "EXPRESIONES: contento, preocupado, pensando, sorprendido.",
               "POSES (aprendiz): pie, caminando, senalando, sentado, saludando.",
               "",
               "OBJETOS (campo \"objeto\" + \"nombre\" en aprendiz; \"sprite\"/\"icono\" en retro):"]
    for nombre, desc in OBJETOS_DESC.items():
        lineas.append(f"- {nombre}: {desc}")
    lineas += ["",
               "ESCENARIOS (campo \"escenario\" en la escena):"]
    for nombre, desc in ESCENARIOS_DESC.items():
        lineas.append(f"- {nombre}: {desc}")
    lineas += ["",
               "REGLAS: si un objeto o personaje no está en este catálogo, NO lo uses;",
               "elige el más parecido de la lista. Los escenarios van en el campo",
               "\"escenario\" de la escena; si no pones escenario, el fondo es el",
               "estándar del estilo (blanco con mancha menta en aprendiz, estrellado",
               "en retro)."]
    return "\n".join(lineas)
