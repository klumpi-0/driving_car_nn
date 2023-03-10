import cv2
import numpy
import tensorflow as tf


def load_images(image_path):
    """
    Creates an training and validation dataset
    :param image_path: Place where images are stored in their class folders
    :return: training dataset and validation dataset
    """
    batch_size = 20
    image_width = 480
    image_height = 270
    train_ds = tf.keras.utils.image_dataset_from_directory(
        image_path,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(image_height, image_width),
        color_mode='grayscale',
        batch_size=batch_size
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        image_path,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(image_height, image_width),
        color_mode='grayscale',
        batch_size=batch_size
    )
    # print(train_ds.class_names)
    return train_ds, val_ds


class NeuralNetworkTrackmania:
    def __init__(self, number_outputs, load_model=False, path_to_model='', input_picture_shape=(135, 240)):
        print("Start creating a model...")
        if load_model:
            self.model = tf.keras.models.load_model(path_to_model)
            print("Loaded model from ", path_to_model)
        else:
            self.model = self.create_nn_model(number_outputs, input_picture_shape=input_picture_shape)
            print("Created model")
        self.labels = []

    def create_nn_model(self, number_outputs, input_picture_shape=(135, 240)):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(270,480)),
            tf.keras.layers.Rescaling(1. / 255),
            tf.keras.layers.Dense(128),
            tf.keras.layers.Dense(64),
            tf.keras.layers.Dense(32),
            tf.keras.layers.Dense(number_outputs)
        ])
        return model

    def train_model(self, train_ds, val_ds, epochs_, save_model=False, save_model_path=''):
        print("Train model...")
        self.model.compile(
            optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy']
        )
        self.model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs_
        )
        if save_model:
            print("Saved model at:", save_model_path)
            tf.keras.models.save_model(model=self.model, filepath=save_model_path)

    def check_single_picture_disk(self, picture_path):
        """
        Gives output of NN with given picture
        :param picture_path: where picture is stored
        :return:the label of the given class
        """
        data = numpy.expand_dims(cv2.cvtColor(cv2.imread(picture_path), cv2.COLOR_BGR2GRAY), axis=0)
        output = self.model.predict(data)
        max_value_index = numpy.argmax(output[0])
        label = self.labels[max_value_index]
        return label

    def check_single_picture(self, picture):
        """
        Gives output of NN with given picture
        :param picture_path: where picture is stored
        :return:the label of the given class
        """
        data = numpy.expand_dims(cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY), axis=0)
        output = self.model.predict(data)
        max_value_index = numpy.argmax(output[0])
        label = self.labels[max_value_index]
        return label

    def check_single_picture_canny(self, picture):
        """
        Gives output of NN with given picture
        :param picture_path: where picture is stored
        :return:the label of the given class
        """
        data = numpy.expand_dims(cv2.Canny(cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY), threshold1=100, threshold2=100), axis=0)
        output = self.model.predict(data)
        max_value_index = numpy.argmax(output[0])
        label = self.labels[max_value_index]
        return label

    def create_and_train_model(self, path_to_data, save_model_path, save_model=True, get_labels=False):
        """
        Creates amd trains a model
        :param get_labels: True if you want to get possible output labels as return
        :param path_to_data: where the training data is stored
        :param save_model_path: where the model should be saved
        :param save_model:if the model should be saved
        :return: Returns the model and a list with all possible labels
        """
        print("Start creating and training model...")
        train_ds, val_ds = load_images(path_to_data)
        print("val_ds \n", val_ds)
        model = self.create_nn_model(16)
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
        if save_model:
            print("Saved model at:", save_model_path)
            tf.keras.models.save_model(model=model, filepath=save_model_path)
        if get_labels:
            return model, train_ds.class_names
        else:
            return model

    def set_labels(self, train_ds):
        self.labels = train_ds.class_names
