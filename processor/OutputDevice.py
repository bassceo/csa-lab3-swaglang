class OutputDevice:
    def __init__(self):
        self.buffer = {}

    def write(self, data, port):
        if port not in self.buffer:
            self.buffer[port] = []
        self.buffer[port].append(data)
