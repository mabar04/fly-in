from .hub import hub_class
from .connection import Connection_class
from .graph_modeling import Graph
from .pathfinding import Dijkstra
from .drone import Drone
from .helper_functions import zone_helper
from colorama import Fore, init, Style


class Simulation:
    def __init__(self, hubs: list[hub_class],
                 connections: list[Connection_class], drones: list[Drone],
                 start_hub: str, end_hub: str) -> None:
        self.hubs = hubs
        self.connections = connections
        self.drones = drones
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.moves = 0

    def transit(self, zone_dict: dict[str, hub_class],
                connection_dict: dict[str, Connection_class],
                help_functions: zone_helper) -> None:
        for drone in self.drones:
            if drone.status == "travelling" and drone.remaining_time > 0:
                drone.remaining_time -= 1
                if drone.remaining_time == 0:
                    connection_dict[drone.current_connection].current_drones =\
                        connection_dict[drone.current_connection].\
                        current_drones - 1
                    drone.current_connection = ""
                    drone.current_zone = drone.target
                    drone.path_index += 1
                    drone.target = ""
                    drone.target_connection = ""
                    drone.status = "waiting"
                else:
                    drone.current_zone = ""

    def update(self, zone_dict: dict[str, hub_class],
               help_functions: zone_helper) -> None:
        for drone in self.drones:

            if drone.current_zone == drone.endzone:
                drone.status = "finished"
                continue
            if drone.status == "finished" or drone.status == "travelling":
                continue
            if drone.path_index + 1 < len(drone.path):
                drone.target = drone.path[drone.path_index + 1]
                drone.target_connection = help_functions.get_connection(
                    drone.current_zone, drone.target, self.connections)

    def conflict_resolve(self, zone_dict: dict[str, hub_class],
                         connections: dict[str, Connection_class]) -> None:
        zone_counter = {
            zone: 0 for zone in zone_dict.keys()
        }
        connection_counter = {
            connection: 0 for connection in connections.keys()
        }
        for drone in self.drones:
            if drone.status == "finished" or drone.status == "travelling":
                continue
            if drone.target == "" or drone.target_connection == "":
                continue
            drone.approved = False
            if (zone_dict[drone.target].current_drones +
                    zone_counter[drone.target] <
                    zone_dict[drone.target].max_drones):
                if (connections[drone.target_connection].current_drones +
                    connection_counter[drone.target_connection] <
                        connections[drone.target_connection].
                        max_link_capacity):
                    drone.approved = True
                    zone_counter[drone.target] += 1
                    connection_counter[drone.target_connection] += 1
                    zone_counter[drone.current_zone] -= 1
                else:
                    drone.approved = False
            else:
                drone.approved = False

    def decision(self, zone_dict: dict[str, hub_class],
                 connections: dict[str, Connection_class],
                 help_functions: zone_helper) -> None:
        for drone in self.drones:
            if drone.status == "finished" or drone.status == "travelling":
                continue
            if drone.approved is True:
                zone_dict[drone.current_zone].current_drones -= 1
                zone_dict[drone.target].current_drones += 1
                connections[drone.target_connection].current_drones += 1
                drone.status = "travelling"
                drone.remaining_time = zone_dict[drone.target].cost
                drone.current_connection = drone.target_connection
                drone.target_connection = ""
                drone.approved = False
            else:
                drone.status = "waiting"

    def logging_turn(self) -> None:
        for drone in self.drones:
            drone.get_log()

    def simulate(self) -> None:
        init()
        graph = Graph(self.hubs, self.connections)
        graph_setup = graph.graph_setup()
        djikstra = Dijkstra(self.start_hub, graph_setup)
        help_functions = zone_helper()
        count = 0
        zone_dict: dict[str, hub_class] = help_functions.zonelist_to_dict(
            self.hubs)
        zone_dict[self.start_hub].max_drones = len(self.drones)
        zone_dict[self.start_hub].current_drones = len(self.drones)
        zone_dict[self.end_hub].max_drones = len(self.drones)
        connection_dict = help_functions.connectionlist_to_dict(
            self.connections)
        paths = djikstra.all_paths(self.start_hub,
                                   self.end_hub)
        i = 0
        for drone in self.drones:
            drone.path = paths[i % 2]
            drone.current_zone = self.start_hub
            drone.path_index = 0
            i += 1
        while any(drone.current_zone != self.end_hub for drone in self.drones):
            print(f"Turn {count + 1}")
            self.update(zone_dict, help_functions)
            self.conflict_resolve(zone_dict, connection_dict)
            self.decision(zone_dict, connection_dict, help_functions)
            self.transit(zone_dict, connection_dict, help_functions)
            count += 1
            self.logging_turn()
            print("\nzones:")
            for zone in self.hubs:
                drones = 0
                color = zone.color.upper()
                if color == "ORANGE":
                    my_color = "\033[38;2;255;165;0m"
                elif color == "BROWN":
                    my_color = "\033[38;2;139;69;19m"
                elif color == "LIME":
                    my_color = "\033[38;2;0;255;0m"
                elif color == "GOLD":
                    my_color = "\033[38;2;255;215;0m"
                elif color == "MAROON":
                    my_color = "\033[38;2;128;0;0m"
                elif color == "DARKRED":
                    my_color = "\033[38;2;139;0;0m"
                elif color == "VIOLET":
                    my_color = "\033[38;2;138;43;226m"
                elif color == "CRIMSON":
                    my_color = "\033[38;2;220;20;60m"
                elif color == "RAINBOW":
                    my_color = "\033[38;2;255;0;200m"
                else:
                    if color == "PURPLE":
                        color = "MAGENTA"
                    my_color = getattr(Fore, color)
                print(my_color + f"\t{zone.label}: ", end="")
                for drone in self.drones:
                    if drone.current_zone == zone.label:
                        print(drone.id, end=" ")
                        drones += 1
                if drones == 0:
                    print("empty", end="")
                print()
                print(Style.RESET_ALL, end="")
            print()
        print(f"Total turns: {count}")
