"""CLI entry point for the AI-native workshop demo."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from utils.formatting import extract_section, format_terminal_section
from utils.llm import LLMClientError
from workflow import WorkflowCoordinator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the AI-native workshop workflow.")
    parser.add_argument(
        "--input",
        type=Path,
        help="Optional path to a text file containing the assignment.",
    )
    return parser.parse_args()


def load_assignment(input_path: Path | None) -> str:
    if input_path:
        return input_path.read_text(encoding="utf-8")

    print("Paste the assignment and press Ctrl-D when finished:\n")
    return sys.stdin.read()


def main() -> int:
    args = parse_args()

    try:
        assignment = load_assignment(args.input)
        coordinator = WorkflowCoordinator()
        for step in coordinator.run_incremental(assignment):
            if step.name == "assignment":
                print(format_terminal_section("Assignment", step.content))
            elif step.name == "planner":
                requirements = extract_section(step.content, "Requirements")
                project_structure = extract_section(step.content, "Proposed Project Structure")
                plan = extract_section(step.content, "Implementation Steps")

                if requirements:
                    print(format_terminal_section("Requirements", requirements))
                if project_structure:
                    print(format_terminal_section("Proposed Project Structure", project_structure))
                if plan:
                    print(format_terminal_section("Plan", plan))
                if not any((requirements, project_structure, plan)):
                    print(format_terminal_section("Planner Output", step.content))
            elif step.name == "builder":
                print(format_terminal_section("Starter Code", step.content))
            elif step.name == "reviewer":
                print(format_terminal_section("Review", step.content))
            elif step.name == "next_steps":
                print(format_terminal_section("Final Next Steps", step.content))
    except FileNotFoundError as exc:
        print(f"Input file not found: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except LLMClientError as exc:
        print(f"Model error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
