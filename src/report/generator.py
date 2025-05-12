from pathlib import Path
from typing import List
from datetime import datetime
import jinja2
from weasyprint import HTML
from loguru import logger

from ..core.models import SecurityReport

class ReportGenerator:
    """Генератор отчётов о безопасности"""
    
    def __init__(self, template_dir: Path):
        self.template_dir = template_dir
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(template_dir)),
            autoescape=True
        )

    def _generate_summary(self, report: SecurityReport) -> str:
        """Генерирует краткое описание результатов анализа"""
        score = report.security_score
        return f"""
        Общая оценка безопасности: {score.overall_score:.1f}/100
        
        Критические уязвимости: {score.critical_vulnerabilities}
        Высокий уровень риска: {score.high_vulnerabilities}
        Средний уровень риска: {score.medium_vulnerabilities}
        Низкий уровень риска: {score.low_vulnerabilities}
        
        Категории безопасности:
        - Безопасность кода: {score.category_scores['code_security']:.1f}
        - Защита данных: {score.category_scores['data_security']:.1f}
        - Аутентификация: {score.category_scores['authentication']:.1f}
        - Системная безопасность: {score.category_scores['system_security']:.1f}
        """

    def _generate_recommendations(self, report: SecurityReport) -> List[str]:
        """Генерирует список рекомендаций на основе результатов анализа"""
        recommendations = []
        
        # Анализ критических уязвимостей
        critical_vulns = [
            v for result in report.scan_results
            for v in result.vulnerabilities
            if v.severity == "critical"
        ]
        
        if critical_vulns:
            recommendations.append(
                "Необходимо немедленно устранить критические уязвимости:"
            )
            for vuln in critical_vulns:
                recommendations.append(f"- {vuln.title}: {vuln.recommendation}")
        
        # Анализ по категориям
        for category, score in report.security_score.category_scores.items():
            if score < 70:
                recommendations.append(
                    f"Требуется улучшение в категории {category}: "
                    f"текущий балл {score:.1f}/100"
                )
        
        return recommendations

    def generate_html(self, report: SecurityReport) -> str:
        """Генерирует HTML-версию отчёта"""
        template = self.env.get_template("report.html")
        
        # Обновляем summary и recommendations
        report.summary = self._generate_summary(report)
        report.recommendations = self._generate_recommendations(report)
        
        return template.render(
            report=report,
            generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    def generate_pdf(self, report: SecurityReport, output_path: Path) -> None:
        """Генерирует PDF-версию отчёта"""
        html_content = self.generate_html(report)
        HTML(string=html_content).write_pdf(output_path)
        logger.info(f"Отчёт сохранен в {output_path}")

    def generate_json(self, report: SecurityReport, output_path: Path) -> None:
        """Генерирует JSON-версию отчёта"""
        import json
        
        # Обновляем summary и recommendations
        report.summary = self._generate_summary(report)
        report.recommendations = self._generate_recommendations(report)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(report.dict(), f, ensure_ascii=False, indent=2)
        
        logger.info(f"JSON-отчёт сохранен в {output_path}") 