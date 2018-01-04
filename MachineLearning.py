import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import numpy as np
import pandas_datareader.data as web
import matplotlib.finance as mpf
from sklearn import preprocessing
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline


style.use('ggplot')
from sklearn.ensemble import RandomForestRegressor
start = dt.datetime(2017, 1, 1)
end = dt.datetime(2017, 06, 1)

#df = web.DataReader('GOOG', "yahoo", start, end) #google stock values, from yahoo, between times

#print(df.head())

#df.to_csv('GOOG.csv')

df = pd.read_csv('GOOG.csv', parse_dates=True, index_col=0)


df_norm = (df - df.mean()) / (df.max() - df.min())

#print df_norm['Open']
openDataArray = df_norm['Open'][:]
timeaxis = range(0,464)
def f(x):

    return np.sin(x)


def backtesting(trainingWindow, data,days, model):
    totalMoney = 1000000
    trainingdata = []

    for a in range(0,len(data)-trainingWindow-1):
        endpoint=trainingWindow+a
        windowData = data[a:endpoint]
        dayz = days[a:endpoint]

        nextdayPrice =data[endpoint]
        nextday =  days[endpoint]
        #print windowData,'\n', dayz,'\n\n'
        totalMoney = totalMoney + backtesting_helper(windowData,dayz, nextdayPrice, totalMoney, model,nextday)
        print 'MONEY IS',totalMoney
        if(totalMoney<=0):
            break
        #print totalMoney
    return totalMoney

def backtesting_helper(traindata,dayz, nextdayPrice, totalMoney, model,nextday):
    traindata = np.array(traindata).reshape(len(traindata),1)
    dayz= np.array(dayz).reshape(len(dayz),1)
    model.fit(traindata,dayz)
    a = model.predict(nextday)
    print traindata[-1],nextdayPrice, a
    if(traindata[-1]<a):
        print 'BUY ', (nextdayPrice - traindata[-1])/traindata[-1]* totalMoney
        return (nextdayPrice - traindata[-1])/traindata[-1]* totalMoney
    if(traindata[-1]>=a):
        print 'SELL ', (traindata[-1] -nextdayPrice)/traindata[-1]*totalMoney
        return (traindata[-1] -nextdayPrice)/traindata[-1]*totalMoney

timeaxis = np.array(timeaxis)
openDataArray = np.array(openDataArray)

X = openDataArray[:, np.newaxis]
y = f(openDataArray)
X_plot = openDataArray[:, np.newaxis]

#model=RandomForestRegressor(n_estimators=100, oob_score=True, random_state=42)
model = make_pipeline(PolynomialFeatures(), Ridge())
#model.fit(df['High'],timeaxis)


df=pd.read_csv('merged.csv', index_col=0)
y=df['Adj Close']
df.drop(['Adj Close'], inplace=True, axis=1)




X =  np.array(df['High'])
bero = backtesting(10,X,timeaxis,model)

print "Final money",bero
#print X
#model.fit(X, y)


plt.show()