from .hub import hub_class
from .connection import Connection_class
from .graph_modeling import Graph
from .pathfinding import Dijkstra
from .drone import Drone
from .helper_functions import zone_helper

class Simulation:
    def __init__(self, hubs: list[hub_class], connections: list[Connection_class], drones: list[Drone], start_hub: str, end_hub: str) -> None:
        self.hubs = hubs
        self.connections = connections
        self.drones = drones
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.moves = 0

    def transit(self, zone_dict: dict[str, hub_class], help_functions: zone_helper) -> None:
        for drone in self.drones:
            if drone.status == "travelling":
                if drone.remaining_time == 0:
                    drone.current_connection = ""
                    drone.current_zone = drone.target
                    drone.target_connection = ""
                    drone.path_index += 1


    def update(self, zone_dict: dict[str, hub_class], help_functions: zone_helper) -> None:
        for drone in self.drones:
            if drone.current_zone == drone.endzone:
                drone.status = "finished"
                continue
            if drone.path_index + 1 < len(drone.path):
                drone.target = drone.path[drone.path_index + 1]
                drone.target_connection = help_functions.get_connection(drone.current_zone, drone.target)

    def conflict_resolve(self) -> None:
        pass

    def decision(self) -> None:
        # for drone in self.drones:
            #     if drone.status == "finished":
            #         continue
            #     if drone.status == "moving":
            #         zone_dict[drone.current_zone].current_drones -= 1
            #         help_functions.minus_connection_link(drone.current_zone, drone.target, self.connections)
            #         drone.current_zone = drone.target
            #         drone.path_index += 1
            #         zone_dict[drone.current_zone].current_drones += 1
        pass
    
    def simulate(self) -> None:
        graph = Graph(self.hubs, self.connections)
        graph_setup = graph.graph_setup()
        djikstra = Dijkstra(self.start_hub, graph_setup)
        help_functions = zone_helper()
        zone_dict: dict[str, hub_class] = help_functions.zonelist_to_dict(self.hubs)
        connection_dict = help_functions.connectionlist_to_dict(self.connections)
        for drone in self.drones:
            drone.path = djikstra.find_shortest_path(self.start_hub, self.end_hub)
            drone.current_zone = self.start_hub
            drone.path_index = 0
        self.update(zone_dict, help_functions)
        for zone in zone_dict.values():
            print(zone.get_info())
        for drone in self.drones:
            print(drone.get_info())
        # while any(drone.path_index == len(drone.path) - 1 for drone in self.drones):
        #     self.update(zone_dict, help_functions)
        #     self.conflict_resolve()
        #     self.decision()
        #     self.moves += 1
            