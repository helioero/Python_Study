"""
    主函数运行文件
"""
from Game.start_command import Game
from Game.start_GUI import GameGUI

# 运行 cmd 游戏
# runner = Game(3)
# runner.start()

# 运行 GUI game 
runner = GameGUI(3)
runner.start()
