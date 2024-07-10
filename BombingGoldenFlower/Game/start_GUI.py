"""
    调用 ScreenMethod 方法以图形化方式运行
"""
import sys
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

    def restart(self):
        self.__init__(self.user_count)
        self.start()

    def start(self):
        """ start game """

        # 初始化
        cfg = self.cfg
        # 背景图片
        background_convert = pg.image.load(cfg.BACKGROUND_PATH).convert()
        background = pg.transform.scale(background_convert, cfg.WINDOWS_SIZE)

        # poker img
        poker_convert = pg.image.load(cfg.POKER_BACKGROUND_PATH).convert()
        poker_background = pg.transform.scale(poker_convert, cfg.POKER_CARD_SIZE)

        # rect button list
        checked_rect_list = []
        uncheck_rect_list = []
        for idx, text in enumerate(cfg.BUTTON_TEXT_DIST['checked']):
            rect = self.get_rect_type(text, cfg.BUTTON_POSITION_DICT['checked'][idx])
            checked_rect_list.append(rect)
        for idx, text in enumerate(cfg.BUTTON_TEXT_DIST['uncheck']):
            rect = self.get_rect_type(text, cfg.BUTTON_POSITION_DICT['uncheck'][idx])
            uncheck_rect_list.append(rect)

        restart_rect = self.get_rect_type(cfg.BUTTON_TEXT_DIST['restart'][0], cfg.BUTTON_POSITION_DICT['restart'][0])

        while True:
            # 初始化
            # 筹码池以及用户牌面初始化
            self.round_init_pool_user_info_dict(self.info['username_list'], self.info,
                                                self.info['chips_pool'], self.info['low_chips'])

            # 如果 玩家 只剩一个，退出循环
            if self.info['valid_user'] == 1:
                print(f"{'*' * 80}")
                print(
                    f"{'*' * 2}/t/t游戏结束, 玩家 {self.info['not_folded_list'][0]} 是本次活动大赢家,\n"
                    f" 该玩家赢得筹码 {self.info[self.info['not_folded_list'][0]]['chips'] + 10}/t/t{'*' * 2}")
                print(f"{'*' * 80}")
                break

            # 初始化内部 while 循环变量
            last_follow_amount = 10

            for username in self.info['username_list']:

                while True:
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            pg.quit()
                            sys.exit()
                        elif event.type == pg.MOUSEBUTTONDOWN:
                            mouse_pos = pg.mouse.get_pos()
                            if self.check_rect_clicked(restart_rect, mouse_pos):
                                print('restart')
                                self.restart()
                                break
                            if self.info[username]['view']:
                                checked_button_is_select = self.check_clicked(checked_rect_list, mouse_pos, 'checked')
                                if not self.is_selected(username, checked_button_is_select, self.info):
                                    continue
                            else:
                                uncheck_button_is_select = self.check_clicked(uncheck_rect_list, mouse_pos, 'uncheck')
                                if not self.is_selected(username, uncheck_button_is_select, self.info):
                                    continue
                                if uncheck_button_is_select == cfg.BUTTON_TEXT_DIST['uncheck'][0]:
                                    self.info[username]['view'] = True

                    # 画出背景
                    self.draw(background, (0, 0))
                    # 画出筹码池
                    self.draw(self.get_rect_text(str(cfg.BUTTON_TEXT_DIST['chips'][0]) + str(self.info['chips_pool'])),
                              cfg.BUTTON_POSITION_DICT['chips'][0])
                    # 画出自己的筹码
                    self.draw(
                        self.get_rect_text(str(cfg.BUTTON_TEXT_DIST['chips'][1]) + str(self.info[username]['chips'])),
                        cfg.BUTTON_POSITION_DICT['chips'][1])
                    # 画出重开按钮
                    self.draw(self.get_rect_text(cfg.BUTTON_TEXT_DIST['restart'][0]), restart_rect)

                    # 判断什么时候显示什么按钮
                    if self.info[username]['view']:
                        # 画出看牌后的按钮
                        for idx, rect in enumerate(checked_rect_list):
                            self.draw(self.get_rect_text(cfg.BUTTON_TEXT_DIST['checked'][idx]), rect)
                        # 画出看牌后的牌面
                        for idx, point in enumerate(self.info[username]['init_card']):
                            self.draw(self.load_poker_card_surface(point), cfg.POKER_POSITION[idx])
                    else:
                        # 画出未看牌的按钮
                        for idx, rect in enumerate(uncheck_rect_list):
                            self.draw(self.get_rect_text(cfg.BUTTON_TEXT_DIST['uncheck'][idx]), rect)
                        # 画出未看牌的牌面
                        for i in range(3):
                            self.draw(poker_background, cfg.POKER_POSITION[i])

                    pg.display.flip()


g = GameGUI(3)
g.start()
