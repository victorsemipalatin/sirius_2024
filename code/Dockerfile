# Указываем базовый образ с Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем все файлы из текущей директории в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем переменную окружения для запуска Flask
ENV FLASK_APP=app.py

# Открываем порт, на котором работает приложение Flask
EXPOSE 5000

# Команда для запуска Flask
CMD ["flask", "run", "--host=0.0.0.0"]