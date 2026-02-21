#!/usr/bin/with-contenv bashio
# The line above uses the Home Assistant "Bashio" library, 
# which makes reading config options MUCH easier than raw jq.

set -e

echo "Starting Huawei Smart Logger Add-on..."

# 1. Get configuration using bashio (cleaner than raw jq)
# If these keys in your config.yaml are lowercase, use lowercase here.
HUAWEI_HOST=$(bashio::config 'HUAWEI_HOST')
HUAWEI_USERNAME=$(bashio::config 'HUAWEI_USERNAME')
HUAWEI_PASSWORD=$(bashio::config 'HUAWEI_PASSWORD')
MQTT_HOST=$(bashio::config 'MQTT_HOST')
MQTT_USERNAME=$(bashio::config 'MQTT_USERNAME')
MQTT_PASSWORD=$(bashio::config 'MQTT_PASSWORD')
UPDATE_INTERVAL=$(bashio::config 'UPDATE_INTERVAL')

# 2. Export variables so the Python script can see them
export HUAWEI_HOST
export HUAWEI_USERNAME
export HUAWEI_PASSWORD
export MQTT_HOST
export MQTT_USERNAME
export MQTT_PASSWORD
export UPDATE_INTERVAL

# 3. Run the Python application directly
# We use 'python3' because we aren't using a venv anymore.
# We use 'exec' so Python becomes PID 1 (important for clean shutdowns).
cd /share/huawei_smart_logger
exec python3 -u huawei_smart_logger.py