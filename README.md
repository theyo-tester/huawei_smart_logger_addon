# huawei_smart_logger_docker
Forked from https://github.com/mayberryjp/huawei_smart_logger_docker 

Use this HASS addon to monitor the smart grade Huawei SmartLogger 30000. <br>

Tested with Smartlogger with SW: V300R023C10SPC551

## Confguration
Will be done from the Addon Configuration Menu. You will need to specify
- HUAWEI_HOST: IP of the Smart Logger
- HUAWEI_USERNAME: Username to use to login into the logger. I suggest to not use the installer user because you will be logged out from the logger UI every time this addon makes a request. Create a separate user for HASS
- HUAWEI_PASSWORD: Password of the User chosen above.
- MQTT_HOST: IP of the mosquitto broker. If this also runs as an HASS Addon you can leave the default hostname: homeassistant
- MQTT_USERNAME
- MQTT_PASSWORD
- UPDATE_INTERVAL: How often should the logger be quieried. Default 60sec.

## Limitations
The actual implementation shows the aggregated values, no separate datas (for each inverter connected separately) available.
