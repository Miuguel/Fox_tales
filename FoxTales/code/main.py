import pygame
import sys
from settings import *
from level import Level
from menu import Menu  

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Foxtales')
        self.clock = pygame.time.Clock()

        self.menu = Menu()
        self.difficulty = self.menu.difficulty

        # A instância de Level é criada apenas quando o jogo começa
        self.level = None

        main_sound = pygame.mixer.Sound('../audio/main.ogg')
        main_sound.set_volume(0.5)
        main_sound.play(loops=-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                action = self.menu.handle_event(event)
                if action == 'start':
                    self.level = Level(self.menu.difficulty)
                    self.game_loop()
                elif action == 'ranking':
                    self.show_ranking()

            self.screen.fill((0, 0, 0))  # Cor de fundo preta
            self.menu.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

    def show_ranking(self):
        self.screen.fill((0, 0, 0))
        pygame.font.init()
        font = pygame.font.Font(None, 74)
        title = font.render('Ranking', True, (255, 255, 255))
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        try:
            with open("highscore.txt", 'r') as file:
                scores = file.readlines()
        except FileNotFoundError:
            scores = []

        scores = [s.strip().split(": ") for s in scores]
        scores = sorted(scores, key=lambda x: int(x[1]), reverse=True)

        y_pos = 150
        for i, (name, score) in enumerate(scores):
            score_text = f'{i + 1}. {name} - {score}'
            score_surface = font.render(score_text, True, (255, 255, 255))
            self.screen.blit(score_surface, (WIDTH // 2 - score_surface.get_width() // 2, y_pos))
            y_pos += 50

        pygame.display.update()
        pygame.time.wait(3000)  # Exibe o ranking por 3 segundos

if __name__ == '__main__':
    game = Game()
    game.run()
