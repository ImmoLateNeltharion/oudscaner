import subprocess
from pathlib import Path
from typing import Dict, Any
import json
from loguru import logger
from .base_scanner import BaseScanner

class SemgrepScanner(BaseScanner):
    """Сканер на основе Semgrep"""
    
    def __init__(self, config_path: str = None):
        super().__init__("Semgrep")
        self.config_path = config_path or "p/android"
        
    async def scan(self, apk_path: Path) -> Dict[str, Any]:
        """Выполняет сканирование через Semgrep"""
        logger.info(f"Начинаю сканирование {apk_path} через Semgrep")
        
        # Распаковываем APK во временную директорию
        tmp_dir = apk_path.parent / "tmp_semgrep"
        subprocess.run(["apktool", "d", str(apk_path), "-o", str(tmp_dir), "-f"])
        
        try:
            # Запускаем Semgrep
            cmd = [
                "semgrep",
                "--config", self.config_path,
                "--json",
                str(tmp_dir)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            findings = json.loads(result.stdout)
            
            logger.info("Сканирование Semgrep завершено")
            return findings
            
        finally:
            # Очищаем временную директорию
            import shutil
            shutil.rmtree(tmp_dir, ignore_errors=True)
            
    def is_available(self) -> bool:
        """Проверяет доступность Semgrep"""
        try:
            subprocess.run(["semgrep", "--version"], capture_output=True)
            return True
        except:
            return False
            
    def get_requirements(self) -> str:
        return """
        1. Установленный Semgrep (pip install semgrep)
        2. Установленный apktool
        3. Python пакеты: subprocess, json
        """ 