# Main script
import time

from scanner import input_scanner
from keyboard_recorder import keyboard_recorder
import cv2 as cv

i_s = input_scanner(1000, 1000, 0, 0)
kr = keyboard_recorder()

for i in range(100):
    kr.on_press()

#i_s.record_keyboard(2, True, 'p')
#i_s.record_screen_keyboard(True, "esc", "p")
#print(len(i_s.current_save))
#cv.imshow("Name 0", i_s.current_save[4][0])
#i_s.record_screen_keyboard(True, "p", "u ")