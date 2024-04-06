##################################################################################
# CÁLCULO DE MAGNITUD LOCAL EVENTOS DE CALVING, GLACIAR PERITO MORENO, PATAGONIA.

# Elaboracion	: Edgardo A. Casanova Pino, Mayo-2023
# Modificacion	: Edgardo A. Casanova Pino, Enero-2024
# Ej Lanzamiento: python3 magnitud_calving_py3.py
##################################################################################

# MODULOS
#-*-coding: utf-8-*-
import matplotlib.pyplot as plt
from math import log10
from obspy import UTCDateTime, read
from obspy.geodetics import gps2dist_azimuth


# Direccionar a los archivos del día a analizar
st_Z = read('/Users/valeriarojas/Desktop/6dic_C.GO09..BHZ')
#st_E += read('XXX') 		# cuando evento necesita la siguiente traza diaria se agrega día en canal E y N.
#st_E.merge(method=1, fill_value='latest')
st_Z_2 = st_Z.copy()

# Parámetros sensores Trilliun 240 Sec Response sn 0-399 y Wood-Anderson (WA)
paz_trillium240 = {'gain': 1193.95,
		'poles': [-0.01813 + 0.01813j,
                        -0.01813 - 0.01813j,
                        -124.9 + 0j,
			-197.5 + 256.1j,
			-197.5 - 256.1j, 
			-569 + 1150j,
			-569 - 1150j],
		'sensitivity': 500778926.08,
		'zeros': [0 + 0j,
                         0 + 0j,   
                        -90 + 0j,
			-164.2 + 0j,
			-3203 + 0j]}

# (antiguos parámetros WA)
#paz_wa = {'sensitivity': 2800, 'zeros': [0j], 'gain': 1, 
#          'poles': [-6.2832 - 4.7124j, -6.2832 + 4.7124j]}

# Nueva recomendación IASPEI 2011, WA
paz_wa = {'sensitivity': 2080, 'zeros': [0 + 0j, 0 + 0j], 'gain': 1,
          'poles': [-5.49779 - 5.60886j, -5.49779 + 5.60886j]}


# Simular componentes en WA
st_Z_2.simulate(paz_remove=paz_trillium240, paz_simulate=paz_wa, water_level=10)

# Hora de evento de calving y ventana de tiempo
time = UTCDateTime('2023-12-06T14:24:50') 	# en formato año-mes-diaThora:minuto:segundo
print('Evento de Calving Glaciar Grey:', time)

st_Z_2.trim(time - 10, time + 20) # graficar segundos antes de inicio traza y segundos despues de termino de evento
tr_Z = st_Z_2[0]

# Calcular amplitudes máximas en WA
tr_Z = st_Z_2[0]
ampl_Z = max(abs(tr_Z.data))
print('Amplitud Maxima WA (mm):', ampl_Z)

#Coordenadas Estación GO09
sta_lat = -51.2707
sta_lon = -72.3381

#Coordenadas Evento Calving
event_lat = -50.993000
event_lon = -73.233300

# Cálculo de distancia a evento de calving
epi_dist, az, baz = gps2dist_azimuth(event_lat, event_lon, sta_lat, sta_lon)
epi_dist = epi_dist / 1000  	# Para pasar de metros a kilómetros


# Magnitud Local (fórmula empírica de Lillie)
ml_1 = log10(ampl_Z) - 2.48 + 2.76*log10(epi_dist) 

# Magnitud Local (IASPEI, 2011, ecuación estándar sismos corticales)
ml_2 = log10(ampl_Z) + 1.11*log10(epi_dist) + 0.00189*(epi_dist) - 2.09 

print('Distancia Epicentral (km):', epi_dist)
print('Magnitud Local 1 (Ml):', ml_1)
print('Magnitud Local 2 (ML):', ml_2)
