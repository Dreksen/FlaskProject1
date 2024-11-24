from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Task, UserTask, db
from flask_login import login_required, current_user
import subprocess

bp = Blueprint("tasks", __name__, url_prefix="/tasks", template_folder="templates/tasks")

@bp.route("/task_<int:task_id>", methods=["GET", "POST"])
@login_required
def task_detail(task_id: int):
    """Отображает задачу и принимает решение от пользователя."""
    task = Task.query.get_or_404(task_id)
    user_task = UserTask.query.filter_by(user_id=current_user.id, task_id=task.id).first()
    result = None
    success = False
    if request.method == "POST":
        solution_code = request.form["solution_code"]
        result = run_tests(solution_code, str(task_id))

        if "Правильное ответ!" in result:
            success = True
            if user_task:
                user_task.solved = True
            else:
                user_task = UserTask(user_id=current_user.id, task_id=task.id, solved=True)
                db.session.add(user_task)
            db.session.commit()
    print("point1end")
    return render_template("task_detail.html", task=task, result=result, success=success)

@bp.route("/", methods=["GET"])
@login_required
def task_list():
    """Отображает список всех задач"""
    tasks = Task.query.all()
    return render_template("list.html", tasks=tasks)

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
            'python3', 'app/utils/run_solution.py', code, str(task_number), str(test_count)
        ]
        result = subprocess.run(command, capture_output=True, text=True)

        # Логирование stdout и stderr
        # app.logger.info(f"stdout: {result.stdout}")
        # app.logger.error(f"stderr: {result.stderr}")

        # Возвращаем результат выполнения тестов
        return result.stdout.strip()
    except Exception as e:
        return f"Ошибка при запуске тестов: {str(e)}"