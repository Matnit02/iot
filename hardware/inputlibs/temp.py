import os
import glob
import time

# Ścieżka do pliku z danymi czujnika
base_dir = '/sys/bus/w1/devices/'
device_folders = glob.glob(base_dir + '28*')
device_file=[]
if device_folders:
    device_file.append(device_folders[0] + '/w1_slave')
    device_file.append(device_folders[1] + '/w1_slave')
else:
    print("Czujnik nie został wykryty. Sprawdź połączenia i konfigurację 1-Wire.")
    exit(1)

def read_temp_raw(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp(filepath):
    lines = read_temp_raw(filepath)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

while True:
    print("Temperatura 1: ", read_temp(device_file[0]), "°C")
    print("Temperatura 2: ", read_temp(device_file[1]), "°C")
    time.sleep(1)
