# Main script
import time

import cv2
import numpy
from mss import mss

from scanner import input_scanner
import tf_nn
from keyboard_recorder import keyboard_recorder
import keyboard
import cv2 as cv



#i_s.record_screen_keyboard_seconds(1000, True)
#i_s.save_data_at('Assets/', 'input_string')

def main():
    print("Wuhu")
    i_s = input_scanner(1920, 1080, 0, 0)
    tf_nn.load_images('Assets')


if __name__ == '__main__':
    main()
# kr = keyboard_recorder()
# kr.record_keys()
# for i in range(100):
#    kr.on_press()

# i_s.record_keyboard(2, True, 'p')
# i_s.record_screen_keyboard(True, "esc", "p")
# print(len(i_s.current_save))
# cv.imshow("Name 0", i_s.current_save[4][0])
# i_s.record_screen_keyboard(True, "p", "u ")
