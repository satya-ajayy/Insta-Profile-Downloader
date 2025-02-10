# Use slim Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy only the requirements file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the application file
COPY main.py .

# Command to run the application
CMD ["python", "main.py"]
