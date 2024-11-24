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
    """Отображает рейтинг пользователей по количеству решённых задач"""
    users = db.session.query(User, db.func.count(UserTask.id).label("solved_count"))\
        .join(UserTask, User.id == UserTask.user_id)\
        .filter(UserTask.solved == True)\
        .group_by(User.id)\
        .order_by(db.desc("solved_count"))\
        .limit(50).all()  # Показываем только топ 50 пользователей

    return render_template("ranking.html", users=users)
