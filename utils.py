import pygame
import math
from config import *

def obtener_y_canal(x):
        """
        Calcula la coordenada Y del canal en posición x.
        - Recto desde inicio hasta CANAL_RECTO_HASTA_X
        - Serpenteante desde CANAL_RECTO_HASTA_X hasta 1000
        - Recto desde 1000 hasta el final
        """
        if x < CANAL_INICIO_X:
            return CANAL_Y_BASE
        if x > CANAL_FIN_X:
            return CANAL_Y_BASE
        
        # Sección recta inicial
        if x <= CANAL_RECTO_HASTA_X:
            return CANAL_Y_BASE
        
        # Sección serpenteante (hasta x=1000)
        if x <= CANAL_SERPIENTE_HASTA_X:
            offset = AMPLITUD_SERPIENTE * math.sin((x - CANAL_RECTO_HASTA_X) * FRECUENCIA_SERPIENTE)
            return CANAL_Y_BASE + offset
        
        # Sección recta final (después de 1000)
        return CANAL_Y_BASE


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

def dibujar_canal_recirculacion(pantalla):
    """Dibuja el canal de recirculación que conecta el final con el inicio"""
    if not CIRCULACION_ACTIVA:
        return
    
    # Puntos del canal de recirculación
    puntos = []
    
    # Desde el final del canal principal (x=CANAL_FIN_X)
    x_fin = CANAL_FIN_X
    y_fin = obtener_y_canal(x_fin)
    
    # Bajar hasta el nivel del canal de recirculación
    y_recirc = y_fin + CIRCULACION_Y_OFFSET
    
    # Camino de ida (superior)
    for x in range(x_fin, CANAL_INICIO_X - 50, -8):
        # Curva suave hacia abajo
        if x > x_fin - 60:
            factor = (x_fin - x) / 60
            y = y_fin + (y_recirc - y_fin) * factor
        else:
            y = y_recirc
        puntos.append((x, y - CANAL_ALTO//4))
    
    # Borde inferior (retorno)
    for x in range(CANAL_INICIO_X - 50, x_fin, 8):
        if x < CANAL_INICIO_X + 60:
            factor = (x - (CANAL_INICIO_X - 50)) / 110
            y = y_recirc + (y_fin - y_recirc) * factor
        else:
            y = y_recirc
        puntos.append((x, y + CANAL_ALTO//4))
    
    if len(puntos) > 2:
        # Dibujar canal de recirculación
        pygame.draw.polygon(pantalla, (45, 45, 55), puntos)
        pygame.draw.polygon(pantalla, (100, 100, 120), puntos, 2)
    
    # Flechas indicadoras de dirección
    for x in range(CANAL_FIN_X, CANAL_INICIO_X - 50, -100):
        y = y_recirc
        # Dibujar flecha
        pygame.draw.polygon(pantalla, (150, 150, 200), [
            (x, y - 8),
            (x - 15, y),
            (x, y + 8)
        ])
    
    # Texto de recirculación
    pantalla.blit(FUENTE_PEQUEÑA.render("RECIRCULACIÓN", True, (150, 150, 200)), 
                 (CANAL_FIN_X - 150, y_recirc - 25))


def obtener_y_recirculacion(x):
    """Obtiene la Y del canal de recirculación en una posición X"""
    if not CIRCULACION_ACTIVA:
        return None
    
    x_fin = CANAL_FIN_X
    y_fin = obtener_y_canal(x_fin)
    y_recirc = y_fin + CIRCULACION_Y_OFFSET
    
    # Zona de entrada (curva desde el final hacia abajo)
    if x >= x_fin - 60 and x <= x_fin + 60:
        factor = (x - (x_fin - 60)) / 120
        return y_fin + (y_recirc - y_fin) * factor
    
    # Zona de salida (curva desde abajo hacia el inicio)
    elif x >= CANAL_INICIO_X - 60 and x <= CANAL_INICIO_X + 60:
        factor = (x - (CANAL_INICIO_X - 60)) / 120
        return y_recirc + (y_fin - y_recirc) * factor
    
    # Zona recta del canal de recirculación
    elif x >= CANAL_INICIO_X + 60 and x <= x_fin - 60:
        return y_recirc
    
    # Si está más allá del inicio (más a la izquierda)
    elif x < CANAL_INICIO_X - 60:
        return y_fin  # Volver al nivel del canal principal
    
    # Si está más allá del final (más a la derecha)
    elif x > x_fin + 60:
        return y_recirc
    
    return y_recirc