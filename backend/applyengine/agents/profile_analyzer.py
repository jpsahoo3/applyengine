from __future__ import annotations

import re

from applyengine.agents.base import AgentResult
from applyengine.schemas.profile import ProfileSnapshot


KNOWN_SKILLS = {
    "python",
    "fastapi",
    "django",
    "flask",
    "sql",
    "postgresql",
    "redis",
    "docker",
    "kubernetes",
    "aws",
    "gcp",
    "langgraph",
    "langchain",
    "machine learning",
    "pytorch",
    "tensorflow",
    "react",
    "next.js",
    "typescript",
    "java",
    "golang",
    "ci/cd",
}

ROLE_KEYWORDS = {
    "backend": {"fastapi", "django", "flask", "api", "python", "sql"},
    "fullstack": {"react", "next.js", "typescript", "frontend", "backend"},
    "ai": {"langgraph", "langchain", "machine learning", "pytorch", "tensorflow"},
    "data": {"sql", "python", "analytics", "airflow"},
    "devops": {"docker", "kubernetes", "aws", "gcp", "ci/cd"},
}


class ProfileAnalyzerAgent:
    agent_name = "profile_analyzer"

    def analyze_resume(self, content: str) -> AgentResult:
        text = " ".join(content.lower().split())
        skills = sorted(skill for skill in KNOWN_SKILLS if skill in text)
        target_roles = [
            role
            for role, role_signals in ROLE_KEYWORDS.items()
            if role_signals.intersection(set(skills) | set(text.split()))
        ]
        years = self._extract_years_experience(text)
        headline = self._build_headline(target_roles, skills)
        summary = self._build_summary(skills, years, target_roles)
        profile = ProfileSnapshot(
            headline=headline,
            target_roles=target_roles or ["backend"],
            skills=skills,
            years_experience=years,
            resume_summary=summary,
        )
        return AgentResult(agent_name=self.agent_name, payload={"profile": profile})

    @staticmethod
    def _extract_years_experience(content: str) -> int:
        match = re.search(r"(\d+)\+?\s+years", content)
        if match:
            return int(match.group(1))
        return 0

    @staticmethod
    def _build_headline(target_roles: list[str], skills: list[str]) -> str:
        if target_roles and skills:
            return f"{target_roles[0].title()} engineer focused on {', '.join(skills[:3])}"
        if target_roles:
            return f"{target_roles[0].title()} engineer"
        return "Software engineer"

    @staticmethod
    def _build_summary(skills: list[str], years: int, target_roles: list[str]) -> str:
        role_text = ", ".join(target_roles) if target_roles else "software engineering"
        if skills:
            return f"{years} years aligned to {role_text}; core skills: {', '.join(skills[:6])}."
        return f"{years} years aligned to {role_text}."

