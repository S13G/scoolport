# Use the official Python 3.10 slim image from the Docker Hub
FROM python:3.10-slim

# Install build and PostgreSQL dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev gcc libc-dev libffi-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Create a folder for the app
WORKDIR /scoolport

# Copy the requirements.txt file into the workdir
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install watchdog (assuming it's still needed)
RUN pip install --no-cache-dir watchdog

# Copy the Django project into the image
COPY . /scoolport

# Set environment variables
EXPOSE $PORT

# Command to run the server with auto-restart for code changes
CMD ["sh", "-c", "python manage.py migrate --settings=$DJANGO_SETTINGS_MODULE && \
    python manage.py collectstatic --noinput --settings=$DJANGO_SETTINGS_MODULE && \
    python manage.py createsu --settings=$DJANGO_SETTINGS_MODULE && \
    watchmedo auto-restart --directory=/scoolport/ --pattern=*.py --recursive -- python manage.py runserver 0.0.0.0:$PORT --settings=$DJANGO_SETTINGS_MODULE"]