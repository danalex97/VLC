import serial
import time
import sys

import threading
from threading import Lock


class Device():
    def __init__(self, address):
        self.serial = serial.Serial('/dev/ttyACM0', 115200, timeout = 1)
        time.sleep(2)

        # for listening
        self.buffer = []
        self.lock = Lock()
        self.listener = threading.Thread(target=self.listen)
        self.listener.start()

        # initialize
        self._send("a[{}]".format(address))
        self._read()

    def stop(self):
        self.listener.join()

    def listen(self):
        def _read(timeout=0):
            """ reads from serial port until \n """

            message = ""
            byte = ""
            while byte != "\n":
                byte = self.serial.read(1)
                byte = byte.decode('UTF-8')

                if byte != "\n":
                    message += byte
            return message

        while True:
            message = _read()

            self.lock.acquire()
            self.buffer.append(message)
            self.lock.release()

    def _send(self, message):
        """ send message to serial port """

        self.serial.write(str.encode(message + "\n"))
        time.sleep(0.5)

    def _read(self):
        message = None

        self.lock.acquire()
        if len(self.buffer) > 0:
            message = self.buffer[0]
            self.buffer = self.buffer[1:]
        self.lock.release()

        return message

    def set_retransmissions(self, nbr):
        self._send("c[1,0,{}]".format(nbr))
        print(self._read())

    def set_FEC(self, size):
        self._send("c[0,1,{}]".format(size))
        print(self._read())

    def send_message(self, message, dest):
        self._send("m[{}\0,{}]".format(message, dest))
        print(self._read())

    def broadcast(self, message):
        self.send_message(message, "FF")

if __name__ == "__main__":
    d = Device("AB")

    d.set_retransmissions(5)
    d.set_FEC(30)

    d.send_message("hello world", "CD")
    d.stop()
