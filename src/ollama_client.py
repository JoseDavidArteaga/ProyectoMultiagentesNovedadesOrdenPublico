"""Cliente HTTP mínimo para conversar con Ollama."""

from __future__ import annotations

import json
from typing import Any

import requests

from config import OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL, OLLAMA_TEMPERATURE


class OllamaClient:
    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model: str = OLLAMA_CHAT_MODEL,
        temperature: float = OLLAMA_TEMPERATURE,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.temperature = temperature

    def ping(self) -> None:
        response = requests.get(f"{self.base_url}/api/tags", timeout=10)
        response.raise_for_status()

    def chat(self, messages: list[dict[str, str]], format: str | None = None) -> str:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": self.temperature},
        }
        if format:
            payload["format"] = format

        response = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"].strip()

    def chat_json(self, messages: list[dict[str, str]]) -> dict[str, Any]:
        raw = self.chat(messages, format="json")
        return self._parse_json(raw)

    @staticmethod
    def _parse_json(raw: str) -> dict[str, Any]:
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Ollama no devolvió JSON válido: {raw[:200]}") from exc