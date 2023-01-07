import cv2
import numpy
import tensorflow as tf


# does not work
def parse_function(filename, label):
    image_string = tf.read_file("Assets/" + filename)
    image_decode = tf.image.decode_jpeg(image_string, channels=1)
    image = tf.cast(image_decode, tf.float32)
    return image, label


# does not work
def create_dataset(data, recorder, label_txt):
    list_filenames = []
    list_labels = []
    label_file = open(label_txt, 'r')
    Lines = label_file.readlines()

    # Create list filled with the picture names and labels
    for line in Lines:
        tmp = []
        for letter in line:
            tmp.append(True if letter == 'x' else False)
        list_labels.append(tmp)
    for i in range(len(recorder.current_save)):
        list_filenames.append('image_training_grey' + str(i) + '.jpg')

    filenames = tf.constant(list_filenames)
    labels = tf.constant(list_labels)

    dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))

    dataset = dataset.map(parse_function)
    dataset = dataset.batch(2)

    iterator = dataset.make_one_shot_iterator()


def load_images(image_path):
    """
    Creates an training and validation dataset
    :param image_path: Place where images are stored in their class folders
    :return: training dataset and validation dataset
    """
    batch_size = 20
    image_width = 240
    image_height = 135
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
    def __init__(self, number_outputs, load_model=False, path_to_model=''):
        print("Start creating a model...")
        if load_model:
            self.model = tf.keras.models.load_model(path_to_model)
            print("Loaded model from ", path_to_model)
        else:
            self.model = self.create_nn_model(number_outputs)
            print("Created model")
        self.labels = []

    def create_nn_model(self, number_outputs):
        model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(135, 240)),
            tf.keras.layers.Rescaling(1. / 255),
            tf.keras.layers.Dense(128),
            tf.keras.layers.Dense(64),
            tf.keras.layers.Dense(32),
            tf.keras.layers.Dense(number_outputs)
        ])
        return model

    def train_model(self, train_ds, val_ds, epochs_):
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

    def check_single_picture(self, picture_path):
        data = numpy.expand_dims(cv2.cvtColor(cv2.imread(picture_path), cv2.COLOR_BGR2GRAY), axis=0)
        output = self.model.predict(data)
        # output = numpy.sort(output)
        print("Output for ", picture_path, " ", output)
        return output

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
