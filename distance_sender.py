import sys
import time
import random
import string

from device import Device
from stats import Stats

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

def check_messages(messages, sender, stats):
    start_time = time.time()
    get_time = lambda: time.time() - start_time

    sender.send_payload()
    for message in messages:
        if message.is_send:
            sender.send_payload()
        elif message.is_send_stat or message.is_ack_stat:
            seq  = message.seq
            t    = get_time()
            if message.is_send_stat:
                print("Snd: {} {}".format(seq, t))
                stats.register_send(seq, t)
            else:
                print("Ack: {} {}".format(seq, t))
                stats.register_ack(seq, t)

def main():
    device = sys.argv[1]
    me     = sys.argv[2]
    other  = sys.argv[3]

    d = Device(device, me)
    d.set_retransmissions(0)
    d.set_FEC(30)

    stats = Stats()

    d.listen(handler=check_messages, sender=Sender(d, other), stats=stats)
    print(stats.delays)

if __name__ == "__main__":
    main()
