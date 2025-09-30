import importlib
import io
import sys
import types

import pytest

def _import_tasks():
    try:
        return importlib.import_module("tasks")
    except Exception as e:
        pytest.fail(
            "Не удалось импортировать файл tasks.py.\n"
            "Убедитесь, что файл tasks.py лежит рядом с тестом и не содержит ошибок синтаксиса.\n"
            f"Подробности ошибки: {e}"
        )


class CaptureStdout:
    """
    Контекстный менеджер для аккуратного захвата stdout.
    Не требует capsys, можно использовать и внутри вспомогательных функций.
    """
    def __enter__(self):
        self._old = sys.stdout
        self.buffer = io.StringIO()
        sys.stdout = self.buffer
        return self

    def __exit__(self, exc_type, exc, tb):
        sys.stdout = self._old

    @property
    def text(self):
        return self.buffer.getvalue()


def call_and_grab(func, *args, **kwargs) -> str:
    """Вызывает функцию и возвращает всё, что было напечатано в stdout."""
    if not isinstance(func, types.FunctionType):
        pytest.fail(
            f"Ожидалась функция, но получено: {type(func)}. "
            "Проверьте, что вы определили нужную функцию в tasks.py."
        )
    with CaptureStdout() as cap:
        func(*args, **kwargs)
    return cap.text


def normalize_eol(s: str) -> str:
    """Нормализуем переводы строк к '\n' и убираем завершающий перевод строки, если он один."""
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    # Разрешаем финальный перевод строки, поэтому .rstrip('\n') только один раз:
    if s.endswith("\n"):
        s = s[:-1]
    return s


def assert_exact_output(actual: str, expected: str, help_text: str):
    a = normalize_eol(actual)
    e = normalize_eol(expected)
    assert a == e, (
        f"{help_text}\n"
        "— ОЖИДАЛОСЬ:\n"
        f"{repr(e)}\n"
        "— ПОЛУЧЕНО:\n"
        f"{repr(a)}\n"
        "Проверьте: пробелы, знаки препинания, кавычки, табуляции и переносы строк."
    )


def test_01_name_age():
    tasks = _import_tasks()
    assert hasattr(tasks, "print_name_age"), (
        "В tasks.py должна быть функция print_name_age(name, age). "
        "См. описание в шапке теста."
    )
    out = call_and_grab(tasks.print_name_age, "Аня", 15)
    expected = "Имя: Аня, Возраст: 15"
    assert_exact_output(
        out, expected,
        "Задание: вывод имени и возраста. Формат должен быть точным: Имя: <name>, Возраст: <age>"
    )


def test_02_greeting():
    tasks = _import_tasks()
    out = call_and_grab(tasks.print_greeting)
    expected = "Привет!Как твои дела?"
    assert_exact_output(
        out, expected,
        "Задание: вывод фразы 'Привет!Как твои дела?'. Обратите внимание: после '!' нет пробела."
    )


def test_03_poem():
    tasks = _import_tasks()
    out = call_and_grab(tasks.print_poem)
    expected = (
        "Береза под моим окном\n"
        "Принакрылась снегом.\n"
        "Точно серебром."
    )
    assert_exact_output(
        out, expected,
        "Задание: вывод стихотворения тремя строками. Каждая строка на новой строке."
    )


def test_04_quote():
    tasks = _import_tasks()
    out = call_and_grab(tasks.print_quote)
    expected = "Он сказал: \"Учить Python - это весело!\""
    assert_exact_output(
        out, expected,
        "Задание: вывод текста с кавычками. Используйте двойные кавычки внутри строки, "
        "экранируйте при необходимости."
    )


def test_05_numbers_with_space():
    tasks = _import_tasks()
    out = call_and_grab(tasks.print_numbers_with_space)
    expected = "1 2 3 4 5"
    assert_exact_output(
        out, expected,
        "Задание 1: числа от 1 до 5 через ПРОБЕЛ в одной строке."
    )


def test_06_hello_exclamations():
    tasks = _import_tasks()
    out = call_and_grab(tasks.print_hello_exclamations)
    expected = "Hello!\nHello!\nHello!"
    assert_exact_output(
        out, expected,
        "Задание 2: три строки 'Hello!' — каждая на новой строке."
    )


def test_07_table_squares():
    tasks = _import_tasks()
    out = call_and_grab(tasks.print_table_squares)
    expected = "1\t1\n2\t4\n3\t9"
    assert_exact_output(
        out, expected,
        "Задание 3: таблица с табуляцией между числом и квадратом. Символ табуляции — '\\t'."
    )


def test_08_sum_with_text():
    tasks = _import_tasks()
    out = call_and_grab(tasks.print_sum_with_text)
    expected = "5 + 10 = 15"
    assert_exact_output(
        out, expected,
        "Задание 4: выведите результат сложения 5 и 10 в формате '5 + 10 = 15'."
    )


def test_09_three_numbers_with_commas():
    tasks = _import_tasks()
    out = call_and_grab(tasks.print_three_numbers_with_commas)
    expected = "1, 2, 3"
    assert_exact_output(
        out, expected,
        "Задание 5: три числа в одной строке с ЗАПЯТОЙ и пробелом после запятой."
    )
