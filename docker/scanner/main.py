import os
import requests
import time
import json
from pathlib import Path

class SimpleMobSFScanner:
    def __init__(self):
        self.api_key = os.getenv('MOBSF_API_KEY')
        self.host = os.getenv('MOBSF_HOST', 'http://mobsf:8000')
        
    def scan_apk(self, apk_path):
        # Загрузка файла
        upload_url = f"{self.host}/api/v1/upload"
        with open(apk_path, 'rb') as apk_file:
            files = {'file': apk_file}
            headers = {'Authorization': self.api_key}
            response = requests.post(upload_url, files=files, headers=headers)
            
        if response.status_code != 200:
            raise Exception(f"Ошибка загрузки файла: {response.text}")
            
        scan_data = response.json()
        
        # Запуск сканирования
        scan_url = f"{self.host}/api/v1/scan"
        data = {
            'scan_type': scan_data['scan_type'],
            'file_name': scan_data['file_name'],
            'hash': scan_data['hash']
        }
        response = requests.post(scan_url, data=data, headers=headers)
        
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
        response = requests.post(pdf_url, data=data, headers=headers)
        
        if response.status_code == 200:
            with open(reports_path / f"{scan_data['file_name']}_report.pdf", 'wb') as f:
                f.write(response.content)
            
        return response.json()

def main():
    scanner = SimpleMobSFScanner()
    
    # Сканирование всех APK файлов в директории
    source_dir = Path('/app/source')
    for apk_file in source_dir.glob('*.apk'):
        print(f"Сканирование {apk_file.name}...")
        try:
            results = scanner.scan_apk(str(apk_file))
            print(f"Сканирование {apk_file.name} завершено успешно")
            print(f"Результаты сохранены в папках /results и /app/reports")
        except Exception as e:
            print(f"Ошибка при сканировании {apk_file.name}: {str(e)}")

if __name__ == '__main__':
    # Ждем, пока MobSF будет готов
    time.sleep(30)
    main() 