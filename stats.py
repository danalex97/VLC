class Stats():
    def __init__(self):
        self.sent_t = {}
        self.recv = set()

        self.delays = []

    def register_send(self, seq, t):
        if seq not in self.sent_t:
            self.sent_t[seq] = t

    def register_ack(self, seq, t):
        if seq not in self.recv:
            self.recv.add(seq)
            self.delays.append((t, t - self.sent_t[seq]))
