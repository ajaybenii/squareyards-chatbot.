# Use Ubuntu 24.04 as the base image
FROM ubuntu:24.04

# Set workdir
WORKDIR /app

# Install system dependencies including Python, TLS, DNS, certificates, etc.
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-venv \
    python3.11-dev \
    python3-pip \
    gcc \
    libssl-dev \
    libffi-dev \
    curl \
    ca-certificates \
    gnupg \
    build-essential \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as the default python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Install pip
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py && rm get-pip.py

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app and CA certificate
COPY . .
COPY isrgrootx1.pem /app/isrgrootx1.pem

# Expose port used by uvicorn
EXPOSE 10000

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]