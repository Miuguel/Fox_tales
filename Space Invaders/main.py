from PPlay.window import *
from PPlay.sprite import *
from PPlay.animation import *
from PPlay.collision import *
import dificuldade as df


dificuldade = [8,4,2,1]
score1 = 0
resolution_width = 1600
resolution_height = 900

janela = Window(resolution_width, resolution_height)
janela.set_title("Space Invaders")

teclado = Window.get_keyboard()


nave = Sprite("bola.png")
nave.x = (resolution_width / 2) - (nave.width / 2)
nave.y = (resolution_height / 2) - (nave.height / 2)
velx = 300
vely = 300
pad1 = Sprite('pad.png')
pad1.x = 0
pad1.y = (resolution_height / 2) - (pad1.height / 2)
pad2 = Sprite('pad.png')
pad2.x = resolution_width - pad2.width
pad2.y = (resolution_height / 2) - (pad2.height / 2)
IA = True


#menu.game_loop()
while True:
    janela.set_background_color((255, 255, 255))
    nave.x += velx * janela.delta_time()
    nave.y += vely * janela.delta_time()


    if teclado.key_pressed('LEFT') and nave.x >= 10:
        pad2.x -= 300 * janela.delta_time()
    if teclado.key_pressed('RIGHT') and nave.x + nave.height + 10 <= resolution_height:
        pad2.x += 300 * janela.delta_time()

    if teclado.key_pressed('A') and pad1.y >= 10:
        pad1.y -= 300 * janela.delta_time()
    if teclado.key_pressed('D') and pad1.y + pad1.height + 10 <= resolution_height:
        pad1.y += 300 * janela.delta_time()

    if mouse.is_button_pressed() and True:
        pass
    if nave.collided(pad2):
        velx = -1 * velx
        nave.x += -1
    if nave.collided(pad1):
        nave.x += 1
        velx *= -1

    #if clicou_dificuldade():
     #   df.game_loop()
    if teclado.key_pressed('ESC'):
        break
    nave.draw()
    pad1.draw()
    pad2.draw()
    janela.update()
