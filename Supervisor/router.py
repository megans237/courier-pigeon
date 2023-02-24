import dotenv
import os
import Common.common_datatypes
import requests


class Routing:
    def __init__(self):
        """Initializes the routing class with Token
        and DBG flag from .env file
        """
        dotenv.load_dotenv()
        self.TKN = os.getenv("MAPBOX_TOKEN")
        self.DBG = int(os.getenv("DEBUG"))
        self.OPT = ["source=first", "destination=last", "roundtrip=true"]
        self.API_URL = "https://api.mapbox.com/optimized-trips/v1/mapbox/driving/"

    def assemble_request(
        self,
        coordinates: [Common.Location] = None,
        options: [str] = None,
        token: str = None,
    ) -> str:
        """Assembles the routing request for a series of coordinates, options, and an access token.

        If there are no locations provided, returns no route?

        First location must be current location, last location must be final destination location.

        :param coordinates: List of Location
        :param options:
        :param token:
        :return:
        """
        # check for none inputs
        # ? is it better to use `is` or `==`
        if options is None:
            options = self.OPT
        if token is None:
            token = self.TKN

        # Init Vars
        str_coord = ""
        str_opt = ""

        for loc in coordinates:
            # FIXME: ensure that it's lat, lon not lon, lat
            str_coord += str(loc.lat) + "," + str(loc.lon) + ";"

        for opt in options:
            str_opt += opt + "&"
        if len(str_opt) == 1:
            str_opt = str_opt[:-1]  # no option, remove &

        # todo: consider not using mapbox?

        # returns a url string
        str_url = self.API_URL + str_coord + "?" + str_opt + "access_token=" + token
        return str_url

    def get_waypoints(self, url: str) -> []:
        """Gets raw waypoint data from mapbox request URL

        doesn't do any sorting atm.

        :param url: mapbox URL to request from
        :return: waypoints from data json
        """
        r = requests.get(url=url)
        rdata = r.json()
        waypoints = rdata["waypoints"]

        return waypoints

    def sort_waypoints(
        self, waypoints: [(float, float)]
    ) -> [Common.common_datatypes.Location]:
        """extracts data from waypoint structs

        :param waypoints: list of Waypoints
        :return: list of Location
        """
        sorted_waypoints = [None] * len(waypoints)
        for waypoint in waypoints:
            idx = waypoint["waypoint_index"]
            name = waypoint["name"]

            # todo: check this works
            lat, lon = waypoint["location"]

            t_loc = Common.common_datatypes.Location(lat=lat, lon=lon, tag=name)
            sorted_waypoints[idx] = t_loc

        return sorted_waypoints
