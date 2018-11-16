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
        self.lock = Lock()
        self.listener = threading.Thread(target=self.listen)
        self.listener.start()

        # initialize
        self._send("a[{}]".format(address))
        self._read()

        def signal_handler(sig, frame):
            self.stopped = True
            self.listener.join()
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)

    def check_loop(self, func):
        self.funcs.append(func)

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

        while not self.stopped:
            message   = _read()
            processed = False
            for f in self.funcs:
                if f(message):
                    processed = True
            if not processed:
                self.lock.acquire()
                self.buffer.append(message)
                self.lock.release()

    def _send(self, message):
        """ send message to serial port """

        self.serial.write(str.encode(message + "\n"))
        time.sleep(0.2)

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

    def set_FEC(self, size):
        self._send("c[0,1,{}]".format(size))

    def send_message(self, message, dest):
        self._send("m[{}\0,{}]".format(message, dest))

    def broadcast(self, message):
        self.send_message(message, "FF")
