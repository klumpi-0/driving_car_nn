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


def create_train_model():
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
    #model = create_train_model()
    model = tf.keras.models.load_model('Models/NN')
    #print(model.summary())
    data = (cv2.imread('Assets/___x/image_training_grey123.jpg'))
    data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
    #data = cv2.resize(data, (135, 240))
    data = numpy.expand_dims(data, axis=0)
    #data = numpy.expand_dims(data, axis=-1)
    #print("Shape ", data.shape)
    print("data ", data.shape)
    output = model.predict(data)
    print(output)



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
