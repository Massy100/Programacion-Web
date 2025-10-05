FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN groupadd -r django && useradd -r -g django django

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-dev \
        netcat-openbsd \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY scripts/wait_for_db.sh /wait_for_db.sh
RUN chmod +x /wait_for_db.sh

RUN chown -R django:django /app

USER django

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

CMD ["/wait_for_db.sh", "gunicorn", "--bind", "0.0.0.0:8000", "veterinaria_project.wsgi:application"]