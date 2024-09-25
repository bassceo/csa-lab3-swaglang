import re


class SwagLangTranslator:
    OPCODES = {
        "load": "00001",
        "load_from": "00010",
        "store": "00011",
        "add": "00100",
        "sub": "00101",
        "cmp": "00110",
        "jmp": "00111",
        "je": "01000",
        "jn": "01001",
        "input": "01010",
        "output": "01011",
        "inputchar": "01100",
        "outputchar": "01101",
        "stop": "01110",
        "store_to": "01111",
        "mod": "11111",
    }

    REGISTERS = {"R1": "000000001", "R2": "000000010", "R3": "000000011"}

    def __init__(self):
        self.data_section = {}
        self.marks = {}
        self.current_address = 0
        pass

    def parse_syntax(self, code):
        def parse_block(block):
            commands = []
            while block:
                block = block.lstrip()
                if not block:
                    break

                # Проверка на метку (блок)
                match = re.match(r"^(\w+)\s*:\s*{", block)
                if match:
                    label = match.group(1)
                    block = block[match.end() :]
                    nested_block_content, block = extract_nested_block(block)
                    nested_commands = parse_block(nested_block_content)
                    commands.append({label: nested_commands})
                    continue

                match = re.match(r"^(\w+)\s*\[([^\]]*?)\]\s*;", block)
                if match:
                    cmd_name = match.group(1)
                    args = match.group(2)
                    args_list = [arg.strip() for arg in args.split(",")]

                    if (
                        cmd_name == "load"
                        and len(args_list) > 1
                        and args_list[1].startswith("(")
                        and args_list[1].endswith(")")
                    ):
                        args_list[1] = args_list[1][1:-1].strip()
                        cmd_name = "load_from"

                    if (
                        cmd_name == "store"
                        and len(args_list) > 1
                        and args_list[1].startswith("(")
                        and args_list[1].endswith(")")
                    ):
                        args_list[1] = args_list[1][1:-1].strip()
                        cmd_name = "store_to"

                    commands.append({cmd_name: args_list})
                    block = block[match.end() :]
                    continue

                match = re.match(r'^(\w+)\s*:\s*"(.*?)"\s*;', block)
                if match:
                    key = match.group(1)
                    value = match.group(2)
                    commands.append({key: value})
                    block = block[match.end() :]
                    continue

                match = re.match(r"^(\w+)\s*:\s*(.*?);", block)
                if match:
                    key = match.group(1)
                    value = match.group(2).strip()
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    else:
                        try:
                            value = int(value)
                        except ValueError:
                            pass
                    commands.append({key: value})
                    block = block[match.end() :]
                    continue

                # Проверка на 'stop;'
                match = re.match(r"^(stop)\s*;", block)
                if match:
                    commands.append({"stop": None})
                    block = block[match.end() :]
                    continue

                break

            for cmd in commands:
                for key, args in cmd.items():
                    if isinstance(args, list):
                        for i in range(len(args)):
                            arg = args[i]
                            if isinstance(arg, str) and arg.isdigit():
                                args[i] = int(arg)
                    else:
                        pass
            return commands

        def extract_nested_block(code):
            balance = 1
            i = 0
            while balance > 0 and i < len(code):
                if code[i] == "{":
                    balance += 1
                elif code[i] == "}":
                    balance -= 1
                i += 1
            if balance != 0:
                raise ValueError("Несбалансированные фигурные скобки в блоке")
            nested_block_content = code[: i - 1]
            remaining_code = code[i:]
            return nested_block_content, remaining_code

        def parse_blocks(code):
            code = code.strip()
            blocks = {}
            while code:
                code = code.lstrip()
                if not code:
                    break

                match = re.match(r"^(\w+)\s*:\s*{", code)
                if match:
                    label = match.group(1)
                    code = code[match.end() :]
                    nested_block_content, code = extract_nested_block(code)
                    # Парсим содержимое блока
                    parsed_commands = parse_block(nested_block_content)
                    blocks[label] = parsed_commands
                    continue
                break

            return blocks

        return parse_blocks(code)

    def translate_command(self, command):
        op = list(command.keys())[0]
        args = command[op]

        if op == "stop":
            return self.OPCODES[op].zfill(5) + ("0" * 23 * 2)

        binary = self.OPCODES[op].zfill(5)

        if op in ["jmp", "je", "jn"]:
            addr = args[0]
            addr_bin = f"{int(self.marks[addr]):023b}"
            return binary + ("0" * 23) + addr_bin

        reg = args[0]
        if reg not in self.REGISTERS:
            raise ValueError(f"Unknown register: {reg}")

        reg_bin = self.REGISTERS[reg].zfill(23)

        if len(args) == 2:
            val = args[1]

            if val in self.REGISTERS:
                val_bin = self.REGISTERS[val].zfill(23)
                return binary + reg_bin + val_bin

            if isinstance(val,int):
                val_bin = self.format_immediate(val, 23)
                return binary + reg_bin + val_bin

            if val in self.data_section:
                val_bin = self.format_immediate(self.data_section[val], 23)
                return binary + reg_bin + val_bin
            raise ValueError(f"Unknown value: {type(val)}")
        return binary + reg_bin + ("0" * 23)

    def format_immediate(self, value, bits):
        return format(int(value), f"0{bits}b")

    def parse_data(self):
        binary = ""
        data = self.code_tree["data"]
        for x in data:
            self.data_section[list(x.keys())[0]] = self.current_address
            if isinstance(x[list(x.keys())[0]],int):
                binary += (
                    self.translate_command({"load": ["R1", int(x[list(x.keys())[0]])]})
                    + "\n"
                    + self.translate_command({"store": ["R1", self.current_address]})
                    + "\n"
                )
            else:
                string_value = x[list(x.keys())[0]] + chr(0)
                for char in string_value:
                    char_code = ord(char)
                    self.data_section[f"{x}_{char}"] = self.current_address
                    binary += (
                        self.translate_command({"load": ["R1", char_code]})
                        + "\n"
                        + self.translate_command(
                            {"store": ["R1", self.current_address]}
                        )
                        + "\n"
                    )
                    self.current_address += 1
            self.current_address += 1
        return binary

    def set_marks(self, tree):
        for node in tree:
            if list(node.keys())[0] in self.OPCODES:
                self.counter += 1
            else:
                self.marks[list(node.keys())[0]] = self.counter
                self.set_marks(tree=node[list(node.keys())[0]])

    def parse_run(self, run):
        binary = ""
        for node in run:
            if list(node.keys())[0] in self.OPCODES:
                binary += self.translate_command(node) + "\n"
            else:
                binary += self.parse_run(run=node[list(node.keys())[0]])
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
        parsed_data = self.parse_data()
        self.counter = len(parsed_data.replace("\n", "")) // 51
        self.set_marks(self.code_tree["run"])
        parsed_run = self.parse_run(self.code_tree["run"])
        return (parsed_data + parsed_run).replace("\n", "")
