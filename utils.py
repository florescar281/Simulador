import pygame
from config import BLANCO, AZUL, GRIS, ROJO, VERDE, FUENTE, AMARILLO, NARANJA

def dibujar_canales(pantalla):
    """Dibuja los canales del microreactor"""
    # Canal principal
    pygame.draw.rect(pantalla, BLANCO, (200, 250, 800, 100), 2)
    
    # Canales de entrada
    pygame.draw.rect(pantalla, BLANCO, (50, 275, 150, 50), 2)
    pygame.draw.rect(pantalla, BLANCO, (125, 225, 50, 50), 2) 
    
    # Canales de salida
    pygame.draw.rect(pantalla, BLANCO, (1000, 250, 150, 50), 2)
    pygame.draw.rect(pantalla, BLANCO, (1000, 350, 150, 50), 2)
    
    # Etiquetas
    pantalla.blit(FUENTE.render("Reactivo", True, AZUL), (60, 240))
    pantalla.blit(FUENTE.render("Ferrofluido", True, GRIS), (100, 190))
    pantalla.blit(FUENTE.render("Producto", True, VERDE), (1010, 220))
    pantalla.blit(FUENTE.render("Recuperación", True, GRIS), (1010, 320))

def dibujar_iman(pantalla, x, y, activo=False, oscilando=False):
    """Dibuja un electroimán"""
    color = ROJO if activo else NARANJA if oscilando else (50, 50, 50)
    pygame.draw.circle(pantalla, color, (x, y), 30)
    pygame.draw.circle(pantalla, BLANCO, (x, y), 30, 2)
    
    # Líneas de campo
    if activo or oscilando:
        for i in range(0, 360, 45):
            import math
            rad = math.radians(i)
            x2 = x + 40 * math.cos(rad)
            y2 = y + 40 * math.sin(rad)
            pygame.draw.line(pantalla, color, (x, y), (x2, y2), 1)

def dibujar_info(pantalla, fase, vibracion):
    """Muestra información en pantalla"""
    textos = [
        f"FASE: {fase}",
        f"Mezcla activa: {'SI' if vibracion else 'NO'}",
        "ESPACIO: cambiar fase",
        "V: activar/desactivar mezcla"
    ]
    
    y = 20
    for texto in textos:
        color = AMARILLO if "FASE" in texto else BLANCO
        pantalla.blit(FUENTE.render(texto, True, color), (20, y))
        y += 25