from dataclasses import dataclass
from enum import Enum

PKG_MAX = 400
VEH_MAX = 20


@dataclass
class Location:
    lat: float
    lon: float
    tag: str = ""


class PackageState(Enum):
    WAITING_FOR_PICKUP = 0
    ON_ROUTE = 1
    DELIVERED = 2


@dataclass
class Package:
    pkg_name: str
    pkg_id: int
    pkg_location: Location
    pkg_status: PackageState


class VehicleState(Enum):
    WAITING = 0
    ASSIGNED = 1
    ON_ROUTE = 2
    DONE = 3


@dataclass
class Vehicle:
    veh_name: str
    veh_id: int
    veh_location: Location
    veh_status: VehicleState
    veh_payload = list[Package]  # TODO: change this to use dataclass field
    veh_route = list[Location]

    def update_location(self, lat: float, lon: float):
        Location.lat = lat
        Location.lon = lon

    def pickup_package(self, pkg: Package) -> Package:
        pkg.pkg_status = PackageState.ON_ROUTE
        self.veh_payload.append(pkg)
        self.veh_route.pop(0)
        return pkg
