"""Deterministic workflow coordinator."""

from __future__ import annotations

from typing import Iterator

from agents import DeepAgent, WorkflowResult, WorkflowStep
from utils.llm import LLMClientError, OllamaClient


class WorkflowCoordinator:
    """Coordinates Planner, Builder, and Reviewer in a fixed sequence."""

    def __init__(self, client: OllamaClient | None = None) -> None:
        self.agent = DeepAgent(client or OllamaClient())

    def run(self, assignment: str) -> WorkflowResult:
        return self.agent.run(assignment)

    def run_incremental(self, assignment: str) -> Iterator[WorkflowStep]:
        return self.agent.run_incremental(assignment)


__all__ = ["WorkflowCoordinator", "WorkflowResult", "WorkflowStep", "LLMClientError"]
