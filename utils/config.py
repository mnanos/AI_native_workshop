"""Configuration loading for the workshop demo."""

from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - optional local convenience
    def load_dotenv() -> None:
        """Fallback when python-dotenv is not installed."""
        return None


@dataclass(frozen=True)
class AppConfig:
    """Runtime configuration for local model access."""

    model_provider: str = "ollama"
    model_name: str = "llama3"
    ollama_base_url: str = "http://localhost:11434"
    ollama_timeout: int = 90


def get_config() -> AppConfig:
    """Load environment variables and return normalized config."""
    load_dotenv()
    timeout_raw = os.getenv("OLLAMA_TIMEOUT", "90")

    try:
        timeout = int(timeout_raw)
    except ValueError:
        timeout = 90

    return AppConfig(
        model_provider=os.getenv("MODEL_PROVIDER", "ollama"),
        model_name=os.getenv("MODEL_NAME", "llama3"),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        ollama_timeout=timeout,
    )
