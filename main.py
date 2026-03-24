"""
SIMULADOR DE MICROREACTOR CON FERROFLUIDOS
Sistema automático de transporte y mezcla
Versión 2.0 - Modular
"""

import pygame
import sys
from config import ANCHO, ALTO, FPS
from sistemas.simulador import Simulador

def main():
    """Punto de entrada principal del simulador"""
    
    # Inicializar pygame
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("SIMULADOR DE MICROREACTOR CON FERROFLUIDOS")
    reloj = pygame.time.Clock()
    
    # Crear instancia del simulador
    simulador = Simulador()
    
    # Bucle principal
    corriendo = True
    while corriendo:
        # Procesar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False
                elif evento.key == pygame.K_r:
                    # Reiniciar simulación (útil para pruebas)
                    simulador = Simulador()
                    print(">>> Simulación reiniciada")
        
        # Actualizar lógica
        simulador.actualizar()
        
        # Dibujar
        simulador.dibujar(pantalla)
        
        # Actualizar pantalla
        pygame.display.flip()
        reloj.tick(FPS)
    
    # Cerrar pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()