import datetime
import tensorflow as tf
from Model_Build import model_LSTM
from Data_preprocessing import data_preprocessing as data_T


# #LSTM模型训练并保存
def LSTM_Train4G():
    log_dir = "Data_IO/logs/4G/LSTM/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1,
                                                          write_graph=True, write_grads=True, update_freq='epoch')

    model_LSTM.model1.fit(data_T.train_x3, data_T.train_y3, epochs=1000, batch_size=64,
                          validation_data=(data_T.test_x3, data_T.test_y3), callbacks=tensorboard_callback)
    model_LSTM.model1.save('Model_Save/LSTM_model1.h5')