import sys
import time
from device import Device

class Sender():
    def __init__(self, device, other, interval=5):
        # init structs
        self.payload = 0
        self.device = device
        self.other = other

        self.send_times = {}
        self.recv_times = {}
        self.step = 0
        self.interval = interval

        # setup loop
        self.device.check_loop(self.send_next)
        # self.device.check_loop(self.process_stats)

        # send initial messages
        self.start()

    def send_payload(self):
        to_send = str(self.payload)
        self.device.send_message(to_send, self.other)
        self.payload += 1
        if self.payload > 255:
            self.payload = 0

    def start(self):
        self.send_payload()
        self.last = 0

    def send_next(self, message):
        if "m[D]" in message:
            self.send_payload()
            t = time.time()
            print(t - self.last)
            self.last = t

    def process_stats(self, message):
        def get_seq(message):
            return message.split(',')[4]

        if "s[T,D" in message:
            seq = get_seq(message)
            self.send_times[seq] = time.time()
            self.step += 1

            if self.step % self.interval == 0:
                avg_time = 0
                cnt = 0
                for seq in self.send_times.keys():
                    if seq not in self.recv_times:
                        continue
                    cur_time = self.recv_times[seq] - self.send_times[seq]
                    avg_time += cur_time
                    cnt += 1

                avg_time /= cnt
                print(avg_time)

                self.send_times = {}
                self.recv_times = {}

        if "s[R,A" in message:
            seq = get_seq(message)
            self.recv_times[seq] = time.time()

def main():
    device = sys.argv[1]
    me     = sys.argv[2]
    other  = sys.argv[3]

    d = Device(device, me)

    d.set_retransmissions(5)
    d.set_FEC(30)

    sender = Sender(d, other)
    d.listen()

if __name__ == "__main__":
    main()
