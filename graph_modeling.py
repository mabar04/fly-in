from hub import hub_class
from connection import Connection_class
from helper_functions import zone_helper


class EdgeInfo:
    def __init__(self, max_link_capacity: int, cost: float, zone_type: str)\
          -> None:
        self.max_link_capacity = max_link_capacity
        self.cost = cost
        self.zone_type = zone_type

    def get_info(self) -> dict[str, object]:
        return {
            "max_link_capacity": self.max_link_capacity,
            "cost": self.cost,
            "zone_type": self.zone_type
        }


class Graph:
    def __init__(self, zones: list[hub_class],
                 connections: list[Connection_class]) -> None:
        self.zones = zones
        self.connections = connections
        self.adjacency: dict[str, dict[str, EdgeInfo]] = {}

    def get_zones_info(self) -> list[dict[str, object]]:
        return [zone.get_info() for zone in self.zones]

    def get_connections_info(self) -> list[dict[str, object]]:
        return [connection.get_info() for connection in self.connections]

    def graph_setup(self) -> dict[str, dict[str, EdgeInfo]]:
        zone_dict = zone_helper().zonelist_to_dict(self.zones)
        for zone_2 in self.zones:
            if zone_2.zone_type != "blocked" and zone_2.max_drones > 0:
                self.adjacency[zone_2.label] = {}
        for connection in self.connections:
            zone: hub_class | None = zone_dict.get(connection.end_zone)
            if zone is not None:
                if ((zone.zone_type != "blocked" and zone.max_drones > 0) and
                        connection.start_zone in self.adjacency):
                    self.adjacency[connection.start_zone][connection.end_zone]\
                         = EdgeInfo(
                        max_link_capacity=connection.max_link_capacity,
                        cost=zone.cost,
                        zone_type=zone.zone_type
                    )

            zone_1: hub_class | None = zone_dict.get(connection.start_zone)
            if zone_1 is not None:
                if ((zone_1.zone_type != "blocked" and zone_1.max_drones > 0)
                        and connection.end_zone in self.adjacency):
                    self.adjacency[connection.end_zone][connection.start_zone]\
                        = EdgeInfo(
                        max_link_capacity=connection.max_link_capacity,
                        cost=zone_1.cost,
                        zone_type=zone_1.zone_type
                    )
        return self.adjacency
