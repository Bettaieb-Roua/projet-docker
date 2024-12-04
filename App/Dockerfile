FROM python:3.9-slim

EXPOSE 8081

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    libssl-dev \
    libsndfile1 \
    musl-dev \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY ./requirements.txt /var/www/App/requirements.txt
RUN pip install -r /var/www/App/requirements.txt

RUN pip install --ignore-installed six watson-developer-cloud
RUN pip install soundfile
RUN pip install --upgrade tensorflow

# Set the working directory to /app
WORKDIR /app

# Copy the entire application directory into the Docker image
COPY . /app

# Copy the model (SVM.pkl) into the Docker image (assuming it's in the same directory as app.py)
COPY SVM.pkl /app/SVM.pkl

ENV NUMBA_CACHE_DIR=/tmp/numba_cache

# Create a non-root user and change ownership of the app files
RUN useradd appuser && chown -R appuser /app
USER appuser

# Command to run your app
CMD ["python", "app.py"]
