# Main script
import keyboard

from scanner import input_scanner
from playsound import playsound
import tf_nn

from tm_controller import tm_controller


def record_screen_sceonds_batch(seconds, inputscanner, save_path='Training/Level1/'):
    keep_recording = True
    c = 22
    while keep_recording:
        record_screen_seconds(seconds=seconds, inputscanner=inputscanner, name_picture=str(c).zfill(4), path=save_path)
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


def record_screen_seconds(seconds, inputscanner, name_picture='0010_training', path='Training/Level1/'):
    playsound('Assets/Audio/start_recording.mp3')
    inputscanner.record_screen_keyboard_seconds(seconds=seconds, save_in_class=True)
    playsound('Assets/Audio/stop_recording.mp3')
    inputscanner.save_data_at(path=path, name_text_file=name_picture)


def load_nn():
    train_ds, val_ds = tf_nn.load_images('Training/AllLevels')
    # train_ds_2, val_ds_2 = tf_nn.load_images('Training/Level2')
    print(len(train_ds.class_names))
    # nnmodel = tf_nn.NeuralNetworkTrackmania(len(train_ds.class_names), load_model=False)
    nnmodel = tf_nn.NeuralNetworkTrackmania(len(train_ds.class_names), load_model=True, path_to_model='Models/NN')
    nnmodel.train_model(train_ds, val_ds, 10, save_model=True, save_model_path='Models/NN/AllLevels')
    # nnmodel.train_model(train_ds_2, val_ds_2, 25, save_model=True, save_model_path='Models/NN')
    nnmodel.set_labels(train_ds)
    return nnmodel


def controll_trackmania(nnmodel, i_s, seconds):
    tm_con1 = tm_controller()
    tm_con1.control_car(seconds=seconds, nn_model=nnmodel, monitor=i_s.monitor)


def main():
    print("Wuhu")
    i_s = input_scanner(1920, 1080, 0, 0)
    # record_screen_sceonds_batch(inputscanner=i_s, seconds=20, save_path='Training/AllLevels/')
    # can be uncommented if wanted
    nnmodel = load_nn()
    # controll_trackmania(nnmodel=nnmodel, i_s=i_s, seconds=20)
    """"
    train_ds, val_ds = tf_nn.load_images('Assets')
    print(len(train_ds.class_names))
    #nnmodel = tf_nn.NeuralNetworkTrackmania(len(train_ds.class_names), load_model=False)
    nnmodel = tf_nn.NeuralNetworkTrackmania(len(train_ds.class_names), load_model=True, path_to_model='Models/NN')
    nnmodel.train_model(train_ds, val_ds, 100)
    nnmodel.set_labels(train_ds)
    """
    print("-------\nIt works\n-------")


if __name__ == '__main__':
    main()
