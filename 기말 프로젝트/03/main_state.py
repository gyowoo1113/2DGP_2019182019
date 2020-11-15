import gfw
import os.path
from pico2d import *
import gobj
from player import Player
from background import HorzScrollBackground
from platform import Platform
from jelly import Jelly
from boss import Boss
from life_gauge import Life
from score import Score
import random
import stage_gen
import result_state

# ''
canvas_width= 1120
canvas_height = 630

def build_world():
    gfw.world.init(['bg','platform','enemy','boss','item','player','ui','score'])
    Player.load_all_images()
    Jelly.load_all_images()

    center = get_canvas_width() // 2, get_canvas_height() // 2

    for n, speed in [(1,10), (2,100), (3,150)]:
        bg = HorzScrollBackground('map_bg/bg_%d.png' % n)
        bg.speed = speed
        gfw.world.add(gfw.layer.bg, bg)

    global player
    player = Player()
    gfw.world.add(gfw.layer.player, player)

    global font
    font = load_font(gobj.RES_DIR + 'font/CookieRun Regular.ttf', 30)

    global life
    life = Life()
    gfw.world.add(gfw.layer.ui, life)

    global score
    score = Score(canvas_width/2-30, canvas_height - 65)
    gfw.world.add(gfw.layer.score, score)

    stage_gen.load(gobj.res('stage_boss.txt'))

paused = False

def enter():
    build_world()

def update():
    if paused:
        return
    gfw.world.update()

    dx = -250 * gfw.delta_time

    for layer in range(gfw.layer.platform, gfw.layer.item + 1):
        for obj in gfw.world.objects_at(layer):
            obj.move(dx)

    check_items()
    check_obstacles()
    check_obsBoss()

    stage_gen.update(dx)

    call_obj()

def check_items():
    for item in gfw.world.objects_at(gfw.layer.item):
        if gobj.collides_box(player, item):
            gfw.world.remove(item)
            player.check(item)
            if gfw.world.count_at(gfw.layer.boss) > 0:
                boss.check(item)
            break

def check_obstacles():
    for enemy in gfw.world.objects_at(gfw.layer.enemy):
        if enemy.hit: continue
        if enemy.crash: continue
        if gobj.collides_box(player, enemy):
            if player.SUPER:
                if not player.mag == 1.0:
                    enemy.crash = True
                    score.display += 100
                    score.score +=100
            else:
                enemy.hit = True
                life.life -= enemy.power
                player.give_super()

def check_obsBoss():
    for boss in gfw.world.objects_at(gfw.layer.boss):
        if boss.hit: continue
        if gobj.collides_box(player, boss):
            if not boss.action in ['sleep','end'] :
                boss.hit = True
                life.life -= boss.power
                player.give_super()

def call_obj():
    for item in gfw.world.objects_at(gfw.layer.item):
        item.check_player()

    global boss
    if gfw.world.count_at(gfw.layer.boss) > 0:
        boss = gfw.world.object(gfw.layer.boss, 0)

def draw():
    gfw.world.draw()
    #gobj.draw_collision_box()

def handle_event(e):
    if e.type == SDL_QUIT:
        gfw.quit()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
        gfw.pop()
    elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_RETURN):
        gfw.push(result_state)
        print(score.score)
        result_state.add(score.score)
    elif e.key == SDLK_p:
        global paused
        paused = not paused

    if player.handle_event(e):
        return

def exit():
    pass
def pause():
    pass
def resume():
    pass
#    build_world()


if __name__ == '__main__':
    gfw.run_main()