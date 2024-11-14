import time
import os
import RPi.GPIO as GPIO

class Microphone:
  pin_id = 0
  def setup(self, pin_id: int):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_id, GPIO.IN)
    self.pin_id=pin_id

  def read(self):
    return GPIO.input(self.pin_id)

  def clean(self):
    GPIO.cleanup()
