# Используем базовый образ с Python
FROM python:latest

# Устанавливаем зависимости
WORKDIR /server
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы приложения в контейнер
COPY . .

# Указываем переменную окружения, чтобы не было ошибок с локализацией
ENV PYTHONUNBUFFERED 1

