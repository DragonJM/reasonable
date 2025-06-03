# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy the test_app folder from your machine into the container
COPY test_app/ /app/test_app/

# Install flake8 for linting
RUN pip install flake8

# Command to run your tests when container starts
CMD ["python", "test_app/test_app.py"]
