"""
Class which is used for Bildverarbeitung steps.
Such as greyscalling, downsizing, edgedetection and flood fill
"""
import numpy
import cv2
from collections import deque


def point_in_picture(position_point, size_picture):
    return True if size_picture[0] > position_point[0] >= 0 and size_picture[1] > position_point[1] >= 0 else False


def floodfill(picture_path, seedpoint, homogenitycondition):
    picture = cv2.cvtColor(cv2.imread(picture_path), cv2.COLOR_BGR2GRAY)
    pic_size = picture.shape
    map = numpy.zeros(pic_size)
    seedvalue = picture[seedpoint[0], seedpoint[1]]
    print("Seedvalue", seedvalue)
    q = deque()
    q.append(seedpoint)
    while len(q) != 0:
        point_to_check = q.popleft()
        # print("Calc", picture[point_to_check[0], point_to_check[1]], " - ", seedvalue, " = ", abs(int(picture[point_to_check[0]][point_to_check[1]]) - int(seedvalue)))
        if (point_in_picture(point_to_check, pic_size)) and (
                homogenitycondition >= abs(int(picture[point_to_check[0]][point_to_check[1]]) - int(seedvalue))) and (
                map[point_to_check[0]][point_to_check[1]] == 0):
            print("Set 1 for point", point_to_check)
            map[point_to_check[0], point_to_check[1]] = 255
            q.append([point_to_check[0] + 1, point_to_check[1] + 0])
            q.append([point_to_check[0] + 0, point_to_check[1] + 1])
            q.append([point_to_check[0] - 1, point_to_check[1] + 0])
            q.append([point_to_check[0] + 0, point_to_check[1] - 1])
    return map


pic = cv2.cvtColor(cv2.imread('C:/Jonas/Python/Projects/driving_car_nn/Assets/x___/image_training_grey105.jpg'),
                   cv2.COLOR_BGR2GRAY)

floodp = floodfill('C:/Jonas/Python/Projects/driving_car_nn/Assets/x___/image_training_grey105.jpg', [75, 120], 10)
cv2.imwrite('../Assets/FloodFill/test.png', floodp)
print(floodp[120][65])
# cv2.imshow('Hey', "Assets/FloodFill/test.png")
