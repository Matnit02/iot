import time, asyncio, requests, logging
from logging.handlers import RotatingFileHandler
from inputlibs.air import Air
from inputlibs.proxy import Proximity
from inputlibs.pres import Pressure
from inputlibs.temp import Temperature

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
log_handler = RotatingFileHandler("log.txt", mode = "a", maxBytes=1024*1024, backupCount=2, encoding=None, delay=0)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

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

#r = requests.post('SOME URL', data={'mic': mic.read(), 'proxy': proxy.read(), 'air': asyncio.run(air.read())})

proxy.clean()
air.clean()
pres.clean()
try:
  temp.clean()
except:
  pass
print(data)

logger.info("Finished")
