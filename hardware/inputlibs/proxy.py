import board
import busio
import adafruit_apds9960.apds9960

class Proximity:
  def setup(self):
    self.i2c = busio.I2C(board.SCL, board.SDA)
    self.sensor = adafruit_apds9960.apds9960.APDS9960(self.i2c)
    self.sensor.enable
    self.sensor.enable_proximity = True
    self.sensor.enable_color = True
    self.sensor.enable_gesture = True
  def read(self):
    return {"Proximity": self.sensor.proximity,
            "Colors": self.sensor.color_data,
            "Gesture": self.sensor.gesture()}
  def clean(self):
    pass




