import subprocess
import os
from app.models import Task
def run_tests(code, task_number):
    """Запуск тестов для решения пользователя"""
    try:
        # Получаем задачу из базы данных
        task = Task.query.filter_by(id=task_number).first()
        if not task:
            return f"Задача с номером {task_number} не найдена.", 404

        test_count = task.test_count  # Количество тестов для данной задачи

        # Запуск процесса с передачей кода, номера задачи и количества тестов
        command = [
            'python3', 'run_solution.py', code, str(task_number), str(test_count)
        ]

        result = subprocess.run(command, capture_output=True, text=True)


        # Возвращаем результат выполнения тестов
        return result.stdout.strip()
    except Exception as e:
        return f"Ошибка при запуске тестов: {str(e)}"
