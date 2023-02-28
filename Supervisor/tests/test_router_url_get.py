"""test_router_url_get.py

Tries to generate a URL and get from the URL using mapbox for a unique
set of waypoints (that are kinda close to each other).

TODO:
    - add support for pytest regression
    - add multiple test cases
"""

from typing import List, Tuple

import Common.common_datatypes as pigeon_dtype
import Supervisor.router as router


def latlon_to_location(coord: Tuple[float, float], index) -> pigeon_dtype.Location:
    lat, lon = coord
    tag = "testpoint %d" % index
    new_location = pigeon_dtype.Location(lat=lat, lon=lon, tag=tag)
    return new_location


def assemble_waypoints() -> List[pigeon_dtype.Location]:
    LATLON_LIST1 = [(37.78, -122.42), (37.91, -122.45), (37.73, -122.48)]
    data_list = LATLON_LIST1

    waypoint_list = []
    for index, elem in enumerate(data_list):
        waypoint_list.append(latlon_to_location(index=index, coord=elem))
    return waypoint_list


if __name__ == "__main__":
    test_router_inst = router.Routing()
    locations = assemble_waypoints()
    url = test_router_inst.assemble_request(coordinates=locations)
    print(url)
    waypoints = test_router_inst.get_waypoints(url=url)
    # print(waypoints)
    sorted_waypoints = test_router_inst.sort_waypoints(waypoints=waypoints)
    for elem in sorted_waypoints:
        print(elem)
    print(test_router_inst.gen_route(coordinates=locations))