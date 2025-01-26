FROM python:3.11-alpine3.21 AS builder

WORKDIR /app

RUN apk add --no-cache build-base libffi-dev

COPY requirements.txt ./

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.11-alpine3.21

WORKDIR /app

ENV GPIOZERO_PIN_FACTORY=rpigpio

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY / .

RUN export PYTHONPATH=/app
HEALTHCHECK --start-period=1m --interval=5m --timeout=15s \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:5000/status > /dev/null || exit 1