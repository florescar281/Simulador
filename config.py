import pygame
import math

# ============================================
# CONFIGURACIÓN DE PANTALLA
# ============================================
ANCHO = 1400
ALTO = 700
FPS = 60

# ============================================
# COLORES
# ============================================
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 100, 255)
AZUL_CLARO = (100, 200, 255)
AZUL_OSCURO = (0, 50, 150)
GRIS = (100, 100, 100)
GRIS_CLARO = (150, 150, 150)
GRIS_OSCURO = (50, 50, 60)
GRIS_METALICO = (80, 80, 100)
GRIS_BRILLANTE = (180, 180, 200)
ROJO = (255, 0, 0)
ROJO_OSCURO = (150, 0, 0)
VERDE = (0, 255, 0)
VERDE_OSCURO = (0, 150, 0)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)
NARANJA_OSCURO = (200, 100, 0)
MORADO = (170, 102, 255)
CIAN = (0, 255, 255)
DORADO = (255, 200, 100)

# ============================================
# GEOMETRÍA DEL CANAL SERRPENTEANTE
# ============================================
CANAL_INICIO_X = 180
CANAL_FIN_X = 1100
CANAL_Y_BASE = 280
CANAL_ALTO = 55
AMPLITUD_SERPIENTE = 30
FRECUENCIA_SERPIENTE = 0.05
CANAL_RECTO_HASTA_X = 600    # Cambia este valor para alargar/acortar la parte recta
CANAL_SERPIENTE_HASTA_X = 850 # Fin de la sección serpenteante (nueva variable)

# ============================================
# POSICIONES DE LOS IMANES
# ============================================
POS_IMANES = [
    {'x': 320, 'y': 240},   # Iman 1 - Captura
    {'x': 380, 'y': 310},   # Iman 2
    {'x': 440, 'y': 240},   # Iman 3 - Mezcla
    {'x': 500, 'y': 310},   # Iman 4
    {'x': 560, 'y': 240},   # Iman 5 - Transporte final
]

# ============================================
# CONFIGURACIÓN DEL IMÁN SENSOR
# ============================================
IMAN_SENSOR_POS = {'x': 1150, 'y': 360}  # Posición del sensor
IMAN_SENSOR_RADIO = 120                   # Radio de detección
IMAN_SENSOR_ACTIVO = True                # Activar/desactivar

# ============================================
# CONFIGURACIÓN DE IMÁGENES DEL SENSOR
# ============================================
RUTA_IMAGEN_SENSOR_NORMAL = "src/images/electroiman-1-removebg-preview.png"
RUTA_IMAGEN_SENSOR_DETECTANDO = "src/images/Electroiman-1-on.png"
ESCALA_IMAN_SENSOR = 0.25  # Tamaño de la imagen

# ============================================
# VELOCIDADES POR FASE
# ============================================
VEL_FLUJO_BASE = 0.9
VEL_FLUJO_CAPTURA = 0.3
VEL_FLUJO_TRANSPORTE = 1.6
VEL_FLUJO_SEPARACION = 1.2

# ============================================
# DURACIÓN DE FASES (en frames)
# ============================================
DURACION_FASE_INYECCION = 180
DURACION_FASE_CAPTURA = 90
DURACION_FASE_TRANSPORTE = 300
DURACION_FASE_SEPARACION = 120

# ============================================
# PROPIEDADES DE FLUIDOS (default)
# ============================================
DENSIDAD_BASE = 1000.0          # kg/m³
VISCOSIDAD_BASE = 0.001         # Pa·s
TENSION_SUPERFICIAL_BASE = 0.072  # N/m
TEMPERATURA_INICIAL = 25.0      # °C

# ============================================
# PARÁMETROS FÍSICOS
# ============================================
UMBRAL_ACTIVACION_IMAN = 55
RADIO_INFLUENCIA_IMAN = 90
MAX_TEMPERATURA = 80.0
MIN_TEMPERATURA = 25.0
COEFICIENTE_VISCOSIDAD_TEMP = 0.6  # Factor de reducción de viscosidad con temperatura

# ============================================
# PARÁMETROS DE GENERACIÓN DE GOTAS
# ============================================
FRAMES_ENTRE_GOTAS = 100        # Aprox 0.66 segundos a 60 FPS
MAX_GOTAS_SIMULTANEAS = 15

# ============================================
# INICIALIZACIÓN DE FUENTES
# ============================================
pygame.init()
FUENTE = pygame.font.Font(None, 20)
FUENTE_GRANDE = pygame.font.Font(None, 28)
FUENTE_PEQUEÑA = pygame.font.Font(None, 16)
FUENTE_TITULO = pygame.font.Font(None, 36)

# ============================================
# FUNCIÓN PARA OBTENER Y DEL CANAL
# ============================================
def obtener_y_canal(x):
    """Calcula la coordenada Y del canal en posición x (forma serpenteante)"""
    if x < CANAL_INICIO_X:
        return CANAL_Y_BASE
    if x > CANAL_FIN_X:
        return CANAL_Y_BASE
    offset = AMPLITUD_SERPIENTE * math.sin((x - CANAL_INICIO_X) * FRECUENCIA_SERPIENTE)
    return CANAL_Y_BASE + offset

# ============================================
# RUTA DE IMÁGENES
# ============================================
RUTA_FONDO = "SRC/images/fondo.png"  # Asegúrate de tener esta imagen en la carpeta assets

# ============================================
# CONFIGURACIÓN DE IMAGEN DEL REACTOR
# ============================================
RUTA_IMAGEN_REACTOR = "src/images/Base_reactor.png"  # Ruta de tu imagen
POS_X_IMAGEN_REACTOR = 150  # Posición X donde empieza la imagen
POS_Y_IMAGEN_REACTOR = 180  # Posición Y donde empieza la imagen

# ============================================

# CONFIGURACIÓN DE IMÁGENES DE ELECTROIMANES
# ============================================
RUTA_IMAGEN_ELECTROIMAN_INACTIVO = "src/images/electroiman-2.png"
RUTA_IMAGEN_ELECTROIMAN_ACTIVO = "src/images/electroiman-on.png"
ESCALA_IMAN = 0.2  # Ajusta el tamaño

# Posición del LED
LED_OFFSET_X = 35
LED_OFFSET_Y = -25
LED_RADIO = 8

# ============================================
# GEOMETRÍA DEL CANAL DE RECIRCULACIÓN
# ============================================
CIRCULACION_ACTIVA = True  # Activar/desactivar recirculación
CIRCULACION_INICIO_X = CANAL_INICIO_X - 50
CIRCULACION_FIN_X = CANAL_FIN_X + 50
CIRCULACION_Y_OFFSET = 80   # Distancia vertical desde el canal principal
VELOCIDAD_RECIRCULACION = 0.8  # Factor de velocidad en recirculación
UMBRAL_ENTRADA_RECIRCULACION = 40   # Distancia desde el final para entrar
UMBRAL_SALIDA_RECIRCULACION = 30    # Distancia desde el inicio para salir

# ============================================
# CONFIGURACIÓN DE IMAGEN DEL CANAL
# ============================================
RUTA_IMAGEN_CANAL = "src/images/Canal-simulación.png"  # Ruta de tu imagen del canal
AJUSTE_Y_IMAGEN_CANAL = 0  # Ajuste vertical de la imagen (positivo = abajo, negativo = arriba)