# Use an official Python runtime as a parent image
FROM python:3.10 as base

# Create and set the virtual environment
RUN python -m venv /opt/venvs/qtracker
ENV VIRTUAL_ENV=/opt/venvs/qtracker
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set the working directory in the Docker container
WORKDIR /quotes_tracker/

# Upgrade pip and install pip-tools
RUN python -m pip install --upgrade pip-tools

# Copy the requirements file and compile it using pip-tools
COPY requirements.in /quotes_tracker/
RUN pip-compile --generate-hashes /quotes_tracker/requirements.in --output-file /quotes_tracker/requirements.txt

# Development stage
FROM base as dev

# Install the compiled dependencies
RUN python -m pip install -r /quotes_tracker/requirements.txt

# Copy the rest of your application's code into the container
COPY . /quotes_tracker/

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Production stage
FROM base as prod

# Install gunicorn and the compiled dependencies
RUN python -m pip install -r /quotes_tracker/requirements.txt

# Copy the rest of your application's code into the container
COPY . /quotes_tracker/

# Expose port 8000
EXPOSE 8000

# Command to run the gunicorn server
CMD ["gunicorn", "quotes_tracker.wsgi:application", "--bind", "0.0.0.0:8000"]
