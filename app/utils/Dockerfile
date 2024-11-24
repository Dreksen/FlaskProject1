# Используем официальный образ Python как базовый
FROM python:3.11-slim


# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем весь код в контейнер
COPY . /app

# Устанавливаем зависимости (если они есть)
RUN pip install --no-cache-dir -r requirements.txt

# Команда по умолчанию для запуска вашего кода
CMD ["python", "solution.py"]
