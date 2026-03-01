FROM ghcr.io/astral-sh/uv:latest AS uv
FROM dhi.io/python:3.14-dev AS builder

WORKDIR /build

# Install uv
COPY --from=uv /uv /usr/local/bin/uv

# Copy dependency files and OpenAPI specs
COPY pyproject.toml ./
COPY uv.lock* ./
COPY context/ ./context/
COPY app/ ./app/

# Install dependencies (with dev for openapi-python-client) and generate API clients
RUN uv sync --frozen
RUN uv run poe generate-clients

# Downgrade builder venv to production deps only (smaller image)
RUN uv sync --frozen --no-dev

# Runtime stage
FROM dhi.io/python:3.14

WORKDIR /app

# Copy the virtual environment and application from builder
COPY --from=builder /build/.venv /app/.venv
COPY --from=builder /build/app ./app

# Make sure we use the virtual environment's Python
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Expose port
EXPOSE 9090

# Health check using Python (hardened images don't include curl)
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD /app/.venv/bin/python -c "import urllib.request; urllib.request.urlopen('http://localhost:9090/health').read()" || exit 1

CMD ["/app/.venv/bin/python", "-m", "app.main"]

