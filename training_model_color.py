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
for image in os.listdir('data_color/OK'):
    img = cv2.imread('data_color/OK/{}'.format(image))
    data_set.append([img, [1, 0]])
    # img = cv2.rotate(img, cv2.ROTATE_180
    # data_set.append([img, [1, 0]])

for image in os.listdir('data_color/NOT_OK'):
    img = cv2.imread('data_color/NOT_OK/{}'.format(image))
    data_set.append([img, [0, 1]])
    # img = cv2.rotate(img, cv2.ROTATE_180)
    # data_set.append([img, [0, 1]])

# Распределяем данные случайным образом
np.random.shuffle(data_set)

x_train = []
y_train = []
# Создаём обучающую выборку с соответствующими ожидаемыми выходными данными
for i in data_set:
    x_train.append(i[0] / 255)
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
    Dense(1024, activation='relu'),
    Dense(2, activation='softmax')
])
print(model.summary())

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

his = model.fit(x_train, y_train, batch_size=16, epochs=5, validation_split=0.2)

model.save('model_color_0.5')

test_img = cv2.imread('data_color/00088.jpg')
print(model.predict(np.array([test_img / 255])))
test_img1 = cv2.imread('data_color/00127.jpg')
print(model.predict(np.array([test_img1 / 255])))
