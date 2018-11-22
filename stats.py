from math import sqrt

def get_std(avg, lst):
    variance = sum((x - avg) ** 2 for x in lst)
    return sqrt(variance)

class Stats():
    def __init__(self, packet_size = 1):
        self.packet_size = packet_size
        self.first_timestamp = 0

        self.sent_t = {}
        self.recv = set()

        self.delays = []

    def register_send(self, seq, t):
        if len(self.sent_t) == 0:
            self.first_timestamp = t
        if seq not in self.sent_t:
            self.sent_t[seq] = t

    def register_ack(self, seq, t):
        if seq not in self.sent_t:
            # stuff remined from last session...
            return
        if seq not in self.recv:
            self.recv.add(seq)
            self.delays.append((t, t - self.sent_t[seq]))

    @property
    def avg_delay(self):
        return sum(d for t, d in self.delays) / len(self.delays)

    @property
    def std_delay(self):
        return get_std(self.avg_delay, (d for _, d in self.delays))

    @property
    def avg_throughput(self):
        time = self.delays[-1][0] - self.first_timestamp
        data = self.packet_size * len(self.delays)
        return data / time

    @property
    def std_throughput(self, packets=5):
        avg = self.avg_throughput

        throuhputs = []
        times = sorted(self.sent_t.values())
        i_start = 0
        i_end   = packets
        while i_end < len(times):
            times_start = times[i_start]
            times_end = times[i_end]

            acked_packets = 0
            for seq, t in self.sent_t.items():
                if times_start <= t and t < times_end:
                    if seq in self.recv:
                        acked_packets += 1

            i_start += packets
            i_end += packets

            throuhputs.append(
                acked_packets * self.packet_size / (times_end - times_start))
        return get_std(avg, throuhputs)
