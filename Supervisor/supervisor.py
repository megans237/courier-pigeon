import Common.solace_client


class Supervisor(Common.solace_client.SolaceClient):
    def __init__(self):
        super().__init__()
        self.topics = ["pigeon/#"]

        self.packages = []
        self.vehicles = []

        if self.DBG:
            self.client.subscribe("#")

    def on_message(self, client, userdata, msg):

        if self.DBG:
            print(msg.topic, msg.payload.decode("utf-8"))

        # decode the input message by topic & msg
        topics = msg.topic.split("/")
        payload = msg.payload.decode("utf-8")

        # topics[0] = "pigeon"
        type = topics[1]
        if (topics[2]):
            van_no = topics[2]
        if (topics[3]):
            pkg_no = topics[3]

        match type:
            case "gpsupdate":
                if self.DBG:
                    print("in case gpsupdate")
            case "delivery":
                if self.DBG:
                    print("in case delivery")
            case "pickup":
                if self.DBG:
                    print("in case pickup")
            case "reroute":
                if self.DBG:
                    print("in case reroute")
            case "request":
                if self.DBG:
                    print("in case debug")
            case "logon":
                if self.DBG:
                    print("in case logon")
            case "weather":
                if self.DBG:
                    print("in case weather")
            case "traffic":
                if self.DBG:
                    print("in case traffic")



if __name__ == "__main__":
    supervisor_inst = Supervisor()
    supervisor_inst.loop_forever()
