"""Helpers for prompt loading and output formatting."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_prompt(filename: str) -> str:
    """Load a prompt file from the prompts directory."""
    prompt_path = PROJECT_ROOT / "prompts" / filename
    return prompt_path.read_text(encoding="utf-8").strip()


def derive_next_steps(review_text: str) -> str:
    """Turn review output into a compact next-steps section."""
    lines = [line.strip("- ").strip() for line in review_text.splitlines() if line.strip()]
    suggestion_lines = []
    capture = False

    for line in lines:
        lowered = line.lower()
        if lowered.startswith("improvement suggestions"):
            capture = True
            continue
        if capture and lowered.endswith(":"):
            break
        if capture:
            suggestion_lines.append(line)

    if not suggestion_lines:
        suggestion_lines = [
            "Run the generated code with sample input.",
            "Address any missing requirements highlighted in the review.",
            "Refine the starter code into a tested solution.",
        ]

    return "\n".join(f"- {line}" for line in suggestion_lines[:5])


def extract_section(text: str, heading: str) -> str:
    """Extract one heading section from markdown-like agent output."""
    target = heading.lower().rstrip(":")
    lines = text.splitlines()
    collected = []
    capture = False

    for raw_line in lines:
        stripped = raw_line.strip()
        normalized = stripped.lstrip("#").strip().lower().rstrip(":")

        if normalized == target:
            capture = True
            continue

        if capture and normalized in {
            "requirements",
            "proposed project structure",
            "assumptions",
            "implementation steps",
            "edge cases",
            "coverage check",
            "missing parts",
            "risks / edge cases",
            "improvement suggestions",
        }:
            break

        if capture:
            collected.append(raw_line)

    section = "\n".join(collected).strip()
    return section or text.strip()


def format_terminal_section(title: str, body: str) -> str:
    """Format one CLI output section."""
    return f"{title}\n{'=' * len(title)}\n{body.strip()}\n"
