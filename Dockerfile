# Builder stage
FROM dhi.io/python:3.14-dev AS builder

WORKDIR /build

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml ./
COPY uv.lock* ./

# Install dependencies using uv into a virtual environment
# uv sync creates a .venv directory with all dependencies
RUN if [ -f uv.lock ]; then \
        uv sync --frozen --no-dev; \
    else \
        uv sync --no-dev; \
    fi

# Runtime stage
FROM dhi.io/python:3.14

WORKDIR /app

# Copy the virtual environment from builder
# uv creates .venv in the working directory
COPY --from=builder /build/.venv /app/.venv

# Copy application code
COPY app/ ./app/

# Make sure we use the virtual environment's Python
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Expose port
EXPOSE 9090

# Health check using Python (hardened images don't include curl)
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD /app/.venv/bin/python -c "import urllib.request; urllib.request.urlopen('http://localhost:9090/health').read()" || exit 1

CMD ["/app/.venv/bin/python", "app/main.py"]
