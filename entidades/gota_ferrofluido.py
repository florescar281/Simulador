import pygame
import math
import random
from config import *

class GotaFerrofluido:
    """Gota de ferrofluido con deformación por campo magnético y efecto metálico"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radio_base = 22
        self.radio_x = 28
        self.radio_y = 18
        self.vel_x = VEL_FLUJO_BASE
        self.vel_y = 0
        self.picos = []
        self.intensidad_campo = 0
        self.recirculando = False
        self.tiempo_vida = 0
        
        # Partículas internas para efecto metálico
        self.particulas = []
        for _ in range(25):
            self.particulas.append({
                'x': random.uniform(-self.radio_x + 8, self.radio_x - 8),  # Ajustado para forma oval
                'y': random.uniform(-self.radio_y + 6, self.radio_y - 6),  # Ajustado para forma oval
                'tam': random.uniform(2, 4)
            })
    
    def actualizar_deformacion(self, imanes):
        """Actualiza la deformación de la gota según campo magnético cercano"""
        self.intensidad_campo = 0
        campo_total_x = 0
        campo_total_y = 0
        
        for iman in imanes:
            if iman.activo or iman.oscilando:
                dx = iman.x - self.x
                dy = iman.y - self.y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < RADIO_INFLUENCIA_IMAN:
                    intensidad = iman.intensidad * (1 - dist / RADIO_INFLUENCIA_IMAN)
                    self.intensidad_campo = max(self.intensidad_campo, intensidad)
                    campo_total_x += dx * intensidad
                    campo_total_y += dy * intensidad
        
        # Deformación: se estira en dirección del campo (efecto de picos)
        # Deformación simple
        if self.intensidad_campo > 0.1:
            magnitud = math.sqrt(campo_total_x**2 + campo_total_y**2)
            if magnitud > 0:
                angulo = math.atan2(campo_total_y, campo_total_x)
                # Mantener la forma ovalada base
                self.radio_x = self.radio_base * 1.45 * (1 + 0.2 * self.intensidad_campo * abs(math.cos(angulo)))
                self.radio_y = self.radio_base * 0.73 * (1 - 0.15 * self.intensidad_campo * abs(math.sin(angulo)))
        else:
            self.radio_x = self.radio_base * 1.45  # 32 aprox (22 * 1.45)
            self.radio_y = self.radio_base * 0.73  # 16 aprox (22 * 0.73)

            
    
    def mover(self, imanes, vibracion, temperatura, viscosidad_actual, velocidad_fase):
        """Mueve la gota con influencia magnética y térmica"""
        self.tiempo_vida += 1
        
        # Ajustar velocidad por temperatura (menor viscosidad = mayor velocidad)
        factor_temp = 1 + (temperatura - MIN_TEMPERATURA) / MAX_TEMPERATURA * 0.3
        
        # Movimiento base con velocidad de fase
        self.x += velocidad_fase * factor_temp
        self.y += self.vel_y
        
        # Atracción magnética
        for iman in imanes:
            if iman.activo or iman.oscilando:
                dx = iman.x - self.x
                dy = iman.y - self.y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < RADIO_INFLUENCIA_IMAN:
                    fuerza = iman.intensidad * (1 - dist / RADIO_INFLUENCIA_IMAN) * 0.8
                    self.x += dx * fuerza
                    self.y += dy * fuerza
        
        # Vibración por mezcla activa
        if vibracion:
            self.x += random.uniform(-0.6, 0.6)
            self.y += random.uniform(-0.5, 0.5)
        
        # Ajuste Y al canal serpenteante
        from config import obtener_y_canal
        y_canal = obtener_y_canal(self.x)
        self.y = y_canal + random.uniform(-3, 3)
    
    def dibujar(self, pantalla):
        """Dibuja la gota con forma ovalada"""
        # Sombra (ovalada)
        pygame.draw.ellipse(pantalla, (20, 20, 25), 
                        (int(self.x - self.radio_x - 2), int(self.y - self.radio_y - 2),
                            int(self.radio_x * 2 + 4), int(self.radio_y * 2 + 4)))
        
        # Cuerpo principal con gradiente (ovalado)
        for i in range(int(self.radio_y), 0, -3):
            escala = i / self.radio_y
            gris = int(60 + 50 * escala)
            radio_x_actual = self.radio_x * escala
            radio_y_actual = self.radio_y * escala
            pygame.draw.ellipse(pantalla, (gris, gris, gris + 40),
                            (int(self.x - radio_x_actual), int(self.y - radio_y_actual),
                                int(radio_x_actual * 2), int(radio_y_actual * 2)))
        
        # Brillo especular (ovalado, desplazado hacia arriba)
        pygame.draw.ellipse(pantalla, (200, 200, 220),
                        (int(self.x - self.radio_x * 0.5), int(self.y - self.radio_y * 0.6),
                            int(self.radio_x * 1.0), int(self.radio_y * 0.4)))
        
        # Borde (ovalado)
        pygame.draw.ellipse(pantalla, (120, 120, 140),
                        (int(self.x - self.radio_x), int(self.y - self.radio_y),
                            int(self.radio_x * 2), int(self.radio_y * 2)), 2)
        
        # Partículas internas
        for p in self.particulas:
            px = self.x + p['x'] * (self.radio_x / self.radio_base)
            py = self.y + p['y'] * (self.radio_y / self.radio_base)
            gris = int(100 + 60 * self.intensidad_campo)
            pygame.draw.circle(pantalla, (gris, gris, gris), (int(px), int(py)), int(p['tam']))