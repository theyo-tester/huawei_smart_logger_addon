# huawei smart logger docker
Forked from https://github.com/mayberryjp/huawei_smart_logger_docker 

Use this HASS addon to monitor the industry grade Huawei SmartLogger 30000. <br>

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

## Note
I suggest to use a direct modbus tcp integration instead, as you already have all the hardware needed for this matter
You can find here all relevant steps and my modbus config for HomeAssistant here: https://github.com/theyo-tester/ha-smartlogger3000-modbus-config

With little configuration and adaptions, you can use it for your system.

### Why?
- Granular Data: You can access much more specific data. Every device connected to the SmartLogger can deliver unique information.
- Custom Polling: You can define different polling frequencies for different registers.
- Stability: The HTTP requests in the Add-on use an unofficial, undocumented API likely discovered via reverse engineering. A firmware update could break it instantly.
- Speed: Nothing beats Modbus for real-time data retrieval. I couldn’t achieve true real-time updates via the API, even if the “Real-time mode” in the FusionSolar app is available.



