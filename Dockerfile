# Builder stage
FROM python:3.13-slim AS builder

WORKDIR /build

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml ./
COPY uv.lock* ./

# Install dependencies using uv into a virtual environment
# uv sync creates a .venv directory with all dependencies
# Include tools optional dependencies for DuckDuckGo, Wikipedia, and Arxiv tools
RUN if [ -f uv.lock ]; then \
        uv sync --frozen --no-dev --extra tools; \
    else \
        uv sync --no-dev --extra tools; \
    fi

# Runtime stage
FROM python:3.13-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

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

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:9090/health || exit 1

CMD ["/app/.venv/bin/python", "app/main.py"]
