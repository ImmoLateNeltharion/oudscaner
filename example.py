import asyncio
from pathlib import Path
from src.core.analyzer import SecurityAnalyzer
from src.scanners.mobsf import MobSFScanner
from src.report.generator import ReportGenerator

async def main():
    # Конфигурация сканеров
    mobsf_config = {
        "api_key": "your_api_key_here",
        "server_url": "http://localhost:8000"
    }
    
    # Инициализация сканеров
    scanners = [
        MobSFScanner(mobsf_config)
        # Здесь можно добавить другие сканеры
    ]
    
    # Создание анализатора
    analyzer = SecurityAnalyzer(scanners)
    
    # Путь к APK-файлу
    apk_path = Path("path/to/your/app.apk")
    
    # Анализ приложения
    report = await analyzer.analyze_apk(apk_path)
    
    # Генерация отчётов
    report_generator = ReportGenerator(Path("src/report/templates"))
    
    # Сохранение в разных форматах
    report_generator.generate_pdf(report, Path("report.pdf"))
    report_generator.generate_json(report, Path("report.json"))

if __name__ == "__main__":
    asyncio.run(main()) 