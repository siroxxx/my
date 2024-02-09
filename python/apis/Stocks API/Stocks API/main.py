# Author: Yasser Khaloufi
# Date: 01/02/2024

# Consegna:
"""
Crea un grafico (plot) che mostra l'andamento di un'asset nell'arco di un mese ( apertura e chiusura ),
usando le api di seguito:
-www.alphavantage.co
-polygon.io

"""

# Appunto: non per forza hai bisogno di un solo valore per ogni giorno del mese interessato,
#          anzi è meglio estrarre più di un valore per ogni giorno, in modo da poter fare un
#          grafico più preciso.
# 
# Esempio Apple gennaio 2024:
# https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&month=2024-01&outputsize=full&apikey=YLEIKH36XS8BP6KX

from secret import *
from alphavantage import alphavantageApiManager as alpha
from polygon import polygonApiManager as polygon
from plot import plotter

"""
  LEGGI:
  - Polygon API approssima a sole due cifre decimali, mentre alphavantae a quattro.
  - Polygon API usa il timestamp in millisecondi, mentre alphavantage in secondi.
  - Polygon non sempre dispone di dati ogni 5 minuti, quindi fa dei salti nel campionare.
  - Le due API iniziano dal secondo giorno del mese in quanto probabilmente il primo giorno
    non era giorno di scambio.
  - Le due curve sono leggermente sfasate, anche se seguono lo stesso andamento, devo ancora capire perchè.
"""

# Esempio Apple gennaio 2024:
data = alpha.get_data("AAPL", "01", "2024", API_KEY_ALPHAVANTAGE)
data = alpha.extract_data(data)
data_polygon = polygon.get_data("AAPL", "01", "2024", API_KEY_POLYGON)
data_polygon = polygon.extract_data(data_polygon)
plotter.plot_data(data, data_polygon)

"""
    Giusto per fare chiarezza:
    - I dati di un titolo presi in un certo mese sono campionati ogni 5 minti di quest'ultimo,
      di conseguenza i valori di apertura e chiusura sono presi ogni 5 minuti.
"""