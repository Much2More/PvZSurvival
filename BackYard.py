# -*- coding: utf-8 -*-
"""
脚本功能：植物大战僵尸生存模式后院 - 泳池八炮 | 雾四炮
创建日期：2021-4-9
说明：1 2 3 4 和炮弹的左右顺序对应，炸前场
     q w e r 炸后场
"""

from pynput import mouse, keyboard
from Survival import Survival


# 泳池八炮 | 雾四炮
class BackYard(Survival):
    # 构造函数
    def __init__(self, is_night=False):
        super().__init__()

        # @override 按键(8) - 前四个键炸前场 后四个键炸后场
        self.keys = (
            keyboard.KeyCode(char='1'),
            keyboard.KeyCode(char='2'),
            keyboard.KeyCode(char='3'),
            keyboard.KeyCode(char='4'),
            keyboard.KeyCode(char='q'),
            keyboard.KeyCode(char='w'),
            keyboard.KeyCode(char='e'),
            keyboard.KeyCode(char='r'),
        )

        # @override 选卡(10)
        self.cards = (
            (self.card_cols[0], self.card_rows[2]),  # 睡莲
            (self.card_cols[6], self.card_rows[3]),  # 南瓜
            (self.card_cols[2], self.card_rows[4]),  # 玉米
            (self.card_cols[7], self.card_rows[5]),  # 加农
            (self.card_cols[3], self.card_rows[4]),  # 咖啡
            (self.card_cols[6], self.card_rows[1]),  # 冰菇
            (self.card_cols[1], self.card_rows[2]),  # 窝瓜
            (self.card_cols[2], self.card_rows[0]),  # 樱桃
            (self.card_cols[3], self.card_rows[3]),  # 三叶
            (self.card_cols[5], self.card_rows[4]),  # 莴苣
        ) if not is_night else (
            (self.card_cols[6], self.card_rows[1]),  # 寒冰菇
            self.imitator_pos,  # 模仿者
            Survival.imitator_offset((self.card_cols[6], self.card_rows[1])),  # 模仿寒冰菇
            (self.card_cols[7], self.card_rows[1]),  # 毁灭菇
            (self.card_cols[0], self.card_rows[2]),  # 睡莲
            (self.card_cols[6], self.card_rows[3]),  # 南瓜
            (self.card_cols[2], self.card_rows[1]),  # 大喷菇
            (self.card_cols[2], self.card_rows[0]),  # 樱桃
            (self.card_cols[3], self.card_rows[3]),  # 三叶
            (self.card_cols[1], self.card_rows[1]),  # 小喷菇
            (self.card_cols[0], self.card_rows[1]),  # 阳光菇
        )

        # 行：初始值 160/1.5, 行距 130/1.5
        self.rows = tuple(108 + i * 87 for i in range(0, 6))

        # 列：0 1 2 - 从左到右三列炮, 3 4 - 落点
        self.cols = (166, 300, 426, 613, 686, )

        # Cannons 坐标
        self.cannons = (
            (self.cols[0], self.rows[2]),
            (self.cols[0], self.rows[3]),
            (self.cols[1], self.rows[2]),
            (self.cols[1], self.rows[3]),
            (self.cols[2], self.rows[0]),
            (self.cols[2], self.rows[1]),
            (self.cols[2], self.rows[4]),
            (self.cols[2], self.rows[5]),
        )

        # 落点
        self.drop_row = (self.rows[1], self.rows[4])
        self.drop_col = (self.cols[3], self.cols[4])

    # @override 发炮函数
    def launch_cannon_pair(self, i):
        n_pair = i % 4  # 第几组炮 0~3
        n_col = 1 if i < 4 else 0  # 落点在前场还是后场

        c1 = n_pair * 2  # cannon1
        c2 = c1 + 1  # cannon2

        self.mouse_controller.position = Survival.get_display_pos(self.cannons[c1])
        self.mouse_controller.click(mouse.Button.left, 1)
        self.mouse_controller.position = Survival.get_display_pos((self.drop_col[n_col], self.drop_row[0]))
        self.mouse_controller.click(mouse.Button.left, 1)

        self.mouse_controller.position = Survival.get_display_pos(self.cannons[c2])
        self.mouse_controller.click(mouse.Button.left, 1)
        self.mouse_controller.position = Survival.get_display_pos((self.drop_col[n_col], self.drop_row[1]))
        self.mouse_controller.click(mouse.Button.left, 1)


if __name__ == "__main__":
    survival = BackYard(is_night=False)
    survival.listen()
