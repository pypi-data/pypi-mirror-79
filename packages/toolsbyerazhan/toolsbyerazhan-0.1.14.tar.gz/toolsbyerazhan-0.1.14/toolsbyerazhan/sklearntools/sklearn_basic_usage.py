import numpy as np

"""
sklearn常用函数
https://www.cnblogs.com/traditional/p/9594570.html
"""
def test_train_test_split():
    from sklearn.model_selection import train_test_split
    tips = """
tips:
    execute code:
    X = [1,2,3,4,5]
    Y = [1,1,1,1,0]
    X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size = 0.2)
    print("X_train:",X_train)
    print("Y_train:",Y_train)
    print("X_test:",X_test)
    print("Y_test:",Y_test)
"""
    print(tips)
    X = [1,2,3,4,5]
    Y = [1,1,1,1,0]
    X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size = 0.2)
    print("X_train:",X_train)
    print("Y_train:",Y_train)
    print("X_test:",X_test)
    print("Y_test:",Y_test)
    
if __name__ == "__main__":
    #test_train_test_split()
    pass
