import os
import json
import requests
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

from .base import BaseScanner
from ..core.models import ScanResult, Vulnerability, Severity

class MobSFScanner(BaseScanner):
    """Сканер безопасности на основе MobSF"""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.server_url = config.get("server_url", "http://localhost:8000")
        self.upload_url = f"{self.server_url}/api/v1/upload"
        self.scan_url = f"{self.server_url}/api/v1/scan"
        self.report_url = f"{self.server_url}/api/v1/report_json"

    async def is_available(self) -> bool:
        """Проверяет доступность MobSF сервера"""
        try:
            response = requests.get(f"{self.server_url}/api/v1/health")
            return response.status_code == 200
        except:
            return False

    async def get_version(self) -> str:
        """Получает версию MobSF"""
        try:
            response = requests.get(f"{self.server_url}/api/v1/version")
            return response.json().get("version", "unknown")
        except:
            return "unknown"

    def _map_severity(self, mobsf_severity: str) -> Severity:
        """Преобразует уровни уязвимостей MobSF в наши"""
        severity_map = {
            "high": Severity.HIGH,
            "warning": Severity.MEDIUM,
            "info": Severity.LOW,
            "error": Severity.CRITICAL
        }
        return severity_map.get(mobsf_severity.lower(), Severity.INFO)

    def _parse_vulnerabilities(self, report: Dict) -> list[Vulnerability]:
        """Парсит уязвимости из отчёта MobSF"""
        vulnerabilities = []
        
        # Обработка статических уязвимостей
        for category, issues in report.get("static_analysis", {}).items():
            for issue in issues:
                vuln = Vulnerability(
                    id=f"mobsf_{category}_{len(vulnerabilities)}",
                    title=issue.get("title", "Unknown"),
                    description=issue.get("description", ""),
                    severity=self._map_severity(issue.get("severity", "info")),
                    category=category,
                    location=issue.get("file", ""),
                    recommendation=issue.get("recommendation", ""),
                    scanner="MobSF",
                    cwe_id=issue.get("cwe", None)
                )
                vulnerabilities.append(vuln)
        
        return vulnerabilities

    async def scan(self, apk_path: Path) -> ScanResult:
        """
        Выполняет сканирование APK-файла с помощью MobSF
        
        Args:
            apk_path: Путь к APK-файлу
            
        Returns:
            ScanResult: Результаты сканирования
        """
        # Загрузка файла
        with open(apk_path, "rb") as f:
            files = {"file": f}
            response = requests.post(
                self.upload_url,
                files=files,
                headers={"Authorization": self.api_key}
            )
        
        if response.status_code != 200:
            raise Exception(f"Ошибка загрузки файла: {response.text}")
        
        file_hash = response.json().get("hash")
        
        # Запуск сканирования
        scan_data = {
            "scan_type": "apk",
            "file_name": apk_path.name,
            "hash": file_hash
        }
        
        response = requests.post(
            self.scan_url,
            json=scan_data,
            headers={"Authorization": self.api_key}
        )
        
        if response.status_code != 200:
            raise Exception(f"Ошибка запуска сканирования: {response.text}")
        
        # Получение результатов
        response = requests.get(
            f"{self.report_url}/{file_hash}",
            headers={"Authorization": self.api_key}
        )
        
        if response.status_code != 200:
            raise Exception(f"Ошибка получения отчёта: {response.text}")
        
        report = response.json()
        vulnerabilities = self._parse_vulnerabilities(report)
        
        return ScanResult(
            scanner_name="MobSF",
            scan_time=datetime.now(),
            vulnerabilities=vulnerabilities,
            metadata={
                "file_hash": file_hash,
                "mobsf_version": await self.get_version()
            }
        ) 