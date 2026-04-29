"""Deterministic workflow coordinator."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterator, Literal

from agents import BuilderAgent, PlannerAgent, ReviewerAgent
from utils.formatting import derive_next_steps, extract_section
from utils.llm import LLMClientError, OllamaClient


WorkflowStepName = Literal[
    "assignment",
    "planner",
    "builder",
    "reviewer",
    "next_steps",
]


@dataclass(frozen=True)
class WorkflowStep:
    """A single step emitted by the workflow as it progresses."""

    name: WorkflowStepName
    title: str
    content: str


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
        cleaned_assignment = self._validate_assignment(assignment)

        planner_output = self.planner.run(cleaned_assignment)
        builder_output = self.builder.run(cleaned_assignment, planner_output)
        review_output = self.reviewer.run(cleaned_assignment, planner_output, builder_output)

        return self._build_result(
            assignment=cleaned_assignment,
            planner_output=planner_output,
            builder_output=builder_output,
            review_output=review_output,
        )

    def run_incremental(self, assignment: str) -> Iterator[WorkflowStep]:
        """Yield workflow output step by step for progressive consumption."""
        cleaned_assignment = self._validate_assignment(assignment)
        yield WorkflowStep(name="assignment", title="Assignment", content=cleaned_assignment)

        planner_output = self.planner.run(cleaned_assignment)
        yield WorkflowStep(name="planner", title="Planner", content=planner_output)

        builder_output = self.builder.run(cleaned_assignment, planner_output)
        yield WorkflowStep(name="builder", title="Builder", content=builder_output)

        review_output = self.reviewer.run(cleaned_assignment, planner_output, builder_output)
        yield WorkflowStep(name="reviewer", title="Reviewer", content=review_output)

        next_steps = derive_next_steps(review_output)
        yield WorkflowStep(name="next_steps", title="Final Next Steps", content=next_steps)

    @staticmethod
    def _validate_assignment(assignment: str) -> str:
        cleaned_assignment = assignment.strip()
        if not cleaned_assignment:
            raise ValueError("Assignment input is empty. Paste an assignment before running the workflow.")
        return cleaned_assignment

    @staticmethod
    def _build_result(
        assignment: str,
        planner_output: str,
        builder_output: str,
        review_output: str,
    ) -> WorkflowResult:
        return WorkflowResult(
            assignment=assignment,
            requirements=extract_section(planner_output, "Requirements"),
            plan=extract_section(planner_output, "Implementation Steps"),
            starter_code=builder_output,
            review=review_output,
            next_steps=derive_next_steps(review_output),
        )


__all__ = ["WorkflowCoordinator", "WorkflowResult", "WorkflowStep", "LLMClientError"]
