"""Cliente HTTP mínimo para conversar con Ollama."""

from __future__ import annotations

import json
from typing import Any

import requests

from config import (
    GROQ_API_KEY,
    GROQ_BASE_URL,
    LLM_PROVIDER,
    OLLAMA_BASE_URL,
    OLLAMA_CHAT_MODEL,
    OLLAMA_TEMPERATURE, 
    OLLAMA_TIMEOUT_SECONDS,
)


class OllamaClient:
    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model: str = OLLAMA_CHAT_MODEL,
        temperature: float = OLLAMA_TEMPERATURE,
        timeout_seconds: int = OLLAMA_TIMEOUT_SECONDS,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model  # modelo por defecto; cada llamada puede usar otro con `model=`
        self.temperature = temperature
        self.timeout_seconds = timeout_seconds

    def ping(self) -> None:
        if LLM_PROVIDER == "groq":
            if not GROQ_API_KEY:
                raise ValueError("Falta GROQ_API_KEY en .env.")
            response = requests.get(
                f"{GROQ_BASE_URL.rstrip('/')}/models",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                timeout=(10, self.timeout_seconds),
            )
            response.raise_for_status()
            return

        response = requests.get(f"{self.base_url}/api/tags", timeout=(10, self.timeout_seconds))
        response.raise_for_status()

    def chat(
        self,
        messages: list[dict[str, str]],
        format: str | None = None,
        model: str | None = None,
        options: dict[str, Any] | None = None,
    ) -> str:
        try:
            if LLM_PROVIDER == "groq":
                if not GROQ_API_KEY:
                    raise ValueError("Falta GROQ_API_KEY en .env.")
                payload: dict[str, Any] = {
                    "model": model or self.model,
                    "messages": messages,
                    "temperature": self.temperature,
                }
                if format == "json":
                    payload["response_format"] = {"type": "json_object"}
                response = requests.post(
                    f"{GROQ_BASE_URL.rstrip('/')}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                    timeout=(10, self.timeout_seconds),
                )
            else:
                merged_options: dict[str, Any] = {"temperature": self.temperature}
                if options:
                    merged_options.update(options)
                payload = {
                    "model": model or self.model,
                    "messages": messages,
                    "stream": False,
                    "options": merged_options,
                }
                if format:
                    payload["format"] = format
                response = requests.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                    timeout=(10, self.timeout_seconds),
                )
            response.raise_for_status()
            data = response.json()
            if LLM_PROVIDER == "groq":
                return data["choices"][0]["message"]["content"].strip()
            return data["message"]["content"].strip()
        except requests.exceptions.ReadTimeout as exc:
            raise TimeoutError(
                f"Ollama tardó más de {self.timeout_seconds}s en responder. "
                "Aumenta OLLAMA_TIMEOUT_SECONDS en .env o usa una consulta más corta."
            ) from exc
        except requests.exceptions.ConnectionError as exc:
            raise ConnectionError(
                "No se pudo conectar con Ollama. Verifica que esté corriendo en "
                f"{self.base_url} y que el modelo exista en `ollama list`."
            ) from exc
        except requests.exceptions.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else "?"
            body = (exc.response.text[:240] if exc.response is not None else "").strip()
            raise RuntimeError(f"Ollama respondió HTTP {status}. Detalle: {body}") from exc
        except requests.exceptions.RequestException as exc:
            raise RuntimeError(f"Error de red al llamar Ollama: {exc}") from exc

    def chat_json(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        raw = self.chat(messages, format="json", model=model, options=options)
        return self._parse_json(raw)

    @staticmethod
    def _parse_json(raw: str) -> dict[str, Any]:
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Ollama no devolvió JSON válido: {raw[:200]}") from exc