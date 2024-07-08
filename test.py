import os
import sys
from time import sleep

import pygame as pg

# 使用pygame 前必须先初始化
pg.init()
# windows size
windows_size = (1470, 826)
# 设置主屏幕窗口大小
screen = pg.display.set_mode(windows_size)

# 设置标题，即游戏名称
pg.display.set_caption('Hello world')

# # 字体
# f = pg.font.Font(None, 50)
# # 生成文本信息, 消除字体锯齿，字体颜色，背景颜色, 颜色用RGB表示
# text = f.render("My first GUI app", True, (255, 0, 0), (0,0,0))
# # 获得显示对象的rect 区域坐标
# textRect = text.get_rect()
# # 设置显示对象居中
# textRect.center = (400, 400)
# # 将文本信息绘制到主屏幕 Screen 上
# screen.blit(text, textRect)

#
# screen.fill('white')
# # create 50 * 50 image
# face = pg.Surface((50,50), flags=pg.HWSURFACE)
# # 填充
# face.fill(color='pink')
#
# 根目录
rootdir = os.path.split(os.path.abspath(__file__))[0]

# 加载背景图片
background_img = pg.image.load('BombingGoldenFlower/Resources/Images/background.jpg').convert()
background = pg.transform.scale(background_img, windows_size)


image_surface = pg.image.load("BombingGoldenFlower/Resources/Images/pokers/poker.png").convert()
poker_back = pg.transform.scale(image_surface, (105, 150))
image_2 = pg.image.load("BombingGoldenFlower/Resources/Images/pokers/1_1.jpg").convert()
# 旋转 0 度，将图像缩小0.5倍
image_roto = pg.transform.scale(image_2, (105, 150))

# 设置按钮属性
button_size = (70, 40)
button_color = (255, 255, 255)
button_background = (255, 100, 100)
button_text = '点 我'
button_text_color = (0, 0, 153)
button_position = (350, 525)

button_image = pg.Surface(button_size,flags=pg.HWSURFACE)
button_image.fill(button_color)
button_text_image = pg.font.Font('BombingGoldenFlower/Resources/Font/WeiRuanYaHei.ttf', 28).render(button_text, True, button_text_color)

f = pg.font.Font('BombingGoldenFlower/Resources/Font/WeiRuanYaHei.ttf', 30)
# 生成文本信息, 消除字体锯齿，字体颜色，背景颜色, 颜色用RGB表示
text = f.render("点 我", True, button_color, button_background)
# 获得显示对象的rect 区域坐标
textRect = text.get_rect()
# 设置显示对象居中
textRect.center = button_position



check_status = False
uncheck_status = False
verify_status = False

# 固定代码， 实现点击 X 关闭退出的功能，所有 pygame 程序都会使用
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()

            if textRect.collidepoint(mouse_pos):
                print('点到了')

    #

    # load background
    screen.blit(background, (0, 0))

    # 将绘制的图像添加到主屏幕上，（100，100） 是位置坐标, 显示屏左上角是 0，0
    if check_status:
        screen.blit(text, textRect)
        # 默认盲注值
        # screen.blit(button_image, (400, 504))
        # screen.blit(button_text_image, (404, 504))
        # 50
        screen.blit(button_image, (550, 504))
        screen.blit(button_text_image, (554, 504))
        # 100
        screen.blit(button_image, (700, 504))
        screen.blit(button_text_image, (704, 504))
        # 点击一次 默认值+=20
        screen.blit(button_image, (850, 504))
        screen.blit(button_text_image, (854, 504))
        # 弃牌
        screen.blit(button_image, (1000, 504))
        screen.blit(button_text_image, (1004, 504))
    else:

        screen.blit(text, textRect)
        # 看牌
        # screen.blit(button_image, (300, 504))
        # screen.blit(button_text_image, (304, 504))
        # 默认盲注值
        screen.blit(button_image, (450, 504))
        screen.blit(button_text_image, (454, 504))
        # 50
        screen.blit(button_image, (600, 504))
        screen.blit(button_text_image, (604, 504))
        # 100
        screen.blit(button_image, (750, 504))
        screen.blit(button_text_image, (754, 504))
        # 点击一次 默认值+=20
        screen.blit(button_image, (900, 504))
        screen.blit(button_text_image, (904, 504))
        # 弃牌
        screen.blit(button_image, (1050, 504))
        screen.blit(button_text_image, (1054, 504))

    # 3张卡牌
    screen.blit(image_roto, (490, 600))
    screen.blit(poker_back, (690, 600))
    screen.blit(poker_back, (890, 600))





    # 更新屏幕内容
    pg.display.flip()
