from app import create_app, db
from app.models import User, Task, UserTask

from app import db
from app.models import Task  # Замените на ваш файл с моделью Task

def update_task_tests(task_id, new_test_count):
    """
    Обновляет количество тестов у задачи по её ID.

    :param task_id: int - ID задачи
    :param new_test_count: int - Новое количество тестов
    """
    task = Task.query.get(task_id)
    if task:
        task.test_count = new_test_count  # Предполагается, что в модели Task есть поле test_count
        db.session.commit()
        print(f"Количество тестов для задачи {task_id} обновлено на {new_test_count}.")
    else:
        print(f"Задача с ID {task_id} не найдена.")


def seed_data():
    """Добавляет фиктивные данные в базу данных."""

    # Создание пользователей
    user1 = User(username="user1", email="user1@example.com", password="password")
    user2 = User(username="user2", email="user2@example.com", password="password")
    db.session.add_all([user1, user2])

    # Создание задач
    task1 = Task(title="А степень Б", description="Напишите программу, которая принимает два числа в отдельных строчках и выводит А в степени Б.")
    task2 = Task(title="Дни недели", description="Напишите программу, которая принимает номер дня недели и выводит ее название")
    db.session.add_all([task1, task2])
    db.session.commit()

    # Присваиваем задачи пользователям
    user1_task = UserTask(user_id=user1.id, task_id=task1.id, solved=True)
    user2_task = UserTask(user_id=user2.id, task_id=task2.id, solved=True)
    db.session.add_all([user1_task, user2_task])
    db.session.commit()

    print("Фиктивные данные успешно добавлены!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # Создаём таблицы, если их ещё нет
        # seed_data()
        update_task_tests(1,1)
