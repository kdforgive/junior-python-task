import time
import random
import asyncio
from threading import Thread

from data import data


chunk_len = random.randint(500, 1500)
chunks = [(index, data[i:i+chunk_len])
          for index, i in enumerate(range(0, len(data), chunk_len))]
random.shuffle(chunks)


async def handle_client(reader, writer):
    print("connected")
    gen = (index.to_bytes(1, byteorder="big") + chunk for index, chunk in chunks)
    while True:
        data = await reader.read(1024)
        if not data:
            break
        if data.replace(b"\n", b"") != b"next":
            writer.close()
            break
        try:
            data = next(gen)
        except StopIteration:
            writer.close()
            break
        writer.write(data)
        await writer.drain()
    print("disconnected")


async def server():
    await asyncio.start_server(handle_client, host="localhost", port=8888)


def main():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(server())
    loop.run_forever()


Thread(target=main, daemon=True).start()
time.sleep(1)

__all__ = []