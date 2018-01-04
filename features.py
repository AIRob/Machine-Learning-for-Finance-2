import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import matplotlib.finance as mpf
import numpy as np
from collections import Counter
from risk_adjustment import buy_sell_holdHigh,buy_sell_holdMedium,buy_sell_holdLow
import os
def emovingav(values,window):
    weights = np.exp(np.linspace(-1.0,0.0,window))
    weights /= weights.sum()
    a = np.convolve(values,weights)[:len(values)]
    a[:window] = a[window]
    return a

#SWING INDEX OF MY MODEL#################################################
LimitMove = 75
def calcR(H2,C1,L2,O1,LM):
    x=H2-C1
    y=L2-C1
    z= H2-L2
    if z< x > y:
        R= (H2-C1)-(0.5*(L2-C1))+(0.25*(C1-O1))
        return R
    elif x< y> z:
        R = (L2 - C1) - (0.5*(H2 - C1)) + (0.25 * (C1 - O1))
        return R
    elif x< z>y:
        R = (H2-L2)+ (0.25*(C1-O1))
        return R
    else:
        return (H2-L2)+ (0.25*(C1-O1))

def calcK(H2,L2,C1):
    x =H2-C1
    y = L2 - C1
    if x>y:
        K=x
        return K
    else:
        return y
def SwingIndexHelper(H1, H2,C1, C2, L1, L2,O1, O2,LM):

    L = LimitMove
    R = calcR(H2,C1,L2,O1,LM)
    K = calcK(H2,L2,C1)
    return 50*((C2-C1+(0.5*(C2-O2))+(0.25*(C1-O1)))/R)*(K/L)

def SwingIndex(df):
    hi = df['High']
    lo = df['Low']
    op = df['Open']
    cl = df['Close']
    svals = []
    svals.append(0)
    for i in range(1,len(df)):
        #print hi[i]-hi[i-1]
        svals.append(SwingIndexHelper(hi[i-1],hi[i],cl[i-1],cl[i],lo[i-1],lo[i],op[i-1],op[i],LimitMove))
    df['SwingIndex'] = svals
###############################################

###TRUE RANGE FONKSIYONUM****************
def TRHelper(cl,hi,lo,op,yc):
    x = hi - lo
    y = abs(hi-yc)
    z = abs(lo - yc)

    if y <= x >=z:
        return x
    elif x <= y >=z:
        return y
    elif x <= z >=y:
        return z

def TR(df):
    hi = df['High']
    lo = df['Low']
    op = df['Open']
    cl = df['Close']
    trVals = []
    trVals.append(0)
    for i in range(1,len(df)):
        trVals.append(TRHelper(cl[i],hi[i],lo[i],op[i],cl[i-1]))
    df['TrueRange']= trVals

#==========================

#Average Directional Index
def DMHelper (op,hi,lo,cl,yo,yh,yl,yc):
    moveup = hi-yh
    movedown= yl-lo
    if 0 < moveup > movedown:
        PDM = moveup
    else:
        PDM =0
    if 0 <movedown > moveup:
        NDM = movedown
    else:
        NDM =0
    return PDM,NDM

def calDIs( ):
    return 0

#calculate PDM and NDM
def PNDMhelper(op, hi, lo, cl, yo, yh, yl, yc):
    moveup = hi - yh
    movedown = yl - lo
    if 0 < moveup > movedown:
        PDM = moveup
    else:
        PDM = 0
    if 0 < movedown > moveup:
        NDM = movedown
    else:
        NDM = 0
    return PDM, NDM

def PDNDM(df):
    hi = df['High']
    lo = df['Low']
    op = df['Open']
    cl = df['Close']
    PDMVals = []
    PDMVals.append(0)
    NDMVals = []
    NDMVals.append(0)
    for i in range(1, len(df)):
        PDMVals.append(PNDMhelper(op[i],hi[i],lo[i],cl[i],op[i-1],hi[i-1],lo[i-1],cl[i-1])[0])
        NDMVals.append(PNDMhelper(op[i],hi[i],lo[i],cl[i],op[i-1],hi[i-1],lo[i-1],cl[i-1])[1])

    df['PDM'] = PDMVals
    df['NDM'] = NDMVals

##new

def percentCha(startPoint,currentPoint):
    return ((float(currentPoint)-startPoint)/abs(startPoint))*100.0

def chaiVol(emaUsed,periodsBfr,df):
    chaikin_volatility = []
    chaikin_volatility.append(0)
    highM_low =[]
    x =0
    while x < len(df):
        hml = df['High'][x]-df['Low'][x]
        highM_low.append(hml)
        x =x +1
    highMlowEMA = emovingav(highM_low,emaUsed)
    y = emaUsed +periodsBfr
    while y<len(df):
        cvc = percentCha(highMlowEMA[y-periodsBfr],highMlowEMA[y])
        chaikin_volatility.append(cvc)
        y = y +1

    return df['Volume'][emaUsed+periodsBfr:],chaikin_volatility

def chaFin():
    # df['ChaikinVol10']=chaiVol(10,0)
    arr = chaiVol(10, 10)
    arr = np.array(arr)
    print arr.shape
##chaikin volatility bitti

#GAPO
def Gapo(timeFrame,df):
    gapo = []
    for i in range(0,timeFrame):
        gapo.append(0)
    x = timeFrame
    while x < len(df['High']):
        consHigh = df['High'][x-timeFrame:x]
        consLow = df['Low'][x-timeFrame:x]
        highestHigh = max(consHigh)
        lowestLow = min(consLow)
        gapos = ((np.log(highestHigh-lowestLow ))/np.log(timeFrame))
        #print gapos
        gapo.append(gapos)
        x = x+1
    return gapo

def process_data_for_labels(ticker):
    hm_days = 7
    tickers = df.columns.values.tolist()
    df.fillna(0, inplace=True)
    for i in range(1, hm_days + 1): #creates columns for future percent change
        df['{}_{}d_percentC'.format(ticker, i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
    df.fillna(0, inplace=True)
    return tickers, df



def extract_featuresets(ticker):
    tickers, df = process_data_for_labels(ticker)
    df['{}_classHigh'.format(ticker)] = list(map( buy_sell_holdHigh,
                                               df['{}_1d_percentC'.format(ticker)]))
    df['{}_classMedium'.format(ticker)] = list(map(buy_sell_holdMedium,
                                                 df['{}_1d_percentC'.format(ticker)]))
    df['{}_classLow'.format(ticker)] = list(map(buy_sell_holdLow,
                                                 df['{}_1d_percentC'.format(ticker)]))
    vals = df['{}_classHigh'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread:',Counter(str_vals))

    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_vals = df[[ticker]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)
    #print df_vals.info()
    X = df_vals.values

    y = df['{}_classHigh'.format(ticker)].values
    print df
    return X, y, df






style.use('ggplot')

start = dt.datetime(2017, 1, 1)
end = dt.datetime(2017, 06, 1)

if not os.path.exists('features'):
    os.makedirs('features')

for i in ['AMGN','BAC','EFX','FB','GOOG','VZ']:
    df = pd.read_csv('stocks/'+str(i)+'.csv', parse_dates=True, index_col=0)

    df['100movingaverage'] = df['Adj Close'].rolling(window=100).mean() ##son 100 entrynin ortalamasini yaz

    #df.dropna(inplace=True) inplace nalari sil
    df['100movingaverage'] = df['Adj Close'].rolling(window=100,min_periods=0).mean()

    df['3dexpmv'] =emovingav(df['Adj Close'], 3)
    df['10dexpmv'] =emovingav(df['Adj Close'], 10)
    df_norm = (df - df.mean()) / (df.max() - df.min())
    print(df_norm.head())
    df_norm['Adj Close'].plot()
    df_norm['100movingaverage'].plot()
    df_norm['3dexpmv'].plot()
    fig, ax = plt.subplots()
    mpf.candlestick2_ochl(ax, opens=df['Open'], closes=df['Close'], highs=df['High'], lows=df['Low'], width=2, colorup='g', colordown='r', alpha=0.75)


    SwingIndex(df)
    TR(df)
    PDNDM(df)
    df['Gapo10']= (Gapo(10,df))
    df['Gapo5']= (Gapo(5,df))




    X,y,df=extract_featuresets('Adj Close')
    print df.info()

    df.to_csv('features/features{}.csv'.format(i))
#plt.show()