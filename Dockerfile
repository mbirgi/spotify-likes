FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create logs directory
RUN mkdir -p /root/logs

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set Spotify credentials from build args
ARG SPOTIFY_CLIENT_ID
ARG SPOTIFY_CLIENT_SECRET
ARG SPOTIFY_REDIRECT_URI
ENV SPOTIFY_CLIENT_ID=${SPOTIFY_CLIENT_ID}
ENV SPOTIFY_CLIENT_SECRET=${SPOTIFY_CLIENT_SECRET}
ENV SPOTIFY_REDIRECT_URI=${SPOTIFY_REDIRECT_URI}

# Run the script
CMD ["python", "main.py"]