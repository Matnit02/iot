import time, asyncio, requests
from inputlibs.mic import Microphone
from inputlibs.air import Air
from inputlibs.proxy import Proximity


mic = Microphone()
mic.setup(5)
proxy = Proximity()
proxy.setup()
air = Air()
air.setup("/dev/ttyS0")

time.sleep(1)

while True:
  print(proxy.read())
  print(mic.read())
  print(asyncio.run(air.read()))

#r = requests.post('SOME URL', data={'mic': mic.read(), 'proxy': proxy.read(), 'air': asyncio.run(air.read())})

proxy.clean()
mic.clean()
air.clean()
