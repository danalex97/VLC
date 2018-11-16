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
        self.listener = None

        # initialize
        self._send("a[{}]".format(address), wait=True)

        # set signal handler for stopping the program
        def signal_handler(sig, frame):
            self.stopped = True
            if self.listener:
                self.listener.join()
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)

    def stop(self):
        self.stopped = True

    def check_loop(self, func):
        self.funcs.append(func)

    def _listen(self):
        message=""
        while not self.stopped:
            try:
                byte = self.serial.read(1)
                byte = byte.decode('UTF-8')

                if byte == '\n':
                    yield message
                    message=""
                else:
                    message = message + byte
            except serial.SerialException:
                print("Serial exception!")
                continue
        yield None

    def listen(self, thread=False):
        if thread:
            self.listener = threading.Thread(target=self.listen)
            self.listener.start()
        else:
            for message in self._listen():
                if self.stopped:
                    break
                for f in self.funcs:
                    f(message)

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
