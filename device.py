import signal
import serial
import time
import sys

import threading
from threading import Lock

class Device():
    def __init__(self, device, address):
        self.serial = serial.Serial(device, 115200, timeout = 1)
        time.sleep(2)

        # check loop
        self.funcs = []
        self.stopped = False

        # for listening
        self.buffer = []

        # initialize
        self._send("a[{}]".format(address), wait=True)

        def signal_handler(sig, frame):
            self.stopped = True
            self.listener.join()
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)

    def check_loop(self, func):
        self.funcs.append(func)

    def _listen(self):
        message=""
        while True:
            try:
                byte = self.serial.read(1)
                byte = byte.decode('UTF-8')

                if byte == '\n':
                    return message
                else:
                    message = message + byte
            except serial.SerialException:
                continue  # on timeout try to read again
            except KeyboardInterrupt:
                sys.exit()  # on ctrl-c terminate program

    def listen(self):
        while not self.stopped:
            mess = self._listen()
            for f in self.funcs:
                f(mess)

    def _send(self, message, wait=False):
        """ send message to serial port """

        self.serial.write(str.encode(message + "\n"))
        if wait:
            time.sleep(0.2)

    def set_retransmissions(self, nbr):
        self._send("c[1,0,{}]".format(nbr), wait=True)

    def set_FEC(self, size):
        self._send("c[0,1,{}]".format(size), wait=True)

    def send_message(self, message, dest):
        self._send("m[{}\0,{}]".format(message, dest), wait=False)

    def broadcast(self, message):
        self.send_message(message, "FF", wait=False)
