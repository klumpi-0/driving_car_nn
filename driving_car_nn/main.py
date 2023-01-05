# Main script
import time

import cv2
import numpy
from mss import mss

from scanner import input_scanner
from keyboard_recorder import keyboard_recorder
import keyboard
import cv2 as cv


def print_switcher(input):
    output = ""
    tmp = ""
    tmp = "x" if input["up"] else "_"
    output += tmp
    tmp = "x" if input["left"] else "_"
    output += tmp
    tmp = "x" if input["down"] else "_"
    output += tmp
    tmp = "x" if input["right"] else "_"
    output += tmp
    return output


time.sleep(4)

i_s = input_scanner(1000, 1000, 0, 0)
i_s.record_screen_keyboard_seconds(100, True)
for i in range(len(i_s.current_save)):
    print(i, print_switcher(i_s.current_save[i][1]))
# kr = keyboard_recorder()
# kr.record_keys()
# for i in range(100):
#    kr.on_press()

# i_s.record_keyboard(2, True, 'p')
# i_s.record_screen_keyboard(True, "esc", "p")
# print(len(i_s.current_save))
# cv.imshow("Name 0", i_s.current_save[4][0])
# i_s.record_screen_keyboard(True, "p", "u ")
