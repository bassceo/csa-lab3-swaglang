class InputDevice:
    def __init__(self, data):
        self.buffer = data 

    def read(self, port, type):
        if port in self.buffer and self.buffer[port]:
            
            if type=='number':
                tmp = ''
                word = ''
                while(True):
                    tmp = self.buffer[port].pop(0)
                    if tmp==chr(0):
                        break
                    word+=tmp
                return int(word)
            data = self.buffer[port].pop(0)
            return data
        else:
            return None 