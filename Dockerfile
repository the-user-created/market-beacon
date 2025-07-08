# ==============================================================================
#  ARG - Define Build-Time Variables
# ==============================================================================
ARG PYTHON_VERSION=3.12
ARG PYTHON_VARIANT=slim
ARG APP_VERSION=0.0.0

# ==============================================================================
#  Builder Stage
# ==============================================================================
FROM python:${PYTHON_VERSION}-${PYTHON_VARIANT} AS builder

ARG APP_VERSION

LABEL org.opencontainers.image.title="Market Beacon Builder"
LABEL org.opencontainers.image.description="Builder stage for the Market Beacon application."
LABEL org.opencontainers.image.version=${APP_VERSION}
LABEL org.opencontainers.image.authors="David Young <davidsamuelyoung@protonmail.com>"
LABEL org.opencontainers.image.url="https://github.com/the-user-created/market-beacon"
LABEL org.opencontainers.image.source="https://github.com/the-user-created/market-beacon.git"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN set -e; \
    echo "--> Syncing dependencies..." && \
    uv sync --locked --no-cache --no-install-project --all-extras --dev

COPY src/ ./src/

RUN set -e; \
    echo "--> Syncing application..." && \
    uv sync --locked --no-cache --no-editable

# ==============================================================================
#  Final Stage
# ==============================================================================
FROM python:${PYTHON_VERSION}-${PYTHON_VARIANT}

ARG APP_VERSION
ARG BUILD_DATE

LABEL org.opencontainers.image.title="Market Beacon"
LABEL org.opencontainers.image.description="A Python bot to retrieve and analyze trade data from the Bitget exchange."
LABEL org.opencontainers.image.version=${APP_VERSION}
LABEL org.opencontainers.image.authors="David Young <davidsamuelyoung@protonmail.com>"
LABEL org.opencontainers.image.url="https://github.com/the-user-created/market-beacon"
LABEL org.opencontainers.image.documentation="https://github.com/the-user-created/market-beacon/blob/main/README.md"
LABEL org.opencontainers.image.source="https://github.com/the-user-created/market-beacon.git"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV HOME=/home/app \
    PATH="/opt/venv/bin:$PATH"

RUN set -e; \
    addgroup --system app && \
    adduser --system --group app

WORKDIR /home/app/market-beacon

COPY --from=builder /app/.venv /opt/venv
COPY entrypoint.sh ./entrypoint.sh

RUN set -e; \
    chmod +x ./entrypoint.sh && \
    chown -R app:app /home/app/market-beacon /opt/venv

USER app

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "from market_beacon import __main__"

ENTRYPOINT ["./entrypoint.sh"]

CMD ["run"]
