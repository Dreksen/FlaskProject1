from flask import Blueprint, render_template
from app.models import db, UserTask, Task, User
from flask_login import login_required, current_user

bp = Blueprint("profile", __name__, url_prefix="/profile", template_folder="templates/profile")

@bp.route("/", methods=["GET"])
@login_required
def profile():
    """Отображает профиль пользователя и список решённых им задач"""
    solved_tasks = UserTask.query.filter_by(user_id=current_user.id, solved=True).all()
    return render_template("profile.html", solved_tasks=solved_tasks)


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
