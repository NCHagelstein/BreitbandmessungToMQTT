# BreitbandmessungToMQTT

This repository implements a Docker container that runs internet speed tests using the web tool provided by Breitbandmessung.de

The content of this repository is strongly based on shiaky's proposal here: https://community.home-assistant.io/t/automated-speedtest-with-breitbandmessung-docker-send-to-mqtt-and-read-with-node-red/544355
Instead of only publishing a subset of the results from the measurement, the whole measurement is published through MQTT.

The results of the individual measurements are sent through MQTT and can either be used by Node red as proposed by Shiaky or an MQTT sensor in home assistant can be used to collect and show the data.

Example Docker compose usage:

```yaml
version: "3.2"
services:
  breitbandmessung:
    image: spuzzd/breitbandmessung_mqtt
    container_name: breitbandmessung
    restart: unless-stopped # Recommended in case the Python script encounters an error
    volumes:
      - ./export:/app/export # This is optional
    environment:
      - MQTT_BROKER=127.0.0.1 #MQTT Broker IP - Required
      - MQTT_PORT=1883 # MQTT Broker Port - Required
      - MQTT_USERNAME=user_name # MQTT User name - Required
      - MQTT_PASSWORD=password # MQTT password for user - Required
      - INTERVALL_MINUTES=60 # Optional: Will set the measurement interval to 60 minutes. Default is 30
    privileged: True
```
