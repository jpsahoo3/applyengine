FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY backend ./backend

RUN python -m pip install --upgrade pip && \
    python -m pip install .

ENV PYTHONPATH=/app/backend

EXPOSE 8000

CMD ["python", "-m", "applyengine.main"]

