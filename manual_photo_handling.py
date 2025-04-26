import cv2
import numpy as np
import os


def naming(path):
    if len(os.listdir(path)) == 0:
        name = '000001'
    else:
        l = list(map(lambda x: int(x.split('_')[-1][:-4]), os.listdir(path)))
        name = str(max(l) + 1)
        while len(name) < 5:
            name = '0' + name
    return name


def photo_handler(path):

    frame = cv2.imread(path)

    frame = cv2.resize(frame, (400, 400))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blank = np.zeros(frame.shape[:2], dtype='uint8')
    square = cv2.rectangle(blank, (60, 45), (340, 325), 255, -1)

    crop_color = cv2.bitwise_and(frame, frame, mask=square)
    crop_gray = cv2.bitwise_and(gray, gray, mask=square)

    (x, y) = np.where(square == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))

    output_color = crop_color[x1:x2, y1:y2]
    output_gray = crop_gray[x1:x2, y1:y2]

    output_binary = cv2.GaussianBlur(output_gray, (5, 5), 0)
    output_binary = cv2.Canny(output_binary, 100, 100)

    return [output_color, output_gray, output_binary]


for i in os.listdir("data_photo_split/OK"):
    output = photo_handler("data_photo_split/OK/{}".format(i))
    cv2.imwrite("data_color/OK/{}.jpg".format(naming("data_color/OK")), output[0])
    cv2.imwrite("data_gray/OK/{}.jpg".format(naming("data_gray/OK")), output[1])
    cv2.imwrite("data_binary/OK/{}.jpg".format(naming("data_binary/OK")), output[2])

for i in os.listdir("data_photo_split/NOT_OK"):
    output = photo_handler("data_photo_split/NOT_OK/{}".format(i))
    cv2.imwrite("data_color/NOT_OK/{}.jpg".format(naming("data_color/NOT_OK")), output[0])
    cv2.imwrite("data_gray/NOT_OK/{}.jpg".format(naming("data_gray/NOT_OK")), output[1])
    cv2.imwrite("data_binary/NOT_OK/{}.jpg".format(naming("data_binary/NOT_OK")), output[2])



