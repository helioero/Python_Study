"""
    调用 ScreenMethod 方法以图形化方式运行
"""
import sys
from time import sleep
import pygame as pg

from BombingGoldenFlower.Base.card_method import CardMethod
from BombingGoldenFlower.Base.screen_method import ScreenMethod


class GameGUI(CardMethod, ScreenMethod):
    user_count = 0
    user_init_chips = 0
    user_info_dict_list = {}
    user_init_card_list = []
    user_color_card_list = []
    user_point_and_color_card_list = []
    user_size_card_list = []

    def __init__(self, user_count):
        ScreenMethod.__init__(self)
        """ 初始化 筹码"""

        self.user_init_chips = 1000
        self.user_count = int(user_count)
        if self.user_count > 17:
            print('此游戏最多17人玩')
            exit(1)
        self.user_info_dict_list = self.generate_user_info(self.user_count, self.user_init_chips)
        self.get_cards(self.user_count)
        # 将牌的花色以及大小写入字典
        for idx, items in enumerate(self.user_info_dict_list['username_list']):
            if not self.user_info_dict_list[items]['disuse']:
                self.user_info_dict_list[items]["color_card"] = self.user_color_card_list[idx]
                self.user_info_dict_list[items]["size_card"] = self.user_size_card_list[idx]

        print(self.user_color_card_list)
        print(self.user_size_card_list)

    def start(self):
        """ start game """
        # 初始化
        cfg = self.cfg
        screen = self.screen
        info = self.user_info_dict_list
        # 背景图片
        background_convert = pg.image.load(cfg.BACKGROUND_PATH).convert()
        background = pg.transform.scale(background_convert, cfg.WINDOWS_SIZE)

        # poker img
        poker_convert = pg.image.load(cfg.POKER_BACKGROUND_PATH).convert()
        poker_background = pg.transform.scale(poker_convert, cfg.POKER_CARD_SIZE)

        # list
        checked_rect = self.get_rect_group("checked")
        uncheck_rect = self.get_rect_group("uncheck")

        while True:
            # 初始化
            # 筹码池初始化
            self.round_init_pool_user_info_dict(info['username_list'], info, info['chips_pool'], info['low_chips'])

            # 如果 玩家 只剩一个，退出循环
            if info['valid_user'] == 1:
                print(f"{'*' * 80}")
                print(
                    f"{'*' * 2}/t/t游戏结束, 玩家 {info['not_folded_list'][0]} 是本次活动大赢家, 该玩家赢得筹码 {info[info['not_folded_list'][0]]['chips'] + 10}/t/t{'*' * 2}")
                print(f"{'*' * 80}")
                break

            # print()
            # # self.loading_card()
            # print()
            # print(f"{'-' * 50} 第 {round_count} 局开始 {'-' * 50}")
            # print(f"所有玩家扣除底注 {low_chips}")

            # 生成 当前已有玩家的牌
            self.get_cards(info['valid_user'])

            # 初始化内部 while 循环变量
            rounds_over = False
            internal_rounds = 1
            last_follow_amount = 10

            check_status = False
            uncheck_status = False
            verify_status = False

            for item in range(self.user_count):
                while True:

                    self.draw(background, (0, 0))
                    for event in pg.event.get():
                        if event.type == pg.QUIT:
                            pg.quit()
                            sys.exit()

                    if check_status:
                        # 画出看牌后的按钮
                        for idx, rect in enumerate(checked_rect):
                            self.draw(self.cfg.BUTTON_TEXT_DIST[idx], rect)
                        # 画出看牌后的牌面
                        for i in range(2):
                            self.draw(self.load_poker_card_surface(i), cfg.POKER_POSITION[i])
                    else:
                        # 画出未看牌的按钮
                        for idx, rect in enumerate(uncheck_rect):
                            self.draw(self.cfg.BUTTON_TEXT_DIST[idx], rect)
                        # 画出未看牌的牌面
                        for i in range(2):
                            self.draw(poker_background, cfg.POKER_POSITION[i])

                    pg.display.flip()

