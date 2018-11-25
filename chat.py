from device import Device

import sys

BLUE = '\033[94m'
END = '\033[0m'

def check_messages(messages):
    for message in messages:
        if message.is_recv_data:
            print("{}{}{}".format(BLUE, message.data, END))

if __name__ == "__main__":
    device = sys.argv[1]
    me     = sys.argv[2]

    d = Device(device, me)

    d.set_retransmissions(5)
    d.set_FEC(30)

    d.listen(handler=check_messages, thread=True)
    while True:
        message = input("")
        d.broadcast(message)
