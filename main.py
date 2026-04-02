"""CLI entry point for the AI-native workshop demo."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from utils.formatting import format_terminal_section
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
        result = WorkflowCoordinator().run(assignment)
    except FileNotFoundError as exc:
        print(f"Input file not found: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except LLMClientError as exc:
        print(f"Model error: {exc}", file=sys.stderr)
        return 1

    sections = [
        ("Assignment", result.assignment),
        ("Requirements", result.requirements),
        ("Plan", result.plan),
        ("Starter Code", result.starter_code),
        ("Review", result.review),
        ("Final Next Steps", result.next_steps),
    ]

    for title, body in sections:
        print(format_terminal_section(title, body))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
