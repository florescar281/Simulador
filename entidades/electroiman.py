import pygame
import math
from config import *

class Electroiman:
    """Electroimán con control de intensidad, oscilación y efecto visual"""
    
    def __init__(self, x, y, indice):
        self.x = x
        self.y = y
        self.indice = indice
        self.activo = False
        self.oscilando = False
        self.intensidad = 0.7
        self.tiempo_oscilacion = 0
    
    def actualizar(self):
        """Actualiza estado del imán (oscilación)"""
        if self.oscilando:
            self.tiempo_oscilacion += 1
            # Oscilación de alta frecuencia (simula 10-100 Hz)
            self.intensidad = 0.5 + 0.4 * math.sin(self.tiempo_oscilacion * 0.25)
        else:
            self.intensidad = 0.7 if self.activo else 0
    
    def activar(self):
        """Activa el imán en modo estático"""
        self.activo = True
        self.oscilando = False
    
    def activar_oscilacion(self):
        """Activa el imán en modo oscilación (mezcla activa)"""
        self.activo = False
        self.oscilando = True
        self.tiempo_oscilacion = 0
    
    def desactivar(self):
        """Desactiva el imán"""
        self.activo = False
        self.oscilando = False
        self.intensidad = 0
    
    def dibujar(self, pantalla):
        """Dibuja el electroimán con aspecto industrial"""
        # Base
        pygame.draw.rect(pantalla, (50, 50, 65), 
                        (self.x - 28, self.y - 18, 56, 36))
        pygame.draw.rect(pantalla, (80, 80, 100), 
                        (self.x - 28, self.y - 18, 56, 36), 2)
        
        # Bobinas
        if self.activo:
            color_bobina = (180, 50, 50)
        elif self.oscilando:
            intensidad_color = int(100 + 100 * self.intensidad)
            color_bobina = (intensidad_color, 80, 0)
        else:
            color_bobina = (60, 60, 75)
        
        for i in range(3):
            x_bobina = self.x - 15 + i * 15
            pygame.draw.circle(pantalla, color_bobina, (x_bobina, self.y - 8), 8)
            pygame.draw.circle(pantalla, (120, 120, 140), (x_bobina, self.y - 8), 8, 1)
        
        # Núcleo central
        pygame.draw.rect(pantalla, (90, 90, 110), (self.x - 8, self.y - 12, 16, 24))
        
        # LED de estado
        if self.activo:
            led_color = ROJO
        elif self.oscilando:
            led_color = NARANJA
        else:
            led_color = (40, 40, 40)
        pygame.draw.circle(pantalla, led_color, (self.x + 32, self.y - 22), 6)
        pygame.draw.circle(pantalla, BLANCO, (self.x + 32, self.y - 22), 6, 1)
        
        # Líneas de campo magnético
        if self.activo or self.oscilando:
            for ang in range(0, 360, 45):
                rad = math.radians(ang)
                longitud = 45 * self.intensidad
                x2 = self.x + longitud * math.cos(rad)
                y2 = self.y + longitud * math.sin(rad)
                color_linea = ROJO if self.activo else NARANJA
                pygame.draw.line(pantalla, color_linea, (self.x, self.y), (int(x2), int(y2)), 2)