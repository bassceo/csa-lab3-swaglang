import sys
from translator.Translator import SwagLangTranslator
from processor.ControlUnit import ControlUnit
from processor.InputDevice import InputDevice
from processor.OutputDevice import OutputDevice
from processor.DataPath import Datapath
from processor.Clock import Clock
from processor.Decoder import OPCODES

def read_code_from_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code

def run_pipeline(file_path, input_str=' '):
    code = read_code_from_file(file_path)
    
    translator = SwagLangTranslator()
    translated = translator.translate_code(code)
    
    input_data = {
        0: list(input_str + chr(0))
    }
    
    input_device = InputDevice(input_data)
    output_device = OutputDevice()
    
    clock = Clock()
    datapath = Datapath(input_device, output_device)
    control_unit = ControlUnit(datapath)
    
    instructions = []
    for i in range(len(translated) // 51):
        instr = translated[i*51:(i+1)*51]
        instructions.append(instr)
        for j in OPCODES:
            if OPCODES[j] == instr[:5]:
                print(j)
    
    control_unit.run(clock, instructions)
    
    output = {}
    for port, data in output_device.buffer.items():
        output[port] = ''.join(data)
    
    return output

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the file path as an argument.")
    else:
        file_path = sys.argv[1]
        input_str = sys.argv[2] if len(sys.argv) > 2 else ' '
        output = run_pipeline(file_path, input_str)
        
        print("\nВывод программы:")
        for port, data in output.items():
            print(f"Порт {port}: {data}")
