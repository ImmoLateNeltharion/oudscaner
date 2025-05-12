from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime

class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class Vulnerability(BaseModel):
    id: str
    title: str
    description: str
    severity: Severity
    category: str
    location: Optional[str] = None
    recommendation: str
    scanner: str
    cwe_id: Optional[str] = None
    cvss_score: Optional[float] = None

class ScanResult(BaseModel):
    scanner_name: str
    scan_time: datetime
    vulnerabilities: List[Vulnerability]
    metadata: Dict = Field(default_factory=dict)

class SecurityScore(BaseModel):
    overall_score: float
    category_scores: Dict[str, float]
    critical_vulnerabilities: int
    high_vulnerabilities: int
    medium_vulnerabilities: int
    low_vulnerabilities: int

class SecurityReport(BaseModel):
    app_name: str
    package_name: str
    version: str
    scan_date: datetime
    scan_results: List[ScanResult]
    security_score: SecurityScore
    summary: str
    recommendations: List[str]

    def save(self, format: str = "pdf") -> None:
        """Сохраняет отчёт в указанном формате"""
        pass 