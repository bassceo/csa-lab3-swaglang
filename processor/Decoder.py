from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict

REGISTERS = {
    "R1": "00000000000000000000001",
    "R2": "00000000000000000000010",
    "R3": "00000000000000000000011"
}

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


@dataclass
class ControlSignals:
    load_enable: bool = False
    load_from_enable: bool = False
    store_enable: bool = False
    alu_enable: bool = False
    alu_op: str | None = None
    read_enable: bool = False
    write_enable: bool = False
    jump: bool = False
    branch: str | None = None
    halt: bool = False
    reg_src: str | None = None
    reg_dest: str | None = None
    immediate: int | None = None
    address: int | None = None
    port: int | None = None
    input_type: str | None = None
    output_type: str | None = None

    def reset(self):
        for field_name in self.__dataclass_fields__:
            if field_name == "halt":
                continue
            value = getattr(self, field_name)
            if isinstance(value, bool):
                setattr(self, field_name, False)
            else:
                setattr(self, field_name, None)


MicroInstruction = Callable[["ControlSignals", Dict[str, str]], None]

def micro_load_set_dest(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.reg_dest = operands.get("reg_dest")

def micro_load_set_immediate(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.immediate = int(operands.get("immediate", "0"), 2)

def micro_load_enable(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.load_enable = True

def micro_load_from_set_dest(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.reg_dest = operands.get("reg_dest")

def micro_load_from_set_src(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.reg_src = operands.get("reg_src")

def micro_load_from_enable(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.load_from_enable = True

def micro_store_set_src(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.reg_src = operands.get("reg_src")

def micro_store_set_dest(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.reg_dest = operands.get("reg_src")
    control_signals.reg_src = operands.get("reg_dest")

def micro_store_set_address(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.address = int(operands.get("address"),2)


def micro_store_enable(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.store_enable = True

def micro_add_sub_mod_set_dest(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.reg_dest = operands.get("reg_dest")

def micro_add_sub_mod_set_src(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.reg_src = operands.get("reg_src")

def micro_add_sub_mod_enable(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.alu_enable = True
    control_signals.alu_op = operands.get("alu_op")

def micro_cmp_set_src1(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.reg_src1 = operands.get("reg_src1")

def micro_cmp_set_src2(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.reg_src2 = operands.get("reg_src2")

def micro_cmp_enable(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.alu_enable = True
    control_signals.alu_op = "cmp"

def micro_jmp_set_address(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.address = int(operands.get("address", "0"), 2)

def micro_jmp_set_branch(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.branch = operands.get("branch")

def micro_jmp_enable(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.jump = True

def micro_input_set_dest(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.reg_dest = operands.get("reg_dest")

def micro_input_set_port(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.port = int(operands.get("port", "0"), 2)

def micro_input_set_type(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.input_type = operands.get("input_type")

def micro_input_enable(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.read_enable = True

def micro_output_set_src(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.reg_src = operands.get("reg_src")

def micro_output_set_port(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.port = int(operands.get("port", "0"), 2)

def micro_output_set_type(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.output_type = operands.get("output_type")

def micro_output_enable(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.write_enable = True

def micro_stop(control_signals: ControlSignals, operands: dict[str, str]):
    control_signals.halt = True

MICROPROGRAM: dict[str, list[MicroInstruction]] = {
    "load": [
        micro_load_set_dest,
        micro_load_set_immediate,
        micro_load_enable
    ],
    "load_from": [
        micro_load_from_set_dest,
        micro_load_from_set_src,
        micro_load_from_enable
    ],
    "store": [
        micro_store_set_src,
        micro_store_set_address,
        micro_store_enable
    ],
    "store_to": [
        micro_store_set_dest,
        micro_store_enable
    ],
    "add": [
        micro_add_sub_mod_set_dest,
        micro_add_sub_mod_set_src,
        lambda cs, operands: micro_add_sub_mod_enable(cs, {**operands, "alu_op": "add"})
    ],
    "sub": [
        micro_add_sub_mod_set_dest,
        micro_add_sub_mod_set_src,
        lambda cs, operands: micro_add_sub_mod_enable(cs, {**operands, "alu_op": "sub"})
    ],
    "mod": [
        micro_add_sub_mod_set_dest,
        micro_add_sub_mod_set_src,
        lambda cs, operands: micro_add_sub_mod_enable(cs, {**operands, "alu_op": "mod"})
    ],
    "cmp": [
        micro_cmp_set_src1,
        micro_cmp_set_src2,
        micro_cmp_enable
    ],
    "jmp": [
        micro_jmp_set_address,
        micro_jmp_set_branch,
        micro_jmp_enable
    ],
    "je": [
        micro_jmp_set_address,
        micro_jmp_set_branch,
        micro_jmp_enable
    ],
    "jn": [
        micro_jmp_set_address,
        micro_jmp_set_branch,
        micro_jmp_enable
    ],
    "input": [
        micro_input_set_dest,
        micro_input_set_port,
        lambda cs, operands: micro_input_set_type(cs, {"input_type": "number"}),
        micro_input_enable
    ],
    "inputchar": [
        micro_input_set_dest,
        micro_input_set_port,
        lambda cs, operands: micro_input_set_type(cs, {"input_type": "char"}),
        micro_input_enable
    ],
    "output": [
        micro_output_set_src,
        micro_output_set_port,
        lambda cs, operands: micro_output_set_type(cs, {"output_type": "number"}),
        micro_output_enable
    ],
    "outputchar": [
        micro_output_set_src,
        micro_output_set_port,
        lambda cs, operands: micro_output_set_type(cs, {"output_type": "char"}),
        micro_output_enable
    ],
    "stop": [
        micro_stop
    ],
}

class Decoder:
    def __init__(self):
        self.control_signals = ControlSignals()
        self.current_microprogram: list[MicroInstruction] = []
        self.micro_step = 0
        self.reg_bin_to_name = {v: k for k, v in REGISTERS.items()}
        self.operands: dict[str, str] = {}

    def reset_microcode(self):
        self.control_signals.reset()
        self.current_microprogram = []
        self.micro_step = 0
        self.operands = {}

    def decode(self, instruction_str: str) -> dict[str, str | None]:
        self.control_signals.reset()
        opcode_bin = instruction_str[:5]
        operand1_bin = instruction_str[5:28]
        operand2_bin = instruction_str[28:51]

        opcode_str = None
        for key, value in OPCODES.items():
            if value == opcode_bin:
                opcode_str = key
                break

        if opcode_str is None:
            raise Exception(f"[Error] Неизвестный опкод: {opcode_bin}")

        self.operands = {}
        if opcode_str in ["load", "load_from", "store", "store_to",
                            "add", "sub", "mod", "cmp",
                            "jmp", "je", "jn",
                            "input", "inputchar", "output", "outputchar"]:
            self.operands["reg_dest"] = self.reg_bin_to_name.get(operand1_bin, None)
            self.operands["reg_src"] = self.reg_bin_to_name.get(operand2_bin, None)
            if opcode_str in ["store", "outputchar", "output", "input", "inputchar"]:
                self.operands["reg_src"] = self.reg_bin_to_name.get(operand1_bin, None)
            self.operands["immediate"] = operand2_bin
            self.operands["address"] = operand2_bin
            self.operands["port"] = operand2_bin
            self.operands["reg_src1"] = self.reg_bin_to_name.get(operand1_bin, None)
            self.operands["reg_src2"] = self.reg_bin_to_name.get(operand2_bin, None)
            self.operands["branch"] = opcode_str  # Для jmp, je, jn

            if opcode_str == "inputchar":
                self.operands["input_type"] = "char"
            elif opcode_str == "input":
                self.operands["input_type"] = "number"

            if opcode_str == "outputchar":
                self.operands["output_type"] = "char"
            elif opcode_str == "output":
                self.operands["output_type"] = "number"

        self.current_microprogram = MICROPROGRAM.get(opcode_str, [])
        for i in range(len(self.current_microprogram)):
            micro_instruction = self.current_microprogram[i]
            micro_instruction(self.control_signals,self.operands)

        return self.control_signals.__dict__.copy()
