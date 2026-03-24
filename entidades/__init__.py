"""
Módulo de entidades del simulador
Contiene las clases que representan los elementos físicos del sistema
"""

from entidades.gota_ferrofluido import GotaFerrofluido
from entidades.segmento_reactivo import  FlujoContinuo
from entidades.electroiman import Electroiman

__all__ = [
    'GotaFerrofluido',
    'SegmentoReactivo', 
    'Electroiman'
]