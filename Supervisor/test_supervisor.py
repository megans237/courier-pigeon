import dotenv
import os
import certifi
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    client.subscribe("pigeon/#")

    client.publish("pigeon/chirp", payload="chirp chirp")
    client.publish("pigeon/death", payload="runover by a car")


def on_message(client, userdata, msg):
    print(
        f'Message received on topic: {msg.topic}. Message: {msg.payload.decode("utf-8")}'
    )


def connect(SOLACE_USERNAME, SOLACE_PASSWORD, SOLACE_HOST, SOLACE_PORT):
    # wss only
    # client = mqtt.Client(transport="websockets")
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.tls_set(ca_certs=certifi.where())

    client.username_pw_set(SOLACE_USERNAME, SOLACE_PASSWORD)

    client.connect(SOLACE_HOST, SOLACE_PORT)
    return client


if __name__ == "__main__":
    dotenv.load_dotenv()
    DBG = int(os.getenv("DEBUG"))
    SOLACE_USERNAME = os.getenv("SOLACE_USERNAME")
    print(SOLACE_USERNAME)
    SOLACE_PASSWORD = os.getenv("SOLACE_PASSWORD")
    print(SOLACE_PASSWORD)
    SOLACE_HOST = os.getenv("SOLACE_HOST")
    print(SOLACE_HOST)
    SOLACE_PORT = int(os.getenv("SOLACE_PORT"))
    print(SOLACE_PORT)

    client = connect(SOLACE_USERNAME, SOLACE_PASSWORD, SOLACE_HOST, SOLACE_PORT)
    client.loop_forever()
