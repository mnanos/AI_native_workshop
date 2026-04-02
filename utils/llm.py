"""Small Ollama client used by all agents."""

from __future__ import annotations

from typing import Any

import requests

from utils.config import AppConfig, get_config


class LLMClientError(RuntimeError):
    """Raised when local model access fails."""


class OllamaClient:
    """Minimal wrapper around the Ollama generate API."""

    def __init__(self, config: AppConfig | None = None) -> None:
        self.config = config or get_config()

    def ask_model(self, system_prompt: str, user_prompt: str) -> str:
        """Send a prompt to the configured local model and return the text response."""
        if self.config.model_provider.lower() != "ollama":
            raise LLMClientError(
                f"Unsupported MODEL_PROVIDER '{self.config.model_provider}'. "
                "This project expects 'ollama'."
            )

        prompt = self._build_prompt(system_prompt=system_prompt, user_prompt=user_prompt)
        payload = {
            "model": self.config.model_name,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = requests.post(
                f"{self.config.ollama_base_url}/api/generate",
                json=payload,
                timeout=self.config.ollama_timeout,
            )
        except requests.exceptions.ConnectionError as exc:
            raise LLMClientError(
                "Could not connect to Ollama. Start Ollama and verify "
                f"the base URL is reachable at {self.config.ollama_base_url}."
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise LLMClientError(
                "The request to Ollama timed out. Try a smaller prompt, a lighter model, "
                "or increase OLLAMA_TIMEOUT."
            ) from exc
        except requests.RequestException as exc:
            raise LLMClientError(f"Unexpected request error while calling Ollama: {exc}") from exc

        if response.status_code == 404:
            raise LLMClientError(
                f"The model '{self.config.model_name}' was not found. "
                f"Run `ollama pull {self.config.model_name}` and try again."
            )

        if not response.ok:
            raise LLMClientError(self._format_error_response(response))

        data = self._parse_json(response)
        text = str(data.get("response", "")).strip()
        if not text:
            raise LLMClientError("Ollama returned an empty response.")
        return text

    @staticmethod
    def _build_prompt(system_prompt: str, user_prompt: str) -> str:
        return (
            "System Instructions:\n"
            f"{system_prompt.strip()}\n\n"
            "User Request:\n"
            f"{user_prompt.strip()}"
        )

    @staticmethod
    def _parse_json(response: requests.Response) -> dict[str, Any]:
        try:
            return response.json()
        except ValueError as exc:
            raise LLMClientError("Ollama returned invalid JSON.") from exc

    @staticmethod
    def _format_error_response(response: requests.Response) -> str:
        try:
            data = response.json()
        except ValueError:
            data = {}

        error_text = data.get("error") if isinstance(data, dict) else None
        if error_text:
            return f"Ollama returned an error: {error_text}"
        return f"Ollama returned HTTP {response.status_code}."
