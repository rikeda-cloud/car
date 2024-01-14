# Copyright (c) 2021 Takenoshin
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import time
import os
from decimal import Decimal
import pygame
import Adafruit_PCA9685
from multiprocessing import Value, Process
from json_buffer import JsonBuffer

MAX_SPEED = 370
MIN_SPEED = 350

MAX_HANDLE = 450
MIN_HANDLE = 270

os.environ["SDL_VIDEODRIVER"] = "dummy"


def change_var(var, diff, max, min):
    if min < var + diff and var + diff < max:
        return var + diff
    return min if var + diff <= min else max


def joystick_control(handle, speed, is_measure) -> None:
    j = JsonBuffer()
    pwm = Adafruit_PCA9685.PCA9685(address=0x40)
    pwm.set_pwm_freq(60)
    #モーター
    pwm.set_pwm(14, 0, speed.value)
    #ハンドル
    pwm.set_pwm(15, 0, handle.value)

    pygame.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()
    try:
        n_btn = joy.get_numbuttons()
        n_axe = joy.get_numaxes()
        n_hat = joy.get_numhats()
        print("Joystick Name: " + joy.get_name())

        pygame.event.get()
        s_btn = [0] * n_btn
        s_axe = [0.0] * n_axe
        s_hat = [0] * n_hat
        while True:
            # Buttons
            for i in range(n_btn):
                s_btn[i] = joy.get_button(i)
            # Axes
            for i in range(n_axe):
                #s_axe[i] = round(joy.get_axis(i), 2)
                s_axe[i] = float(Decimal(joy.get_axis(i)).quantize(Decimal('0.01')))
            # Hats
            for i in range(n_hat):
                s_hat[i] = joy.get_hat(i)

            # コントローラLBでデータ取得スイッチをon
            if s_btn[4] == 1:
                is_measure.value = 1
            # コントローラRBでデータ取得スイッチをoff
            if s_btn[5] == 1:
                is_measure.value = 0
            
            if s_btn[6] == 1:
                j.del_newest_file()

            if s_btn[2] == 1:
                diff = -1 if speed.value != MAX_SPEED else -10
                speed.value = change_var(speed.value, diff, MAX_SPEED, MIN_SPEED)
            elif s_btn[1] == 1:
                speed.value = change_var(speed.value, 5, MAX_SPEED, MIN_SPEED)
            else:
                speed.value = change_var(speed.value, 1, MAX_SPEED, MIN_SPEED)
            pwm.set_pwm(14, 0, speed.value)

            handle.value = int(360 + s_axe[0] * 70)
            pwm.set_pwm(15, 0, handle.value)
            
            #pygame.event.pump()
            pygame.event.get()

            #print(handle.value, speed.value)
            time.sleep(0.1)
    except( KeyboardInterrupt, SystemExit): # Exit with Ctrl-C
        print("Exit")


class JoystickControl():
    def __init__(self):
        self.speed = Value('i', 370)
        self.handle = Value('i', 360)
        self.is_measure = Value('i', 0)
        self.process = Process(target=joystick_control, args=[self.handle, self.speed, self.is_measure])
        self.process.start()

    def __del__(self):
        self.process.join()


from multiprocessing import Value
if __name__ == "__main__":
    handle = Value('i', 360)
    speed = Value('i', 370)
    is_measure = Value('i', 0)
    joystick_control(handle, speed, is_measure)
