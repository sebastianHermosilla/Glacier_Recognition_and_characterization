####################################################################
# Grafica 1 dia de Estacion PMOR, GLACIAR PERITO MORENO, PATAGONIA.

# Elaboracion	: Edgardo A. Casanova Pino, Mayo-2023
# Modificacion	: Edgardo A. Casanova Pino, Enero-2024
# Ej Lanzamiento: python3 dayplot_py3.py
####################################################################

# MODULO
from obspy.core import read

# Direccionar archivo de dia a analizar
st_Z = read('/Users/valeriarojas/Desktop/26dic_C.GO09..BHZ')
print(st_Z) # para corroborar dia


# Filtrado de la traza
st_Z.filter('bandpass', freqmin=1, freqmax=5)

# Generar Dayplot y leyenda
st_Z.plot(type='dayplot', interval=60, right_vertical_labels=False, one_tick_per_line=True, number_of_ticks=31, tick_format='%d/%m %Hh',title='Estación Cerro Castillo (GO09), 26/12/23, canal HHZ, 200 sps, filtro: bandpass 1 - 5 Hz')
