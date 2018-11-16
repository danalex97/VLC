class Message():
    def __init__(self, message):
        self.message = message

    @property
    def is_send_stat(self):
        return "s[T,D" in self.message

    @property
    def is_ack_stat(self):
        return "s[R,A" in self.message

    @property
    def is_send(self):
        return "m[D]" == self.message

    @property
    def seq(self):
        return int(self.message.split(',')[4])

    def __repr__(self):
        return self.message

    def __str__(self):
        return self.__repr__()
