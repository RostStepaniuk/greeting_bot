# Используйте официальный образ Python как базовый
FROM python:3.11-slim

# Установите рабочую директорию в контейнере
WORKDIR /app

# Копируйте файлы зависимостей в рабочую директорию
COPY ./requirements.txt /app/requirements.txt

# Обновите pip
RUN pip install --upgrade pip

# Установите зависимости
RUN pip install -v --no-cache-dir -r requirements.txt

# Копируйте код вашего бота в рабочую директорию
COPY . .

# Укажите команду для запуска бота
CMD ["python", "./main.py"]
