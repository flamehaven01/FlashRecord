# FlashRecord Dockerfile
# Multi-stage build for optimized image size

# Build stage
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install --no-cache-dir poetry

# Copy project files
COPY pyproject.toml poetry.lock* ./
COPY flashrecord ./flashrecord
COPY README.md ./

# Configure poetry to not create virtual env
RUN poetry config virtualenvs.create false

# Build wheel
RUN poetry build -f wheel

# Runtime stage
FROM python:3.11-slim

LABEL maintainer="Flamehaven"
LABEL description="FlashRecord - Fast screen capture and GIF recording"
LABEL version="0.3.3"

# Set working directory
WORKDIR /app

# Install runtime dependencies for screenshot capture
RUN apt-get update && apt-get install -y \
    # For Linux screenshot capture
    gnome-screenshot \
    scrot \
    imagemagick \
    # X11 dependencies
    xvfb \
    x11-utils \
    # Cleanup
    && rm -rf /var/lib/apt/lists/*

# Copy wheel from builder
COPY --from=builder /build/dist/*.whl /tmp/

# Install FlashRecord
RUN pip install --no-cache-dir /tmp/*.whl && \
    rm /tmp/*.whl

# Create output directory
RUN mkdir -p /output

# Set environment variables
ENV FLASHRECORD_SAVE_DIR=/output
ENV DISPLAY=:99

# Create entrypoint script
RUN echo '#!/bin/bash\n\
# Start Xvfb for headless screenshot capture\n\
Xvfb :99 -screen 0 1920x1080x24 &\n\
XVFB_PID=$!\n\
\n\
# Wait for Xvfb to start\n\
sleep 2\n\
\n\
# Run flashrecord\n\
flashrecord "$@"\n\
\n\
# Cleanup\n\
kill $XVFB_PID 2>/dev/null\n\
' > /usr/local/bin/docker-entrypoint.sh && \
    chmod +x /usr/local/bin/docker-entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]

# Default command (shows help)
CMD ["--help"]

# Volume for output
VOLUME ["/output"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD flashrecord --version || exit 1
