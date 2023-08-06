import tensorflow as tf
import numpy as np
import pandas as pd
import tensorflow.keras as keras
import matplotlib.pyplot as plt
from Model_Build.model_LSTM import R2_Score
from Data_preprocessing import data_preprocessing as data_P


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
font1 = {'weight': 'normal', 'size': 13}

#预测4G并画图保存
def LSTM_Predict():

    model = keras.models.load_model('Model_Save/LSTM_model1.h5', custom_objects={"R2_Score": R2_Score})
    predict_result1 = model.predict(data_P.train_x3)
    predict_result2 = model.predict(data_P.test_x3)
    predict_result = np.append(predict_result1, predict_result2)
    predict_result = pd.DataFrame(predict_result)
    predict_result.to_csv('Data_IO/train_result.csv', index=False)

    #标准化恢复
    actual1 = data_P.train_y3[:, 0]
    actual2 = data_P.test_y3[:, 0]
    size1 = data_P.train_y3.shape[0]
    size2 = data_P.test_y3.shape[0]

    actual1 = data_P.st3.inverse_transform(actual1)
    predict_result1 = data_P.st3.inverse_transform(predict_result1)

    actual2= data_P.st3.inverse_transform(actual2)
    predict_result2 = data_P.st3.inverse_transform(predict_result2)




    #作图并保存
    fig, axes = plt.subplots(figsize=(30,20), nrows=1, ncols=2)
    fig.suptitle('LSTM模型预测展示',fontsize=20, y=0.95)
    axes[0].plot(range(0, size1), actual1, 'g-', linewidth='1.5', label=' 真实值')
    axes[0].plot(range(0, size1), predict_result1, 'r-', linewidth='1.5', label=' 预测值')
    axes[0].set_title('训练集', fontdict={'weight':'normal','size': 15}, y=1.01)
    axes[0].tick_params(labelsize=15)
    for xtick in axes[0].get_xticklabels():
        xtick.set_rotation(50)
    axes[0].set_ylabel('上\n行\n速\n率\n(Mbps)', fontdict={'weight': 'normal', 'size': 15}, labelpad=40, rotation=0,
                       loc='center', verticalalignment='bottom')
    axes[0].set_xlabel('样本', fontdict={'weight': 'normal', 'size': 15}, labelpad=40, rotation=0,
                       loc='center', verticalalignment='bottom')
    axes[0].grid()
    axes[1].plot(range(0, size2), actual2, 'g-', linewidth='1.5', label=' 真实值')
    axes[1].plot(range(0, size2), predict_result2, 'r-', linewidth='1.5', label='预测值')
    axes[1].set_title('测试集', fontdict={'weight':'normal','size': 15}, y=1.01)
    axes[1].tick_params(labelsize=15)
    for xtick in axes[1].get_xticklabels():
        xtick.set_rotation(50)
    axes[1].set_ylabel('预\n测\n指\n标', fontdict={'weight': 'normal', 'size': 15}, labelpad=40, rotation=0,
                       loc='center', verticalalignment='bottom')
    axes[1].set_xlabel('样本', fontdict={'weight': 'normal', 'size': 15}, labelpad=40, rotation=0,
                       loc='center', verticalalignment='bottom')
    legend1 = plt.legend(bbox_to_anchor=(0.775, 1.015), loc=3, borderaxespad=0, prop=font1, markerscale=1, handletextpad=0)
    frame = legend1.get_frame()
    frame.set_alpha(1)
    frame.set_facecolor('none')  # 设置图例legend背景透明
    axes[1].grid()
    fig.savefig('Data_IO/LSTM_model1.png', dpi=100, bbox_inches='tight', transparent=True)
    plt.show()


def test():
        testx = data_P.test_x2[-data_P.past_history:,:]

        model = keras.models.load_model('Model_Save/LSTM_model1.h5', custom_objects={"R2_Score": R2_Score})
        test_result = model.predict(testx)
        test_result = test_result.flatten()

        test_result = data_P.st3.inverse_transform(test_result)

        test_result = pd.DataFrame(test_result)
        test_result.columns=['label']
        test_result.to_csv('Data_IO/predict_result.csv', encoding='utf_8_sig')
