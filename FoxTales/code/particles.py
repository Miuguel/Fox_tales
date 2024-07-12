import pygame
from support import import_folder
from random import choice

class AnimationPlayer:
    def __init__(self):
        # Carrega os frames de animação de várias categorias
        self.frames = {
            # Magic
            'flame': import_folder('../graphics/particles/flame/frames'),
            'aura': import_folder('../graphics/particles/aura'),
            'heal': import_folder('../graphics/particles/heal/frames'),
            
            # Attacks
            'claw': import_folder('../graphics/particles/claw'),
            'slash': import_folder('../graphics/particles/slash'),
            'sparkle': import_folder('../graphics/particles/sparkle'),
            'leaf_attack': import_folder('../graphics/particles/leaf_attack'),
            'thunder': import_folder('../graphics/particles/thunder'),

            # Monster deaths
            'squid': import_folder('../graphics/particles/smoke_orange'),
            'raccoon': import_folder('../graphics/particles/raccoon'),
            'spirit': import_folder('../graphics/particles/nova'),
            'bamboo': import_folder('../graphics/particles/bamboo'),
            
            # Leafs
            'leaf': (
                import_folder('../graphics/particles/leaf1'),
                import_folder('../graphics/particles/leaf2'),
                import_folder('../graphics/particles/leaf3'),
                import_folder('../graphics/particles/leaf4'),
                import_folder('../graphics/particles/leaf5'),
                import_folder('../graphics/particles/leaf6'),
                self.reflect_images(import_folder('../graphics/particles/leaf1')),
                self.reflect_images(import_folder('../graphics/particles/leaf2')),
                self.reflect_images(import_folder('../graphics/particles/leaf3')),
                self.reflect_images(import_folder('../graphics/particles/leaf4')),
                self.reflect_images(import_folder('../graphics/particles/leaf5')),
                self.reflect_images(import_folder('../graphics/particles/leaf6'))
            )
        }

    def reflect_images(self, frames):
        """
        Método para espelhar frames de animação.

        Args:
            frames (list): Lista de frames de animação a serem espelhados.

        Returns:
            list: Lista de frames de animação espelhados.
        """
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups):
        """
        Cria partículas de grama (folhas) em uma posição específica.

        Args:
            pos (tuple): Posição onde as partículas serão criadas.
            groups (pygame.sprite.Group): Grupo de sprites onde as partículas serão adicionadas.
        """
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups):
        """
        Cria partículas de efeito em uma posição específica.

        Args:
            animation_type (str): Tipo de animação de partículas a ser criada.
            pos (tuple): Posição onde as partículas serão criadas.
            groups (pygame.sprite.Group): Grupo de sprites onde as partículas serão adicionadas.
        """
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        """
        Método para animar as partículas.

        Verifica se deve passar para o próximo frame da animação ou destruir a partícula se
        alcançar o último frame.
        """
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()  # Remove a partícula do grupo quando a animação termina
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        """
        Método update padrão do pygame para atualizar a animação da partícula.
        """
        self.animate()
