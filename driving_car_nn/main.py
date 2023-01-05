# Main script
import time

import numpy
from mss import mss

from scanner import input_scanner
from keyboard_recorder import keyboard_recorder
import keyboard
import cv2 as cv

time.sleep(4)
screenshot = []
c = 0
monitor = {"top": 0, "left": 0, "width": 1000, "height": 1000}

print("Start recording")
with mss() as sct:
    for _ in range(1000):
        key_dict = {
            "up": keyboard.is_pressed("w"),
            "left": keyboard.is_pressed("a"),
            "down": keyboard.is_pressed("s"),
            "right": keyboard.is_pressed("d"),
            "number": c
        }
        screenshot.append([numpy.array(sct.grab(monitor)), key_dict])
        c = c + 1
        print(c, " picture taken")

print(screenshot[999][1])
# i_s = input_scanner(1000, 1000, 0, 0)
# kr = keyboard_recorder()
# kr.record_keys()
# for i in range(100):
#    kr.on_press()

# i_s.record_keyboard(2, True, 'p')
# i_s.record_screen_keyboard(True, "esc", "p")
# print(len(i_s.current_save))
# cv.imshow("Name 0", i_s.current_save[4][0])
# i_s.record_screen_keyboard(True, "p", "u ")
