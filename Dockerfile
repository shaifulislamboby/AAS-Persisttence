FROM python:3.8

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpcre3-dev \
    libpq-dev \
    pipenv \
    mime-support \
    postgresql-client \
    dos2unix \
    libpq-dev \
    libmariadb-dev-compat \
    libmariadb-dev \
    gcc \
&& apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Copy Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /app/
RUN pipenv install psycopg2-binary

RUN pip3 install --upgrade pip
RUN pip3 install pipenv
RUN cd /app && pipenv install

# Install Python dependencies
RUN pip install --upgrade pip && pipenv install -d --deploy

# Copy the rest of the application code
COPY . /app

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

