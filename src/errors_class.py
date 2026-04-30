from .hub import hub_class
from .helper_functions import zone_helper

class Parsing_Errors(Exception):
    pass

class Zone_Errors(Exception):
    pass

class Connection_Errors(Exception):
    pass

class Check_errors:
    zone_help = zone_helper()
    zone_names = set()
    zone_connections = set()
    
    def metadata_check(cls, value :hub_class | Connection_class):
        pass

    def zone_check(cls, zones: list[hub_class]):
        start_zone, end_zone = cls.zone_help.zone_count(zones)
        if start_zone != 1:
            raise Zone_Errors(f"Error: There should be exactly one start zone, found {start_zone}")
        if end_zone != 1:
            raise Zone_Errors(f"Error: There should be exactly one end zone, found {end_zone}")           
        for zone in zones:
            if zone.label.count(" ") > 0 or zone.label.count("-") > 0:
                raise Zone_Errors(f"Error: Invalid zone name \"{zone.label}\"")
            if zone.label in cls.zone_names:
                raise Zone_Errors(f"Error: Duplicate zone name found: {zone.label}")
            cls.zone_names.add(zone.label)
            x, y = map(int, zone.coord)
            if not (isinstance(x, (int)) and isinstance(y, (int))):
                raise Zone_Errors(f"Error: Coordinates for zone {zone.label} must be numeric. Found: {zone.coord}")
            if zone.max_drones < 0:
                raise Zone_Errors(f"Error: max_drones for zone {zone.label} must be positive. Found: {zone.max_drones}")
    
    def connection_check(cls, connections):
        valid_zone_types = {"normal", "blocked", "restricted", "priority"}
        for connection in connections:
            if connection.start_zone not in cls.zone_names:
                raise Connection_Errors(f"Error: Connection {connection.name} has invalid start zone: {connection.start_zone}")
            if connection.end_zone not in cls.zone_names:
                raise Connection_Errors(f"Error: Connection {connection.name} has invalid end zone: {connection.end_zone}")
            connection_tuple_normal = (connection.start_zone, connection.end_zone)
            connection_tuple_reverse = (connection.end_zone, connection.start_zone)
            if connection_tuple_normal in cls.zone_connections or connection_tuple_reverse in cls.zone_connections:
                raise Connection_Errors(f"Error: Duplicate connection found between {connection.start_zone} and {connection.end_zone}")
            cls.zone_connections.add(connection_tuple_normal)
            if connection.max_link_capacity < 0:
                raise Connection_Errors(f"Error: max_link_capacity for connection {connection.name} must be positive. Found: {connection.max_link_capacity}")