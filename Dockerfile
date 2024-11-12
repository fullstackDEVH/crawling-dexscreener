# Use official Python image as base
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy poetry files (pyproject.toml and poetry.lock) into the container
COPY dexscreener_crawling/pyproject.toml dexscreener_crawling/poetry.lock /app/

# Install dependencies using Poetry (without creating a virtualenv)
RUN poetry config virtualenvs.create false && poetry install --no-root

# Install wget and gnupg to enable the downloading and installation of Google Chrome
RUN apt-get update -y && apt-get install -y wget gnupg

# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - 
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update the package list and install chrome
RUN apt-get update -y && apt-get install -y google-chrome-stable

# Copy the application code (dexscreener_crawling directory) into the container
COPY dexscreener_crawling /app/dexscreener_crawling

# Expose port 8000 (if your app uses it)
EXPOSE 8000

# Run the Celery worker (tasks.py) using Poetry
CMD poetry run python dexscreener_crawling/dexscreener_crawling/tasks.py
