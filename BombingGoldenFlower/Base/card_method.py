"""
  此处代码用于实现关于卡牌的相关方法
"""
import time
from random import choice, shuffle, randint


class CardMethod:

    @staticmethod
    def post_cards(user_count):
        """ 生成对应用户的牌 """
        user_card_list = []
        card_index = [i for i in range(1, 53)]
        # 洗牌
        shuffle(card_index)
        # 初始化用户的列表
        for i in range(user_count):
            user_card_list.append([])
        # 按顺序发牌, 一次发一张, 每人发 3 张
        for i in range(3):
            for u in range(user_count):
                index = choice(card_index)
                user_card_list[u].append(index)
                card_index.remove(index)

        return user_card_list

    @staticmethod
    def print_color_card(card):
        """ 计算牌的分数以及牌的花色 """
        color_card = []
        for i in range(len(card)):

            index_card = []
            for j in range(len(card[i])):

                point = card[i][j]
                if 1 <= point <= 13:
                    if point == 1:
                        card_str = "♠️" + "A"
                    elif point == 11:
                        card_str = "♠️" + "J"
                    elif point == 12:
                        card_str = "♠️" + "Q"
                    elif point == 13:
                        card_str = "♠️" + "K"
                    else:
                        card_str = "♠️" + str(point)
                elif 14 <= point <= 26:
                    point -= 13
                    if point == 1:
                        card_str = "♥️" + "A"
                    elif point == 11:
                        card_str = "♥️" + "J"
                    elif point == 12:
                        card_str = "♥️" + "Q"
                    elif point == 13:
                        card_str = "♥️" + "K"
                    else:
                        card_str = "♥️" + str(point)
                elif 27 <= point <= 39:
                    point -= 13 * 2
                    if point == 1:
                        card_str = "♣️" + "A"
                    elif point == 11:
                        card_str = "♣️" + "J"
                    elif point == 12:
                        card_str = "♣️" + "Q"
                    elif point == 13:
                        card_str = "♣️" + "K"
                    else:
                        card_str = "♣️" + str(point)
                else:
                    point -= 13 * 3
                    if point == 1:
                        card_str = "♦️" + "A"
                    elif point == 11:
                        card_str = "♦️" + "J"
                    elif point == 12:
                        card_str = "♦️" + "Q"
                    elif point == 13:
                        card_str = "♦️" + "K"
                    else:
                        card_str = "♦️" + str(point)

                index_card.append(card_str)

            color_card.append(index_card)

        return color_card

    @staticmethod
    def compute_card_point(card):
        """ 计算牌面点数大小 """
        color_card = []
        point_card = []

        for i in range(len(card)):
            index_point_card = []
            index_color_card = []
            for j in range(len(card[i])):
                point = card[i][j]
                if point <= 13:
                    color_type = 1
                    if point == 1:
                        point = 14
                elif point < 27:
                    color_type = 2
                    point -= 13
                    if point == 1:
                        point = 14
                elif point < 40:
                    color_type = 3
                    point -= 13 * 2
                    if point == 1:
                        point = 14
                else:
                    color_type = 4
                    point -= 13 * 3
                    if point == 1:
                        point = 14

                index_color_card.append(color_type)
                index_point_card.append(point)
            point_card.append(index_point_card)
            color_card.append(index_color_card)

        return point_card, color_card

    @staticmethod
    def compute_winner_size(point_card, color_card):
        """ 计算牌面积分大小 """
        winner_list = []
        for i in range(len(point_card)):
            point_card[i].sort()
            point = point_card[i][0] + point_card[i][1] + point_card[i][2] * 10
            winner_list.append(point)
            # 判断 3 个数 点数是否相同
            if point_card[i].count(point_card[i][0]) == 3:
                winner_list[i] *= 100000
            # 判断是否是 同花顺
            elif color_card[i].count(color_card[i][0]) == 3 and point_card[i][0] + 1 == point_card[i][1] and \
                    point_card[i][1] + 1 == point_card[i][2]:
                winner_list[i] *= 10000
            # 判断是否是 同花
            elif color_card[i].count(color_card[i][0]) == 3:
                winner_list[i] *= 1000
            # 判断是否为 顺子
            elif point_card[i][0] + 1 == point_card[i][1] and point_card[i][1] + 1 == point_card[i][2]:
                winner_list[i] *= 100
            # 判断 123 顺子
            elif point_card[i][0] == 2 and point_card[i][1] == 3 and point_card[i][2] == 14:
                winner_list[i] = 33 * 100
                # 判断是否是 同花顺
                if color_card[i].count(color_card[i][0]) == 3:
                    winner_list[i] = 33 * 1000
            # 判断 3 个数是否是对子
            elif point_card[i].count(point_card[i][0]) == 2 or point_card[i].count(point_card[i][1]) == 2:
                winner_list[i] *= 10

        return winner_list

    @staticmethod
    def round_init_pool_user_info_dict(username_list, info, chips_pool, low_chips):
        # 状态初始化
        for item in username_list:
            if not info[item]['disuse']:
                # 扣除底注 10
                if info[item]['chips'] >= low_chips:
                    info[item]['view'] = False
                    info[item]['drop'] = False
                    info[item]['win'] = False
                    info[item]['chips'] -= low_chips
                    chips_pool += low_chips
                else:
                    # 玩家筹码不足，淘汰
                    print(f"玩家 {item} 剩余筹码 {info[item]['chips']} ，筹码不足，请充值或退出")
                    info[item]['disuse'] = True
                    info['valid_user'] -= 1
                    info['username_list'].remove(item)

        info['unchecked_count'] = info['valid_user']
        info['checked_count'] = 0
        info['not_drop_card_count'] = info['valid_user']
        info['not_folded_list'] = []
        return chips_pool, low_chips

    @staticmethod
    def generate_user_info(user_count, user_init_chips):
        """ 生成用户信息字典列表 """
        user_info = {}
        username_list = []
        for i in range(user_count):
            username = str(randint(1000, 10000))
            dict_v = {'view': False, 'drop': False, 'disuse': False, 'win': False, 'color_card': [], 'size_card': 0,
                      'chips': user_init_chips}
            username_list.append(username)
            user_info[username] = dict_v

        user_info['valid_user'] = user_count
        user_info['unchecked_count'] = user_info['valid_user']
        user_info['checked_count'] = 0
        user_info['not_drop_card_count'] = user_info['valid_user']
        user_info['not_folded_list'] = []
        user_info['username_list'] = username_list

        return user_info

    @staticmethod
    def loading_card():
        """ 加载进度条 """
        scale = 30
        print("正在洗牌中, 3 秒后开始...".center(scale // 2, "-"))
        start = time.perf_counter()
        for i in range(scale + 1):
            a = "#" * i
            b = "." * (scale - i)
            c = (i / scale) * 100
            dur = time.perf_counter() - start
            print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, dur), end="")
            time.sleep(0.1)

        print("\n" + "洗牌完成".center(scale // 2, "-"))
