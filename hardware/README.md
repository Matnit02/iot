# Non-`requirements.txt` prerequisites

## I2C

Install [Cicuit Python](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi) for I2C

TL;DR

```
cd ~
sudo apt install python3-venv
python3 -m venv venv --system-site-packages
source venv/bin/activate
pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo -E env PATH=$PATH python3 raspi-blinka.py
```

After reboot check with `ls /dev/i2c* /dev/spi*` to see if I2C ports are listed

## Other interfaces

Enable UART through `sudo raspi-config` > Interfaces

# `requirements.txt` install

Check if you're in venv, if not, run `source venv/bin/activate`

If you don't have `venv` folder, run `python -m venv venv`, then run command above

After entering `venv` (you should see `(venv)` at the beginning of your commandline prompt), run `pip install -r requirements.txt`
