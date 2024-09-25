# Stage 1: Build the Python environment using an Alpine image with all build dependencies
FROM python:3.9-alpine AS build

# Install required build dependencies for Python
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    gcc \
    musl-dev \
    libxml2-dev \
    libxslt-dev \
    python3-dev

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies inside a virtual environment
RUN python3 -m venv /app/venv && \
    . /app/venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Create a minimal runtime environment
FROM python:3.9-alpine AS runtime

# Install runtime dependencies
RUN apk add --no-cache \
    libffi \
    openssl \
    libxml2 \
    libxslt

# Copy virtual environment from build stage
COPY --from=build /app/venv /app/venv

# Set the working directory inside the container
WORKDIR /app

# Copy your bot code into the container
COPY app.py .

# Ensure the virtual environment is activated and the bot runs
ENV PATH="/app/venv/bin:$PATH"

# Command to run your bot
CMD ["python", "app.py"]
