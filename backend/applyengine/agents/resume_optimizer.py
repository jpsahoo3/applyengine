from __future__ import annotations

from applyengine.agents.base import AgentResult
from applyengine.schemas.profile import ProfileSnapshot


class ResumeOptimizerAgent:
    agent_name = "resume_optimizer"

    def optimize(self, profile: ProfileSnapshot) -> AgentResult:
        optimized_variants: dict[str, dict[str, object]] = {}
        role_templates = {
            "backend": ["python", "fastapi", "postgresql", "redis"],
            "fullstack": ["react", "next.js", "typescript", "python"],
            "ai": ["langgraph", "langchain", "python", "machine learning"],
            "data": ["python", "sql", "analytics", "etl"],
            "devops": ["docker", "kubernetes", "aws", "ci/cd"],
        }
        for role, preferred_keywords in role_templates.items():
            optimized_variants[role] = {
                "headline": f"{role.title()} resume | {profile.headline}",
                "keywords": sorted(set(profile.skills).union(preferred_keywords)),
                "summary": profile.resume_summary,
            }
        return AgentResult(agent_name=self.agent_name, payload={"variants": optimized_variants})

