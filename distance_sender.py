import sys
import time
import random
import string

from device import Device

class Sender():
    def __init__(self, device, other, length=1):
        # init
        self.device = device
        self.other = other
        self.length = length

    def send_payload(self):
        message = ''.join(random.choice(string.digits)
            for x in range(self.length))
        self.device.send_message(message, self.other)

def check_messages(messages, sender):
    start_time = time.time()
    get_time = lambda: time.time() - start_time

    sender.send_payload()
    for message in messages:
        if message.is_send:
            sender.send_payload()
        elif message.is_send_stat:
            print("Sent: {} {}".format(message.seq, get_time()))
        elif message.is_ack_stat:
            print("Ack: {} {}".format(message.seq, get_time()))

def main():
    device = sys.argv[1]
    me     = sys.argv[2]
    other  = sys.argv[3]

    d = Device(device, me)
    d.set_retransmissions(0)
    d.set_FEC(30)

    d.listen(handler=check_messages, sender=Sender(d, other))

if __name__ == "__main__":
    main()
