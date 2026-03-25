import pygame
import math
import random
from config import *
from utils import obtener_y_canal

class ParticulaLiquida:
    """Partícula individual del flujo líquido"""
    
    def __init__(self, x, y, color_base=(80, 150, 255)):
        self.x = x
        self.y = y
        self.x_original = x
        self.vel_x = random.uniform(0.5, 1.2)
        self.vel_y = random.uniform(-0.3, 0.3)
        self.tam = random.uniform(5, 10)
        self.nivel_mezcla = 0.0
        self.angulo = random.uniform(0, math.pi * 2)
        self.color_base = color_base  # Color personalizable
    
    def mover(self, velocidad_base, vibracion, y_canal):
        """Mueve la partícula siguiendo el canal"""
        self.x += velocidad_base + self.vel_x * 0.3
        
        # Seguir la forma del canal
        y_deseada = y_canal
        
        # Movimiento suave hacia la posición deseada
        diferencia = y_deseada - self.y
        self.y += diferencia * 0.1
        
        # Efecto de vibración por mezcla
        if vibracion:
            self.y += random.uniform(-0.8, 0.8)
            self.x += random.uniform(-0.3, 0.3)
        
        # Movimiento ondulatorio propio (efecto de líquido)
        self.angulo += 0.05
        self.y += math.sin(self.angulo + self.x * 0.02) * 0.3
    
    def dibujar(self, pantalla):
        """Dibuja la partícula"""
        # Color según nivel de mezcla
        if self.nivel_mezcla > 0.5:
            r = min(255, self.color_base[0] + 100)
            g = min(255, self.color_base[1] + 100)
            b = min(255, self.color_base[2] + 50)
            color = (r, g, b)
        elif self.nivel_mezcla > 0.2:
            r = min(255, self.color_base[0] + 50)
            g = min(255, self.color_base[1] + 50)
            b = min(255, self.color_base[2] + 25)
            color = (r, g, b)
        else:
            color = self.color_base
        
        # Brillo según mezcla
        brillo = int(80 + 100 * self.nivel_mezcla)
        color_brillo = (min(255, color[0] + brillo), 
                       min(255, color[1] + brillo), 
                       min(255, color[2] + brillo))
        
        # Dibujar partícula
        pygame.draw.circle(pantalla, color_brillo, (int(self.x), int(self.y)), int(self.tam))
        pygame.draw.circle(pantalla, color, (int(self.x), int(self.y)), int(self.tam - 1))


class FlujoContinuo:
    """Flujo continuo como sistema de partículas (Fluido 1 - Reactivo A)"""
    
    def __init__(self, x, y, densidad, viscosidad, color=(80, 150, 255)):
        self.x = x
        self.y = y
        self.densidad = densidad
        self.viscosidad = viscosidad
        self.temperatura = TEMPERATURA_INICIAL
        self.nivel_mezcla = 0.0
        self.color = color  # Azul por defecto
        
        # Crear muchas partículas para el flujo continuo
        self.particulas = []
        self._crear_particulas_iniciales()
        
        # Control de generación continua
        self.tiempo_entre_particulas = 0
    
    def _crear_particulas_iniciales(self):
        """Crea las partículas iniciales del flujo"""
        for i in range(80):
            x_offset = i * 8
            y_canal = obtener_y_canal(self.x + x_offset)
            particula = ParticulaLiquida(self.x + x_offset, y_canal, self.color)
            self.particulas.append(particula)
    
    def actualizar_mezcla(self, vibracion, temperatura):
        """Actualiza nivel de mezcla y temperatura"""
        self.temperatura = temperatura
        
        if vibracion:
            self.nivel_mezcla = min(1.0, self.nivel_mezcla + 0.01)
        else:
            self.nivel_mezcla = max(0.0, self.nivel_mezcla - 0.008)
        
        # Propagar nivel de mezcla a las partículas
        for p in self.particulas:
            p.nivel_mezcla = self.nivel_mezcla
    
    def mover(self, velocidad_actual):
        """Mueve todas las partículas y genera nuevas"""
        # Mover partículas existentes
        particulas_activas = []
        for p in self.particulas:
            y_canal_actual = obtener_y_canal(p.x)
            p.mover(velocidad_actual, self.nivel_mezcla > 0.3, y_canal_actual)
            
            # Mantener partículas dentro del canal
            if p.x < CANAL_FIN_X + 200:
                particulas_activas.append(p)
            else:
                # Reciclar al inicio
                p.x = CANAL_INICIO_X + random.uniform(0, 50)
                p.y = obtener_y_canal(p.x)
                p.vel_x = random.uniform(0.5, 1.2)
                particulas_activas.append(p)
        
        self.particulas = particulas_activas
        
        # Generar nuevas partículas continuamente
        self.tiempo_entre_particulas += 1
        if self.tiempo_entre_particulas > 3:
            y_nueva = obtener_y_canal(CANAL_INICIO_X + 20)
            nueva_particula = ParticulaLiquida(CANAL_INICIO_X + 20, y_nueva, self.color)
            nueva_particula.nivel_mezcla = self.nivel_mezcla
            self.particulas.append(nueva_particula)
            self.tiempo_entre_particulas = 0
        
        # Limitar número de partículas
        if len(self.particulas) > 200:
            self.particulas = self.particulas[-200:]
    
    def dibujar(self, pantalla):
        """Dibuja todas las partículas del flujo"""
        for p in sorted(self.particulas, key=lambda p: p.x):
            p.dibujar(pantalla)
    
    def obtener_eficiencia(self):
        """Devuelve la eficiencia de mezcla actual"""
        return self.nivel_mezcla * 100