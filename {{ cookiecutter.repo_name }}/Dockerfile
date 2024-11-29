# Base image with Python 3.10 installed
FROM python:3.10

# Set the working directory
WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Copy the package code into the container
COPY src ./src
COPY data ./data
COPY setup.py ./setup.py
COPY tests ./tests
COPY requirements.txt ./requirements.txt
COPY pytest.ini ./pytest.ini
COPY tox.ini ./tox.ini
COPY README.md ./README.md
COPY pyproject.toml ./pyproject.toml

# Install package requirements
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8001

# Set environment variables
ENV DD_ENV=dev
ENV DEBUG=True
ENV LOG_LVL=INFO
ENV ENV_STATE=INFO
ENV DD_LOGS_INJECTION=true

# Run the application with Datadog tracing
CMD ["ddtrace-run", "uvicorn", "src.interface.wsgi.app:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "4"]
