class InputDevice:
    def __init__(self, data):
        self.buffer = data 

    def read(self, port):
        if port in self.buffer and self.buffer[port]:
            data = self.buffer[port].pop(0)
            print(f"[InputDevice] Чтение данных с порта {port}: '{data}'")
            return data
        else:
            print(f"[InputDevice] Буфер ввода порта {port} пуст.")
            return None 