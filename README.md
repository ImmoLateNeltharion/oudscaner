# APK Security Scanner

Система автоматизированного анализа безопасности Android-приложений на базе MobSF.

## Структура проекта

```
.
├── docker/             # Конфигурация Docker
│   ├── mobsf/         # Настройки MobSF
│   └── scanner/       # Сканер безопасности
├── source/            # Исходные APK файлы
├── results/           # JSON отчеты
└── reports/           # PDF отчеты
```

## Требования

- Docker Desktop
- Git

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/ImmoLateNeltharion/oudscaner.git
cd oudscaner
```

2. Создайте файл `.env` в корневой директории:
```
MOBSF_API_KEY=your_secret_key_here
```

3. Поместите APK файлы для анализа в папку `source/`

4. Запустите систему:
```bash
cd docker
docker compose up -d
```

## Использование

1. Система автоматически сканирует все APK файлы в папке `source/`
2. Результаты доступны в:
   - `results/` - JSON отчеты
   - `reports/` - PDF отчеты
   - Веб-интерфейс: http://localhost:8003

## Обновление

```bash
git pull
cd docker
docker compose down
docker compose up -d --build
``` 