"""
Hackathon Genius — moduł zabezpieczeń agentów (security boundary).

Ten moduł implementuje ochronę na granicy wejścia do systemu (human → agent):

1. **Prompt injection guard** — wykrywa próby zmiany zachowania agenta przez prompt injection, jailbreak, manipulację poleceniami.
2. **Rate limiting** — ogranicza liczbę żądań na użytkownika (token bucket, burst, refill rate).
3. **Tool argument guard** — waliduje argumenty narzędzi (typy, długości, allowlisty, path traversal, znaki specjalne).
4. **Tool isolation** — enforce'uje allowlistę narzędzi per agent (każdy agent może wywołać tylko wybrane narzędzia).

**Architektura:**
- Zabezpieczenia są stosowane WYŁĄCZNIE na granicy człowiek → system (np. wejście do IdeaAgent).
- Komunikacja wewnętrzna między agentami (przez session.state) jest zaufana i nie przechodzi przez te bramki.
- Dzięki temu atakujący nie może obejść zabezpieczeń przez chain-of-thought lub prompt chaining.

**Przykład:**
Użytkownik → [prompt_injection_guard + rate_limiter] → IdeaAgent → [tool_argument_guard + tool isolation] → narzędzie

Każda blokada zwraca bezpieczną odmowę (nie wycieka szczegółów implementacji).
"""

from __future__ import annotations

import logging
import re
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

from .rate_limiter import get_rate_limiter

logger = logging.getLogger(__name__)

MAX_INPUT_LENGTH = 500

_INJECTION_PATTERNS: tuple[str, ...] = (
    "ignore previous instructions",
    "zignoruj poprzednie instrukcje",
    "ignore all instructions",
    "forget your instructions",
    "forget everything",
    "you are now",
    "jestes teraz",
    "act as",
    "udawaj ze jestes",
    "system prompt",
    "reveal your instructions",
    "ujawnij instrukcje",
    "print your system",
    "show me your prompt",
    "pretend you are",
    "override instructions",
    "bypass safety",
    "jailbreak",
    "dan mode",
    "developer mode",
    "disable your filters",
    "wylacz filtry",
)

_AGENT_TOOL_ALLOWLIST: dict[str, frozenset[str]] = {
    "IdeaAgent": frozenset({"browse_hackathon_themes"}),
}

_TOOL_ARG_CONSTRAINTS: dict[str, dict[str, dict]] = {
    "browse_hackathon_themes": {
        "theme": {"type": str, "max_len": 100},
    },
}

_DANGEROUS_CHARS = re.compile(r"\.\.[\\/]|[;|&`$<>{}]")


def prompt_injection_guard(
    callback_context: CallbackContext,
    llm_request: LlmRequest,
) -> Optional[LlmResponse]:
    """Callback before_model z ochrona injection i rate limit."""
    user_id = "anonymous"
    try:
        if hasattr(callback_context, "session") and callback_context.session:
            state = getattr(callback_context.session, "state", None)
            if isinstance(state, dict):
                user_id = state.get("user_id", "anonymous")
            elif state is not None:
                user_id = getattr(state, "user_id", "anonymous")
    except Exception as e:
        logger.debug("[SECURITY] Could not extract user_id from session: %s", e)

    rate_limiter = get_rate_limiter()
    if not rate_limiter.is_allowed(user_id, tokens=1, agent_name="IdeaAgent"):
        status = rate_limiter.get_status(user_id)
        logger.warning(
            "[SECURITY] Rate limit exceeded for user %r: remaining_tokens=%.1f",
            user_id,
            status["remaining_tokens"],
        )
        raise ValueError(
            f"[SECURITY BLOCK] Zbyt wiele żądań. Prosimy czekać.\n"
            f"Refill: {status['refill_rate_per_second']:.2f} token/s."
        )

    user_text = ""
    if llm_request.contents:
        last = llm_request.contents[-1]
        if hasattr(last, "parts") and last.parts:
            user_text = " ".join(p.text for p in last.parts if hasattr(p, "text") and p.text)

    if len(user_text) > MAX_INPUT_LENGTH:
        logger.warning(
            "[SECURITY] Input too long: %d chars (max %d)",
            len(user_text),
            MAX_INPUT_LENGTH,
        )
        raise ValueError(
            f"[SECURITY BLOCK] Wejście jest zbyt długie ({len(user_text)} znaków). "
            f"Maksimum to {MAX_INPUT_LENGTH}."
        )

    lower = user_text.lower()
    for pattern in _INJECTION_PATTERNS:
        if pattern in lower:
            logger.warning("[SECURITY] Prompt injection detected: %r", pattern)
            raise ValueError(
                "[SECURITY BLOCK] Wykryto niedozwoloną próbę zmiany zachowania agenta."
            )

    return None


def tool_argument_guard(
    tool: BaseTool,
    args: dict,
    tool_context: ToolContext,
) -> Optional[dict]:
    """Callback before_tool z izolacja narzedzi i walidacja argumentow."""
    tool_name = tool.name
    agent_name: Optional[str] = getattr(tool_context, "agent_name", None)

    if agent_name and agent_name in _AGENT_TOOL_ALLOWLIST:
        allowed = _AGENT_TOOL_ALLOWLIST[agent_name]
        if tool_name not in allowed:
            logger.warning(
                "[SECURITY] Agent %r attempted unauthorized tool %r (allowed: %s)",
                agent_name,
                tool_name,
                sorted(allowed),
            )
            raise ValueError(
                f"[SECURITY BLOCK] Agent '{agent_name}' nie ma uprawnień do narzędzia '{tool_name}'. "
                f"Dozwolone narzędzia: {sorted(allowed)}."
            )

    constraints = _TOOL_ARG_CONSTRAINTS.get(tool_name, {})

    for arg_name, value in args.items():
        constraint = constraints.get(arg_name, {})

        if isinstance(value, str):
            if _DANGEROUS_CHARS.search(value):
                logger.warning(
                    "[SECURITY] Dangerous chars in arg %r for tool %r: %r",
                    arg_name,
                    tool_name,
                    value,
                )
                raise ValueError(
                    f"[SECURITY BLOCK] Argument '{arg_name}' zawiera niedozwolone znaki (path traversal lub iniekcja)."
                )

            max_len = constraint.get("max_len", 200)
            if len(value) > max_len:
                logger.warning(
                    "[SECURITY] Arg %r too long for tool %r: %d > %d",
                    arg_name,
                    tool_name,
                    len(value),
                    max_len,
                )
                raise ValueError(
                    f"[SECURITY BLOCK] Argument '{arg_name}' przekracza dozwoloną długość {max_len} (podano {len(value)})."
                )

            if "allowlist" in constraint:
                normalized = value.lower().strip()
                if normalized not in constraint["allowlist"]:
                    logger.warning(
                        "[SECURITY] Arg %r value %r not in allowlist for tool %r",
                        arg_name,
                        value,
                        tool_name,
                    )
                    raise ValueError(
                        f"[SECURITY BLOCK] Wartość '{value}' dla argumentu '{arg_name}' jest niedozwolona. "
                        f"Dozwolone: {sorted(constraint['allowlist'])}."
                    )

        elif isinstance(value, int):
            if "min" in constraint and value < constraint["min"]:
                raise ValueError(
                    f"[SECURITY BLOCK] Argument '{arg_name}' = {value} jest poniżej minimum ({constraint['min']})."
                )
            if "max" in constraint and value > constraint["max"]:
                raise ValueError(
                    f"[SECURITY BLOCK] Argument '{arg_name}' = {value} przekracza maksimum ({constraint['max']})."
                )
            if "allowlist" in constraint and value not in constraint["allowlist"]:
                raise ValueError(
                    f"[SECURITY BLOCK] Wartość {value} dla '{arg_name}' jest niedozwolona. "
                    f"Dozwolone: {sorted(constraint['allowlist'])}."
                )

    return None
