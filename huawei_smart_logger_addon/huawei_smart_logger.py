import requests
import paho.mqtt.client as mqtt
import logging
import json
import re
import time
import os
import datetime
from const import IS_CONTAINER, ENTITIES

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress SSL warnings
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Environment Variables
if IS_CONTAINER:
    HUAWEI_HOST = os.getenv("HUAWEI_HOST", "https://192.168.50.38")
    HUAWEI_PASSWORD = os.getenv("HUAWEI_PASSWORD", "")
    HUAWEI_USERNAME = os.getenv("HUAWEI_USERNAME", "admin")
    MQTT_HOST = os.getenv("MQTT_HOST", "earthquake.832-5.jp")
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
    MQTT_USERNAME = os.getenv("MQTT_USERNAME", "japan")
    UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "60"))
    VERSION = os.getenv('BUILD_VERSION')

class HuaweiSmartLoggerSensor:
    def __init__(self, name_constant):
        name_object = ENTITIES[name_constant]
        self.name = f"huawei_smart_logger_{name_constant}"
        self.device_class = name_object['type']
        self.unit_of_measurement = name_object['unit']
        self.state_class = name_object.get('attribute', 'measurement')
        self.state_topic = f"homeassistant/sensor/{self.name}/state"
        self.unique_id = self.name
        self.device = {
            "identifiers": [self.name],
            "name": f"Huawei Smart Logger For {name_constant}",
        }

    def to_json(self):
        return {
            "name": self.name,
            "device_class": self.device_class,
            "unit_of_measurement": self.unit_of_measurement,
            "state_class": self.state_class,
            "state_topic": self.state_topic,
            "unique_id": self.unique_id,
            "device": self.device
        }

def get_session_and_token():
    """Handles the login logic and returns a session and CSRF token."""
    session = requests.Session()
    login_url = f"{HUAWEI_HOST}/action/login"
    login_data = {
        'langlist': 0,
        'usrname': HUAWEI_USERNAME,
        'string': HUAWEI_PASSWORD,
        'vercodeinput': '',
        'login': 'Log+In'
    }

    try:
        # 1. Login
        session.post(login_url, data=login_data, verify=False, timeout=10)
        
        # 2. Get CSRF token
        csrf_url = f"{HUAWEI_HOST}/js/csrf.jst"
        response = session.get(csrf_url, verify=False, timeout=10)
        token_match = re.search(r'tokenObj.value = \"([^\"]+)\"', response.text)
        
        if token_match:
            return session, token_match.group(1)
        else:
            logger.error("Failed to find CSRF token in response.")
            return None, None
    except Exception as e:
        logger.error(f"Login failed: {e}")
        return None, None

def send_discovery(mqtt_client):
    """Sends MQTT discovery configs for all entities."""
    for entity in ENTITIES:
        sensor = HuaweiSmartLoggerSensor(entity)
        discovery_topic = f"homeassistant/sensor/huawei_smart_logger_{entity}/config"
        payload = json.dumps(sensor.to_json())
        mqtt_client.publish(discovery_topic, payload=payload, qos=1, retain=True)
    logger.info("MQTT Discovery sent.")

def request_and_publish(session, mqtt_client, csrf_token):
    """Fetches data and returns True if successful, False if session failed."""
    info_url = f"{HUAWEI_HOST}/get_set_page_info.asp?type=88"
    headers = {'x-csrf-token': csrf_token}

    try:
        response = session.get(info_url, headers=headers, verify=False, timeout=10)
        
        # Check if session expired (when not logged it, the info url shows 404 - not found)
        if response.status_code == 404 or response.status_code != 200:
            return False # Signal that we need to re-login

        response_lines = response.text.split('|')
        for line in response_lines:
            element = line.split('~')
            if len(element) < 8: # Ensure index 7 exists
                continue
            
            entity_raw = element[2].lower().strip()
            if entity_raw == "(null)":
                continue

            # Clean entity name for MQTT topic
            entity = re.sub(r'\'', '', entity_raw) # Delete quotes
            entity = re.sub(r'[\s/]+', '_', entity) # Spaces/Slashes to Underscore
            value = element[7]
            state_topic = f"homeassistant/sensor/huawei_smart_logger_{entity}/state"
            mqtt_client.publish(state_topic, payload=value, qos=1, retain=False)
        return True
    except Exception as e:
        logger.error(f"Data fetch error: {e}")
        return False

if __name__ == '__main__':
    logger.info(f"Starting Huawei Smart Logger Addon v{VERSION}")

    # 1. Setup Persistent MQTT Client
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    mqtt_client.connect(MQTT_HOST, 1883)
    mqtt_client.loop_start()

    send_discovery(mqtt_client)

    # 2. Setup Persistent HTTP Session
    active_session = None
    active_token = None

    while True:
        # Re-login logic if session is missing or invalid
        if active_session is None:
            logger.info("Attempting SmartLogger login...")
            active_session, active_token = get_session_and_token()

        if active_session:
            success = request_and_publish(active_session, mqtt_client, active_token)
            if not success:
                logger.warning("Session expired or fetch failed. Clearing session for retry.")
                active_session = None
                active_token = None
        
        logger.info(f"Sleeping for {UPDATE_INTERVAL} seconds...")
        time.sleep(UPDATE_INTERVAL)