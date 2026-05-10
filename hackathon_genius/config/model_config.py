import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLLMClient
from google.adk.models.lite_llm import LiteLlm
from pydantic import Field


_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_ENV_CANDIDATES = [
    _PROJECT_ROOT / "config" / ".env",
    _PROJECT_ROOT / ".env",
]
for _env_path in _ENV_CANDIDATES:
    if _env_path.exists():
        load_dotenv(_env_path, override=False)
        break


class SafeLiteLlm(LiteLlm):
    """LiteLlm variant safe to expose in ADK Web graphs.

    ADK 1.32.0 serializes agent definitions for the Dev UI. The upstream
    LiteLlm model keeps a runtime-only LiteLLMClient instance as a regular
    Pydantic field, which breaks JSON serialization in /dev/build_graph.
    We keep the same runtime behavior for provider APIs (Gemini/OpenAI-compatible),
    but exclude the client from serialization so the app remains compatible
    with ADK Web.
    """

    llm_client: LiteLLMClient = Field(default_factory=LiteLLMClient, exclude=True)


def _normalize_model_name(model_name: str, api_base: str) -> str:
    normalized_model = model_name.strip()
    if "/" not in normalized_model:
        normalized_model = f"openai/{normalized_model}"

    if "localhost:4000" in api_base or "127.0.0.1:4000" in api_base:
        provider, _, provider_model = normalized_model.partition("/")
        if provider == "openai":
            normalized_model = f"{provider}/{provider_model.lower()}"

    return normalized_model


def _normalize_api_base(api_base: str) -> str:
    normalized_base = api_base.strip().rstrip("/")

    if "localhost:4000" not in normalized_base and "127.0.0.1:4000" not in normalized_base:
        return normalized_base

    if normalized_base.endswith("/openai/v1"):
        return normalized_base
    if normalized_base.endswith("/openai"):
        return f"{normalized_base}/v1"
    if normalized_base.endswith("/v1"):
        return normalized_base[:-3] + "/openai/v1"

    return f"{normalized_base}/openai/v1"


def build_demo_model() -> LiteLlm:
    gemini_key = os.getenv("GEMINI_API_KEY")

    if gemini_key:
        api_base = os.getenv("GEMINI_API_BASE", "https://generativelanguage.googleapis.com/v1beta/openai")
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        api_key = gemini_key
    else:
        api_base = os.getenv("LM_PROXY_BASE_URL", os.getenv("OPENAI_API_BASE", "https://generativelanguage.googleapis.com/v1beta/openai"))
        model_name = os.getenv("LM_PROXY_MODEL", os.getenv("OPENAI_MODEL", "gemini-2.5-flash"))
        api_key = os.getenv("LM_PROXY_API_KEY", os.getenv("OPENAI_API_KEY"))

    api_base = _normalize_api_base(api_base)
    model_name = _normalize_model_name(model_name, api_base)

    if not api_key:
        raise ValueError(
            "Brak klucza API. Ustaw GEMINI_API_KEY w pliku .env "
            "(lub alternatywnie LM_PROXY_API_KEY / OPENAI_API_KEY)."
        )

    # LiteLLM w ADK pobiera parametry dostawcy z env.
    os.environ["OPENAI_API_BASE"] = api_base
    os.environ["OPENAI_API_KEY"] = api_key

    return SafeLiteLlm(
        model=model_name,
    )
