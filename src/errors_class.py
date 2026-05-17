from .hub import hub_class
from .helper_functions import zone_helper
from .connection import Connection_class


class Parsing_Errors(Exception):
    def __init__(self, message: str):
        super().__init__(f"Parsing Error :{message}")


class Zone_Errors(Exception):
    def __init__(self, message: str):
        super().__init__(f"Zone Errors :{message}")


class Connection_Errors(Exception):
    def __init__(self, message: str):
        super().__init__(f"Connection Errors :{message}")


class Metadata_Errors(Exception):
    def __init__(self, message: str):
        super().__init__(f"Metadata Errors :{message}")


class PathError(Exception):
    def __init__(self, message: str):
        super().__init__(f"Path Errors :{message}")


class Check_errors:
    def __init__(self) -> None:
        self.zone_help = zone_helper()
        self.zone_names: set[str] = set()
        self.zone_connections: set[tuple[str, str]] = set()

    def metadata_check(self, value: dict[str, str]):
        for k, v in value.items():
            if '[' in v or ']' in v:
                if ("[" not in v and "]" in v) or ("[" in v and "]" not in v):
                    raise Metadata_Errors(f"Error: Incomplete metadata bracket"
                                          f" for {k}")
                _, meta = v.split("[")
                meta = meta.strip("]")
                meta_list = meta.split()
                for item in meta_list:
                    if '=' not in item:
                        raise Metadata_Errors(f"Error: Invalid metadata format"
                                              f" for {k}. Found: {item}")
                    item_sublist = item.split("=")
                    for subitem in item_sublist:
                        if subitem.strip() == "":
                            raise Metadata_Errors(f"Error: Empty metadata "
                                                  f"value in {k}. Found: "
                                                  f"{item}")
                    if not (item.startswith("zone=") or
                            item.startswith("color=")
                            or item.startswith("max_drones=") or
                            item.startswith("max_link_capacity=")):
                        raise Metadata_Errors(f"Error: Invalid metadata key in"
                                              f" {k}. Found: {item}")

    def zone_check(self, zones: list[hub_class]):
        valid_zone_types = {"normal", "blocked", "restricted", "priority"}
        start_zone, end_zone = self.zone_help.zone_count(zones)
        if start_zone != 1:
            raise Zone_Errors(f"Error: There should be exactly one start zone,"
                              f" found {start_zone}")
        if end_zone != 1:
            raise Zone_Errors(f"Error: There should be exactly one end zone, "
                              f"found {end_zone}")
        for zone in zones:
            if zone.label.count(" ") > 0 or zone.label.count("-") > 0:
                raise Zone_Errors(f"Error: Invalid zone name \"{zone.label}\"")
            if zone.label in self.zone_names:
                raise Zone_Errors(f"Error: Duplicate zone name found: "
                                  f"{zone.label}")
            self.zone_names.add(zone.label)
            if zone.max_drones < 0:
                raise Zone_Errors(f"Error: max_drones for zone {zone.label} "
                                  f"must be positive. Found: "
                                  f"{zone.max_drones}")
            if zone.zone_type not in valid_zone_types:
                raise Zone_Errors(f"Error: Invalid zone type for zone "
                                  f"{zone.label}. Found: {zone.zone_type}")

    def connection_check(self, connections: list[Connection_class]):

        for connection in connections:
            if connection.start_zone not in self.zone_names:
                raise Connection_Errors(f"Error: Connection {connection.name} "
                                        f"has invalid start zone: "
                                        f"{connection.start_zone}")
            if connection.end_zone not in self.zone_names:
                raise Connection_Errors(f"Error: Connection {connection.name} "
                                        f"has invalid end zone: "
                                        f"{connection.end_zone}")
            connection_tuple_normal = (connection.start_zone,
                                       connection.end_zone)
            connection_tuple_reverse = (connection.end_zone,
                                        connection.start_zone)
            if (connection_tuple_normal in self.zone_connections
                    or connection_tuple_reverse in self.zone_connections):
                raise Connection_Errors(f"Error: Duplicate connection found "
                                        f"between {connection.start_zone} and "
                                        f"{connection.end_zone}")
            self.zone_connections.add(connection_tuple_normal)
            if connection.max_link_capacity < 1:
                raise Connection_Errors(f"Error: max_link_capacity for "
                                        f"connection {connection.name} must be"
                                        f" at least 1. Found: "
                                        f"{connection.max_link_capacity}")
