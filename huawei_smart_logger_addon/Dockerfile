#Use an official Python runtime as the base image
ARG CACHEBUST=1
FROM python:3.12-slim

# Set the working directory
WORKDIR /huawei_smart_logger

# Install jq for parsing JSON configuration
RUN apt-get update && apt-get install -y jq && rm -rf /var/lib/apt/lists/*

# Copy all files from addon subfolder into the container
# This replaces the 'git clone' command
COPY . /huawei_smart_logger/

# Create a virtual environment and install the dependencies
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install paho.mqtt
RUN venv/bin/pip install requests

# Ensure your run script is executable
RUN chmod a+x /huawei_smart_logger/run.sh

# Run the app via the startup script
CMD [ "/huawei_smart_logger/run.sh" ]
