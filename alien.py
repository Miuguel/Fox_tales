import pygame.time
from PPlay.sprite import *
import gc
import random

class Alien:
    def __init__(self, timer):
        self.timer = timer
        self.lista_tir_A = []
        self.velx = 200
        self.vely = 200
        self.matrizAl = []
        self.tempo_recarga = 2  # Tempo de recarga em segundos
        self.ultimo_tiro = 0

    def movimento(self, linha, coluna, jogoJ, nave):
        self.matrizAl = []  # Resetar a matriz de alienígenas
        posicao_x = jogoJ.width / 2 - ((coluna * 1.5 * Sprite("alienrosa.png").width) / 2)
        posicao_y = Sprite("alienrosa.png").height / 2
        alien = "alienrosa.png"
        aux = Sprite(alien)
        altura = aux.height
        largura = aux.width

        for i in range(linha):
            nova_linha = []
            for j in range(coluna):
                novo_al = Sprite(alien)
                novo_al.set_position(posicao_x, posicao_y)
                nova_linha.append(novo_al)
                posicao_x += largura * 1.5
            self.matrizAl.append(nova_linha)
            posicao_y += altura * 1.5
            posicao_x = jogoJ.width / 2 - ((coluna * 1.5 * largura) / 2)

    def draw_aliens(self):
        for line in self.matrizAl:
            for alien in line:
                alien.draw()

    def move_aliens(self, jogoJ):
        change_direction = False

        for line in self.matrizAl:
            for alien in line:
                alien.move_x(self.velx * jogoJ.delta_time())
                if alien.x <= 0 or alien.x + alien.width >= jogoJ.width:
                    change_direction = True

        if change_direction:
            self.velx *= -1
            for line in self.matrizAl:
                for alien in line:
                    alien.move_y(10)

    def tirosA(self, jogoJ):
        tempo_atual = pygame.time.get_ticks() / 1000
        if tempo_atual - self.ultimo_tiro > self.tempo_recarga:
            if self.timer <= 0 and any(self.matrizAl):
                tiro = 'tiroalien.png'
                tr = Sprite(tiro)

                while True:
                    randomL = random.randint(0, len(self.matrizAl) - 1)
                    if len(self.matrizAl[randomL]) > 0:
                        break

                randomC = random.randint(0, len(self.matrizAl[randomL]) - 1)
                AlienAl = self.matrizAl[randomL][randomC]

                tr.x = AlienAl.x + AlienAl.width / 2 - tr.width / 2
                tr.y = AlienAl.y
                self.lista_tir_A.append(tr)
                self.ultimo_tiro = tempo_atual
                self.tempo_recarga = random.uniform(1, 3)  # Escala aleatória

    def att_tiros_A(self, jogoJ, nave):
        colidiu = False

        for tiro in self.lista_tir_A:
            tiro.y += self.vely * jogoJ.delta_time()
            if tiro.collided(nave):
                colidiu = True
            if tiro.y > jogoJ.height:
                self.lista_tir_A.remove(tiro)
                del tiro
                gc.collect()

        return colidiu
