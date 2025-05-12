from pathlib import Path
from typing import List, Dict
from datetime import datetime
import asyncio
from loguru import logger

from .models import SecurityReport, SecurityScore, ScanResult
from ..scanners.base import BaseScanner

class SecurityAnalyzer:
    """Основной класс для анализа безопасности мобильных приложений"""
    
    def __init__(self, scanners: List[BaseScanner]):
        self.scanners = scanners
        self._validate_scanners()

    def _validate_scanners(self):
        """Проверяет доступность всех сканеров"""
        for scanner in self.scanners:
            if not asyncio.run(scanner.is_available()):
                logger.warning(f"Сканер {scanner.name} недоступен")

    async def _run_scans(self, apk_path: Path) -> List[ScanResult]:
        """Запускает все доступные сканеры параллельно"""
        tasks = []
        for scanner in self.scanners:
            if asyncio.run(scanner.is_available()):
                tasks.append(scanner.scan(apk_path))
        
        return await asyncio.gather(*tasks)

    def _calculate_security_score(self, scan_results: List[ScanResult]) -> SecurityScore:
        """Рассчитывает итоговую оценку безопасности"""
        # Веса для разных уровней уязвимостей
        weights = {
            "critical": 1.0,
            "high": 0.7,
            "medium": 0.4,
            "low": 0.1
        }
        
        # Подсчет уязвимостей по категориям
        vulnerabilities_count = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        # Подсчет уязвимостей по категориям безопасности
        category_scores = {
            "code_security": 0,
            "data_security": 0,
            "authentication": 0,
            "system_security": 0
        }
        
        for result in scan_results:
            for vuln in result.vulnerabilities:
                vulnerabilities_count[vuln.severity] += 1
                # Здесь должна быть логика распределения уязвимостей по категориям
                # и расчета баллов для каждой категории
        
        # Расчет общего балла
        total_score = 100
        for severity, count in vulnerabilities_count.items():
            total_score -= count * weights[severity] * 10
        
        return SecurityScore(
            overall_score=max(0, total_score),
            category_scores=category_scores,
            critical_vulnerabilities=vulnerabilities_count["critical"],
            high_vulnerabilities=vulnerabilities_count["high"],
            medium_vulnerabilities=vulnerabilities_count["medium"],
            low_vulnerabilities=vulnerabilities_count["low"]
        )

    async def analyze_apk(self, apk_path: Path) -> SecurityReport:
        """
        Анализирует APK-файл и генерирует отчёт о безопасности
        
        Args:
            apk_path: Путь к APK-файлу
            
        Returns:
            SecurityReport: Отчёт о безопасности
        """
        logger.info(f"Начинаем анализ {apk_path}")
        
        # Запуск сканирования
        scan_results = await self._run_scans(apk_path)
        
        # Расчет оценки безопасности
        security_score = self._calculate_security_score(scan_results)
        
        # Формирование отчёта
        report = SecurityReport(
            app_name="",  # TODO: Извлечь из APK
            package_name="",  # TODO: Извлечь из APK
            version="",  # TODO: Извлечь из APK
            scan_date=datetime.now(),
            scan_results=scan_results,
            security_score=security_score,
            summary="",  # TODO: Сгенерировать на основе результатов
            recommendations=[]  # TODO: Сгенерировать на основе результатов
        )
        
        logger.info("Анализ завершен")
        return report 