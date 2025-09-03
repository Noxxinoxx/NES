# Use official Python base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements (optional if you have a requirements.txt)
# We'll install packages directly here
RUN pip install --no-cache-dir confluent-kafka pymongo

# Copy your worker script into the container
COPY worker.py /app/worker.py

# Expose ports if needed (not strictly necessary for this worker)
# EXPOSE 5000

# Set default command to run the worker
CMD ["python", "testDBconnect.py"]