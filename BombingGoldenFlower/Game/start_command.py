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

    def __init__(self, user_count):
        """ 初始化 筹码"""

        self.user_init_chips = 1000
        self.user_count = int(user_count)
        if self.user_count > 17:
            print('此游戏最多17人玩')
            exit(1)
        self.user_info_dict_list = self.generate_user_info(self.user_count, self.user_init_chips)

    def get_cards(self, users, username_list):
        """ 将用户的牌生成以并计算牌面大小 """

        self.user_init_card_list = self.post_cards(users)
        self.user_color_card_list = self.print_color_card(self.user_init_card_list)
        self.user_point_and_color_card_list = self.compute_card_point(self.user_init_card_list)
        self.user_size_card_list = self.compute_winner_size(self.user_point_and_color_card_list[0],
                                                            self.user_point_and_color_card_list[1])
        # 将牌的花色以及大小写入字典
        for idx, items in enumerate(username_list):
            if not self.user_info_dict_list[items]['disuse']:
                self.user_info_dict_list[items]["color_card"] = self.user_color_card_list[idx]
                self.user_info_dict_list[items]["size_card"] = self.user_size_card_list[idx]

        print(self.user_color_card_list)
        print(self.user_size_card_list)

    def user_input(self, head_amount, username):
        """ 用户循环输入判断"""
        while True:
            user_input_value = input(f"请输入下注的筹码，必须在区间({head_amount} - {self.user_info_dict_list[username]['chips']}), 默认为 {head_amount}: ")
            if user_input_value == '':
                user_input_value = head_amount
                print(f'玩家下注 {head_amount}')
                break
            elif user_input_value.isdigit():
                if head_amount <= int(user_input_value) <= self.user_info_dict_list[username]['chips']:
                    print(f'玩家下注 {int(user_input_value)}')
                    break
            else:
                print("输入的值不为正整数，请重新输入")
        return int(user_input_value)

    def start(self):
        """ 游戏运行主逻辑 """
        print(f"{'-' * 50}")
        print("欢迎来到澳门新葡京娱乐城，这里正在进行名为 炸金花 的扑克牌牌局")
        print(f"本次牌局共有 {self.user_count} 名玩家参加，每名玩家初始筹码为 {self.user_init_chips}, 每轮底注为10")
        print("游戏马上开始，祝你玩的开心")
        # 局数初始化
        round_count = 1
        while True:

            # 初始化
            # 筹码池初始化
            chips_pool = 0
            low_chips = 10
            info = self.user_info_dict_list
            chips_pool, low_chips = self.round_init_pool_user_info_dict(info['username_list'], info, chips_pool, low_chips)

            # 如果 玩家 只剩一个，退出循环
            if info['valid_user'] == 1:
                print(f"{'*' * 80}")
                print(
                    f"{'*' * 2}/t/t游戏结束, 玩家 {info['not_folded_list'][0]} 是本次活动大赢家, 该玩家赢得筹码 {info[info['not_folded_list'][0]]['chips'] + 10}/t/t{'*' * 2}")
                print(f"{'*' * 80}")
                break

            print()
            # self.loading_card()
            print()
            print(f"{'-' * 50} 第 {round_count} 局开始 {'-' * 50}")
            print(f"所有玩家扣除底注 {low_chips}")

            # 生成 当前已有玩家的牌
            self.get_cards(info['valid_user'], info['username_list'])

            # 初始化内部 while 循环变量
            rounds_over = False
            internal_rounds = 1
            last_follow_amount = 10

            while True:

                print(f"{'#' * 30} 第 {round_count} 局, 第 {internal_rounds} 回合 {'#' * 30}")
                for username in info['username_list']:

                    if info[username]['disuse'] or info[username]['drop']:
                        continue
                    print(
                        f"{'#' * 20} 本回合剩余玩家 {info['not_drop_card_count']}, {info['unchecked_count']} 位下盲注, {info['checked_count']} 位跟注 {'#' * 20}")
                    print(f"{'-' * 30}> 玩家 {username} 的回合")
                    # 其他玩家弃牌，只剩 1 名玩家时
                    if info['not_drop_card_count'] < 2:
                        info[username]['chips'] += chips_pool
                        print(f"{'*' * 50}")
                        print(
                            f"{'*' * 2} 🎉🎉🎉 玩家 {username} 赢，赢得筹码 {chips_pool} 🎉🎉🎉 {'*' * 2}")
                        print(f"{'*' * 50}")
                        print(f"{'-' * 50} 第 {round_count} 局结束 {'-' * 50}")
                        rounds_over = True
                        round_count += 1
                        break
            
                    # 看牌
                    if info[username]['view']:
                        view_card = 1
                    else:
                        view_card = input("请输入 1 回车后看牌， 按任意键回车后不看牌: ")

                    if view_card == '1':
                        if username not in info['not_folded_list']:
                            info['not_folded_list'].append(username)
                            info[username]['view'] = True
                            info['unchecked_count'] -= 1
                        print(f"玩家 {username} 的牌是： {info[username]['color_card']}")
                        print(f"玩家 {username} 剩余筹码 {info[username]['chips']}")
                        print(f"当前池子筹码为 {chips_pool}")
                        choose_view_card = input("请输入 1 回车后弃牌， 按任意键回车后跟注: ")
                        # 看牌跟注
                        if choose_view_card == '1':
                            info[username]['drop'] = True
                            info['not_drop_card_count'] -= 1
                            info['not_folded_list'].remove(username)
                            print(
                                f"玩家 {username} 弃牌, 当前池子筹码为 {chips_pool}, 剩余玩家 {info['not_drop_card_count']}")
                            continue
                        # 看牌后弃牌
                        else:
                            if info[username]['chips'] >= last_follow_amount:
                                follow_amount = self.user_input(last_follow_amount, username)
                                info[username]['chips'] -= follow_amount
                                chips_pool += follow_amount
                                last_follow_amount = follow_amount
                                info['checked_count'] += 1
                            else:
                                choose_borrow = input(
                                    f"玩家 {username} 剩余筹码 {info[username]['chips']} ，筹码不足，按 1 回车后借贷，按任意键回车后弃牌 ")
                                if choose_borrow == '1':
                                    borrow_chips = int(input("输入借贷金额: "))
                                    info[username]['chips'] += borrow_chips
                                else:
                                    info[username]['drop'] = True
                                    info['not_drop_card_count'] -= 1
                                    info['valid_user'] -= 1
                                    info['username_list'].remove(username)
                                    print(
                                        f"玩家 {username} 弃牌, 当前池子筹码为 {chips_pool}, 剩余玩家 {info['not_drop_card_count']}")
                                    continue

                    # 不看牌 玩家下盲注
                    else:
                        print("不看牌下盲注，下一位玩家跟注时，将至少是你盲注的2倍")
                        unchecked_card_follow_amount = self.user_input(int(last_follow_amount / 2), username)
                        info[username]['chips'] -= unchecked_card_follow_amount
                        chips_pool += unchecked_card_follow_amount
                        last_follow_amount = unchecked_card_follow_amount * 2

                    # 开牌
                    if info['not_drop_card_count'] == 2 and info['unchecked_count'] == 0:
                        open_card = input(f"当前玩家剩余 {info['not_drop_card_count']} ，请输入 1/2 (1. 开牌 2. 不开牌): ")
                        if open_card == '1':
                            print(
                                f"玩家 {info['not_folded_list'][0]} 的牌为  {info[info['not_folded_list'][0]]['color_card']}")
                            print(
                                f"玩家 {info['not_folded_list'][1]} 的牌为  {info[info['not_folded_list'][1]]['color_card']}")
                            if info[info['not_folded_list'][0]]['size_card'] > info[info['not_folded_list'][1]]['size_card']:
                                info[info['not_folded_list'][0]]['chips'] += chips_pool
                                print(f"{'*' * 50}")
                                print(
                                    f"**   玩家 {info['not_folded_list'][0]} 赢，赢得筹码 {chips_pool}, 剩余 {info[info['not_folded_list'][0]]['chips']} 筹码  **")
                                print(f"{'*' * 50}")
                            else:
                                info[info['not_folded_list'][1]]['chips'] += chips_pool
                                print(f"{'*' * 50}")
                                print(
                                    f"**   玩家 {info['not_folded_list'][1]} 赢，赢得筹码 {chips_pool}, 剩余 {info[info['not_folded_list'][1]]['chips']} 筹码  **")
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



