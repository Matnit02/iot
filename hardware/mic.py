import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.IN)

while True:
  print(GPIO.input(5))
  time.sleep(0.1)

GPIO.cleanup()
