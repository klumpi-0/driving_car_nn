# Main script

from scanner import input_scanner
import tf_nn
from tm_controller import tm_controller


def load_nn():
    train_ds, val_ds = tf_nn.load_images('../Training/Level1Big')
    # train_ds_2, val_ds_2 = tf_nn.load_images('Training/Level2')
    print(len(train_ds.class_names))
    # nnmodel = tf_nn.NeuralNetworkTrackmania(len(train_ds.class_names), load_model=False, input_picture_shape=(270, 480))
    nnmodel = tf_nn.NeuralNetworkTrackmania(len(train_ds.class_names), load_model=True, path_to_model='../Training/Level1Big/NN')
    # nnmodel.train_model(train_ds, val_ds, 15, save_model=True, save_model_path='Training/Level1Big/NN')
    # nnmodel.train_model(train_ds_2, val_ds_2, 25, save_model=True, save_model_path='Models/NN')
    nnmodel.set_labels(train_ds)
    return nnmodel


def controll_trackmania(nnmodel, i_s, seconds, use_canny, image_width, image_height):
    tm_con1 = tm_controller()
    if use_canny:
        tm_con1.control_car_canny(seconds=seconds, nn_model=nnmodel, monitor=i_s.monitor)
    else:
        tm_con1.control_car(seconds=seconds, nn_model=nnmodel, monitor=i_s.monitor, image_width=image_width, image_height=image_height)


def main():
    print("Wuhu")
    i_s = input_scanner(1920, 1080, 0, 0)
    i_s.record_screen_seconds_batch_save(seconds=20, starting_number_batch=20, save_path='../Training/Level1Big', edge=False, output_widht=480, output_height=270)
    # can be uncommented if wanted
    # nnmodel = load_nn()
    # controll_trackmania(nnmodel=nnmodel, i_s=i_s, seconds=20, use_canny=False, image_width=480, image_height=270)
    print("-------\nIt works\n-------")


if __name__ == '__main__':
    main()
