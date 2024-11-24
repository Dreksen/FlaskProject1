from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
from flask_login import logout_user

bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates/auth")



@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        password_hash = generate_password_hash(password, method="pbkdf2:sha256")

        if User.query.filter_by(email=email).first():
            flash("Email уже зарегистрирован.", "danger")
            return redirect(url_for("auth.register"))

        user = User(username=username, email=email, password=password_hash)
        db.session.add(user)
        db.session.commit()

        flash("Регистрация успешна. Теперь вы можете войти.", "success")
        return redirect(url_for("auth.login"))

    return render_template('register.html')

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Вы успешно вошли.", "success")
            return redirect(url_for("profile.profile", username=user.username))

        flash("Неправильный email или пароль.", "danger")
        return redirect(url_for("auth.login"))

    return render_template("login.html")

@bp.route("/logout")
def logout():
    """Выход пользователя из системы"""
    logout_user()
    flash("Вы успешно вышли из системы.", "success")
    return redirect(url_for("auth.login"))
