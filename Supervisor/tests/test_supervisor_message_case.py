"""test_supervisor_message_case.py

Tests the message case-switch statement inside the supervisor logic by
sending a bunch of different payloads.

TODO:
    - add support for actual pytest regression
"""
import Common.solace_client as pigeon_client
import paho.mqtt.client as mqtt
import certifi


class TestSupervisorMessageCase(pigeon_client.SolaceClient):
    def __init__(self):
        self.DBG = 0
        super().__init__()
        self.topics = ["#"]

    def on_connect(self, client, userdata, flags, rc):
        """
        Function that runs when connecting.

        Should be overriden for non-default setup
        :param client:
        :param userdata:
        :param flags:
        :param rc:
        :return:
        """

        for topic in self.topics:
            client.subscribe(topic)

        client.publish("pigeon/gpsupdate/vanx/pkgx", payload="gpsupdate")
        client.publish("pigeon/delivery/vanx/pkgx", payload="delivery")
        client.publish("pigeon/pickup/vanx/pkgx", payload="pickup")
        client.publish("pigeon/reroute/vanx/pkgx", payload="reroute")
        client.publish("pigeon/request/vanx/pkgx", payload="request")
        client.publish("pigeon/logon/vanx/pkgx", payload="logon")
        client.publish("pigeon/weather/vanx/pkgx", payload="weather")
        client.publish("pigeon/traffic/vanx/pkgx", payload="traffic")


if __name__ == "__main__":
    test_supervisor_inst = TestSupervisorMessageCase()
    test_supervisor_inst.loop_forever()
