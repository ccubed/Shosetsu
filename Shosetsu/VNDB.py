import asyncio
import ujson
from curses.ascii import EOT
from logbook import Logger

class Shosetsu:
    def __init__(self, username=None, password=None, loop=None):
        self.username = username
        self.password = password
        self.logtxt = Logger("Shosetsu")

        if loop is None:
            self.loop = asyncio.get_event_loop()
        else:
            self.loop = loop

        ret = loop.create_task(asyncio.open_connection(host='api.vndb.org', port='19535', ssl=True, server_hostname='api.vndb.org'))
        ret.add_done_callback(self._grab_reader_writer)

    def _grab_reader_writer(self, future):
        self.reader = future.result()[0]
        self.writer = future.result()[1]
        self.loop.create_task(self.VNDB_login)

    async def VNDB_login(self):
        if self.username and self.password:
            jsd = ujson.dumps({'protocol': 1, 'client': 'Shosetsu', 'Clientver': '0.1', 'username': self.username, 'password': self.password})
        else:
            jsd = ujson.dumps({'protocol': 1, 'client': 'Shosetsu', 'Clientver': '0.1'})
        self.writer.write("login {}{}".format(jsd, EOT))
        data = await self.reader.readuntil(EOT)
        if data.startswith('ok'):
            self.login = True
        else:
            self.writer.close()
            raise ConnectionRefusedError("VNDB says no. Going down.")