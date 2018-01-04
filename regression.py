import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import roc_auc_score

df=pd.read_csv('merged.csv', index_col=0)

y=df['Adj Close']
df.drop(['Adj Close'], inplace=True, axis=1)


y=y[1:]
df=df[:-1]

model1a=RandomForestRegressor(n_estimators=100, oob_score=True, random_state=42)
model1a.fit(df[:-200],y[:-200])
print "Train Accuracy :: ", model1a.oob_score_

