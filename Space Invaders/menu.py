from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.animation import *
from pathlib import Path

path = Path('imgs', 'menu')


class Menu:
    tela_atual = 'menu'
    menu_botoes = []  # fica todos os botoes da tela menu principal aqui
    menu_dificuldades_botoes = []  # fica todos os botoes da tela de dificuldade aqui

    dificuldade = 0

    def __init__(self):
        #iniciar os fundos
        self.fundo = GameImage(path.joinpath('fundo space.png'))
        self.fundo_dificuldade = GameImage(path.joinpath('fundo dificuldade.png'))

        #iniciar o planeta da primeira tela
        self.planeta = Animation(path.joinpath('planetacinza.png'), 50)
        self.planeta.set_sequence_time(0, 24, 200, True)

        #iniciar a estrela da primeira tela
        self.estrela = Animation(path.joinpath('estrela.png'), 50)
        self.estrela.set_sequence_time(0, 24, 200, True)

        #iniciar o titulo
        self.spaceinv_logo = Animation(path.joinpath('space invaders.png'), 1)

        #inicia os botes do menu principal e coloca na respectiva lista
        jogar = Botao(path.joinpath('play.png'), total_frames=2, pos=[43, 135], funcao='jogar')
        dificuldade = Botao(path.joinpath('difficulty.png'), total_frames=2, pos=[43, 271], funcao='dificuldade')
        ranking = Botao(path.joinpath('Ranking.png'), total_frames=2, pos=[43, 412], funcao='ranking')
        sair = Botao(path.joinpath('quit.png'), total_frames=2, pos=[43, 585], funcao='sair')

        self.menu_botoes = [jogar, dificuldade, ranking, sair]

        #inicia os botes do menu de dificuldade e coloca na respectiva lista
        easy = Botao(path.joinpath('Easy.png'), total_frames=3, pos=[516, 98], funcao=0)
        meduim = Botao(path.joinpath('Medium.png'), total_frames=3, pos=[458, 253], funcao=1)
        hard = Botao(path.joinpath('Hard.png'), total_frames=3, pos=[516, 417], funcao=2)
        self.menu_dificuldades_botoes = [easy, meduim, hard]

    #Redireciona para a tela certa
    def gerenciador(self, teclado, cursor, janela):
        '''Redireciona para a tela certa'''
        if self.tela_atual == 'menu':
            self.tela_principal(cursor)
        elif self.tela_atual == 'ranking':
            self.tela_ranking(teclado, janela)
        elif self.tela_atual == 'jogar':
            return self.tela_jogar(teclado, janela)
        elif self.tela_atual == 'dificuldade':
            self.tela_dificuldade(teclado, cursor)
        elif self.tela_atual == 'sair':
            janela.close()

    # comportamento da tela principal
    def tela_principal(self, cursor: Mouse):
        self.planeta.set_position(120 - self.planeta.width / 2, -30)
        self.estrela.set_position(530, -150)
        self.spaceinv_logo.set_position(670, 28)

        self.fundo.draw()

        self.planeta.draw()
        self.planeta.update()
        self.estrela.draw()
        self.estrela.update()
        self.spaceinv_logo.draw()

        # cada botao realiza sua funcao se clicado
        for item in self.menu_botoes:
            item.clica_ou_nao(cursor, self)
            item.draw()

    # vazia por enquanto, mas volta com o esc
    def tela_jogar(self, teclado: keyboard.Keyboard, janela):
        janela.set_background_color([0, 0, 0])
        if teclado.key_pressed('esc'):
            self.tela_atual = 'menu'
        return 'jogo'

    def tela_ranking(self, teclado: keyboard.Keyboard, janela):
        janela.set_background_color([0, 0, 0])
        texto = janela.draw_text("RANKING:", janela.width / 2 - 200, 15, size=100, color=(0, 100, 50),
                                 font_name="Consola", bold=False, italic=False)

        with open("highscore.txt", 'r') as file:
            scores = file.readlines()

        scores = [s.strip().split(": ") for s in scores]
        scores = sorted(scores, key=lambda x: int(x[1]), reverse=True)

        y_pos = 150  # Posicionamento inicial dos rankings
        for i, (nome, score) in enumerate(scores):
            janela.draw_text(f'{i + 1}. {nome} - {score}', janela.width / 2 - 100, y_pos, size=20,
                             color=(255, 255, 255),
                             font_name="Arial")
            y_pos += 30
        if teclado.key_pressed('esc'):
            self.tela_atual = 'menu'
        return 'jogo'

    def tela_dificuldade(self, teclado, cursor):
        self.fundo_dificuldade.draw()

        # cada botao realiza sua funcao se clicado
        for item in self.menu_dificuldades_botoes:
            item.clica_ou_nao(cursor, self)
            item.draw()

        if teclado.key_pressed('esc'):
            self.tela_atual = 'menu'


class Botao(Animation):
    def __init__(self, image_file, total_frames, pos: list, funcao, loop=True):
        super().__init__(image_file, total_frames, loop)
        self.pos = pos
        self.funcao = funcao
        self.set_position(pos[0], pos[1])

    def clica_ou_nao(self, cursor: mouse, menu: Menu):

        if menu.tela_atual == 'menu' or menu.tela_atual == 'ranking':
            if cursor.is_over_object(self):
                self.set_curr_frame(1)  # se o mouse fica em cima seleciona
                if cursor.is_button_pressed(cursor.BUTTON_LEFT):
                    menu.tela_atual = self.funcao
            else:
                self.set_curr_frame(0)

        ## NOTE uma possivel ideia pode ser ser fazer cada janela definir seu menu antes e aqui chamar diretamente a janela

        # se tiver na tela de dificuldade os botoes sao diferentes
        elif menu.tela_atual == 'dificuldade':
            if menu.dificuldade == self.funcao:
                self.set_curr_frame(2)  ##se tiver na dificuldade selecionada coloca o frame especial
            else:
                if cursor.is_over_object(self):
                    self.set_curr_frame(1)  # se o mouse fica em cima seleciona
                    if cursor.is_button_pressed(cursor.BUTTON_LEFT):
                        global dificuldade
                        dificuldade = self.funcao

                        menu.dificuldade = self.funcao
                else:
                    self.set_curr_frame(0)


def menu_loop(diff=0):
    janela = Window(1280, 720)
    janela.set_title("Space Invaders")
    cursor = Mouse()
    menu = Menu()
    menu.dificuldade = diff
    teclado = Window.get_keyboard()

    while True:
        if menu.gerenciador(teclado, cursor, janela) == 'jogo':
            return menu.dificuldade

        janela.update()
