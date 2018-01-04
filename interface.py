import matplotlib
matplotlib.use("TkAgg")
from Tkinter import *
from classification import classification
import backer
import pandas as pd
from backer import backer
from regressor import regressor,modelz
from matplotlib.figure import Figure
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import matplotlib.animation as animation
from matplotlib import style
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
import Tkinter as tk
import ttk
import pandas as pd
import copy

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import matplotlib.finance as mpf
import numpy as np
from sklearn import preprocessing


LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

style.use("ggplot")

f = plt.figure()

paneCount = 1

topIndicator = "none"
bottomIndicator = "none"
middleIndicator = "none"
chartLoad = True

darkColor = "#183A54"
lightColor = "#00A3E0"

EMAs = []
SMAs = []



class SeaofBTCapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Stock Prediction Project")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}

        for F in (StartPage, Prediction_Page):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        tk.Tk.iconbitmap(self, default="clienticon.ico")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=("""Use Stock Price Prediction Project at your own risk. \nThere is no promise of warranty."""), font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text="Agree",command=lambda: controller.show_frame(Prediction_Page))
        button1.pack()
        button2 = tk.Button(self, text="Disagree",command=quit)
        button2.pack()

class Prediction_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        bottom = tk.Frame(self)
        bottom.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        stocklabel = tk.Label(self, text="\nSelect your preferred Stock:" ,font=("Calibri", 16, 'bold'))
        stocklabel.pack()
        secondlabel = tk.Label(self, text="\nEnter number of days you want to predict:" ,font=("Calibri", 16, 'bold'))
        stockCsv = ttk.Combobox(self)
        stockCsv['values'] = (
        'Amgen Inc (AMGN)', 'Bank of America (BAC)', 'Equifax (EFX)', 'Facebook (FB)', 'Google (GOOG)', 'Verizon (VZ)')
        stockCsv.pack()
        firstlabel = tk.Label(self, text="\nEnter your balance in USD:" ,font=("Calibri", 16, 'bold'))

        initialMon = tk.StringVar()
        dayss = tk.StringVar()
        mEntry1 = tk.Entry(self, textvariable=initialMon)
        mEntry2 = tk.Entry(self, textvariable=dayss)

        firstlabel.pack()
        mEntry1.pack()
        secondlabel.pack()
        mEntry2.pack()

        riskLabel = tk.Label(self, text="\nSelect a risk setting:" ,font=("Calibri", 16, 'bold'))
        riskLabel.pack()
        risk = ttk.Combobox(self)
        risk['values'] = ('High Risk', 'Medium Risk', 'Low Risk')
        risk.pack()

        def callback():
            riskValue = risk.get()
            stockValue = stockCsv.get()
            mEntry1Label=mEntry1.get()
            mEntry2Label = mEntry2.get()

            if(riskValue=='' or stockValue=='' or len(mEntry1Label)==0 or len(mEntry2Label)==0 ):
                printable=''
                if (stockValue ==''):
                    printable = printable + "Select a stock!\n"
                if (len(mEntry1Label)==0):
                    printable = printable + "Enter your balance!\n"
                if (len(mEntry2Label)==0):
                    printable = printable + "Enter number of days!\n"
                if(riskValue==''):
                    printable= printable+"Select a risk setting!\n"

                outputlabel['text'] = printable
                outputlabel['fg'] = 'red'

            else:
                dff = 'Initialize'
                if (stockValue == stockCsv['values'][0]):
                    dff = pd.read_csv('merges/mergesAMGN.csv', index_col=0)
                if (stockValue == stockCsv['values'][1]):
                    dff = pd.read_csv('merges/mergesBAC.csv', index_col=0)
                if (stockValue == stockCsv['values'][2]):
                    dff = pd.read_csv('merges/mergesEFX.csv', index_col=0)
                if (stockValue == stockCsv['values'][3]):
                    dff = pd.read_csv('merges/mergesFB.csv', index_col=0)
                if (stockValue == stockCsv['values'][4]):
                    dff = pd.read_csv('merges/mergesGOOG.csv', index_col=0)
                if (stockValue == stockCsv['values'][5]):
                    dff = pd.read_csv('merges/mergesVZ.csv', index_col=0)

                deffer=copy.copy(dff)
                if (riskValue == 'High Risk'):
                    hunnit = backer(int(mEntry1.get()), classification(deffer, 'High',int(mEntry2.get())), deffer, 0, int(mEntry2.get()))[0][-1]

                if (riskValue == 'Medium Risk'):
                    hunnit = backer(int(mEntry1.get()), classification(deffer, 'Medium',int(mEntry2.get())), deffer, 0, int(mEntry2.get()))[0][-1]

                if (riskValue == 'Low Risk'):
                    hunnit = backer(int(mEntry1.get()), classification(deffer, 'Low',int(mEntry2.get())), deffer, 0, int(mEntry2.get()))[0][-1]

                val = int(mEntry1.get()) * (1.0 + (0.05 / 365))
                bank = [val]
                gold = [int(mEntry1.get())]
                golddf = pd.read_csv('stocks/GOLD.csv', index_col=0)
                for i in range(0, int(mEntry2.get()) - 1):
                    bank.append(bank[-1] * (1.0 + (0.05 / 365)))
                    finalGoldVal = golddf['Adj Close'][-int(mEntry2.get()) + i]
                    initialGoldVal = golddf['Adj Close'][-int(mEntry2.get())]
                    changeGold = (finalGoldVal - initialGoldVal) / initialGoldVal
                    goldReturn = str(int((1.0 + changeGold) * int(mEntry1.get())))
                    gold.append(goldReturn)

                hunnit = str(int(hunnit))
                printable = 'Your balance changed from $' + mEntry1.get() + ' to $' + hunnit + '\n\n'
                printable = printable + "In the mean time, your money would be:\n\n $" + str(
                    int(bank[-1])) + " in bank with 5% interest annually\n $" + gold[-1] + " if you invested in gold"


                outputlabel['text'] = printable
                outputlabel['fg'] = 'black'

                return dff

        b = tk.Button(self, text="PREDICT !", command= lambda:callback(), bg="blue")
        b.pack()


        def plotsPrice():
            dff = callback()
            toplevel = Toplevel()
            f = Figure()
            a = f.add_subplot(111)

            t = arange(int(mEntry2.get()))
            s = regressor(dff, modelz, int(mEntry2.get()))
            ll=dff['Adj Close']
            a.plot(t, s,label="Predicted Price")
            a.plot(t,ll,label="Actual Price")
            a.legend()
            a.set_ylabel('Price per Share ($)')
            a.set_xlabel('Days')
            canvas = FigureCanvasTkAgg(f, master=toplevel)
            canvas.set_window_title('Prediction')
            canvas.show()
            canvas._tkcanvas.pack()


        outputlabel = tk.Label(self, width=300, height=150,font=("Helvetica", 18))
        outputlabel.pack()


        def plotsStrategies():
            dff=callback()
            toplevel = Toplevel()
            val = int(mEntry1.get()) * (1.0 + (0.05 / 365))
            bank = [val]
            gold = [int(mEntry1.get())]
            golddf = pd.read_csv('stocks/GOLD.csv', index_col=0)
            for i in range(0, int(mEntry2.get()) - 1):
                bank.append(bank[-1] * (1.0 + (0.05 / 365)))
                finalGoldVal = golddf['Adj Close'][-int(mEntry2.get()) + i]
                initialGoldVal = golddf['Adj Close'][-int(mEntry2.get())]
                changeGold = (finalGoldVal - initialGoldVal) / initialGoldVal
                goldReturn = str(int((1.0 + changeGold) * int(mEntry1.get())))
                gold.append(goldReturn)
            print bank
            riskVal = risk.get()
            f = Figure()
            a = f.add_subplot(111)
            t = arange(int(mEntry2.get()))
            s = 'temp'
            if (riskVal == 'High Risk'):
                s = backer(int(mEntry1.get()), classification(dff, 'High',int(mEntry2.get())), dff, 0, int(mEntry2.get()))[0]
            if (riskVal == 'Medium Risk'):
                s = backer(int(mEntry1.get()), classification(dff, 'Medium',int(mEntry2.get())), dff, 0, int(mEntry2.get()))[0]
            if (riskVal == 'Low Risk'):
                s = backer(int(mEntry1.get()), classification(dff, 'Low',int(mEntry2.get())), dff, 0, int(mEntry2.get()))[0]
            print s

            a.plot(t, s, label="Strategy Result")
            a.plot(bank, label="Bank Result")
            a.plot(gold, label="Gold Result")
            a.legend()
            a.set_ylabel('Current Money ($)')
            a.set_xlabel('Days')
            canvas = FigureCanvasTkAgg(f, master=toplevel)
            canvas.show()
            canvas.set_window_title('Strategies')
            canvas._tkcanvas.pack()

        def listActions():
            dff = callback()
            riskVal = risk.get()
            s = 'temp'
            if (riskVal == 'High Risk'):
                s = backer(int(mEntry1.get()), classification(dff, 'High',int(mEntry2.get())), dff, 0, int(mEntry2.get()))[1]
            if (riskVal == 'Medium Risk'):
                s = backer(int(mEntry1.get()), classification(dff, 'Medium',int(mEntry2.get())), dff, 0, int(mEntry2.get()))[1]
            if (riskVal == 'Low Risk'):
                s = backer(int(mEntry1.get()), classification(dff, 'Low',int(mEntry2.get())), dff, 0, int(mEntry2.get()))[1]
            print s

        def candleStick():
            dff = callback()
            dff=dff[-int(mEntry2.get())-90:-int(mEntry2.get())]
            fig, ax = plt.subplots()
            mpf.candlestick2_ochl(ax, opens=dff['Open'], closes=dff['Close'], highs=dff['High'], lows=dff['Low'], width=2,
                                  colorup='g', colordown='r', alpha=0.75)
            ax.set_ylabel('Price per Share ($)')
            ax.set_xlabel('Days Before Prediction ')
            plt.show()

        def expoMov():
            dff = callback()
            dff = dff[-int(mEntry2.get()) - 90:-int(mEntry2.get())]

            fig, ax = plt.subplots()
            t = arange(90)
            ax.plot(t,dff['10dexpmv'], label="10D exp MA")
            ax.plot(t,dff['Adj Close'], label="Actual Price")
            ax.plot(t,dff['3dexpmv'], label="3D exp MA")
            ax.set_ylabel('Price per Share ($)')
            ax.set_xlabel('Days Before Prediction ')
            ax.legend()
            plt.show()

        candleStickButton=tk.Button(self, text="Candlestick Graph", command=lambda: candleStick())
        expMoving=tk.Button(self, text="Exp. MA Graph ", command=lambda: expoMov())
        priceButton = tk.Button(self, text="Adj. Close Prediction", command=lambda: plotsPrice())
        actionButton=tk.Button(self,text="Show Actions", command=lambda:listActions())
        strategyButton = tk.Button(self, text="Compare Strategies", command=lambda: plotsStrategies())
        backButton = tk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        backButton.pack(in_=bottom, side=TOP)
        priceButton.pack(in_=bottom, side=TOP)
        actionButton.pack(in_=bottom, side=TOP)
        strategyButton.pack(in_=bottom, side=TOP)
        candleStickButton.pack(in_=bottom, side=TOP)
        expMoving.pack(in_=bottom, side=TOP)




app = SeaofBTCapp()
app.geometry("520x700")
style = ttk.Style(app)
style.configure(app,background="black")
app.mainloop()
