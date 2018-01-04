import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import matplotlib.finance as mpf
import os
style.use('ggplot')

start = dt.datetime(2016, 1, 1)
end = dt.datetime(2017, 11, 1)


if not os.path.exists('stocks'):
    os.makedirs('stocks')

df1 = web.DataReader('BAC', "yahoo", start, end) #BANK OF AMERICA stock values, from yahoo, between times
print(df1.head())
df1.to_csv('stocks/BAC.csv')

df2 = web.DataReader('EFX', "yahoo", start, end) #EQUIFAX stock values, from yahoo, between times
print(df2.head())
df2.to_csv('stocks/EFX.csv')

df3 = web.DataReader('AMGN', "yahoo", start, end) #AMGEN stock values, from yahoo, between times
print(df3.head())
df3.to_csv('stocks/AMGN.csv')

df4 = web.DataReader('FB', "yahoo", start, end) #FACEBOOK stock values, from yahoo, between times
print(df4.head())
df4.to_csv('stocks/FB.csv')

df5 = web.DataReader('VZ', "yahoo", start, end) #VERIZON stock values, from yahoo, between times
print(df5.head())
df5.to_csv('stocks/VZ.csv')

df6 = web.DataReader('GOOG', "yahoo", start, end) #GOOGLE stock values, from yahoo, between times
print(df6.head())
df6.to_csv('stocks/GOOG.csv')

dfGold = web.DataReader('GLD', "yahoo", start, end) #google stock values, from yahoo, between times
print(dfGold.head())
dfGold.to_csv('stocks/GOLD.csv')

df = pd.read_csv('GOOG.csv', parse_dates=True, index_col=0)
fig, ax = plt.subplots()
mpf.candlestick2_ochl(ax, opens=df['Open'], closes=df['Close'], highs=df['High'], lows=df['Low'], width=2, colorup='g', colordown='r', alpha=0.75)

df['Adj Close'].plot()
plt.show()
