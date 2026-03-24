import pygame
import random
from config import *

class FlujoContinuo:
    """Flujo continuo de reactivo (como agua de una pluma)"""
    
    def __init__(self, x, y, densidad, viscosidad):
        self.x = x
        self.y = y
        self.largo = 0  # El largo se va extendiendo
        self.ancho = 70
        self.alto = 45
        self.nivel_mezcla = 0.0
        self.densidad = densidad
        self.viscosidad = viscosidad
        self.temperatura = TEMPERATURA_INICIAL
        self.fluyendo = True
        
        # Trazadores para efecto visual
        self.trazadores = []
        for _ in range(80):
            self.trazadores.append({
                'x': random.uniform(-self.ancho/2 + 10, self.ancho/2 - 10),
                'y': random.uniform(-self.alto/2 + 10, self.alto/2 - 10),
                'vx': random.uniform(-0.2, 0.2),
                'vy': random.uniform(-0.2, 0.2)
            })
    
    def actualizar_mezcla(self, vibracion, temperatura):
        """Actualiza nivel de mezcla"""
        self.temperatura = temperatura
        
        if vibracion:
            self.nivel_mezcla = min(1.0, self.nivel_mezcla + 0.012)
        else:
            self.nivel_mezcla = max(0.0, self.nivel_mezcla - 0.005)
        
        # Mover trazadores
        for t in self.trazadores:
            if vibracion:
                t['x'] += random.uniform(-0.8, 0.8)
                t['y'] += random.uniform(-0.8, 0.8)
            else:
                t['x'] += t['vx']
                t['y'] += t['vy']
            
            # Mantener dentro
            t['x'] = max(-self.ancho/2 + 5, min(self.ancho/2 - 5, t['x']))
            t['y'] = max(-self.alto/2 + 5, min(self.alto/2 - 5, t['y']))
    
    def extender(self, velocidad):
        """Extiende el flujo continuamente"""
        self.largo += velocidad
        # Mantener el flujo dentro del canal
        if self.x + self.largo > CANAL_FIN_X + 200:
            self.largo = 0  # Reiniciar cuando sale (recirculación)
    
    def mover(self, velocidad_actual):
        """Mueve todo el flujo"""
        self.x += velocidad_actual
    
    def dibujar(self, pantalla):
        """Dibuja el flujo continuo"""
        if self.largo <= 0:
            return
        
        # Dibujar como un rectángulo alargado (flujo continuo)
        ancho_visible = min(self.largo, self.ancho * 3)  # Limitar visualmente
        
        # Color según mezcla
        if self.nivel_mezcla > 0.5:
            color_fondo = (120, 80, 40)
        elif self.nivel_mezcla > 0.2:
            color_fondo = (70, 90, 120)
        else:
            color_fondo = (40, 50, 80)
        
        # Dibujar el flujo como un rectángulo continuo
        rect = pygame.Rect(int(self.x - self.ancho/2), 
                          int(self.y - self.alto/2), 
                          int(ancho_visible), 
                          self.alto)
        pygame.draw.rect(pantalla, color_fondo, rect, border_radius=6)
        pygame.draw.rect(pantalla, AZUL, rect, 2, border_radius=6)
        
        # Trazadores (solo en la parte visible)
        for t in self.trazadores:
            px = self.x + t['x']
            py = self.y + t['y']
            # Solo dibujar si está dentro del área visible
            if px > self.x - self.ancho/2 and px < self.x + ancho_visible:
                if self.nivel_mezcla > 0.5:
                    color = (255, 200, 50)
                    tam = 3
                elif self.nivel_mezcla > 0.2:
                    color = (255, 150, 50)
                    tam = 2
                else:
                    color = (100, 150, 255)
                    tam = 2
                pygame.draw.circle(pantalla, color, (int(px), int(py)), tam)
        
        # Barra de mezcla
        if self.nivel_mezcla > 0.05:
            barra_x = self.x + ancho_visible + 5
            barra_y = self.y - self.alto/2
            alto_barra = self.alto * self.nivel_mezcla
            pygame.draw.rect(pantalla, NARANJA,
                           (int(barra_x), int(barra_y + self.alto - alto_barra), 4, int(alto_barra)))