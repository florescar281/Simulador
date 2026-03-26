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
        titulo = FUENTE_TITULO.render("MICROREACTOR CON FERROFLUIDOS", True, NEGRO)
        pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 10))
        
        subtitulo = FUENTE.render("Sistema automático de transporte y mezcla", True, GRIS_OSCURO)
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

    def dibujar_marco_reactor(self, pantalla):
        """Dibuja un rectángulo con esquinas redondeadas como marco del reactor"""
        # Definir el área del marco (ajusta estos valores según tu bandeja)
        marco_x = CANAL_INICIO_X + 10
        marco_y = CANAL_Y_BASE - 70
        marco_ancho = CANAL_FIN_X - CANAL_INICIO_X - 100
        marco_alto = 110
        
        # Color del marco (gris metálico con borde más oscuro)
        color_fondo = (45, 45, 55)
        color_borde = (120, 120, 140)
        
        # Dibujar rectángulo con esquinas redondeadas
        self._dibujar_rect_redondeado(pantalla, marco_x, marco_y, marco_ancho, marco_alto, 
                                      color_fondo, radio=15)
        self._dibujar_rect_redondeado(pantalla, marco_x, marco_y, marco_ancho, marco_alto, 
                                      color_borde, radio=15, grosor=2)
        
        # Efecto de brillo en los bordes (opcional)
        self._dibujar_rect_redondeado(pantalla, marco_x + 2, marco_y + 2, 
                                      marco_ancho - 4, marco_alto - 4, 
                                      (70, 70, 85), radio=13, grosor=1)
        
        # Sombra para dar profundidad
        self._dibujar_rect_redondeado(pantalla, marco_x + 3, marco_y + 3, 
                                      marco_ancho - 6, marco_alto - 6, 
                                      (25, 25, 35), radio=12, grosor=1)
    
    def _dibujar_rect_redondeado(self, pantalla, x, y, ancho, alto, color, radio=10, grosor=0):
        """Dibuja un rectángulo con esquinas redondeadas"""
        if grosor == 0:
            # Rectángulo relleno
            pygame.draw.rect(pantalla, color, (x + radio, y, ancho - 2 * radio, alto))
            pygame.draw.rect(pantalla, color, (x, y + radio, ancho, alto - 2 * radio))
            
            # Esquinas redondeadas
            pygame.draw.circle(pantalla, color, (x + radio, y + radio), radio)
            pygame.draw.circle(pantalla, color, (x + ancho - radio, y + radio), radio)
            pygame.draw.circle(pantalla, color, (x + radio, y + alto - radio), radio)
            pygame.draw.circle(pantalla, color, (x + ancho - radio, y + alto - radio), radio)
        else:
            # Solo borde
            # Líneas rectas
            pygame.draw.line(pantalla, color, (x + radio, y), (x + ancho - radio, y), grosor)
            pygame.draw.line(pantalla, color, (x + radio, y + alto), (x + ancho - radio, y + alto), grosor)
            pygame.draw.line(pantalla, color, (x, y + radio), (x, y + alto - radio), grosor)
            pygame.draw.line(pantalla, color, (x + ancho, y + radio), (x + ancho, y + alto - radio), grosor)
            
            # Esquinas redondeadas
            pygame.draw.arc(pantalla, color, (x, y, radio * 2, radio * 2), math.pi, math.pi * 1.5, grosor)
            pygame.draw.arc(pantalla, color, (x + ancho - radio * 2, y, radio * 2, radio * 2), math.pi * 1.5, math.pi * 2, grosor)
            pygame.draw.arc(pantalla, color, (x, y + alto - radio * 2, radio * 2, radio * 2), math.pi * 0.5, math.pi, grosor)
            pygame.draw.arc(pantalla, color, (x + ancho - radio * 2, y + alto - radio * 2, radio * 2, radio * 2), 0, math.pi * 0.5, grosor)

    def dibujar_marco_reactor_2(self, pantalla):
        """Dibuja un rectángulo con esquinas redondeadas como marco del reactor"""
        # Definir el área del marco (ajusta estos valores según tu bandeja)
        marco_x = CANAL_INICIO_X + 40
        marco_y = 130
        marco_ancho = CANAL_FIN_X - CANAL_INICIO_X - 190
        marco_alto = 270
        
        # Color del marco (gris metálico con borde más oscuro)
        color_fondo = (45, 45, 55)
        color_borde = (120, 120, 140)
        
        # Dibujar rectángulo con esquinas redondeadas
        self._dibujar_rect_redondeado(pantalla, marco_x, marco_y, marco_ancho, marco_alto, 
                                      color_fondo, radio=15)
        self._dibujar_rect_redondeado(pantalla, marco_x, marco_y, marco_ancho, marco_alto, 
                                      color_borde, radio=15, grosor=2)
        
        # Efecto de brillo en los bordes (opcional)
        self._dibujar_rect_redondeado(pantalla, marco_x + 2, marco_y + 2, 
                                      marco_ancho - 4, marco_alto - 4, 
                                      (70, 70, 85), radio=13, grosor=1)
        
        # Sombra para dar profundidad
        self._dibujar_rect_redondeado(pantalla, marco_x + 3, marco_y + 3, 
                                      marco_ancho - 6, marco_alto - 6, 
                                      (25, 25, 35), radio=12, grosor=1)
    def dibujar_marco_reactor_3(self, pantalla):
        """Dibuja un rectángulo con esquinas redondeadas como marco del reactor"""
        # Definir el área del marco (ajusta estos valores según tu bandeja)
        marco_x = CANAL_FIN_X - 180
        marco_y = CANAL_Y_BASE - 70
        marco_ancho = CANAL_INICIO_X + 100
        marco_alto = 240
        
        # Color del marco (gris metálico con borde más oscuro)
        color_fondo = GRIS_CLARO 
        color_borde = (120, 120, 140)
        
        # Dibujar rectángulo con esquinas redondeadas
        self._dibujar_rect_redondeado(pantalla, marco_x, marco_y, marco_ancho, marco_alto, 
                                      color_fondo, radio=15)
        self._dibujar_rect_redondeado(pantalla, marco_x, marco_y, marco_ancho, marco_alto, 
                                      color_borde, radio=15, grosor=2)
        
        # Efecto de brillo en los bordes (opcional)
        self._dibujar_rect_redondeado(pantalla, marco_x + 2, marco_y + 2, 
                                      marco_ancho - 4, marco_alto - 4, 
                                      (70, 70, 85), radio=13, grosor=1)
        
        # Sombra para dar profundidad
        self._dibujar_rect_redondeado(pantalla, marco_x + 3, marco_y + 3, 
                                      marco_ancho - 6, marco_alto - 6, 
                                      (25, 25, 35), radio=12, grosor=1)
    
    def dibujar_marco_reactor_4(self, pantalla):
            """Dibuja un rectángulo con esquinas redondeadas como marco del reactor"""
            # Definir el área del marco (ajusta estos valores según tu bandeja)
            marco_x = CANAL_INICIO_X - 100
            marco_y = CANAL_Y_BASE - 70
            marco_ancho = 200
            marco_alto = 140
            
            # Color del marco (gris metálico con borde más oscuro)
            color_fondo = GRIS_CLARO 
            color_borde = (120, 120, 140)
            
            # Dibujar rectángulo con esquinas redondeadas
            self._dibujar_rect_redondeado(pantalla, marco_x, marco_y, marco_ancho, marco_alto, 
                                        color_fondo, radio=15)
            self._dibujar_rect_redondeado(pantalla, marco_x, marco_y, marco_ancho, marco_alto, 
                                        color_borde, radio=15, grosor=2)
            
            # Efecto de brillo en los bordes (opcional)
            self._dibujar_rect_redondeado(pantalla, marco_x + 2, marco_y + 2, 
                                        marco_ancho - 4, marco_alto - 4, 
                                        (70, 70, 85), radio=13, grosor=1)
            
            # Sombra para dar profundidad
            self._dibujar_rect_redondeado(pantalla, marco_x + 3, marco_y + 3, 
                                        marco_ancho - 6, marco_alto - 6, 
                                        (25, 25, 35), radio=12, grosor=1)
        

    def dibujar_marco_reactor_5(self, pantalla):
        """Dibuja un rectángulo con esquinas redondeadas como marco del reactor"""
        # Definir el área del marco (ajusta estos valores según tu bandeja)
        marco_x = CANAL_INICIO_X - 140
        marco_y = 80
        marco_ancho = CANAL_FIN_X - CANAL_INICIO_X + 300
        marco_alto = 400
        
        # Color del marco (gris metálico con borde más oscuro)
        color_fondo = GRIS
        color_borde = (120, 120, 140)
        
        # Dibujar rectángulo con esquinas redondeadas
        self._dibujar_rect_redondeado(pantalla, marco_x, marco_y, marco_ancho, marco_alto, 
                                      color_fondo, radio=15)
        self._dibujar_rect_redondeado(pantalla, marco_x, marco_y, marco_ancho, marco_alto, 
                                      color_borde, radio=15, grosor=2)
        
        # Efecto de brillo en los bordes (opcional)
        self._dibujar_rect_redondeado(pantalla, marco_x + 2, marco_y + 2, 
                                      marco_ancho - 4, marco_alto - 4, 
                                      (70, 70, 85), radio=13, grosor=1)
        
        # Sombra para dar profundidad
        self._dibujar_rect_redondeado(pantalla, marco_x + 3, marco_y + 3, 
                                      marco_ancho - 6, marco_alto - 6, 
                                      (25, 25, 35), radio=12, grosor=1)
    