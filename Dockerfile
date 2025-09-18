FROM python:3.12-slim

# Install curl and uv
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/ \
    && mv /root/.local/bin/uvx /usr/local/bin/

WORKDIR /app

# Copy dependency files first (layer caching)
COPY requirements.txt .
COPY pyproject.toml uv.lock ./

# Sync deps with uv (lock consistency)
RUN uv sync --frozen --no-dev

# Install deps into system Python
RUN uv pip install --system --no-cache -r requirements.txt

# Copy app source
COPY . .

EXPOSE 8001

# Use python -m uvicorn instead of bare "uvicorn"
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
