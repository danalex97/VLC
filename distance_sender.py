import random
import string

from VLC.device import Device

if __name__ == "__main__":
    d = Device()
    payloadLength = 1

    message = ""
    while True:  # while not terminated
        message = ''.join(random.choice(string.digits) for x in range(payloadLength))
        d.send(message, "AB")
        d.listen()
