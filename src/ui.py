"""
Streamlit UI rendering helpers.
"""

import streamlit as st
from src.models import IssueCategory, ReviewResult, Severity


SEVERITY_COLORS = {
    Severity.CRITICAL: "#ef4444",
    Severity.HIGH: "#f97316",
    Severity.MEDIUM: "#facc15",
    Severity.LOW: "#94a3b8",
    Severity.INFO: "#64748b",
}

SEVERITY_BG = {
    Severity.CRITICAL: "#1c1010",
    Severity.HIGH: "#1c1208",
    Severity.MEDIUM: "#1c1a08",
    Severity.LOW: "#12151e",
    Severity.INFO: "#12151e",
}


def render_header():
    st.markdown(
        """
        <div class="header-wrap">
            <span class="header-icon">🔍</span>
            <div>
                <h1 class="header-title">AI Code Reviewer</h1>
                <p class="header-sub">Syntax · Logic · Security · Performance — ranked by severity</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        st.markdown("## ⚙️ About")
        st.markdown(
            "This tool reviews AI-generated code (ChatGPT, Claude, Copilot, Gemini…) "
            "and surfaces real issues ranked by severity."
        )
        st.markdown("---")
        st.markdown("### Severity Legend")
        rows = [
            ("🔴", "Critical", "Crashes, data loss, severe security"),
            ("🟠", "High", "Likely bugs, significant security risk"),
            ("🟡", "Medium", "Logic flaws, moderate security"),
            ("🔵", "Low", "Performance, best practices"),
            ("⚪", "Info", "Observations only"),
        ]
        for icon, label, desc in rows:
            st.markdown(f"{icon} **{label}** — {desc}")
        st.markdown("---")
        st.markdown("Built with [Streamlit](https://streamlit.io) · Powered by Claude")


def render_score_badge(score: int, label: str, color: str):
    st.markdown(
        f"""
        <div class="score-badge" style="border-color:{color}">
            <span class="score-number" style="color:{color}">{score}</span>
            <span class="score-label" style="color:{color}">{label}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_results(result: ReviewResult):
    # Score + summary row
    col_score, col_summary = st.columns([1, 3])

    with col_score:
        render_score_badge(result.overall_score, result.score_label, result.score_color)

    with col_summary:
        st.markdown("**Summary**")
        st.markdown(result.summary)
        if result.model_used and result.model_used != "demo":
            st.caption(f"Reviewed by `{result.model_used}`")

    # Issue count chips
    chips_html = _build_chips(result)
    st.markdown(chips_html, unsafe_allow_html=True)

    st.markdown("---")

    if not result.issues:
        st.success("✅ No issues found. Code looks clean!")
        return

    # Category filter
    all_cats = sorted({i.category.value for i in result.issues})
    selected_cats = st.multiselect(
        "Filter by category",
        options=all_cats,
        default=all_cats,
    )

    filtered = [i for i in result.sorted_issues if i.category.value in selected_cats]

    for issue in filtered:
        color = SEVERITY_COLORS[issue.severity]
        bg = SEVERITY_BG[issue.severity]

        with st.expander(
            f"{issue.severity_emoji} {issue.category_emoji} **{issue.title}**"
            + (f" — line {issue.line_number}" if issue.line_number else ""),
            expanded=issue.severity in (Severity.CRITICAL, Severity.HIGH),
        ):
            st.markdown(
                f'<div class="issue-card" style="border-left: 4px solid {color}; background:{bg}; padding:12px; border-radius:6px">',
                unsafe_allow_html=True,
            )
            badge = (
                f'<span class="severity-badge" style="background:{color};color:#fff;'
                f'padding:2px 10px;border-radius:20px;font-size:0.75rem;font-weight:600">'
                f'{issue.severity.value.upper()}</span>'
                f'&nbsp;&nbsp;'
                f'<span style="color:#6b7280;font-size:0.85rem">{issue.category.value}</span>'
            )
            st.markdown(badge, unsafe_allow_html=True)
            st.markdown(f"\n{issue.description}")

            if issue.code_snippet:
                st.code(issue.code_snippet, language="python")

            if issue.suggestion:
                st.markdown(f"**💡 Suggestion:** {issue.suggestion}")

            st.markdown("</div>", unsafe_allow_html=True)


def _build_chips(result: ReviewResult) -> str:
    counts = [
        (result.critical_count, "#ef4444", "Critical"),
        (result.high_count, "#f97316", "High"),
        (result.medium_count, "#eab308", "Medium"),
        (result.low_count, "#3b82f6", "Low"),
    ]
    chips = ""
    for count, color, label in counts:
        if count:
            chips += (
                f'<span style="background:{color};color:#fff;padding:3px 12px;'
                f'border-radius:20px;font-size:0.8rem;font-weight:600;margin-right:6px">'
                f'{count} {label}</span>'
            )
    return f'<div style="margin:8px 0">{chips}</div>' if chips else ""
