class InputDevice:
    def __init__(self, data):
        self.buffer = data

    def read(self, port, type):
        if self.buffer.get(port):
            if type == "number":
                tmp = ""
                word = ""
                while True:
                    tmp = self.buffer[port].pop(0)
                    if tmp == chr(0):
                        break
                    word += tmp
                return int(word)
            return self.buffer[port].pop(0)
        return None
