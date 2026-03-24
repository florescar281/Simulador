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
AMPLITUD_SERPIENTE = 45
FRECUENCIA_SERPIENTE = 0.012
CANAL_RECTO_HASTA_X = 650    # Cambia este valor para alargar/acortar la parte recta
AMPLITUD_SERPIENTE = 28      # Aumenta para más amplitud, disminuye para menos
FRECUENCIA_SERPIENTE = 0.018 # Aumenta para más oscilaciones, disminuye para menos
# ============================================
# POSICIONES DE LOS IMANES
# ============================================
POS_IMANES = [
    {'x': 320, 'y': 295},   # Iman 1 - Captura
    {'x': 480, 'y': 270},   # Iman 2
    {'x': 640, 'y': 310},   # Iman 3 - Mezcla
    {'x': 800, 'y': 285},   # Iman 4
    {'x': 960, 'y': 315},   # Iman 5 - Transporte final
]

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
FRAMES_ENTRE_GOTAS = 40        # Aprox 0.66 segundos a 60 FPS
MAX_GOTAS_SIMULTANEAS = 6

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
POS_Y_IMAGEN_REACTOR = 220  # Posición Y donde empieza la imagen