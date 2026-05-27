"""
Data models for the AI Code Reviewer.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class IssueCategory(str, Enum):
    SYNTAX = "Syntax Error"
    LOGIC = "Logic Error"
    SECURITY = "Security Vulnerability"
    PERFORMANCE = "Performance Issue"
    STYLE = "Style / Best Practice"


@dataclass
class Issue:
    category: IssueCategory
    severity: Severity
    title: str
    description: str
    line_number: Optional[int] = None
    code_snippet: Optional[str] = None
    suggestion: Optional[str] = None

    @property
    def severity_rank(self) -> int:
        order = {
            Severity.CRITICAL: 0,
            Severity.HIGH: 1,
            Severity.MEDIUM: 2,
            Severity.LOW: 3,
            Severity.INFO: 4,
        }
        return order[self.severity]

    @property
    def severity_emoji(self) -> str:
        emojis = {
            Severity.CRITICAL: "🔴",
            Severity.HIGH: "🟠",
            Severity.MEDIUM: "🟡",
            Severity.LOW: "🔵",
            Severity.INFO: "⚪",
        }
        return emojis[self.severity]

    @property
    def category_emoji(self) -> str:
        emojis = {
            IssueCategory.SYNTAX: "🐛",
            IssueCategory.LOGIC: "🧠",
            IssueCategory.SECURITY: "🔒",
            IssueCategory.PERFORMANCE: "⚡",
            IssueCategory.STYLE: "✨",
        }
        return emojis[self.category]


@dataclass
class ReviewResult:
    language: str
    source: str
    code: str
    issues: List[Issue] = field(default_factory=list)
    overall_score: int = 100          # 0–100, higher = better
    summary: str = ""
    model_used: str = ""

    @property
    def sorted_issues(self) -> List[Issue]:
        return sorted(self.issues, key=lambda i: i.severity_rank)

    @property
    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.CRITICAL)

    @property
    def high_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.HIGH)

    @property
    def medium_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.MEDIUM)

    @property
    def low_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == Severity.LOW)

    @property
    def score_label(self) -> str:
        if self.overall_score >= 90:
            return "Excellent"
        elif self.overall_score >= 75:
            return "Good"
        elif self.overall_score >= 55:
            return "Needs Work"
        elif self.overall_score >= 35:
            return "Poor"
        else:
            return "Critical Issues"

    @property
    def score_color(self) -> str:
        if self.overall_score >= 90:
            return "#22c55e"
        elif self.overall_score >= 75:
            return "#84cc16"
        elif self.overall_score >= 55:
            return "#eab308"
        elif self.overall_score >= 35:
            return "#f97316"
        else:
            return "#ef4444"
