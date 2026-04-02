"""Planner agent implementation."""

from __future__ import annotations

from utils.formatting import load_prompt
from utils.llm import OllamaClient


class PlannerAgent:
    """Extracts requirements and creates an implementation plan."""

    def __init__(self, client: OllamaClient | None = None) -> None:
        self.client = client or OllamaClient()
        self.system_prompt = load_prompt("planner_prompt.txt")

    def run(self, assignment: str) -> str:
        user_prompt = (
            "Assignment:\n"
            f"{assignment.strip()}\n\n"
            "Return the plan using the required headings."
        )
        return self.client.ask_model(system_prompt=self.system_prompt, user_prompt=user_prompt)
