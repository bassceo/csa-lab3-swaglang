from processor.Decoder import Decoder, OPCODES
import logging

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
            self.pc = addr
            self.instruction_stage = 'FETCH'
        elif branch == 'je':
            if self.datapath.get_zero_flag():
                self.pc = addr
                self.instruction_stage = 'FETCH'
            else:
                self.pc += 1
        elif branch == 'jn':
            if self.datapath.get_negative_flag():
                self.pc = addr
                self.instruction_stage = 'FETCH'
            else:
                self.pc += 1
    
    def log(self, tick,instruction_memory):
        op = ""
        for i in OPCODES:
            if(OPCODES[i]==instruction_memory[self.pc][:5]):
                op=i
        logging.debug(f" Tick={tick} | STAGE={self.instruction_stage} | OP={op} | PC={self.pc} | R1={self.datapath.registers['R1']} | R2={self.datapath.registers['R2']} | R3={self.datapath.registers['R3']} |  data={self.datapath.memory}")
    
    def run(self, clock, instruction_memory):
        while not self.halted:
            tick = clock.tick()
            self.log(tick,instruction_memory)
            if self.instruction_stage == 'FETCH':
                self.fetch_instruction(instruction_memory)
                self.instruction_stage = 'DECODE'
            elif self.instruction_stage == 'DECODE':
                self.decode_instruction()
                self.instruction_stage = 'EXECUTE'
            elif self.instruction_stage == 'EXECUTE':
                self.execute_instruction()
                if not self.instruction_stage == "FETCH":
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
        logging.getLogger().setLevel(logging.DEBUG)
        pass