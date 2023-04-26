import atexit
import re
import serial

# Constants
port_name = serial.Serial("COM6", 9600)
file_name = 'Audios/audio1.txt'

file = open(file_name, 'w')


def clean(port):
    port.close()
    file.close()
    print("File save successfully and port closed")


atexit.register(clean, port=port_name)

while True:
    data = port_name.readline()
    data_str = data.decode()  # convierte bytes en una cadena
    # busca números enteros con signo
    numbers_only = re.findall(r'[-+]?\d+', data_str)
    for number in numbers_only:
        file.write(number + '\n')
        print(number)
