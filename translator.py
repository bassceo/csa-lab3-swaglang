import re

class SwagLangTranslator:
    OPCODES = {
        'load': '00001',
        'store': '00010',
        'add': '00011',
        'sub': '00100',
        'cmp': '00101',
        'jmp': '00110',
        'je': '00111',
        'jne': '01000',
        'input': '01001',
        'output': '01010',
        'inputchar': '01011',
        'outputchar': '01100',
        'stop': '10000'
    }

    REGISTERS = {
        'R1': '000000001',
        'R2': '000000010',
        'R3': '000000011'
    }
    
    def __init__(self):
        self.data_section = {}
        self.marks = {}
        self.current_address = 0
        pass
    
    def parse_syntax(self, code):
        def parse_block(block: str):
            result = {}
            while block:
                match = re.match(r'(\w+):{', block)
                if match:
                    key = match.group(1)
                    block = block[len(key)+2:]
                    nested_block, block = extract_nested_block(block)
                    result[key] = parse_block(nested_block)
                else:
                    match = re.match(r'(\w+)\[([^\]]+)\];', block)
                    if match:
                        key = match.group(1)
                        value = match.group(2)
                        
                        result[key] = value.split(',')
                        for i in range(len(result[key])):
                            if result[key][i].isdigit():
                                result[key][i] = int(result[key][i])
                        block = block[len(match.group(0)):]
                    else:
                        match = re.match(r'(\w+):"(.*?)";', block)
                        if match:
                            key = match.group(1)
                            value = '"' + match.group(2) + chr(0) + '"'
                            result[key] = value
                            block = block[len(match.group(0)):]
                        else:
                            match = re.match('stop;', block)
                            if match:
                                
                                result[match.group(0)[:-1]] = ''
                                block = block[len(match.group(0)):]
                            else:
                                break
            return result

        def extract_nested_block(block: str):
            balance = 1
            i = 0
            while balance > 0 and i < len(block):
                if block[i] == '{':
                    balance += 1
                elif block[i] == '}':
                    balance -= 1
                i += 1
            return block[:i-1], block[i:]

        return parse_block(code)
    
    def translate_command(self, command):
        op = list(command.keys())[0]
        args = command[op]
        
        if op=='stop':
            return self.OPCODES[op].zfill(5) + ("0"*9*3)

        binary = self.OPCODES[op].zfill(5)

        if op in ['jmp', 'je', 'jne']:
            addr = args[0]
            addr_bin = f"{int(self.marks[addr]):09b}" 
            return binary + '000000000000000000' + addr_bin 

        reg = args[0]
        if reg not in self.REGISTERS:
            raise ValueError(f"Unknown register: {reg}")

        reg_bin = self.REGISTERS[reg].zfill(9)

        if len(args) == 2:
            val = args[1]

            if val in self.REGISTERS:
                val_bin = self.REGISTERS[val].zfill(9) 
                return binary + reg_bin + val_bin + '000000000'
            
            elif type(val)==int:
                val_bin = self.format_immediate(val, 9)
                return binary + reg_bin + '000000000' + val_bin
            
            elif val in self.data_section:
                val_bin = self.format_immediate(self.data_section[val], 9)
                return binary + reg_bin + '000000000' + val_bin 
            else:
                raise ValueError(f"Unknown value: {type(val)}")
        else:
            return binary + reg_bin + '0000000000000000'

    def format_immediate(self, value, bits):
        return format(int(value), f'0{bits}b')

    
    def parse_data(self):
        binary = ""
        data = self.code_tree['data']
        for x in data:
            self.data_section[x] = self.current_address
            if data[x].isdigit():
                binary += self.translate_command({"load":['R1', int(data[x])]})+"\n"+self.translate_command({"store": ['R1', self.current_address]})+"\n"
            else:
                string_value = data[x][1:-1]
                for char in string_value:
                    char_code = ord(char)
                    self.data_section[f"{x}_{char}"] = self.current_address
                    binary += self.translate_command({"load":['R1', char_code]})+"\n"+self.translate_command({"store": ['R1', self.current_address]})+"\n"
                    self.current_address += 1
            self.current_address += 1
        return binary
    
    def set_marks(self, tree):
        for node in tree:
            if node in self.OPCODES:
                self.counter+=1
            else:
                self.marks[node] = self.counter+1
                self.set_marks(tree=tree[node])
        
    
    def parse_run(self,run):
        binary = ""
        for node in run:
            if node in self.OPCODES:
                binary+=self.translate_command({node: run[node]})+"\n"
            else:
                binary+=self.parse_run(run=run[node])
        return binary
    
    def translate_code(self, code):
        code_parts = code.split('"')
        clean_code = ""
        
        for i, part in enumerate(code_parts):
            if i % 2 == 0:
                part = part.replace(" ", "").replace("\n", "")
            else:
                clean_code += '"'
            clean_code += part
            if i % 2 == 1:
                clean_code += '"'
        
        self.code_tree = self.parse_syntax(clean_code)
        print(self.code_tree)
        parsed_data = self.parse_data()
        self.counter = len(parsed_data.replace("\n", ""))//32
        
        self.set_marks(self.code_tree['run'])
        parsed_run = self.parse_run(self.code_tree['run'])
        return (parsed_data+parsed_run).replace("\n", "")


translator = SwagLangTranslator()

code = """
data: {
    str: "Hello world!";           
}
run: {
    load[R1, str];          

    read_loop: {
        cmp[R1, 0];          
        je[write_loop];         
        
        add[R1, 1];     
        jmp[read_loop]; 
    }

    write_loop: {
        load[R1, 0];         
    }

    output_loop: {
        load[R2, R1];   
        cmp[R2, 0];            
        je[end];  

        add[R1, 1];             
        jmp[output_loop];      
    }
    end: {
        stop;
    }
}
"""
translated = translator.translate_code(code)

buffer = ""
command = 1
for i in translated:
    if len(buffer) == 32:
        op = ""
        for j in translator.OPCODES:
            if translator.OPCODES[j]==buffer[:5]:
                op=j
        
        print(command, " ",op, " ", int(buffer[5:14],2)," ", int(buffer[14:23],2) ," ", int(buffer[23:32],2))
        buffer = ""
        command+=1
    buffer += i
if len(buffer) == 32:
        op = ""
        for j in translator.OPCODES:
            if translator.OPCODES[j]==buffer[:5]:
                op=j
        
        print(command, " ",op, " ", int(buffer[5:14],2)," ", int(buffer[14:23],2) ," ", int(buffer[23:32],2))
        buffer = ""
        command+=1