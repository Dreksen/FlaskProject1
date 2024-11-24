# app/routes/admin.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Task, db
from app.forms import TaskForm

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Убедимся, что только администратор может редактировать задачи
@bp.before_request
def check_admin():
    if not current_user.is_admin:
        return redirect(url_for('profile.profile'))

# Страница списка задач
@bp.route("/tasks", methods=["GET"])
@login_required
def tasks_list():
    tasks = Task.query.all()
    return render_template("templates/admin/tasks_list.html", tasks=tasks)

# Страница добавления новой задачи
@bp.route("/tasks/add", methods=["GET", "POST"])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        num_tests = form.num_tests.data
        correct_solution = form.correct_solution.data

        new_task = Task(
            title=title,
            description=description,
            num_tests=num_tests,
            correct_solution=correct_solution
        )

        db.session.add(new_task)
        db.session.commit()

        flash("Задача успешно добавлена!", "success")
        return redirect(url_for("admin.tasks_list"))

    return render_template("templates/admin/add_task.html", form=form)

# Страница редактирования задачи
@bp.route("/tasks/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.num_tests = form.num_tests.data
        task.correct_solution = form.correct_solution.data

        db.session.commit()
        flash("Задача успешно обновлена!", "success")
        return redirect(url_for("admin.tasks_list"))

    return render_template("templates/admin/edit_task.html", form=form, task=task)

# Страница удаления задачи
@bp.route("/tasks/delete/<int:task_id>", methods=["GET", "POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Задача успешно удалена!", "success")
    return redirect(url_for("admin.tasks_list"))
