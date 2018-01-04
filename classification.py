
import pandas as pd
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score


from tabulate import tabulate

def classification(df,risk,days):

    # data=pd.read_csv('merged.csv', index_col=0)
    # df=pd.read_csv('merged.csv', index_col=0)
    y=df['Adj Close_class'+risk]
    if 'Adj Close_classHigh' in df:
        df.drop(['Adj Close_classHigh'], inplace=True, axis=1)
    if 'Adj Close_classMedium' in df:
        df.drop(['Adj Close_classMedium'], inplace=True, axis=1)
    if 'Adj Close_classLow' in df:
        df.drop(['Adj Close_classLow'], inplace=True, axis=1)

    y=y[1:]
    df=df[:-1]

    model1a=RandomForestClassifier(n_estimators=100, oob_score=True, max_features=30, random_state=42,min_samples_leaf=40)
    papa=model1a.fit(df[:-days],y[:-days])
    print "Random Forest Classifier n_estimators=100 "
    print "Test Accuracy: ", accuracy_score(y[-100:], model1a.predict(df[-100:]))
    headers = ["name", "score"]
    values = sorted(zip(df.columns, model1a.feature_importances_), key=lambda x: x[1] * -1)
    print(tabulate(values, headers, tablefmt="plain"))
    return papa




# #BUY SELL YAPIYOR SON PARAYI BASACAK PREDICTE GORE
# totalmoney=1000000
# stock_bought=0
# for index, x in df[:-20].iterrows():
#     predicted_class=model1a.predict(x.reshape(1,-1))
#
#     if(predicted_class==1):
#         harca=totalmoney*0.1
#         stock_bought=stock_bought+harca/x['Close']
#         totalmoney=totalmoney*0.9
#     if(predicted_class==-1):
#         totalmoney=totalmoney+stock_bought*x['Close']
#         stock_bought=0
#
# print totalmoney
#
#
# #BUY SELL YAPIYOR SON PARAYI BASACAK GERCEK CEVABA GORE
# totalmoney=1000000
# stock_bought=0
# for index, x in data[:-20].iterrows():
#     predicted_class=x['Adj Close_class']
#
#     if(predicted_class==1):
#         harca=totalmoney*0.1
#         stock_bought=stock_bought+harca/x['Close']
#         totalmoney=totalmoney*0.9
#     if(predicted_class==-1):
#         totalmoney=totalmoney+stock_bought*x['Close']
#         stock_bought=0
#
# print totalmoney
#


# model2=SVC(gamma=2)
# papa1=model2.fit(df[:-100],y[:-100])
#
# print "Train Accuracy: ", accuracy_score(y[-100:], model2.predict(df[-100:]))
#
#
# model3=MLPClassifier()
# papa2=model3.fit(df[:-100],y[:-100])
#
# print "Train Accuracy: ", accuracy_score(y[-100:], model3.predict(df[-100:]))