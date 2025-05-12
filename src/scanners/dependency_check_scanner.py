import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Dict, Any
from loguru import logger
from .base_scanner import BaseScanner

class DependencyCheckScanner(BaseScanner):
    """Сканер на основе OWASP Dependency-Check"""
    
    def __init__(self, dependency_check_path: str = "dependency-check.sh"):
        super().__init__("OWASP Dependency-Check")
        self.dependency_check_path = dependency_check_path
        
    async def scan(self, apk_path: Path) -> Dict[str, Any]:
        """Выполняет сканирование через Dependency-Check"""
        logger.info(f"Начинаю сканирование {apk_path} через Dependency-Check")
        
        # Создаем временную директорию для отчета
        report_path = apk_path.parent / "dependency-check-report.xml"
        
        try:
            # Запускаем сканирование
            cmd = [
                self.dependency_check_path,
                "--scan", str(apk_path),
                "--format", "XML",
                "--out", str(report_path),
                "--enableExperimental"
            ]
            
            subprocess.run(cmd, check=True)
            
            # Парсим XML отчет
            tree = ET.parse(report_path)
            root = tree.getroot()
            
            # Преобразуем XML в словарь
            dependencies = []
            for dependency in root.findall(".//dependency"):
                vulns = []
                for vuln in dependency.findall(".//vulnerability"):
                    vulns.append({
                        'name': vuln.find('name').text,
                        'severity': vuln.find('severity').text,
                        'description': vuln.find('description').text,
                        'cwe': vuln.find('cwe').text if vuln.find('cwe') is not None else None,
                        'cvss': vuln.find('.//score').text if vuln.find('.//score') is not None else None,
                    })
                    
                dependencies.append({
                    'fileName': dependency.find('fileName').text,
                    'vulnerabilities': vulns
                })
                
            results = {
                'dependencies': dependencies,
                'total_dependencies': len(dependencies),
                'vulnerable_dependencies': len([d for d in dependencies if d['vulnerabilities']])
            }
            
            logger.info("Сканирование Dependency-Check завершено")
            return results
            
        finally:
            # Удаляем отчет
            report_path.unlink(missing_ok=True)
            
    def is_available(self) -> bool:
        """Проверяет доступность Dependency-Check"""
        try:
            subprocess.run([self.dependency_check_path, "--version"], capture_output=True)
            return True
        except:
            return False
            
    def get_requirements(self) -> str:
        return """
        1. Установленный OWASP Dependency-Check
        2. Java 8 или выше
        3. Python пакеты: subprocess, xml
        """ 