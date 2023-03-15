"""supervisor.py
Updated: March 14, 2023
Author: Anthony Luo
--------------------------------------
Main Supervisor class for pigeon hackathon. Handles all of the update interrupts & calls map generation.

Errata:
-
"""
import Common.solace_client
import Common.common_datatypes as pigeon_dtype
from typing import List, TypedDict


class Supervisor(Common.solace_client.SolaceClient):
    def __init__(self):
        super().__init__()
        self.topics = ["pigeon/#"]

        # TODO: make these dicts, and not arbitrarily assigned max length python lists
        self.packages: List[pigeon_dtype.Package] = [] * pigeon_dtype.PKG_MAX
        self.vehicles: List[pigeon_dtype.Vehicle] = [] * pigeon_dtype.VEH_MAX

        # TODO: some way to check for veh_no conflict (for now, just make sure that vehicles *don't* have conflicts)

        if self.DBG:
            self.client.subscribe("#")

    def on_message(self, client, userdata, msg):
        if self.DBG:
            print(msg.topic, msg.payload.decode("utf-8"))

        # decode the input message by topic & msg
        topics = msg.topic.split("/")
        payload = msg.payload.decode("utf-8")

        # topics[0] = "pigeon"
        # type = topics[1]
        # van_no = topics[2]
        # pkg_no = topics[3]

        # TODO: update the case statements to ignore ACK updates sent from the supervisor itself
        match type:
            case "gpsupdate":
                if self.DBG:
                    print("in case gpsupdate")

                self.gpsupdate_handler(topics=topics, payload=payload)

            case "delivery":
                if self.DBG:
                    print("in case delivery")

                self.delivery_handler(topics=topics, payload=payload)

            case "pickup":
                if self.DBG:
                    print("in case pickup")

                self.pickup_handler(topics=topics, payload=payload)

            case "reroute":
                if self.DBG:
                    print("in case reroute")

                self.reroute_handler(topics=topics, payload=payload)

            case "request":
                if self.DBG:
                    print("in case debug")

                self.request_handler(topics=topics, payload=payload)

            case "logon":
                if self.DBG:
                    print("in case logon")

                self.logon_handler(topics=topics, payload=payload)

            case "weather":
                if self.DBG:
                    print("in case weather")

                self.weather_handler(topics=topics, payload=payload)

            case "traffic":
                if self.DBG:
                    print("in case traffic")

                self.traffic_handler(topics=topics, payload=payload)

    def gpsupdate_handler(self, topics: [str], payload: str):
        """Called when there is a <gpsupdate> topic from a <vehicle>.

        Updates the Location field of the respective vehicle.

        :param topics: pigeon / gpsupdate / veh_no / xxx / xxx
        :param payload: (lat: float, lon: float)
        :return:
        """
        veh_no = topics[2]

        veh_no = int(veh_no)
        lat, lon = payload.strip('"').split(",")
        self.vehicles[veh_no].update_location(float(lat), float(lon))
        return

    def delivery_handler(self, topics: [str], payload: str):
        """Called when there is a <delivery> topic from a <vehicle> with a <package>

        Marks the package as delivered, removes it from the vehicle & the supervisors list of packages

        :param topics: pigeon / delivery / veh_no / pkg_no / xxx
        :param payload: (lat: float, lon: float)
        :return:
        """
        return

    def pickup_handler(self, topics: [str], payload: str):
        """Called when there is a <pickup> topic from a <vehicle> regarding a <package>

        Adds the package to the vehicle and the supervisor, marks the package as ON_DELIVERY.
        Adds package destination to re-route request, re-routes everything.

        :param topics:
        :param payload:
        :return:
        """
        return

    def reroute_handler(self, topics: [str], payload: str):
        """Ignored in a supervisor context since there cannot be anyone else other than the supervisor themselves
        broadcasting re-route messages

        :param topics:
        :param payload:
        :return:
        """
        return

    def request_handler(self, topics: [str], payload: str):
        """Called when there is a request to pickup a package from <package>

        sequences the package in to be picked up, re-routes vehicles to enable picking up the package.

        :param topics: pigeon / request / XXX / pkg_no / (curr loc)
        :param payload: destination location (float, float)
        :return:
        """
        return

    def logon_handler(self, topics: [str], payload: str):
        """Called when there is a <logon> with <request> from a <vehicle>

        checks that the vehicle number is within bounds, and not already occupied.
        returns ACK with payload "SUCCESS" if successful

        :param topics: pigeon / logon / veh_no / XXX / req
        :param payload: current location (float, float)
        :return:
        """
        return

    def weather_handler(self, topics: [str], payload: str):
        """Called when there is a <weather> update

        Re-routes the vehicles accordingly

        :param topics: pigeon / weather / XXX / XXX / ???
        :param payload: ???
        :return:
        """
        return

    def traffic_handler(self, topics: [str], payload: str):
        """Called when there is a <traffic> update

        Re-routes the vehicles accordingly

        :param topics: pigeon / traffic / XXX / XXX / ???
        :param payload: ???
        :return:
        """
        return


if __name__ == "__main__":
    supervisor_inst = Supervisor()
    supervisor_inst.loop_forever()
