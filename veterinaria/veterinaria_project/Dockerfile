FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libpq-dev \
        netcat-openbsd \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/staticfiles /app/media

COPY scripts/wait_for_db.sh /wait_for_db.sh
RUN chmod +x /wait_for_db.sh

EXPOSE 8000

CMD ["/wait_for_db.sh", "gunicorn", "--bind", "0.0.0.0:8000", "veterinaria.wsgi:application"]