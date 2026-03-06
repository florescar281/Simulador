import pygame

# Configuración de pantalla
ANCHO = 1400
ALTO = 700
FPS = 60

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 100, 255)
GRIS = (100, 100, 100)
GRIS_CLARO = (150, 150, 150)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)

# Posiciones de los imanes
POS_IMANES = [400, 550, 700, 850]
Y_IMAN = 280

# Velocidades
VEL_FLUJO = 1.8
TIEMPO_ENTRE_GOTAS = 2

# Fuentes
pygame.init()
FUENTE = pygame.font.Font(None, 20)
FUENTE_GRANDE = pygame.font.Font(None, 24)
FUENTE_PEQUEÑA = pygame.font.Font(None, 16)