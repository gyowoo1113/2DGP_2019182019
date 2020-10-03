import gfw
from pico2d import *
import game_state

def enter():
    global image
    image = load_image('../res/map_bg/title.png')

def update():
    pass

def draw():
    image.draw(800, 300)

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_SPACE):
        gfw.change(game_state)

def exit():
    global image
    del image

if __name__ == '__main__':
    gfw.run_main()
