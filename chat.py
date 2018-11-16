import sys
from device import Device

def check_message(message):
    if "m[R,D" in message:
        message = message.split('[')[1]
        message = message.split(',')[2]
        message = message[:-1]
        print(message)
        return True
    return False

if __name__ == "__main__":
    device = sys.argv[1]
    me     = sys.argv[2]
    other  = sys.argv[3]

    d = Device(device, me)

    d.set_retransmissions(0)
    d.set_FEC(30)

    d.check_loop(check_message)
    while True:
        message = input("")
        d.send_message(message, other)

    d.stop()
