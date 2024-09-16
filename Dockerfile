FROM python:3.9-alpine

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

RUN python3 manage.py migrate --settings=$DJANGO_SETTINGS_MODULE && \
    python3 manage.py collectstatic --noinput --settings=$DJANGO_SETTINGS_MODULE && \
    python3 manage.py createsu --settings=$DJANGO_SETTINGS_MODULE

CMD ["sh", "-c", "watchmedo auto-restart --directory=/scoolport/ --pattern=*.py --recursive -- python3 manage.py runserver 0.0.0.0:$PORT --settings=$DJANGO_SETTINGS_MODULE"]

