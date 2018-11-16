import signal
import serial
import time
import sys

import threading
import traceback
from message import Message

class Device():
    _LISTEN_SIG = "_listen"
    _SERIAL_SIG = "_serial"

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

    def _listen(self):
        message=""
        while not self.stopped:
            try:
                byte = self.serial.read(1)
                byte = byte.decode('UTF-8')

                if byte == '\n':
                    yield Message(message)
                    message=""
                else:
                    message = message + byte
            except serial.SerialException:
                raise RuntimeError(Device._SERIAL_SIG)
        raise RuntimeError(Device._LISTEN_SIG)

    def listen(self, handler, thread=False, *args, **kwargs):
        if thread:
            self.listener = threading.Thread(target=self.listen, args=(handler, *args), kwargs=kwargs)
            self.listener.start()
        else:
            try:
                handler(self._listen(), *args, **kwargs)
            except RuntimeError as e:
                if str(e) == Device._LISTEN_SIG:
                    print("App stopped.")
                elif str(e) == Device._SERIAL_SIG:
                    print("Serial device stopped.")
                else:
                    raise e

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
