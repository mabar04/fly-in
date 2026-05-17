from src import Parsing_class
from src import Check_errors
from src import Drone
import sys
# from src import Graph
# from src import Dijkstra
from src import Simulation
# from src import zone_helper


def main():
    parsing = Parsing_class()
    errors = Check_errors()
    drones_list: list[Drone] = []
    hubs = []
    connections = []
    start_hub = ""
    end_hub = ""
    with open(sys.argv[1]) as f:
        d = parsing.basic_parsing(f)
    if isinstance(d["hubs"], dict):
        errors.metadata_check(d["hubs"])
        hubs = parsing.hub_parsing(d["hubs"])
        errors.zone_check(hubs)
    if isinstance(d["connections"], dict):
        errors.metadata_check(d["connections"])
        connections = parsing.connection_parsing(d["connections"])
        errors.connection_check(connections)
    for hub in hubs:
        if hub.name == "start_hub":
            start_hub = hub.label
        if hub.name == "end_hub":
            end_hub = hub.label
    if isinstance(d["nb_drones"], int):
        for i in range(0, d["nb_drones"]):
            drone_inst = Drone(f"D{i}", start_hub, end_hub)
            drones_list.append(drone_inst)
    simulation_inst = Simulation(hubs, connections, drones_list, start_hub,
                                 end_hub)
    simulation_inst.simulate()


if __name__ == "__main__":
    # try:
    #     main()
    # except Exception as e:
    #     print(e)
    main()
