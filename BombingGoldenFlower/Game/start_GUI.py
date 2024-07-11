"""
    调用 ScreenMethod 方法以图形化方式运行
"""
import sys
from time import sleep
import pygame as pg

from BombingGoldenFlower.Base.card_method import CardMethod
from BombingGoldenFlower.Base.screen_method import ScreenMethod


class GameGUI(CardMethod, ScreenMethod):

    def __init__(self, user_count):
        """ init chips """
        # 调用 ScreenMethod 初始化方法
        ScreenMethod.__init__(self)
        self.user_init_chips = 1000
        self.user_count = int(user_count)
        if self.user_count > 17:
            print('此游戏最多17人玩')
            exit(1)
        self.info = self.generate_user_info(self.user_count, self.user_init_chips)

        self.select_status = False
        self.round_over = False
        cfg = self.cfg
        # 背景图片
        self.background_convert = pg.image.load(cfg.BACKGROUND_PATH).convert()
        self.background = pg.transform.scale(self.background_convert, cfg.WINDOWS_SIZE)

        # poker img
        self.poker_convert = pg.image.load(cfg.POKER_BACKGROUND_PATH).convert()
        self.poker_background = pg.transform.scale(self.poker_convert, cfg.POKER_CARD_SIZE)

        # rect button list
        self.operate_rect_list = []
        for idx, text in enumerate(cfg.BUTTON_TEXT_DIST['operate']):
            rect = self.get_rect_type(text, cfg.BUTTON_POSITION_DICT['operate'][idx])
            self.operate_rect_list.append(rect)

        self.restart_rect = self.get_rect_type(cfg.BUTTON_TEXT_DIST['restart'][0], cfg.BUTTON_POSITION_DICT['restart'][0])

    def draw_winner(self, username):
        # 画出谁赢
        pg.display.flip()
        self.draw(
            self.get_rect_text('玩家 ' + username + str(self.cfg.BUTTON_TEXT_DIST['winner'][0]) +
                               str(self.info['chips_pool'])), self.cfg.BUTTON_POSITION_DICT['winner'][0])
        pg.display.flip()
        sleep(3)

    def user_operate(self, username, select_status):

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()
                    # 点击重启
                    if self.check_rect_clicked(self.restart_rect, mouse_pos):
                        print('restart')
                        self.restart()
                        break
                    if not self.round_over and not self.info[username]['win'] and self.info[username]['view']:
                        operate_button_text = self.check_clicked(self.info, username, self.operate_rect_list,
                                                                 mouse_pos, 'operate')
                        if operate_button_text is None:
                            continue
                        if self.is_selected(username, operate_button_text, self.info, 'operate'):
                            select_status = True
                    elif not self.round_over and not self.info[username]['win'] and not self.info[username]['view']:
                        operate_button_text = self.check_clicked(self.info, username, self.operate_rect_list,
                                                                 mouse_pos, 'operate')
                        if operate_button_text is None:
                            continue
                        if self.is_selected(username, operate_button_text, self.info, 'operate'):
                            select_status = True

            # 画出背景
            self.draw(self.background, (0, 0))
            # 画出筹码池
            self.draw(self.get_rect_text(str(self.cfg.BUTTON_TEXT_DIST['chips'][0]) + str(self.info['chips_pool'])),
                      self.cfg.BUTTON_POSITION_DICT['chips'][0])
            # 画出自己的筹码
            self.draw(
                self.get_rect_text(str(self.cfg.BUTTON_TEXT_DIST['chips'][1]) + str(self.info[username]['chips'])),
                self.cfg.BUTTON_POSITION_DICT['chips'][1])
            # 画出重开按钮
            self.draw(self.get_rect_text(self.cfg.BUTTON_TEXT_DIST['restart'][0]), self.restart_rect)

            # 判断什么时候显示什么按钮
            # 已看牌
            if self.info[username]['view']:
                # 画出看牌后的按钮
                for idx, rect in enumerate(self.operate_rect_list):
                    if idx == 0:
                        continue
                    self.draw(self.get_rect_text(self.cfg.BUTTON_TEXT_DIST['operate'][idx]), rect)
                    # 画出开牌按钮
                    if len(self.info['not_drop_user_list']) == 2 and self.info['unchecked_count'] == 0 and idx == 6:
                        self.draw(self.get_rect_text(self.cfg.BUTTON_TEXT_DIST['operate'][6]), rect)
                    else:
                        continue

                # 画出看牌后的牌面
                for idx, point in enumerate(self.info[username]['init_card']):
                    self.draw(self.load_poker_card_surface(point), self.cfg.POKER_POSITION[idx])
            # 未看牌
            else:
                # 画出未看牌的按钮
                for idx, rect in enumerate(self.operate_rect_list):
                    if idx == 6:
                        break
                    self.draw(self.get_rect_text(self.cfg.BUTTON_TEXT_DIST['operate'][idx]), rect)
                # 画出未看牌的牌面
                for i in range(3):
                    self.draw(self.poker_background, self.cfg.POKER_POSITION[i])
            if self.round_over:
                break
            if select_status:
                break
            pg.display.flip()

    def restart(self):
        self.__init__(self.user_count)
        self.start()

    def start(self):
        """ start game """

        while True:
            # 初始化
            # 筹码池以及用户牌面初始化
            self.reinit_info(self.info['username_list'], self.info, self.info['chips_pool'], self.info['low_chips'])

            # 如果 玩家 只剩一个，退出循环
            if self.info['valid_user'] == 1:
                print(f"{'*' * 80}")
                print(
                    f"{'*' * 2}/t/t游戏结束, 玩家 {self.info['not_drop_user_list'][0]} 是本次活动大赢家,\n"
                    f" 该玩家赢得筹码 {self.info[self.info['not_drop_user_list'][0]]['chips'] + 10}/t/t{'*' * 2}")
                print(f"{'*' * 80}")
                break

            # 初始化内部 while 循环变量
            self.round_over = False
            while True:
                self.select_status = False
                for username in self.info['username_list']:
                    print(username)
                    if self.info[username]['drop']:
                        continue
                    if self.info[username]['all_in']:
                        continue

                    self.user_operate(username, self.select_status)

                    # 判断开牌时机
                    if self.info['not_drop_card_count'] == 2 and self.info['unchecked_count'] == 0:
                        if self.info['open_card']:
                            if self.info[self.info['not_drop_user_list'][0]]['size_card'] > \
                                    self.info[self.info['not_drop_user_list'][1]][
                                        'size_card']:
                                self.info[self.info['not_drop_user_list'][0]]['chips'] += self.info[
                                    'chips_pool']
                                self.info[self.info['not_drop_user_list'][0]]['win'] = True
                                self.draw_winner(self.info['not_drop_user_list'][0])
                            else:
                                self.info[self.info['not_drop_user_list'][1]]['chips'] += self.info[
                                    'chips_pool']
                                self.info[self.info['not_drop_user_list'][1]]['win'] = True
                                self.draw_winner(self.info['not_drop_user_list'][1])
                            self.round_over = True
                    elif self.info['not_drop_card_count'] == 1:
                        self.info[self.info['not_drop_user_list'][0]]['chips'] += self.info['chips_pool']
                        self.info[self.info['not_drop_user_list'][0]]['win'] = True
                        self.round_over = True
                        self.draw_winner(self.info['not_drop_user_list'][0])

                    if self.select_status:
                        continue
                    if self.round_over:
                        break
                if self.round_over:
                    break


g = GameGUI(3)
g.start()
