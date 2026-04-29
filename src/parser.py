from typing import TextIO
from .hub import hub_class
from .connection import Connection_class

class Parsing_class():
    def basic_parsing(cls, file: TextIO):
        from . import Parsing_Errors
        linecount = 1
        nb_drones = 0
        count_hubs = 0
        count_connections = 0
        hubs = {}
        connections = {}
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

    def hub_parsing(cls, hubs: dict) -> list[hub_class]:
        hub_list = []
        for k, v in hubs.items():
            name = k
            coord, meta= v.split("[")
            meta = meta.strip("]")
            label, x, y = coord.strip(" ").split(" ")
            hub_inst = hub_class(name, label, (x,y), meta)
            hub_list.append(hub_inst)
        return hub_list

    def connection_parsing(cls, connections: dict):
        connection_list = []
        for k,v in connections.items():
            start, end = v.strip().split("-")
            con = Connection_class(k, start, end)
            connection_list.append(con)
        return connection_list