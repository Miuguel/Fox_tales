import pygame

# Inicializa o pygame e define uma fonte para o texto de depuração
pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, y=10, x=10):
    """
    Exibe informações de depuração na tela.

    Args:
    - info (any): Informação a ser exibida na tela. Será convertida para string.
    - y (int): Posição vertical (em pixels) onde o texto será exibido na tela. Padrão é 10.
    - x (int): Posição horizontal (em pixels) onde o texto será exibido na tela. Padrão é 10.
    """
    # Obtém a superfície de exibição atual do pygame
    display_surface = pygame.display.get_surface()

    # Renderiza o texto de depuração
    debug_surf = font.render(str(info), True, 'White')

    # Obtém o retângulo do texto de depuração e define sua posição na tela
    debug_rect = debug_surf.get_rect(topleft=(x, y))

    # Desenha um retângulo preto ao redor do texto de depuração para melhor legibilidade
    pygame.draw.rect(display_surface, 'Black', debug_rect)

    # Exibe o texto de depuração na tela
    display_surface.blit(debug_surf, debug_rect)
