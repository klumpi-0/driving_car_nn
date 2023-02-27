# Class which can record the screen at the inputs on the keyboard at the same time
import cv2
from mss import mss
from playsound import playsound
import numpy
import keyboard
import time


class input_scanner:
    def __init__(self, width_, height_, top_, left_):
        """
        Creates a scanner which records the screen and teh input on the keyboard
        :param width_: x-size
        :param height_: y-size
        :param top_: y-position
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

    def record_screen_keyboard_seconds(self, seconds, save_in_class):
        """
        Records screen and keyboard fpr given time
        :param seconds: length of recording in seconds
        :param save_in_class: if it should be saved in the class
        :return: recorded data
        """
        print("Start recording screen and keyboard in 3 seconds")
        time.sleep(3)
        screenshots = []
        c = 0
        t_end = time.time() + seconds
        print("Start recording...")
        playsound('Assets/Audio/b.mp3')
        with mss() as sct:
            while time.time() < t_end:
                key_dict = {
                    "up": keyboard.is_pressed("w"),
                    "left": keyboard.is_pressed("a"),
                    "down": keyboard.is_pressed("s"),
                    "right": keyboard.is_pressed("d")
                }
                screenshots.append([numpy.array(sct.grab(self.monitor)), key_dict])
                print(c, " picture")
                c = c + 1
                if keyboard.is_pressed("right shift"):
                    print("Break recording early...")
                    break
        if save_in_class:
            self.current_save = screenshots
        print("Stop recording")
        return screenshots

    def save_data_at(self, path, name_text_file, output_widht=240, output_height=135):
        """
        Works only if data is stored in list with entries: [picture, dictionary pressed keys]
        :param name_text_file: How to name the txt file
        :param path: Where to save the recorded data
        :return:
        """
        print("Start saving data")
        with open(path + name_text_file + '.txt', 'w') as f:
            for i in range(len(self.current_save)):
                if i % 100 == 0:
                    cv2.imwrite(path + "image_training_original" + str(i) + ".jpg", self.current_save[i][0])
                cv2.imwrite(
                    path + "/" +
                    self.switch_dictionary_to_string(self.current_save[i][1]) + "/" +
                    name_text_file + "_" + str(i) + ".jpg",
                    cv2.resize(cv2.cvtColor(self.current_save[i][0], cv2.COLOR_BGR2GRAY), (output_widht, output_height)))
                f.write(self.switch_dictionary_to_string(self.current_save[i][1]) + "\n")
        print("Finished saving data")


    def save_data_at_canny_edge_gradient(self, path, name_text_file, output_widht=240, output_height=135):
        print("Start saving data")
        with open(path + name_text_file + '.txt', 'w') as f:
            for i in range(len(self.current_save)):
                if i % 100 == 0:
                    cv2.imwrite(path + "image_training_original" + str(i) + ".jpg", self.current_save[i][0])
                cv2.imwrite(
                    path + "/" +
                    self.switch_dictionary_to_string(self.current_save[i][1]) + "/" +
                    name_text_file + "_" + str(i) + ".jpg",
                    cv2.resize(cv2.Canny((cv2.cvtColor(self.current_save[i][0], cv2.COLOR_BGR2GRAY)), threshold1=100, threshold2=100), (output_widht, output_height)))
                f.write(self.switch_dictionary_to_string(self.current_save[i][1]) + "\n")
        print("Finished saving data")

    def switch_dictionary_to_string(self, input_):
        output = ""
        tmp = ""
        tmp = "x" if input_["up"] else "_"
        output += tmp
        tmp = "x" if input_["left"] else "_"
        output += tmp
        tmp = "x" if input_["down"] else "_"
        output += tmp
        tmp = "x" if input_["right"] else "_"
        output += tmp
        return output

    def get_current_save(self):
        return self.current_save


    def record_screen_seconds_batch_save(self, seconds, starting_number_batch, save_path, edge, output_widht=240, output_height=135):
        """
        Records screen and keyboard in batch mode for seconds
        :param seconds: How many each video should record
        :param starting_number_batch: with which number the each batch should start saving the pictures (dont use same number twice)
        :param save_path: where the pictures should be saved
        :return: nothing
        """
        keep_recording = True
        c = starting_number_batch
        while keep_recording:
            self.record_screen_seconds_save(seconds=seconds, name_picture=str(c).zfill(4), save_path=save_path, edge=edge, output_widht=output_widht, output_height=output_height)
            playsound('Assets/Audio/press_o_to.mp3')
            while True:
                if keyboard.is_pressed("o"):
                    keep_recording = True
                    break
                if keyboard.is_pressed("l"):
                    keep_recording = False
                    playsound('Assets/Audio/stoping_session.mp3')
                    break
            c = c + 1

    def record_screen_seconds_save(self, seconds, name_picture, save_path, edge, output_widht=240, output_height=135):
        """
        Records and saves the screen and keys
        :param edge: if we want to use edge detection
        :param seconds:
        :param name_picture:
        :param save_path:
        :return:
        """
        playsound('Assets/Audio/start_recording.mp3')
        self.record_screen_keyboard_seconds(seconds=seconds, save_in_class=True)
        playsound('Assets/Audio/stop_recording.mp3')
        if edge:
            self.save_data_at_canny_edge_gradient(path=save_path, name_text_file=name_picture, output_widht=output_widht, output_height=output_height)
        else:
            self.save_data_at(path=save_path, name_text_file=name_picture, output_widht=output_widht, output_height=output_height)