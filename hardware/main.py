import time
from inputlibs.mic import Microphone
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
