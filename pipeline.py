import sys
from translator.Translator import SwagLangTranslator
from processor.ControlUnit import ControlUnit
from processor.InputDevice import InputDevice
from processor.InputDevice import InputDevice
from processor.OutputDevice import OutputDevice
from processor.DataPath import Datapath
from processor.Clock import Clock
from processor.Decoder import OPCODES

def read_code_from_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the file path as an argument.")
    else:
        file_path = sys.argv[1]
        code = read_code_from_file(file_path)
        
        translator = SwagLangTranslator()
        translated = translator.translate_code(code)
        if(len(sys.argv) > 2):
            input_data = {
                0: list(sys.argv[2]+chr(0))
            }
        else:
            input_data = {
                0: list(' '+chr(0))
            }
        input_device = InputDevice(input_data)
        output_device = OutputDevice()

        clock = Clock()
        datapath = Datapath(input_device, output_device)
        control_unit = ControlUnit(datapath)
        
        instructions = []
        for i in range(len(translated)//51):
            instructions.append(translated[i*51:(i+1)*51])
            for j in OPCODES:
                if OPCODES[j]== translated[i*51:(i+1)*51][:5]:
                    print(j)
            

        control_unit.run(clock, instructions)
        
        print("\nВывод программы:")
        for port, data in output_device.buffer.items():
            print(f"Порт {port}: {''.join(data)}")