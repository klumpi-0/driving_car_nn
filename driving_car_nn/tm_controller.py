import ctypes
import time

import cv2
import keyboard
import numpy
from mss import mss

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


class tm_controller:
    def __init__(self):
        print("Creating a controller for Trackmania")
        self.list_all_keys = [0x11, 0x1E, 0x1F, 0x20]
        self.key_w = 0x11
        self.key_a = 0x1E
        self.key_s = 0x1F
        self.key_d = 0x20

    def control_car(self, seconds, nn_model, monitor):
        print("Start controlling car in 3 seconds\nEnds in ", seconds, " seconds or by pressing shift")
        time.sleep(3)
        print("Controlling car")
        t_end = time.time() + seconds
        with mss() as sct:
            while time.time() < t_end:
                if keyboard.is_pressed("right shift"):
                    print("Stop controlling early...")
                    break
                # create picture of screen
                screenshot = numpy.array(sct.grab(monitor))
                screenshot = cv2.resize((screenshot), (240, 135))
                # send picture into nn
                label_action = nn_model.check_single_picture(screenshot)
                # press buttons according to action
                for button in self.list_all_keys:
                    ReleaseKey(button)
                for i in range(len(label_action)):
                    if label_action[i] == 'x':
                        PressKey(self.list_all_keys[i])
