import serial
import asyncio

class Air:
  def config(self, port: str):
    self.ser = serial.Serial(port,9600)
    self.ser.reset_input_buffer()

  async def read():
    buffer = b''
    miss = 0

    while True:
      if ser.in_waiting>0:
        miss = 0
        received_data = ser.read(ser.in_waiting)
        buffer += received_data
      else:
        miss+=1


      if miss > 5 and len(buffer)>0:
        if not len(buffer.hex()) == 80:
          return {"status": "fail", "error": "length", "length": len(buffer.hex())}
        calc_cr = sum(buffer[0:38])
        if not calc_cr == int.from_bytes(buffer[38:40]):
          return {"status": "fail", "error": "crc", "cr1":int.from_bytes(buffer[38:40]), "cr2": calc_cr}
        return {"status": "success", "length": len(buffer.hex())}
              "PM 1.0":int.from_bytes(buffer[10:12],'big'),
              "PM 2.5":int.from_bytes(buffer[12:14],'big'),
              "PM 10":int.from_bytes(buffer[14:16],'big'),
              "0.3um":int.from_bytes(buffer[16:18],'big'),
              "0.5um":int.from_bytes(buffer[18:20],'big'),
              "1.0um":int.from_bytes(buffer[20:22],'big'),
              "2.5um":int.from_bytes(buffer[22:24],'big'),
              "5.0um":int.from_bytes(buffer[24:26],'big'),
              "10um":int.from_bytes(buffer[26:28],'big'),
              "temp":int.from_bytes(buffer[30:32],'big')/10,
              "humi":int.from_bytes(buffer[32:34],'big')/10}
      asyncio.sleep(0.02)
  def clean(self):
    pass
