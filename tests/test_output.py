import pytest
import runpy
import io
import sys

def run_student_code():
    buf = io.StringIO()
    sys_stdout = sys.stdout
    try:
        sys.stdout = buf
        # Выполнить main.py как скрипт
        runpy.run_path("main.py", run_name="__main__")
    finally:
        sys.stdout = sys_stdout
    return buf.getvalue().strip().splitlines()

def test_output_lines():
    output = run_student_code()
    # проверим, что хотя бы 2 строки вывода
    assert len(output) >= 2, "Должно быть минимум 2 print()"
    # первая строка должна быть строкой
    assert output[0] == "Hello, world!"
    # вторая строка должна быть числом
    assert output[1] == "42"
