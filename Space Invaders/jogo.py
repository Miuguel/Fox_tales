from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import * 
from PPlay.animation import *
import gc
from menu import menu_loop
from alien import Alien
import time
from gameover import Gameover

# As dificuldades são:
# Easy = 0
# Medium = 1
# Hard = 2

dificuldade = menu_loop(0)  # O menu retorna a dificuldade escolhida pelo jogador

jogoJ = Window(1280, 720)  # Inicializa a janela do jogo
teclado = Window.get_keyboard()  # Inicializa o teclado
jogoJ.set_title("SPACE INVADERS")  # Define o título da janela
jogoJ.set_background_color((0,0,0))  # Define a cor de fundo da janela

nave = Sprite("nave.png", 1)  # Cria o sprite da nave
nave.set_position(jogoJ.width / 2 - nave.width / 2, jogoJ.height - nave.height - 20)  # Posiciona a nave

animacao_dano = Animation('naveA.png', 3)  # Cria a animação de dano
animacao_dano.set_sequence_time(0, 2, 200, loop=True)  # Define o tempo da sequência de animação

velx = 250 - (10 * dificuldade)  # Define a velocidade horizontal da nave, ajustada pela dificuldade
vely = 200  # Define a velocidade vertical dos tiros
listaT = []  # Lista para armazenar os tiros da nave
timer = 0  # Timer para controlar o intervalo entre os tiros
fundo = GameImage("esp.jpg")  # Imagem de fundo do jogo

aliens = Alien(3, 5)  # Inicializa os aliens (3 linhas, 5 colunas)
fps = 0  # Inicializa o contador de FPS
pontos = 0  # Inicializa a pontuação do jogador
ani_tempo_inicio = 0  # Tempo de início da animação de dano
vidas = 3  # Define o número de vidas do jogador
timer_tiro = 1  # Timer para controlar o intervalo entre os tiros dos aliens
ani_de_dano = False  # Flag para controlar a animação de dano

auxN = Sprite('nave.png', 1)  # Sprite auxiliar para reposicionar a nave após o dano
auxN.set_position(jogoJ.width / 2 - nave.width / 2, jogoJ.height - nave.height - 20)  # Posiciona o sprite auxiliar

gameover = False  # Flag para controlar o estado de game over
timing = 100  # Intervalo para os tiros dos aliens
entradaUsuario = False  # Flag para controlar a entrada do nome do jogador
jaColocouNome = False  # Flag para controlar se o nome do jogador já foi inserido

escudo = Sprite("escudo.png", 1)  # Cria os sprites dos escudos
escudo2 = Sprite("escudo.png", 1)
escudo3 = Sprite("escudo.png", 1)
escudo.set_position(100, 500)  # Posiciona os escudos
escudo2.set_position(600, 500)
escudo3.set_position(1100, 500)

hpescudo = 3  # Define a vida dos escudos
hpescudo2 = 3
hpescudo3 = 3

def iniciar_animacao_dano():
    """Inicia a animação de dano na nave"""
    global ani_de_dano, ani_tempo_inicio
    ani_de_dano = True
    ani_tempo_inicio = time.time()
    animacao_dano.set_position(jogoJ.width / 2 - animacao_dano.width / 2, jogoJ.height - animacao_dano.height - 20)

while True:

    if teclado.key_pressed('esc'):
        dificuldade = menu_loop(dificuldade)  # Volta para o menu se a tecla ESC for pressionada
    jogoJ.set_background_color((0, 0, 0))
    fundo.draw()

    delta = jogoJ.delta_time()  # Calcula o tempo desde o último frame
    if delta != 0:
        fps = 1 // jogoJ.delta_time()  # Calcula os FPS

    texto = jogoJ.draw_text(str(fps), 70, 15, size=15, color=(100, 200, 100), font_name="Arial", bold=False, italic=False)

    aliens.tirosA(timing)  # Chama a função de tiro dos aliens
    timer_tiro -= jogoJ.delta_time()
    escudo.draw()
    escudo2.draw()
    escudo3.draw()

    aliens.tirosA(timer_tiro)  # Chama a função de tiro dos aliens novamente

    if teclado.key_pressed("SPACE") and timer == 0:
        tiro = Sprite("tiro.png", 1)  # Cria um novo tiro
        tiro.set_position(nave.x + nave.width / 2 - tiro.width / 2, nave.y - 10)  # Posiciona o tiro
        listaT.append(tiro)  # Adiciona o tiro à lista de tiros
        timer = 30 - (10 * dificuldade)  # Reinicia o timer dos tiros

    for tiro in listaT:
        tiro.draw()  # Desenha o tiro
        if tiro.y > 0:
            tiro.y = tiro.y + vely * jogoJ.delta_time() * -1
        else:
            tiro.y = tiro.y + vely * jogoJ.delta_time() * -1
        if tiro.y <= 0 or tiro.collided(escudo) or tiro.collided(escudo2) or tiro.collided(escudo3):
            listaT.remove(tiro)  # Remove o tiro da lista se colidir ou sair da tela
            del tiro
            gc.collect()

    if teclado.key_pressed("RIGHT") and nave.x + nave.width <= jogoJ.width:
        nave.x += velx * jogoJ.delta_time()  # Move a nave para a direita

    if teclado.key_pressed("LEFT") and nave.x >= 0:
        nave.x -= velx * jogoJ.delta_time()  # Move a nave para a esquerda

    terminou = aliens.atualiza_aliens(jogoJ, nave)  # Atualiza a posição dos aliens e verifica colisões
    terminou2 = aliens.acabou_jogo()  # Verifica se o jogo acabou
    pontos = aliens.pontuacao(listaT, pontos)  # Atualiza a pontuação

    textoP = jogoJ.draw_text('Pontos: ' + str(pontos), 550, 10, size=40, color=(100, 50, 200), font_name="Consola", bold=True, italic=False)

    aliens.desenha_aliens()  # Desenha os aliens
    aliens.desenha_tiro()  # Desenha os tiros dos aliens
    textoVida = jogoJ.draw_text('Vidas: ' + str(vidas), 850, 10, size=40, color=(100, 50, 200), font_name="Consola", bold=True, italic=False)

    colidiu = aliens.att_tiros_A(jogoJ, nave)  # Verifica colisão dos tiros dos aliens com a nave
    colidiu2 = aliens.att_tiros_A(jogoJ, escudo)  # Verifica colisão dos tiros dos aliens com o escudo
    colidiu3 = aliens.att_tiros_A(jogoJ, escudo2)
    colidiu4 = aliens.att_tiros_A(jogoJ, escudo3)
    if colidiu2:
        hpescudo -= 1  # Reduz a vida do escudo se colidir
    if colidiu3:
        hpescudo2 -= 1
    if colidiu4:
        hpescudo3 -= 1
    if not ani_de_dano:

        if colidiu:
            vidas -= 1  # Reduz as vidas se colidir com a nave
            if vidas > 0:
                iniciar_animacao_dano()

    if ani_de_dano:
        tempo_decorrido = time.time() - ani_tempo_inicio
        if tempo_decorrido >= 2:
            ani_de_dano = False  # Para a animação de dano após 2 segundos
            nave = auxN
            nave.set_position(jogoJ.width / 2 - nave.width / 2, jogoJ.height - nave.height - 20)
        else:
            animacao_dano.draw()  # Desenha a animação de dano
            animacao_dano.update()
    else:
        nave.draw()  # Desenha a nave

    if timer_tiro <= 0:
        timer_tiro = 1
    if teclado.key_pressed("ESC"):
        break
    if timer > 0:
        timer -= 1
    if terminou:
        break
    if vidas <= 0:
        gameover = True
    if gameover:

        jogoJ.set_background_color((0, 0, 0))

        texto = jogoJ.draw_text("GAME OVER", jogoJ.width / 2 - 200, 15, size=100, color=(200, 0, 0),
                                font_name="Consola", bold=False,
                                italic=False)

        if entradaUsuario and not jaColocouNome:

            nome = input(print("Insira seu nome: "))

            with open("highscore.txt", 'a') as file:
                file.write(f'{nome}: {pontos} \n')
            
            entradaUsuario = False
            jaColocouNome = True

        entradaUsuario = True

        if entradaUsuario and jaColocouNome:
            break

    aliens.proxima_fase()  # Vai para a próxima fase se todos os aliens forem derrotados
    jogoJ.update()  # Atualiza a tela do jogo
