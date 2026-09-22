# --- Base Stage ---
FROM python:3.12-slim AS base

# Installe uv et les dépendances système
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /bin/
RUN apt-get update && apt-get upgrade -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installe les dépendances en premier pour optimiser le cache des layers Docker
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Ajoute un utilisateur non-root pour la sécurité
RUN useradd -m appuser && chown -R appuser /app
USER appuser

ENV PYTHONPATH=/app/src
ENV PATH="/app/.venv/bin:$PATH"

# --- Labels ---

LABEL org.opencontainers.image.title="Titanic ML" \
      org.opencontainers.image.description="Apprentissage supervisé sur le dataset Titanic" \
      org.opencontainers.image.authors="bonnienaccache@gmail.com"

ARG BUILD_VERSION="dev"
ARG BUILD_REVISION="unknown"
ARG BUILD_DATE="unknown"

LABEL org.opencontainers.image.version="${BUILD_VERSION}" \
      org.opencontainers.image.revision="${BUILD_REVISION}" \
      org.opencontainers.image.created="${BUILD_DATE}"

# --- API Stage ---
FROM base AS api

COPY . .

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "titanic_ml.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- Streamlit Stage ---
FROM base AS streamlit

COPY . .

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
