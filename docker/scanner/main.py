import os
import requests
import time
import json
from pathlib import Path
import mimetypes

class SimpleMobSFScanner:
    def __init__(self):
        self.api_key = os.getenv('MOBSF_API_KEY')
        self.host = os.getenv('MOBSF_HOST', 'http://mobsf:8000')
        print(f"Инициализация сканера с хостом: {self.host}")
        print(f"API ключ установлен: {'Да' if self.api_key else 'Нет'}")
        
    def scan_apk(self, apk_path):
        print(f"Начинаем сканирование файла: {apk_path}")
        print(f"Проверяем существование файла: {os.path.exists(apk_path)}")
        
        # Загрузка файла
        upload_url = f"{self.host}/api/v1/upload"
        print(f"URL для загрузки: {upload_url}")
        
        try:
            with open(apk_path, 'rb') as apk_file:
                filename = os.path.basename(apk_path)
                # Формируем multipart/form-data как в веб-интерфейсе
                files = {
                    'file': (
                        filename,
                        apk_file,
                        'application/vnd.android.package-archive'
                    )
                }
                headers = {
                    'Authorization': self.api_key,
                    'Accept': 'application/json',
                }
                print("Отправляем файл на сервер...")
                # Добавляем параметр verify=False для игнорирования SSL
                response = requests.post(
                    upload_url,
                    files=files,
                    headers=headers,
                    verify=False
                )
                print(f"Код ответа: {response.status_code}")
                print(f"Ответ сервера: {response.text}")
                
            if response.status_code != 200:
                raise Exception(f"Ошибка загрузки файла: {response.text}")
                
            scan_data = response.json()
            print(f"Данные для сканирования: {scan_data}")
            
            # Запуск сканирования
            scan_url = f"{self.host}/api/v1/scan"
            data = {
                'scan_type': scan_data['scan_type'],
                'file_name': scan_data['file_name'],
                'hash': scan_data['hash']
            }
            response = requests.post(scan_url, data=data, headers=headers, verify=False)
            
            if response.status_code != 200:
                raise Exception(f"Ошибка сканирования: {response.text}")
                
            # Сохранение результатов
            results_path = Path('/results')
            reports_path = Path('/app/reports')
            
            results_path.mkdir(exist_ok=True)
            reports_path.mkdir(exist_ok=True)
            
            # Сохраняем JSON результат
            with open(results_path / f"{scan_data['file_name']}_report.json", 'w') as f:
                json.dump(response.json(), f, indent=4)
                
            # Запрашиваем PDF отчет
            pdf_url = f"{self.host}/api/v1/download_pdf"
            response = requests.post(pdf_url, data=data, headers=headers, verify=False)
            
            if response.status_code == 200:
                with open(reports_path / f"{scan_data['file_name']}_report.pdf", 'wb') as f:
                    f.write(response.content)
                
            return response.json()
        except Exception as e:
            print(f"Произошла ошибка при сканировании: {str(e)}")
            raise

def main():
    scanner = SimpleMobSFScanner()
    
    # Сканирование всех APK файлов в директории
    source_dir = Path('/app/source')
    print(f"Ищем APK файлы в директории: {source_dir}")
    print(f"Директория существует: {source_dir.exists()}")
    print(f"Содержимое директории: {list(source_dir.glob('*'))}")
    
    for apk_file in source_dir.glob('*.apk'):
        print(f"Сканирование {apk_file.name}...")
        try:
            results = scanner.scan_apk(str(apk_file))
            print(f"Сканирование {apk_file.name} завершено успешно")
            print(f"Результаты сохранены в папках /results и /app/reports")
        except Exception as e:
            print(f"Ошибка при сканировании {apk_file.name}: {str(e)}")

def wait_for_mobsf():
    print("Ожидаем готовности MobSF...")
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            response = requests.get('http://mobsf:8000', verify=False)
            if response.status_code == 200:
                print("MobSF готов к работе!")
                return True
        except:
            print(f"Попытка {attempt + 1}/{max_attempts}. MobSF еще не готов...")
        time.sleep(10)
    raise Exception("MobSF не запустился после нескольких попыток")

if __name__ == '__main__':
    # Отключаем предупреждения о SSL
    requests.packages.urllib3.disable_warnings()
    wait_for_mobsf()
    main() 