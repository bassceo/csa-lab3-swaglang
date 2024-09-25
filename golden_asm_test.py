import tempfile
import os
import pytest
import logging

from translator.Translator import SwagLangTranslator
from processor.ControlUnit import ControlUnit
from processor.InputDevice import InputDevice
from processor.OutputDevice import OutputDevice
from processor.DataPath import Datapath
from processor.Clock import Clock


@pytest.mark.golden_test("golden/*_sl.yml")
def test_translator_pipeline(golden, caplog):
    caplog.set_level(logging.DEBUG)

    with tempfile.TemporaryDirectory() as tmpdirname:
        source = os.path.join(tmpdirname, "source.sl")
        input_data = golden["in_stdin"]

        with open(source, "w", encoding="utf-8") as file:
            file.write(golden["in_source"])

        output, translated = run_pipeline(source, input_data)
        
        assert output.replace(" ", '').replace('\n', '').replace('\x00', '') == (golden.out["out_stdout"].replace(" ", '').replace('\n', '').replace('\x00', ''))
        assert translated.replace(" ", '').replace('\n', '') == (golden.out["out_code"].replace(" ", '').replace('\n', ''))
        
        if len(caplog.text) >= 124000:
            lines = caplog.text.splitlines()[:1000]
            assert "\n".join(lines).replace(" ", '').replace('\n', '') == golden.out["out_log"].splitlines()[:1000].replace(" ", '').replace('\n', '')
        else:
            assert caplog.text.replace(" ", '').replace('\n', '') == golden.out["out_log"].replace(" ", '').replace('\n', '')


def read_code_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
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
        instr = translated[i * 51:(i + 1) * 51]
        instructions.append(instr)
    
    control_unit.run(clock, instructions)
    
    output = {}
    for port, data in output_device.buffer.items():
        output[port] = ''.join(data)
    
    return output[2],translated