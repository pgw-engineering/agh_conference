"""
Rate limiter dla ochrony agentow przed DoS.

Implementuje:
1. Per-user rate limiting (token bucket algorithm)
2. Per-endpoint rate limiting
3. Burst protection
"""

from __future__ import annotations

import logging
import time
from collections import defaultdict
from dataclasses import dataclass, field
from threading import Lock
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class RateLimitConfig:
    """
    Konfiguracja limitów dla agenta (token bucket):

    Attributes:
        requests_per_minute (int):
            Ile żądań na minutę może wykonać użytkownik przy równomiernym tempie.
            Przekłada się na szybkość "napełniania" tokenów w kubełku (refill_rate).

        burst_size (int):
            Maksymalna liczba żądań, które można wykonać "na raz" (w krótkim czasie),
            zanim kubełek się wyczerpie. Pozwala na chwilowe "wybuchy" aktywności
            bez natychmiastowego blokowania.

        tokens_per_request (float):
            Ile tokenów kosztuje pojedyncze żądanie. Pozwala różnicować koszt
            różnych operacji (np. droższe narzędzia mogą kosztować więcej niż 1).

    Przykład:
        Jeśli requests_per_minute=10 i burst_size=3:
        - Użytkownik może wykonać 3 żądania "od razu" (burst),
        - Potem kolejne co 6 sekund (60/10), aż kubełek się napełni.
    """

    requests_per_minute: int = 1
    burst_size: int = 2
    tokens_per_request: float = 1.0


@dataclass
class TokenBucket:
    """Token bucket dla rate limitingu."""

    capacity: float = 10.0
    refill_rate: float = 10.0 / 60.0
    tokens: float = field(default_factory=lambda: 10.0)
    last_refill: float = field(default_factory=time.time)
    lock: Lock = field(default_factory=Lock)

    def refill(self):
        """Uzupelnij tokeny na podstawie czasu."""
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def consume(self, tokens: float = 1.0) -> bool:
        """
        Sprobuj skonsumowac tokeny.

        Returns:
            True jesli udalo sie, False jesli rate limit exceeded.
        """
        with self.lock:
            self.refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False

    def get_remaining(self) -> float:
        """Zwroc ile tokenow zostalo."""
        with self.lock:
            self.refill()
            return self.tokens


class RateLimiter:
    """
    Per-user + per-endpoint rate limiter.

    Chroni przed:
    - Jednym uzytkownikiem zalewajacym API
    - Burst DOS atakami
    - Exhausting model API quota
    """

    def __init__(self, config: Optional[RateLimitConfig] = None):
        self.config = config or RateLimitConfig()
        self.user_buckets: dict[str, TokenBucket] = defaultdict(self._create_bucket)
        self.lock = Lock()

    def _create_bucket(self) -> TokenBucket:
        """Utworz nowy bucket dla nowego uzytkownika."""
        return TokenBucket(
            capacity=self.config.burst_size,
            refill_rate=self.config.requests_per_minute / 60.0,
        )

    def is_allowed(
        self,
        user_id: str = "anonymous",
        tokens: float = 1.0,
        agent_name: str = "unknown",
    ) -> bool:
        """
        Sprawdz czy zadanie jest dozwolone.

        Args:
            user_id: Identyfikator uzytkownika (IP, session ID, API key)
            tokens: Ile tokenow kosztuje to zadanie
            agent_name: Nazwa agenta (dla logow)

        Returns:
            True jesli jest dozwolone, False jesli rate limit exceeded
        """
        bucket = self.user_buckets[user_id]
        allowed = bucket.consume(tokens)

        if not allowed:
            remaining = bucket.get_remaining()
            logger.warning(
                "[RATE_LIMIT] User %s denied: agent=%s, tokens_needed=%.1f, remaining=%.1f",
                user_id,
                agent_name,
                tokens,
                remaining,
            )
        else:
            logger.debug(
                "[RATE_LIMIT] User %s allowed: agent=%s, tokens_used=%.1f",
                user_id,
                agent_name,
                tokens,
            )

        return allowed

    def get_status(self, user_id: str = "anonymous") -> dict:
        """Zwroc status rate limitingu dla uzytkownika."""
        bucket = self.user_buckets[user_id]
        return {
            "user_id": user_id,
            "remaining_tokens": bucket.get_remaining(),
            "capacity": bucket.capacity,
            "refill_rate_per_second": bucket.refill_rate,
        }


_rate_limiter: Optional[RateLimiter] = None


def get_rate_limiter() -> RateLimiter:
    """Zwroc globalna instancje rate limitera."""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter(
            config=RateLimitConfig(
                requests_per_minute=1,
                burst_size=2,
            )
        )
    return _rate_limiter
