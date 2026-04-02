"""Reviewer agent implementation."""

from __future__ import annotations

from utils.formatting import load_prompt
from utils.llm import OllamaClient


class ReviewerAgent:
    """Reviews generated code against the assignment and plan."""

    def __init__(self, client: OllamaClient | None = None) -> None:
        self.client = client or OllamaClient()
        self.system_prompt = load_prompt("reviewer_prompt.txt")

    def run(self, assignment: str, planner_output: str, starter_code: str) -> str:
        user_prompt = (
            "Assignment:\n"
            f"{assignment.strip()}\n\n"
            "Planner Output:\n"
            f"{planner_output.strip()}\n\n"
            "Generated Code:\n"
            f"{starter_code.strip()}\n\n"
            "Review the code using the required headings."
        )
        return self.client.ask_model(system_prompt=self.system_prompt, user_prompt=user_prompt)
