#!/usr/bin/python
import time
import logging
import random
import subprocess
import os
from paho.mqtt import client as mqtt_client

### Logging festlegen
logging.basicConfig(level=logging.INFO) # DEBUG, INFO, WARNING, ERROR, CRITICAL
### Einen eigenen Logging-Befehl mit Info festlegen
logMqtt = logging.getLogger("MQTT")
logger = logging.getLogger("HA_Breitbandmessung_Status")

MQTT_BROKER = os.environ.get("MQTT_BROKER")# ENV VAR
MQTT_PORT = int(os.environ.get("MQTT_PORT"))# ENV VAR

MQTT_TOPIC = os.environ.get("MQTT_TOPIC") #ENV_VAR with default
if MQTT_TOPIC is None:
    MQTT_TOPIC = "mqtt-breitbandmessung"
MQTT_USERNAME = os.environ.get("MQTT_USERNAME") #ENV VAR
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD") #ENV VAR
MQTT_CLIENT_ID = f'python-mqtt-{random.randint(0, 1000)}' # Keep this random
INTERVALL_MINUTES = int(os.environ.get("INTERVALL_MINUTES"))

if INTERVALL_MINUTES is None: #ENV_VAR with default
    INTERVALL_SECONDS = 900 # Default to 15 minutes
else:
    INTERVALL_SECONDS = 60*INTERVALL_MINUTES
### MQTT-Connect funktion
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logMqtt.info(f"Connected to MQTT Broker!")
        else:
            logMqtt.info(f"Failed to connect, return code '{rc}'")

    client = mqtt_client.Client(MQTT_CLIENT_ID)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT)
    return client

### Funktion um Programm sauber zu beenden
def exit_gracefully(signum=0, frame=None):
    logger.info('Exiting now')
#    loop.quit()
    ha_update("False")
    exit(0)

### Funktion um Status via MQTT an HomeAssistant zu senden
def ha_update(msg):
    if not client.is_connected:
        client.reconnect()
    result = client.publish(MQTT_TOPIC, msg)
    if result[0] == 0:
        logger.info(f"Send `{msg}` to topic `{MQTT_TOPIC}`")


#################
### Hauptprogramm

client = connect_mqtt()
client.loop_start()
time.sleep(1)

try:
    while True:
        logger.info(f"Messung gestartet")
        processing = subprocess.run(["docker run -v /app/export:/export/ shiaky/breitbandmessung:latest  | awk '/RESULTS >>>/{x=NR+2;next}(NR<=x){print}'"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process = str(processing.stdout.decode("utf-8"))
        download = process.split("\n",1)[0].replace("D:[", "").replace("]","")
        upload = process.split("\n",1)[1].replace("U:[", "").replace("]\n","")
        msg = '{download:' + str(download) + ', updload:' + str(upload) +'}'
        ha_update(msg)
        time.sleep(INTERVALL_SECONDS)
except KeyboardInterrupt:
    if client.is_connected:
        exit_gracefully()
    else:
        exit
