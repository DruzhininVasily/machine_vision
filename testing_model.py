import time
import os
import keras
import cv2
import numpy as np
import tensorflow_addons as tfa

# Определение метрики для увеличения стоимости NOT_OK
f2_score = tfa.metrics.FBetaScore(
    num_classes=1,
    average='micro',
    beta=2.0,
    threshold=0.5,
)

start_time = time.time()
model = keras.models.load_model('best_model', custom_objects={'FBetaScore': f2_score})

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