# APK Security Scanner

Система автоматизированного анализа безопасности Android-приложений на базе MobSF.

## Требования

- Docker Desktop
- Git

## Быстрая установка

1. Клонируйте репозиторий:
```bash
git clone <URL_РЕПОЗИТОРИЯ>
cd <НАЗВАНИЕ_ПАПКИ>
```

2. Создайте файл `.env` со следующим содержимым:
```
MOBSF_API_KEY=your_secret_key_here
```

3. Создайте необходимые директории:
```bash
mkdir apk results reports
```

4. Запустите систему:
```bash
docker compose up -d
```

## Использование

1. Поместите APK файл в папку `apk/`
2. Система автоматически начнет сканирование
3. Результаты будут доступны в:
   - `results/` - JSON отчеты
   - `reports/` - HTML отчеты
   - Веб-интерфейс: http://localhost:8003

## Обновление

Для получения последних обновлений:
```bash
git pull
docker compose down
docker compose up -d --build
```

## Структура проекта

```
.
├── apk/                # Папка для APK файлов
├── results/            # JSON отчеты
├── reports/            # HTML отчеты
├── main.py            # Основной скрипт
├── docker-compose.yml # Конфигурация Docker
├── Dockerfile         # Сборка сканера
└── requirements.txt   # Python зависимости
``` 