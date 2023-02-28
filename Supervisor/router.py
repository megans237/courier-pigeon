import os

import dotenv
import requests
from typing import List, Tuple, Dict, Union

import Common.common_datatypes as pigeon_dtype


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
        coordinates: [pigeon_dtype.Location] = None,
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

        # append coordinates to the http request url
        for loc in coordinates:
            # Reminder: Mapbox uses lon, lat
            str_coord += str(loc.lon) + "," + str(loc.lat) + ";"

        # remove the last semicolon
        str_coord = str_coord[:-1]

        # append options to the http request url
        for opt in options:
            str_opt += opt + "&"
        if len(str_opt) == 1:
            str_opt = str_opt[:-1]  # no option, remove &

        # todo: consider not using mapbox?

        # returns a url string
        str_url = self.API_URL + str_coord + "?" + str_opt + "access_token=" + token
        return str_url

    def get_waypoints(self, url: str) -> List[Dict[str, Tuple[float, float]]]:
        """Gets raw waypoint data from mapbox request URL

        doesn't do any sorting atm.

        :param url: mapbox URL to request from
        :return: waypoints from data json
        """

        # http GET request
        r = requests.get(url=url)

        # decode json into dict
        rdata = r.json()

        # extract waypoint data from rdata dict
        waypoints = rdata["waypoints"]

        # for waypoint in waypoints:
        #     print(waypoint)

        return waypoints

    def sort_waypoints(
        self, waypoints: Dict[str, Union[int, float, str]]
    ) -> List[pigeon_dtype.Location]:
        """extracts data from waypoint structs

        :param waypoints: list of Waypoints
        :return: list of Location
        """

        # create list w/length of num waypoints
        sorted_waypoints = [None] * len(waypoints)
        for waypoint in waypoints:
            # decode index and name from the waypoint dict
            idx = waypoint["waypoint_index"]
            name = waypoint["name"]

            # todo: check this works
            # decodes latitude and longitude from the waypoint dict
            lat, lon = waypoint["location"]

            # create temporary location to put into waypoints
            t_loc = pigeon_dtype.Location(lat=lat, lon=lon, tag=name)

            # todo: determine that this returns a copy of t_loc and that we aren't modifying the same t_loc over and over when we return the list
            # add temporary location to sorted waypoints list
            sorted_waypoints[idx] = t_loc

        return sorted_waypoints
