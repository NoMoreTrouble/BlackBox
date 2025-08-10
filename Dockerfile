# Multi-arch capable when built with buildx
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1     PIP_NO_CACHE_DIR=1     TZ=Europe/Rome

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends         build-essential git curl tmux locales     && rm -rf /var/lib/apt/lists/*

# Locales for Flask-Babel
RUN sed -i '/it_IT.UTF-8/s/^# //' /etc/locale.gen &&     sed -i '/en_US.UTF-8/s/^# //' /etc/locale.gen && locale-gen

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# Create runtime dirs
RUN mkdir -p var/log && mkdir -p plant_monitor/web/translations

EXPOSE 8080

CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:8080", "wsgi:app"]
