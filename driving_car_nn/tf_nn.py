import tensorflow as tf

def parse_function(filename, label):
    image_string = tf.read_file("Assets/" + filename)
    image_decode = tf.image.decode_jpeg(image_string, channels=1)
    image = tf.cast(image_decode, tf.float32)
    return image, label

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
    batch_size = 20
    image_width = 240
    image_height = 135
    train_ds = tf.keras.utils.image_dataset_from_directory(
        image_path,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(image_height, image_width),
        batch_size=batch_size
    )
    val_ds = tf.keras.utils.image_dataset_from_directory(
        image_path,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(image_height, image_width),
        batch_size=batch_size
    )
    print(train_ds.class_names)


