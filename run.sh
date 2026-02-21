#!/bin/bash
set -e

CONFIG_PATH=/data/options.json

# Check if config file exists
if [ ! -f "$CONFIG_PATH" ]; then
    echo "WARNING: No configuration found at $CONFIG_PATH"
    echo "Using defaults from config.yaml"
    HUAWEI_HOST="https://192.168.1.22"
    HUAWEI_USERNAME="admin"
    HUAWEI_PASSWORD="admin"
    MQTT_HOST="homeassistant"
    MQTT_USERNAME="hassio"
    MQTT_PASSWORD="changeMe"
else
    echo "Loading configuration from $CONFIG_PATH"
   # cat $CONFIG_PATH  # ... Print the entire config file for debugging

    # Extract values from the JSON config file
    HUAWEI_HOST=$(jq -r '.HUAWEI_HOST' $CONFIG_PATH)
    HUAWEI_USERNAME=$(jq -r '.HUAWEI_USERNAME' $CONFIG_PATH)
    HUAWEI_PASSWORD=$(jq -r '.HUAWEI_PASSWORD' $CONFIG_PATH)
    MQTT_HOST=$(jq -r '.MQTT_HOST' $CONFIG_PATH)
    MQTT_USERNAME=$(jq -r '.MQTT_USERNAME' $CONFIG_PATH)
    MQTT_PASSWORD=$(jq -r '.MQTT_PASSWORD' $CONFIG_PATH)
fi

# Export as environment variables
export HUAWEI_HOST
export HUAWEI_USERNAME
export HUAWEI_PASSWORD
export MQTT_HOST
export MQTT_USERNAME
export MQTT_PASSWORD

# Debug: Print the variables before starting Python
#echo "========================================="
#echo "Environment Variables Being Passed:"
#echo "HUAWEI_HOST: $HUAWEI_HOST"
#echo "HUAWEI_USERNAME: $HUAWEI_USERNAME"
#echo "HUAWEI_PASSWORD: $HUAWEI_PASSWORD"
#echo "MQTT_HOST: $MQTT_HOST"
#echo "MQTT_USERNAME: $MQTT_USERNAME"
#echo "MQTT_PASSWORD: $MQTT_PASSWORD"
#echo "========================================="

# Run the Python application
cd /huawei_smart_logger_docker-v1.0.18
exec venv/bin/python -u huawei_smart_logger.py
