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
import Supervisor.router as router
from typing import List, TypedDict


class Supervisor(Common.solace_client.SolaceClient):
    def __init__(self):
        super().__init__()
        self.topics = ["pigeon/#"]

        # TODO: make these dicts, and not arbitrarily assigned max length python lists
        self.packages: List[pigeon_dtype.Package] = [] * pigeon_dtype.PKG_MAX
        self.vehicles: List[pigeon_dtype.Vehicle] = [] * pigeon_dtype.VEH_MAX

        # TODO: some way to check for veh_no conflict (for now, just make sure that vehicles *don't* have conflicts)

        self.mapbox_router = router.Routing()

        self.wait_ack = None

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
        match topics[1]:
            case "gpsupdate":
                if self.DBG:
                    print("in case gpsupdate")

                self.gpsupdate_handler(topics=topics, payload=payload)

            case "delivery":
                if self.DBG:
                    print("in case delivery")

                if topics[4] == "ACK":
                    # don't care about acknowledgement of delivery (self generated)
                    return
                else:
                    # cares about vehicle saying they have delivered something
                    self.delivery_handler(topics=topics, payload=payload)

            case "pickup":
                if self.DBG:
                    print("in case pickup")

                if topics[4] == "ACK":
                    # don't care about acknowledgment of pickup (self generated)
                    return
                else:
                    # acknowledge that an item has been picked up.
                    self.pickup_handler(topics=topics, payload=payload)

            case "reroute":
                if self.DBG:
                    print("in case reroute")

                if topics[4] == "ACK":
                    # TODO: update vehicle route information.
                    if self.wait_ack == "reroute":
                        self.wait_ack = None
                    self.reroute_handler(topics=topics, payload=payload)
                else:
                    # don't care for self-generated re-route request
                    return

            case "request":
                if self.DBG:
                    print("in case debug")

                if topics[4] == "ACK":
                    # ignore self generated acknowledgement for pickup request
                    return
                else:
                    # handle request for new package
                    self.request_handler(topics=topics, payload=payload)

            case "logon":
                if self.DBG:
                    print("in case logon")

                if topics[4] == "ACK":
                    # ignore self generated acknowledgement for pickup request
                    return
                else:
                    # TODO: add vehicle to list of vehicles
                    self.logon_handler(topics=topics, payload=payload)

            # TODO: weather & traffic cases

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

        :param topics: pigeon / delivery / veh_no / pkg_no / update
        :param payload: (lat: float, lon: float)
        :return:
        """
        veh_no = topics[2]
        pkg_no = topics[3]
        lat, lon = payload.strip('"').split(",")

        # sets package status as delivered
        self.packages[pkg_no].pkg_status = pigeon_dtype.PackageState.DELIVERED

        for pkg in self.vehicles[veh_no].veh_payload:
            # iterate through each of the packages

            if pkg.pkg_id == pkg_no:
                # deletes the package if it matches the package number
                self.vehicles[veh_no].veh_payload.remove(pkg)

        # TODO: generate new-route, broadcast to vehicle

        # TODO: generate ACK message
        return

    def pickup_handler(self, topics: [str], payload: str):
        """Called when there is a <pickup> topic from a <vehicle> regarding a <package>

        Adds the package to the vehicle and the supervisor, marks the package as ON_DELIVERY.
        Adds package destination to re-route request, re-routes everything.

        :param topics: pigeon / pickup / veh_no / pkg_no / update
        :param payload: (lat: float, lon: float)
        :return:
        """
        return

    def reroute_handler(self, topics: [str], payload: str):
        """Ignored in a supervisor context since there cannot be anyone else other than the supervisor themselves
        broadcasting re-route messages

        :param topics: pigeon / reroute / veh_no / xxx / update
        :param payload: ???
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
        # grab vehicle information
        veh_no = topics[2]
        lat, lon = payload.strip('"').split(",")

        veh_loc = pigeon_dtype.Location(lat=lat, lon=lon)

        # check bounds
        if veh_no > pigeon_dtype.VEH_MAX:
            # TODO: reject
            return

        # add vehicle to supervisor
        self.vehicles[veh_no] = pigeon_dtype.Vehicle(veh_name="", veh_id=veh_no, veh_location=veh_loc,
                                                     veh_status=pigeon_dtype.VehicleState.WAITING)

        # generate ACK
        assembled_topic = topics[0] + "/" + topics[1] + "/" + topics[2] + "/" + topics[3] + "/" + "ACK"
        self.send_message(topic=assembled_topic)

        # generate path with N items.
        # because we use mapbox v1, we have to take only the open items and then truncate to some limit.
        # with mapbox v2, we will be able to dynamically sequence multiple vehicles to optimize routes further.
        await_destinations = []
        agiven_destinations = []
        for pkg in self.packages:
            if pkg.pkg_status == pigeon_dtype.PackageState.WAITING_FOR_PICKUP:
                await_destinations.append(pkg.pkg_location)

        # generate route and only go through first 10 points.
        agiven_destinations = self.mapbox_router.gen_route(await_destinations)
        agiven_destinations = agiven_destinations[0:10]

        # TODO: sequence vehicle
        assembled_topic = topics[0]+"/reroute/"+topics[3]+"/update"
        self.send_message(topic=assembled_topic, payload=agiven_destinations)

        self.wait_ack = "reroute"

        # TODO: blocking loop for ACK

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
