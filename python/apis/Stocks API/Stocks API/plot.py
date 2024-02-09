from matplotlib.pyplot import plot, legend, show

class plotter:

    # Crea il grafico a partire dai dati estratti da alphavantage e polygon per una certa azione in un certo mese ogni 5 minuti dello stesso.
    """
        Nel momento in cui questa funzione viene chiamata, i dati delle due diverse API sono già stati estratti e trasformati in dizionari
        che contengono solo le informazioni essenziali (i campioni) per la creazione del grafico.
        Per ogni ciascuna API disegno sia la curva di apertura che quella di chiusura.
    """
    def plot_data(data_alpha, data_polygon):
        """
            La funzione plot necessita di due liste di valori, una per l'asse x che da il nome ad ogni campione (che in questo caso è la data-orario di ogni campione, 
            quindi la chiave di ogni campione nel dizionario data) e una per l'asse y, cioè i valori effettivi e poi, opzionalmente, il nome della curva disegnata.
        """
        # I valori di alphavantage hanno bisogno di essere convertiti in float, in quanto sono stringhe, mentre quelli di polygon sono già float nel JSON.
        plot(data_alpha.keys(), [float(d["1. open"]) for d in data_alpha.values()], label="Open alphavantage")
        plot(data_alpha.keys(), [float(d["4. close"]) for d in data_alpha.values()], label="Close alphavantage")
        plot(data_polygon.keys(), [d["o"] for d in data_polygon.values()], label="Open Polygon")
        plot(data_polygon.keys(), [d["c"] for d in data_polygon.values()], label="Close Polygon")
        legend()
        show()