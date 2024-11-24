from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='templates/static')
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = Config.SECRET_KEY

    # app.jinja_env.globals['EXPLAIN_TEMPLATE_LOADING'] = True  # Включить отладку загрузки шаблонов

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Редирект для неавторизованных пользователей

    # Импортируем маршруты и модели внутри контекста приложения
    with app.app_context():
        # Регистрируем маршруты
        from app.routes.auth import auth
        app.register_blueprint(auth.bp, url_prefix='/auth')

        from app.routes.tasks import tasks
        app.register_blueprint(tasks.bp, url_prefix='/tasks')

        from app.routes.profile import profile
        app.register_blueprint(profile.bp, url_prefix='/profile')

        from app.routes.admin import admin
        app.register_blueprint(admin.bp, url_prefix='/admin')

        from app.models import User, Task, UserTask
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Импортируем модель только здесь
    return User.query.get(int(user_id))

