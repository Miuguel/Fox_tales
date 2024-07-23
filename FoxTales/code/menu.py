import pygame
from pygame.locals import *
import os

class Menu:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 50)
        self.current_screen = 'main_menu'
        self.difficulty = 'easy'  # Valor padrão de dificuldade

        # Carregar imagens
        self.background = pygame.image.load(os.path.join('imgs', 'menu_background.png'))
        self.difficulty_background = pygame.image.load(os.path.join('imgs', 'difficulty_background.png'))
        
        # Definir botões
        self.buttons = {
            'start': pygame.Rect(50, 100, 200, 50),
            'difficulty': pygame.Rect(50, 200, 200, 50),
            'ranking': pygame.Rect(50, 300, 200, 50),
            'quit': pygame.Rect(50, 400, 200, 50)
        }
        
        self.difficulty_buttons = {
            'easy': pygame.Rect(50, 100, 200, 50),
            'medium': pygame.Rect(50, 200, 200, 50),
            'hard': pygame.Rect(50, 300, 200, 50)
        }

    def draw_text(self, text, font, surface, x, y):
        textobj = font.render(text, True, (255, 255, 255))
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def draw(self, surface):
        if self.current_screen == 'main_menu':
            surface.blit(self.background, (0, 0))
            self.draw_text('Start Game', self.small_font, surface, 150, 125)
            self.draw_text('Difficulty', self.small_font, surface, 150, 225)
            self.draw_text('Ranking', self.small_font, surface, 150, 325)
            self.draw_text('Quit', self.small_font, surface, 150, 425)
        elif self.current_screen == 'difficulty':
            surface.blit(self.difficulty_background, (0, 0))
            self.draw_text('Select Difficulty', self.font, surface, 400, 50)
            self.draw_text('Easy', self.small_font, surface, 150, 125)
            self.draw_text('Medium', self.small_font, surface, 150, 225)
            self.draw_text('Hard', self.small_font, surface, 150, 325)

    def handle_event(self, event):
        if self.current_screen == 'main_menu':
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.buttons['start'].collidepoint(mouse_pos):
                    return 'start'
                elif self.buttons['difficulty'].collidepoint(mouse_pos):
                    self.current_screen = 'difficulty'
                elif self.buttons['ranking'].collidepoint(mouse_pos):
                    return 'ranking'
                elif self.buttons['quit'].collidepoint(mouse_pos):
                    pygame.quit()
                    quit()
        elif self.current_screen == 'difficulty':
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.difficulty_buttons['easy'].collidepoint(mouse_pos):
                    self.difficulty = 'easy'
                    return 'start'
                elif self.difficulty_buttons['medium'].collidepoint(mouse_pos):
                    self.difficulty = 'medium'
                    return 'start'
                elif self.difficulty_buttons['hard'].collidepoint(mouse_pos):
                    self.difficulty = 'hard'
                    return 'start'
        elif self.current_screen == 'ranking':
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.current_screen = 'main_menu'
        return None
