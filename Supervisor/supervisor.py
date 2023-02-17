import Common.solace_client


class Supervisor(Common.solace_client.SolaceClient):
    def __init__(self):
        super().__init__()
        self.topics = ["pigeon/#"]
    def on_message(self, client, userdata, msg):
        print("in supervisor class")
        print(msg.topic, msg.payload.decode("utf-8"))


if __name__ == "__main__":
    supervisor_inst = Supervisor()
    supervisor_inst.loop_forever()
