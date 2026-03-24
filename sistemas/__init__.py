"""
Módulo de sistemas del simulador
Contiene la lógica principal y cálculos físicos
"""

from sistemas.simulador import Simulador
from sistemas.fisica import (
    calcular_reynolds,
    calcular_viscosidad_por_temperatura,
    calcular_velocidad_por_fase,
    obtener_nombre_fase,
    obtener_color_fase
)

__all__ = [
    'Simulador',
    'calcular_reynolds',
    'calcular_viscosidad_por_temperatura',
    'calcular_velocidad_por_fase',
    'obtener_nombre_fase',
    'obtener_color_fase'
]