"""Builder agent implementation."""

from __future__ import annotations

from utils.formatting import load_prompt
from utils.llm import OllamaClient


class BuilderAgent:
    """Generates starter code from the assignment and plan."""

    def __init__(self, client: OllamaClient | None = None) -> None:
        self.client = client or OllamaClient()
        self.system_prompt = load_prompt("builder_prompt.txt")

    def run(self, assignment: str, planner_output: str) -> str:
        user_prompt = (
            "Assignment:\n"
            f"{assignment.strip()}\n\n"
            "Planner Output:\n"
            f"{planner_output.strip()}\n\n"
            "Generate starter code now. Use the file names from the proposed project "
            "structure and label each code block with its relative file path."
        )
        return self.client.ask_model(system_prompt=self.system_prompt, user_prompt=user_prompt)
