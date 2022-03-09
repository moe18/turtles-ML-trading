import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import recall_score, precision_score, confusion_matrix

from sklearn.metrics import mean_squared_error
import statsmodels.api as sm


def get_data():
    X_train = pd.read_parquet(
        '/Users/mordechaichabot/Projects/investment_framework/strats/sma_ml/data/prosseced_data/X_train.parquet')
    y_train = pd.read_parquet(
        '/Users/mordechaichabot/Projects/investment_framework/strats/sma_ml/data/prosseced_data/y_train.parquet')
    y_train_clf = np.where(y_train > 0, 1, 0)

    return X_train, y_train, y_train_clf


def cross_val(clf, X_train, y_train_clf, thresh=.5):
    tscv = TimeSeriesSplit(n_splits=4)
    for train_index, test_index in tscv.split(X_train):
        X_train_val, X_test_val = X_train.values[train_index], X_train.values[test_index]
        y_train_val, y_test_val = y_train_clf[train_index], y_train_clf[test_index]

        clf.fit(X_train_val, y_train_val)
        proba = rnd_clf.predict_proba(X_test_val)
        pred = np.where(proba[:, 1:] > thresh, 1, 0)
        print('recall:',recall_score(pred, y_test_val))
        print('precision', precision_score(pred, y_test_val))
        print(confusion_matrix(y_test_val,pred))


X_train, y_train, y_train_clf = get_data()[:100000]

rnd_clf = RandomForestClassifier(n_estimators=400, random_state=42,n_jobs=-1)

#cross_val(rnd_clf, X_train, y_train_clf, .6)

rnd_clf.fit(X_train, y_train_clf)

dump(rnd_clf,
     '/Users/mordechaichabot/Projects/investment_framework/strats/sma_ml/models/trained_models/rnd_f_model.joblib')
