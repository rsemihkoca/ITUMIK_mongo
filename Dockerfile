# Use an official Python runtime as the parent image
FROM python:3.10-alpine as compile-image

# Set the working directory inside the container
WORKDIR /app

# Copy the local requirements.txt to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Runtime stage
FROM python:3.10-alpine as runtime-image

# Copy Python dependencies and the application from the compile-image stage
COPY --from=compile-image /root/.local /root/.local
COPY --from=compile-image /app /app

WORKDIR /app

# Set the environment variable to ensure Python output is set straight to terminal (unbuffered)
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
