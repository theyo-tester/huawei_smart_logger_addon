#Use an official Python runtime as the base image
ARG CACHEBUST=1
FROM python:3.11.7

# Set the working directory
WORKDIR /huawei_smart_logger_docker-v1.0.17

# Install jq for parsing JSON configuration
RUN apt-get update && apt-get install -y jq && rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/mayberryjp/huawei_smart_logger_docker .

# Create a virtual environment and install the dependencies
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install paho.mqtt
RUN venv/bin/pip install requests

# Copy the run script
COPY run.sh /
RUN chmod +x /run.sh

# Run the app via the startup script
CMD ["/run.sh"]
