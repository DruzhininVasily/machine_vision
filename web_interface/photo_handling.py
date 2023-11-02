import cv2
import os
import numpy as np
from tensorflow import keras
from datetime import datetime as dt
import sqlite3 as sq
# import time


def get_photo(data_pallet, obj):
    # time.sleep(1)
    # Получение изображения с камеры и сохранение его на жесткий диск
    obj.error_camera = False
    try:
        cap = cv2.VideoCapture('rtsp://admin:SLB_123456@192.168.0.64/80/video')
        ret, frame = cap.read()
    except RuntimeError:
        print("Ошибка подключения камеры")
        obj.error_camera = True
    if len(os.listdir('C:/PycharmProjects/Machine_vision/web_interface/static/data')) == 0:
        name = '000001'
    else:
        l = list(map(lambda x: int(x.split('_')[-1][:-4]), os.listdir('C:/PycharmProjects/Machine_vision/web_interface/static/data')))
        name = str(max(l) + 1)
        while len(name) < 5:
            name = '0' + name
    cv2.imwrite("C:/PycharmProjects/Machine_vision/web_interface/static/data/{}.jpg".format(name), frame)
    cap.release()
    # Проверка изображения нейросетью
    check("C:/PycharmProjects/Machine_vision/web_interface/static/data/{}.jpg".format(name), data_pallet, obj)


def check(img_path, pallet, obj):
    model = keras.models.load_model('C:/PycharmProjects/Machine_vision/model_color_0.3')

    test_img = photo_handler(img_path)
    check_result = model.predict(np.array([test_img / 255]))
    now_time = dt.now()
    now_time = now_time.strftime("%Y-%m-%d %H:%M:%S")
    # Сохранение параметров всех фото в БД
    with sq.connect("C:/PycharmProjects/Machine_vision/data_base/trash_pallets.db") as con:
        cur = con.cursor()
        cur.execute("""INSERT INTO pallets (pallet_number, datetime, path, OK, NOT_OK) VALUES (?, ?, ?, ?, ?)""",
                    (pallet, now_time, img_path, round(float(check_result[0][0]), 3), round(float(check_result[0][1]), 3)))
    # Сохранение параметров фото с заливом в БД
    if check_result[0][1] > 0.7:
        # Блокировка паллеты (plc_interaction --> PlcClient ---> blocking_pallet)
        obj.blocking_pallet()
        with sq.connect("C:/PycharmProjects/Machine_vision/data_base/trash_pallets.db") as con:
            cur = con.cursor()
            cur.execute("""INSERT INTO trash (pallet_number, datetime, path, OK, NOT_OK) VALUES (?, ?, ?, ?, ?)""",
                        (pallet, now_time, img_path, round(float(check_result[0][0]), 3),
                         round(float(check_result[0][1]), 3)))
    # Запись сигнала о завершении работы с изображением (plc_interaction --> PlcClient ---> camera_shot)
    obj.camera_shot()


def photo_handler(path):
    # Приведение изображения к виду используемого в нейросети
    frame = cv2.imread(path)
    # Сжатие изображения
    frame = cv2.resize(frame, (400, 400))
    # Cоздание шаблона обрезки
    blank = np.zeros(frame.shape[:2], dtype='uint8')
    square = cv2.rectangle(blank, (60, 45), (340, 325), 255, -1)
    # Обрезка операцией "И"
    crop_color = cv2.bitwise_and(frame, frame, mask=square)

    (x, y) = np.where(square == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    # Обрезка полей изображения
    output_color = crop_color[x1:x2, y1:y2]
    return output_color

