# Use the official Python 3.10 slim image from the Docker Hub
FROM python:3.10-slim

# Install PostgreSQL dependencies and build dependencies
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

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install watchdog
RUN pip install --no-cache-dir watchdog

# Copy the Django project into the image
COPY . /scoolport

# Run migrations, collectstatic, and createsuperuser
RUN python manage.py migrate --settings=$DJANGO_SETTINGS_MODULE && \
    python manage.py collectstatic --noinput --settings=$DJANGO_SETTINGS_MODULE

# Expose the port the app runs on
EXPOSE 8000

# Command to run the server with auto-restart for code changes
CMD ["sh", "-c", "watchmedo auto-restart --directory=/scoolport/ --pattern=*.py --recursive -- python manage.py runserver 0.0.0.0:$PORT --settings=$DJANGO_SETTINGS_MODULE"]
