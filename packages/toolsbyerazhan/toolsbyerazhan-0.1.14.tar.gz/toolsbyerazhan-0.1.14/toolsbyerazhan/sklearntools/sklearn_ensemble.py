import numpy as np

def test_RandomForestClassifier():
    print("直接看代码或者sklearn源码")
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import make_classification

    X,y = make_classification(n_samples=1000, n_features=4,
                              n_informative=2, n_redundant=0,
                              random_state=0, shuffle=False)
    clf = RandomForestClassifier(max_depth=2, random_state=0)
    clf.fit(X, y)
    
    print(clf.predict([[0, 0, 0, 0]]))

def test_RandomForestRegressor():
    
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.datasets import make_regression

    print("直接看代码或者sklearn源码")
    #n_informative表示有价值的特征个数#n_samples = 100(default)
    X, y = make_regression(n_features=4, n_informative=2,
                           random_state=0, shuffle=False)
    
    regr = RandomForestRegressor(max_depth=2, random_state=0)
    regr.fit(X, y)
    print(regr.predict([[0, 0, 0, 0]]))

if __name__ == "__main__":
    #test_RandomForestClassifier()
    test_RandomForestRegressor()
