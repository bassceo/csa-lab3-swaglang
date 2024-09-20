class InputDevice:
    """Устройство ввода, предоставляющее данные процессору."""
    def __init__(self, data):
        self.buffer = data  # Словарь списков символов для ввода по портам

    def read(self, port):
        if port in self.buffer and self.buffer[port]:
            data = self.buffer[port].pop(0)
            print(f"[InputDevice] Чтение данных с порта {port}: '{data}'")
            return data
        else:
            print(f"[InputDevice] Буфер ввода порта {port} пуст.")
            return None  # Нет больше данных