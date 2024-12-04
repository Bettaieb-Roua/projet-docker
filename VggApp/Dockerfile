# Use an official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (for TensorFlow, etc.)
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt first to cache dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Flask application into the container
COPY . .

# Copy the model file into the container
COPY vgg19_music_genre_classification.h5 /app/vgg19_music_genre_classification.h5

# Expose the port the app will run on (default is 5000)
EXPOSE 8082

# Set environment variable to indicate Flask is in production
ENV FLASK_ENV=production

# Command to run the Flask application
CMD ["python", "app.py"]
