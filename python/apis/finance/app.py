from finance import *
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates

while True:
    print("Inserisci l'asset che desideri analizzare")
    asset = input()
    print("Inserisci la data iniziale")
    start = input()
    print("Inserisci la data finale")
    end = input()
    
    # Ottenimento dei dati storici
    datex, apertura, chiusura, massimo, minimo = getBilancioDaA(asset, start, end)
    
    if datex is not None:
        # Converti le date in formato datetime

        # Creazione del grafico a candele
        dates = [datetime.strptime(date, "%Y-%m-%d").date() for date in datex]

        # Creazione del grafico a candele
        fig, ax = plt.subplots()
        ax.xaxis_date()

        candele = ax.plot_date(mdates.date2num(dates), apertura, '-', label='Apertura')
        candele += ax.plot_date(mdates.date2num(dates), chiusura, '-', label='Chiusura')

        for i in range(len(dates)):
            # Linea verticale per il minimo e il massimo
            ax.vlines(dates[i], minimo[i], massimo[i], color='black', linewidth=2)

        # Aggiungi titoli e legenda
        plt.title('Grafico a Candele')
        plt.xlabel('Date')
        plt.ylabel('Valore')
        plt.legend()

        # Formattazione della data sull'asse x
        plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))

        # Visualizzazione del grafico
        plt.show()
