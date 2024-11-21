import time
import board
import busio
import bmp180

class Pressure():
  def setup(self, sampling = 2, height = 383):
    i2c = board.I2C()
    self.sensor = bmp180.BMP180(i2c)
    self.sensor.oversampling = sampling
    self.height = height
  def read(self):
    temp = self.sensor.temperature
    pres = self.sensor.pressure
    pres_on_sea = pres / (1 - (self.height / 44330.0))**5.255
    return {"temperature": temp, "absolute_pressure": pres, "sea_level_pressure": pres_on_sea}
  def clean(self):
    pass
