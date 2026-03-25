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
    """Flujo continuo como sistema de partículas"""
    
    def __init__(self, x, y, densidad, viscosidad, color=(80, 150, 255), offset_y=0):
        self.x = x
        self.y = y
        self.offset_y = offset_y  # Desplazamiento vertical inicial
        self.densidad = densidad
        self.viscosidad = viscosidad
        self.temperatura = TEMPERATURA_INICIAL
        self.nivel_mezcla = 0.0
        self.color = color
        
        self.particulas = []
        self._crear_particulas_iniciales()
        self.tiempo_entre_particulas = 0
    
    def _crear_particulas_iniciales(self):
        for i in range(80):
            x_offset = i * 8
            y_canal = obtener_y_canal(self.x + x_offset) + self.offset_y
            particula = ParticulaLiquida(self.x + x_offset, y_canal, self.color)
            self.particulas.append(particula)
    
    def actualizar_mezcla(self, vibracion, temperatura):
        self.temperatura = temperatura
        
        if vibracion:
            self.nivel_mezcla = min(1.0, self.nivel_mezcla + 0.01)
        else:
            self.nivel_mezcla = max(0.0, self.nivel_mezcla - 0.008)
        
        for p in self.particulas:
            p.nivel_mezcla = self.nivel_mezcla
    
    def mover(self, velocidad_actual):
        particulas_activas = []
        for p in self.particulas:
            y_canal_actual = obtener_y_canal(p.x)
            
            # Calcular la Y deseada según la posición X
            if p.x < APROXIMACION_INICIO_X:
                # Antes de empezar a acercarse, mantener el offset fijo
                y_deseada = y_canal_actual + self.offset_y
            elif p.x < PUNTO_UNION_X:
                # En la zona de aproximación, ir acercándose gradualmente
                # Calcular progreso (0 en APROXIMACION_INICIO_X, 1 en PUNTO_UNION_X)
                progreso = (p.x - APROXIMACION_INICIO_X) / (PUNTO_UNION_X - APROXIMACION_INICIO_X)
                progreso = max(0, min(1, progreso))  # Limitar entre 0 y 1
                
                # Interpolación lineal: desde offset_y hasta 0
                offset_actual = self.offset_y * (1 - progreso)
                y_deseada = y_canal_actual + offset_actual
            else:
                # Después de la unión, seguir el canal normal
                y_deseada = y_canal_actual
            
            # Movimiento suave hacia la posición deseada
            diferencia = y_deseada - p.y
            p.y += diferencia * 0.1
            
            p.mover(velocidad_actual, self.nivel_mezcla > 0.3, y_deseada)
            
            if p.x < CANAL_FIN_X + 200:
                particulas_activas.append(p)
            else:
                p.x = CANAL_INICIO_X + random.uniform(0, 50)
                p.y = obtener_y_canal(p.x) + self.offset_y
                p.vel_x = random.uniform(0.5, 1.2)
                particulas_activas.append(p)
        
        self.particulas = particulas_activas
        
        # Generar nuevas partículas
        self.tiempo_entre_particulas += 1
        if self.tiempo_entre_particulas > 3:
            y_nueva = obtener_y_canal(CANAL_INICIO_X + 20) + self.offset_y
            nueva_particula = ParticulaLiquida(CANAL_INICIO_X + 20, y_nueva, self.color)
            nueva_particula.nivel_mezcla = self.nivel_mezcla
            self.particulas.append(nueva_particula)
            self.tiempo_entre_particulas = 0
        
        if len(self.particulas) > 200:
            self.particulas = self.particulas[-200:]
    
    def dibujar(self, pantalla):
        for p in sorted(self.particulas, key=lambda p: p.x):
            p.dibujar(pantalla)
    
    def obtener_eficiencia(self):
        return self.nivel_mezcla * 100