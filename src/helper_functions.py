from src.connection import Connection_class
from .hub import hub_class

class zone_helper:
    def zone_count(self, zones: list[hub_class]) -> tuple[int, int]:
        start_zone = 0
        end_zone = 0
        for zone in zones:
            if zone.name == "start_hub":
                start_zone += 1
            elif zone.name == "end_hub":
                end_zone += 1
        return start_zone, end_zone
    
    def zonelist_to_dict(self, zones: list[hub_class]) -> dict[str, hub_class]:
        zone_dict: dict[str, hub_class] = {}
        for zone in zones:
            zone_dict[zone.label] = zone
        return zone_dict
    
    def connectionlist_to_dict(self, connections: list[Connection_class]) -> dict[str, Connection_class]:
        connection_dict: dict[str, Connection_class] = {}
        for connection in connections:
            connection_dict[connection.name] = connection
        return connection_dict