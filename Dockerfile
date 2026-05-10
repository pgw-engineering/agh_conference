# ---------------------------------------------------------------------------
# Hackathon Genius — Dockerfile
#
# Zasady bezpieczeństwa:
#   - obraz bazowy slim (minimalna powierzchnia ataku)
#   - budowa w dwóch etapach: builder (pip install) + runtime
#   - runtime uruchamiany jako nieuprzywilejowany użytkownik appuser (UID 1001)
#   - tylko niezbędne pliki kopiowane do obrazu
#   - brak .env w obrazie — sekrety przez zmienne środowiskowe
# ---------------------------------------------------------------------------

# ---- Etap 1: instalacja zależności ----------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

# Kopiuj tylko requirements, żeby Docker cache działał optymalnie
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir --prefix=/install -r requirements.txt


# ---- Etap 2: obraz runtime -------------------------------------------------
FROM python:3.12-slim AS runtime

# Utwórz nieuprzywilejowanego użytkownika
RUN groupadd -r appuser --gid 1001 \
 && useradd  -r -g appuser --uid 1001 --no-create-home appuser

WORKDIR /app

# Skopiuj zainstalowane pakiety z etapu builder
COPY --from=builder /install /usr/local

# Skopiuj tylko kod aplikacji (bez .env, .venv, .git, notebooków)
COPY hackathon_genius/ ./hackathon_genius/

# Katalogi wymagające zapisu — właściciel appuser
# .adk/artifacts  — artefakty ADK
# hackathon_genius/.adk — session.db tworzony przez adk web
RUN mkdir -p /app/.adk/artifacts \
           /app/hackathon_genius/.adk \
 && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Uruchom ADK Web — wywołanie przez skrypt CLI (nie python -m adk)
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8000"]
