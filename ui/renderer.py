import pygame
from config import *

class Renderer:
    """Clase para renderizar elementos estáticos de la interfaz"""
    
    def __init__(self):
        pass
    
    def dibujar_fondo(self, pantalla):
        """Dibuja el fondo con imagen o rejilla por defecto"""
        try:
            # Intentar cargar y dibujar la imagen de fondo
            fondo = pygame.image.load(RUTA_FONDO).convert()
            fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
            pantalla.blit(fondo, (0, 0))
        except:
            # Si no se encuentra la imagen, usar la rejilla por defecto
            pantalla.fill((18, 18, 25))
            
            # Rejilla de fondo
            for x in range(0, ANCHO, 40):
                pygame.draw.line(pantalla, (28, 28, 35), (x, 0), (x, ALTO), 1)
            for y in range(0, ALTO, 40):
                pygame.draw.line(pantalla, (28, 28, 35), (0, y), (ANCHO, y), 1)
    
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
        
        # Nombres de fase
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
        
    def dibujar_reactor(self, pantalla):
        """Dibuja la imagen base del reactor que cubre todo el canal"""
        try:
            # Intentar cargar la imagen del reactor
            reactor_img = pygame.image.load(RUTA_IMAGEN_REACTOR).convert_alpha()
            
            # Calcular el ancho necesario para cubrir desde la entrada hasta la salida
            ancho_reactor = CANAL_FIN_X - CANAL_INICIO_X + 200  # +200 para cubrir entradas y salidas
            
            # Escalar la imagen al ancho necesario
            ancho_original = reactor_img.get_width()
            alto_original = reactor_img.get_height()
            escala = ancho_reactor / ancho_original
            nuevo_alto = int(alto_original * escala)
            
            reactor_img = pygame.transform.scale(reactor_img, (ancho_reactor, nuevo_alto))
            
            # Dibujar la imagen en la posición configurada
            pantalla.blit(reactor_img, (POS_X_IMAGEN_REACTOR, POS_Y_IMAGEN_REACTOR))
            
        except Exception as e:
            # Si no se encuentra la imagen, no hacer nada (solo mostrar el canal por defecto)
            pass

    