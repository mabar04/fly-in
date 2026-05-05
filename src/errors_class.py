from .hub import hub_class
from .helper_functions import zone_helper
from .connection import Connection_class

class Parsing_Errors(Exception):
    pass

class Zone_Errors(Exception):
    pass

class Connection_Errors(Exception):
    pass

class Metadata_Errors(Exception):
    pass

class Check_errors:
    def __init__(self) -> None:
        self.zone_help = zone_helper()
        self.zone_names: set[str] = set()
        self.zone_connections: set[tuple[str, str]] = set()

    def metadata_check(self, value :dict[str, str]):
        for k, v in value.items():
            if '[' in v or ']' in v:
                if ("[" not in v and "]" in v) or ("[" in v and "]" not in v):
                    raise Metadata_Errors(f"Error: Incomplete metadata bracket for {k}")
                _, meta = v.split("[")
                meta = meta.strip("]")
                meta_list = meta.split()
                for item in meta_list:
                    if '=' not in item:
                        raise Metadata_Errors(f"Error: Invalid metadata format for {k}. Found: {item}")
                    item_sublist = item.split("=")
                    for subitem in item_sublist:
                        if subitem.strip() == "":
                            raise Metadata_Errors(f"Error: Empty metadata value in {k}. Found: {item}")
                    if not (item.startswith("type=") or item.startswith("color=") or item.startswith("max_drones=") or item.startswith("max_link_capacity=")):
                        raise Metadata_Errors(f"Error: Invalid metadata key in {k}. Found: {item}")


    def zone_check(self, zones: list[hub_class]):
        valid_zone_types = {"normal", "blocked", "restricted", "priority"}
        start_zone, end_zone = self.zone_help.zone_count(zones)
        if start_zone != 1:
            raise Zone_Errors(f"Error: There should be exactly one start zone, found {start_zone}")
        if end_zone != 1:
            raise Zone_Errors(f"Error: There should be exactly one end zone, found {end_zone}")           
        for zone in zones:
            if zone.label.count(" ") > 0 or zone.label.count("-") > 0:
                raise Zone_Errors(f"Error: Invalid zone name \"{zone.label}\"")
            if zone.label in self.zone_names:
                raise Zone_Errors(f"Error: Duplicate zone name found: {zone.label}")
            self.zone_names.add(zone.label)
            if zone.max_drones < 0:
                raise Zone_Errors(f"Error: max_drones for zone {zone.label} must be positive. Found: {zone.max_drones}")
            if zone.zone_type not in valid_zone_types:
                raise Zone_Errors(f"Error: Invalid zone type for zone {zone.label}. Found: {zone.zone_type}")

    def connection_check(self, connections: list[Connection_class]):

        for connection in connections:
            if connection.start_zone not in self.zone_names:
                raise Connection_Errors(f"Error: Connection {connection.name} has invalid start zone: {connection.start_zone}")
            if connection.end_zone not in self.zone_names:
                raise Connection_Errors(f"Error: Connection {connection.name} has invalid end zone: {connection.end_zone}")
            connection_tuple_normal = (connection.start_zone, connection.end_zone)
            connection_tuple_reverse = (connection.end_zone, connection.start_zone)
            if connection_tuple_normal in self.zone_connections or connection_tuple_reverse in self.zone_connections:
                raise Connection_Errors(f"Error: Duplicate connection found between {connection.start_zone} and {connection.end_zone}")
            self.zone_connections.add(connection_tuple_normal)
            if connection.max_link_capacity < 1:
                raise Connection_Errors(f"Error: max_link_capacity for connection {connection.name} must be at least 1. Found: {connection.max_link_capacity}")