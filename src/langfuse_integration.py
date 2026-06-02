"""Langfuse tracing helpers for the Vigía Cauca pipeline.

This module uses the current Langfuse Python SDK v4 API:
- start_as_current_observation() for nested observations
- propagate_attributes() for session/user correlation
- update() and score()/score_trace() on the active observation
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Iterator

from langfuse import Langfuse, propagate_attributes

from config import LANGFUSE_ENABLED, LANGFUSE_HOST, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY


@dataclass
class _NoopObservation:
    """Fallback object used when Langfuse is disabled."""

    name: str

    def update(self, **kwargs: Any) -> None:
        return None

    def score(self, **kwargs: Any) -> None:
        return None

    def score_trace(self, **kwargs: Any) -> None:
        return None

    def end(self) -> None:
        return None


class _ObservationWrapper:
    """Wrap a real Langfuse observation and normalize score() signatures.

    The Langfuse SDK surface varies between versions; this adapter attempts
    several calling patterns to remain compatible with installed client.
    """

    def __init__(self, obs: Any) -> None:
        self._obs = obs

    def update(self, **kwargs: Any) -> None:
        try:
            self._obs.update(**kwargs)
        except Exception:
            # Best-effort: ignore update failures to keep pipeline running
            import traceback
            traceback.print_exc()

    def score(self, name: str | None = None, score: float | None = None, reason: str | None = None) -> None:
        # Try several call signatures used across Langfuse versions.
        tried = []
        # 1) positional: value, name, comment
        if score is not None:
            try:
                self._obs.score(score, name or None, reason)
                return
            except Exception as e:
                tried.append(e)
        # 2) positional value, name=..., comment=...
        if score is not None:
            try:
                self._obs.score(score, name=name, comment=reason)
                return
            except Exception as e:
                tried.append(e)
        # 3) value=..., name=..., comment=...
        if score is not None:
            try:
                self._obs.score(value=score, name=name, comment=reason)
                return
            except Exception as e:
                tried.append(e)
        # 4) older variants might use (value, label, note)
        if score is not None:
            try:
                self._obs.score(score, name or reason)
                return
            except Exception as e:
                tried.append(e)

        # 5) fallback: try calling with provided kwargs if obs accepts them
        try:
            kwargs = {}
            if name is not None:
                kwargs["name"] = name
            if score is not None:
                # Some implementations expect 'value' instead of 'score'
                kwargs["value"] = score
            if reason is not None:
                # some implementations use 'comment' or 'reason'
                kwargs["comment"] = reason
            if kwargs:
                self._obs.score(**kwargs)
                return
        except Exception as e:
            tried.append(e)

        # If we reach here, we couldn't call score() in a compatible way.
        print("⚠️  Langfuse observation: unable to call score() with supplied args. Exceptions:")
        for ex in tried:
            print(" -", ex)

    def score_trace(self, **kwargs: Any) -> None:
        try:
            self._obs.score_trace(**kwargs)
        except Exception:
            # Some SDKs may not implement score_trace; attempt a best-effort
            try:
                # try calling score as fallback when trace scoring unavailable
                name = kwargs.get("name")
                score = kwargs.get("score") or kwargs.get("value")
                reason = kwargs.get("reason") or kwargs.get("comment")
                if score is not None:
                    self.score(name=name, score=score, reason=reason)
            except Exception:
                import traceback
                traceback.print_exc()

    def end(self) -> None:
        try:
            self._obs.end()
        except Exception:
            pass


class LangfuseTracer:
    """Small wrapper around the Langfuse client for this app."""

    def __init__(self, enabled: bool = LANGFUSE_ENABLED) -> None:
        self.enabled = bool(enabled and LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY)
        self.client: Langfuse | None = None

        if not self.enabled:
            return

        try:
            self.client = Langfuse(
                public_key=LANGFUSE_PUBLIC_KEY,
                secret_key=LANGFUSE_SECRET_KEY,
                host=LANGFUSE_HOST or None,
            )
        except Exception:
            # If initialization fails, disable the tracer but keep the app running.
            import traceback
            print("⚠️  Langfuse client initialization failed; tracer disabled.")
            traceback.print_exc()
            self.client = None
            self.enabled = False

    @staticmethod
    def _clean_metadata(metadata: dict[str, Any] | None) -> dict[str, str]:
        cleaned: dict[str, str] = {}
        for key, value in (metadata or {}).items():
            if value is None:
                continue
            cleaned[str(key)] = str(value)[:200]
        return cleaned

    @staticmethod
    def _safe_name(name: str) -> str:
        return name.strip()[:120] or "vigia-cauca"

    @contextmanager
    def trace_pipeline(
        self,
        pipeline_name: str,
        question: str,
        *,
        session_id: str | None = None,
        user_id: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Iterator[Any]:
        if not self.enabled or self.client is None:
            yield _NoopObservation(name=pipeline_name)
            return

        clean_metadata = self._clean_metadata(metadata)
        with propagate_attributes(
            trace_name=self._safe_name(pipeline_name),
            session_id=session_id,
            user_id=user_id,
            tags=tags,
            metadata=clean_metadata or None,
        ):
            with self.client.start_as_current_observation(
                as_type="span",
                name=self._safe_name(pipeline_name),
                input={"question": question},
                metadata=clean_metadata or None,
            ) as observation:
                yield _ObservationWrapper(observation)

    @contextmanager
    def trace_agent(
        self,
        agent_name: str,
        *,
        as_type: str = "generation",
        input: Any | None = None,
        model: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Iterator[Any]:
        if not self.enabled or self.client is None:
            yield _NoopObservation(name=agent_name)
            return

        clean_metadata = self._clean_metadata(metadata)
        with self.client.start_as_current_observation(
            as_type=as_type,  # type: ignore[arg-type]
            name=self._safe_name(agent_name),
            input=input,
            model=model,
            metadata=clean_metadata or None,
        ) as observation:
            yield _ObservationWrapper(observation)

    @contextmanager
    def trace_neo4j(
        self,
        query: str,
        params: dict[str, Any] | None = None,
        *,
        metadata: dict[str, Any] | None = None,
    ) -> Iterator[Any]:
        if not self.enabled or self.client is None:
            yield _NoopObservation(name="Neo4j Query")
            return

        clean_metadata = self._clean_metadata(metadata)
        input_payload = {
            "query": query,
            "param_keys": sorted(list((params or {}).keys())),
        }
        with self.client.start_as_current_observation(
            as_type="tool",
            name="Neo4j Query",
            input=input_payload,
            metadata=clean_metadata or None,
        ) as observation:
            yield _ObservationWrapper(observation)

    def flush(self) -> None:
        if self.enabled and self.client is not None:
            try:
                self.client.flush()
            except Exception as e:
                msg = str(e) or ""
                # Detect common unauthorized error messages
                if "401" in msg or "Unauthorized" in msg or "authentication" in msg.lower():
                    print("❌ Langfuse export failed: 401 Unauthorized. Check your LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY.")
                    # disable tracer to avoid repeated errors
                    self.enabled = False
                else:
                    print(f"⚠️ Langfuse flush error: {e}")
                # avoid raising to keep pipeline functional

    def shutdown(self) -> None:
        if self.enabled and self.client is not None:
            self.client.shutdown()


__all__ = ["LangfuseTracer"]
