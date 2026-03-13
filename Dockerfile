# MurphyX — multi-purpose image for API + worker.
# Build: docker build -t murphyx .
# API:   docker run -p 8000:8000 murphyx
# Worker: docker run murphyx python -m murphyx.runtime.worker_loop

FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY murphyx ./murphyx

ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["uvicorn", "murphyx.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
