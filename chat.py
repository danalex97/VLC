import sys
from device import Device

def check_messages(messages):
    for message in messages:
        if "m[R,D" in message:
            message = message.split('[')[1]
            message = message.split(',')[2]
            message = message[:-1]
            print(message)

if __name__ == "__main__":
    device = sys.argv[1]
    me     = sys.argv[2]
    other  = sys.argv[3]

    d = Device(device, me)

    d.set_retransmissions(5)
    d.set_FEC(30)

    d.listen(handler=check_messages, thread=True)
    while True:
        message = input("")
        d.send_message(message, other)

    d.stop()
