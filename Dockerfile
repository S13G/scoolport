FROM python:3.10-slim

# Install PostgreSQL dependencies
# Install build dependencies
RUN apk add --no-cache postgresql-dev gcc musl-dev libffi-dev

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create a folder for the app
WORKDIR /scoolport

# Copy the requirements.txt file into the workdir
COPY requirements.txt ./

# Install the dependencies
RUN pip3 install -r requirements.txt

# Install watchdog
RUN pip3 install watchdog

# Copy the Django project into the image
COPY . /scoolport
