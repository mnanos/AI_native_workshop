"""Deterministic workflow coordinator."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from agents import BuilderAgent, PlannerAgent, ReviewerAgent
from utils.formatting import derive_next_steps, extract_section
from utils.llm import LLMClientError, OllamaClient


@dataclass
class WorkflowResult:
    """Structured result returned by the workflow."""

    assignment: str
    requirements: str
    plan: str
    starter_code: str
    review: str
    next_steps: str

    def to_dict(self) -> dict[str, str]:
        """Convert the result into a plain dictionary."""
        return asdict(self)


class WorkflowCoordinator:
    """Coordinates Planner, Builder, and Reviewer in a fixed sequence."""

    def __init__(self, client: OllamaClient | None = None) -> None:
        shared_client = client or OllamaClient()
        self.planner = PlannerAgent(shared_client)
        self.builder = BuilderAgent(shared_client)
        self.reviewer = ReviewerAgent(shared_client)

    def run(self, assignment: str) -> WorkflowResult:
        cleaned_assignment = assignment.strip()
        if not cleaned_assignment:
            raise ValueError("Assignment input is empty. Paste an assignment before running the workflow.")

        planner_output = self.planner.run(cleaned_assignment)
        builder_output = self.builder.run(cleaned_assignment, planner_output)
        review_output = self.reviewer.run(cleaned_assignment, planner_output, builder_output)

        return WorkflowResult(
            assignment=cleaned_assignment,
            requirements=extract_section(planner_output, "Requirements"),
            plan=extract_section(planner_output, "Implementation Steps"),
            starter_code=builder_output,
            review=review_output,
            next_steps=derive_next_steps(review_output),
        )


__all__ = ["WorkflowCoordinator", "WorkflowResult", "LLMClientError"]
