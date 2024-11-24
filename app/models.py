from app import db  # Импортируем экземпляр db из app/__init__.py
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)  # Роль администратора

    # Связь с UserTask
    tasks = relationship("UserTask", back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.username}>"

class Task(db.Model):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    test_count = Column(Integer, default=0)

    # Связь с UserTask
    users = relationship("UserTask", back_populates="task")

    def __repr__(self) -> str:
        return f"<Task {self.title}>"

class UserTask(db.Model):
    __tablename__ = "user_tasks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    solved = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Связи с User и Task
    user = relationship("User", back_populates="tasks")
    task = relationship("Task", back_populates="users")

    def __repr__(self) -> str:
        return f"<UserTask User={self.user_id}, Task={self.task_id}, Solved={self.solved}>"
