FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies required by discord.py and confluent-kafka
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3 -m pip install --upgrade pip setuptools wheel

# Install Python dependencies
RUN python3 -m pip install --no-cache-dir \
    confluent-kafka \
    pymongo \
    watchdog \
    "discord.py" \
    requests