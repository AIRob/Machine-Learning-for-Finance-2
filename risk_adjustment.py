def buy_sell_holdHigh(column):
    requirement=0.0
    if column>requirement:
        return 1
    if column<-requirement:
        return -1
    return 0

def buy_sell_holdMedium(column):
    requirement=0.005
    if column>requirement:
        return 1
    if column<-requirement:
        return -1
    return 0

def buy_sell_holdLow(column):
    requirement=0.010
    if column>requirement:
        return 1
    if column<-requirement:
        return -1
    return 0

