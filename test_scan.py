import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
from src.core.analyzer import SecurityAnalyzer
from src.scanners.mobsf import MobSFScanner
from src.report.generator import ReportGenerator

async def main():
    # Загрузка конфигурации
    load_dotenv()
    
    # Конфигурация сканеров
    mobsf_config = {
        "api_key": os.getenv("MOBSF_API_KEY"),
        "server_url": os.getenv("MOBSF_SERVER_URL", "http://localhost:8000")
    }
    
    # Инициализация сканеров
    scanners = [
        MobSFScanner(mobsf_config)
    ]
    
    # Создание анализатора
    analyzer = SecurityAnalyzer(scanners)
    
    # Проверка доступности сканеров
    for scanner in scanners:
        is_available = await scanner.is_available()
        print(f"Сканер {scanner.name} {'доступен' if is_available else 'недоступен'}")
        if is_available:
            version = await scanner.get_version()
            print(f"Версия: {version}")

if __name__ == "__main__":
    asyncio.run(main()) 