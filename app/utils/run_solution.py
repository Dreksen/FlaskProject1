import sys
import logging
import os
import subprocess
import tempfile

# Настройка логирования
logging.basicConfig(filename='solution_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def execute_code(code, test_inputs):
    """Запуск кода в Docker с передачей тестовых данных через stdin"""
    try:
        # Сохраняем код решения в файл
        with open('solution.py', 'w') as f:
            f.write(code)

        # Формируем команду для Docker
        command = [
            'sudo', 'docker', 'run', '--rm', '-i',  # -i для ввода данных через stdin
            '-v', f'{os.getcwd()}:/app',  # Монтируем текущую директорию
            'my_python_image',  # Используем заранее созданный образ
            'python3', '/app/solution.py'  # Запускаем решение
        ]

        # Передаем данные в контейнер через stdin
        result = subprocess.run(command, input=test_inputs, text=True, capture_output=True)
        # print("RES: ", result.stdout)
        # Проверяем вывод и возвращаем результат
        if result.returncode != 0:
            return f"Ошибка выполнения: {result.stderr}"

        return result.stdout.strip()

    except Exception as e:
        return f"Ошибка при запуске тестов: {str(e)}"


def run_solution():
    """Запуск тестов с количеством, переданным через аргументы."""
    code = sys.argv[1]  # Получаем код решения из аргументов
    task_number = sys.argv[2]  # Номер задачи
    test_count = int(sys.argv[3])  # Количество тестов для задачи

    task_folder = f"tests/task_{task_number}"

    for i in range(1, test_count + 1):  # Тестируем столько раз, сколько указано
        test_input_file = os.path.join(task_folder, f"test{i}.txt")
        correct_answer_file = os.path.join(task_folder, f"answer{i}.txt")

        if not os.path.exists(test_input_file) or not os.path.exists(correct_answer_file):
            print(f"Не хватает тестов или ответов для теста {i} задачи {task_number}!")
            return

        # Читаем входные данные и правильные ответы
        with open(test_input_file, 'r') as test_file:
            test_inputs = test_file.read().strip()

        with open(correct_answer_file, 'r') as answer_file:
            correct_answer = answer_file.read().strip()

        # Выполнение решения
        result = execute_code(code, test_inputs)

        # Логирование полученного результата
        logging.info(f"Тест {i}: Ввод: {test_inputs}, Полученный результат: {result}, Ожидаемый ответ: {correct_answer}")

        # Сравнение с правильным ответом
        if result != correct_answer:
            logging.warning(f"Неправильный ответ на тесте {i}. Ожидалось: {correct_answer}, но получено: {result}")
            print(f"Неправильный ответ на тесте {i}.")
            return

    logging.info("Все тесты пройдены успешно!")
    print("Правильный ответ!")



if __name__ == "__main__":
    run_solution()
