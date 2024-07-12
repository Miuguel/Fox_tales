import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        # Configuração geral
        pygame.init()  # Inicializa todos os módulos do Pygame
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))  # Cria a janela do jogo com as dimensões definidas
        pygame.display.set_caption('Foxtales')  # Define o título da janela do jogo
        self.clock = pygame.time.Clock()  # Cria um objeto de relógio para controlar o framerate

        self.level = Level()  # Cria uma instância da classe Level, que gerencia os elementos do nível

        # Som
        main_sound = pygame.mixer.Sound('../audio/main.ogg')  # Carrega o arquivo de som principal
        main_sound.set_volume(0.5)  # Define o volume do som principal
        main_sound.play(loops = -1)  # Reproduz o som principal em loop infinito

    def run(self):
        while True:  # Loop principal do jogo
            for event in pygame.event.get():  # Verifica eventos na fila de eventos
                if event.type == pygame.QUIT:  # Verifica se o evento de sair do jogo foi acionado
                    pygame.quit()  # Encerra o Pygame
                    sys.exit()  # Sai do programa
                if event.type == pygame.KEYDOWN:  # Verifica se uma tecla foi pressionada
                    if event.key == pygame.K_m:  # Verifica se a tecla 'M' foi pressionada
                        self.level.toggle_menu()  # Alterna o estado do menu no nível

            self.screen.fill(WATER_COLOR)  # Preenche a tela com a cor definida para a água
            self.level.run()  # Executa o método run do nível, que atualiza e desenha os elementos do nível
            pygame.display.update()  # Atualiza a tela com as mudanças feitas
            self.clock.tick(FPS)  # Controla o framerate do jogo

if __name__ == '__main__':
    game = Game()  # Cria uma instância do jogo
    game.run()  # Inicia o loop principal do jogo