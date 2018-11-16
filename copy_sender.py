import random
import string
import time

from VLC.copy_device import Device

if __name__ == "__main__":
    d = Device("COM3", "AB")
    payloadLength = 1

    message = ""
    while True:  # while not terminated
        message = ''.join(random.choice(string.digits) for x in range(payloadLength))
        d.send(message, "AB")
        send_time = time.time()
        while True:
            received = d.listen()
            if "m[T]" in received:
                pass
            if "m[D]" in received:
                print_time = time.time() - send_time
                print("Test: %s" % str(print_time))

                break
