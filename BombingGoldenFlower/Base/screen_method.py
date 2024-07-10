"""
    使用 pygame 库实现用户操作页面
"""
import os
import pygame as pg


class Config:
    # 根目录
    rootdir = os.path.split(os.path.abspath(__file__))[0]
    # FPS
    FPS = 30
    # Game Windows size
    WINDOWS_SIZE = (1470, 826)
    # 标题
    TITLE = '炸金花'
    # 定义一些颜色
    BUTTON_COLOR = (255, 255, 255)
    BUTTON_TEXT_COLOR = (0, 0, 153)

    # 位置
    BUTTON_POSITION_DICT = {
        'checked': [(400, 525), (550, 525), (700, 525), (850, 525), (1000, 525)],
        'uncheck': [(350, 525), (500, 525), (650, 525), (800, 525), (950, 525), (1100, 525)],
        'chips': [(680, 350), (1200, 700)],
        'restart': [(40, 40)]
    }
    POKER_POSITION = [(490, 600), (690, 600), (890, 600)]
    # 按钮text
    BUTTON_TEXT_DIST = {
        'checked': ['跟 注', '50', '100', '全 压', '弃 牌'],
        'uncheck': ['看 牌', '跟 注', '50', '100', '全 压', '弃 牌'],
        'chips': ['筹码池:  ', '我的筹码:  '],
        'restart': ['重 开']
    }

    # 字体
    BUTTON_FONT_PATH = os.path.join(rootdir.replace('Base', ''), 'Resources/Font/WeiRuanYaHei.ttf')
    BUTTON_FONT_SIZE = 30
    # 背景图片
    BACKGROUND_PATH = os.path.join(rootdir.replace('Base', ''), 'Resources/Images/background.jpg')
    # Pocker background img
    POKER_BACKGROUND_PATH = os.path.join(rootdir.replace('Base', ''), 'Resources/Images/pokers/poker.png')
    POKER_IMG_PATH_DIR = os.path.join(rootdir.replace('Base', ''), 'Resources/Images/pokers/')
    POKER_CARD_SIZE = (105, 150)


class ScreenMethod:
    def __init__(self):
        self.cfg = Config
        pg.init()
        self.screen = pg.display.set_mode(self.cfg.WINDOWS_SIZE)
        pg.display.set_caption(self.cfg.TITLE)

    def load_poker_card_surface(self, number):
        point = number

        if 1 <= point <= 13:
            card_color = 1
        elif 14 <= point <= 26:
            point -= 13
            card_color = 2
        elif 27 <= point <= 39:
            point -= 13 * 2
            card_color = 3
        else:
            point -= 13 * 3
            card_color = 4

        item_convert = pg.image.load(
            self.cfg.POKER_IMG_PATH_DIR + str(point) + '_' + str(card_color) + '.jpg')
        return pg.transform.scale(item_convert, self.cfg.POKER_CARD_SIZE)

    def draw(self, surf, pos):
        self.screen.blit(surf, pos)

    @ staticmethod
    def check_rect_clicked(rect_type, pos):
        if rect_type.collidepoint(pos):
            return True

    def check_clicked(self, rect_list, pos, text):
        for idx, each in enumerate(rect_list):
            if self.check_rect_clicked(each, pos):
                print(self.cfg.BUTTON_TEXT_DIST[text][idx])
                return self.cfg.BUTTON_TEXT_DIST[text][idx]

    def get_rect_text(self, text):
        f = pg.font.Font(self.cfg.BUTTON_FONT_PATH, self.cfg.BUTTON_FONT_SIZE)
        text_rect = f.render(text, True, self.cfg.BUTTON_TEXT_COLOR, self.cfg.BUTTON_COLOR)
        return text_rect

    def get_rect_type(self, text, pos):
        text_render = self.get_rect_text(text)
        # 获得显示对象的rect 区域坐标
        text_rect = text_render.get_rect()
        # 设置显示对象居中
        text_rect.center = pos
        return text_rect

    def is_selected(self, username, select_text, info):
        match self.cfg.BUTTON_TEXT_DIST['checked'].index(select_text):
            case 0:
                info['chips_pool'] += info['low_chips']
                info[username]['chips'] -= info['low_chips']
            case 1:
                info['chips_pool'] += 50
                info[username]['chips'] -= 50
            case 2:
                info['chips_pool'] += 100
                info[username]['chips'] -= 100
            case 3:
                info['chips_pool'] += info['chips']
                info[username]['chips'] = 0
            case 4:
                info[username]['drop'] = True
            case _:
                return False
