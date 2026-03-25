import pygame
import math
from config import *

class Electroiman:
    """Electroimán con imagen (encendido/apagado) y LED de estado"""
    
    def __init__(self, x, y, indice):
        self.x = x
        self.y = y
        self.indice = indice
        self.activo = False
        self.oscilando = False
        self.intensidad = 0.7
        self.tiempo_oscilacion = 0
        
        # Imágenes
        self.imagen_off = None
        self.imagen_on = None
        self.ancho = 50
        self.alto = 50
        self.cargar_imagenes()
    
    def cargar_imagenes(self):
        """Carga las imágenes de los electroimanes"""
        try:
            # Cargar imagen apagada
            self.imagen_off = pygame.image.load(RUTA_IMAGEN_ELECTROIMAN_INACTIVO).convert_alpha()
            self.imagen_off = pygame.transform.scale(self.imagen_off, 
                                                     (int(self.imagen_off.get_width() * ESCALA_IMAN),
                                                      int(self.imagen_off.get_height() * ESCALA_IMAN)))
            self.ancho = self.imagen_off.get_width()
            self.alto = self.imagen_off.get_height()
            
            # Cargar imagen encendida
            self.imagen_on = pygame.image.load(RUTA_IMAGEN_ELECTROIMAN_ACTIVO).convert_alpha()
            self.imagen_on = pygame.transform.scale(self.imagen_on, (self.ancho, self.alto))
                
        except Exception as e:
            print(f"⚠️ Error cargando imágenes: {e}")
            print("Usando representación gráfica por defecto")
            self.imagen_off = None
            self.imagen_on = None
    
    def actualizar(self):
        """Actualiza estado del imán"""
        if self.oscilando:
            self.tiempo_oscilacion += 1
            self.intensidad = 0.5 + 0.4 * math.sin(self.tiempo_oscilacion * 0.25)
        else:
            self.intensidad = 0.7 if self.activo else 0
    
    def activar(self):
        """Activa el imán en modo estático"""
        self.activo = True
        self.oscilando = False
    
    def activar_oscilacion(self):
        """Activa el imán en modo oscilación (usa imagen encendida)"""
        self.activo = False
        self.oscilando = True
        self.tiempo_oscilacion = 0
    
    def desactivar(self):
        """Desactiva el imán"""
        self.activo = False
        self.oscilando = False
        self.intensidad = 0
    
    def dibujar(self, pantalla):
        """Dibuja el electroimán con imagen"""
        
        # Seleccionar imagen según estado
        if self.imagen_off and self.imagen_on:
            if self.activo or self.oscilando:
                imagen = self.imagen_on   # Usar misma imagen para encendido y oscilación
            else:
                imagen = self.imagen_off
            
            # Centrar la imagen en la posición del imán
            rect = imagen.get_rect(center=(self.x, self.y))
            pantalla.blit(imagen, rect)
        else:
            # Representación alternativa si no hay imágenes
            self._dibujar_alternativo(pantalla)
        
        # Dibujar LED de estado
        self._dibujar_led(pantalla)
        
        # Líneas de campo magnético (opcional)
        if self.activo or self.oscilando:
            self._dibujar_campo_magnetico(pantalla)
    
    def _dibujar_alternativo(self, pantalla):
        """Dibujo alternativo sin imágenes"""
        pygame.draw.rect(pantalla, (50, 50, 65), 
                        (self.x - 25, self.y - 20, 50, 40))
        pygame.draw.rect(pantalla, (80, 80, 100), 
                        (self.x - 25, self.y - 20, 50, 40), 2)
        
        if self.activo or self.oscilando:
            color = (180, 50, 50)
        else:
            color = (60, 60, 75)
        
        for i in range(3):
            x_bobina = self.x - 12 + i * 12
            pygame.draw.circle(pantalla, color, (x_bobina, self.y - 5), 6)
        
        pygame.draw.rect(pantalla, (90, 90, 110), (self.x - 6, self.y - 10, 12, 20))
    
    def _dibujar_led(self, pantalla):
        """Dibuja el LED de estado"""
        led_x = self.x + LED_OFFSET_X
        led_y = self.y + LED_OFFSET_Y
        
        if self.activo:
            # LED rojo parpadeante cuando está activo
            if pygame.time.get_ticks() % 400 < 200:
                led_color = (255, 80, 80)
            else:
                led_color = (255, 0, 0)
        elif self.oscilando:
            # LED naranja parpadeante cuando oscila
            if pygame.time.get_ticks() % 300 < 150:
                led_color = (255, 150, 50)
            else:
                led_color = (200, 100, 0)
        else:
            led_color = (40, 40, 40)
        
        pygame.draw.circle(pantalla, led_color, (led_x, led_y), LED_RADIO)
        pygame.draw.circle(pantalla, (200, 200, 200), (led_x, led_y), LED_RADIO, 1)
    
    def _dibujar_campo_magnetico(self, pantalla):
        """Dibuja líneas de campo magnético"""
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            longitud = 40 * self.intensidad
            x2 = self.x + longitud * math.cos(rad)
            y2 = self.y + longitud * math.sin(rad)
            color = (255, 100, 100) if self.activo else (255, 150, 50)
            pygame.draw.line(pantalla, color, (self.x, self.y), (int(x2), int(y2)), 1)