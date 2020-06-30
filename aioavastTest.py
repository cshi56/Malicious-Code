import asyncio
from aioavast import Avast
from tkinter.filedialog import askopenfilename

@asyncio.coroutine
def scan(item):
    av = Avast()
    yield from av.connect()
    return (yield from av.scan(item))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(scan('/Users/joecus1/Desktop/Career'))
    print(results)