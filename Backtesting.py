totalMoney = 1000000
trainingdata = []


def backtesting(trainingWindow, data, model):
    for a in range(0,len(data)-trainingWindow-1):
        endpoint=trainingWindow+a
        windowData = data[a:endpoint]
        nextdayPrice =data[endpoint]

        totalMoney = totalMoney + backtesting_helper(windowData, nextdayPrice, totalMoney, model)
    return totalMoney

def backtesting_helper(traindata, nextdayPrice, totalMoney, model,nextday):
    model.train(traindata)
    a = model.predict(nextday)
    if(a=='buy'):
        return (nextdayPrice - traindata.lastelement)* totalMoney
    if(a=='sell'):
        return (traindata.lastelement -nextdayPrice) *totalMoney