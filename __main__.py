from PySide2 import QtWidgets, QtGui
import asyncio
import os
import server  # DON`T REMOVE
PICTURE_NAME = 'output.jpg'


async def receive_data(message: str) -> None:
    reader, writer = await asyncio.open_connection('localhost', 8888)
    hash_map = {}
    while True:
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(2048)
        if not data:
            writer.close()
            await writer.wait_closed()
            write_data(hash_map)
            break
        # dict key is decoded serial number from first byte, value the rest of the chunk
        hash_map[int.from_bytes(data[:1], byteorder="big")] = data[1:]


def write_data(hash_map: dict) -> None:
    with open(PICTURE_NAME, 'ab') as w_file:
        # sort dict by keys, and write chunks in correct order
        for i in sorted(hash_map.keys()):
            w_file.write(hash_map[i])


def client() -> str:
    path_to_image = os.path.abspath(PICTURE_NAME)
    return path_to_image


def main():
    asyncio.run(receive_data('next'))
    path = client()
    app = QtWidgets.QApplication([])
    label = QtWidgets.QLabel()
    label.setMinimumSize(100, 100)
    label.setPixmap(QtGui.QPixmap(path))
    label.show()
    app.exec_()


if __name__ == '__main__':
    main()
