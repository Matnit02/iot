import time, asyncio
from inputlibs.mic import Microphone
from inputlibs.uart import Air
from inputlibs.proxy import Proximity

mic = Microphone()
mic.setup(5)
print(mic.read())
mic.clean()

proxy = Proximity()
proxy.setup()
time.sleep(1)
print(proxy.read())
proxy.clean()

air = Air()
air.setup("/dev/ttyS0")
print(asyncio.run(air.read()))
air.clean()
