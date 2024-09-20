class OutputDevice:
    def __init__(self):
        self.buffer = {}  

    def write(self, data, port):
        if port not in self.buffer:
            self.buffer[port] = []
        print(f"[OutputDevice] Запись данных на порт {port}: '{data}'")
        self.buffer[port].append(data)