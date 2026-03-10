# MurphyX control API — scaffold image.
# Build: docker build -t murphyx-api .
# Run:   docker run -p 8000:8000 murphyx-api
#
# TODO: Multi-stage build, non-root user, and COPY murphyx/ when api imports runtime.
# Safe for public repo — no secrets baked in.

FROM python:3.12-slim

WORKDIR /app

# Minimal deps for api/main.py only; extend when murphyx is wired.
RUN pip install --no-cache-dir fastapi uvicorn[standard]

COPY api ./api

ENV PYTHONPATH=/app
EXPOSE 8000

# TODO: Switch to gunicorn + uvicorn workers for production.
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
