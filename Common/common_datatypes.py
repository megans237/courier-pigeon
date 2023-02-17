from dataclasses import dataclass
from enum import Enum


@dataclass
class Location:
    lat: float
    lon: float


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
    veh_payload = [Package]  # TODO: change this to use dataclass field
