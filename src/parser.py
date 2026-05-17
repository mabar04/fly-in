from typing import Dict, TextIO, Union
from .hub import hub_class
from .connection import Connection_class
from .errors_class import Parsing_Errors

ParsedDict = Dict[str, Union[int, dict[str, str]]]


class Parsing_class():

    def is_int_string(self, s: str) -> bool:
        try:
            int(s)
            return True
        except ValueError:
            return False

    def basic_parsing(self, file: TextIO) -> ParsedDict:
        from . import Parsing_Errors
        linecount = 1
        nb_drones = 0
        count_hubs = 0
        count_connections = 0
        hubs: dict[str, str] = {}
        connections: dict[str, str] = {}
        for line in file:
            if line.startswith("#"):
                continue
            elif line.startswith("nb_drones"):
                if linecount != 1:
                    raise Parsing_Errors("File do not start with nb_drones")
                _, number = line.split(":")
                nb_drones = int(number)
                if nb_drones < 0:
                    raise Parsing_Errors("nb_drones should be positive")
            elif line.strip() == "":
                continue
            elif "hub:" in line:
                line = line.replace("\n", "")
                name, coord = line.split(":")
                if name not in ["start_hub", "end_hub"]:
                    name = name + str(count_hubs)
                    count_hubs += 1
                hubs.update({f"{name}": coord})
            elif "connection" in line:
                line = line.replace("\n", "")
                name, coord = line.split(":")
                name = name + str(count_connections)
                connections.update({f"{name}": coord})
                count_connections += 1
            linecount += 1
        return {
            "nb_drones": nb_drones,
            "hubs": hubs,
            "connections": connections
            }

    def hub_parsing(self, hubs: dict[str, str]) -> list[hub_class]:
        hub_list: list[hub_class] = []
        for k, v in hubs.items():
            name = k
            coord, meta = v.split("[")
            meta = meta.strip("]")
            label, x, y = coord.strip(" ").split(" ")
            if not self.is_int_string(x) and not self.is_int_string(y):
                raise Parsing_Errors(f"Error: Coordinates for zone {label} "
                                     f"must be numeric. Found: {x}, {y}")
            meta_list = meta.split()
            zone_type = "normal"
            color = None
            max_drones = 1
            cost = 1
            for item in meta_list:
                if item.startswith("zone="):
                    zone_type = item.split("=")[1]

                    if zone_type == "normal":
                        cost = 1
                    elif zone_type == "blocked":
                        cost = float("inf")
                    elif zone_type == "restricted":
                        cost = 2
                    elif zone_type == "priority":
                        cost = 1
                elif item.startswith("color="):
                    color = item.split("=")[1]
                elif item.startswith("max_drones="):
                    max_drones = int(item.split("=")[1])
            hub_inst = hub_class(name, label, (int(x), int(y)),
                                 max_drones, cost, zone_type, color)
            hub_list.append(hub_inst)
        return hub_list

    def connection_parsing(self, connections:
                           dict[str, str]) -> list[Connection_class]:
        connection_list: list[Connection_class] = []
        for k, v in connections.items():
            if "[" in v:
                coord, meta = v.split("[")
                meta = meta.strip("]")
                meta = int(meta.split("=")[1])
                start, end = coord.strip().split("-")
            else:
                start, end = v.strip().split("-")
                meta = 1
            con = Connection_class(k, start, end, meta)
            connection_list.append(con)
        return connection_list
