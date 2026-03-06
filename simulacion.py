import pygame
import math
import random
from config import *
from utils import *

pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("SISTEMA DE CONTROL - MICROREACTOR CON FERROFLUIDOS")
reloj = pygame.time.Clock()

class GotaFerrofluido:
    """Gota de ferrofluido con aspecto metálico"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radio = 22
        self.vel_x = VEL_FLUJO
        self.vel_y = 0
        self.particulas = []
        self.brillo = random.uniform(0.5, 1.0)
        
        # Crear partículas internas
        for _ in range(25):
            self.particulas.append({
                'x': random.uniform(-18, 18),
                'y': random.uniform(-18, 18),
                'tam': random.uniform(2, 5),
                'brillo': random.uniform(0.3, 1.0)
            })
    
    def mover(self, imanes, vibracion=False):
        self.x += self.vel_x
        self.y += self.vel_y
        
        campo_cercano = False
        for iman in imanes:
            if iman.activo or iman.oscilando: 
                dx = iman.x - self.x
                dy = iman.y - self.y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist < 120:
                    campo_cercano = True
                    factor = 0.08 * (1 - dist/120)
                    self.x += dx * factor
                    self.y += dy * factor
        
        if vibracion:
            self.x += random.uniform(-0.8, 0.8)
            self.y += random.uniform(-0.8, 0.8)
        
        if campo_cercano:
            self.brillo = min(1.0, self.brillo + 0.02)
        else:
            self.brillo = max(0.5, self.brillo - 0.01)
    
    def dibujar(self, pantalla):
        # Sombra
        pygame.draw.circle(pantalla, (30, 30, 30), (int(self.x+3), int(self.y+3)), self.radio)
        
        # Cuerpo principal con gradiente metálico
        for i in range(self.radio, 0, -3):
            gris = int(80 + 50 * self.brillo)
            color = (gris, gris, gris)
            pygame.draw.circle(pantalla, color, (int(self.x), int(self.y)), i)
        
        # Brillo 
        pygame.draw.circle(pantalla, (220, 220, 220), (int(self.x-5), int(self.y-5)), 8)
        
        # Borde
        pygame.draw.circle(pantalla, (150, 150, 150), (int(self.x), int(self.y)), self.radio, 2)
        
        # Partículas internas
        for p in self.particulas:
            px = self.x + p['x']
            py = self.y + p['y']
            gris = int(150 * p['brillo'])
            pygame.draw.circle(pantalla, (gris, gris, gris), (int(px), int(py)), int(p['tam']))

class SegmentoReactivo:
    """Segmento de reactivo con aspecto de fluido real"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 65
        self.alto = 45
        self.vel_x = VEL_FLUJO
        self.trazadores = []
        self.nivel_mezcla = 0

        for _ in range(40):
            self.trazadores.append({
                'x': random.uniform(-self.ancho/2, self.ancho/2),
                'y': random.uniform(-self.alto/2, self.alto/2),
                'vx': random.uniform(-0.3, 0.3),
                'vy': random.uniform(-0.3, 0.3),
                'edad': random.uniform(0, 100)
            })
    
    def mover(self, vibracion=False):
        self.x += self.vel_x
        
        if vibracion:
            self.nivel_mezcla = min(1.0, self.nivel_mezcla + 0.02)
        else:
            self.nivel_mezcla = max(0, self.nivel_mezcla - 0.01)
        
        # Movimiento de los trazadores
        for t in self.trazadores:
            if vibracion:
                # Efecto de vórtices
                ang = t['edad'] * 0.1
                t['vx'] += math.cos(ang) * 0.3
                t['vy'] += math.sin(ang) * 0.3
                t['edad'] += 1
            else:
                # Flujo laminar
                t['vx'] *= 0.98
                t['vy'] *= 0.98
            
            t['x'] += t['vx']
            t['y'] += t['vy']
            
            # Rebote en bordes
            if abs(t['x']) > self.ancho/2:
                t['vx'] *= -0.5
            if abs(t['y']) > self.alto/2:
                t['vy'] *= -0.5
    
    def dibujar(self, pantalla):
        sombra_rect = pygame.Rect(self.x - self.ancho/2 + 3, self.y - self.alto/2 + 3, self.ancho, self.alto)
        pygame.draw.rect(pantalla, (30, 30, 30), sombra_rect, border_radius=5)
        
        for i in range(self.alto):
            y_pos = self.y - self.alto/2 + i
            intensidad = int(50 + 50 * (1 - i/self.alto))
            color = (0, intensidad, 255)
            pygame.draw.line(pantalla, color, (self.x - self.ancho/2, y_pos), 
                           (self.x + self.ancho/2, y_pos))
        
        # Borde
        rect = pygame.Rect(self.x - self.ancho/2, self.y - self.alto/2, self.ancho, self.alto)
        pygame.draw.rect(pantalla, (0, 150, 255), rect, 2, border_radius=5)
        
        # Dibujar trazadores
        for t in self.trazadores:
            velocidad = math.sqrt(t['vx']**2 + t['vy']**2)
            if velocidad > 2:
                color = (255, 200, 0)
                tam = 4
            elif velocidad > 1:
                color = (255, 150, 0)
                tam = 3
            else:
                color = (100, 200, 255)
                tam = 2
            
            px = self.x + t['x']
            py = self.y + t['y']
            pygame.draw.circle(pantalla, color, (int(px), int(py)), tam)
        
        # Indicador de nivel
        if self.nivel_mezcla > 0.1:
            barra_x = self.x + self.ancho/2 + 5
            barra_y = self.y - self.alto/2
            alto_barra = self.alto * self.nivel_mezcla
            pygame.draw.rect(pantalla, (255, 200, 0), 
                           (barra_x, barra_y + self.alto - alto_barra, 5, alto_barra))

class PanelControl:
    """Panel de control con aspecto industrial"""
    def __init__(self):
        self.leds = {}
        self.medidores = {}
        self.tiempo = 0
        
    def dibujar(self, pantalla, fase, vibracion, temperatura=25):
        self.tiempo += 1
        
        # Fondo del panel
        pygame.draw.rect(pantalla, (40, 40, 45), (10, 10, 280, 200))
        pygame.draw.rect(pantalla, (80, 80, 90), (10, 10, 280, 200), 2)
        
        # Título del panel
        pantalla.blit(FUENTE_GRANDE.render("PANEL DE CONTROL", True, (0, 255, 255)), (20, 15))
        
        # Indicador de fase con LED
        y = 50
        fases_colores = {
            "INYECCION": (0, 255, 0),
            "CAPTURA": (255, 255, 0),
            "TRANSPORTE": (255, 165, 0),
            "SEPARACION": (255, 0, 0)
        }
        color_fase = fases_colores.get(fase, (255, 255, 255))
        
        # LED parpadeante
        if self.tiempo % 30 < 15:
            pygame.draw.circle(pantalla, color_fase, (40, y+10), 8)
            pygame.draw.circle(pantalla, BLANCO, (40, y+10), 8, 1)
        
        pantalla.blit(FUENTE.render(f"FASE: {fase}", True, color_fase), (60, y))
        
        # Medidor de temperatura
        y += 30
        pygame.draw.rect(pantalla, (30, 30, 35), (40, y, 150, 15))
        temp_width = int(150 * (temperatura - 20) / 30)
        pygame.draw.rect(pantalla, (255, 100, 0), (40, y, temp_width, 15))
        pantalla.blit(FUENTE.render(f"Temp: {temperatura}°C", True, BLANCO), (200, y))
        
        # Medidor de mezcla
        y += 25
        mezcla_color = (255, 255, 0) if vibracion else (100, 100, 100)
        pygame.draw.circle(pantalla, mezcla_color, (45, y+5), 5)
        pantalla.blit(FUENTE.render(f"Mezcla activa: {'SI' if vibracion else 'NO'}", 
                                   True, mezcla_color), (60, y))
        
        # Contador de gotas
        y += 25
        pantalla.blit(FUENTE.render(f"Flujo: {VEL_FLUJO} μL/min", True, BLANCO), (40, y))
        
        # Barra de progreso de fase
        y += 30
        pygame.draw.rect(pantalla, (30, 30, 35), (40, y, 200, 10))
        progreso = (self.tiempo % 300) / 300
        pygame.draw.rect(pantalla, (0, 255, 0), (40, y, int(200 * progreso), 10))

class MicroreactorVista:
    """Vista del microreactor con aspecto de máquina"""
    def __init__(self):
        self.ventanas = []
        self.tuberias = []
        self.valvulas = []
        
    def dibujar_estructura(self, pantalla):
        # Placa base
        pygame.draw.rect(pantalla, (60, 60, 70), (180, 200, 900, 200))
        pygame.draw.rect(pantalla, (100, 100, 110), (180, 200, 900, 200), 3)
        
        # Canal principal (como tubería de vidrio)
        pygame.draw.rect(pantalla, (150, 150, 160), (200, 250, 800, 60))
        pygame.draw.rect(pantalla, (200, 200, 210), (200, 250, 800, 60), 2)
        
        # Líneas de flujo
        for x in range(220, 980, 40):
            pygame.draw.line(pantalla, (100, 100, 110), (x, 255), (x, 305), 1)
        
        # Conexiones de entrada
        pygame.draw.rect(pantalla, (120, 120, 130), (50, 265, 150, 30))
        pygame.draw.rect(pantalla, (180, 180, 190), (50, 265, 150, 30), 2)
        texto_reactivo = FUENTE_PEQUEÑA.render("REACTIVO", True, AZUL)
        pantalla.blit(texto_reactivo, (80, 270))
        
        pygame.draw.rect(pantalla, (120, 120, 130), (125, 215, 50, 30))
        pygame.draw.rect(pantalla, (180, 180, 190), (125, 215, 50, 30), 2)
        texto_ferro = FUENTE_PEQUEÑA.render("FERRO", True, GRIS_CLARO)
        pantalla.blit(texto_ferro, (130, 220))
        
        # Conexiones de salida
        pygame.draw.rect(pantalla, (120, 120, 130), (1000, 265, 150, 30))
        pygame.draw.rect(pantalla, (180, 180, 190), (1000, 265, 150, 30), 2)
        texto_producto = FUENTE_PEQUEÑA.render("PRODUCTO", True, VERDE)
        pantalla.blit(texto_producto, (1030, 270))
        
        pygame.draw.rect(pantalla, (120, 120, 130), (1000, 315, 150, 30))
        pygame.draw.rect(pantalla, (180, 180, 190), (1000, 315, 150, 30), 2)
        texto_recuperacion = FUENTE_PEQUEÑA.render("RECUPERACIÓN", True, GRIS_CLARO)
        pantalla.blit(texto_recuperacion, (1010, 320))

class ElectroimanIndustrial:
    """Electroimán con aspecto industrial"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.activo = False
        self.oscilando = False
        self.intensidad = 0
        
    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, (70, 70, 80), (self.x-25, self.y-15, 50, 30))
        
        # Bobinas
        for i in range(3):
            if self.activo:
                color = (150, 50, 50)
            elif self.oscilando:
                parpadeo = 0.7 + 0.3 * math.sin(pygame.time.get_ticks() * 0.01)
                color = (180, int(150 * parpadeo), 0)
            else:
                color = (80, 80, 90)
            
            pygame.draw.circle(pantalla, color, (self.x-10 + i*10, self.y-10), 8)
            pygame.draw.circle(pantalla, (200, 200, 200), (self.x-10 + i*10, self.y-10), 8, 1)
        
        # Núcleo
        pygame.draw.rect(pantalla, (100, 100, 110), (self.x-8, self.y-5, 16, 20))
        
        # Líneas de campo
        if self.activo or self.oscilando:
            if self.activo:
                intensidad = 0.8
                color_linea = (200, 50, 50)
            else:
                intensidad = 0.5 + 0.3 * math.sin(pygame.time.get_ticks() * 0.01)
                color_linea = (255, 165, 0)
                
            for ang in range(0, 360, 30):
                rad = math.radians(ang)
                x2 = self.x + 40 * math.cos(rad)
                y2 = self.y + 40 * math.sin(rad)
                pygame.draw.line(pantalla, color_linea, (self.x, self.y), (x2, y2), 2)
        
        # LED de estado
        if self.activo:
            led_color = (255, 0, 0)
        elif self.oscilando:
            led_color = (255, 165, 0)
        else:
            led_color = (50, 50, 50)
            
        pygame.draw.circle(pantalla, led_color, (self.x+30, self.y-20), 5)
        pygame.draw.circle(pantalla, BLANCO, (self.x+30, self.y-20), 5, 1)

def main():
    fase = "INYECCION"
    vibracion = False
    tiempo_ultima_gota = 0
    temperatura = 25
    
    imanes = []
    for i, x in enumerate(POS_IMANES):
        iman = ElectroimanIndustrial(x, Y_IMAN)
        imanes.append(iman)
    
    panel = PanelControl()
    vista = MicroreactorVista()
    
    gotas = []
    reactivos = []
    
    corriendo = True
    while corriendo:
        dt = reloj.tick(FPS) / 1000
        
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if fase == "INYECCION":
                        fase = "CAPTURA"
                    elif fase == "CAPTURA":
                        fase = "TRANSPORTE"
                    elif fase == "TRANSPORTE":
                        fase = "SEPARACION"
                    else:
                        fase = "INYECCION"
                    print(f"FASE: {fase}")
                
                elif evento.key == pygame.K_v:
                    vibracion = not vibracion
                    print(f"MEZCLA: {'ACTIVA' if vibracion else 'INACTIVA'}")
        
        # Lógica de fases
        if fase == "INYECCION":
            tiempo_ultima_gota += dt
            if tiempo_ultima_gota > TIEMPO_ENTRE_GOTAS:
                gotas.append(GotaFerrofluido(180, 280))
                reactivos.append(SegmentoReactivo(250, 300))
                tiempo_ultima_gota = 0
                temperatura += 0.1
            
            for iman in imanes:
                iman.activo = False
                iman.oscilando = False
        
        elif fase == "CAPTURA":
            if gotas:
                imanes[0].activo = True
                gotas[0].vel_x *= 0.97
                temperatura += 0.05
        
        elif fase == "TRANSPORTE":
            for iman in imanes:
                iman.activo = False
                iman.oscilando = False
            
            if gotas:
                gota = gotas[0]
                for i, iman in enumerate(imanes):
                    if abs(gota.x - iman.x) < 60:
                        if vibracion and i == 2:
                            iman.oscilando = True
                            temperatura += 0.2
                        else:
                            iman.activo = True
                        
                        if i < len(imanes) - 1:
                            gota.vel_x = VEL_FLUJO * 1.8
                        break
        
        elif fase == "SEPARACION":
            for iman in imanes:
                iman.activo = False
                iman.oscilando = False
            
            for gota in gotas:
                if gota.x > 950:
                    gota.y = 350
                    gota.vel_x = VEL_FLUJO
            
            for reactivo in reactivos:
                if reactivo.x > 950:
                    reactivo.y = 300
                    reactivo.vel_x = VEL_FLUJO
                    temperatura = max(25, temperatura - 0.1)
        
        # Mover elementos
        for gota in gotas:
            gota.mover(imanes, vibracion)
        
        for reactivo in reactivos:
            reactivo.mover(vibracion)
        
        # Limpiar elementos fuera de pantalla
        gotas = [g for g in gotas if g.x < 1150]
        reactivos = [r for r in reactivos if r.x < 1150]
        
        pantalla.fill((20, 20, 25))
        
        # Fondo industrial
        for x in range(0, ANCHO, 50):
            pygame.draw.line(pantalla, (30, 30, 35), (x, 0), (x, ALTO), 1)
        for y in range(0, ALTO, 50):
            pygame.draw.line(pantalla, (30, 30, 35), (0, y), (ANCHO, y), 1)
        
        vista.dibujar_estructura(pantalla)
        
        for iman in imanes:
            iman.dibujar(pantalla)
        
        for reactivo in reactivos:
            reactivo.dibujar(pantalla)
        
        for gota in gotas:
            gota.dibujar(pantalla)
        
        panel.dibujar(pantalla, fase, vibracion, int(temperatura))
        
        pygame.draw.rect(pantalla, (40, 40, 45), (ANCHO-320, ALTO-120, 300, 100))
        pygame.draw.rect(pantalla, (80, 80, 90), (ANCHO-320, ALTO-120, 300, 100), 2)
        
        instrucciones = [
            "CONTROL DEL SISTEMA:",
            "[ESPACIO] Cambiar fase de operación",
            "[V] Activar/desactivar mezcla",
            f"FASE ACTUAL: {fase}"
        ]
        
        y = ALTO-110
        for texto in instrucciones:
            if "FASE ACTUAL" in texto:
                color = (0, 255, 255)
            else:
                color = BLANCO
            texto_render = FUENTE.render(texto, True, color)
            pantalla.blit(texto_render, (ANCHO-310, y))
            y += 20
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()