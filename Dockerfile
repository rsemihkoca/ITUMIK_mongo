# Use an official Python runtime as the parent image
FROM python:3.10-alpine as compile-image

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV VIRTUAL_ENV=/opt/py310
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set the working directory inside the container
WORKDIR /app

# Copy the local requirements.txt to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Runtime stage
FROM compile-image as  runtime-image

WORKDIR /app

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application using Uvicorn
CMD ["python3", "main.py"]
