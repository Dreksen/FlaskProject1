# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем код в контейнер
WORKDIR /app
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем директорию, где будут находиться тесты
WORKDIR /app/tests

# Запускаем решение
CMD ["python3", "solution.py"]
