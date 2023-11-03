'''
运行此代码需要 Python3.10 +
这是一个 炸金花 的纸牌游戏, 在命令行运行
由 Helioer 学习 N 天后独家撰写, 如果有疑问请咨询： helioer@sina.cn
'''

from random import randrange

def GenerateList():
    
    cards_list = []
    for i in range(1,53):
        cards_list.append(i)
    return cards_list

def RandomPoint():
    
    point_num = randrange(1, 53)
    return point_num


def GenerateCards(count):
    
    all_cards_list = []
    all_cards_list = GenerateList()
    i = 0
    random_cards_list = []
    while True:
        random_num = RandomPoint()
        if all_cards_list.count(random_num):
            random_cards_list.append(random_num)
            all_cards_list.remove(random_num)
            i += 1
        else:
            continue
        
        if count == i:
            break
        
    return random_cards_list

def PostCards(user_count):
    
    cards_list = GenerateCards(user_count * 3)
    user_cards = []
    cards = []
    j = 1
    for i in range(user_count * 3):
        user_cards.append(cards_list[i])
        if j % 3 == 0:
            cards.append(user_cards)
            user_cards = []
        j += 1
    
    return cards

def PrintColorCards(card):
    
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


def ComputeColorPointCard(card):
    
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
 

def ComputeWinnerSize(point_card,color_card):
    
    winner_list = []
    for i in range(len(point_card)):
        point_card[i].sort()
        point =  point_card[i][0] + point_card[i][1] + point_card[i][2] * 10
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

def GenerateUserInfoDictList(user_count, user_init_chips):
    
    user_info_dict_list = {}
    for i in range(user_count):
        
        dict_v = {'view': False, 'drop': False, 'disuse': False}
        dict_v['name'] = '000' + str(i)
        dict_v['chips'] = user_init_chips
        user_info_dict_list[i] = dict_v

    user_info_dict_list["unview_count"] = 0
    user_info_dict_list["undrop_count"] = user_count
    user_info_dict_list["undrop_list"] = []
    user_info_dict_list["valid_user"] = user_count
    return user_info_dict_list
    
class Game(object):
    
    user_count = 0
    user_init_chips = 0
    user_info_dict_list = {}
    user_init_card_list = []
    user_color_card_list = []
    user_point_and_color_card_list = []
    user_size_card_list = []
    
    # 初始化 生成玩家的牌 以及筹码
    def __init__(self,user_count):
        
        self.user_init_chips = 1000
        self.user_count = int(user_count)
        self.user_info_dict_list = GenerateUserInfoDictList(self.user_count, self.user_init_chips)
        
    def GetCards(self, users):
        
        self.user_init_card_list = PostCards(users)
        self.user_color_card_list = PrintColorCards(self.user_init_card_list)
        self.user_point_and_color_card_list = ComputeColorPointCard(self.user_init_card_list)
        self.user_size_card_list = ComputeWinnerSize(self.user_point_and_color_card_list[0], self.user_point_and_color_card_list[1])
        print(self.user_color_card_list)
        print(self.user_size_card_list)
        
    def Start(self):
        
        print(f"{'-' * 50 }")
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
            # 状态初始化
            for item in range(self.user_count):
                
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
            
            info['unview_count'] = info['valid_user']
            info['undrop_count'] = info['valid_user']
            info['undrop_list'] = []
                        
            # 如果 玩家 只剩一个，退出循环       
            if info['valid_user'] == 1:
                print(f"{'*' * 50}")
                print(f"{'*' * 2}  玩家 {info[item]['name']} 是本次活动大赢家, 该玩家总共筹码 {info[item]['chips']}  {'*' * 2}")
                print(f"{'*' * 50}")
                break
            
            print(f"{'-' * 50 } 第 {round_count} 局开始 {'-' * 50 }")
            print(f"所有玩家扣除底注 {low_chips}")
            
            # 生成 当前已有玩家的牌
            self.GetCards(info['valid_user'])
            
            # 初始化内部 while 循环变量
            rounds_over = False
            internal_rounds = 1
            last_follow_amount = 10
            unknow_card_follow_amount = 5
            
            while True:
                
                print(f"{'#' * 30 } 第 {round_count} 局, 第 {internal_rounds} 回合 {'#' * 30 }")
                
                for dict_i in range(self.user_count):
                    
                    if info[dict_i]['disuse'] or info[dict_i]['drop']:
                        continue
                    print(f"{'#' * 20 } 本回合剩余玩家 {info['undrop_count']}, {info['unview_count']} 位下盲注, {info['undrop_count'] - info['unview_count']} 位跟注 {'#' * 20 }")
                    print(f"{'-' * 30}> 玩家 {info[dict_i]['name']} 的回合")
                    # 其他玩家弃牌，只剩 1 名玩家时
                    if info['undrop_count'] < 2 and not info[dict_i]['view']:
                        info[dict_i]['chips'] += chips_pool
                        print(f"{'*' * 50}")
                        print(f"{'*' * 2}  玩家 {info[dict_i]['name']} 赢，赢得筹码 {chips_pool} 剩余 {info[dict_i]['chips']} 筹码  {'*' * 2}")
                        print(f"{'*' * 50}")
                        print(f"{'-' * 50 } 第 {round_count} 局结束 {'-' * 50 }")
                        rounds_over = True
                        round_count += 1
                        break
                    elif info['undrop_count'] < 2 and info[dict_i]['view']:
                        info[info['undrop_list'][0]]['chips'] += chips_pool
                        print(f"{'*' * 50}")
                        print(f"{'*' * 2}  玩家 {info[info['undrop_list'][0]]['name']} 赢，赢得筹码 {chips_pool} 剩余 {info[info['undrop_list'][0]]['chips']} 筹码  {'*' * 2}")
                        print(f"{'*' * 50}")
                        print(f"{'-' * 50 } 第 {round_count} 局结束 {'-' * 50 }")
                        rounds_over = True
                        round_count += 1
                        break
                    # 看牌
                    if info[dict_i]['view']:
                        view_card = '1'
                    else:
                        view_card = input("请输入 1/2 (1、看牌 2、不看牌): ")
                        
                    if view_card == '1':
                        if dict_i not in info['undrop_list']:
                            info['undrop_list'].append(dict_i)
                        if not info[dict_i]['view']:
                            info[dict_i]['view'] = True
                            info['unview_count'] -= 1
                        print(f"玩家 {info[dict_i]['name']} 的牌是： {self.user_color_card_list[dict_i]}")
                        print(f"玩家 {info[dict_i]['name']} 剩余筹码 {info[dict_i]['chips']}")
                        print(f"当前池子筹码为 {chips_pool}")
                        choose_view_card = input("1.弃牌 2.跟注，请输入(1/2): ")
                        # 看牌跟注
                        if choose_view_card == '' or choose_view_card == '2':
                            follow_amount = int(input(f"请输入跟注的筹码({last_follow_amount} - 1000): "))
                            if follow_amount >= last_follow_amount:
                                if info[dict_i]['chips'] >= last_follow_amount:
                                    last_follow_amount *= 2
                                    info[dict_i]['chips'] -= follow_amount
                                    chips_pool += follow_amount
                                    last_follow_amount = follow_amount
                                else:
                                    choose_borrow = input(f"玩家 {info[dict_i]['name']} 剩余筹码 {info[dict_i]['chips']} ，筹码不足，请借贷或弃牌 (1. 弃牌 2. 借贷) ")
                                    if choose_borrow == '' or choose_borrow == '2':
                                        borrow_chips = int(input("输入借贷金额: "))
                                        info[dict_i]['chips'] += borrow_chips
                                    elif choose_borrow == '1':
                                        info[dict_i]['drop'] = True
                                        info['undrop_count'] -= 1
                                        info['undrop_list'].remove(dict_i)
                                        print(f"玩家 {info[dict_i]['name']} 弃牌, 当前池子筹码为 {chips_pool}, 剩余玩家 {info['undrop_count']}")
                                        continue
                            else:
                                print(f"跟注筹码小于上一名玩家的筹码")
                        # 看牌后弃牌
                        elif choose_view_card == '1':
                            info[dict_i]['drop'] = True
                            info['undrop_count'] -= 1
                            info['undrop_list'].remove(dict_i)
                            print(f"玩家 {info[dict_i]['name']} 弃牌, 当前池子筹码为 {chips_pool}, 剩余玩家 {info['undrop_count']}")
                            continue
                        
                    # 不看牌 玩家下盲注
                    elif view_card == '' or view_card == '2':
                        unknow_card_follow_amount = int(input(f"请输入盲注筹码({last_follow_amount} - 1000): "))
                        info[dict_i]['chips'] -= unknow_card_follow_amount
                        chips_pool += unknow_card_follow_amount
                        last_follow_amount = unknow_card_follow_amount
                    else:
                        print("!!!! 输入错误，请重新输入 1/2 (1、看牌 2、不看牌)")
                    
                    # 开牌
                    print(info['undrop_count'])
                    print(info['unview_count'])
                    if info['undrop_count'] == 2 and info['unview_count'] == 0:
                        open_card = input(f"当前玩家剩余 {info['undrop_count']} ，请输入 1/2 (1. 开牌 2. 不开牌): ")
                        if open_card == '1':
                            print(f"玩家 {info[info['undrop_list'][0]]['name']} 的牌为  {self.user_color_card_list[info['undrop_list'][0]]}")
                            print(f"玩家 {info[info['undrop_list'][1]]['name']} 的牌为  {self.user_color_card_list[info['undrop_list'][1]]}")
                            if self.user_size_card_list[info['undrop_list'][0]] > self.user_size_card_list[info['undrop_list'][1]]:
                                info[info['undrop_list'][0]]['chips'] += chips_pool
                                print(f"{'*' * 50}")
                                print(f"**   玩家 {info[info['undrop_list'][0]]['name']} 赢，赢得筹码 {chips_pool}, 剩余 {info[info['undrop_list'][0]]['chips']} 筹码  **")
                                print(f"{'*' * 50}")
                            else:
                                info[info['undrop_list'][1]]['chips'] += chips_pool
                                print(f"{'*' * 50}")
                                print(f"**   玩家 {info[info['undrop_list'][1]]['name']} 赢，赢得筹码 {chips_pool}, 剩余 {info[info['undrop_list'][1]]['chips']} 筹码  **")
                                print(f"{'*' * 50}")
                            # 局数累加
                            print(f"{'-' * 50 } 第 {round_count} 局结束 {'-' * 50 }")
                            rounds_over = True
                            round_count += 1
                            break
                    
                    
                # 回合累加
                internal_rounds += 1
                
                if rounds_over:
                    break
                
            






x = Game(4)
# print(x.user_init_card_list)
# print(x.user_color_card_list)
# print(x.user_point_and_color_card_list)
# print(x.user_size_card_list)
print(x.Start())

