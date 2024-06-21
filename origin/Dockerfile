# Use the official lightweight Python image from the Docker Hub
FROM image-registry.openshift-image-registry.svc:5000/openshift/python:3.9-ubi8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN yum update \
    && yum install -y gcc libpq-dev \
    && yum clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port Flask runs on

# Command to run the Flask application
CMD ["python", "app.py"]
