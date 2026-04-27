import os
from pathlib import Path

from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv


_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_ENV_CANDIDATES = [
    _PROJECT_ROOT / "config" / ".env",
    _PROJECT_ROOT / ".env",
]
for _env_path in _ENV_CANDIDATES:
    if _env_path.exists():
        load_dotenv(_env_path, override=False)
        break


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
    api_base = os.getenv("LM_PROXY_BASE_URL", os.getenv("OPENAI_API_BASE", "http://localhost:4000/openai/v1"))
    api_base = _normalize_api_base(api_base)

    model_name = os.getenv("LM_PROXY_MODEL", "gpt-4.1")
    model_name = _normalize_model_name(model_name, api_base)

    api_key = os.getenv("LM_PROXY_API_KEY", os.getenv("OPENAI_API_KEY", "local-proxy"))

    return LiteLlm(
        model=model_name,
        api_base=api_base,
        api_key=api_key,
    )