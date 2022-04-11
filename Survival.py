# -*- coding: utf-8 -*-
"""
脚本功能：植物大战僵尸生存模式键控发炮回车选卡
创建日期：2021-4-9
"""

from pynput import mouse, keyboard
import win32gui
# import ctypes
import time


# 抽象父类，不允许直接构造对象
class Survival:
    """
    ------------ 待子类实现的成员 ------------
      keys = tuple()  发炮按键
      cards = tuple()  选卡
      launch_cannon_pair(self, i)  发炮函数
    ---------------------------------------
    """

    # 屏幕缩放比例，在 keyboard_on_press 动态获取实际数值
    zoom = 1.0

    # 窗口偏移
    window_offset = (0, 0)

    # 游戏窗口名称
    game_name = 'Plants vs. Zombies'

    # 构造函数
    def __init__(self):
        # ---- 公共成员 ---- #
        # 鼠标控制器
        self.mouse_controller = mouse.Controller()

        # 键盘监听器
        self.keyboard_listener = None
        # keyboard.Listener(on_press=self.keyboard_on_press, on_release=self.keyboard_on_release)

        # 选卡界面行列
        self.card_rows = tuple(160 + i * 70 for i in range(0, 6))
        self.card_cols = tuple(50 + i * 50 for i in range(0, 8))

        # 模仿者坐标
        self.imitator_pos = (490, 550)

        # Let's Rock 坐标
        self.lets_rock_pos = (234, 567)

        # 选卡按键集合
        self.keys_select = {
            keyboard.Key.enter,
            keyboard.KeyCode(char='s'),
            keyboard.KeyCode(char='d'),
            keyboard.Key.f2,
            keyboard.Key.f3,
        }

        # 停止按钮 combo
        self.keys_halt = {
            keyboard.KeyCode(char='h'),
            keyboard.Key.alt_l,
        }

        # Ignore other keyboard input if one of these keys is pressed.
        self.keys_modifier_ignore = {
            keyboard.Key.cmd,  # Win key.
            keyboard.Key.ctrl_l,
        }

        # 通过 self.main.keys_pressed 获取已经按下的键集合
        self.main = None

    def renew_keyboard_listener(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.keyboard_on_press, on_release=self.keyboard_on_release)

    # 开始监听
    def listen(self):
        self.renew_keyboard_listener()
        self.keyboard_listener.start()  # 持续运行，直到 on_press() 或 on_release() 返回 False 时结束
        self.keyboard_listener.join()

    # 按下按键
    def keyboard_on_press(self, key):
        self.main.keys_pressed.add(key)
        # print('keys pressed: ' + str(self.main.keys_pressed))

        # 停止按键
        if self.keys_halt <= self.main.keys_pressed:
            print('halt')
            return False

        # Ignore input.
        if self.keys_modifier_ignore & self.main.keys_pressed:
            return

        # 游戏窗口
        game_window = win32gui.GetForegroundWindow()
        if win32gui.GetWindowText(game_window) != Survival.game_name:
            return
        last_offset = Survival.window_offset
        Survival.window_offset = Survival.get_window_offset(game_window)
        if Survival.window_offset != last_offset:
            print('window_offset: ' + str(Survival.window_offset))

        # 缩放比例
        last_zoom = Survival.zoom
        Survival.zoom = Survival.get_windows_zoom_scale(game_window)  # 实时获取屏幕缩放比例
        if Survival.zoom != last_zoom:
            print('zoom = ' + str(Survival.zoom))

        sleep_time = 0.1

        # 发炮按键
        try:
            i = self.keys.index(key)  # Raises ValueError if the value is not present.

            # SaveMousePos
            saved_mouse_pos = self.mouse_controller.position

            self.launch_cannon_pair(i)

            # RestoreMousePos
            self.mouse_controller.position = saved_mouse_pos

        # 选卡按键
        except ValueError:
            if key in self.keys_select:
                # SaveMousePos
                saved_mouse_pos = self.mouse_controller.position

                is_last_card_imitator = False

                # 点击卡片
                for card in self.cards:

                    self.mouse_controller.position = Survival.get_display_pos(card)
                    if card == self.imitator_pos:
                        is_last_card_imitator = True
                        time.sleep(sleep_time)
                    elif is_last_card_imitator:
                        is_last_card_imitator = False
                        time.sleep(sleep_time)
                    else:
                        pass
                    self.mouse_controller.click(mouse.Button.left, 1)

                # 点击 Let's Rock
                self.mouse_controller.position = Survival.get_display_pos(self.lets_rock_pos)
                time.sleep(sleep_time)
                self.mouse_controller.click(mouse.Button.left, 1)

                # RestoreMousePos
                self.mouse_controller.position = saved_mouse_pos

            # 其他无关按钮
            else:
                pass

    # 抬起按键
    def keyboard_on_release(self, key):
        # 从当前已按按键集合中删除
        try:
            self.main.keys_pressed.remove(key)
        except KeyError:
            pass

    # 获取 Windows 屏幕缩放比例
    @staticmethod
    def get_windows_zoom_scale(window):
        client_rect = win32gui.GetClientRect(window)
        height = client_rect[3]
        standard_height = 600
        return height / standard_height

        # # [Obsolete] Even when zoom=1.25 (width: 1920, width_scale: 1536),
        # # the client_rect is still (0, 0, 800, 600).
        # user32 = ctypes.windll.user32
        # gdi32 = ctypes.windll.gdi32
        # dc = user32.GetDC(None)
        # width = gdi32.GetDeviceCaps(dc, 118)  # 原始分辨率的宽度
        # width_scale = gdi32.GetDeviceCaps(dc, 8)  # 分辨率缩放后的宽度
        # print('width:', width, 'width_scale:', width_scale)

    # 模仿植物卡片坐标偏移
    @staticmethod
    def imitator_offset(pos):
        return pos[0] + 160, pos[1] + 5

    @staticmethod
    def get_window_offset(window):
        window_rect = win32gui.GetWindowRect(window)
        client_rect = win32gui.GetClientRect(window)
        border_width = (window_rect[2] - window_rect[0] - client_rect[2]) // 2
        header_height = window_rect[3] - window_rect[1] - client_rect[3] - border_width * 2
        # print('window_rect:', window_rect, 'client_rect:', client_rect,
        #       'border_width:', border_width, 'header_height:', header_height)

        # Black bars will occur when it is fullscreen with ratio > 4:3.
        black_bar_width = 0
        if client_rect[2] * 3 > 4 * client_rect[3]:
            desired_width = client_rect[3] * 4 // 3
            black_bar_width = (client_rect[2] - desired_width) // 2
        return window_rect[0] + border_width + black_bar_width, window_rect[1] + border_width + header_height

    @staticmethod
    def get_display_pos(pos):
        return pos[0] * Survival.zoom + Survival.window_offset[0], pos[1] * Survival.zoom + Survival.window_offset[1]
