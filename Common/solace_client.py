import dotenv
import os
import certifi
import paho.mqtt.client as mqtt
class SolaceClient:
    def __init__(self):
        """Initializes default client information

        :return: connected mqtt.Client class
        """
        dotenv.load_dotenv()
        self.USR = os.getenv("SOLACE_USERNAME")
        self.PWD = os.getenv("SOLACE_PASSWORD")
        self.HOST = os.getenv("SOlACE_HOST")
        self.PORT = int(os.getenv("SOLACE_PORT"))
        self.DBG = int(os.getenv("DEBUG"))

        # connect to something somehow
        self.client = self.connect()

    def get_client(self):
        return self.client

    def loop_forever(self):
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("connecting")
        client.subscribe("pigeon/#")

        client.publish("pigeon/chirp", payload="chirp chirp")
        client.publish("pigeon/death", payload="runover by a car")

    def on_message(self, client, userdata, msg):
        print(f'Message received on topic: {msg.topic}. Message: {msg.payload.decode("utf-8")}')
    def connect(self) -> mqtt.Client:
        client = mqtt.Client()

        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.tls_set(ca_certs=certifi.where())

        client.username_pw_set(self.USR, self.PWD)

        client.connect(self.HOST, self.PORT)

        return client

if __name__=="__main__":
    solace_client = SolaceClient()

    solace_client.loop_forever()