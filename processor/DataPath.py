from processor.ALU import ALU

class Datapath:
    def __init__(self, input_device, output_device):
        self.registers = {
            'R1': 0,
            'R2': 0,
            'R3': 0
        }
        self.memory = {}  # Память для инструкций load_from и store
        self.alu = ALU()
        self.input_device = input_device  # Устройство ввода
        self.output_device = output_device  # Устройство вывода
        self.memory_buffer = None  # Буфер для операций load_from

    def perform_alu_operation(self, control_signals):
        alu_op = control_signals.get('alu_op', None)
        reg_src = control_signals.get('reg_src', '')
        reg_dest = control_signals.get('reg_dest', '')
        if alu_op == 'cmp' or alu_op == 'isneg':
            reg_src1 = control_signals.get('reg_src1', '')
            reg_src2 = control_signals.get('reg_src2', '')
            src_val1 = self.registers[reg_src1]
            if alu_op=='cmp':
                src_val2 = self.registers[reg_src2]
            else:
                src_val2 = self.registers['R2']
            self.alu.compute(alu_op, src_val2, src_val1)
        else:
            src_val = self.registers[reg_src]
            dest_val = self.registers[reg_dest]
            self.alu.compute(alu_op, src_val, dest_val)

    def perform_memory_operation(self, control_signals):
        load_from_enable = control_signals.get('load_from_enable', False)
        store_enable = control_signals.get('store_enable', False)
        reg_src = control_signals.get('reg_src', '')
        reg_dest = control_signals.get('reg_dest', '')
        address = control_signals.get('address', None)

        if load_from_enable:
            print(f"[Datapath] Загрузка из памяти[{self.registers[reg_src]}] в буфер")
            self.memory_buffer = self.memory.get(self.registers[reg_src], 0)
        if store_enable:
            if address is not None:
                print(f"[Datapath] Сохранение из {reg_src} в память[{address}]")
                value = self.registers[reg_src]
                self.memory[address] = value
            else:
                print(f"[Datapath] Сохранение из {reg_src} в память[{self.registers[reg_dest]}]")
                value = self.registers[reg_src]
                self.memory[self.registers[reg_dest]] = value

    def perform_register_write(self, control_signals):
        load_enable = control_signals.get('load_enable', False)
        alu_enable = control_signals.get('alu_enable', False)
        reg_dest = control_signals.get('reg_dest', '')
        immediate = control_signals.get('immediate', None)

        if load_enable:
            print(f"[Datapath] Загрузка числа {immediate} в {reg_dest}")
            self.registers[reg_dest] = immediate
        elif alu_enable:
            alu_op = control_signals.get('alu_op', None)
            if alu_op != 'cmp':
                self.registers[reg_dest] = self.alu.get_result()
                print(f"[Datapath] Результат АЛУ записан в {reg_dest}: {self.registers[reg_dest]}")
        elif self.memory_buffer is not None:
            print(f"[Datapath] Запись из буфера памяти в {reg_dest}")
            self.registers[reg_dest] = self.memory_buffer
            self.memory_buffer = None

    def perform_io_operation(self, control_signals):
        read_enable = control_signals.get('read_enable', False)
        write_enable = control_signals.get('write_enable', False)
        reg_src = control_signals.get('reg_src', '')
        reg_dest = control_signals.get('reg_dest', '')
        port = control_signals.get('port', None)
        input_type = control_signals.get('input_type', None)
        output_type = control_signals.get('output_type', None)
        if read_enable:
            print(f"[Datapath] Чтение в {reg_dest} с порта {port}")
            self.read_from_port(reg_dest, port, input_type)
        if write_enable:
            print(f"[Datapath] Запись из {reg_src} на порт {port}")
            self.write_to_port(reg_src, port, output_type)

    def get_zero_flag(self):
        return self.alu.get_zero_flag()

    def read_from_port(self, reg_dest, port, input_type):
        data = self.input_device.read(port)
        if data is not None:
            if input_type == 'char':
                self.registers[reg_dest] = ord(data)
                print(f"[Datapath] {reg_dest} <- '{data}' (код {self.registers[reg_dest]})")
            elif input_type == 'number':
                self.registers[reg_dest] = int(data)
                print(f"[Datapath] {reg_dest} <- {self.registers[reg_dest]}")
            else:
                raise Exception(f"[Error] Неизвестный тип ввода: {input_type}")
        else:
            raise Exception(f"[Error] Буфер ввода порта {port} пуст. Остановка выполнения.")

    def write_to_port(self, reg_src, port, output_type):
        value = self.registers[reg_src]
        if output_type == 'char':
            data = chr(value & 0xFF)
            self.output_device.write(data, port)
            print(f"[Datapath] Вывод символа на порт {port}: '{data}'")
        elif output_type == 'number':
            data = str(value)
            self.output_device.write(data, port)
            print(f"[Datapath] Вывод числа на порт {port}: {data}")
        else:
            raise Exception(f"[Error] Неизвестный тип вывода: {output_type}")