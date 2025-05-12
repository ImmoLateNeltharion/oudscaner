from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path
from ..core.models import ScanResult

class BaseScanner(ABC):
    """Базовый класс для всех сканеров безопасности"""
    
    def __init__(self, config: dict):
        self.config = config
        self.name = self.__class__.__name__

    @abstractmethod
    async def scan(self, apk_path: Path) -> ScanResult:
        """
        Выполняет сканирование APK-файла
        
        Args:
            apk_path: Путь к APK-файлу
            
        Returns:
            ScanResult: Результаты сканирования
        """
        pass

    @abstractmethod
    async def is_available(self) -> bool:
        """
        Проверяет доступность сканера
        
        Returns:
            bool: True если сканер доступен, False в противном случае
        """
        pass

    @abstractmethod
    async def get_version(self) -> str:
        """
        Возвращает версию сканера
        
        Returns:
            str: Версия сканера
        """
        pass 