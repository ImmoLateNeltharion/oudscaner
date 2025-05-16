import os
import requests
import json
import time
from pathlib import Path

# Конфигурация
MOBSF_URL = "http://localhost:9001"
API_KEY = "b0d4bff3ceeeb37fd673827dcf7c2f510fcb40a875d0cbf7635dfe6c1d7bf5d5"
APK_PATH = "dvba.apk"

def upload_and_scan():
    # Заголовки для API
    headers = {
        "Authorization": API_KEY
    }
    
    # Загрузка файла
    print("Загрузка APK файла...")
    with open(APK_PATH, 'rb') as f:
        files = {'file': (APK_PATH, f, 'application/octet-stream')}
        response = requests.post(
            f"{MOBSF_URL}/api/v1/upload",
            headers=headers,
            files=files
        )
    
    if response.status_code != 200:
        print(f"Ошибка при загрузке: {response.text}")
        return
    
    # Получаем хеш файла
    file_hash = response.json().get('hash')
    print(f"Файл загружен. Хеш: {file_hash}")
    
    # Запускаем сканирование
    print("Запуск сканирования...")
    scan_data = {
        'scan_type': 'apk',
        'file_name': APK_PATH,
        'hash': file_hash,
        're_scan': '0',
        'scan_mode': 'static',
        'skip_apkid': '1'  # Пропускаем APKiD анализ
    }
    
    response = requests.post(
        f"{MOBSF_URL}/api/v1/scan",
        headers=headers,
        data=scan_data
    )
    
    if response.status_code != 200:
        print(f"Ошибка при сканировании: {response.text}")
        return
    
    print("Сканирование запущено успешно")
    
    # Ждем немного, чтобы сканирование успело начаться
    print("Ожидание результатов сканирования...")
    time.sleep(10)
    
    # Получаем результаты
    print("Получение результатов...")
    max_attempts = 12  # 12 попыток по 10 секунд = 2 минуты
    for attempt in range(max_attempts):
        response = requests.get(
            f"{MOBSF_URL}/api/v1/report_json/{file_hash}",
            headers=headers
        )
        if response.status_code == 200:
            # Сохраняем результаты в JSON
            with open(f"scan_results_{file_hash}.json", 'w', encoding='utf-8') as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=2)
            print(f"Результаты сохранены в scan_results_{file_hash}.json")
            # Выводим основные результаты
            results = response.json()
            print("\nОсновные результаты сканирования:")
            print(f"Имя приложения: {results.get('app_name', 'Неизвестно')}")
            print(f"Версия: {results.get('version_name', 'Неизвестно')}")
            print(f"Пакет: {results.get('package_name', 'Неизвестно')}")
            print(f"Уровень безопасности: {results.get('security_score', 'Неизвестно')}")
            break
        else:
            print(f"Попытка {attempt+1}: отчет не готов, жду 10 секунд...")
            time.sleep(10)
    else:
        print(f"JSON-отчёт не найден через GET. Пробую получить через POST...")
        post_data = {"hash": file_hash, "type": "apk"}
        post_response = requests.post(f"{MOBSF_URL}/api/v1/report_json", headers=headers, data=post_data)
        if post_response.status_code == 200:
            with open(f"scan_results_{file_hash}_post.json", 'w', encoding='utf-8') as f:
                json.dump(post_response.json(), f, ensure_ascii=False, indent=2)
            print(f"JSON-отчёт (POST) сохранён в scan_results_{file_hash}_post.json")
            results = post_response.json()
            print("\nОсновные результаты сканирования:")
            print(f"Имя приложения: {results.get('app_name', 'Неизвестно')}")
            print(f"Версия: {results.get('version_name', 'Неизвестно')}")
            print(f"Пакет: {results.get('package_name', 'Неизвестно')}")
            print(f"Уровень безопасности: {results.get('security_score', 'Неизвестно')}")
        else:
            print(f"Ошибка при получении JSON-отчёта через POST: {post_response.text}")

if __name__ == "__main__":
    upload_and_scan() 