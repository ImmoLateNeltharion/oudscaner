FROM python:3.9-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка необходимых Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов проекта
COPY . .

# Создание необходимых директорий
RUN mkdir -p /app/apk /results /app/reports

# Установка прав на директории
RUN chmod -R 755 /app/apk /results /app/reports

ENTRYPOINT ["python", "main.py"]
CMD ["--auto-scan"] 