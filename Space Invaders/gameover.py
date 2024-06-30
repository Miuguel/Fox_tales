from PPlay.window import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.mouse import*
from PPlay.animation import*
import gc
from menu import menu_loop
from alien import Alien
import time

class Gameover:
    def gm(self, pontos):

        teclado = Window.get_keyboard()
        gm_ovr = Window(1280, 720)

        gm_ovr.set_background_color((0,0,0))

        texto = gm_ovr.draw_text("GAME OVER", gm_ovr.width / 2 - 200, 15, size=100, color=(200, 0, 0),
                                 font_name="Consola", bold=False,
                                 italic=False)
        
        nome = input(print("Insira seu nome: "))

        with open("highscore.txt", 'a') as file:
            file.write(f'{nome}: {pontos} \n')

        while True:
            texto = gm_ovr.draw_text("GAME OVER", gm_ovr.width/2-200, 15, size=100, color=(200, 0,0), font_name="Consola", bold=False,
                                   italic=False)

            if teclado.key_pressed("ESC") or teclado.key_pressed("SPACE") or teclado.key_pressed("ENTER"):
                aux = menu_loop()
                break
            gm_ovr.update()
