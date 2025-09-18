FROM python:3.12-slim

# Install curl and uv
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/ \
    && mv /root/.local/bin/uvx /usr/local/bin/

WORKDIR /app

# Copy only dependency file first (caches layers)
COPY requirements.txt .

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev


# Install dependencies into system Python
# "--frozen" ensures lock file consistency if present
RUN uv pip install --system --no-cache -r requirements.txt

# Now copy the rest of your app
COPY . .

# Expose port
EXPOSE 8001

# Run the app directly (no uv needed at runtime)
CMD ["uv", "run","uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
