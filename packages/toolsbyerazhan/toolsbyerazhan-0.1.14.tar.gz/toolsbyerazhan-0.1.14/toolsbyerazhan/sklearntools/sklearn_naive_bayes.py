import numpy as np

def test_GaussianNB():
    from sklearn.naive_bayes import GaussianNB
    print("直接查看代码,或者sklearn中的源码")
    X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
    Y = np.array([1, 1, 1, 2, 2, 2])

    clf = GaussianNB()
    clf.fit(X, Y)#需要调用_partial_fit()
    
    print(clf.predict([[-0.8, -1]]))

    clf_pf = GaussianNB()
    clf_pf.partial_fit(X, Y, np.unique(Y))#需要输入label(去重后的唯一类别)

    print(clf_pf.predict([[-0.8, -1]]))

def test_MultinomialNB():
    from sklearn.naive_bayes import MultinomialNB
    print("直接查看代码,或者sklearn中的源码")
    rng = np.random.RandomState(1)
    X = rng.randint(5, size=(6, 100))
    y = np.array([1, 2, 3, 4, 5, 6])
    
    clf = MultinomialNB()
    clf.fit(X, y)
    
    print(clf.predict(X[2:3]))

if __name__ == "__main__":
    test_GaussianNB()
    #test_MultinomialNB()
