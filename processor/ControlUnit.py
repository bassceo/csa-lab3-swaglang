from processor.Decoder import Decoder

class ControlUnit:
    def __init__(self, datapath):
        self.pc = 0
        self.datapath = datapath
        self.halted = False
        self.decoder = Decoder()
        self.instruction_stage = 'FETCH'
        self.current_instruction = None
        self.control_signals = None

    def fetch_instruction(self, instruction_memory):
        if self.pc < len(instruction_memory):
            self.current_instruction = instruction_memory[self.pc]
            print(f"[ControlUnit] Fetch: '{self.current_instruction}', PC: {self.pc}")
        else:
            self.halted = True
            self.current_instruction = None

    def decode_instruction(self):
        if self.current_instruction:
            try:
                self.control_signals = self.decoder.decode(self.current_instruction)
            except Exception as e:
                print(str(e))
                self.halted = True
        else:
            self.control_signals = None

    def execute_instruction(self):
        if self.control_signals:
            if self.control_signals['halt']:
                self.halted = True
                return
            if self.control_signals['alu_enable']:
                self.datapath.perform_alu_operation(self.control_signals)
            if self.control_signals['jump']:
                self.handle_branch()
        else:
            pass

    def memory_access(self):
        if self.control_signals:
            if self.control_signals['load_from_enable'] or self.control_signals['store_enable']:
                self.datapath.perform_memory_operation(self.control_signals)
        else:
            pass

    def write_back(self):
        if self.control_signals:
            self.datapath.perform_register_write(self.control_signals)
            self.datapath.perform_io_operation(self.control_signals)
            if not self.control_signals.get('jump', False):
                self.pc += 1
        else:
            pass

    def handle_branch(self):
        branch = self.control_signals['branch']
        addr = self.control_signals['address']
        if branch == 'jmp':
            print(f"[ControlUnit] Безусловный переход на адрес {addr}")
            self.pc = addr
        elif branch == 'je':
            if self.datapath.get_zero_flag():
                print(f"[ControlUnit] Переход при равенстве на адрес {addr}")
                self.pc = addr
            else:
                self.pc += 1
        elif branch == 'jne':
            if not self.datapath.get_zero_flag():
                print(f"[ControlUnit] Переход при неравенстве на адрес {addr}")
                self.pc = addr
            else:
                self.pc += 1

    def run(self, clock, instruction_memory):
        while not self.halted:
            clock.tick()
            if self.instruction_stage == 'FETCH':
                self.fetch_instruction(instruction_memory)
                self.instruction_stage = 'DECODE'
            elif self.instruction_stage == 'DECODE':
                self.decode_instruction()
                self.instruction_stage = 'EXECUTE'
            elif self.instruction_stage == 'EXECUTE':
                self.execute_instruction()
                self.instruction_stage = 'MEMORY'
            elif self.instruction_stage == 'MEMORY':
                self.memory_access()
                self.instruction_stage = 'WRITEBACK'
            elif self.instruction_stage == 'WRITEBACK':
                self.write_back()
                self.instruction_stage = 'FETCH'
                self.print_state()
            else:
                raise Exception(f"[Error] Неизвестный этап инструкции: {self.instruction_stage}")

    def print_state(self):
        print(f"[State] PC: {self.pc}")
        print(f"[State] Регистры: {self.datapath.registers}")
        print(f"[State] Флаг нуля: {self.datapath.get_zero_flag()}")