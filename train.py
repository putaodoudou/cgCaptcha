from sklearn.svm import SVC
from sklearn import grid_search
from sklearn import cross_validation as cs
from sklearn.externals import  joblib
import numpy as np
import persistence
from numpy import *
import time
import warnings

def cross_validation():
    dataSet, labels = persistence.allData(persistence.openConnection())
    # dataMatrix = mat(dataSet)
    # labelMatrix = mat(labels)
    clf = SVC(kernel='rbf', C=1000)
    clf.fit(dataSet, labels)
    scores = cs.cross_val_score(clf, dataSet, labels, cv=5)
    print('Accuracy: %0.2f (+- %0.2f)' % (scores.mean(), scores.std()))
    return clf

# t0 = time.time()
# cross_validation()
# print('fit time:', round(time.time()-t0, 3), 's')

def searchBestParameter():
    parameters = {'kernel': ('linear', 'poly', 'rbf', 'sigmoid'), 'C': [1, 100]}
    dataSet, labels = persistence.allData(persistence.openConnection())
    svr = SVC()
    clf = grid_search.GridSearchCV(svr, parameters)
    clf.fit(dataSet, labels)

    print(clf.best_params_)

# searchBestParameter()
# print('fit time: %.2f s' % round(time.time()-t0, 3))


def predict(binImg1, binImg2, binImg3):
    parameters = {'kernel': ('linear', 'poly', 'rbf', 'sigmoid'), 'C': [1, 100]}
    dataSet, labels = persistence.allData(persistence.openConnection())
    svr = SVC()
    clf = grid_search.GridSearchCV(svr, parameters)
    clf.fit(dataSet, labels)

    v1 = clf.predict(binImg1)
    v2 = clf.predict(binImg2)
    v3 = clf.predict(binImg3)

    return (v1, v2, v3)