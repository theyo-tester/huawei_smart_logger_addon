# https://developers.home-assistant.io/docs/add-ons/configuration#add-on-dockerfile
ARG BUILD_FROM
FROM $BUILD_FROM

# Set the working directory
WORKDIR /share/huawei_smart_logger

# Use 'apk' instead of 'apt-get' (HA base images are Alpine-based)
RUN apk add --no-cache python3 py3-pip

# Copy all files from addon into the container
COPY . .

#Install dependencies directly 
# (Virtual environments are rarely used inside containers; the container IS the environment)
RUN pip install --no-cache-dir paho-mqtt requests --break-system-packages

# Ensure your run script is executable
RUN chmod a+x run.sh

# Run the app via the startup script
CMD [ "./run.sh" ]
