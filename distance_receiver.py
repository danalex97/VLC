import sys
from device import Device

def check_messages(messages):
    for message in messages:
        print(message)

if __name__ == "__main__":
    device = sys.argv[1]
    me     = sys.argv[2]
    other  = sys.argv[3]

    d = Device(device, me)
    d.set_retransmissions(0)
    d.set_FEC(1)

    d.listen(handler=check_messages)
