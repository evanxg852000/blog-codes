'''Types
Errors -
Simple String +
Integers :
Bulk String $
Arrays *

https://redis.io/topics/protocol
'''
import asyncio

def encode(data, simple_str=False):
    if isinstance(data, ValueError):
        return f'-{str(data)}\r\n' 
    elif isinstance(data, str) and simple_str:
        return f'+{data}\r\n'
    elif isinstance(data, int):
        return f':{data}\r\n'
    elif isinstance(data, str):
        return f'${len(data)}\r\n{data}\r\n'
    elif isinstance(data, list) or isinstance(data, tuple):
        enc = f'*{len(data)}\r\n'
        for itm in data:
            enc += encode(itm)
        return enc

def decode(data):
    marker = data[0]
    if marker == '-':
        return str(data[1:-2])
    elif marker == '+':
        return str(data[1:-2])
    elif marker == ':':
        return int(data[1:-2])
    elif marker == '$':
        parts = data[1:].split('\r\n')
        ln = int(parts[0])
        if ln == -1:
            return None
        elif ln == 0:
            return ''
        else:
            return str(parts[1])
    elif marker == '*':
        parts = data[1:].split('\r\n')
        ln = int(parts[0])
        items = [None] * ln
        for i in range(1, 1+ln):
            items[i-1] = decode(f'{parts[i]}\r\n')
        return items
    else:
        raise Exception('resp decoding error')


class Client():
    def __init__(self, evt_loop):
        self.event_loop = evt_loop
        self.reader = None
        self.writer = None

    async def execute(self, cmd):
        if self.reader == None:
            if cmd.startswith('.connect'):
                cmd = cmd.replace('.connect', '').strip()
                parts = cmd.split(':')
                (r, w) = await asyncio.open_connection(parts[0], parts[1], loop=self.event_loop)
                self.reader = r
                self.writer = w
            else:
                return 'Please connect with <.connect ip:port>'
        else:
            cmd = cmd.split(' ')
            self.writer.write(encode(cmd).encode())
            data = await self.reader.read(1024)
            return decode(data.decode())

    def close(self):
        if self.writer != None:
            self.writer.close()

