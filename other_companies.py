import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle


if not os.path.exists('correlations'):
    os.makedirs('correlations')


def save_tickers(stock):
    if(stock=='AMGN'):
        tickers=['LH', 'PFE', 'WAT', 'MCO', 'EBAY', 'ZBH', 'CSCO', 'MRK', 'MDT', 'ABBV']
    if (stock == 'BAC'):
        tickers =['CFG', 'PRU', 'PNC', 'RF', 'MTB', 'SCHW', 'HBAN', 'RJF', 'USB', 'KEY']
    if (stock == 'EFX'):
        tickers =['EQIX', 'AVY', 'MAS', 'STZ', 'BSX', 'AMZN', 'FB', 'GPN', 'BDX', 'FBHS']
    if (stock == 'FB'):
        tickers =['AMZN', 'EQIX', 'ATVI', 'AVY', 'V', 'FISV', 'GOOGL', 'GOOG', 'INFO', 'RTN']
    if (stock == 'GOOG'):
        tickers =['FB', 'AMZN', 'ATVI', 'V', 'MSFT', 'HD', 'AIZ', 'FISV', 'MCD', 'GPN']
    if (stock == 'VZ'):
        tickers =['O', 'T', 'SJM', 'NEM', 'SCG', 'GIS', 'AWK', 'TSN', 'CPB', 'REG']

    with open("other_companies.pickle", "wb") as f:
        pickle.dump(tickers, f)
    print tickers
    return tickers




def get_data_from_yahoo(stock,reload_sp500=False):
    tickers=save_tickers(stock)
    if not os.path.exists('other_stocks'):
        os.makedirs('other_stocks')

    start = dt.datetime(2016, 1, 1)
    end = dt.datetime(2017, 11, 1)

    for ticker in tickers:
        # just in case your connection breaks, we'd like to save our progress!

        if not os.path.exists('other_stocks/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, "yahoo", start, end)
            df.to_csv('other_stocks/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))






def compile_data(stock):
    get_data_from_yahoo(stock, reload_sp500=False)
    with open("other_companies.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()
    print tickers
    for count, ticker in enumerate(tickers):
        df = pd.read_csv('other_stocks/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns={'Adj Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)
    #print(main_df.head())

    main_df.to_csv('correlations/correlations{}.csv'.format(stock))

for stock in ['AMGN','BAC','EFX','FB','GOOG','VZ']:
    compile_data(stock)

