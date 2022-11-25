######################################################################################################################

#                Demo de sistema de transferencia de informcacion del sistema 4us con MQTT

#                           User: 4us_client             Pass: recicle

#####################################################################################################################
import random
import time
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"

client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = '4us_client'
password = 'recicle'

######### Mensaje de ejemplo::
msg = {"msttrown":["plastico",3452],
        "lsstrown":["metal",184],
        "cnttrown":[52987,9098]}

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Conectado!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client,msg):
    msttrown = msg["msttrown"]
    lsstrown = msg["lsstrown"]
    cnttrown = msg["cnttrown"]
    topics = ["Depositado mas veces","Depositado menos veces","cantidad de residuos depositados"]
    for a in range(len(topics)):
        time.sleep(1)
        if a == 0:
            topic = topics[a]
            msg = "Se recomienda reducir la cantidad de "+str(msttrown[0])+" porque se tiro "+str(msttrown[1])+" veces"
            result = client.publish(topic,msg)
        if a == 1:
            topic = topics[a]
            msg = "El material que menos veces se deposito fue: "+str(lsstrown[0])+" Y se deposito "+str(lsstrown[1])+" veces"
            result = client.publish(topic,msg)
        if a == 2:
            topic = topics[a]
            msg = "Se depositaron "+str(cnttrown[0])+" materiales reciclables, y se devolvieron "+str(cnttrown[1])+" materiales"
            result = client.publish(topic,msg)
        else:
            pass
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client,msg)


if __name__ == '__main__':
    run()
