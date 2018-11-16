import sys
import time

import serial


class Device:
    def __init__(self, logging=False):
        self.logging=logging
        self.s = serial.Serial('COM5', 115200, timeout=1)
        time.sleep(2)
        self.configure()

    def log(self, message):
        if self.logging:
            print(message)

    def write(self, command):
        self.log("Write: '%s'" % command)
        self.s.write(str.encode(command + "\n"))
        time.sleep(0.1)
        self.listen()

    def send(self, message, receiver):
        payload = "m[%s\0,%s]" % (message, receiver)
        self.log("Sending: '%s'" % payload)
        self.s.write(str.encode(payload + "\n"))

    def listen(self):
        message=""
        while True:
            try:
                byte = self.s.read(1)
                byte = byte.decode('UTF-8')

                if byte == '\n':
                    self.log("Received: " + message)
                    return message
                else:
                    message = message + byte
            except serial.SerialException:
                continue  # on timeout try to read again
            except KeyboardInterrupt:
                sys.exit()  # on ctrl-c terminate program

    def configure(self):
        # self.write("a[CD]")
        self.write("a[CD]")
        self.write("c[1,0,5]")  # set number of retransmissions to 5
        self.write("c[0,1,30]")  # set FEC threshold to 30 (apply FEC to packets with payload >= 30)
