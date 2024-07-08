"""
    使用 pygame 库实现用户操作页面
"""
import os
import sys
from time import sleep
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
        "checked": [(400, 525), (550, 525), (700, 525), (850, 525), (1000, 525)],
        "uncheck": [(350, 525), (500, 525), (650, 525), (800, 525), (950, 525), (1100, 525)]
    }
    POKER_POSITION = [(490, 600), (690, 600), (890, 600)]
    # 按钮text
    BUTTON_TEXT_DIST = {
        "checked": ['跟 注', '50', '100', '全 压', '弃 牌'],
        "uncheck": ['看 牌', '跟 注', '50', '100', '全 压', '弃 牌']
    }

    # 字体
    BUTTON_FONT_PATH = os.path.join(rootdir.replace('Base', ''), 'Resources/Font/WeiRuanYaHei.ttf')
    BUTTON_FONT_SIZE = 28
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
        if 1 <= number <= 13:
            card_point = number
            card_color = 1
            item_convert = pg.image.load(
                self.cfg.POKER_IMG_PATH_DIR + str(card_point) + '_' + str(card_color) + '.jpg')
        elif 14 <= number <= 26:
            card_point = number - 13
            card_color = 2
            item_convert = pg.image.load(
                self.cfg.POKER_IMG_PATH_DIR + str(card_point) + '_' + str(card_color) + '.jpg')
        elif 27 <= number <= 39:
            card_point = number - 26
            card_color = 1
            item_convert = pg.image.load(
                self.cfg.POKER_IMG_PATH_DIR + str(card_point) + '_' + str(card_color) + '.jpg')
        else:
            card_point = number - 39
            card_color = 1
            item_convert = pg.image.load(self.cfg.POKER_IMG_PATH_DIR + str(card_point) + '_' + str(card_color) + '.jpg')
        return pg.transform.scale(item_convert, self.cfg.POKER_CARD_SIZE)

    def draw(self, surf, pos):
        self.screen.blit(surf, pos)

    def check_clicked(self, pos):
        pass

    def get_rect_group(self, dict_text):
        f = pg.font.Font(self.cfg.BUTTON_FONT_PATH, self.cfg.BUTTON_FONT_SIZE)

        rect_group = []
        for idx, text in enumerate(self.cfg.BUTTON_TEXT_DIST[dict_text]):
            text_render = f.render(text, True, self.cfg.BUTTON_TEXT_COLOR, self.cfg.BUTTON_COLOR)
            # 获得显示对象的rect 区域坐标
            text_rect = text_render.get_rect()
            # 设置显示对象居中
            text_rect.center = self.cfg.BUTTON_POSITION_DICT[dict_text][idx]
            rect_group.append(text_rect)

        return rect_group

# f = pg.font.Font('BombingGoldenFlower/Resources/Font/WeiRuanYaHei.ttf', 28)
# # 生成文本信息, 消除字体锯齿，字体颜色，背景颜色, 颜色用RGB表示
# text = f.render("点 我", True, button_color, button_background)
# # 获得显示对象的rect 区域坐标
# textRect = text.get_rect()
# # 设置显示对象居中
# textRect.center = button_position
