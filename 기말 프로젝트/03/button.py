import gfw
from pico2d import *
from gobj import *

LBTN_DOWN = (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT)
LBTN_UP   = (SDL_MOUSEBUTTONUP,   SDL_BUTTON_LEFT)
NORMAL_BUTTON, COOKIE_BUTTON, X_BUTTON = range(3)

class BtnBg:
    def __init__(self, image):
        self.image = gfw.image.load(image)
        self.left = self.image.w // 2
        self.right = self.image.w - self.left - 1

    def draw(self, l, b, w, h):
        src_left = 0, 0, self.left, self.image.h
        dst_left = l, b, self.left, h
        self.image.clip_draw_to_origin(*src_left, *dst_left)

        center = w - self.left - self.right
        src_mid = self.left, 0, 1, self.image.h
        dst_mid = l + self.left, b, center, h
        self.image.clip_draw_to_origin(*src_mid, *dst_mid)

        src_right = self.image.w - self.right, 0, self.right, self.image.h
        dst_right = l + w - self.right, b, self.right, h
        self.image.clip_draw_to_origin(*src_right, *dst_right)

    btn_bg_cache = {}
    @staticmethod
    def get(choose,state):
        key = 'ui/button/btn' + '_' + str(choose) + str(state)
        if key in BtnBg.btn_bg_cache:
            return BtnBg.btn_bg_cache[key]

        file = 'ui/button/btn' + '_'+ choose + state + '.png'
        btn_bg = BtnBg(res(file))
        BtnBg.btn_bg_cache[key] = btn_bg
        return btn_bg

class Button:
    def __init__(self,state,l, b, w, h, font, text, callback, btnClass=None):
        self.l, self.b, self.w, self.h = l, b, w, h
        self.callback = callback
        self.set_text(font, text)
        self.t_x = self.l + (self.w - self.t_w) / 2
        self.t_y = self.b + self.h // 2
        self.mouse_point = None
        self.state = state
        self.bg = BtnBg.get(self.state,'normal')
        self.sound = load_wav(RES_DIR + 'sound/ui.wav')
        self.sound.set_volume(30)

    def set_text(self, font, text):
        self.text = text
        self.font = font
        self.t_w, self.t_h = get_text_extent(font, text)
        
    def draw(self):
        self.bg.draw(self.l, self.b, self.w, self.h)
        # self.font.draw(self.t_x, self.t_y, self.text)
        draw_centered_text(self.font, self.text, self.l, self.b, self.w, self.h)
        # draw_rectangle(self.l, self.b, self.l + self.w, self.b + self.h)

    def handle_event(self, e):
        pair = (e.type, e.button)
        if self.mouse_point is None:
            if pair == LBTN_DOWN:
                if pt_in_rect(mouse_xy(e), self.get_bb()):
                    self.mouse_point = mouse_xy(e)
                    self.backup = self.text
                    self.bg = BtnBg.get(self.state,'down')
                    self.sound.play()
                    return True
            if e.type == SDL_MOUSEMOTION:
                mpos = mouse_xy(e)
                in_rect = pt_in_rect(mpos, self.get_bb())
                if in_rect:
                    self.bg = BtnBg.get(self.state,'down')
                    return True
                else:
                    self.bg = BtnBg.get(self.state,'normal')
                    return False

            return False

        if pair == LBTN_UP:
            self.mouse_point = None
            self.text = self.backup
            mpos = mouse_xy(e)
            if pt_in_rect(mpos, self.get_bb()):
                self.callback()
            self.bg = BtnBg.get(self.state,'normal')
            return False

        if e.type == SDL_MOUSEMOTION:
            mpos = mouse_xy(e)
            in_rect = pt_in_rect(mpos, self.get_bb())
            if in_rect:
                self.bg = BtnBg.get(self.state,'down')
            else:
                self.bg = BtnBg.get(self.state,'down')

        return True

    def get_bb(self):
        return self.l, self.b, self.l + self.w, self.b + self.h

    def update(self):
        pass

    # def __del__(self):
    #     print('Del Button:', self)

def get_text_extent(font, text):
    w, h = c_int(), c_int()
    TTF_SizeText(font.font, text.encode('utf-8'), ctypes.byref(w), ctypes.byref(h))
    return w.value, h.value

def draw_centered_text(font, text, l, b, w, h):
    tw, th = get_text_extent(font, text)
    tx = l + (w - tw) // 2
    ty = b + h // 2
    font.draw(tx, ty, text)

class ReadyPlayer:
    def __init__(self,name,callback):
        self.char = name
        self.image = gfw.image.load(res('cookie/%s.png'%self.char))
        self.mouse_point = None
        self.callback = callback
        self.sound = load_wav(RES_DIR + 'sound/ui.wav')
        self.sound.set_volume(30)
    def draw(self):
        w = get_canvas_width()/2
        h = get_canvas_height()/2-70
        self.image.draw(w,h)
    def handle_event(self,e):
        pair = (e.type, e.button)
        if self.mouse_point is None:
            if pair == LBTN_DOWN:
                if pt_in_rect(mouse_xy(e), self.get_bb()):
                    self.mouse_point = mouse_xy(e)
                    self.sound.play()
                    return True
            if e.type == SDL_MOUSEMOTION:
                mpos = mouse_xy(e)
                in_rect = pt_in_rect(mpos, self.get_bb())
                if in_rect:
                    return True
                else:
                    return False

            return False

        if pair == LBTN_UP:
            self.mouse_point = None
            mpos = mouse_xy(e)
            if pt_in_rect(mpos, self.get_bb()):
                self.callback()
            return False

        if e.type == SDL_MOUSEMOTION:
            mpos = mouse_xy(e)
            in_rect = pt_in_rect(mpos, self.get_bb())

        return True

    def get_bb(self):
        w = get_canvas_width()/2
        h = get_canvas_height()/2-70

        return w-self.image.w/2,h-self.image.h/2,w+self.image.w/2,h+self.image.h/2

    def remove(self):
        gfw.world.remove(self)

    def update(self):
        pass
