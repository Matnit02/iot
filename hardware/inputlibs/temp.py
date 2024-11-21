import os
import glob
import time

class Temperature():
  def setup(self):
    base_dir = '/sys/bus/w1/devices/'
    device_folders = glob.glob(base_dir+'28*')
    self.device_file = []
    if device_folders:
      self.device_file.append(device_folders[0] + '/w1_slave')
      self.device_file.append(device_folders[1] + '/w1_slave')
    else:
      raise Exception('W1 not found')
  def read(self):
    return {"temp1":self.read_temp(self.device_file[0]),"temp2":self.read_temp(self.device_file[1])}
  def clean(self):
    pass

  def read_temp_raw(self,filepath):
    with open(filepath, 'r') as f:
      lines = f.readlines()
    return lines

  def read_temp(self,filepath):
    lines = self.read_temp_raw(filepath)
    while lines[0].strip()[-3:] != 'YES':
      time.sleep(0.2)
      lines = self.read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
      temp_string = lines[1][equals_pos + 2:]
      temp_c = float(temp_string) / 1000.0
      return temp_c
