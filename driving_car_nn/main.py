# Main script
import time

from scanner import input_scanner
import cv2 as cv

i_s = input_scanner(1000, 1000, 0, 0)
#test = i_s.record_screen_seconds(100, save_in_class=True)
#print(type(test[0]))
#cv.imshow("Name0", test[0])
#cv.waitKey(0)
#cv.imshow("Name1", test[99])
#cv.waitKey(0)
#cv.imshow("Last Picture", i_s.get_current_save()[59])
#cv.waitKey(0)
#cv.destroyAllWindows()

#i_s.record_keyboard(2, True, 'p')
#i_s.record_screen_keyboard(True, "esc", "p")
#print(len(i_s.current_save))
#cv.imshow("Name 0", i_s.current_save[4][0])
i_s.record_screen_keyboard(True, "p", "u ")