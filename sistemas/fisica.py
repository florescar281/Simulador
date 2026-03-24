import math
from config import *

def calcular_reynolds(velocidad, densidad, viscosidad, diametro_caracteristico=0.055):
    """
    Calcula el número de Reynolds
    velocidad: m/s
    densidad: kg/m³
    viscosidad: Pa·s
    diametro_caracteristico: m (en metros, 55mm = 0.055m)
    """
    if viscosidad <= 0:
        return 4.0
    re = (densidad * velocidad * diametro_caracteristico) / viscosidad
    return max(0.01, min(5.0, re))

def calcular_viscosidad_por_temperatura(temperatura, viscosidad_base=VISCOSIDAD_BASE):
    """
    Calcula la viscosidad en función de la temperatura
    La viscosidad disminuye al aumentar la temperatura
    """
    factor = 1 - (temperatura - MIN_TEMPERATURA) / MAX_TEMPERATURA * COEFICIENTE_VISCOSIDAD_TEMP
    viscosidad = viscosidad_base * max(0.2, factor)
    return max(0.0002, viscosidad)

def calcular_velocidad_por_fase(fase, temperatura=25):
    """Calcula la velocidad de flujo según la fase y temperatura"""
    if fase == 1:
        base = VEL_FLUJO_BASE
    elif fase == 2:
        base = VEL_FLUJO_CAPTURA
    elif fase == 3:
        base = VEL_FLUJO_TRANSPORTE
    else:
        base = VEL_FLUJO_SEPARACION
    
    # Ajuste por temperatura (a mayor temperatura, menor viscosidad, mayor velocidad)
    factor_temp = 1 + (temperatura - MIN_TEMPERATURA) / MAX_TEMPERATURA * 0.2
    return base * factor_temp

def obtener_nombre_fase(fase):
    """Devuelve el nombre de la fase según su número"""
    fases = {
        1: "INYECCIÓN",
        2: "CAPTURA",
        3: "TRANSPORTE",
        4: "SEPARACIÓN"
    }
    return fases.get(fase, "DESCONOCIDO")

def obtener_color_fase(fase):
    """Devuelve el color asociado a la fase"""
    colores = {
        1: VERDE,
        2: AMARILLO,
        3: NARANJA,
        4: ROJO
    }
    return colores.get(fase, BLANCO)