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
            f"PM1.0: {int.from_bytes(buffer[10:12],'big')}","|",
            f"PM2.5: {int.from_bytes(buffer[12:14],'big')}","|",
            f"PM10: {int.from_bytes(buffer[14:16],'big')}","|",
            f"Data: {buffer[16:18].hex()}, {int.from_bytes(buffer[16:18],'big')}"," | ",
            f"Data: {buffer[18:20].hex()}, {int.from_bytes(buffer[18:20],'big')}"," | ",
            f"Data: {buffer[20:22].hex()}, {int.from_bytes(buffer[20:22],'big')}"," | ",
            f"Data: {buffer[22:24].hex()}, {int.from_bytes(buffer[22:24],'big')}"," | ",
            f"Data: {buffer[24:26].hex()}, {int.from_bytes(buffer[24:26],'big')}"," | ",
            f"Data: {buffer[26:28].hex()}, {int.from_bytes(buffer[26:28],'big')}"," | ",
            f"Data: {buffer[28:30].hex()}, {int.from_bytes(buffer[28:30],'big')}"," | ",
            f"Temp: {int.from_bytes(buffer[30:32],'big')/10}"," | ",
            f"Humi: {int.from_bytes(buffer[32:34],'big')/10}"," | ",
            f"Data: {buffer[34:36].hex()}, {int.from_bytes(buffer[34:36],'big')}"," | ",
            f"Data: {buffer[36:38].hex()}, {int.from_bytes(buffer[36:38],'big')}"," | ",
            f"Data: {buffer[38:40].hex()}, {int.from_bytes(buffer[38:40],'big')}")
    buffer = b''
  sleep(0.02)
