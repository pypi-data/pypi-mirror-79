#from Model_Train import train
#from Model_Predict import predict
import pyotp


# #训练模型
#train.LSTM_Train4G()

# #训练结果展示
#predict.LSTM_Predict()

# #验证
#predict.test()


totp = pyotp.TOTP('449685')
a=totp.now()
print (a)