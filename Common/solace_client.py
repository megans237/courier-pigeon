import dotenv
import os
import certifi
import paho.mqtt.client as mqtt
class SolaceClient():
    def __init__(self):
        """Initializes default client information
        """
        dotenv.load_dotenv()
        self.USR = os.getenv("SOLACE_USERNAME")
        self.PWD = os.getenv("SOLACE_PASSWORD")
        self.HST = os.getenv("SOlACE_HOST")
        self.PRT = os.getenv("SOLACE_PORT")
        self.DBG = int(os.getenv("DEBUG"))

