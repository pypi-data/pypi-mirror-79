import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import backend as K
#from sklearn.metrics import r2_score
from Data_preprocessing import data_preprocessing as data_T

#配置GPU运行tensorflow
gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpus[0], True)

#自定义评价函数
def R2_Score(y_true, y_pred):
    x = 1-((K.sum(K.pow((y_true-y_pred), 2)))/(K.sum(K.pow(y_true-K.mean(y_pred), 2))))
    return x

#LSTM架构
model1 = keras.models.Sequential()
model1.add(layers.LSTM(1024, kernel_initializer='glorot_uniform', input_shape=data_T.train_x3.shape[-2:], return_sequences=True))
model1.add(layers.LSTM(512, return_sequences=True))
model1.add(layers.LSTM(256))
model1.add(layers.Dense(128, activation='relu'))
model1.add(layers.Dense(64, activation='relu'))
model1.add(layers.Dense(1, activation='relu'))
#模型编译
model1.compile(loss="mse", optimizer=keras.optimizers.Adam(lr=0.0001), metrics=['MSE', R2_Score])