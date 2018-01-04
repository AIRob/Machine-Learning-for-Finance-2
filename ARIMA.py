import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import matplotlib.finance as mpf
from sklearn import preprocessing

import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
# plt.style.use('fivethirtyeight')
# style.use('ggplot')
#
# start = dt.datetime(2017, 1, 1)
# end = dt.datetime(2015, 1, 1)
#
# df = web.DataReader('GOOG', "yahoo", start, end) #google stock values, from yahoo, between times
#
# #print(df.head())
#
# df.to_csv('GOOG.csv')

df = pd.read_csv('GOOG.csv', parse_dates=True, index_col=0)

#print df

data = sm.datasets.co2.load_pandas()
y = data.data
# print(y)
# The 'MS' string groups the data in buckets by start of the month
y = y['co2'].resample('MS').mean()

# The term bfill means that we use the value before filling in missing values
y = y.fillna(y.bfill())

# print(y)
# print(df)

a=df['Close']
print(a)

# Define the p, d and q parameters to take any value between 0 and 2
p= d = q = range(0, 2)
s=[12,52,365]
# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))
#print pdq

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], x[3]) for x in list(itertools.product(p, d, q, s))]


warnings.filterwarnings("ignore") # specify to ignore warning messages

# for param in pdq:
#     for param_seasonal in seasonal_pdq:
#         print str(param)+" "+str(param_seasonal)
#         try:
#             mod = sm.tsa.statespace.SARIMAX(a,
#                                             order=param,
#                                             seasonal_order=param_seasonal,
#                                             enforce_stationarity=False,
#                                             enforce_invertibility=False)
#
#             results = mod.fit(disp=0)
#
#             print('SARIMA{}x{} - AIC:{}'.format(param, param_seasonal, results.aic))
#         except:
#             continue

mod = sm.tsa.statespace.SARIMAX(a,
                                order=(1, 1, 0),
                                seasonal_order=(1, 0, 0, 52),
                                enforce_stationarity=False,
                                enforce_invertibility=False)

results = mod.fit()

#print(results.summary())

pred = results.get_prediction(start=pd.to_datetime('2017-07-03'), dynamic=False)
pred_ci = pred.conf_int()

y_forecasted = pred.predicted_mean
y_truth = a['2017-07-03':]

# Compute the mean square error
mse = ((y_forecasted - y_truth) ** 2).mean()
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

print(a.index.freq)
a = a.asfreq(freq='7d')
# Get forecast 500 steps ahead in future
pred_uc = results.get_forecast(steps=10)

# Get confidence intervals of forecasts
pred_ci = pred_uc.conf_int()

ax = a.plot(label='observed')
pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Date')
ax.set_ylabel('CO2 Levels')

plt.legend()
plt.show()