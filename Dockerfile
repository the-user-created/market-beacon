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

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN set -e; \
    wget https://github.com/ta-lib/ta-lib/releases/download/v0.6.4/ta-lib-0.6.4-src.tar.gz && \
    tar -xzf ta-lib-0.6.4-src.tar.gz && \
    cd ta-lib-0.6.4 && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.6.4-src.tar.gz

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

COPY --from=builder /usr/lib/libta-lib.so.* /usr/lib/

COPY --from=builder /app/.venv /opt/venv
COPY entrypoint.sh ./entrypoint.sh

RUN set -e; \
    chmod +x ./entrypoint.sh && \
    chown -R app:app /home/app/market-beacon /opt/venv && \
    ldconfig

USER app

STOPSIGNAL SIGTERM

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "from market_beacon.api import BitgetClient; from market_beacon.config import settings; client = BitgetClient(settings.bitget_api_key, settings.bitget_api_secret, settings.bitget_api_passphrase); client.market.get_server_time();"

ENTRYPOINT ["./entrypoint.sh"]

CMD ["run"]
