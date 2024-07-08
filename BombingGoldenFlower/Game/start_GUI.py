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
            pg.quit()
            sys.exit()
        self.user_info_dict_list = self.generate_user_info_dict_list(self.user_count, self.user_init_chips)

    def get_cards(self, users):
        """ 将用户的牌生成以并计算牌面大小 """

        self.user_init_card_list = self.post_cards(users)
        self.user_color_card_list = self.print_color_card(self.user_init_card_list)
        self.user_point_and_color_card_list = self.compute_card_point(self.user_init_card_list)
        self.user_size_card_list = self.compute_winner_size(self.user_point_and_color_card_list[0],
                                                            self.user_point_and_color_card_list[1])
        print(self.user_color_card_list)
        print(self.user_size_card_list)

    def start(self):
        """ start game """
        # 初始化
        cfg = self.cfg
        screen = self.screen
        # 背景图片
        background_convert = pg.image.load(cfg.BACKGROUND_PATH).convert()
        background = pg.transform.scale(background_convert, cfg.WINDOWS_SIZE)

        # poker img
        poker_convert = pg.image.load(cfg.POKER_BACKGROUND_PATH).convert()
        poker_background = pg.transform.scale(poker_convert, cfg.POKER_CARD_SIZE)

        # list
        checked_rect = self.get_rect_group("checked")
        uncheck_rect = self.get_rect_group("uncheck")
        check_status = False
        uncheck_status = False
        verify_status = False

        while True:
            # 初始化
            # 筹码池初始化
            chips_pool = 0
            low_chips = 10
            info = self.user_info_dict_list
            user_item = 0
            # 状态初始化
            for item in range(self.user_count):
                user_item = item
                if not info[item]['disuse']:
                    # 扣除底注 10
                    if info[item]['chips'] >= low_chips:
                        info[item]['view'] = False
                        info[item]['drop'] = False
                        info[item]['chips'] -= low_chips
                        chips_pool += low_chips
                    else:
                        # 玩家筹码不足，淘汰
                        print(f"玩家 {info[item]['name']} 剩余筹码 {info[item]['chips']} ，筹码不足，请充值或退出")
                        info[item]['disuse'] = True
                        info['valid_user'] -= 1

            info['unchecked_count'] = 0
            info['not_folded_count'] = info['valid_user']
            info['not_folded_list'] = []

            # 如果 玩家 只剩一个，退出循环
            if info['valid_user'] == 1:
                print(f"{'*' * 80}")
                print(
                    f"{'*' * 2}/t/t游戏结束, 玩家 {info[user_item]['name']} 是本次活动大赢家, 该玩家赢得筹码 {info[user_item]['chips'] + 10}/t/t{'*' * 2}")
                print(f"{'*' * 80}")
                break

            # 生成 当前已有玩家的牌
            self.get_cards(info['valid_user'])

            # 将牌的花色以及大小写入字典
            card_index = 0
            for items in range(self.user_count):
                if not info[items]['disuse']:
                    info[items]["color_card"] = self.user_color_card_list[card_index]
                    info[items]["size_card"] = self.user_size_card_list[card_index]
                    card_index += 1

            # 初始化内部 while 循环变量
            rounds_over = False
            internal_rounds = 1
            last_follow_amount = 10

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

