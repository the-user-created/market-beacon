# =================
#  Builder Stage
# =================
FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-cache --no-install-project --all-extras --dev

COPY src/ ./src/

RUN uv sync --locked --no-cache --no-editable

# =================
#   Final Stage
# =================
FROM python:3.12-slim

RUN addgroup --system app && adduser --system --group app
WORKDIR /home/app/market-beacon
ENV HOME=/home/app

COPY --from=builder /app/.venv /opt/venv

COPY entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

ENV PATH="/opt/venv/bin:$PATH"

RUN chown -R app:app .

USER app

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "from market_beacon import __main__"

ENTRYPOINT ["./entrypoint.sh"]

CMD ["run"]
