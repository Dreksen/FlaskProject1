from flask import Blueprint, render_template
from app.models import db, UserTask, Task, User
from flask_login import login_required, current_user

bp = Blueprint("profile", __name__, url_prefix="/profile", template_folder="templates/profile")


@bp.route("/", methods=["GET"])
@login_required
def profile():
    """Отображает профиль пользователя."""
    # Получаем текущего пользователя
    user = current_user

    # Получаем количество решённых задач
    solved_tasks_count = UserTask.query.filter_by(user_id=user.id, solved=True).count()

    # Получаем общее количество задач
    total_tasks_count = Task.query.count()

    return render_template("profile.html", user=user, solved_tasks_count=solved_tasks_count,
                           total_tasks_count=total_tasks_count)

@bp.route("/ranking", methods=["GET"])
def ranking():
    """Отображает таблицу с рейтингом пользователей."""
    # Получаем всех пользователей
    users = User.query.all()

    # Для каждого пользователя считаем количество решённых задач
    user_ranks = []
    for user in users:
        solved_tasks_count = UserTask.query.filter_by(user_id=user.id, solved=True).count()
        total_tasks_count = Task.query.count()
        user_ranks.append({
            'username': user.username,
            'solved': solved_tasks_count,
            'total': total_tasks_count,
            'rank': solved_tasks_count / total_tasks_count * 100  # Процент решённых задач
        })

    # Сортируем пользователей по количеству решённых задач в порядке убывания
    user_ranks.sort(key=lambda x: x['solved'], reverse=True)

    return render_template("ranking.html", user_ranks=user_ranks)
