# Pull official base image.
FROM python:3.7

# Set work directory.
WORKDIR /code

# Set environmental variables.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV DEBUG 1

# Install dependencies.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project.
COPY src .

# Add and run as non-root user.
# RUN adduser -D myuser
# USER myuser

# Run gunicorn.
CMD gunicorn website.wsgi:application --bind 0.0.0.0:$PORT