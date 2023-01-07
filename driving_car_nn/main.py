# Main script
import time

import cv2
import numpy
from mss import mss

from scanner import input_scanner
import tf_nn


from tm_controller import tm_controller

def record_screen_seconds(seconds):



def main():
    print("Wuhu")
    i_s = input_scanner(1920, 1080, 0, 0)

    train_ds, val_ds = tf_nn.load_images('Assets')
    print(len(train_ds.class_names))
    #nnmodel = tf_nn.NeuralNetworkTrackmania(len(train_ds.class_names), load_model=False)
    nnmodel = tf_nn.NeuralNetworkTrackmania(len(train_ds.class_names), load_model=True, path_to_model='Models/NN')
    nnmodel.train_model(train_ds, val_ds, 100)
    nnmodel.set_labels(train_ds)
    print(nnmodel.check_single_picture_disk('Assets/___x/image_training_grey123.jpg'))
    print("-------\nIt workes\n-------")
    tm_con1 = tm_controller()
    tm_con1.control_car(seconds=10, nn_model=nnmodel, monitor=i_s.monitor)



if __name__ == '__main__':
    main()

