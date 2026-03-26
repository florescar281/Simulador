import pygame
import random
from config import *
from entidades import GotaFerrofluido,  FlujoContinuo, Electroiman
from sistemas.fisica import (
    calcular_reynolds, 
    calcular_viscosidad_por_temperatura,
    calcular_velocidad_por_fase,
    obtener_nombre_fase,
    obtener_color_fase
)
from utils import *
from ui.panel import PanelControl
from ui.renderer import Renderer

class Simulador:
    """Clase principal del simulador con lógica automática"""
    
    def __init__(self):
        # Estado general
        self.simulando = True
        self.fase = 1  # 1: Inyección, 2: Captura, 3: Transporte, 4: Separación
        self.fase_tiempo = 0
        self.temperatura = TEMPERATURA_INICIAL
        self.ciclos = 0
        self.vibracion = True  # Mezcla activa automática en fase 3
        self.frame_count = 0
        
        # Propiedades de fluidos (variables)
        self.densidad = DENSIDAD_BASE
        self.viscosidad_base = VISCOSIDAD_BASE
        self.viscosidad_actual = VISCOSIDAD_BASE
        self.tension_superficial = TENSION_SUPERFICIAL_BASE
        
        # Elementos de la simulación
        self.gotas = []
        # self.reactivos = []
        self.imanes = []
        self.flujo_reactivo = None 
        
        # Contadores
        self.tiempo_entre_gotas = 0
        
        # Inicializar componentes
        self._inicializar_imanes()
        self._inicializar_gotas_iniciales()
        
        # Componentes UI
        self.panel = PanelControl()
        self.renderer = Renderer()
    
    def _inicializar_imanes(self):
        """Inicializa los electroimanes"""
        for i, pos in enumerate(POS_IMANES):
            self.imanes.append(Electroiman(pos['x'], pos['y'], i))

         # Agregar imán sensor (si está activo)
        if IMAN_SENSOR_ACTIVO:
            from entidades.electroiman import ImanSensor
            self.imanes.append(ImanSensor(IMAN_SENSOR_POS['x'], 
                                        IMAN_SENSOR_POS['y'], 
                                        5))
    
    def _inicializar_gotas_iniciales(self):
        y_ini = obtener_y_canal(CANAL_INICIO_X)
        self.gotas.append(GotaFerrofluido(CANAL_INICIO_X + 100, y_ini))
        
        # Reactivo A - entrada SUPERIOR (azul)
        self.flujo_reactivo_a = FlujoContinuo(
            ENTRADA_A_X, 
            y_ini, 
            self.densidad, 
            self.viscosidad_actual, 
            color=(80, 150, 255),
            offset_y=ENTRADA_A_Y_OFFSET
        )
        
        # Reactivo B - entrada INFERIOR (verde)
        self.flujo_reactivo_b = FlujoContinuo(
            ENTRADA_B_X, 
            y_ini, 
            self.densidad, 
            self.viscosidad_actual, 
            color=(0, 200, 150),
            offset_y=ENTRADA_B_Y_OFFSET
        )
        
    def obtener_velocidad_actual(self):
        """Obtiene velocidad actual según fase y temperatura"""
        return calcular_velocidad_por_fase(self.fase, self.temperatura)
    
    def actualizar_sensor(self):
        """Actualiza el imán sensor detectando gotas cercanas"""
        sensor = None
        for iman in self.imanes:
            if hasattr(iman, 'nombre') and iman.nombre == "SENSOR":
                sensor = iman
                break
        
        if sensor:
            # Detectar si alguna gota está cerca
            detectado = False
            for gota in self.gotas:
                if sensor.detectar_gota(gota.x, gota.y):
                    detectado = True
            
            # Actualizar el sensor
            sensor.actualizar()

    def actualizar_fase_automatica(self):
        """Actualiza la fase automáticamente según condiciones"""
        if self.fase == 1:
            # Fase de inyección: esperar a tener suficiente flujo o tiempo
            if self.fase_tiempo > DURACION_FASE_INYECCION or len(self.gotas) >= MAX_GOTAS_SIMULTANEAS:
                self._cambiar_fase(2)
        
        elif self.fase == 2:
            # Fase de captura: esperar tiempo suficiente
            if self.fase_tiempo > DURACION_FASE_CAPTURA:
                self._cambiar_fase(3)
        
        elif self.fase == 3:
            # Fase de transporte: esperar a que gotas lleguen al final
            if self.gotas and self.gotas[-1].x > CANAL_FIN_X - 100:
                self._cambiar_fase(4)
        
        elif self.fase == 4:
            # Fase de separación: procesar separación y recirculación
            if self.fase_tiempo > DURACION_FASE_SEPARACION:
                self._cambiar_fase(1)
                self.ciclos += 1
        
        self.fase_tiempo += 1
    
    def _cambiar_fase(self, nueva_fase):
        """Cambia la fase y resetea contadores"""
        self.fase = nueva_fase
        self.fase_tiempo = 0
    
    def actualizar_imanes(self):
        """Actualiza estado de imanes según fase y posición de gotas"""
        # Resetear todos los imanes
        for iman in self.imanes:
            iman.desactivar()
        
        if self.fase == 2 and self.gotas:
            # Captura: activar primer imán
            self.imanes[0].activar()
        
        elif self.fase == 3 and self.gotas:
            # Transporte: activación secuencial según posición
            gota_principal = self.gotas[0]
            mejor_iman = None
            menor_dist = 999
            
            for iman in self.imanes:
                dist = abs(gota_principal.x - iman.x)
                if dist < UMBRAL_ACTIVACION_IMAN and dist < menor_dist:
                    menor_dist = dist
                    mejor_iman = iman
            
            if mejor_iman:
                mejor_iman.activar()
                # Mezcla activa automática en imán central (índice 2)
                if mejor_iman.indice == 2 and self.vibracion:
                    mejor_iman.oscilando = True
                    mejor_iman.activo = False
    
    def actualizar_temperatura(self):
        """Actualiza temperatura según mezcla activa y disipación"""
        if self.fase == 3 and self.vibracion:
            # Mezcla activa genera calor por fricción viscosa
            self.temperatura += 0.03
        else:
            # Disipación natural
            self.temperatura -= 0.01
        
        self.temperatura = max(MIN_TEMPERATURA, min(MAX_TEMPERATURA, self.temperatura))
        
        # Actualizar viscosidad según temperatura
        self.viscosidad_actual = calcular_viscosidad_por_temperatura(self.temperatura, self.viscosidad_base)
    
    def actualizar_gotas(self):
        velocidad = self.obtener_velocidad_actual()
    
        for gota in self.gotas:
            # Debug para ver posición de gotas cercanas al final
            if gota.x > CANAL_FIN_X - 50 and not hasattr(gota, 'en_recirculacion'):
                print(f"Gota cerca del final: x={gota.x}, en_recirculacion={hasattr(gota, 'en_recirculacion')}")
            
            gota.mover(self.imanes, self.fase == 3, self.temperatura, 
                    self.viscosidad_actual, velocidad)
            gota.actualizar_deformacion(self.imanes)
        
        # Actualizar ambos flujos
        if self.flujo_reactivo_a:
            self.flujo_reactivo_a.mover(velocidad)
            self.flujo_reactivo_a.actualizar_mezcla(self.fase == 3, self.temperatura)
        
        if self.flujo_reactivo_b:
            self.flujo_reactivo_b.mover(velocidad)
            self.flujo_reactivo_b.actualizar_mezcla(self.fase == 3, self.temperatura)
        
    def generar_nuevas_gotas(self):
        """Genera nuevas gotas de ferrofluido de forma continua"""
        self.tiempo_entre_gotas += 1
        if self.tiempo_entre_gotas > FRAMES_ENTRE_GOTAS and len(self.gotas) < MAX_GOTAS_SIMULTANEAS:
            y_nueva = obtener_y_canal(CANAL_INICIO_X)
            self.gotas.append(GotaFerrofluido(CANAL_INICIO_X + 20, y_nueva))
            self.tiempo_entre_gotas = 0
    
    def procesar_separacion_y_recirculacion(self):
        """Procesa la recirculación de gotas a través del canal de recirculación"""
        nuevas_gotas = []
        velocidad_actual = self.obtener_velocidad_actual()
        
        for gota in self.gotas:
            # Verificar si la gota está en el canal de recirculación
            if hasattr(gota, 'en_recirculacion') and gota.en_recirculacion:
                # MOVER HACIA LA IZQUIERDA (x disminuye)
                gota.x -= velocidad_actual * VELOCIDAD_RECIRCULACION  # ← Restar para ir hacia atrás
                
                # Actualizar Y según posición
                y_recirc = obtener_y_recirculacion(gota.x)
                if y_recirc:
                    gota.y = y_recirc + random.uniform(-2, 2)
                
                # Verificar si ya llegó al inicio del canal (ZONA DE SALIDA)
                if gota.x <= CANAL_INICIO_X + 30:
                    gota.en_recirculacion = False
                    gota.x = CANAL_INICIO_X + 20
                    gota.y = obtener_y_canal(gota.x)
                    nuevas_gotas.append(gota)
                else:
                    nuevas_gotas.append(gota)
            
            # Verificar si la gota debe entrar al canal de recirculación
            elif gota.x >= CANAL_FIN_X - 40:
                if CIRCULACION_ACTIVA:
                    gota.en_recirculacion = True
                    gota.x = CANAL_FIN_X + 10  # Posición inicial en recirculación
                    gota.y = obtener_y_recirculacion(gota.x)
                    gota.vel_y = 0
                    nuevas_gotas.append(gota)
                else:
                    y_nueva = obtener_y_canal(CANAL_INICIO_X)
                    gota.x = CANAL_INICIO_X + 10
                    gota.y = y_nueva
                    nuevas_gotas.append(gota)
            
            # Movimiento normal en canal principal (hacia la derecha)
            else:
                nuevas_gotas.append(gota)
        
        self.gotas = nuevas_gotas
        
        # Procesar reactivos...
        if self.flujo_reactivo_a and self.flujo_reactivo_a.x > CANAL_FIN_X + 100:
            y_nueva = obtener_y_canal(CANAL_INICIO_X)
            self.flujo_reactivo_a.x = CANAL_INICIO_X + 50
            self.flujo_reactivo_a.y = y_nueva
        
        if self.flujo_reactivo_b and self.flujo_reactivo_b.x > CANAL_FIN_X + 100:
            y_nueva = obtener_y_canal(CANAL_INICIO_X)
            self.flujo_reactivo_b.x = CANAL_INICIO_X + 80
            self.flujo_reactivo_b.y = y_nueva
            self.flujo_reactivo_b.largo = 0
    
    def calcular_reynolds_actual(self):
        """Calcula el Reynolds actual en tiempo real"""
        velocidad = self.obtener_velocidad_actual() / 1000  # convertir a m/s
        diametro = CANAL_ALTO / 1000  # convertir a metros
        return calcular_reynolds(velocidad, self.densidad, self.viscosidad_actual, diametro)
    
    def obtener_eficiencia_mezcla(self):
        eficiencia_a = self.flujo_reactivo_a.obtener_eficiencia() if self.flujo_reactivo_a else 0
        eficiencia_b = self.flujo_reactivo_b.obtener_eficiencia() if self.flujo_reactivo_b else 0
        return (eficiencia_a + eficiencia_b) / 2
    
    def actualizar(self):
        """Actualiza toda la simulación"""
        self.frame_count += 1
        self.actualizar_fase_automatica()
        self.actualizar_imanes()
        self.actualizar_temperatura()
        self.actualizar_gotas()
        self.generar_nuevas_gotas()
        self.procesar_separacion_y_recirculacion()
        self.actualizar_sensor()
        
        # Actualizar imanes
        for iman in self.imanes:
            iman.actualizar()

    def dibujar_entradas_separadas(pantalla):
        """Dibuja las dos entradas separadas que se unen"""
        
        # Entrada Reactivo A (superior)
        pygame.draw.rect(pantalla, (40, 40, 55), 
                        (ENTRADA_A_X - 30, CANAL_Y_BASE + ENTRADA_A_Y_OFFSET - 15, 50, 30))
        pygame.draw.rect(pantalla, AZUL, 
                        (ENTRADA_A_X - 30, CANAL_Y_BASE + ENTRADA_A_Y_OFFSET - 15, 50, 30), 2)
        pantalla.blit(FUENTE_PEQUEÑA.render("REACTIVO A", True, AZUL), 
                    (ENTRADA_A_X - 28, CANAL_Y_BASE + ENTRADA_A_Y_OFFSET - 12))
        
        # Entrada Reactivo B (inferior)
        pygame.draw.rect(pantalla, (40, 40, 55), 
                        (ENTRADA_B_X - 30, CANAL_Y_BASE + ENTRADA_B_Y_OFFSET - 15, 50, 30))
        pygame.draw.rect(pantalla, (0, 200, 150), 
                        (ENTRADA_B_X - 30, CANAL_Y_BASE + ENTRADA_B_Y_OFFSET - 15, 50, 30), 2)
        pantalla.blit(FUENTE_PEQUEÑA.render("REACTIVO B", True, (0, 200, 150)), 
                    (ENTRADA_B_X - 28, CANAL_Y_BASE + ENTRADA_B_Y_OFFSET - 12))
        
        # Tuberías que se unen
        puntos_a = [
            (ENTRADA_A_X - 10, CANAL_Y_BASE + ENTRADA_A_Y_OFFSET),
            (ENTRADA_A_X + 20, CANAL_Y_BASE + ENTRADA_A_Y_OFFSET),
            (PUNTO_UNION_X, CANAL_Y_BASE - 5)
        ]
        pygame.draw.lines(pantalla, AZUL, False, puntos_a, 2)
        
        puntos_b = [
            (ENTRADA_B_X - 10, CANAL_Y_BASE + ENTRADA_B_Y_OFFSET),
            (ENTRADA_B_X + 20, CANAL_Y_BASE + ENTRADA_B_Y_OFFSET),
            (PUNTO_UNION_X, CANAL_Y_BASE + 5)
        ]
        pygame.draw.lines(pantalla, (0, 200, 150), False, puntos_b, 2)
        
        # Punto de unión
        pygame.draw.circle(pantalla, (100, 100, 120), (PUNTO_UNION_X, CANAL_Y_BASE), 8)
        pygame.draw.circle(pantalla, (150, 150, 180), (PUNTO_UNION_X, CANAL_Y_BASE), 8, 2)
        
    def dibujar(self, pantalla):
        """Dibuja toda la escena"""

        dibujar_canal_serpenteante(pantalla)
        dibujar_entradas(pantalla)
        dibujar_bifurcacion_y(pantalla)
        
        # Dibujar canal de recirculación (NUEVO)
        dibujar_canal_recirculacion(pantalla)
        
        # Fondo
        self.renderer.dibujar_fondo(pantalla)
        
        # Base del reactor
        self.renderer.dibujar_marco_reactor_5(pantalla)
        self.renderer.dibujar_marco_reactor_3(pantalla)
        self.renderer.dibujar_marco_reactor_4(pantalla)
        
        # Dibujar imagen base del reactor (cubre todo el canal)
        self.renderer.dibujar_reactor(pantalla)

        # Dibujar marco del reactor
        self.renderer.dibujar_marco_reactor_2(pantalla)
        self.renderer.dibujar_marco_reactor(pantalla)
        
        # Título
        self.renderer.dibujar_titulo(pantalla)
        
        # imanes por encima
        imanes_arriba = []
        imanes_abajo = []

        for iman in self.imanes:
            if iman.y < CANAL_Y_BASE:
                imanes_arriba.append(iman)
            else:
                imanes_abajo.append(iman)

        # Imanes por encima del canal
        for iman in imanes_arriba:
            iman.dibujar(pantalla)
        

        self.renderer.dibujar_imagen_canal(pantalla)

        # 8. Flujos continuos
        if self.flujo_reactivo_a:
            self.flujo_reactivo_a.dibujar(pantalla)
        
        if self.flujo_reactivo_b:
            self.flujo_reactivo_b.dibujar(pantalla)
        
        # 9. Gotas de ferrofluido
        for gota in self.gotas:
            gota.dibujar(pantalla)

        # Imanes por debajo  
        for iman in imanes_abajo:
            iman.dibujar(pantalla)
        
        
        # Panel de control
        self.panel.dibujar(
            pantalla,
            fase=self.fase,
            fase_tiempo=self.fase_tiempo,
            temperatura=self.temperatura,
            reynolds=self.calcular_reynolds_actual(),
            vibracion=self.fase == 3,
            velocidad=self.obtener_velocidad_actual(),
            ciclos=self.ciclos,
            eficiencia=self.obtener_eficiencia_mezcla(),
            densidad=self.densidad,
            viscosidad=self.viscosidad_actual,
            tension=self.tension_superficial
        )
        
        # Instrucciones en la parte inferior
        self.renderer.dibujar_instrucciones(pantalla, self.fase, self.ciclos)