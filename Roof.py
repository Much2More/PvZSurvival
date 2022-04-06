# -*- coding: utf-8 -*-
"""
脚本功能：植物大战僵尸生存模式屋顶 - 屋顶十炮 | 月夜十炮
创建日期：2021-4-11
说明：1 2 3 4 5 前场
     Q W E R T 后场（防蹦极）
     使用左侧炮时，原版游戏落点会向上偏移，所以用来炸上两行；右侧炮炸下三行
     当每个最后一波蹦极放僵尸或中途偷东西时，都要放寒冰菇冻住
"""

from pynput import mouse, keyboard
from Survival import Survival
import time


# 屋顶
class Roof(Survival):
    # 构造函数
    def __init__(self, is_night=False):
        super().__init__()

        # @override 按键(10) - 前五个键炸前场 后五个键炸后场
        self.keys = (
            keyboard.KeyCode(char='1'),
            keyboard.KeyCode(char='2'),
            keyboard.KeyCode(char='3'),
            keyboard.KeyCode(char='4'),
            keyboard.KeyCode(char='5'),
            keyboard.KeyCode(char='q'),
            keyboard.KeyCode(char='w'),
            keyboard.KeyCode(char='e'),
            keyboard.KeyCode(char='r'),
            keyboard.KeyCode(char='t'),
        )

        # @override 选卡(10)
        self.cards = (
            (self.card_cols[2], self.card_rows[4]),  # 玉米
            (self.card_cols[7], self.card_rows[5]),  # 加农
            (self.card_cols[6], self.card_rows[3]),  # 南瓜
            (self.card_cols[3], self.card_rows[4]),  # 咖啡
            (self.card_cols[6], self.card_rows[1]),  # 冰菇
            self.imitator_pos,  # 模仿者
            Survival.imitator_offset((self.card_cols[6], self.card_rows[1])),  # 模仿寒冰菇
            (self.card_cols[1], self.card_rows[2]),  # 窝瓜
            (self.card_cols[2], self.card_rows[0]),  # 樱桃
            (self.card_cols[1], self.card_rows[4]),  # 花盆
            (self.card_cols[3], self.card_rows[3]),  # 三叶
        ) if not is_night else (
            (self.card_cols[2], self.card_rows[4]),  # 玉米
            (self.card_cols[7], self.card_rows[5]),  # 加农
            (self.card_cols[6], self.card_rows[3]),  # 南瓜
            (self.card_cols[6], self.card_rows[1]),  # 冰菇
            self.imitator_pos,  # 模仿者
            Survival.imitator_offset((self.card_cols[6], self.card_rows[1])),  # 模仿寒冰菇
            (self.card_cols[1], self.card_rows[2]),  # 窝瓜
            (self.card_cols[2], self.card_rows[0]),  # 樱桃
            (self.card_cols[1], self.card_rows[4]),  # 花盆
            (self.card_cols[3], self.card_rows[3]),  # 三叶
            (self.card_cols[7], self.card_rows[1]),  # 毁灭菇
        )

        # 行：初始值 160/1.5, 行距 130/1.5
        self.rows_l = tuple(200 + i * 87 for i in range(0, 5))
        self.rows_r = tuple(113 + i * 87 for i in range(0, 5))

        # 列：0 1 - 两列炮, 2 3 - 两列落点
        self.cols = (80, 560, 560, 693,)

        # 落点
        self.drop_row = (self.rows_r[1], self.rows_r[3])
        self.drop_col = (self.cols[2], self.cols[3])

    # @override 发炮函数
    def launch_cannon_pair(self, i):
        n_pair = i % 5  # 第几组炮 0~4
        n_col = 1 if i < 5 else 0  # 落点在前场还是后场

        self.mouse_controller.position = Survival.get_display_pos((self.cols[0], self.rows_l[n_pair]))
        self.mouse_controller.click(mouse.Button.left, 1)
        self.mouse_controller.position = Survival.get_display_pos((self.drop_col[n_col], self.drop_row[0]))
        self.mouse_controller.click(mouse.Button.left, 1)

        self.mouse_controller.position = Survival.get_display_pos((self.cols[1], self.rows_r[n_pair]))
        self.mouse_controller.click(mouse.Button.left, 1)
        # 右下三个炮炸后场时由于落点在炮身，直接点击无法发射，需要等待片刻
        if i >= 7:
            time.sleep(0.4)
        self.mouse_controller.position = Survival.get_display_pos((self.drop_col[n_col], self.drop_row[1]))
        self.mouse_controller.click(mouse.Button.left, 1)


if __name__ == "__main__":
    survival = Roof(is_night=False)
    survival.listen()
