from VNDB import *
from logbook import Logger, StreamHandler
import sys
import asyncio

StreamHandler(sys.stdout).push_application()
log = Logger("Shosetsu")
log.info("Shosetsu Imported")

test = Shosetsu()
loop = asyncio.get_event_loop()
loop.run_forever()