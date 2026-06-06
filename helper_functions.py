from connection import Connection_class
from hub import hub_class


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

    def connectionlist_to_dict(self,
                               connections:
                               list[Connection_class])\
            -> dict[str, Connection_class]:
        connection_dict: dict[str, Connection_class] = {}
        for connection in connections:
            connection_dict[connection.name] = connection
        return connection_dict

    def connection_has_space(self, current_zone: str, target_zone: str,
                             connections: list[Connection_class]) -> bool:
        for connection in connections:
            if (connection.start_zone == current_zone
                    and connection.end_zone == target_zone):
                if connection.current_drones < connection.max_link_capacity:
                    return True
                else:
                    return False
        return False

    def get_connection(self, current_zone: str, target_zone: str,
                       connections:
                       list[Connection_class]) -> str:
        for connection in connections:
            if ((connection.start_zone == current_zone
                 and connection.end_zone == target_zone)
                    or (connection.end_zone == current_zone
                        and connection.start_zone == target_zone)):
                return connection.name
        return ""

    def add_connection_link(self, current_zone: str, target_zone: str,
                            connections: list[Connection_class]) -> None:
        for connection in connections:
            if (connection.start_zone == current_zone
                    and connection.end_zone == target_zone):
                connection.current_drones += 1

    def minus_connection_link(self, current_zone: str, target_zone: str,
                              connections: list[Connection_class]) -> None:
        for connection in connections:
            if (connection.start_zone == current_zone
                    and connection.end_zone == target_zone):
                connection.current_drones -= 1
