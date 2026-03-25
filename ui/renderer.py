import pygame
from config import *

class Renderer:
    """Clase para renderizar elementos estáticos de la interfaz"""
    
    def __init__(self):
        self.imagen_canal = None
        self.imagen_reactor = None
        self.cargar_imagen_canal()
        self.cargar_imagen_reactor()
    
    def cargar_imagen_canal(self):
        """Carga la imagen del canal"""
        try:
            self.imagen_canal = pygame.image.load(RUTA_IMAGEN_CANAL).convert_alpha()
            # Escalar la imagen al tamaño del canal
            ancho_deseado = CANAL_FIN_X - CANAL_INICIO_X + 180
            alto_deseado = CANAL_ALTO + 140
            self.imagen_canal = pygame.transform.scale(self.imagen_canal, (ancho_deseado, alto_deseado))
        except Exception as e:
            print(f"⚠️ Error cargando imagen del canal: {e}")
            self.imagen_canal = None
    
    def cargar_imagen_reactor(self):
        """Carga la imagen base del reactor"""
        try:
            self.imagen_reactor = pygame.image.load(RUTA_IMAGEN_REACTOR).convert_alpha()
            # Escalar para cubrir el área del reactor
            ancho_deseado = ANCHO - (CANAL_INICIO_X + 380)
            alto_deseado = ALTO - (CANAL_Y_BASE + 100)
            self.imagen_reactor = pygame.transform.scale(self.imagen_reactor, (ancho_deseado, alto_deseado))
        except Exception as e:
            print(f"⚠️ Error cargando imagen del reactor: {e}")
            self.imagen_reactor = None
    
    def dibujar_fondo(self, pantalla):
        """Dibuja el fondo con imagen o rejilla por defecto"""
        try:
            fondo = pygame.image.load(RUTA_FONDO).convert()
            fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
            pantalla.blit(fondo, (0, 0))
        except:
            pantalla.fill((18, 18, 25))
            for x in range(0, ANCHO, 40):
                pygame.draw.line(pantalla, (28, 28, 35), (x, 0), (x, ALTO), 1)
            for y in range(0, ALTO, 40):
                pygame.draw.line(pantalla, (28, 28, 35), (0, y), (ANCHO, y), 1)
    
    def dibujar_reactor(self, pantalla):
        """Dibuja la imagen base del reactor que cubre todo el fondo del área de trabajo"""
        if self.imagen_reactor:
            x_pos = CANAL_INICIO_X - 10
            y_pos = CANAL_Y_BASE - self.imagen_reactor.get_height() // 2 - 10
            pantalla.blit(self.imagen_reactor, (x_pos, y_pos))
        else:
            # Si no hay imagen, dibujar un fondo base
            pygame.draw.rect(pantalla, (25, 25, 35), (0, 0, ANCHO, ALTO))
    
    def dibujar_imagen_canal(self, pantalla):
        """Dibuja la imagen del canal por encima del canal dibujado"""
        if self.imagen_canal:
            # Calcular posición para alinear con el canal
            x_pos = CANAL_INICIO_X - 90
            y_pos = CANAL_Y_BASE - self.imagen_canal.get_height() // 2 + AJUSTE_Y_IMAGEN_CANAL + 20
            pantalla.blit(self.imagen_canal, (x_pos, y_pos))
    
    def dibujar_titulo(self, pantalla):
        """Dibuja el título principal"""
        titulo = FUENTE_TITULO.render("MICROREACTOR CON FERROFLUIDOS", True, CIAN)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 10))
        
        subtitulo = FUENTE.render("Sistema automático de transporte y mezcla", True, GRIS_CLARO)
        pantalla.blit(subtitulo, (ANCHO//2 - subtitulo.get_width()//2, 48))
    
    def dibujar_instrucciones(self, pantalla, fase, ciclos):
        """Dibuja las instrucciones en la parte inferior"""
        pygame.draw.rect(pantalla, (30, 30, 40), (20, ALTO - 85, 380, 75))
        pygame.draw.rect(pantalla, (70, 70, 85), (20, ALTO - 85, 380, 75), 2)
        
        fases_nombres = {1: "INYECCIÓN", 2: "CAPTURA", 3: "TRANSPORTE", 4: "SEPARACIÓN"}
        fases_colores = {1: VERDE, 2: AMARILLO, 3: NARANJA, 4: ROJO}
        
        textos = [
            f"SIMULACIÓN AUTOMÁTICA - PROCESO CONTINUO",
            f"Ciclo actual: {ciclos + 1} | Fase: {fases_nombres.get(fase, '?')}",
            "El sistema opera sin intervención manual | ESC: salir"
        ]
        
        for i, texto in enumerate(textos):
            color = fases_colores.get(fase, CIAN) if i == 1 else (CIAN if i == 0 else BLANCO)
            render = FUENTE.render(texto, True, color)
            pantalla.blit(render, (30, ALTO - 75 + i * 22))