import asyncio
from pathlib import Path
import json
from typing import List
from loguru import logger

from scanners.mobsf_scanner import MobSFScanner
from scanners.semgrep_scanner import SemgrepScanner
from scanners.dependency_check_scanner import DependencyCheckScanner
from scanners.base_scanner import BaseScanner

async def run_security_analysis(apk_path: str, output_dir: str = None) -> dict:
    """
    Запускает полный анализ безопасности APK файла
    
    Args:
        apk_path: Путь к APK файлу
        output_dir: Директория для сохранения результатов
        
    Returns:
        dict: Объединенные результаты всех сканеров
    """
    apk_path = Path(apk_path)
    output_dir = Path(output_dir or apk_path.parent)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Инициализируем сканеры
    scanners: List[BaseScanner] = [
        MobSFScanner(api_key="your_mobsf_api_key"),
        SemgrepScanner(),
        DependencyCheckScanner()
    ]
    
    # Проверяем доступность сканеров
    available_scanners = []
    for scanner in scanners:
        if scanner.is_available():
            available_scanners.append(scanner)
        else:
            logger.warning(f"Сканер {scanner.name} недоступен. Требования:\n{scanner.get_requirements()}")
    
    if not available_scanners:
        raise Exception("Нет доступных сканеров!")
    
    # Запускаем сканирование
    results = {}
    for scanner in available_scanners:
        try:
            results[scanner.name] = await scanner.scan(apk_path)
        except Exception as e:
            logger.error(f"Ошибка при сканировании {scanner.name}: {e}")
            results[scanner.name] = {"error": str(e)}
    
    # Сохраняем результаты
    output_file = output_dir / f"{apk_path.stem}_security_report.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Анализ завершен. Результаты сохранены в {output_file}")
    return results

def main():
    """Точка входа в программу"""
    import argparse
    parser = argparse.ArgumentParser(description="Анализ безопасности APK файла")
    parser.add_argument("apk_path", help="Путь к APK файлу")
    parser.add_argument("--output", "-o", help="Директория для сохранения результатов")
    args = parser.parse_args()
    
    asyncio.run(run_security_analysis(args.apk_path, args.output))

if __name__ == "__main__":
    main() 