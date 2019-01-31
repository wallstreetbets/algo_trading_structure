import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import *
from sklearn.svm import *
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import LinearSVR
from sklearn import linear_model
from sklearn import preprocessing
import conn
import time
import matplotlib
import warnings
warnings.filterwarnings("ignore")
matplotlib.use('TkAgg')

df = conn.engine()

df['Adj Price'] = (df['High'] + df['Low']) / 2

df.fillna(method='ffill', inplace=True)
df.fillna(method='bfill', inplace=True)
time.sleep(1)
forecast_out = int(12) # (n) predicting into the future
X = np.array(df)
X = preprocessing.scale(X)
X_forecast = X[-forecast_out:] # set X_forecast equal to last 30
X = X[:-forecast_out] # remove last 30 from X
df['Prediction'] = df[['Adj Price']].shift(-forecast_out)
y = np.array(df['Prediction'])[:-forecast_out]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

classifiers = [
    SVR(kernel='linear', C=1e3),
    SVR(kernel='rbf', C=1e3, gamma=0.1),
    KNeighborsRegressor(n_neighbors=3),
    LinearRegression(),
    LinearSVR(),
    linear_model.SGDRegressor(),
    linear_model.PassiveAggressiveRegressor(),
    linear_model.TheilSenRegressor(),
    linear_model.LinearRegression()]

avg = []

for model in classifiers:
    model.fit(X_train, y_train)
    model_name = str(model).split('(')[0]
    print("--{} confidence: {}".format(model_name, model.score(X_test, y_test)))
    forecast_prediction = model.predict(X_forecast)
    print("First forecast: {}".format(forecast_prediction[0]))
    plt.plot(forecast_prediction, label=model_name)
    avg.append(forecast_prediction[0])

print("Total Avg: {}".format(sum(avg) / len(avg)))

print('Ploting')
plt.show()
