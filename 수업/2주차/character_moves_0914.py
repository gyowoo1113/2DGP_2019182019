#import os
#os.chdir('C:/Users/LG/Desktop/플밍과제/2d겜플/res')
#os.getcwd()
#os.listdir()
from pico2d import *
open_canvas()
grass = load_image('../res/grass.png')
character = load_image('../res/character.png')

x=0
while (x<800):
    clear_canvas()
    grass.draw(400,30)
    character.draw(x,90)
    x=x+2
    update_canvas()
    delay(0.01)
    get_events()

close_canvas()
