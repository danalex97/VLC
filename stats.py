class Stats():
    def __init__(self):
        self.sent_t = {}
        self.delays = []

    def register_send(self, seq, t):
        self.sent_t[seq] = t

    def register_ack(self, seq, t):
        self.delays.append((t, t - self.sent_t[seq]))
