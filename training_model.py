import numpy as np
import os
import cv2
import tensorflow as tf
import keras


#print(tf.config.list_physical_devices('GPU'))

data_set = []

print("Подготовка данных............")
# Загружаем фото в датасет
for image in os.listdir('data_gray/OK'):
    img = cv2.imread('data_gray/OK/{}'.format(image))
    data_set.append([img, [1, 0]])
    # img = cv2.rotate(img, cv2.ROTATE_180
    # data_set.append([img, [1, 0]])

for image in os.listdir('data_gray/NOT_OK'):
    img = cv2.imread('data_gray/NOT_OK/{}'.format(image))
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
    keras.layers.Conv2D(16, (3, 3), padding='same', activation='relu', input_shape=(280, 280, 3)),
    keras.layers.Conv2D(16, (3, 3), padding='same', activation='relu'),
    keras.layers.MaxPooling2D((2, 2), strides=2),
    keras.layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
    keras.layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
    keras.layers.MaxPooling2D((2, 2), strides=2),
    keras.layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
    keras.layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
    keras.layers.MaxPooling2D((2, 2), strides=2),
    keras.layers.Flatten(),
    keras.layers.Dense(512, activation='relu'),
    keras.layers.Dense(2, activation='softmax')
])
print(model.summary())

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

his = model.fit(x_train, y_train, batch_size=16, epochs=10, validation_split=0.2)

test_img = cv2.imread('data_gray/00010.jpg')
print(model.predict(np.array([test_img / 255])))
test_img1 = cv2.imread('data_gray/00013.jpg')
print(model.predict(np.array([test_img1 / 255])))
