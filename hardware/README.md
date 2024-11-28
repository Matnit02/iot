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

## UART

Enable UART through `sudo raspi-config` > Interfaces

## 1-wire

Enable 1-wire through `sudo raspi-config`

Add 

```
dtoverlay=w1-gpio,gpiopin=20
dtoverlay=w1-gpio,gpiopin=21
```

to `/boot/firmware/config.txt` (with `sudo nano`)

After reboot check `cd /sys/bus/w1/devices` to see temperature sensor

# `requirements.txt` install

Check if you're in venv, if not, run `source venv/bin/activate`

If you don't have `venv` folder, run `python -m venv venv`, then run command above

After entering `venv` (you should see `(venv)` at the beginning of your commandline prompt), run `pip install -r requirements.txt`

# Crontab

Verify you have crontab running with `/etc/init.d/cron status` (or its systemd equivalent)

Run `sudo nano /etc/crontab`, and add `* * * * * root /home/raspberrypi/iot/hardware/venv/bin/python /home/raspberrypi/iot/hardware/main.py >/var/log/water_sensor_cron.log 2>&1`

Keep in mind that the above command will change depending on location of this project
