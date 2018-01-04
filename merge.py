import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests

if not os.path.exists('merges'):
    os.makedirs('merges')

def merge(stock):
    companies=pd.read_csv('correlations/correlations{}.csv'.format(stock))
    features = pd.read_csv('features/features{}.csv'.format(stock))
    merged = pd.merge(features,companies,on='Date')

    merged.set_index('Date', inplace=True)
    merged.to_csv('merges/merges{}.csv'.format(stock))


for stock in ['AMGN','BAC','EFX','FB','GOOG','VZ']:
    merge(stock)