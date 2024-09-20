import sys
import logging
from pathlib import Path
from datetime import datetime
from pipeline import run_pipeline
import json
import contextlib
import io

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_result(result_path, data):
    with open(result_path, 'w', encoding='utf-8') as f:
        f.write("in_source: |-\n")
        for line in data['in_source'].splitlines():
            f.write(f"  {line}\n")
        
        f.write("in_stdin: |\n")
        f.write(f"  {data['in_stdin']}\n\n")
        
        f.write("out_code: |-\n")
        json_out_code = json.dumps(data['out_code'], ensure_ascii=False, indent=2)
        for line in json_out_code.splitlines():
            f.write(f"  {line}\n")
        
        f.write("out_stdout: |\n")
        for line in data['out_stdout'].splitlines():
            f.write(f"  {line}\n")
        
        f.write("out_log: |\n")
        for line in data['out_log'].splitlines():
            f.write(f"  {line}\n")

def main():
    project_root = Path(__file__).parent.resolve()
    swag_lang_dir = project_root / "SwagLangPrograms"
    results_dir = project_root / "golden_asm_results"
    results_dir.mkdir(exist_ok=True)
    sl_files = list(swag_lang_dir.glob("*.sl"))
    
    if not sl_files:
        print(f"Нет файлов .sl в директории {swag_lang_dir}")
        sys.exit(1)
    
    for sl_file in sl_files:
        print(f"Запуск теста для файла: {sl_file.name}")
        try:
            in_source = read_file(sl_file)
            stdin_file = swag_lang_dir / f"{sl_file.stem}_stdin.txt"
            in_stdin = read_file(stdin_file).strip() if stdin_file.exists() else ''
            stdout_capture = io.StringIO()
            log_capture = io.StringIO()
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)
            if logger.hasHandlers():
                logger.handlers.clear()
            log_handler = logging.StreamHandler(log_capture)
            log_handler.setLevel(logging.DEBUG)
            log_handler.setFormatter(logging.Formatter('%(levelname)s | %(message)s'))
            logger.addHandler(log_handler)
            
            with contextlib.redirect_stdout(stdout_capture):
                output_code = run_pipeline(str(sl_file), input_str=in_stdin)
            
            out_stdout = stdout_capture.getvalue().strip()
            out_log = log_capture.getvalue().strip()
            result_data = {
                "in_source": in_source,
                "in_stdin": in_stdin,
                "out_code": output_code,
                "out_stdout": out_stdout,
                "out_log": out_log
            }
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            result_filename = f"{sl_file.stem}_result_{timestamp}.yml"
            result_path = results_dir / result_filename
            write_result(result_path, result_data)
            print(f"Результат сохранен в {result_path.name}\n")
        except Exception as e:
            print(f"Ошибка при выполнении теста для {sl_file.name}: {e}\n")
            error_result_data = {
                "in_source": locals().get('in_source', ''),
                "in_stdin": locals().get('in_stdin', ''),
                "out_code": {},
                "out_stdout": "",
                "out_log": f"Ошибка при выполнении пайплайна: {e}"
            }
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            error_result_filename = f"{sl_file.stem}_error_{timestamp}.yml"
            error_result_path = results_dir / error_result_filename
            write_result(error_result_path, error_result_data)
            print(f"Ошибка сохранена в {error_result_path.name}\n")
    
    print(f"Все тесты завершены. Результаты сохранены в директории {results_dir}")

if __name__ == "__main__":
    main()