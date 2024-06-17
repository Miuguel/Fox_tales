import pygame.time
from PPlay.sprite import Sprite
import gc
import random

class Alien:
    def __init__(self, timer):
        self.timer = timer
        self.lista_tir_A = []
        self.velx = 200
        self.vely = 200
        self.matrizAl = []
        self.direcao = 1  # Inicializa a direção dos aliens

    def movimento(self, linha, coluna, jogoJ, nave):
        self.matrizAl = []
        posicao_x = 0
        posicao_y = 0
        alien = "alienrosa.png"
        aux = Sprite(alien)
        altura = aux.height
        largura = aux.width
        espaco = largura / 2

        for i in range(linha):
            nova_linha = []
            for j in range(coluna):
                novo_al = Sprite(alien)
                novo_al.set_position(posicao_x, posicao_y)
                nova_linha.append(novo_al)
                posicao_x += largura + espaco
            self.matrizAl.append(nova_linha)
            posicao_y += altura + espaco
            posicao_x = 0

    def update_movimento(self, jogoJ):
        move_down = False
        for linha in self.matrizAl:
            for alien in linha:
                alien.x += self.velx * self.direcao * jogoJ.delta_time()
                if alien.x <= 0 or alien.x + alien.width >= jogoJ.width:
                    move_down = True

        if move_down:
            self.direcao *= -1
            for linha in self.matrizAl:
                for alien in linha:
                    alien.y += 10  # Ajuste a descida conforme necessário

    def tirosA(self):
        if self.timer <= 0:
            tiro = 'tiroalien.png'
            tr = Sprite(tiro)
            randomL = random.randint(0, len(self.matrizAl) - 1)
            randomC = random.randint(0, len(self.matrizAl[randomL]) - 1)
            AlienAl = self.matrizAl[randomL][randomC]
            tr.x = AlienAl.x + AlienAl.width / 2 - tr.width / 2
            tr.y = AlienAl.y
            self.lista_tir_A.append(tr)
            self.timer = random.randint(1, 3) * 1000  # Intervalo de recarga aleatório

    def att_tiros_A(self, jogoJ, nave):
        colidiu = False
        for tiro in self.lista_tir_A[:]:
            tiro.y += self.vely * jogoJ.delta_time()
            if tiro.collided(nave):
                colidiu = True
            if tiro.y > jogoJ.height:
                self.lista_tir_A.remove(tiro)
                del tiro
                gc.collect()
        return colidiu
