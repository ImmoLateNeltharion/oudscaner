from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any

class BaseScanner(ABC):
    """Базовый класс для всех сканеров безопасности"""
    
    def __init__(self, name: str):
        self.name = name
        
    @abstractmethod
    async def scan(self, apk_path: Path) -> Dict[str, Any]:
        """
        Выполняет сканирование APK файла
        
        Args:
            apk_path: Путь к APK файлу
            
        Returns:
            Dict[str, Any]: Результаты сканирования
        """
        pass
        
    @abstractmethod
    def is_available(self) -> bool:
        """Проверяет, доступен ли сканер для использования"""
        pass
        
    @abstractmethod
    def get_requirements(self) -> str:
        """Возвращает требования для установки сканера"""
        pass 