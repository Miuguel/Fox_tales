from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import *
from PPlay.animation import *
import gc
import random

class Alien:

    def __init__(self, linha, coluna, alien_image="alienrosa.png"):
        self.matrizAl = []  # Matriz para armazenar os aliens
        self.posicao_x = 0  # Posição inicial dos aliens no eixo x
        self.posicao_y = 0  # Posição inicial dos aliens no eixo y
        self.velx = 200  # Velocidade dos aliens no eixo x
        self.vely = 200  # Velocidade dos tiros dos aliens no eixo y
        self.lista_tir_A = []  # Lista para armazenar os tiros dos aliens
        self.alien_image = alien_image  # Imagem dos aliens
        self.altura = Sprite(alien_image).height  # Altura do sprite do alien
        self.largura = Sprite(alien_image).width  # Largura do sprite do alien
        self.cria_aliens(linha, coluna)  # Cria os aliens

    def cria_aliens(self, linha, coluna):
        """Cria uma matriz de aliens com o número de linhas e colunas especificado"""
        self.posicao_x = 0
        self.posicao_y = 0
        for i in range(linha):
            nova_linha = []
            for j in range(coluna):
                novo_al = Sprite(self.alien_image)
                novo_al.set_position(self.posicao_x, self.posicao_y)
                nova_linha.append(novo_al)
                self.posicao_x += novo_al.width
            self.matrizAl.append(nova_linha)
            self.posicao_y += self.altura
            self.posicao_x = 0

    def desenha_aliens(self):
        """Desenha todos os aliens na tela"""
        for linha in self.matrizAl:
            for alien in linha:
                alien.draw()

    def atualiza_aliens(self, jogoJ, nave):
        """Atualiza a posição dos aliens e verifica colisões com a nave"""
        pontos = 0
        atingiu = False
        move_down = False
        
        # Mover Aliens
        for linha in self.matrizAl:
            for alien in linha:
                deltax = self.velx * jogoJ.delta_time()
                alien.x += deltax

        # Verificar as bordas para todos os aliens
        for linha in self.matrizAl:
            for alien in linha:
                if alien.x + alien.width >= jogoJ.width or alien.x <= 0:
                    move_down = True
                if alien.collided(nave):
                    atingiu = True
                    
        if move_down:
            self.velx = -self.velx
            for linha in self.matrizAl:
                for alien in linha:
                    alien.x -= deltax
                    alien.y += 15

        return atingiu

    def tirosA(self, timer):
        """Cria um tiro aleatório de um alien se o timer permitir"""
        if timer <= 0:
            tiro = 'tiroalien.jpg'
            tr = Sprite(tiro)

            # Escolher aleatoriamente um alien para atirar
            aliens_disponiveis = [(i, j) for i in range(len(self.matrizAl)) for j in range(len(self.matrizAl[i]))]
            if aliens_disponiveis:
                randomL, randomC = random.choice(aliens_disponiveis)

                AlienAl = self.matrizAl[randomL][randomC]

                tr.x = AlienAl.x + AlienAl.width / 2 - tr.width / 2
                tr.y = AlienAl.y
                self.lista_tir_A.append(tr)

    def desenha_tiro(self):
        """Desenha os tiros dos aliens na tela"""
        for tiro in self.lista_tir_A:
            tiro.draw()

    def att_tiros_A(self, jogoJ, nave):
        """Atualiza a posição dos tiros dos aliens e verifica colisão com a nave"""
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

    def colidiu_esc(self, escudo):
        """Verifica colisão dos tiros dos aliens com os escudos"""
        colidiu = False

        for tiro in self.lista_tir_A:
            if tiro.collided(escudo):
                colidiu = True
                self.lista_tir_A.remove(tiro)
                del tiro
                gc.collect()

        return colidiu

    def acabou_jogo(self):
        """Verifica se algum alien alcançou a parte inferior da tela"""
        atingiu = False
        for linha in self.matrizAl:
            for alien in linha:
                if alien.y >= 500:
                    atingiu = True
        return atingiu

    def pontuacao(self, listaT, pontos):
        """Atualiza a pontuação do jogador ao destruir aliens"""
        aliens_removidos = []
        total_linhas = len(self.matrizAl)
        for y, linha in enumerate(self.matrizAl):
            for alien in linha:
                for tiro in listaT:
                    if tiro.y >= alien.y and alien.x < tiro.x < alien.x + alien.width:
                        if alien.collided(tiro):
                            pontos += 10 + (total_linhas - y - 1) * 10
                            listaT.remove(tiro)
                            aliens_removidos.append((linha, alien))

        for linha, alien in aliens_removidos:
            if alien in linha:
                linha.remove(alien)
        return pontos

    def proxima_fase(self):
        """Vai para a próxima fase do jogo aumentando a velocidade dos aliens"""
        reset = False
        if not any(self.matrizAl):
            reset = True
            self.velx += 100
            self.cria_aliens(3,5)
            return reset
        else:
            return reset