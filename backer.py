
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from classification import classification
from termcolor import colored
def backer(initialMoney, model, dataframe,stock_bought,days):
    days=-days
    change=[[],[]]
    day=0
    for index, x in dataframe[days:].iterrows():
        predicted_class = model.predict(x.reshape(1, -1))
        day+=1
        if (predicted_class == 1):
            harca = initialMoney * 0.1
            stock_bought = stock_bought + harca / x['Close']
            print colored("BUY ", 'green') + "Current Money: " + "%.2f" % initialMoney + " Number of Shares: " + "%.2f" % stock_bought + "  Day: " + str(day)
            initialMoney = initialMoney * 0.9
            change[0].append(initialMoney)
            change[1].append("BUY")

        if (predicted_class == -1):
            initialMoney = initialMoney + stock_bought * x['Close']
            print colored("SELL ",'red')+"Current Money: " + "%.2f" % initialMoney + " Number of Shares: " + "%.2f" % stock_bought + "  Day: " + str(day)
            stock_bought = 0
            change[0].append(initialMoney)
            change[1].append("SELL")
        if(predicted_class==0):
            print colored("HOLD ", 'yellow') + "Current Money: " + "%.2f" % initialMoney + " Number of Shares: " + "%.2f" % stock_bought + "  Day: " + str(day)
            change[0].append(initialMoney)
            change[1].append("HOLD")

    if(stock_bought>0):
        initialMoney=initialMoney+stock_bought * dataframe['Close'][-1]
        print "Final Money: "+ "%.2f" % initialMoney
        change[0][-1]=initialMoney
    return change

#
