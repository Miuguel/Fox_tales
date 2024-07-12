import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE))):
        """
        Inicializa um objeto Tile.

        Args:
        - pos (tuple): Posição inicial do tile (x, y).
        - groups (pygame.sprite.Group): Grupos aos quais o tile deve ser adicionado.
        - sprite_type (str): Tipo de sprite do tile ('floor', 'wall', 'object', etc.).
        - surface (pygame.Surface, opcional): Superfície para o tile. Padrão é uma superfície preta do tamanho TILESIZExTILESIZE.

        Attributes:
        - sprite_type (str): Tipo de sprite do tile.
        - image (pygame.Surface): Superfície do tile.
        - rect (pygame.Rect): Retângulo que define a posição e o tamanho do tile na tela.
        - hitbox (pygame.Rect): Área de colisão do tile, inflada verticalmente de acordo com HITBOX_OFFSET[sprite_type].
        """
        super().__init__(groups)
        self.sprite_type = sprite_type
        y_offset = HITBOX_OFFSET[sprite_type]
        self.image = surface

        # Define o retângulo e a hitbox do tile
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, y_offset)
