#!/usr/bin/env python3
import atexit
import re
import serial
import numpy as np
import matplotlib.pyplot as plt
import time
from load_model import *

### Variables
inputs=[]
data_save = []
start_time = time.time()

### Constants
# port_name = serial.Serial("COM4", 9600)
port_name = serial.Serial("/dev/ttyACM0", 9600)
folder = 'data_set/'
file_name = 'coral_take.txt'
fs = 16000

# Definir los parámetros para el espectrograma
win = np.hamming(1024)
nfft = 1024
hop = nfft // 2

# Constants from the data set adquisition
time_per_sample = 2
samples_per_record = int (3327)


def clean(port):
    port.close()
    print("Port closed")

atexit.register(clean, port=port_name)

while True:
    # print(len(data_save) < samples_per_record)
    if len(data_save) < samples_per_record:
        # print('recording')
        data = port_name.readline()
        data_str = data.decode()  # convierte bytes en una cadena
        # busca números enteros con signo
        numbers_only = re.findall(r'[-+]?\d+', data_str)
        for number in numbers_only:
            data_save += [number]
            # print(number)
    else:
        # Detener el temporizador
        end_time = time.time()

        # Calcular el tiempo transcurrido y mostrarlo
        elapsed_time = end_time - start_time
        # print("El ciclo tardó", elapsed_time, "segundos en ejecutarse.")
        data_array = np.array(data_save, dtype=np.float64) # convertir data_save a un vector NumPy de tipo float64
        spec, freqs, times, _ = plt.specgram(data_array, NFFT=nfft, Fs=fs, window=win, noverlap=hop, mode='magnitude')
        data_save = []
        spec = np.expand_dims(spec, axis=0)
        
        # Iniciar el temporizador
        start_time = time.time()
        prediction(spec,input_details,interpreter,output_details)
        # print(spec.shape)
    
