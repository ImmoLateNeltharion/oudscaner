from pathlib import Path
import aiohttp
from loguru import logger
from typing import Dict, Any
from .base_scanner import BaseScanner

class MobSFScanner(BaseScanner):
    """Сканер на основе MobSF"""
    
    def __init__(self, api_key: str, host: str = "http://localhost:8003"):
        super().__init__("MobSF")
        self.api_key = api_key
        self.host = host
        
    async def scan(self, apk_path: Path) -> Dict[str, Any]:
        """Выполняет сканирование через MobSF API"""
        logger.info(f"Начинаю сканирование {apk_path} через MobSF")
        
        async with aiohttp.ClientSession() as session:
            # Загрузка файла
            upload_url = f"{self.host}/api/v1/upload"
            files = {'file': open(apk_path, 'rb')}
            headers = {'Authorization': self.api_key}
            
            async with session.post(upload_url, data=files, headers=headers) as response:
                upload_result = await response.json()
                scan_hash = upload_result.get('hash')
                
            if not scan_hash:
                raise Exception("Ошибка при загрузке файла в MobSF")
                
            # Запуск сканирования
            scan_url = f"{self.host}/api/v1/scan"
            data = {'hash': scan_hash, 'scan_type': 'apk'}
            
            async with session.post(scan_url, data=data, headers=headers) as response:
                scan_result = await response.json()
                
            # Получение отчета
            report_url = f"{self.host}/api/v1/report_json"
            data = {'hash': scan_hash}
            
            async with session.post(report_url, data=data, headers=headers) as response:
                report = await response.json()
                
            logger.info("Сканирование MobSF завершено")
            return report
            
    def is_available(self) -> bool:
        """Проверяет доступность MobSF"""
        try:
            import requests
            response = requests.get(self.host)
            return response.status_code == 200
        except:
            return False
            
    def get_requirements(self) -> str:
        return """
        1. Установленный и запущенный MobSF
        2. API ключ MobSF
        3. Python пакеты: aiohttp, requests
        """ 