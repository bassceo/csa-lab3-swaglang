
REGISTERS = {
    'R1': '00000000000000000000001',
    'R2': '00000000000000000000010',
    'R3': '00000000000000000000011'
}

OPCODES = {
    'load': '00001',
    'load_from': '00010',
    'store': '00011',
    'add': '00100',
    'sub': '00101',
    'cmp': '00110',
    'jmp': '00111',
    'je': '01000',
    'isneg': '01001',
    'input': '01010',
    'output': '01011',
    'inputchar': '01100',
    'outputchar': '01101',
    'stop': '01110',
    'store_to': '01111',
    'mod': '11111',
}

class Decoder:
    def __init__(self):
        pass

    def decode(self, instruction_str):
        instruction = instruction_str 
        opcode_bin = instruction[:5]
        operand1_bin = instruction[5:28]
        operand2_bin = instruction[28:51]
        opcode_str = None
        for key, value in OPCODES.items():
            if value == opcode_bin:
                opcode_str = key
                break

        if opcode_str is None:
            raise Exception(f"[Error] Неизвестный опкод: {opcode_bin}")

        control_signals = {
            'load_enable': False,
            'load_from_enable': False,
            'store_enable': False,
            'alu_enable': False,
            'alu_op': None,
            'read_enable': False,
            'write_enable': False,
            'jump': False,
            'branch': False,
            'halt': False,
            'reg_src': '',
            'reg_dest': '',
            'immediate': None,
            'address': None,
            'port': None,
            'input_type': None,
            'output_type': None
        }

        reg_bin_to_name = {v: k for k, v in REGISTERS.items()}

        if opcode_str == 'load':
            reg_dest = reg_bin_to_name.get(operand1_bin)
            immediate = int(operand2_bin, 2)
            control_signals['load_enable'] = True
            control_signals['reg_dest'] = reg_dest
            control_signals['immediate'] = immediate
            print(f"[Decoder] Команда {opcode_str}, {reg_dest}, число {immediate}")
        elif opcode_str == 'load_from':
            reg_dest = reg_bin_to_name.get(operand1_bin)
            reg_src = reg_bin_to_name.get(operand2_bin)
            control_signals['load_from_enable'] = True
            control_signals['reg_dest'] = reg_dest
            control_signals['reg_src'] = reg_src
            print(f"[Decoder] Команда {opcode_str}, {reg_dest}, адрес {reg_src}")
        elif opcode_str == 'store':
            reg_src = reg_bin_to_name.get(operand1_bin)
            address = int(operand2_bin, 2)
            control_signals['store_enable'] = True
            control_signals['reg_src'] = reg_src
            control_signals['address'] = address
            print(f"[Decoder] Команда {opcode_str}, {reg_src}, адрес {address}")
        elif opcode_str == 'store_to':
            reg_src = reg_bin_to_name.get(operand1_bin)
            reg_dest =  reg_bin_to_name.get(operand2_bin)
            control_signals['store_enable'] = True
            control_signals['reg_src'] = reg_src
            control_signals['reg_dest'] = reg_dest
            print(f"[Decoder] Команда {opcode_str}, {reg_src},  {reg_dest}")
        elif opcode_str in ['add', 'sub', 'mod']:
            reg_dest = reg_bin_to_name.get(operand1_bin)
            reg_src = reg_bin_to_name.get(operand2_bin)
            control_signals['alu_enable'] = True
            control_signals['alu_op'] = opcode_str
            control_signals['reg_dest'] = reg_dest
            control_signals['reg_src'] = reg_src
            print(f"[Decoder] Команда {opcode_str}, {reg_dest}, {reg_src}")
        elif opcode_str in ['cmp','isneg']:
            reg_src1 = reg_bin_to_name.get(operand1_bin)
            reg_src2 = reg_bin_to_name.get(operand2_bin)
            control_signals['alu_enable'] = True
            control_signals['alu_op'] = opcode_str
            control_signals['reg_src1'] = reg_src1
            control_signals['reg_src2'] = reg_src2
            print(f"[Decoder] Команда {opcode_str}, {reg_src1}, {reg_src2}")
        elif opcode_str in ['jmp', 'je', 'jne']:
            address = int(operand2_bin, 2)
            control_signals['jump'] = True
            control_signals['branch'] = opcode_str
            control_signals['address'] = address
            print(f"[Decoder] Команда {opcode_str}, адрес {address}")
        elif opcode_str in ['input', 'inputchar']:
            reg_dest = reg_bin_to_name.get(operand1_bin)
            port = int(operand2_bin, 2)
            control_signals['read_enable'] = True
            control_signals['reg_dest'] = reg_dest
            control_signals['port'] = port
            control_signals['input_type'] = 'char' if opcode_str == 'inputchar' else 'number'
            print(f"[Decoder] Команда {opcode_str}, {reg_dest}, порт {port}")
        elif opcode_str in ['output', 'outputchar']:
            reg_src = reg_bin_to_name.get(operand1_bin)
            port = int(operand2_bin, 2)
            control_signals['write_enable'] = True
            control_signals['reg_src'] = reg_src
            control_signals['port'] = port
            control_signals['output_type'] = 'char' if opcode_str == 'outputchar' else 'number'
            print(f"[Decoder] Команда {opcode_str}, {reg_src}, порт {port}")
        elif opcode_str == 'stop':
            control_signals['halt'] = True
            print("[Decoder] Команда stop")
        else:
            raise Exception(f"[Error] Неизвестный опкод: {opcode_str}")

        return control_signals