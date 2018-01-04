from sklearn.ensemble import RandomForestRegressor

modelz=RandomForestRegressor()

def regressor(df,model,days):
    days=-days
    y = df['Adj Close']
    df.drop(['Adj Close'], inplace=True, axis=1)
    y = y[1:]
    df = df[:-1]
    model.fit(df[:days], y[:days])
    z = model.predict(df[days:])
    return z