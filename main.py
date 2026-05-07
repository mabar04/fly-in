from src import Parsing_class
from src import Check_errors
from src import Drone
from src import Graph
from src import Dijkstra

def main():
    parsing = Parsing_class()
    errors = Check_errors()
    drones_list:list[Drone] = []
    hubs = []
    connections = []
    start_hub = ""
    end_hub = ""
    with open("test_file1.txt") as f:
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
    graph = Graph(hubs, connections)
    graph_setup = graph.graph_setup()
    djikstra = Dijkstra(start_hub, graph_setup)
    djikstra.find_shortest_path()
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)