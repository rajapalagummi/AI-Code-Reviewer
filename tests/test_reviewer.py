"""
Unit tests for AI Code Reviewer.
Run: python -m pytest tests/ -v
"""

import pytest
from src.models import Issue, IssueCategory, ReviewResult, Severity
from src.reviewer import CodeReviewer


# ── Model tests ─────────────────────────────────────────────────

class TestSeverityRank:
    def test_critical_is_highest_priority(self):
        critical = Issue(IssueCategory.SECURITY, Severity.CRITICAL, "t", "d")
        info = Issue(IssueCategory.STYLE, Severity.INFO, "t", "d")
        assert critical.severity_rank < info.severity_rank

    def test_sorted_issues_order(self):
        result = ReviewResult(
            language="Python",
            source="ChatGPT",
            code="x=1",
            issues=[
                Issue(IssueCategory.STYLE, Severity.LOW, "t", "d"),
                Issue(IssueCategory.SECURITY, Severity.CRITICAL, "t", "d"),
                Issue(IssueCategory.LOGIC, Severity.MEDIUM, "t", "d"),
            ],
        )
        severities = [i.severity for i in result.sorted_issues]
        assert severities == [Severity.CRITICAL, Severity.MEDIUM, Severity.LOW]


class TestScoreLabel:
    @pytest.mark.parametrize("score,label", [
        (95, "Excellent"),
        (80, "Good"),
        (60, "Needs Work"),
        (40, "Poor"),
        (20, "Critical Issues"),
    ])
    def test_score_labels(self, score, label):
        r = ReviewResult(language="Python", source="Claude", code="x", overall_score=score)
        assert r.score_label == label


class TestIssueCounts:
    def test_counts_by_severity(self):
        result = ReviewResult(
            language="Python",
            source="Copilot",
            code="x",
            issues=[
                Issue(IssueCategory.SECURITY, Severity.CRITICAL, "a", "d"),
                Issue(IssueCategory.SECURITY, Severity.CRITICAL, "b", "d"),
                Issue(IssueCategory.LOGIC, Severity.HIGH, "c", "d"),
                Issue(IssueCategory.PERFORMANCE, Severity.LOW, "e", "d"),
            ],
        )
        assert result.critical_count == 2
        assert result.high_count == 1
        assert result.medium_count == 0
        assert result.low_count == 1


# ── Reviewer demo mode ──────────────────────────────────────────

class TestReviewerDemoMode:
    def test_demo_returns_result(self):
        reviewer = CodeReviewer()
        # Force demo mode
        reviewer.client = None
        result = reviewer.review(
            code="password = 'abc'\nfor i in items:\n    for j in items:\n        pass",
            language="Python",
            source="ChatGPT",
        )
        assert isinstance(result, ReviewResult)
        assert len(result.issues) > 0
        assert 0 <= result.overall_score <= 100
        assert result.model_used == "demo"

    def test_demo_has_security_issue(self):
        reviewer = CodeReviewer()
        reviewer.client = None
        result = reviewer._demo_result("x=1", "Python", "ChatGPT")
        cats = [i.category for i in result.issues]
        assert IssueCategory.SECURITY in cats
