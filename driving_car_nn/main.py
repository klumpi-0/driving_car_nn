# Main script
import time

import cv2
import numpy
from mss import mss

from scanner import input_scanner
import tf_nn
import tensorflow as tf
from keyboard_recorder import keyboard_recorder
import keyboard
import cv2 as cv



#i_s.record_screen_keyboard_seconds(1000, True)
#i_s.save_data_at('Assets/', 'input_string')


def create_and_train_model():
    train_ds, val_ds = tf_nn.load_images('Assets')
    model = tf_nn.create_nn_model(16)
    # tf.keras.models.save_model(model=model, filepath='Assets')
    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )
    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=20
    )
    model.summary()
    tf.keras.models.save_model(model=model, filepath='Models/NN')
    return model


def main():
    print("Wuhu")
    i_s = input_scanner(1920, 1080, 0, 0)

    train_ds, val_ds = tf_nn.load_images('Assets')
    print(len(train_ds.class_names))
    nnmodel = tf_nn.NeuralNetworkTrackmania(len(train_ds.class_names), load_model=False)
    nnmodel.train_model(train_ds, val_ds, 20)
    nnmodel.set_labels(train_ds)
    nnmodel.check_single_picture('Assets/___x/image_training_grey123.jpg')
    print("-----\nIt workes\n-------")

    #model = create_train_model()
    #model = tf_nn.create_and_train_model(path_to_data='Assets', save_model=False, save_model_path='Models/NN')
    """"
    model = tf.keras.models.load_model('Models/NN')
    data = (cv2.imread('Assets/_x__/image_training_grey168.jpg'))
    data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
    data = numpy.expand_dims(data, axis=0)
    print("data ", data.shape)
    output = model.predict(data)
    print(output)
    """
    #output2 = tf_nn.check_single_picture(model, 'Assets/_x__/image_training_grey168.jpg')



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
