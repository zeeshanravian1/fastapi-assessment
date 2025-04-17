FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.21 /uv /uvx /bin/

# Copy project files first for dependency installation
COPY ./pyproject.toml ./uv.lock /app/

# Install dependencies globally instead of in a virtual environment
RUN uv pip compile --all-extras pyproject.toml > requirements.txt && \
    uv pip install --system -r requirements.txt

# Copy your actual project structure
COPY ./scripts /app/scripts
COPY ./static /app/static
COPY ./fastapi_assessment /app/fastapi_assessment
COPY ./main.py ./.env /app/

ENV PYTHONPATH=/app

# Run FastAPI Server
CMD ["fastapi", "run", "--workers", "4", "main.py"]
