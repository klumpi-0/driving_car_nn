# Class which can record the screen at the inputs on the keyboard at the same time
from mss import mss
import numpy
import keyboard
import time


class input_scanner:
    def __init__(self, width_, height_, top_, left_):
        """
        Creates a scanner which records the screen and teh input on the keyboard
        :param width_: x-size
        :param height_: y-size
        :param top_: y-postion
        :param left_:x-position
        """
        self.width = width_
        self.height = height_
        self.top = top_
        self.left = left_
        self.current_save = []
        self.is_recording = False
        self.monitor = {"top": self.top, "left": self.left, "width": self.width, "height": self.height}
        print("Created a scanner from size: ", self.width, self.height)

    def record_screen_seconds(self, seconds, save_in_class):
        screenshots = []
        monitor = {"top": self.top, "left": self.left, "width": self.width, "height": self.height}
        with mss() as sct:
            for _ in range(seconds):
                screenshots.append(numpy.array(sct.grab(monitor)))
        if save_in_class:
            self.current_save = screenshots
        return screenshots

    def record_screen_keyboard(self, save_in_class, start_key, stop_key):
        print("Start recording at the moment [", start_key, "]key is pressed")
        keyboard.wait(start_key)
        print("Start recording...")
        self.is_recording = True
        with mss() as sct:
            while self.is_recording:
                if keyboard.read_key() == stop_key:
                    self.is_recording = False
                if keyboard.read_key() == "w":
                    self.current_save.append([numpy.array(sct.grab(self.monitor)), "w"])
                elif keyboard.read_key() == "a":
                    self.current_save.append([numpy.array(sct.grab(self.monitor)), "a"])
                elif keyboard.read_key() == "s":
                    self.current_save.append([numpy.array(sct.grab(self.monitor)), "s"])
                elif keyboard.read_key() == "d":
                    self.current_save.append([numpy.array(sct.grab(self.monitor)), "s"])
                else:
                    self.current_save.append([numpy.array(sct.grab(self.monitor)), "nothing"])
        print("Stopped recording")

    def save_screenshot_button(self, button):
        with mss() as sct:
            print("Picture taken for:", button)
            self.current_save.append([numpy.array(sct.grab(self.monitor)), button])

    def create_screenshot(self, save_in_class):
        """
        Returns screenshot of selected monitor
        :param save_in_class:
        :return:
        """
        with mss() as sct:
            screenshot_ = numpy.array(sct.grab(self.monitor))
            if save_in_class:
                self.current_save.append(screenshot_)
        return screenshot_

    def grab_keyboard_input(self):
        if keyboard.read_key() == "w":
            return "w"
        elif keyboard.read_key() == "a":
            return "a"
        elif keyboard.read_key() == "s":
            return "s"
        elif keyboard.read_key() == "d":
            return "d"
        else:
            return "nothing"

    def record_keyboard(self, seconds, save_in_class, stop_key):
        print("Start recording of keyboard...")
        keyboard_inputs = keyboard.record(until=stop_key)
        keyboard.press(stop_key)
        print("\nRecording is finished")
        if save_in_class:
            self.current_save = keyboard_inputs
        return keyboard_inputs

    def start_recording(self, stop_key):
        """
        Starts recording of keyboard and set screen-parameters
        """
        print("Start Recording...")
        datapackage = []
        self.is_recording = True
        while self.is_recording:
            print("entering loop")
            save_data = [self.create_screenshot(False), self.grab_keyboard_input()]
            print("Pressed key:", save_data[1])
            self.should_stop_recording(stop_key)
            print("still recording")

    def stop_recording(self):
        """
        Used to stop recording of recorder
        :return:
        """
        print("Stop recording")
        self.is_recording = True

    def should_stop_recording(self, stop_button):
        """
        Returns true if program should stop recording
        :return:
        """
        if keyboard.read_key() == stop_button:
            print("Stop recording")
            self.is_recording = False
            return True
        return False

    def get_current_save(self):
        return self.current_save
