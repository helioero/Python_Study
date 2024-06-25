"""
  此处代码用于实现关于卡牌的相关方法
"""
import time
from random import randrange, choice


class CardMethod:

    # 初始化

    # 生成对应用户的牌
    def post_cards(self, user_count):

        user_card_list = []
        card_index = [i for i in range(52)]
        # 初始化用户的列表
        for i in range(user_count):
            user_card_list.append([])
        # 按顺序发牌, 一次发一张
        for i in range(3):
            for u in range(user_count):
                index = choice(card_index)
                user_card_list[u].append(index)
                card_index.remove(index)
        return user_card_list

    # 打印输出并记录牌的花色
    def print_color_card(self, card):
        color_card = []
        for i in range(len(card)):

            index_card = []
            for j in range(len(card[i])):

                point = card[i][j]
                if point <= 13:
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
                elif point < 27:
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
                elif point < 40:
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

    def compute_card_point(self, card):
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

    def compute_winner_size(self, point_card, color_card):
        winner_list = []
        for i in range(len(point_card)):
            point_card[i].sort()
            point = point_card[i][0] + point_card[i][1] + point_card[i][2] * 10
            winner_list.append(point)
            # 判断 3 个数 点数是否相同
            if point_card[i].count(point_card[i][0]) == 3:
                winner_list[i] += 10000
            # 判断 3 个数 点数是否为顺子
            elif point_card[i][0] + 1 == point_card[i][1] and point_card[i][1] + 1 == point_card[i][2]:
                winner_list[i] += 3000
                # 判断 3 个数 花色是否相同
                if color_card[i].count(color_card[i][0]) == 3:
                    winner_list[i] += 3000
            elif point_card[i][0] == 2 and point_card[i][1] == 3 and point_card[i][2] == 14:
                winner_list[i] += 3000
                # 判断 3 个数 花色是否相同
                if color_card[i].count(color_card[i][0]) == 3:
                    winner_list[i] += 3000
            # 判断 3 个数 其中 2 个点数相同
            elif point_card[i].count(point_card[i][0]) == 2:
                winner_list[i] += point_card[i][0] * 200
            elif point_card[i].count(point_card[i][1]) == 2:
                winner_list[i] += point_card[i][1] * 200
            # 判断 3个数 花色是否相同
            elif color_card[i].count(color_card[i][0]) == 3:
                winner_list[i] += 3000

        return winner_list

    # 生成用户信息字典列表
    def generate_user_info_dict_list(self, user_count, user_init_chips):
        user_info_dict_list = {}
        for i in range(user_count):
            dict_v = {'view': False, 'drop': False, 'disuse': False, 'color_card': [], 'size_card': 0,
                      'name': '000' + str(i), 'chips': user_init_chips}
            user_info_dict_list[i] = dict_v

        user_info_dict_list["unchecked_count"] = 0
        user_info_dict_list["not_folded_count"] = user_count
        user_info_dict_list["not_folded_list"] = []
        user_info_dict_list["valid_user"] = user_count
        return user_info_dict_list

    # 加载进度条
    def loading_card(self):
        scale = 50
        print("正在洗牌中, 5 秒后开始...".center(scale // 2, "-"))
        start = time.perf_counter()
        for i in range(scale + 1):
            a = "#" * i
            b = "." * (scale - i)
            c = (i / scale) * 100
            dur = time.perf_counter() - start
            print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, dur), end="")
            time.sleep(0.1)

        print("\n" + "洗牌完成".center(scale // 2, "-"))
