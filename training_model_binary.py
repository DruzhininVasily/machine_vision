import numpy as np
import os
import cv2
import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D

#print(tf.config.list_physical_devices('GPU'))

data_set = []

print("Подготовка данных............")
# Загружаем фото в датасет
for image in os.listdir('data_binary/OK'):
    data_set.append([cv2.imread('data_binary/OK/{}'.format(image)), [1, 0]])

for image in os.listdir('data_binary/NOT_OK'):
    data_set.append([cv2.imread('data_binary/NOT_OK/{}'.format(image)), [0, 1]])
# Распределяем данные случайным образом
np.random.shuffle(data_set)

x_train = []
y_train = []
# Создаём обучающую выборку с соответствующими ожидаемыми выходными данными
for i in data_set:
    x_train.append(i[0])
    y_train.append(i[1])

x_train = np.array(x_train)
y_train = np.array(y_train)

print('Создание модели............')
# Создаём модель нейросети
model = keras.Sequential([
    Conv2D(16, (3, 3), padding='same', activation='relu', input_shape=(280, 280, 3)),
    Conv2D(16, (3, 3), padding='same', activation='relu'),
    MaxPooling2D((2, 2), strides=2),
    Conv2D(32, (3, 3), padding='same', activation='relu'),
    Conv2D(32, (3, 3), padding='same', activation='relu'),
    MaxPooling2D((2, 2), strides=2),
    Conv2D(64, (3, 3), padding='same', activation='relu'),
    Conv2D(64, (3, 3), padding='same', activation='relu'),
    MaxPooling2D((2, 2), strides=2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(2, activation='softmax')
])
# model = keras.Sequential([
#     Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(280, 280, 3)),
#     MaxPooling2D((2, 2), strides=2),
#     Conv2D(64, (3, 3), padding='same', activation='relu'),
#     MaxPooling2D((2, 2), strides=2),
#     Flatten(),
#     Dense(128, activation='relu'),
#     Dense(2, activation='softmax')
# ])
print(model.summary())

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

his = model.fit(x_train, y_train, batch_size=16, epochs=5, validation_split=0.2)

test_img = cv2.imread('data_binary/00008.jpg')
print(model.predict(np.array([test_img])))
test_img1 = cv2.imread('data_binary/00009.jpg')
print(model.predict(np.array([test_img1])))