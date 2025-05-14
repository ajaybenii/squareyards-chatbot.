# Use a more complete Python image
FROM python:3.12

# Set workdir
WORKDIR /app

# Install system dependencies including TLS, DNS, certificates, etc.
RUN apt-get update && apt-get install -y \
    gcc \
    libssl-dev \
    libffi-dev \
    curl \
    ca-certificates \
    gnupg \
    build-essential \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app
COPY . .

# Expose port used by uvicorn
EXPOSE 10000

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]