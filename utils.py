import pygame
import math
from config import *

def obtener_y_canal(x):
    """
    Calcula la coordenada Y del canal en posición x.
    Desde CANAL_INICIO_X hasta CANAL_RECTO_HASTA_X: línea recta
    Desde CANAL_RECTO_HASTA_X hasta CANAL_FIN_X: forma serpenteante
    """
    # Antes del inicio del canal
    if x < CANAL_INICIO_X:
        return CANAL_Y_BASE
    
    # Después del final del canal
    if x > CANAL_FIN_X:
        return CANAL_Y_BASE
    
    # Sección recta (desde el inicio hasta CANAL_RECTO_HASTA_X)
    if x <= CANAL_RECTO_HASTA_X:
        return CANAL_Y_BASE
    
    # Sección serpenteante (desde CANAL_RECTO_HASTA_X hasta CANAL_FIN_X)
    # Calcular offset con seno, pero solo en la zona serpenteante
    offset = AMPLITUD_SERPIENTE * math.sin((x - CANAL_RECTO_HASTA_X) * FRECUENCIA_SERPIENTE)
    return CANAL_Y_BASE + offset


def dibujar_canal_serpenteante(pantalla):
    """Dibuja el canal con forma serpenteante"""
    puntos = []
    
    # Borde superior
    for x in range(CANAL_INICIO_X - 20, CANAL_FIN_X + 50, 5):
        y_centro = obtener_y_canal(x)
        puntos.append((x, y_centro - CANAL_ALTO//2))
    
    # Borde inferior (inverso)
    for x in range(CANAL_FIN_X + 50, CANAL_INICIO_X - 20, -5):
        y_centro = obtener_y_canal(x)
        puntos.append((x, y_centro + CANAL_ALTO//2))
    
    if len(puntos) > 2:
        pygame.draw.polygon(pantalla, (35, 35, 45), puntos)
        pygame.draw.polygon(pantalla, (100, 100, 120), puntos, 2)
    
    # Líneas de flujo internas
    for x in range(CANAL_INICIO_X, CANAL_FIN_X, 40):
        y_centro = obtener_y_canal(x)
        pygame.draw.line(pantalla, (60, 60, 75), 
                        (x, y_centro - CANAL_ALTO//2 + 8),
                        (x, y_centro + CANAL_ALTO//2 - 8), 1)


def dibujar_bifurcacion_y(pantalla):
    """Dibuja la bifurcación en Y para separación magnetoforética"""
    x_fin = CANAL_FIN_X
    y_fin = obtener_y_canal(x_fin)
    
    # Canal de producto (superior)
    puntos_producto = [
        (x_fin, y_fin - CANAL_ALTO//2),
        (x_fin + 80, y_fin - CANAL_ALTO//2 - 15),
        (x_fin + 150, y_fin - CANAL_ALTO//2 - 10),
        (x_fin + 200, y_fin - CANAL_ALTO//2),
    ]
    pygame.draw.polygon(pantalla, (40, 50, 35), puntos_producto)
    pygame.draw.polygon(pantalla, VERDE_OSCURO, puntos_producto, 2)
    
    # Canal de recuperación (inferior)
    puntos_recuperacion = [
        (x_fin, y_fin + CANAL_ALTO//2),
        (x_fin + 80, y_fin + CANAL_ALTO//2 + 15),
        (x_fin + 150, y_fin + CANAL_ALTO//2 + 10),
        (x_fin + 200, y_fin + CANAL_ALTO//2),
    ]
    pygame.draw.polygon(pantalla, (40, 40, 50), puntos_recuperacion)
    pygame.draw.polygon(pantalla, GRIS_CLARO, puntos_recuperacion, 2)
    
    # Iman permanente en bifurcación
    pygame.draw.circle(pantalla, MORADO, (x_fin + 60, y_fin + 15), 18)
    pygame.draw.circle(pantalla, (120, 80, 200), (x_fin + 60, y_fin + 15), 18, 2)
    
    # Líneas de campo del imán permanente
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        x2 = x_fin + 60 + 35 * math.cos(rad)
        y2 = y_fin + 15 + 35 * math.sin(rad)
        pygame.draw.line(pantalla, MORADO, (x_fin + 60, y_fin + 15), (x2, y2), 1)
    
    # Etiquetas
    pantalla.blit(FUENTE_PEQUEÑA.render("PRODUCTO", True, VERDE), (x_fin + 100, y_fin - 35))
    pantalla.blit(FUENTE_PEQUEÑA.render("RECIRCULACIÓN", True, GRIS_CLARO), (x_fin + 80, y_fin + 25))


def dibujar_entradas(pantalla):
    """Dibuja las entradas de reactivos y ferrofluido"""
    x_entrada = CANAL_INICIO_X - 80
    y_entrada = obtener_y_canal(CANAL_INICIO_X - 50)
    
    # Entrada de reactivo A
    pygame.draw.rect(pantalla, (40, 40, 55), (x_entrada - 30, y_entrada - 20, 50, 35))
    pygame.draw.rect(pantalla, AZUL, (x_entrada - 30, y_entrada - 20, 50, 35), 2)
    pantalla.blit(FUENTE_PEQUEÑA.render("REACTIVO A", True, AZUL), (x_entrada - 28, y_entrada - 15))
    
    # Entrada de reactivo B
    pygame.draw.rect(pantalla, (40, 40, 55), (x_entrada - 30, y_entrada + 20, 50, 35))
    pygame.draw.rect(pantalla, (0, 200, 150), (x_entrada - 30, y_entrada + 20, 50, 35), 2)
    pantalla.blit(FUENTE_PEQUEÑA.render("REACTIVO B", True, (0, 200, 150)), (x_entrada - 28, y_entrada + 25))
    
    # Entrada de ferrofluido
    pygame.draw.rect(pantalla, (55, 55, 70), (x_entrada + 20, y_entrada - 15, 40, 55))
    pygame.draw.rect(pantalla, GRIS_METALICO, (x_entrada + 20, y_entrada - 15, 40, 55), 2)
    pantalla.blit(FUENTE_PEQUEÑA.render("FERRO", True, GRIS_CLARO), (x_entrada + 25, y_entrada))