import pygame
from settings import *
from random import randint

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player
        self.sounds = {
            'heal': pygame.mixer.Sound('../audio/heal.wav'),
            'flame': pygame.mixer.Sound('../audio/Fire.wav')
        }

    def heal(self, player, strength, cost, groups):
        """
        Método para curar o jogador.

        Args:
            player (Player): O objeto do jogador que será curado.
            strength (int): A quantidade de saúde a ser restaurada.
            cost (int): O custo de energia para usar esta habilidade.
            groups (pygame.sprite.Group): Grupo de sprites onde as partículas serão criadas.

        """
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal', player.rect.center, groups)

    def flame(self, player, cost, groups):
        """
        Método para lançar uma habilidade de chama.

        Args:
            player (Player): O objeto do jogador que lançará a chama.
            cost (int): O custo de energia para usar esta habilidade.
            groups (pygame.sprite.Group): Grupo de sprites onde as partículas serão criadas.

        """
        if player.energy >= cost:
            player.energy -= cost
            self.sounds['flame'].play()

            # Determina a direção da chama com base na direção atual do jogador
            if player.status.split('_')[0] == 'right':
                direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left':
                direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up':
                direction = pygame.math.Vector2(0, -1)
            else:
                direction = pygame.math.Vector2(0, 1)

            # Cria partículas de chama ao longo da direção determinada
            for i in range(1, 6):
                if direction.x:  # horizontal
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
                else:  # vertical
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
