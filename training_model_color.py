import numpy as np
import os
import cv2
import random
import time

import keras
import tensorflow_addons as tfa

data_set = []
val_set = []

print("Подготовка данных............")
# Получаем индексы для тестовой выборки
image_quantity_ok = len(os.listdir("data_color/OK"))
image_quantity_not_ok = len(os.listdir("data_color/NOT_OK"))

val_indexes_ok = random.sample(range(image_quantity_ok), int(image_quantity_ok *0.1))
val_indexes_not_ok = random.sample(range(image_quantity_not_ok), int(image_quantity_not_ok*0.1))

# Загружаем фото в датасет
for index, image in enumerate(os.listdir('data_color/OK')):
    if index not in val_indexes_ok:
        img = cv2.imread('data_color/OK/{}'.format(image))
        data_set.append([img, 0])

for index, image in enumerate(os.listdir('data_color/NOT_OK')):
    if index not in val_indexes_not_ok:
        img = cv2.imread('data_color/NOT_OK/{}'.format(image))
        data_set.append([img, 1])

# Загружаем валидационную выборку
for index in val_indexes_ok:
    image = os.listdir('data_color/OK')[index]
    img = cv2.imread('data_color/OK/{}'.format(image))
    val_set.append([img, 0])

for index in val_indexes_not_ok:
    image = os.listdir('data_color/NOT_OK')[index]
    img = cv2.imread('data_color/NOT_OK/{}'.format(image))
    val_set.append([img, 1])

# Распределяем данные случайным образом
np.random.shuffle(data_set)
np.random.shuffle(val_set)

x_train = []
y_train = []
# Создаём обучающую выборку с соответствующими ожидаемыми выходными данными
for i in data_set:
    x_train.append(i[0] / 255)
    y_train.append(i[1])

x_val = []
y_val = []

# Создаём валидационную выборку с соответствующими ожидаемыми выходными данными
for i in val_set:
    x_val.append(i[0] / 255)
    y_val.append(i[1])

x_train = np.array(x_train)
y_train = np.array(y_train)
x_val = np.array(x_val)
y_val = np.array(y_val)

print('Создание модели............')
# Создаём модель нейросети
model = keras.Sequential([
    keras.layers.Conv2D(16, (3, 3), padding='same', activation='relu', input_shape=(280, 280, 3)),
    # keras.layers.Conv2D(16, (3, 3), padding='same', activation='relu'),
    keras.layers.MaxPooling2D((2, 2), strides=2),
    keras.layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
    # keras.layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
    keras.layers.MaxPooling2D((2, 2), strides=2),
    keras.layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
    # keras.layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
    keras.layers.MaxPooling2D((2, 2), strides=2),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.25),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])
print(model.summary())

# Объявляем сохранение модели с лучшими весами
callbacks = [
    keras.callbacks.ModelCheckpoint(filepath='best_model',
                                    monitor='val_fbeta_score',
                                    save_best_only=True,
                                    mode='max',
                                    verbose=0)
]

# Определение метрики для увеличения стоимости NOT_OK
f2_score = tfa.metrics.FBetaScore(
    num_classes=1,
    average='micro',
    beta=2.0,
    threshold=0.5,
)

# Компилируем модель
model.compile(optimizer='Nadam',
              loss='binary_crossentropy',
              metrics=['accuracy', keras.metrics.AUC(), f2_score])

# Запускаем обучение
his = model.fit(x_train, y_train, batch_size=16, epochs=10, callbacks=callbacks, validation_data=(x_val, y_val))

# Загружаем модель
print(max(his.history['val_fbeta_score']))
start_time = time.time()
model = keras.models.load_model('best_model')

# Проверяем на тестовой выборке
count = 0
print('OK')
for i in os.listdir('data_color/test/OK'):
    test_img = cv2.imread('data_color/test/OK/' + i)
    print(model.predict(np.array([test_img / 255])))
    if count < 1:
        end_time = time.time()
        print(end_time - start_time)
        count += 1

print("NOT_OK")
for i in os.listdir('data_color/test/NOT_OK'):
    test_img = cv2.imread('data_color/test/NOT_OK/' + i)
    print(model.predict(np.array([test_img / 255])))

