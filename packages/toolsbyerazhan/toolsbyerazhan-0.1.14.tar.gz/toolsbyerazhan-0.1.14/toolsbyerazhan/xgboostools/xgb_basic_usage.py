import numpy as np
import tensorflow as tf
import xgboost as xgb
from sklearn import datasets
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score,recall_score,accuracy_score
'''参考网址:https://cloud.tencent.com/developer/article/1446627'''

def test_iris_classification():
    t1 = time.perf_counter()
    iris = datasets.load_iris()
    t2 = time.perf_counter()

    X = iris.data
    Y = iris.target
    #print(t2-t1)

    X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size = 0.2)

    D_train = xgb.DMatrix(X_train,label = Y_train)
    D_test = xgb.DMatrix(X_test,label = Y_test)

    param = {
        'eta':0.3,#视为学习率
        'max_depth':3,#最大深度
        'objective':'multi:softprob',#正在使用的损失函数
        'num_class':3}

    steps = 20
    model = xgb.train(param,D_train,steps)

    preds = model.predict(D_test)
    best_preds = np.asarray([np.argmax(line) for line in preds])

    print("Precision = {}".format(precision_score(Y_test, best_preds, average='macro')))
    print("Recall = {}".format(recall_score(Y_test, best_preds, average='macro')))
    print("Accuracy = {}".format(accuracy_score(Y_test, best_preds)))
if __name__ == "__main__":
    
    test_iris_classification()
    
