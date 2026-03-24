import pygame
from config import *
from sistemas.fisica import obtener_nombre_fase, obtener_color_fase

class PanelControl:
    """Panel de control con indicadores industriales"""
    
    def __init__(self):
        self.tiempo_led = 0
        self.rect = pygame.Rect(ANCHO - 320, ALTO - 340, 300, 320)
    
    def dibujar(self, pantalla, fase, fase_tiempo, temperatura, reynolds, 
                vibracion, velocidad, ciclos, eficiencia, densidad, viscosidad, tension):
        """Dibuja el panel de control completo"""
        self.tiempo_led += 1
        
        # Fondo del panel
        pygame.draw.rect(pantalla, (35, 35, 45), self.rect)
        pygame.draw.rect(pantalla, (80, 80, 95), self.rect, 2)
        
        # Título
        titulo = FUENTE_GRANDE.render("PANEL DE CONTROL", True, CIAN)
        pantalla.blit(titulo, (self.rect.x + 10, self.rect.y + 8))
        
        y_actual = self.rect.y + 45
        self._dibujar_fase(pantalla, fase, y_actual)
        
        y_actual += 35
        self._dibujar_barra_progreso(pantalla, fase, fase_tiempo, y_actual)
        
        y_actual += 25
        self._dibujar_temperatura(pantalla, temperatura, y_actual)
        
        y_actual += 30
        self._dibujar_reynolds(pantalla, reynolds, y_actual)
        
        y_actual += 35
        self._dibujar_mezcla(pantalla, vibracion, y_actual)
        
        y_actual += 30
        self._dibujar_velocidad(pantalla, velocidad, y_actual)
        
        y_actual += 28
        self._dibujar_ciclos(pantalla, ciclos, y_actual)
        
        y_actual += 28
        self._dibujar_eficiencia(pantalla, eficiencia, y_actual)
        
        y_actual += 35
        self._dibujar_propiedades(pantalla, densidad, viscosidad, tension, y_actual)
    
    def _dibujar_fase(self, pantalla, fase, y):
        """Dibuja indicador de fase con LED"""
        color_fase = obtener_color_fase(fase)
        nombre_fase = obtener_nombre_fase(fase)
        
        # LED parpadeante
        if self.tiempo_led % 30 < 15:
            pygame.draw.circle(pantalla, color_fase, (self.rect.x + 25, y + 12), 10)
            pygame.draw.circle(pantalla, BLANCO, (self.rect.x + 25, y + 12), 10, 1)
        
        texto = FUENTE_GRANDE.render(f"FASE: {nombre_fase}", True, color_fase)
        pantalla.blit(texto, (self.rect.x + 45, y + 5))
    
    def _dibujar_barra_progreso(self, pantalla, fase, fase_tiempo, y):
        """Dibuja barra de progreso de fase"""
        duraciones = {
            1: DURACION_FASE_INYECCION,
            2: DURACION_FASE_CAPTURA,
            3: DURACION_FASE_TRANSPORTE,
            4: DURACION_FASE_SEPARACION
        }
        duracion = duraciones.get(fase, 180)
        progreso = min(1.0, fase_tiempo / duracion)
        
        pygame.draw.rect(pantalla, (50, 50, 60), (self.rect.x + 15, y, 270, 12))
        pygame.draw.rect(pantalla, obtener_color_fase(fase), 
                        (self.rect.x + 15, y, int(270 * progreso), 12))
    
    def _dibujar_temperatura(self, pantalla, temperatura, y):
        """Dibuja medidor de temperatura"""
        temp_norm = (temperatura - MIN_TEMPERATURA) / (MAX_TEMPERATURA - MIN_TEMPERATURA)
        temp_norm = max(0, min(1, temp_norm))
        color = (int(255 * temp_norm), int(255 * (1 - temp_norm)), 0)
        
        pygame.draw.rect(pantalla, (50, 50, 60), (self.rect.x + 15, y, 180, 20))
        pygame.draw.rect(pantalla, color, (self.rect.x + 15, y, int(180 * temp_norm), 20))
        
        texto = FUENTE.render(f"{temperatura:.0f}°C", True, BLANCO)
        pantalla.blit(texto, (self.rect.x + 200, y + 2))
        pantalla.blit(FUENTE.render("Temperatura", True, BLANCO), (self.rect.x + 15, y + 22))
    
    def _dibujar_reynolds(self, pantalla, reynolds, y):
        """Dibuja medidor de Reynolds"""
        re_norm = min(1.0, reynolds / 2.0)
        if reynolds < 1:
            color = VERDE
        elif reynolds < 2:
            color = AMARILLO
        else:
            color = ROJO
        
        pygame.draw.rect(pantalla, (50, 50, 60), (self.rect.x + 15, y, 180, 20))
        pygame.draw.rect(pantalla, color, (self.rect.x + 15, y, int(180 * re_norm), 20))
        
        texto = FUENTE.render(f"{reynolds:.3f}", True, BLANCO)
        pantalla.blit(texto, (self.rect.x + 200, y + 2))
        pantalla.blit(FUENTE.render("Reynolds (Re)", True, BLANCO), (self.rect.x + 15, y + 22))
    
    def _dibujar_mezcla(self, pantalla, vibracion, y):
        """Dibuja indicador de mezcla activa"""
        if vibracion:
            color = NARANJA
            texto_estado = "ACTIVA"
        else:
            color = GRIS
            texto_estado = "INACTIVA"
        
        pygame.draw.circle(pantalla, color, (self.rect.x + 25, y + 8), 8)
        pygame.draw.circle(pantalla, BLANCO, (self.rect.x + 25, y + 8), 8, 1)
        
        texto = FUENTE.render(f"Mezcla activa: {texto_estado}", True, color)
        pantalla.blit(texto, (self.rect.x + 45, y + 2))
    
    def _dibujar_velocidad(self, pantalla, velocidad, y):
        """Dibuja indicador de velocidad de flujo"""
        vel_norm = min(1.0, velocidad / 2.0)
        pygame.draw.rect(pantalla, (50, 50, 60), (self.rect.x + 15, y, 180, 15))
        pygame.draw.rect(pantalla, CIAN, (self.rect.x + 15, y, int(180 * vel_norm), 15))
        
        texto = FUENTE.render(f"{velocidad:.1f} µL/min", True, BLANCO)
        pantalla.blit(texto, (self.rect.x + 200, y))
        pantalla.blit(FUENTE.render("Flujo", True, BLANCO), (self.rect.x + 15, y + 18))
    
    def _dibujar_ciclos(self, pantalla, ciclos, y):
        """Dibuja contador de ciclos"""
        texto = FUENTE.render(f"Ciclos completados: {ciclos}", True, DORADO)
        pantalla.blit(texto, (self.rect.x + 15, y))
    
    def _dibujar_eficiencia(self, pantalla, eficiencia, y):
        """Dibuja barra de eficiencia de mezcla"""
        pygame.draw.rect(pantalla, (50, 50, 60), (self.rect.x + 15, y, 200, 12))
        pygame.draw.rect(pantalla, VERDE, (self.rect.x + 15, y, int(200 * eficiencia / 100), 12))
        
        texto = FUENTE.render(f"Eficiencia: {eficiencia:.0f}%", True, BLANCO)
        pantalla.blit(texto, (self.rect.x + 220, y))
        pantalla.blit(FUENTE.render("Mezcla", True, BLANCO), (self.rect.x + 15, y + 15))
    
    def _dibujar_propiedades(self, pantalla, densidad, viscosidad, tension, y):
        """Dibuja propiedades de los fluidos"""
        textos = [
            f"ρ: {densidad:.0f} kg/m³",
            f"μ: {viscosidad:.4f} Pa·s",
            f"σ: {tension:.3f} N/m"
        ]
        
        for i, texto in enumerate(textos):
            render = FUENTE_PEQUEÑA.render(texto, True, GRIS_CLARO)
            pantalla.blit(render, (self.rect.x + 15 + i * 95, y))