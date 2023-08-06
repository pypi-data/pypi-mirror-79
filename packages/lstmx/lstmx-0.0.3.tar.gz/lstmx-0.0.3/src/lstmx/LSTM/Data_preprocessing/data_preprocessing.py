import  numpy as np
import pandas as pd
from sklearn import  preprocessing
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


# 创建序列 单特征
def univariate_data(dataset, start_index, end_index, history_size, target_size):

    data1, labels1 = [], []

    start_index = start_index + history_size

    for i in range(start_index, end_index):
        indices = range(i-history_size, i)
        data1.append(np.reshape(dataset[indices], (history_size, 1)))
        labels1.append(dataset[i+target_size])
    return np.array(data1), np.array(labels1)

#创建时间序列 多特征
def multivariate_data(dataset, target, start_index, end_index, history_size, target_size, step, single_step=False):

    data2, labels2 = [], []

    start_index = start_index + history_size

    for i in range(start_index, end_index):
        indices = range(i-history_size, i, step)
        data2.append(dataset[indices])

        if single_step:
            labels2.append(target[i+target_size])
        else:
            labels2.append(target[i:i+target_size])

    return np.array(data2), np.array(labels2)

#读取数据
Data = pd.read_csv("../iris_test.csv")

# #--------------------------------------------------------------------------------------------------------------
#单特征数据
data1 = Data.iloc[:, 0:1]
data1=np.array(data1).reshape(-1,1)
train_size1 = int(len(data1) * 0.8)
test_size1 = len(data1) - train_size1
train1, test1 = data1[0:train_size1, :], data1[train_size1:len(data1), :]
st1 = preprocessing.StandardScaler()
train1 = st1.fit_transform(train1)
test1 = st1.transform(test1)

#单特征历史步长
univariate_past_history = 2
#特征目标点
univariate_future_target = 0


#单特预测单个点 数据生成
train_x1, train_y1 = univariate_data(train1, 0, train_size1, univariate_past_history, univariate_future_target)
test_x1, test_y1 = univariate_data(test1, 0, test_size1, univariate_past_history, univariate_future_target)

#x1_train = np.reshape(train_x1, (train_x1.shape[0], train_x1.shape[1], 1))
#x1_test = np.reshape(test_x1, (test_x1.shape[0], test_x1.shape[1], 1))


# #----------------------------------------------------------------------------------------------------------------------
#多特特征数据
data2 = (Data.iloc[:, :]).values
train_size2 = int(data2.shape[0] * 0.5)
test_size2 = data2.shape[0] - train_size2
train2, test2 = data2[0:train_size2, :], data2[train_size2:data2.shape[0], :]
st2 = preprocessing.StandardScaler()
train2 = st2.fit_transform(train2)
test2 = st2.transform(test2)

# #-------------------------标注化恢复使用--------------------------------------
st3 = preprocessing.StandardScaler()
train2_y = st3.fit_transform(train2[:,-1])


#多特征历史步长
past_history = 2
#多特征预测目标长度
future_target = 0
#多特征采样间隔
STEP = 1




#多特征预测单个点 数据生成
train_x2, train_y2 = multivariate_data(train2, train2[:, -1], 0, train_size2, past_history,
                                       future_target, STEP, single_step=True)
test_x2, test_y2 = multivariate_data(test2, test2[:, -1], 0, test_size2, past_history,
                                     future_target, STEP, single_step=True)
#x2_train = np.reshape(train_x2, (train_x2.shape[0], train_x2.shape[1], train_x2.shape[2]))
#x2_test = np.reshape(test_x2, (test_x2.shape[0], test_x2.shape[1], test_x2.shape[2]))



#多特征预测多个个点 数据生成
train_x3, train_y3 = multivariate_data(train2, train2[:, -1], 0, train_size2, past_history,
                                       future_target, STEP)
test_x3, test_y3 = multivariate_data(test2, test2[:, -1], 0, test_size2, past_history,
                                     future_target, STEP)
#x3_train = np.reshape(train_x3, (train_x3.shape[0], train_x3.shape[1], train_x3.shape[2]))
#x3_test = np.reshape(test_x3, (test_x3.shape[0], test_x3.shape[1], test_x3.shape[2]))





























