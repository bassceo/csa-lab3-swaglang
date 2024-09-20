class OutputDevice:
    """Устройство вывода, собирающее данные от процессора."""
    def __init__(self):
        self.buffer = {}  # Словарь для накопления вывода по портам

    def write(self, data, port):
        if port not in self.buffer:
            self.buffer[port] = []
        print(f"[OutputDevice] Запись данных на порт {port}: '{data}'")
        self.buffer[port].append(data)