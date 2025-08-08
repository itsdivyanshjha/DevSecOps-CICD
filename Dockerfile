# Use an official lightweight Python image
FROM python:3.9-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# --- NEW STEP: Run tests and generate coverage report ---
RUN pytest --cov=. --cov-report=xml

# Expose the port the app runs on
EXPOSE 5000
# The command to run when the container starts
CMD ["python", "app.py"]