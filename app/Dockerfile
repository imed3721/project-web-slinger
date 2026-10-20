FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG APP_VERSION=unknown
ENV APP_VERSION=${APP_VERSION}

WORKDIR /app

COPY app.py /app/app.py

RUN useradd --system --uid 10001 appuser

USER 10001:10001

EXPOSE 8080

CMD ["python", "-u", "/app/app.py"]
