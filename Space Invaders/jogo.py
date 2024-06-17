from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import *
from menu import menu_loop
from alien import Alien
import gc
import random
import os

# Inicializa o ranking
if not os.path.exists("ranking.txt"):
    open("ranking.txt", "w").close()

# Configurações do jogo
dificuldade = menu_loop(0)  # o menu retorna a dificuldade
jogoJ = Window(1280, 720)
teclado = Window.get_keyboard()
jogoJ.set_title("SPACE INVADERS")
jogoJ.set_background_color((0, 0, 0))
nave = Sprite("nave.png", 1)
nave.set_position(jogoJ.width / 2 - nave.width / 2, jogoJ.height - nave.height - 20)
velx = 200
vely = 200
listaT = []
timer = 0
fundo = GameImage("esp.jpg")
linha = 5
col = 6
alien = Alien(timer)
alien.movimento(linha, col, jogoJ, nave)
pontuacao = 0
vidas = 3
invulneravel = False
temporizador_invulneravel = 0
tempo_para_proxima_linha = 2000  # Tempo em milissegundos para iniciar a próxima linha
temporizador_linha = 0

def reset_fase():
    global alien, pontuacao
    alien.movimento(linha, col, jogoJ, nave)
    pontuacao = 0

def reset_nave():
    global invulneravel, temporizador_invulneravel
    nave.set_position(jogoJ.width / 2 - nave.width / 2, jogoJ.height - nave.height - 20)
    invulneravel = True
    temporizador_invulneravel = 2000  # 2 segundos de invulnerabilidade

def verificar_fim_jogo():
    global vidas, pontuacao
    vidas -= 1
    if vidas <= 0:
        print("Game Over")
        print(f"Pontuação final: {pontuacao}")
        salvar_ranking(pontuacao)
        exit()
    else:
        reset_nave()

def salvar_ranking(pontuacao):
    nome = input("Digite seu nome: ")
    with open("ranking.txt", "a") as f:
        f.write(f"{nome},{pontuacao},{jogoJ.time_elapsed()}\n")

def verificar_proxima_fase():
    global linha, col, alien
    if not any(alien.matrizAl):  # Verifica se a matriz está vazia
        linha += 1
        col += 1
        alien.movimento(linha, col, jogoJ, nave)
        alien.velx *= 1.1  # Aumenta a velocidade dos aliens
        alien.vely *= 1.1

while True:
    # Voltar para o menu quando apertar ESC
    if teclado.key_pressed('ESC'):
        dificuldade = menu_loop(dificuldade)  # Atualiza a dificuldade, se necessário

    jogoJ.set_background_color((0, 0, 0))
    fundo.draw()

    # Desenhar os alienígenas
    for linha in alien.matrizAl:
        for al in linha:
            al.draw()

    # Atualizar movimento dos alienígenas
    alien.update_movimento(jogoJ)

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

    # Desenhar a nave
    if invulneravel:
        if int(jogoJ.time_elapsed() * 1000) % 200 < 100:  # Piscar a nave
            nave.draw()
        temporizador_invulneravel -= jogoJ.delta_time() * 1000
        if temporizador_invulneravel <= 0:
            invulneravel = False
    else:
        nave.draw()

    # Verificar se algum alienígena atinge o final da tela e resetar a fase
    for linha in alien.matrizAl:
        for al in linha:
            if al.y >= jogoJ.height - al.height:
                verificar_fim_jogo()
                break

    # Verificar se é hora de mudar de fase
    verificar_proxima_fase()

    # Desenhar a pontuação e vidas
    jogoJ.draw_text(f"Pontuação: {pontuacao}", 10, 10, size=24, color=(255, 255, 255))
    jogoJ.draw_text(f"Vidas: {vidas}", 10, 40, size=24, color=(255, 255, 255))

    if teclado.key_pressed("ESC"):
        break
    if timer > 0:
        timer -= 1

    jogoJ.update()
