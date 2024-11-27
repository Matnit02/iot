import serial
from time import sleep
from termcolor import colored

ser = serial.Serial("/dev/ttyS0",9600)
ser.reset_input_buffer()
buffer = b''
miss = 0
while True:
  if ser.in_waiting>0:
    #print(ser.in_waiting)
    miss = 0
    received_data = ser.read(ser.in_waiting)
    buffer += received_data
  else:
    miss+=1
    #print(miss)
  if miss > 5 and len(buffer)>0:
    if not len(buffer.hex()) == 80:
      print(f"{len(buffer.hex())}: ",colored(f"{buffer.hex()}","red"))
    else:
      print(colored(f"{len(buffer.hex())}: ","green"),
            f"Header: {buffer[0:2].hex()}","|",
            f"Frame Length: {int.from_bytes(buffer[2:4],'big')}","|",
            f"PM 1.0: {int.from_bytes(buffer[10:12],'big')}μg/m3","|",
            f"PM 2.5: {int.from_bytes(buffer[12:14],'big')}μg/m3","|",
            f"PM 10: {int.from_bytes(buffer[14:16],'big')}μg/m3","|",
            f"0.3μm: {int.from_bytes(buffer[16:18],'big')}","|",
            f"0.5μm: {int.from_bytes(buffer[18:20],'big')}","|",
            f"1.0μm: {int.from_bytes(buffer[20:22],'big')}","|",
            f"2.5μm: {int.from_bytes(buffer[22:24],'big')}","|",
            f"5.0μm: {int.from_bytes(buffer[24:26],'big')}","|",
            f"10μm: {int.from_bytes(buffer[26:28],'big')}","|",
            f"Temp: {int.from_bytes(buffer[30:32],'big')/10}","|",
            f"Humi: {int.from_bytes(buffer[32:34],'big')/10}","|",
            f"CRC: {int.from_bytes(buffer[38:40],'big')}","|",
            f"CR2: {sum(buffer[0:38])}")
    buffer = b''
  sleep(0.02)
