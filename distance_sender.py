import sys
import time
import random
import string

from device import Device
from stats import Stats

class Sender():
    def __init__(self, device, other, length):
        # init
        self.device = device
        self.other = other
        self.length = length

    def send_payload(self):
        message = ''.join(random.choice(string.digits)
            for x in range(self.length))
        self.device.send_message(message, self.other)

def check_messages(messages, sender, stats, limit=100):
    ctr = 0

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
                if seq not in stats.sent_t:
                    ctr += 1
                    if ctr == limit + 1:
                        break

                print("Snd: {} {}".format(seq, t))
                stats.register_send(seq, t)
            else:
                print("Ack: {} {}".format(seq, t))
                stats.register_ack(seq, t)

def main():
    device = sys.argv[1]
    me     = sys.argv[2]
    other  = sys.argv[3]

    packet_size     = 10
    retransmissions = 0
    fec_threshold   = 30

    d = Device(device, me)
    d.set_retransmissions(retransmissions)
    d.set_FEC(fec_threshold)

    # d.set_DIFS(0)
    # d.set_cw(mn=1, mx=16)

    stats  = Stats(packet_size = packet_size)
    sender = Sender(d, other, length = packet_size)

    d.listen(handler=check_messages, sender=sender, stats=stats)
    print("{} {} {} {}".format(
        stats.avg_delay,
        stats.std_delay,
        stats.avg_throughput,
        stats.std_throughput))

if __name__ == "__main__":
    main()
