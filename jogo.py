from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
import gc
from menu import menu_loop
from alien import Alien

# Inicializa o jogo
dificuldade = menu_loop(0)  # o menu retorna a dificuldade

jogoJ = Window(1280, 720)
teclado = Window.get_keyboard()
jogoJ.set_title("SPACE INVADERS")
jogoJ.set_background_color((0, 0, 0))
nave = Sprite("nave.png", 1)
nave.set_position(jogoJ.width / 2 - nave.width / 2, jogoJ.height - nave.height - 20)

# Configurações iniciais
velx = 200
vely = 200
listaT = []
timer = 0
fundo = GameImage("esp.jpg")
num_linhas = 3
num_colunas = 3
pontuacao = 0
vidas = 3
invulneravel = False
tempo_invulneravel = 2000  # Tempo de invulnerabilidade em milissegundos
temporizador_invulneravel = 0

# Cria os aliens
alien = Alien(timer)
alien.movimento(num_linhas, num_colunas, jogoJ, nave)  # Popula a matriz de aliens


def reset_fase():
    global pontuacao, invulneravel, temporizador_invulneravel, num_linhas, num_colunas
    alien.movimento(num_linhas, num_colunas, jogoJ, nave)
    pontuacao = 0
    invulneravel = False
    temporizador_invulneravel = 0


def reset_nave():
    global invulneravel, temporizador_invulneravel
    nave.set_position(jogoJ.width / 2 - nave.width / 2, jogoJ.height - nave.height - 20)
    invulneravel = True
    temporizador_invulneravel = 2000  # Tempo de invulnerabilidade em milissegundos


while True:
    # Voltar para o menu quando apertar ESC
    if teclado.key_pressed('esc'):
        dificuldade = menu_loop(dificuldade)  # Atualiza a dificuldade, se necessário

    jogoJ.set_background_color((0, 0, 0))
    fundo.draw()

    # Mover e desenhar os alienígenas
    alien.move_aliens(jogoJ)
    alien.draw_aliens()

    # Verificar se o tiro colide com algum alienígena
    for tiro in listaT[:]:
        tiro.draw()
        tiro.y -= vely * jogoJ.delta_time()
        if tiro.y <= 0:
            listaT.remove(tiro)
        else:
            for linha in alien.matrizAl:
                for al in linha:
                    if tiro.collided(al):
                        listaT.remove(tiro)
                        linha.remove(al)
                        pontuacao += 10
                        break

    # Desenhar os tiros dos aliens
    for tiroA in alien.lista_tir_A:
        tiroA.draw()

    # Controlar a nave
    if teclado.key_pressed("RIGHT") and nave.x + nave.width <= jogoJ.width:
        nave.x += velx * jogoJ.delta_time()
    if teclado.key_pressed("LEFT") and nave.x >= 0:
        nave.x -= velx * jogoJ.delta_time()

    # Verificar se a barra de espaço foi pressionada para disparar
    if teclado.key_pressed("SPACE") and timer == 0:
        tiro = Sprite("tiro.png", 1)
        tiro.set_position(nave.x + nave.width / 2 - tiro.width / 2, nave.y - 10)
        listaT.append(tiro)
        timer = 100  # Ajuste o tempo do temporizador conforme necessário

    # Atualizar os tiros dos aliens
    alien.tirosA(jogoJ)
    if alien.att_tiros_A(jogoJ, nave) and not invulneravel:
        vidas -= 1
        if vidas <= 0:
            dificuldade = menu_loop(dificuldade)
            vidas = 3
            reset_fase()
        else:
            reset_nave()

    # Piscar a nave se invulnerável
    if invulneravel:
        temporizador_invulneravel -= jogoJ.delta_time() * 1000
        if int(temporizador_invulneravel / 200) % 2 == 0:
            nave.draw()
        if temporizador_invulneravel <= 0:
            invulneravel = False
    else:
        nave.draw()

    # Verificar se algum alienígena atinge o final da tela e resetar a fase
    for linha in alien.matrizAl:
        for al in linha:
            if al.y >= jogoJ.height - al.height:
                reset_fase()
                break

    # Verificar se algum alienígena atinge a altura do jogador
    for linha in alien.matrizAl:
        for al in linha:
            if al.y >= nave.y:
                dificuldade = menu_loop(dificuldade)
                vidas = 3
                reset_fase()
                break

    # Desenhar a pontuação e vidas
    jogoJ.draw_text(f"Pontuação: {pontuacao}", 10, 10, size=24, color=(255, 255, 255))
    jogoJ.draw_text(f"Vidas: {vidas}", 10, 40, size=24, color=(255, 255, 255))

    if teclado.key_pressed("ESC"):
        break
    if timer > 0:
        timer -= 1

    jogoJ.update()
