import pygame
from config import *
from entidades import GotaFerrofluido,  FlujoContinuo, Electroiman
from sistemas.fisica import (
    calcular_reynolds, 
    calcular_viscosidad_por_temperatura,
    calcular_velocidad_por_fase,
    obtener_nombre_fase,
    obtener_color_fase
)
from utils import obtener_y_canal, dibujar_canal_serpenteante, dibujar_entradas, dibujar_bifurcacion_y
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
    
    def _inicializar_gotas_iniciales(self):
        y_ini = obtener_y_canal(CANAL_INICIO_X)
        self.gotas.append(GotaFerrofluido(CANAL_INICIO_X + 30, y_ini))
        # Un solo flujo continuo en lugar de múltiples segmentos
        self.flujo_reactivo = FlujoContinuo(CANAL_INICIO_X + 50, y_ini, self.densidad, self.viscosidad_actual)
    
    def obtener_velocidad_actual(self):
        """Obtiene velocidad actual según fase y temperatura"""
        return calcular_velocidad_por_fase(self.fase, self.temperatura)
    
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
            gota.mover(self.imanes, self.fase == 3, self.temperatura, 
                    self.viscosidad_actual, velocidad)
            gota.actualizar_deformacion(self.imanes)
        
        # Actualizar flujo continuo
        if self.flujo_reactivo:
            self.flujo_reactivo.mover(velocidad)
            self.flujo_reactivo.actualizar_mezcla(self.fase == 3, self.temperatura)
            self.flujo_reactivo.extender(velocidad)
    
    def generar_nuevas_gotas(self):
        """Genera nuevas gotas de ferrofluido de forma continua"""
        self.tiempo_entre_gotas += 1
        if self.tiempo_entre_gotas > FRAMES_ENTRE_GOTAS and len(self.gotas) < MAX_GOTAS_SIMULTANEAS:
            y_nueva = obtener_y_canal(CANAL_INICIO_X)
            self.gotas.append(GotaFerrofluido(CANAL_INICIO_X + 20, y_nueva))
            self.tiempo_entre_gotas = 0
    
    def procesar_separacion_y_recirculacion(self):
        nuevas_gotas = []
        
        for gota in self.gotas:
            if gota.x > CANAL_FIN_X - 30:
                y_nueva = obtener_y_canal(CANAL_INICIO_X)
                gota.x = CANAL_INICIO_X + 10
                gota.y = y_nueva
                nuevas_gotas.append(gota)
            else:
                nuevas_gotas.append(gota)
        
        self.gotas = nuevas_gotas
        
        # Reiniciar flujo continuo cuando sale
        if self.flujo_reactivo and self.flujo_reactivo.x > CANAL_FIN_X + 100:
            y_nueva = obtener_y_canal(CANAL_INICIO_X)
            self.flujo_reactivo.x = CANAL_INICIO_X + 50
            self.flujo_reactivo.y = y_nueva
            self.flujo_reactivo.largo = 0
    
    def calcular_reynolds_actual(self):
        """Calcula el Reynolds actual en tiempo real"""
        velocidad = self.obtener_velocidad_actual() / 1000  # convertir a m/s
        diametro = CANAL_ALTO / 1000  # convertir a metros
        return calcular_reynolds(velocidad, self.densidad, self.viscosidad_actual, diametro)
    
    def obtener_eficiencia_mezcla(self):
        if not self.flujo_reactivo:
            return 0
        return self.flujo_reactivo.nivel_mezcla * 100
    
    def actualizar(self):
        """Actualiza toda la simulación"""
        self.frame_count += 1
        self.actualizar_fase_automatica()
        self.actualizar_imanes()
        self.actualizar_temperatura()
        self.actualizar_gotas()
        self.generar_nuevas_gotas()
        self.procesar_separacion_y_recirculacion()
        
        # Actualizar imanes
        for iman in self.imanes:
            iman.actualizar()
    
    def dibujar(self, pantalla):
        """Dibuja toda la escena"""
        # Fondo
        self.renderer.dibujar_fondo(pantalla)
        
        # Dibujar imagen base del reactor (cubre todo el canal)
        self.renderer.dibujar_reactor(pantalla)
        
        # Título
        self.renderer.dibujar_titulo(pantalla)
        
        # Canal y elementos estructurales
        dibujar_canal_serpenteante(pantalla)
        dibujar_entradas(pantalla)
        dibujar_bifurcacion_y(pantalla)
        
        # Imanes
        for iman in self.imanes:
            iman.dibujar(pantalla)
        
        # Flujo continuo de reactivo (detrás de las gotas)
        if self.flujo_reactivo:
            self.flujo_reactivo.dibujar(pantalla)
        
        # Gotas de ferrofluido (encima del flujo)
        for gota in self.gotas:
            gota.dibujar(pantalla)
        
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