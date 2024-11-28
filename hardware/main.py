import time, asyncio, requests, logging
from logging.handlers import RotatingFileHandler
from inputlibs.air import Air
from inputlibs.proxy import Proximity
from inputlibs.pres import Pressure
from inputlibs.temp import Temperature

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
log_handler = RotatingFileHandler("/var/log/water_sensor.log", mode = "a", maxBytes=1024*1024, backupCount=2, encoding=None, delay=0)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)

url = "https://waterlomonitorlo.azurewebsites.net/streamdata/"

api_key = "test_api_key_5"

logger.info("Started")

proxy = Proximity()
proxy.setup()
air = Air()
air.setup("/dev/ttyS0")
pres = Pressure()
pres.setup()
temp = Temperature()
try:
  temp.setup()
except Exception as err:
  logger.error(err)

time.sleep(1)

data = {}
try:
  data["brightness"] = proxy.read()
except Exception as err:
  data["brightness"] = "error"
  logger.error(err)

try:
  ret = asyncio.run(air.read())
  i=0
  while ret["status"] == "fail" and i<3:
    i+=1
    ret = asyncio.run(air.read())
  if ret["status"] == "fail":
    data["air"] = {"status": "error"}
  else:
    data["air"] = ret
except Exception as err:
  data["air"] = {"status": "error"}
  logger.error(err)

try:
  data["pressure"] = pres.read()
except Exception as err:
  data["pressure"] = "error"
  logger.error(err)

try:
  data["temperature"] = temp.read()
except Exception as err:
  data["temperature"] = "error"
  logger.error(err)

logger.debug("Got sensor data")
logger.debug(data)

#r = requests.post('SOME URL', data={'mic': mic.read(), 'proxy': proxy.read(), 'air': asyncio.run(air.read())})
payload = {
    "api_key": api_key,
    "location_latitude": 50.046700,  # Przykładowe współrzędne
    "location_longitude": 19.779300,
    "data": {
        "atmospheric_pressure": data.get("pressure", {}).get("sea_level_pressure", "error"),
        "water_temperature": data.get("temperature", {}).get("temp1", "error"),
        "air_temperature": data.get("temperature", {}).get("temp2", "error"),
        "pm1_0": data.get("air", {}).get("pm_1.0", "error"),
        "pm2_5": data.get("air", {}).get("pm_2.5", "error"),
        "pm10": data.get("air", {}).get("pm_10", "error"),
        "noise_level": 50,  # Przykładowa wartość
        "light_intensity": data.get("brightness", "error"),
    }
}
logger.debug("Setup payload")
logger.debug(payload)

# Wysyłanie danych na backend
headers = {"Content-Type": "application/json"}
try:
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        logger.info("Data succesfully sent")
    else:
        logger.error(f"Error during data transfer! Error code: {response.status_code}, Response: {response.text}")
except Exception as e:
    logger.error(f"Network error during data transfer: {e}")

#time.sleep(60) #wysyłanie co 60 sekund

proxy.clean()
air.clean()
pres.clean()
try:
  temp.clean()
except:
  pass
#print(data)

logger.info("Finished")
