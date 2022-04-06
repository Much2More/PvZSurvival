# -*- coding: utf-8 -*-
"""
脚本功能：植物大战僵尸生存模式主函数
创建日期：2021-4-18
说明：1 2 3 4 5 6
"""

import os
from pynput import mouse, keyboard
from FrontYard import FrontYard
from BackYard import BackYard
from Roof import Roof


class Main:
    def __init__(self):
        self.key2level = {
            keyboard.KeyCode(char='1'): FrontYard(is_night=False),
            keyboard.KeyCode(char='2'): FrontYard(is_night=True),
            keyboard.KeyCode(char='3'): BackYard(is_night=False),
            keyboard.KeyCode(char='4'): BackYard(is_night=True),
            keyboard.KeyCode(char='5'): Roof(is_night=False),
            keyboard.KeyCode(char='6'): Roof(is_night=True),
        }
        self.key_exit = {
            keyboard.Key.esc,
            keyboard.KeyCode(char='q'),
        }
        self.key_modifier = keyboard.Key.alt_l
        self.keys_pressed = set()
        self.keyboard_listener = None
        # keyboard.Listener(on_press=self.keyboard_on_press, on_release=self.keyboard_on_release)
        self.survival = None

    def renew_keyboard_listener(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.keyboard_on_press, on_release=self.keyboard_on_release)

    def keyboard_on_press(self, key):
        self.keys_pressed.add(key)
        if self.key_modifier in self.keys_pressed:
            if key in self.key2level:
                self.survival = self.key2level[key]
                self.survival.main = self
                print(key, self.survival)
                return False
            elif key in self.key_exit:
                # 这里是子线程，无法用 quit() or exit() 结束主线程，
                # 通过设为 None 的方式告知主线程
                self.survival = None
                return False

    def keyboard_on_release(self, key):
        try:
            self.keys_pressed.remove(key)
        except KeyError:
            pass

    def listen(self):
        # 线程不能多次 start，必须重新创建线程对象，否则 raise RuntimeError("threads can only be started once")
        self.renew_keyboard_listener()
        # start() 持续运行，直到 on_press() 或 on_release() 返回 False 时结束
        self.keyboard_listener.start()
        # join() 将销毁线程资源
        self.keyboard_listener.join()

        # 将线程中按了退出键的逻辑推迟至此
        if self.survival is None:
            print('survival is None, exit.')
            Main.play_sound(is_exit=True)
            exit()

        # 监听生存模式
        Main.play_sound(is_start=True)
        self.survival.listen()
        Main.play_sound(is_start=False)

    @staticmethod
    def play_sound(is_start=True, is_exit=False):
        cwd = os.path.dirname(__file__)
        folder = r'.\sounds'
        filename = 'phonograph' if is_exit else 'wakeup' if is_start else 'pause'
        suffix = '.mp3'
        path = os.path.join(cwd, folder, filename + suffix)

        if not os.path.isfile(path):
            print('Invalid sound path: ' + path)
        else:
            try:
                from playsound import playsound
            except ImportError:
                print('No module named `playsound`!')
            else:
                # block=False: 非阻塞播放
                playsound(path, block=is_exit)
                # print('play sound: ' + path)


if __name__ == "__main__":
    print('PvZSurvival listening...')
    main = Main()
    while True:
        main.listen()
