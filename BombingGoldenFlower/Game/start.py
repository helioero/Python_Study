"""
    此文件用于实现游戏启动等相关方法
"""

from BombingGoldenFlower.Base.card_method import CardMethod


class Game(CardMethod):
    user_count = 0
    user_init_chips = 0
    user_info_dict_list = {}
    user_init_card_list = []
    user_color_card_list = []
    user_point_and_color_card_list = []
    user_size_card_list = []

    # 初始化 筹码
    def __init__(self, user_count):

        self.user_init_chips = 1000
        self.user_count = int(user_count)
        self.user_info_dict_list = self.generate_user_info_dict_list(self.user_count, self.user_init_chips)

    # 将用户的牌生成以并计算牌面大小
    def get_cards(self, users):

        self.user_init_card_list = self.post_cards(users)
        self.user_color_card_list = self.print_color_card(self.user_init_card_list)
        self.user_point_and_color_card_list = self.compute_card_point(self.user_init_card_list)
        self.user_size_card_list = self.compute_winner_size(self.user_point_and_color_card_list[0],
                                                            self.user_point_and_color_card_list[1])
        print(self.user_color_card_list)
        print(self.user_size_card_list)

    # 用户循环输入判断
    def user_input(self, head_amount, dict_item):

        while True:
            user_input_value = input(f"请输入下注的筹码，必须在区间({head_amount} - {self.user_info_dict_list[dict_item]['chips']}): ")
            if user_input_value == '':
                print("输入的值不为正整数，请重新输入")
                continue
            elif user_input_value.isdigit():
                if head_amount <= int(user_input_value) <= self.user_info_dict_list[dict_item]['chips']:
                    break
            else:
                print("输入的值不为正整数，请重新输入")
        return int(user_input_value)

    # 游戏运行主逻辑
    def start(self):

        print(f"{'-' * 50}")
        print("欢迎来到澳门新葡京娱乐城，这里正在进行名为 炸金花 的扑克牌牌局")
        print(f"本次牌局共有 {self.user_count} 名玩家参加，每名玩家初始筹码为 {self.user_init_chips} ,每轮底注为10")
        print("游戏马上开始，祝你玩的开心")
        # 局数初始化
        round_count = 1
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

            info['unchecked_count'] = info['valid_user']
            info['not_folded_count'] = info['valid_user']
            info['not_folded_list'] = []

            # 如果 玩家 只剩一个，退出循环
            if info['valid_user'] == 1:
                print(f"{'*' * 80}")
                print(
                    f"{'*' * 2}/t/t游戏结束, 玩家 {info[user_item]['name']} 是本次活动大赢家, 该玩家赢得筹码 {info[user_item]['chips'] + 10}/t/t{'*' * 2}")
                print(f"{'*' * 80}")
                break

            print()
            self.loading_card()
            print()
            print(f"{'-' * 50} 第 {round_count} 局开始 {'-' * 50}")
            print(f"所有玩家扣除底注 {low_chips}")

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

            while True:

                print(f"{'#' * 30} 第 {round_count} 局, 第 {internal_rounds} 回合 {'#' * 30}")
                for dict_i in range(self.user_count):

                    if info[dict_i]['disuse'] or info[dict_i]['drop']:
                        continue
                    print(
                        f"{'#' * 20} 本回合剩余玩家 {info['not_folded_count']}, {info['unchecked_count']} 位下盲注, {info['not_folded_count'] - info['unchecked_count']} 位跟注 {'#' * 20}")
                    print(f"{'-' * 30}> 玩家 {info[dict_i]['name']} 的回合")
                    # 其他玩家弃牌，只剩 1 名玩家时
                    if info['not_folded_count'] < 2 and not info[dict_i]['view']:
                        info[dict_i]['chips'] += chips_pool
                        print(f"{'*' * 50}")
                        print(
                            f"{'*' * 2}  玩家 {info[dict_i]['name']} 赢，赢得筹码 {chips_pool} 剩余 {info[dict_i]['chips']} 筹码  {'*' * 2}")
                        print(f"{'*' * 50}")
                        print(f"{'-' * 50} 第 {round_count} 局结束 {'-' * 50}")
                        rounds_over = True
                        round_count += 1
                        break
                    elif info['not_folded_count'] < 2 and info[dict_i]['view']:
                        info[info['not_folded_list'][0]]['chips'] += chips_pool
                        print(f"{'*' * 50}")
                        print(
                            f"{'*' * 4}  玩家 {info[info['not_folded_list'][0]]['name']} 赢，赢得筹码 {chips_pool} 剩余 {info[info['not_folded_list'][0]]['chips']} 筹码  {'*' * 4}")
                        print(f"{'*' * 50}")
                        print(f"{'-' * 50} 第 {round_count} 局结束 {'-' * 50}")
                        rounds_over = True
                        round_count += 1
                        break
                    # 看牌
                    if info[dict_i]['view']:
                        view_card = '1'
                    else:
                        view_card = input("请输入 1 回车后看牌， 按任意键回车后不看牌: ")

                    if view_card == '1':
                        if dict_i not in info['not_folded_list']:
                            info['not_folded_list'].append(dict_i)
                        if not info[dict_i]['view']:
                            info[dict_i]['view'] = True
                            info['unchecked_count'] -= 1
                        print(f"玩家 {info[dict_i]['name']} 的牌是： {info[dict_i]['color_card']}")
                        print(f"玩家 {info[dict_i]['name']} 剩余筹码 {info[dict_i]['chips']}")
                        print(f"当前池子筹码为 {chips_pool}")
                        choose_view_card = input("请输入 1 回车后弃牌， 按任意键回车后跟注: ")
                        # 看牌跟注
                        if choose_view_card == '1':
                            info[dict_i]['drop'] = True
                            info['not_folded_count'] -= 1
                            info['not_folded_list'].remove(dict_i)
                            print(
                                f"玩家 {info[dict_i]['name']} 弃牌, 当前池子筹码为 {chips_pool}, 剩余玩家 {info['not_folded_count']}")
                            continue
                        # 看牌后弃牌
                        else:
                            if info[dict_i]['chips'] >= last_follow_amount:
                                follow_amount = self.user_input(last_follow_amount, dict_i)
                                info[dict_i]['chips'] -= follow_amount
                                chips_pool += follow_amount
                                last_follow_amount = follow_amount
                            else:
                                choose_borrow = input(
                                    f"玩家 {info[dict_i]['name']} 剩余筹码 {info[dict_i]['chips']} ，筹码不足，按 1 回车后借贷，按任意键回车后弃牌 ")
                                if choose_borrow == '1':
                                    borrow_chips = int(input("输入借贷金额: "))
                                    info[dict_i]['chips'] += borrow_chips
                                else:
                                    info[dict_i]['drop'] = True
                                    info['not_folded_count'] -= 1
                                    info['not_folded_list'].remove(dict_i)
                                    print(
                                        f"玩家 {info[dict_i]['name']} 弃牌, 当前池子筹码为 {chips_pool}, 剩余玩家 {info['not_folded_count']}")
                                    continue

                    # 不看牌 玩家下盲注
                    else:
                        print("不看牌下盲注，下一位玩家跟注时，将至少是你盲注的2倍")
                        unchecked_card_follow_amount = self.user_input(int(last_follow_amount / 2), dict_i)
                        info[dict_i]['chips'] -= unchecked_card_follow_amount
                        chips_pool += unchecked_card_follow_amount
                        last_follow_amount = unchecked_card_follow_amount * 2

                    # 开牌
                    if info['not_folded_count'] == 2 and info['unchecked_count'] == 0:
                        open_card = input(f"当前玩家剩余 {info['not_folded_count']} ，请输入 1/2 (1. 开牌 2. 不开牌): ")
                        if open_card == '1':
                            print(
                                f"玩家 {info[info['not_folded_list'][0]]['name']} 的牌为  {info[info['not_folded_list'][0]]['color_card']}")
                            print(
                                f"玩家 {info[info['not_folded_list'][1]]['name']} 的牌为  {info[info['not_folded_list'][1]]['color_card']}")
                            if info[info['not_folded_list'][0]]['size_card'] > info[info['not_folded_list'][1]]['size_card']:
                                info[info['not_folded_list'][0]]['chips'] += chips_pool
                                print(f"{'*' * 50}")
                                print(
                                    f"**   玩家 {info[info['not_folded_list'][0]]['name']} 赢，赢得筹码 {chips_pool}, 剩余 {info[info['not_folded_list'][0]]['chips']} 筹码  **")
                                print(f"{'*' * 50}")
                            else:
                                info[info['not_folded_list'][1]]['chips'] += chips_pool
                                print(f"{'*' * 50}")
                                print(
                                    f"**   玩家 {info[info['not_folded_list'][1]]['name']} 赢，赢得筹码 {chips_pool}, 剩余 {info[info['not_folded_list'][1]]['chips']} 筹码  **")
                                print(f"{'*' * 50}")
                            # 局数累加
                            print(f"{'-' * 50} 第 {round_count} 局结束 {'-' * 50}")
                            rounds_over = True
                            round_count += 1
                            break

                # 回合累加
                internal_rounds += 1

                if rounds_over:
                    break


x = Game(4)
x.start()
