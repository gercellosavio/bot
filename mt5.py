from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
 
# conectamos con MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
 
# solicitamos el estado y los parámetros de conexión
print(mt5.terminal_info())
# obtenemos la información sobre la versión de MetaTrader 5
print(mt5.version())
 
# solicitamos 1000 ticks de EURAUD
euraud_ticks = mt5.copy_ticks_from("EURAUD", datetime(2022,1,28,13), 1000, mt5.COPY_TICKS_ALL)
# solicitamos los ticks de AUDUSD en el intervalo 2019.04.01 13:00 - 2019.04.02 13:00
audusd_ticks = mt5.copy_ticks_range("AUDUSD", datetime(2022,1,27,13), datetime(2022,1,28,13), mt5.COPY_TICKS_ALL)
 
# obtenemos con distintos métodos las barras de diferentes instrumentos
eurusd_rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M1, datetime(2022,1,28,13), 1000)
eurgbp_rates = mt5.copy_rates_from_pos("EURGBP", mt5.TIMEFRAME_M1, 0, 1000)
eurcad_rates = mt5.copy_rates_range("EURCAD", mt5.TIMEFRAME_M1, datetime(2022,1,27,13), datetime(2022,1,28,13))
 
# finalizamos la conexión con MetaTrader 5
mt5.shutdown()
 
#DATA
print('euraud_ticks(', len(euraud_ticks), ')')
for val in euraud_ticks[:10]: print(val)
 
print('audusd_ticks(', len(audusd_ticks), ')')
for val in audusd_ticks[:10]: print(val)
 
print('eurusd_rates(', len(eurusd_rates), ')')
for val in eurusd_rates[:10]: print(val)
 
print('eurgbp_rates(', len(eurgbp_rates), ')')
for val in eurgbp_rates[:10]: print(val)
 
print('eurcad_rates(', len(eurcad_rates), ')')
for val in eurcad_rates[:10]: print(val)
 
#PLOT
# creamos un DataFrame de los datos obtenidos
ticks_frame = pd.DataFrame(euraud_ticks)
# dibujamos los ticks en el gráfico
plt.plot(ticks_frame['time'], ticks_frame['ask'], 'r-', label='ask')
plt.plot(ticks_frame['time'], ticks_frame['bid'], 'b-', label='bid')
 
# mostramos los rótulos
plt.legend(loc='upper left')
 
# añadimos los encabezados
plt.title('EURAUD ticks')
 
# mostramos el gráfico
plt.show()